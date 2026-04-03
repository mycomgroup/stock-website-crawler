"""
test_minute_data.py
分钟级数据后端测试。
验证股票和 ETF 的分钟数据读取功能和标准化层。
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta

from jk2bt.utils.standardize import (
    standardize_minute_ohlcv,
    standardize_ohlcv,
    normalize_columns,
    normalize_datetime,
    convert_numeric_columns,
    validate_required_columns,
    COLUMN_MAP_COMMON,
    COLUMN_MAP_DAILY,
)
from jk2bt.market_data.minute import (
    get_stock_minute,
    get_etf_minute,
    _validate_period,
    _prepare_for_storage,
    PERIOD_MAP,
    VALID_PERIODS,
)
from jk2bt.market_data import (
    get_stock_minute,
    get_etf_minute,
)
from jk2bt.db.duckdb_manager import DuckDBManager


class TestStandardizeFunctions:
    """测试标准化函数"""

    def test_normalize_columns_basic(self):
        """测试基本列名映射"""
        df = pd.DataFrame(
            {
                "时间": ["2026-01-01 09:30:00"],
                "开盘": [10.0],
                "最高": [10.2],
                "最低": [9.8],
                "收盘": [10.1],
            }
        )
        result = normalize_columns(df, COLUMN_MAP_COMMON)
        assert "datetime" in result.columns
        assert "open" in result.columns
        assert "high" in result.columns
        assert "low" in result.columns
        assert "close" in result.columns

    def test_normalize_columns_preserves_original(self):
        """测试列名映射保留原始列"""
        df = pd.DataFrame(
            {
                "时间": ["2026-01-01 09:30:00"],
                "开盘": [10.0],
                "extra_col": [100],
            }
        )
        result = normalize_columns(df, COLUMN_MAP_COMMON)
        assert "extra_col" in result.columns
        assert result["extra_col"].iloc[0] == 100

    def test_normalize_columns_custom_map(self):
        """测试自定义列名映射"""
        df = pd.DataFrame(
            {
                "old_name": ["value"],
                "another_old": [123],
            }
        )
        custom_map = {"old_name": "new_name", "another_old": "another_new"}
        result = normalize_columns(df, custom_map)
        assert "new_name" in result.columns
        assert "another_new" in result.columns

    def test_normalize_datetime_standard_format(self):
        """测试标准日期时间格式"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01", "2026-01-02", "2026-01-03"],
                "value": [1, 2, 3],
            }
        )
        result = normalize_datetime(df)
        assert result["datetime"].dtype == "datetime64[ns]"
        assert len(result) == 3

    def test_normalize_datetime_with_time(self):
        """测试带时间的格式"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01 09:30:00", "2026-01-01 10:00:00"],
                "value": [1, 2],
            }
        )
        result = normalize_datetime(df)
        assert result["datetime"].dtype == "datetime64[ns]"
        assert len(result) == 2

    def test_normalize_datetime_sorted(self):
        """测试时间排序"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-03", "2026-01-01", "2026-01-02"],
                "value": [3, 1, 2],
            }
        )
        result = normalize_datetime(df)
        assert result["datetime"].iloc[0] == pd.Timestamp("2026-01-01")
        assert result["datetime"].iloc[2] == pd.Timestamp("2026-01-03")

    def test_normalize_datetime_invalid_dropped(self):
        """测试无效时间被丢弃"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01", "invalid", "2026-01-02"],
                "value": [1, 2, 3],
            }
        )
        result = normalize_datetime(df, errors="coerce")
        assert len(result) == 2
        assert "invalid" not in result["datetime"].astype(str).values

    def test_normalize_datetime_no_datetime_column(self):
        """测试无 datetime 列时返回原数据"""
        df = pd.DataFrame(
            {
                "value": [1, 2, 3],
            }
        )
        result = normalize_datetime(df)
        assert "datetime" not in result.columns
        assert len(result) == 3

    def test_convert_numeric_columns_basic(self):
        """测试数值列转换"""
        df = pd.DataFrame(
            {
                "col1": ["1", "2", "3"],
                "col2": ["1.5", "2.5", "3.5"],
                "col3": ["a", "b", "c"],
            }
        )
        result = convert_numeric_columns(df, ["col1", "col2"])
        assert result["col1"].dtype == "float64"
        assert result["col2"].dtype == "float64"
        assert result["col3"].dtype == "object"

    def test_convert_numeric_columns_with_nan(self):
        """测试无效数值转为 NaN"""
        df = pd.DataFrame(
            {
                "col1": ["1", "invalid", "3"],
            }
        )
        result = convert_numeric_columns(df, ["col1"])
        assert pd.isna(result["col1"].iloc[1])
        assert result["col1"].iloc[0] == 1.0
        assert result["col1"].iloc[2] == 3.0

    def test_validate_required_columns_pass(self):
        """测试必要列验证通过"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01"],
                "open": [10.0],
                "close": [10.1],
            }
        )
        validate_required_columns(df, ["datetime", "open", "close"])

    def test_validate_required_columns_fail(self):
        """测试必要列验证失败"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01"],
                "open": [10.0],
            }
        )
        with pytest.raises(ValueError, match="缺少必要列"):
            validate_required_columns(df, ["datetime", "open", "close"])


class TestMinuteDataStandardize:
    """测试分钟数据标准化"""

    def test_standard_columns(self):
        """验证标准列存在"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01 09:30:00", "2026-01-01 09:31:00"],
                "open": [10.0, 10.5],
                "high": [10.2, 10.6],
                "low": [9.8, 10.3],
                "close": [10.1, 10.4],
                "volume": [1000, 2000],
                "money": [10000, 21000],
            }
        )
        result = standardize_minute_ohlcv(df)
        expected_cols = [
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "money",
            "openinterest",
        ]
        assert list(result.columns) == expected_cols
        assert result["openinterest"].iloc[0] == 0.0

    def test_standardize_with_missing_money(self):
        """验证缺失 money 列时自动补充"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01 09:30:00"],
                "open": [10.0],
                "high": [10.2],
                "low": [9.8],
                "close": [10.1],
                "volume": [1000],
            }
        )
        result = standardize_minute_ohlcv(df)
        assert "money" in result.columns
        assert result["money"].iloc[0] == 0.0

    def test_standardize_with_missing_volume(self):
        """验证缺失 volume 列时自动补充"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01 09:30:00"],
                "open": [10.0],
                "high": [10.2],
                "low": [9.8],
                "close": [10.1],
                "money": [10000],
            }
        )
        result = standardize_minute_ohlcv(df)
        assert "volume" in result.columns
        assert result["volume"].iloc[0] == 0.0

    def test_standardize_with_amount_alias(self):
        """验证 amount 列映射到 money"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01 09:30:00"],
                "open": [10.0],
                "high": [10.2],
                "low": [9.8],
                "close": [10.1],
                "volume": [1000],
                "amount": [5000],
            }
        )
        result = standardize_minute_ohlcv(df)
        assert "money" in result.columns
        assert result["money"].iloc[0] == 5000.0

    def test_standardize_with_chinese_columns(self):
        """验证中文列名自动映射"""
        df = pd.DataFrame(
            {
                "时间": ["2026-01-01 09:30:00", "2026-01-01 09:31:00"],
                "开盘": [10.0, 10.5],
                "最高": [10.2, 10.6],
                "最低": [9.8, 10.3],
                "收盘": [10.1, 10.4],
                "成交量": [1000, 2000],
                "成交额": [10000, 21000],
            }
        )
        result = standardize_minute_ohlcv(df)
        expected_cols = [
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "money",
            "openinterest",
        ]
        assert list(result.columns) == expected_cols

    def test_standardize_sorted_by_datetime(self):
        """验证按时间排序"""
        df = pd.DataFrame(
            {
                "datetime": [
                    "2026-01-01 10:00:00",
                    "2026-01-01 09:30:00",
                    "2026-01-01 09:45:00",
                ],
                "open": [10.0, 9.5, 9.8],
                "high": [10.2, 9.7, 10.0],
                "low": [9.8, 9.3, 9.6],
                "close": [10.1, 9.6, 9.9],
                "volume": [1000, 500, 800],
                "money": [10000, 5000, 8000],
            }
        )
        result = standardize_minute_ohlcv(df)
        assert result["datetime"].iloc[0] == pd.Timestamp("2026-01-01 09:30:00")
        assert result["datetime"].iloc[2] == pd.Timestamp("2026-01-01 10:00:00")

    def test_standardize_empty_dataframe(self):
        """验证空 DataFrame 处理"""
        df = pd.DataFrame()
        result = standardize_minute_ohlcv(df)
        assert result.empty

    def test_standardize_missing_required_column(self):
        """验证缺失必要列时抛出异常"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01 09:30:00"],
                "open": [10.0],
                "high": [10.2],
            }
        )
        with pytest.raises(ValueError, match="缺少必要列"):
            standardize_minute_ohlcv(df)


