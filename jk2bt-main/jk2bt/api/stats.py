"""
统计 API 模块

提供线性回归、Z分数、排名、因子筛选等统计工具

聚宽兼容风格
"""

import pandas as pd
import numpy as np
from typing import Union, List, Dict, Optional
import warnings
from scipy import stats
from datetime import datetime, timedelta


# =====================================================================
# get_ols - 线性回归OLS计算
# =====================================================================

def get_ols(
    x: Union[pd.Series, np.ndarray, list],
    y: Union[pd.Series, np.ndarray, list],
    method: str = 'linear'
) -> Dict[str, float]:
    """
    线性回归OLS计算

    使用普通最小二乘法计算线性或对数回归

    参数:
        x: 自变量 (Series/array/list)
        y: 因变量 (Series/array/list)
        method: 回归方法
            - 'linear': 线性回归 y = alpha + beta * x (默认)
            - 'log': 对数回归 y = alpha + beta * log(x)

    返回:
        Dict，包含:
        - 'beta': 斜率
        - 'alpha': 截距
        - 'r_squared': R² 决定系数
        - 'residual': 残差序列 (与输入等长)
        - 'p_value': P值
        - 'std_err': 标准误差

    示例:
        # 线性回归
        result = get_ols([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])
        print(f"斜率: {result['beta']}, 截距: {result['alpha']}, R²: {result['r_squared']}")

        # 对数回归
        result = get_ols(x, y, method='log')

        # 使用 Series
        import pandas as pd
        x = pd.Series([1, 2, 3, 4, 5])
        y = pd.Series([2, 4, 5, 4, 5])
        result = get_ols(x, y)
    """
    # 转换为 numpy array
    if isinstance(x, pd.Series):
        x_values = x.values.copy()
        x_index = x.index
    else:
        x_values = np.array(x, dtype=float)
        x_index = pd.RangeIndex(len(x_values))

    if isinstance(y, pd.Series):
        y_values = y.values.copy()
    else:
        y_values = np.array(y, dtype=float)

    # 检查长度
    if len(x_values) != len(y_values):
        raise ValueError(f"x 和 y 长度不一致: x={len(x_values)}, y={len(y_values)}")

    # 移除 NaN 值
    mask = ~(np.isnan(x_values) | np.isnan(y_values))
    x_clean = x_values[mask]
    y_clean = y_values[mask]

    if len(x_clean) < 2:
        return {
            'beta': np.nan,
            'alpha': np.nan,
            'r_squared': np.nan,
            'residual': pd.Series([np.nan] * len(x_values), index=x_index),
            'p_value': np.nan,
            'std_err': np.nan
        }

    # 对数回归转换
    if method == 'log':
        # 检查 x 值是否为正
        if np.any(x_clean <= 0):
            warnings.warn("对数回归要求 x > 0，将移除非正值")
            valid_mask = x_clean > 0
            x_clean = x_clean[valid_mask]
            y_clean = y_clean[valid_mask]

            if len(x_clean) < 2:
                return {
                    'beta': np.nan,
                    'alpha': np.nan,
                    'r_squared': np.nan,
                    'residual': pd.Series([np.nan] * len(x_values), index=x_index),
                    'p_value': np.nan,
                    'std_err': np.nan
                }

        x_transformed = np.log(x_clean)
    else:
        x_transformed = x_clean

    # 使用 scipy.stats.linregress 进行线性回归
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_transformed, y_clean)

    # 计算残差
    if method == 'log':
        # 对数回归的残差需要用原始 x 值计算
        predicted = intercept + slope * np.log(np.where(x_values > 0, x_values, np.nan))
    else:
        predicted = intercept + slope * x_values

    residual = pd.Series(y_values - predicted, index=x_index)

    # R²
    r_squared = r_value ** 2

    return {
        'beta': float(slope),
        'alpha': float(intercept),
        'r_squared': float(r_squared),
        'residual': residual,
        'p_value': float(p_value),
        'std_err': float(std_err)
    }


# =====================================================================
# get_zscore - 计算Z分数
# =====================================================================

