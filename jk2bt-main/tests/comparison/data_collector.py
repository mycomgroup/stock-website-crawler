"""
tests/comparison/data_collector.py
数据收集模块

从 jk2bt 和 JQ 收集比较数据。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta
from pathlib import Path
import warnings
import json

# 导入 jk2bt API
try:
    from jk2bt.api import (
        get_price, get_bars, get_valuation,
        get_fundamentals, get_fundamentals_balance,
        get_index_stocks, get_industry_stocks,
        get_factor_values_jq,
    )
    JK2BT_AVAILABLE = True
except ImportError as e:
    JK2BT_AVAILABLE = False
    warnings.warn(f"jk2bt API 导入失败: {e}")

# 导入配置
from .config import (
    SAMPLE_STOCKS, SAMPLE_INDEXES,
    START_DATE, END_DATE,
    COMPARISON_CONFIG,
)


class DataCollector:
    """
    数据收集器

    从 jk2bt 和 JQ 收集数据进行比较。

    使用方式:
        collector = DataCollector()
        jk2bt_data = collector.collect_jk2bt_price_data()
        jq_data = collector.load_jq_data('jq_price_data.json')  # 从预先保存的数据加载
    """

    def __init__(
        self,
        sample_stocks: Optional[List[str]] = None,
        sample_indexes: Optional[List[str]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        output_dir: Optional[str] = None,
    ):
        """
        初始化数据收集器。

        Parameters
        ----------
        sample_stocks : list, optional
            样本股票列表
        sample_indexes : list, optional
            样本指数列表
        start_date : str, optional
            开始日期
        end_date : str, optional
            结束日期
        output_dir : str, optional
            数据输出目录
        """
        self.sample_stocks = sample_stocks or SAMPLE_STOCKS
        self.sample_indexes = sample_indexes or SAMPLE_INDEXES
        self.start_date = start_date or START_DATE
        self.end_date = end_date or END_DATE
        self.output_dir = Path(output_dir or COMPARISON_CONFIG["report"]["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if not JK2BT_AVAILABLE:
            warnings.warn("jk2bt API 不可用，数据收集功能受限")

    # =========================================================================
    # jk2bt 数据收集
    # =========================================================================

    def collect_jk2bt_price_data(
        self,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        收集 jk2bt 行情数据。

        Parameters
        ----------
        fields : list, optional
            要收集的字段，默认 ['open', 'high', 'low', 'close', 'volume', 'money']

        Returns
        -------
        Dict[str, DataFrame]
            每只股票的行情数据
        """
        if not JK2BT_AVAILABLE:
            raise RuntimeError("jk2bt API 不可用")

        fields = fields or COMPARISON_CONFIG["compare_fields"]["price"]

        results = {}

        for stock in self.sample_stocks:
            try:
                # 使用 get_price 获取数据
                df = get_price(
                    stock,
                    start_date=self.start_date,
                    end_date=self.end_date,
                    fields=fields,
                )

                if df is not None and not df.empty:
                    results[stock] = df

            except Exception as e:
                warnings.warn(f"收集 {stock} 行情数据失败: {e}")

        return results

    def collect_jk2bt_valuation_data(
        self,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        收集 jk2bt 估值数据。

        Parameters
        ----------
        fields : list, optional
            要收集的字段

        Returns
        -------
        Dict[str, DataFrame]
            每只股票的估值数据
        """
        if not JK2BT_AVAILABLE:
            raise RuntimeError("jk2bt API 不可用")

        fields = fields or COMPARISON_CONFIG["compare_fields"]["valuation"]

        results = {}

        for stock in self.sample_stocks:
            try:
                df = get_valuation(
                    stock,
                    start_date=self.start_date,
                    end_date=self.end_date,
                )

                if df is not None and not df.empty:
                    # 确保列名匹配
                    df = df.rename(columns={
                        'code': 'stock_code',
                        'pe_ratio': 'pe',
                        'pb_ratio': 'pb',
                        'market_cap': 'market_cap',
                        'circulating_market_cap': 'circulating_market_cap',
                        'turnover_ratio': 'turnover_ratio',
                    })
                    results[stock] = df

            except Exception as e:
                warnings.warn(f"收集 {stock} 估值数据失败: {e}")

        return results

    def collect_jk2bt_financial_data(
        self,
        stat_date: Optional[str] = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        收集 jk2bt 财务数据。

        Parameters
        ----------
        stat_date : str, optional
            财报日期

        Returns
        -------
        Dict[str, DataFrame]
            每只股票的财务数据
        """
        if not JK2BT_AVAILABLE:
            raise RuntimeError("jk2bt API 不可用")

        results = {}

        for stock in self.sample_stocks:
            try:
                # 收集资产负债表
                try:
                    balance_df = get_fundamentals_balance(
                        query=stock,
                        stat_date=stat_date,
                    )
                    if balance_df is not None and not balance_df.empty:
                        results[f"{stock}_balance"] = balance_df
                except Exception as e:
                    warnings.warn(f"收集 {stock} 资产负债表失败: {e}")

                # 收集利润表
                try:
                    income_df = get_fundamentals(
                        query=stock,
                        stat_date=stat_date,
                    )
                    if income_df is not None and not income_df.empty:
                        results[f"{stock}_income"] = income_df
                except Exception as e:
                    warnings.warn(f"收集 {stock} 利润表失败: {e}")

            except Exception as e:
                warnings.warn(f"收集 {stock} 财务数据失败: {e}")

        return results

    def collect_jk2bt_index_components(
        self,
    ) -> Dict[str, List[str]]:
        """
        收集 jk2bt 指数成分股。

        Returns
        -------
        Dict[str, List[str]]
            每个指数的成分股列表
        """
        if not JK2BT_AVAILABLE:
            raise RuntimeError("jk2bt API 不可用")

        results = {}

        for index in self.sample_indexes:
            try:
                stocks = get_index_stocks(index)
                if stocks:
                    results[index] = stocks
            except Exception as e:
                warnings.warn(f"收集 {index} 成分股失败: {e}")

        return results

    def collect_jk2bt_factor_data(
        self,
        factors: Optional[List[str]] = None,
    ) -> Dict[str, pd.DataFrame]:
        """
        收集 jk2bt 因子数据。

        Parameters
        ----------
        factors : list, optional
            因子列表

        Returns
        -------
        Dict[str, DataFrame]
            因子数据
        """
        if not JK2BT_AVAILABLE:
            raise RuntimeError("jk2bt API 不可用")

        factors = factors or ['size', 'momentum', 'volatility', 'value']

        results = {}

        try:
            # 获取因子数据
            factor_df = get_factor_values_jq(
                securities=self.sample_stocks,
                factors=factors,
                start_date=self.start_date,
                end_date=self.end_date,
            )

            if factor_df is not None and not factor_df.empty:
                for factor in factors:
                    if factor in factor_df.columns:
                        results[factor] = factor_df[[factor]]

        except Exception as e:
            warnings.warn(f"收集因子数据失败: {e}")

        return results

    # =========================================================================
    # JQ 数据处理（从预先保存的文件加载）
    # =========================================================================

    def load_jq_data(
        self,
        file_path: str,
        data_type: str = "price",
    ) -> Dict[str, pd.DataFrame]:
        """
        从文件加载 JQ 数据。

        JQ 数据需要用户预先从 JoinQuant 平台导出并保存。
        支持的格式: JSON, CSV, Pickle

        Parameters
        ----------
        file_path : str
            数据文件路径
        data_type : str
            数据类型: 'price', 'valuation', 'financial', 'component'

        Returns
        -------
        Dict[str, DataFrame]
            加载的数据
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"JQ 数据文件不存在: {file_path}")

        results = {}

        # 根据文件格式加载
        if path.suffix == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 转换为 DataFrame
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        results[key] = pd.DataFrame(value)
                    elif isinstance(value, dict):
                        results[key] = pd.DataFrame(value)

        elif path.suffix == '.csv':
            df = pd.read_csv(path, encoding='utf-8-sig')

            # 如果有 stock_code/code 列，按股票分组
            if 'stock_code' in df.columns:
                for stock, group in df.groupby('stock_code'):
                    results[stock] = group.copy()
            elif 'code' in df.columns:
                for stock, group in df.groupby('code'):
                    results[stock] = group.copy()
            else:
                results['data'] = df

        elif path.suffix in ['.pkl', '.pickle']:
            data = pd.read_pickle(path)

            if isinstance(data, dict):
                results = data
            elif isinstance(data, pd.DataFrame):
                results['data'] = data

        else:
            raise ValueError(f"不支持的文件格式: {path.suffix}")

        return results

    def load_jq_component_data(
        self,
        file_path: str,
    ) -> Dict[str, List[str]]:
        """
        加载 JQ 成分股数据。

        Parameters
        ----------
        file_path : str
            数据文件路径

        Returns
        -------
        Dict[str, List[str]]
            每个指数的成分股列表
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"JQ 成分股数据文件不存在: {file_path}")

        results = {}

        if path.suffix == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 成分股格式: {index_code: [stock_list]}
            if isinstance(data, dict):
                for index, stocks in data.items():
                    if isinstance(stocks, list):
                        results[index] = stocks

        elif path.suffix == '.csv':
            df = pd.read_csv(path, encoding='utf-8-sig')

            if 'index_code' in df.columns and 'stock_code' in df.columns:
                for index, group in df.groupby('index_code'):
                    results[index] = group['stock_code'].tolist()

        return results

    # =========================================================================
    # 数据保存
    # =========================================================================

    def save_jk2bt_data(
        self,
        data: Dict[str, pd.DataFrame],
        file_name: str,
        format: str = "pickle",
    ) -> str:
        """
        保存 jk2bt 数据到文件。

        Parameters
        ----------
        data : Dict[str, DataFrame]
            数据字典
        file_name : str
            文件名
        format : str
            保存格式: 'pickle', 'json', 'csv'

        Returns
        -------
        str
            保存的文件路径
        """
        file_path = self.output_dir / file_name

        if format == 'pickle':
            pd.to_pickle(data, file_path.with_suffix('.pkl'))
            return str(file_path.with_suffix('.pkl'))

        elif format == 'json':
            # 转换 DataFrame 为可 JSON 序列化的格式
            json_data = {}
            for key, df in data.items():
                if isinstance(df, pd.DataFrame):
                    json_data[key] = df.to_dict(orient='records')
                elif isinstance(df, list):
                    json_data[key] = df

            with open(file_path.with_suffix('.json'), 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)

            return str(file_path.with_suffix('.json'))

        elif format == 'csv':
            # 合并所有数据到一个 DataFrame
            all_dfs = []
            for key, df in data.items():
                if isinstance(df, pd.DataFrame) and not df.empty:
                    df_copy = df.copy()
                    df_copy['source_key'] = key
                    all_dfs.append(df_copy)

            if all_dfs:
                combined = pd.concat(all_dfs, ignore_index=True)
                combined.to_csv(file_path.with_suffix('.csv'), index=False, encoding='utf-8-sig')
                return str(file_path.with_suffix('.csv'))

        raise ValueError(f"不支持的格式: {format}")

    # =========================================================================
    # 数据合并与对齐
    # =========================================================================

    def align_data(
        self,
        jk2bt_data: Dict[str, pd.DataFrame],
        jq_data: Dict[str, pd.DataFrame],
        data_type: str = "price",
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        对齐 jk2bt 和 JQ 数据。

        Parameters
        ----------
        jk2bt_data : Dict[str, DataFrame]
            jk2bt 数据
        jq_data : Dict[str, DataFrame]
            JQ 数据
        data_type : str
            数据类型

        Returns
        -------
        Tuple[DataFrame, DataFrame]
            对齐后的 (jk2bt_df, jq_df)
        """
        # 合并所有股票数据
        jk2bt_all = []
        jq_all = []

        common_stocks = set(jk2bt_data.keys()) & set(jq_data.keys())

        for stock in common_stocks:
            jk2bt_df = jk2bt_data.get(stock)
            jq_df = jq_data.get(stock)

            if jk2bt_df is not None and jq_df is not None:
                # 添加股票代码列
                if 'stock_code' not in jk2bt_df.columns:
                    jk2bt_df['stock_code'] = stock
                if 'code' not in jq_df.columns:
                    jq_df['code'] = stock

                jk2bt_all.append(jk2bt_df)
                jq_all.append(jq_df)

        if not jk2bt_all or not jq_all:
            return pd.DataFrame(), pd.DataFrame()

        # 合并
        jk2bt_combined = pd.concat(jk2bt_all, ignore_index=True)
        jq_combined = pd.concat(jq_all, ignore_index=True)

        # 对齐日期/时间索引
        if 'date' in jk2bt_combined.columns and 'date' in jq_combined.columns:
            # 确保日期格式一致
            jk2bt_combined['date'] = pd.to_datetime(jk2bt_combined['date'])
            jq_combined['date'] = pd.to_datetime(jq_combined['date'])

            # 对齐日期范围
            common_dates = set(jk2bt_combined['date']) & set(jq_combined['date'])

            jk2bt_combined = jk2bt_combined[jk2bt_combined['date'].isin(common_dates)]
            jq_combined = jq_combined[jq_combined['date'].isin(common_dates)]

        return jk2bt_combined, jq_combined

    def prepare_comparison_data(
        self,
        data_type: str = "price",
        jq_data_path: Optional[str] = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        准备比较数据。

        Parameters
        ----------
        data_type : str
            数据类型: 'price', 'valuation', 'financial', 'component'
        jq_data_path : str, optional
            JQ 数据文件路径

        Returns
        -------
        Tuple[DataFrame, DataFrame]
            (jk2bt_df, jq_df)
        """
        # 收集 jk2bt 数据
        if data_type == "price":
            jk2bt_data = self.collect_jk2bt_price_data()
        elif data_type == "valuation":
            jk2bt_data = self.collect_jk2bt_valuation_data()
        elif data_type == "financial":
            jk2bt_data = self.collect_jk2bt_financial_data()
        elif data_type == "component":
            jk2bt_data = self.collect_jk2bt_index_components()
        else:
            raise ValueError(f"不支持的数据类型: {data_type}")

        # 加载 JQ 数据
        if jq_data_path:
            jq_data = self.load_jq_data(jq_data_path, data_type)
        else:
            # 如果没有 JQ 数据文件，返回空 DataFrame
            warnings.warn("未提供 JQ 数据文件路径，将使用 jk2bt 数据作为参考")
            jq_data = {}

        # 对齐数据
        if data_type == "component":
            # 成分股比较返回字典
            return jk2bt_data, jq_data

        return self.align_data(jk2bt_data, jq_data, data_type)

    # =========================================================================
    # 数据验证
    # =========================================================================

    def validate_data(
        self,
        data: pd.DataFrame,
        required_fields: List[str],
    ) -> Tuple[bool, List[str]]:
        """
        验证数据完整性。

        Parameters
        ----------
        data : DataFrame
            待验证数据
        required_fields : list
            必需字段列表

        Returns
        -------
        Tuple[bool, List[str]]
            (是否有效, 缺失字段列表)
        """
        if data is None or data.empty:
            return False, required_fields

        missing_fields = [f for f in required_fields if f not in data.columns]

        return len(missing_fields) == 0, missing_fields

    def get_data_summary(
        self,
        data: Dict[str, pd.DataFrame],
    ) -> pd.DataFrame:
        """
        获取数据摘要。

        Parameters
        ----------
        data : Dict[str, DataFrame]
            数据字典

        Returns
        -------
        DataFrame
            数据摘要
        """
        summary = []

        for key, df in data.items():
            if isinstance(df, pd.DataFrame):
                summary.append({
                    'key': key,
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': ', '.join(df.columns.tolist()[:5]) + '...' if len(df.columns) > 5 else ', '.join(df.columns),
                    'date_range': f"{df['date'].min()} ~ {df['date'].max()}" if 'date' in df.columns else 'N/A',
                    'has_nan': df.isna().any().any(),
                })
            elif isinstance(df, list):
                summary.append({
                    'key': key,
                    'rows': len(df),
                    'columns': 'list',
                    'column_names': 'N/A',
                    'date_range': 'N/A',
                    'has_nan': False,
                })

        return pd.DataFrame(summary)


def generate_jq_data_template(output_path: str) -> str:
    """
    生成 JQ 数据模板文件。

    用户可以在 JoinQuant 平台运行代码导出数据，
    然后将数据填充到模板中。

    Parameters
    ----------
    output_path : str
        输出路径

    Returns
    -------
    str
        生成的模板文件路径
    """
    template = '''# JoinQuant 数据导出脚本
# 在 JoinQuant 平台运行此脚本，将数据导出为 JSON 格式

import json
import pandas as pd
from datetime import datetime

# 样本股票列表
SAMPLE_STOCKS = [
    "600519.XSHG",  # 贵州茅台
    "601318.XSHG",  # 中国平安
    "600036.XSHG",  # 招商银行
    "000858.XSHE",  # 五粮液
    "000333.XSHE",  # 美的集团
    "002415.XSHE",  # 海康威视
    "300750.XSHE",  # 宁德时代
    "300059.XSHE",  # 东方财富
    "002230.XSHE",  # 科大讯飞
    "601398.XSHG",  # 工商银行
    "600030.XSHG",  # 中信证券
    "601899.XSHG",  # 紫金矿业
    "600028.XSHG",  # 中国石化
    "688981.XSHG",  # 中芯国际
    "688599.XSHG",  # 天合光能
]

# 时间范围
START_DATE = '2023-01-01'
END_DATE = '2024-03-31'

def export_price_data():
    """导出行情数据"""
    all_data = {}

    for stock in SAMPLE_STOCKS:
        df = get_price(
            stock,
            start_date=START_DATE,
            end_date=END_DATE,
            fields=['open', 'high', 'low', 'close', 'volume', 'money']
        )
        if df is not None and not df.empty:
            all_data[stock] = df.reset_index().to_dict(orient='records')

    return all_data

def export_valuation_data():
    """导出估值数据"""
    all_data = {}

    for stock in SAMPLE_STOCKS:
        q = query(
            valuation.code,
            valuation.date,
            valuation.pe_ratio,
            valuation.pb_ratio,
            valuation.market_cap,
            valuation.circulating_market_cap,
            valuation.turnover_ratio,
        ).filter(
            valuation.code == stock
        )
        df = get_fundamentals(q, start_date=START_DATE, end_date=END_DATE)

        if df is not None and not df.empty:
            all_data[stock] = df.to_dict(orient='records')

    return all_data

def export_index_components():
    """导出指数成分股"""
    indexes = ['000300.XSHG', '000905.XSHG', '000016.XSHG']
    components = {}

    for index in indexes:
        stocks = get_index_stocks(index)
        components[index] = stocks

    return components

# 主导出函数
def export_all_data():
    """导出所有数据"""
    data = {
        'price': export_price_data(),
        'valuation': export_valuation_data(),
        'components': export_index_components(),
        'export_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    # 保存到文件
    with open('jq_export_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("数据已导出到 jq_export_data.json")
    return data

# 运行导出
export_all_data()
'''

    # 确保目录存在
    path = Path(output_path)
    path.mkdir(parents=True, exist_ok=True)

    # 写入模板
    template_path = path / 'jq_export_template.py'
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template)

    return str(template_path)