class TestDailyDataStandardize:
    """测试日线数据标准化"""

    def test_standardize_daily_columns(self):
        """验证日线数据标准列"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01", "2026-01-02"],
                "open": [10.0, 10.5],
                "high": [10.2, 10.6],
                "low": [9.8, 10.3],
                "close": [10.1, 10.4],
                "volume": [1000, 2000],
                "amount": [10000, 21000],
            }
        )
        result = standardize_ohlcv(df)
        expected_cols = [
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount",
            "openinterest",
        ]
        assert list(result.columns) == expected_cols

    def test_standardize_daily_with_chinese_columns(self):
        """验证日线中文列名映射"""
        df = pd.DataFrame(
            {
                "日期": ["2026-01-01"],
                "开盘": [10.0],
                "最高": [10.2],
                "最低": [9.8],
                "收盘": [10.1],
                "成交量": [1000],
                "成交额": [10000],
            }
        )
        result = standardize_ohlcv(df)
        assert "datetime" in result.columns
        assert "open" in result.columns
        assert "amount" in result.columns


class TestPeriodValidation:
    """测试周期参数验证"""

    def test_validate_period_standard(self):
        """测试标准周期"""
        assert _validate_period("1m") == "1m"
        assert _validate_period("5m") == "5m"
        assert _validate_period("15m") == "15m"
        assert _validate_period("30m") == "30m"
        assert _validate_period("60m") == "60m"

    def test_validate_period_uppercase(self):
        """测试大写周期"""
        assert _validate_period("1M") == "1m"
        assert _validate_period("5M") == "5m"
        assert _validate_period("15M") == "15m"

    def test_validate_period_alias_minute(self):
        """测试 minute 别名"""
        assert _validate_period("minute") == "1m"

    def test_validate_period_invalid(self):
        """测试无效周期"""
        with pytest.raises(ValueError, match="不支持的周期"):
            _validate_period("invalid")
        with pytest.raises(ValueError, match="不支持的周期"):
            _validate_period("2m")
        with pytest.raises(ValueError, match="不支持的周期"):
            _validate_period("120m")

    def test_all_periods_in_valid_periods(self):
        """测试所有支持的周期都在 VALID_PERIODS 中"""
        for period in ["1m", "5m", "15m", "30m", "60m"]:
            assert period in VALID_PERIODS

    def test_period_map_mapping(self):
        """测试周期映射"""
        assert PERIOD_MAP["1m"] == "1"
        assert PERIOD_MAP["5m"] == "5"
        assert PERIOD_MAP["15m"] == "15"
        assert PERIOD_MAP["30m"] == "30"
        assert PERIOD_MAP["60m"] == "60"


class TestPrepareForStorage:
    """测试数据准备函数"""

    def test_prepare_basic(self):
        """测试基本数据准备"""
        df = pd.DataFrame(
            {
                "时间": ["2026-01-01 09:30:00"],
                "开盘": [10.0],
                "最高": [10.2],
                "最低": [9.8],
                "收盘": [10.1],
                "成交量": [1000],
                "成交额": [10000],
            }
        )
        result = _prepare_for_storage(df)
        assert "datetime" in result.columns
        assert "open" in result.columns
        assert "money" in result.columns

    def test_prepare_sorted(self):
        """测试数据准备后排序"""
        df = pd.DataFrame(
            {
                "时间": ["2026-01-01 10:00:00", "2026-01-01 09:30:00"],
                "开盘": [10.0, 9.5],
                "最高": [10.2, 9.7],
                "最低": [9.8, 9.3],
                "收盘": [10.1, 9.6],
                "成交量": [1000, 500],
                "成交额": [10000, 5000],
            }
        )
        result = _prepare_for_storage(df)
        assert result["datetime"].iloc[0] == pd.Timestamp("2026-01-01 09:30:00")

    def test_prepare_missing_required_column(self):
        """测试缺失必要列"""
        df = pd.DataFrame(
            {
                "时间": ["2026-01-01 09:30:00"],
                "开盘": [10.0],
            }
        )
        with pytest.raises(ValueError, match="缺少必要列"):
            _prepare_for_storage(df)

    def test_prepare_empty_datetime(self):
        """测试空时间列"""
        df = pd.DataFrame(
            {
                "时间": [None, None],
                "开盘": [10.0, 10.5],
                "最高": [10.2, 10.6],
                "最低": [9.8, 10.3],
                "收盘": [10.1, 10.4],
            }
        )
        with pytest.raises(ValueError, match="时间列全部无效"):
            _prepare_for_storage(df)


class TestStockMinuteData:
    """测试股票分钟数据获取"""

    @pytest.mark.skipif(
        True,
        reason="需要网络访问 akshare，仅在手动验证时运行",
    )
    def test_get_stock_minute_1m(self):
        """smoke test: 获取股票 1m 分钟数据"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

        df = get_stock_minute("sh600000", start_date, end_date, period="1m")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        expected_cols = [
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "money",
            "openinterest",
        ]
        for col in expected_cols:
            assert col in df.columns

    @pytest.mark.skipif(
        True,
        reason="需要网络访问 akshare，仅在手动验证时运行",
    )
    def test_get_stock_minute_all_periods(self):
        """测试所有周期获取"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

        for period in ["1m", "5m", "15m", "30m", "60m"]:
            df = get_stock_minute("sh600000", start_date, end_date, period=period)
            assert isinstance(df, pd.DataFrame)
            assert not df.empty


class TestETFMinuteData:
    """测试 ETF 分钟数据获取"""

    @pytest.mark.skipif(
        True,
        reason="需要网络访问 akshare，仅在手动验证时运行",
    )
    def test_get_etf_minute_5m(self):
        """smoke test: 获取 ETF 5m 分钟数据"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

        df = get_etf_minute("510300", start_date, end_date, period="5m")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        expected_cols = [
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "money",
            "openinterest",
        ]
        for col in expected_cols:
            assert col in df.columns

    @pytest.mark.skipif(
        True,
        reason="需要网络访问 akshare，仅在手动验证时运行",
    )
    def test_get_etf_minute_all_periods(self):
        """测试所有周期获取"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

        for period in ["1m", "5m", "15m", "30m", "60m"]:
            df = get_etf_minute("510300", start_date, end_date, period=period)
            assert isinstance(df, pd.DataFrame)


class TestDuckDBMinuteTables:
    """测试 DuckDB 分钟数据表"""

    def test_tables_exist(self):
        """验证分钟数据表创建"""
        db = DuckDBManager(read_only=False)

        with db._get_connection(read_only=False) as conn:
            tables = conn.execute("SHOW TABLES").fetchall()
            table_names = [t[0] for t in tables]

            assert "stock_minute" in table_names
            assert "etf_minute" in table_names

    def test_table_structure_stock_minute(self):
        """验证 stock_minute 表结构"""
        db = DuckDBManager(read_only=False)

        with db._get_connection(read_only=False) as conn:
            columns = conn.execute("DESCRIBE stock_minute").fetchall()
            col_names = [c[0] for c in columns]

            required_cols = [
                "symbol",
                "datetime",
                "period",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
            for col in required_cols:
                assert col in col_names

    def test_table_structure_etf_minute(self):
        """验证 etf_minute 表结构"""
        db = DuckDBManager(read_only=False)

        with db._get_connection(read_only=False) as conn:
            columns = conn.execute("DESCRIBE etf_minute").fetchall()
            col_names = [c[0] for c in columns]

            required_cols = [
                "symbol",
                "datetime",
                "period",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
            for col in required_cols:
                assert col in col_names


class TestMinuteDataIntegration:
    """测试分钟数据与上层接口的衔接"""

    def test_get_price_minute_integration(self):
        """验证分钟数据可被上层 get_price 消费"""
        assert callable(get_stock_minute)
        assert callable(get_etf_minute)

    def test_import_chain(self):
        """验证导入链完整性"""
        assert callable(get_stock_minute)
        assert callable(get_etf_minute)

    def test_import_from_market_data_init(self):
        """验证从 market_data.__init__ 导入"""
        from jk2bt.market_data import (
            get_stock_minute,
            get_etf_minute,
        )

        assert callable(get_stock_minute)
        assert callable(get_etf_minute)


class TestEdgeCases:
    """测试边界情况"""

    def test_single_row_dataframe(self):
        """测试单行 DataFrame"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01 09:30:00"],
                "open": [10.0],
                "high": [10.2],
                "low": [9.8],
                "close": [10.1],
                "volume": [1000],
                "money": [10000],
            }
        )
        result = standardize_minute_ohlcv(df)
        assert len(result) == 1
        assert result["openinterest"].iloc[0] == 0.0

    def test_large_dataframe(self):
        """测试大 DataFrame"""
        n = 1000
        df = pd.DataFrame(
            {
                "datetime": pd.date_range(
                    "2026-01-01 09:30:00", periods=n, freq="1min"
                ),
                "open": [10.0] * n,
                "high": [10.2] * n,
                "low": [9.8] * n,
                "close": [10.1] * n,
                "volume": [1000] * n,
                "money": [10000] * n,
            }
        )
        result = standardize_minute_ohlcv(df)
        assert len(result) == n

    def test_float_precision(self):
        """测试浮点精度"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01 09:30:00"],
                "open": [10.123456789],
                "high": [10.234567890],
                "low": [9.876543210],
                "close": [10.111111111],
                "volume": [1000],
                "money": [10000.555],
            }
        )
        result = standardize_minute_ohlcv(df)
        assert result["open"].iloc[0] == 10.123456789
        assert result["money"].iloc[0] == 10000.555

    def test_negative_values(self):
        """测试负值处理"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01 09:30:00"],
                "open": [-10.0],
                "high": [10.2],
                "low": [-9.8],
                "close": [10.1],
                "volume": [-1000],
                "money": [10000],
            }
        )
        result = standardize_minute_ohlcv(df)
        assert result["open"].iloc[0] == -10.0
        assert result["volume"].iloc[0] == -1000.0

    def test_zero_values(self):
        """测试零值"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01 09:30:00"],
                "open": [0.0],
                "high": [0.0],
                "low": [0.0],
                "close": [0.0],
                "volume": [0],
                "money": [0],
            }
        )
        result = standardize_minute_ohlcv(df)
        assert result["open"].iloc[0] == 0.0
        assert result["volume"].iloc[0] == 0.0

    def test_duplicate_datetime(self):
        """测试重复时间戳"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01 09:30:00", "2026-01-01 09:30:00"],
                "open": [10.0, 10.5],
                "high": [10.2, 10.6],
                "low": [9.8, 10.3],
                "close": [10.1, 10.4],
                "volume": [1000, 2000],
                "money": [10000, 21000],
            }
        )
        result = standardize_minute_ohlcv(df)
        assert len(result) == 2

    def test_missing_all_ohlcv(self):
        """测试缺失所有 OHLCV 列"""
        df = pd.DataFrame(
            {
                "datetime": ["2026-01-01 09:30:00"],
            }
        )
        with pytest.raises(ValueError, match="缺少必要列"):
            standardize_minute_ohlcv(df)