def get_zscore(
    data: Union[pd.Series, np.ndarray, list],
    window: Optional[int] = None
) -> pd.Series:
    """
    计算Z分数(标准分数)

    公式: z = (x - mean) / std

    参数:
        data: 输入数据 (Series/array/list)
        window: 滚动窗口大小
            - None: 使用全局均值和标准差 (默认)
            - int: 使用滚动窗口计算均值和标准差

    返回:
        Series，Z分数值

    示例:
        # 全局 Z 分数
        z = get_zscore([1, 2, 3, 4, 5])
        # 结果约: [-1.265, -0.632, 0, 0.632, 1.265]

        # 滚动 Z 分数 (20日)
        z = get_zscore(close_prices, window=20)

        # 使用 Series
        z = get_zscore(pd.Series([1, 2, 3, 4, 5]))
    """
    # 转换为 Series
    if isinstance(data, pd.Series):
        s = data.copy()
    else:
        s = pd.Series(data)

    if window is None:
        # 全局 Z 分数
        mean = s.mean()
        std = s.std()

        if std == 0 or np.isnan(std):
            return pd.Series([np.nan] * len(s), index=s.index)

        z = (s - mean) / std

    else:
        # 滚动 Z 分数
        rolling_mean = s.rolling(window=window, min_periods=window)
        mean = rolling_mean.mean()
        std = rolling_mean.std()

        # 避免除以零
        std = std.replace(0, np.nan)

        z = (s - mean) / std

    return z


# =====================================================================
# get_rank - 排名函数
# =====================================================================

def get_rank(
    data: Union[pd.Series, np.ndarray, list, Dict[str, float]],
    method: str = 'asc'
) -> pd.Series:
    """
    排名函数

    参数:
        data: 输入数据 (Series/array/list/dict)
        method: 排名方法
            - 'asc': 从小到大排名，最小值为1 (默认)
            - 'desc': 从大到小排名，最大值为1
            - 'pct': 百分比排名 (0-1)
            - 'dense': 密集排名，相同值排名相同且不跳过

    返回:
        Series，排名值

    示例:
        # 升序排名
        ranks = get_rank([5, 2, 8, 1, 9], method='asc')
        # 结果: [3, 2, 4, 1, 5]

        # 降序排名
        ranks = get_rank([5, 2, 8, 1, 9], method='desc')
        # 结果: [3, 4, 2, 5, 1]

        # 百分比排名
        ranks = get_rank([5, 2, 8, 1, 9], method='pct')
        # 结果: [0.6, 0.4, 0.8, 0.2, 1.0]

        # 使用字典 (股票代码映射)
        ranks = get_rank({'600519.XSHG': 100, '000858.XSHE': 200, '000001.XSHE': 150})
    """
    # 转换为 Series
    if isinstance(data, dict):
        s = pd.Series(data)
    elif isinstance(data, pd.Series):
        s = data.copy()
    else:
        s = pd.Series(data)

    # 处理 NaN 值
    valid_mask = ~s.isna()

    if not valid_mask.any():
        return pd.Series([np.nan] * len(s), index=s.index)

    # 根据方法计算排名
    if method == 'asc':
        # 升序排名，最小值为1
        ranks = s.rank(method='average', ascending=True)

    elif method == 'desc':
        # 降序排名，最大值为1
        ranks = s.rank(method='average', ascending=False)

    elif method == 'pct':
        # 百分比排名
        ranks = s.rank(method='average', ascending=True, pct=True)

    elif method == 'dense':
        # 密集排名
        ranks = s.rank(method='dense', ascending=True)

    else:
        warnings.warn(f"未知的排名方法 '{method}'，使用默认的 'asc'")
        ranks = s.rank(method='average', ascending=True)

    return ranks


# =====================================================================
# get_factor_filter_list - 因子筛选
# =====================================================================

