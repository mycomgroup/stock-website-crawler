#!/usr/bin/env python
# coding: utf-8
"""
因子评估执行器
封装 auto_train.py 中的训练和评分逻辑
"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
from sklearn.linear_model import BayesianRidge
from sklearn.metrics import mean_squared_error, r2_score
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")

from factor_categories import calculate_diversity_score, get_factor_category
from metrics import calculate_composite_score
from config import PERIOD_CONFIG


def get_period_dates(start_date, end_date, period: str = "W"):
    """
    根据周期生成调仓日期列表

    Args:
        start_date: 开始日期
        end_date: 结束日期
        period: 周期类型，D/W/M

    Returns:
        日期列表
    """
    import datetime

    stock_data = get_price(
        "000001.XSHE", start_date, end_date, "daily", fields=["close"]
    )
    stock_data["date"] = stock_data.index

    if period == "D":
        period_stock_data = stock_data
    elif period == "W":
        period_stock_data = stock_data.resample("W", how="last")
    elif period == "M":
        period_stock_data = stock_data.resample("M", how="last")
    else:
        period_stock_data = stock_data.resample(period, how="last")

    period_stock_data = period_stock_data.set_index("date").dropna()
    date = period_stock_data.index
    pydate_array = date.to_pydatetime()
    date_only_array = np.vectorize(lambda s: s.strftime("%Y-%m-%d"))(pydate_array)
    date_only_series = pd.Series(date_only_array)
    start_date_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    start_date_dt = start_date_dt - datetime.timedelta(days=1)
    start_date_str = start_date_dt.strftime("%Y-%m-%d")
    date_list = date_only_series.values.tolist()
    date_list.insert(0, start_date_str)
    return date_list


def get_period_date(peroid=None, start_date=None, end_date=None, period: str = "W"):
    """
    获取指定周期的日期列表（兼容旧接口）

    Args:
        peroid: 旧参数名，兼容旧调用
        start_date: 开始日期
        end_date: 结束日期
        period: 周期类型，D/W/M

    Returns:
        日期列表
    """
    if peroid is not None and start_date is None:
        start_date = end_date
        end_date = peroid
        peroid = "W"
    if period is None:
        period = "W"
    return get_period_dates(start_date, end_date, period)


def delect_stop(stocks, beginDate, n=30 * 3):
    """去除上市距 beginDate 不足 n 天的股票"""
    import datetime

    stockList = []
    beginDate = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    for stock in stocks:
        start_date = get_security_info(stock).start_date
        if start_date < (beginDate - datetime.timedelta(days=n)).date():
            stockList.append(stock)
    return stockList


def get_stock(stockPool, begin_date):
    """获取股票池"""
    if stockPool == "small":
        stockList = get_index_stocks("399101.XSHE", begin_date)
        stockList = [
            stock for stock in stockList if not stock.startswith(("68", "4", "8"))
        ]

    st_data = get_extras("is_st", stockList, count=1, end_date=begin_date)
    stockList = [stock for stock in stockList if not st_data[stock][0]]
    stockList = delect_stop(stockList, begin_date)
    return stockList


def get_factor_data(securities_list, date, jqfactors_list):
    """获取因子数据"""
    factor_data = get_factor_values(
        securities=securities_list, factors=jqfactors_list, count=1, end_date=date
    )
    df_jq_factor = pd.DataFrame(index=securities_list)
    for i in factor_data.keys():
        df_jq_factor[i] = factor_data[i].iloc[0, :]
    return df_jq_factor


def fetch_data(
    jqfactors_list,
    start_date="2025-01-01",
    end_date="2024-04-15",
    train_ratio=0.66,
    period: str = "W",
):
    """
    获取训练和测试数据

    Args:
        jqfactors_list: 因子列表
        start_date: 开始日期
        end_date: 结束日期
        train_ratio: 训练集比例
        period: 周期类型，D/W/M
    """
    dateList = get_period_dates(start_date, end_date, period)
    train_length = int(len(dateList) * train_ratio)

    train_data = pd.DataFrame()
    for date in tqdm(dateList[:train_length], desc="Fetching train data"):
        try:
            stockList = get_stock("small", date)
            factor_solve_data = get_factor_data(stockList, date, jqfactors_list)
            data_close = get_price(
                stockList, date, dateList[dateList.index(date) + 1], "1d", "close"
            )["close"]
            factor_solve_data["pchg"] = data_close.iloc[-1] / data_close.iloc[1] - 1
            factor_solve_data["date"] = date
            if train_data.empty:
                train_data = factor_solve_data
            else:
                train_data = train_data.append(factor_solve_data)
        except:
            pass

    test_data = pd.DataFrame()
    for date in tqdm(dateList[train_length:-1], desc="Fetching test data"):
        try:
            stockList = get_stock("small", date)
            factor_solve_data = get_factor_data(stockList, date, jqfactors_list)
            data_close = get_price(
                stockList, date, dateList[dateList.index(date) + 1], "1d", "close"
            )["close"]
            factor_solve_data["pchg"] = data_close.iloc[-1] / data_close.iloc[1] - 1
            factor_solve_data["date"] = date
            if test_data.empty:
                test_data = factor_solve_data
            else:
                test_data = test_data.append(factor_solve_data)
        except:
            pass

    return train_data, test_data


def fill_nan_by_date(df, columns):
    """按日期分组填充 NaN"""
    df_filled = df.copy()
    for column in columns:
        df_filled[column] = df.groupby("date")[column].transform(
            lambda x: x.fillna(x.median())
        )
    return df_filled.dropna()


def evaluate_factor_combination(
    factor_combo: List[str],
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    period: str = "W",
) -> Tuple[float, Dict]:
    """
    评估单个因子组合（多指标评价）

    Args:
        factor_combo: 因子组合列表
        X_train: 训练特征
        X_test: 测试特征
        y_train: 训练标签
        y_test: 测试标签
        period: 周期类型，D/W/M

    Returns:
        (total_score, details)
    """
    X_train0 = X_train[factor_combo]
    X_test0 = X_test[factor_combo]

    model = BayesianRidge()
    model.fit(X_train0, y_train)

    predictions = np.dot(X_test0, model.coef_)

    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    X_test_copy = X_test.copy()
    X_test_copy["factor"] = predictions
    X_test_copy.rename(columns={"Unnamed: 0": "id"}, inplace=True)

    factor_df = X_test_copy.set_index(["id", "date"])["factor"].unstack(level="id")
    ret_df = X_test_copy.set_index(["id", "date"])["pchg"].unstack(level="id")

    diversity = calculate_diversity_score(factor_combo)

    metrics = calculate_composite_score(
        factor_df, ret_df, diversity, num_layers=10, period=period
    )

    category_info = {f: get_factor_category(f) for f in factor_combo}

    details = {
        "factors": factor_combo,
        "total_score": metrics["total_score"],
        "base_score": metrics["long_short_return"],
        "diversity": diversity,
        "mse": mse,
        "r2": r2,
        "coefficients": model.coef_.tolist(),
        "intercept": model.intercept_,
        "categories": category_info,
        "period": period,
        "metrics": {
            "long_short_return": metrics["long_short_return"],
            "top_sharpe": metrics["top_sharpe"],
            "ic_mean": metrics["ic_mean"],
            "icir": metrics["icir"],
            "ic_win_rate": metrics["ic_win_rate"],
            "monotonicity": metrics["monotonicity"],
            "return_volatility": metrics["return_volatility"],
            "diversity": metrics["diversity"],
            "annual_return": metrics.get("annual_return", 0),
            "max_drawdown": metrics.get("max_drawdown", 0),
        },
    }

    return metrics["total_score"], details