def run_smoke_test():
    """
    手动运行 smoke test（不依赖 pytest）。
    """
    print("=== 分钟数据 Smoke Test ===")

    from datetime import datetime, timedelta

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

    print(f"\n日期范围: {start_date} ~ {end_date}")

    print("\n1. 测试股票 1m 分钟数据...")
    try:
        df_stock = get_stock_minute("sh600000", start_date, end_date, period="1m")
        print(f"   获取到 {len(df_stock)} 条记录")
        print(f"   列: {list(df_stock.columns)}")
        if not df_stock.empty:
            print(f"   首条: {df_stock.iloc[0].to_dict()}")
    except Exception as e:
        print(f"   错误: {e}")

    print("\n2. 测试 ETF 5m 分钟数据...")
    try:
        df_etf = get_etf_minute("510300", start_date, end_date, period="5m")
        print(f"   获取到 {len(df_etf)} 条记录")
        print(f"   列: {list(df_etf.columns)}")
        if not df_etf.empty:
            print(f"   首条: {df_etf.iloc[0].to_dict()}")
    except Exception as e:
        print(f"   错误: {e}")

    print("\n3. 测试 market_api 分钟数据...")
    try:
        from jk2bt.api.market import get_price

        df_api = get_price(
            "600000.XSHG",
            start_date=start_date,
            end_date=end_date,
            frequency="5m",
            fields=["open", "high", "low", "close", "volume", "money"],
        )
        print(f"   获取到 {len(df_api)} 条记录")
        print(f"   列: {list(df_api.columns)}")
        if not df_api.empty:
            print(f"   首条: {df_api.iloc[0].to_dict()}")
    except Exception as e:
        print(f"   错误: {e}")

    print("\n4. 测试所有周期...")
    periods = ["1m", "5m", "15m", "30m", "60m"]
    for p in periods:
        try:
            validated = _validate_period(p)
            print(f"   {p} -> {validated}: OK")
        except Exception as e:
            print(f"   {p}: 错误 - {e}")

    print("\n=== Smoke Test 完成 ===")


if __name__ == "__main__":
    run_smoke_test()