def get_factor_filter_list(
    factor_name: str,
    threshold: Union[int, float],
    operator: str = '>',
    date: Optional[str] = None,
    stock_list: Optional[List[str]] = None,
    top_n: Optional[int] = None
) -> List[str]:
    """
    因子筛选

    根据因子值和阈值筛选股票

    参数:
        factor_name: 因子名称，支持:
            - 估值因子: PE, PB, PS, market_cap
            - 财务因子: ROE, ROA, net_profit_ratio, revenue_growth
            - 技术因子: RSI, MACD, KDJ, MA
            - 北向资金因子: north_inflow, north_holding
            - 自定义因子名称 (通过 get_factor_values_jq 获取)
        threshold: 阈值
        operator: 比较运算符
            - '>': 大于
            - '>=': 大于等于
            - '<': 小于
            - '<=': 小于等于
            - '==': 等于
            - '!=': 不等于
            - 'top': 前N只 (threshold 为数量)
            - 'bottom': 后N只 (threshold 为数量)
        date: 查询日期，格式 'YYYY-MM-DD'，默认最新
        stock_list: 待筛选股票列表，默认全市场
        top_n: 返回前N只股票

    返回:
        股票代码列表

    示例:
        # 筛选 ROE 大于 15% 的股票
        stocks = get_factor_filter_list('ROE', 15, operator='>')

        # 筛选 PE 小于 30 的股票
        stocks = get_factor_filter_list('PE', 30, operator='<')

        # 获取市值前50的股票
        stocks = get_factor_filter_list('market_cap', 50, operator='top')

        # 在指定股票池中筛选
        stocks = get_factor_filter_list('RSI', 70, operator='<', stock_list=my_stock_list)
    """
    from jk2bt.factors import get_factor_values_jq
    from jk2bt.api.indicators import RSI, MACD, KDJ

    # 获取股票列表
    if stock_list is None:
        try:
            from jk2bt.market_data import get_all_securities
            stock_list = get_all_securities(date=date)
            if isinstance(stock_list, pd.DataFrame):
                stock_list = stock_list.index.tolist()
        except Exception:
            # 默认使用沪深300成分股
            try:
                from jk2bt.market_data import get_index_stocks
                stock_list = get_index_stocks('000300.XSHG', date=date)
            except Exception:
                stock_list = []

    if not stock_list:
        warnings.warn("无法获取股票列表")
        return []

    # 获取因子值
    factor_values = {}

    try:
        # 尝试从因子库获取
        factor_lower = factor_name.lower()

        # 聚宽因子名称映射
        jq_factor_map = {
            'pe': 'pe_ratio',
            'pb': 'pb_ratio',
            'ps': 'ps_ratio',
            'market_cap': 'market_cap',
            'roe': 'roe',
            'roa': 'roa',
            'net_profit_ratio': 'net_profit_margin',
            'revenue_growth': 'inc_revenue_year_on_year',
        }

        jq_factor_name = jq_factor_map.get(factor_lower, factor_lower)

        result = get_factor_values_jq(
            securities=stock_list,
            factors=jq_factor_name,
            end_date=date,
            count=1,
        )

        if result and jq_factor_name in result:
            factor_values = result[jq_factor_name].iloc[-1].to_dict() if hasattr(result[jq_factor_name], 'iloc') else result[jq_factor_name]

    except Exception as e:
        warnings.warn(f"从因子库获取因子 {factor_name} 失败: {e}")

    # 如果因子库没有，尝试技术指标
    if not factor_values:
        try:
            if factor_name.upper() == 'RSI':
                for stock in stock_list:
                    try:
                        factor_values[stock] = RSI(stock, timeperiod=14, check_date=date)
                    except Exception:
                        pass

            elif factor_name.upper() == 'MACD':
                result = MACD(stock_list, check_date=date)
                if 'MACD' in result:
                    factor_values = result['MACD']

            elif factor_name.upper() == 'KDJ':
                result = KDJ(stock_list, check_date=date)
                if 'K' in result:
                    factor_values = result['K']

        except Exception as e:
            warnings.warn(f"获取技术指标 {factor_name} 失败: {e}")

    if not factor_values:
        warnings.warn(f"无法获取因子 {factor_name} 的值")
        return []

    # 转换为 Series 便于处理
    factor_series = pd.Series(factor_values)

    # 移除 NaN 值
    factor_series = factor_series.dropna()

    if factor_series.empty:
        return []

    # 根据运算符筛选
    operator = operator.strip()

    if operator == 'top':
        # 前 N 只
        n = int(threshold)
        result_list = factor_series.sort_values(ascending=False).head(n).index.tolist()

    elif operator == 'bottom':
        # 后 N 只
        n = int(threshold)
        result_list = factor_series.sort_values(ascending=True).head(n).index.tolist()

    else:
        # 条件筛选
        op_map = {
            '>': lambda x, t: x > t,
            '>=': lambda x, t: x >= t,
            '<': lambda x, t: x < t,
            '<=': lambda x, t: x <= t,
            '==': lambda x, t: x == t,
            '!=': lambda x, t: x != t,
        }

        if operator not in op_map:
            warnings.warn(f"未知的运算符 '{operator}'，使用默认的 '>'")
            operator = '>'

        mask = factor_series.apply(lambda x: op_map[operator](x, threshold))
        result_list = factor_series[mask].index.tolist()

        # 排序并取前 N
        if top_n is not None:
            result_list = factor_series[mask].sort_values(ascending=False).head(top_n).index.tolist()

    return result_list


# =====================================================================
# get_num - 数值提取工具
# =====================================================================

def get_num(
    stock: str,
    field: str,
    date: Optional[str] = None
) -> float:
    """
    数值提取工具

    从财务或行情数据中提取指定字段值

    参数:
        stock: 股票代码，如 '600519.XSHG'
        field: 字段名称，支持:
            - 行情字段: open, close, high, low, volume, money, high_limit, low_limit
            - 估值字段: pe, pb, ps, market_cap, circulation_market_cap
            - 财务字段: revenue, net_profit, total_assets, total_liability, roe, roa
            - 技术指标: ma5, ma10, ma20, rsi, macd
        date: 查询日期，格式 'YYYY-MM-DD'，默认最新

    返回:
        float，字段值

    示例:
        # 获取收盘价
        price = get_num('600519.XSHG', 'close')

        # 获取指定日期的 PE
        pe = get_num('600519.XSHG', 'pe', date='2024-01-01')

        # 获取财务数据
        roe = get_num('600519.XSHG', 'roe')
    """
    from jk2bt.api.market import get_price, history
    from jk2bt.finance_data import get_balance_sheet, get_income_statement

    # 行情数据
    market_fields = ['open', 'close', 'high', 'low', 'volume', 'money', 'high_limit', 'low_limit']

    # 估值数据
    valuation_fields = ['pe', 'pb', 'ps', 'market_cap', 'circulation_market_cap', 'total_market_cap']

    # 财务数据字段映射
    finance_field_map = {
        'revenue': 'operating_revenue',
        'net_profit': 'net_profit',
        'total_assets': 'total_assets',
        'total_liability': 'total_liabilities',
        'total_equity': 'total_equity',
        'roe': 'roe',
        'roa': 'roa',
    }

    # 技术指标
    indicator_fields = ['ma5', 'ma10', 'ma20', 'ma60', 'rsi', 'macd', 'kdj_k', 'kdj_d', 'kdj_j']

    field_lower = field.lower()

    # 1. 行情数据
    if field_lower in market_fields:
        try:
            df = get_price(
                security=stock,
                end_date=date,
                count=1,
                frequency='daily',
                fields=[field_lower]
            )

            if not df.empty:
                value = df[field_lower].iloc[-1]
                return float(value) if not pd.isna(value) else np.nan

        except Exception as e:
            warnings.warn(f"获取行情数据 {field} 失败: {e}")

    # 2. 估值数据
    elif field_lower in valuation_fields:
        try:
            from jk2bt.factors import get_factor_values_jq

            jq_field_map = {
                'pe': 'pe_ratio',
                'pb': 'pb_ratio',
                'ps': 'ps_ratio',
                'market_cap': 'market_cap',
                'circulation_market_cap': 'circulating_market_cap',
                'total_market_cap': 'market_cap',
            }

            jq_field = jq_field_map.get(field_lower, field_lower)

            result = get_factor_values_jq(
                securities=[stock],
                factors=jq_field,
                end_date=date,
                count=1,
            )

            if result and jq_field in result:
                value = result[jq_field]
                if isinstance(value, pd.DataFrame):
                    return float(value.iloc[-1, -1]) if not value.empty else np.nan
                elif isinstance(value, pd.Series):
                    return float(value.iloc[-1]) if not value.empty else np.nan
                else:
                    return float(value) if not pd.isna(value) else np.nan

        except Exception as e:
            warnings.warn(f"获取估值数据 {field} 失败: {e}")

    # 3. 财务数据
    elif field_lower in finance_field_map:
        try:
            code = stock.replace('.XSHG', '').replace('.XSHE', '')

            if field_lower in ['total_assets', 'total_liability', 'total_equity']:
                df = get_balance_sheet(code, end_date=date)
            else:
                df = get_income_statement(code, end_date=date)

            if not df.empty:
                col_name = finance_field_map[field_lower]
                if col_name in df.columns:
                    value = df[col_name].iloc[-1]
                    return float(value) if not pd.isna(value) else np.nan

        except Exception as e:
            warnings.warn(f"获取财务数据 {field} 失败: {e}")

    # 4. 技术指标
    elif field_lower in indicator_fields:
        try:
            if field_lower == 'rsi':
                from jk2bt.api.indicators import RSI
                return float(RSI(stock, timeperiod=14, check_date=date))

            elif field_lower == 'macd':
                from jk2bt.api.indicators import MACD
                result = MACD([stock], check_date=date)
                if 'MACD' in result and stock in result['MACD']:
                    return float(result['MACD'][stock])
                return np.nan

            elif field_lower.startswith('kdj'):
                from jk2bt.api.indicators import KDJ
                result = KDJ([stock], check_date=date)
                key = field_lower.replace('kdj_', '').upper()
                if key in result and stock in result[key]:
                    return float(result[key][stock])
                return np.nan

            elif field_lower.startswith('ma'):
                from jk2bt.api.indicators import MA
                window = int(field_lower.replace('ma', ''))
                result = MA([stock], timeperiod=window, check_date=date)
                if stock in result:
                    return float(result[stock])
                return np.nan

        except Exception as e:
            warnings.warn(f"获取技术指标 {field} 失败: {e}")

    # 5. 尝试从因子库获取
    else:
        try:
            from jk2bt.factors import get_factor_values_jq

            result = get_factor_values_jq(
                securities=[stock],
                factors=field_lower,
                end_date=date,
                count=1,
            )

            if result and field_lower in result:
                value = result[field_lower]
                if isinstance(value, pd.DataFrame):
                    return float(value.iloc[-1, -1]) if not value.empty else np.nan
                elif isinstance(value, pd.Series):
                    return float(value.iloc[-1]) if not value.empty else np.nan
                else:
                    return float(value) if not pd.isna(value) else np.nan

        except Exception as e:
            warnings.warn(f"获取字段 {field} 失败: {e}")

    return np.nan


# =====================================================================
# get_beta - Beta系数计算
# =====================================================================

def get_beta(
    security: Union[str, List[str]],
    benchmark: str = "000300.XSHG",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    window: int = 252,
    frequency: str = "1d",
) -> Union[float, Dict[str, float]]:
    """
    计算 Beta 系数

    聚宽兼容接口

    参数:
        security: 股票代码或股票列表
        benchmark: 基准指数，默认沪深300
        start_date: 开始日期
        end_date: 结束日期
        window: 计算窗口
        frequency: 数据频率

    返回:
        Beta 系数

    示例:
        # 获取单只股票的 Beta
        beta = get_beta('600519.XSHG', benchmark='000300.XSHG')

        # 获取多只股票的 Beta
        betas = get_beta(['600519.XSHG', '000858.XSHE'])
    """
    from jk2bt.api.market import history

    # 统一为列表
    if isinstance(security, str):
        securities = [security]
        single_security = True
    else:
        securities = list(security)
        single_security = False

    # 设置默认日期
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=window + 50)).strftime("%Y-%m-%d")

    # 获取基准收益率
    try:
        benchmark_df = history(
            count=window + 50,
            unit=frequency.replace("1", ""),
            field="close",
            security_list=[benchmark],
            end_date=end_date,
        )

        if benchmark_df.empty:
            return 1.0 if single_security else {sec: 1.0 for sec in securities}

        benchmark_returns = benchmark_df[benchmark].pct_change().dropna()

    except Exception:
        return 1.0 if single_security else {sec: 1.0 for sec in securities}

    result = {}

    for sec in securities:
        try:
            stock_df = history(
                count=window + 50,
                unit=frequency.replace("1", ""),
                field="close",
                security_list=[sec],
                end_date=end_date,
            )

            if stock_df.empty:
                result[sec] = 1.0
                continue

            stock_returns = stock_df[sec].pct_change().dropna()

            aligned_data = pd.DataFrame({
                "stock": stock_returns,
                "benchmark": benchmark_returns,
            }).dropna()

            if len(aligned_data) < 20:
                result[sec] = 1.0
                continue

            covariance = aligned_data["stock"].cov(aligned_data["benchmark"])
            benchmark_variance = aligned_data["benchmark"].var()

            if benchmark_variance == 0:
                result[sec] = 1.0
            else:
                result[sec] = covariance / benchmark_variance

        except Exception:
            result[sec] = 1.0

    if single_security:
        return result.get(security, 1.0)
    return result


__all__ = [
    "get_ols",
    "get_zscore",
    "get_rank",
    "get_factor_filter_list",
    "get_num",
    "get_beta",
]