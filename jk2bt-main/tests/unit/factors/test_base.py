"""
test_base.py
factors/base.py 的单元测试。

测试覆盖：
- normalize_factor_name: 因子名标准化
- normalize_factor_names: 批量标准化
- FactorRegistry 类: 注册、获取、列表、元信息、检查注册
- safe_divide: 安全除法
- fill_missing_with_warning: 填充缺失值
- get_trade_days: 获取交易日
- slice_window: 切片窗口
- align_to_trade_days: 交易日对齐
- 缓存工具: load_factor_cache, save_factor_cache
"""

import os
import sys
import warnings
import tempfile
import shutil
import importlib.util
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
import pandas as pd
import numpy as np

# 直接从文件路径加载模块，避免 package __init__.py 的问题
project_root = Path(__file__).parent.parent.parent.parent
base_file_path = project_root / "jk2bt" / "factors" / "base.py"

# 使用 spec_from_file_location 直接加载模块
spec = importlib.util.spec_from_file_location("factors_base", str(base_file_path))
base_module = importlib.util.module_from_spec(spec)

# 在执行模块之前，需要确保模块的相对导入能正确工作
# 设置 __package__ 为 None 以禁用相对导入
base_module.__package__ = None

# 添加项目路径以便模块内的导入能找到依赖
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 预先 mock jk2bt.core.strategy_base 模块以避免导入问题
mock_strategy_base = MagicMock()
mock_strategy_base.get_all_trade_days_jq = MagicMock(return_value=pd.DatetimeIndex([]))
sys.modules['jk2bt.core.strategy_base'] = mock_strategy_base
sys.modules['jk2bt.core'] = MagicMock()
sys.modules['jk2bt'] = MagicMock()

# 执行模块加载
spec.loader.exec_module(base_module)

# 从模块获取要测试的对象
normalize_factor_name = base_module.normalize_factor_name
normalize_factor_names = base_module.normalize_factor_names
FACTOR_ALIAS_MAP = base_module.FACTOR_ALIAS_MAP
FactorRegistry = base_module.FactorRegistry
global_factor_registry = base_module.global_factor_registry
safe_divide = base_module.safe_divide
fill_missing_with_warning = base_module.fill_missing_with_warning
get_trade_days = base_module.get_trade_days
slice_window = base_module.slice_window
align_to_trade_days = base_module.align_to_trade_days
load_factor_cache = base_module.load_factor_cache
save_factor_cache = base_module.save_factor_cache
_cache_key = base_module._cache_key
_ensure_cache_dir = base_module._ensure_cache_dir


# =====================================================================
# normalize_factor_name 测试
# =====================================================================


class TestNormalizeFactorName:
    """测试 normalize_factor_name 函数。"""

    def test_exact_match_in_alias_map(self):
        """测试精确匹配别名映射表。"""
        # 已知别名
        assert normalize_factor_name("PE_ratio") == "pe_ratio"
        assert normalize_factor_name("PB_ratio") == "pb_ratio"
        assert normalize_factor_name("ROE") == "roe"
        assert normalize_factor_name("BIAS5") == "bias_5"
        assert normalize_factor_name("EMAC10") == "emac_10"

    def test_already_normalized_name(self):
        """测试已是标准名称的因子。"""
        assert normalize_factor_name("pe_ratio") == "pe_ratio"
        assert normalize_factor_name("pb_ratio") == "pb_ratio"
        assert normalize_factor_name("roe") == "roe"
        assert normalize_factor_name("bias_5") == "bias_5"
        assert normalize_factor_name("market_cap") == "market_cap"

    def test_case_insensitive_fallback(self):
        """测试大小写不敏感的回退匹配。"""
        # 通过小写匹配
        assert normalize_factor_name("pe_ratio".upper()) == "pe_ratio"
        assert normalize_factor_name("BIAS5".lower()) == "bias_5"

    def test_unknown_factor_name_returns_original(self):
        """测试未知因子名返回原名称。"""
        # 未在映射表中的因子名应原样返回
        assert normalize_factor_name("custom_factor_xyz") == "custom_factor_xyz"
        assert normalize_factor_name("my_new_factor") == "my_new_factor"
        assert normalize_factor_name("test_123") == "test_123"

    def test_empty_string(self):
        """测试空字符串输入。"""
        assert normalize_factor_name("") == ""

    def test_numeric_suffix_factors(self):
        """测试带数字后缀的因子名。"""
        assert normalize_factor_name("ROC6") == "roc_6"
        assert normalize_factor_name("ROC120") == "roc_120"
        assert normalize_factor_name("VOL240") == "vol_240"
        assert normalize_factor_name("ATR14") == "atr_14"

    def test_technical_indicators(self):
        """测试技术指标因子名标准化。"""
        assert normalize_factor_name("MACD") == "macd"
        assert normalize_factor_name("VOSC") == "vosc"
        assert normalize_factor_name("WVAD") == "wvad"
        assert normalize_factor_name("PSY") == "psy"
        assert normalize_factor_name("VR") == "vr"

    def test_risk_factors(self):
        """测试风险因子名标准化。"""
        assert normalize_factor_name("Variance20") == "variance_20"
        assert normalize_factor_name("Skewness60") == "skewness_60"
        assert normalize_factor_name("Kurtosis120") == "kurtosis_120"
        assert normalize_factor_name("Sharpe20") == "sharpe_ratio_20"


class TestNormalizeFactorNames:
    """测试 normalize_factor_names 函数。"""

    def test_single_string_input(self):
        """测试单个字符串输入。"""
        result = normalize_factor_names("PE_ratio")
        assert result == ["pe_ratio"]

    def test_list_input(self):
        """测试列表输入。"""
        result = normalize_factor_names(["PE_ratio", "PB_ratio", "ROE"])
        assert result == ["pe_ratio", "pb_ratio", "roe"]

    def test_mixed_case_list(self):
        """测试混合大小写的列表。"""
        result = normalize_factor_names(["PE_ratio", "pb_ratio", "ROE"])
        assert result == ["pe_ratio", "pb_ratio", "roe"]

    def test_unknown_names_in_list(self):
        """测试包含未知名称的列表。"""
        result = normalize_factor_names(["PE_ratio", "custom_factor", "ROE"])
        assert result == ["pe_ratio", "custom_factor", "roe"]

    def test_empty_list(self):
        """测试空列表。"""
        result = normalize_factor_names([])
        assert result == []

    def test_preserves_list_order(self):
        """测试保持列表顺序。"""
        factors = ["VOL5", "VOL10", "VOL20", "VOL60"]
        result = normalize_factor_names(factors)
        assert result == ["vol_5", "vol_10", "vol_20", "vol_60"]


# =====================================================================
# FactorRegistry 测试
# =====================================================================


class TestFactorRegistry:
    """测试 FactorRegistry 类。"""

    def setup_method(self):
        """每个测试方法前创建新的注册表实例。"""
        self.registry = FactorRegistry()

    def test_register_and_get(self):
        """测试注册和获取因子。"""
        def dummy_factor(symbol, end_date, count, **kwargs):
            return 1.0

        self.registry.register("test_factor", dummy_factor)
        assert self.registry.get("test_factor") == dummy_factor

    def test_register_with_metadata(self):
        """测试带元数据注册因子。"""
        def dummy_factor(symbol, end_date, count, **kwargs):
            return 1.0

        self.registry.register(
            "test_factor",
            dummy_factor,
            window=20,
            dependencies=["daily_ohlcv"],
            description="测试因子"
        )

        meta = self.registry.get_metadata("test_factor")
        assert meta["window"] == 20
        assert meta["dependencies"] == ["daily_ohlcv"]
        assert meta["description"] == "测试因子"

    def test_register_normalizes_name(self):
        """测试注册时自动标准化因子名。"""
        def dummy_factor(symbol, end_date, count, **kwargs):
            return 1.0

        # 注册时使用别名
        self.registry.register("PE_ratio", dummy_factor)
        # 应该被标准化为 pe_ratio
        assert self.registry.get("pe_ratio") == dummy_factor
        assert self.registry.is_registered("PE_ratio")

    def test_get_nonexistent_factor(self):
        """测试获取不存在的因子。"""
        assert self.registry.get("nonexistent_factor") is None

    def test_get_metadata_nonexistent_factor(self):
        """测试获取不存在因子的元信息。"""
        meta = self.registry.get_metadata("nonexistent_factor")
        assert meta == {}

    def test_list_factors_empty(self):
        """测试空注册表列出因子。"""
        assert self.registry.list_factors() == []

    def test_list_factors_multiple(self):
        """测试列出多个已注册因子。"""
        def factor1(*args, **kwargs):
            return 1.0

        def factor2(*args, **kwargs):
            return 2.0

        def factor3(*args, **kwargs):
            return 3.0

        self.registry.register("factor_a", factor1)
        self.registry.register("factor_b", factor2)
        self.registry.register("factor_c", factor3)

        factors = self.registry.list_factors()
        assert len(factors) == 3
        assert "factor_a" in factors
        assert "factor_b" in factors
        assert "factor_c" in factors

    def test_is_registered_true(self):
        """测试检查已注册因子。"""
        def dummy_factor(*args, **kwargs):
            return 1.0

        self.registry.register("test_factor", dummy_factor)
        assert self.registry.is_registered("test_factor") is True

    def test_is_registered_false(self):
        """测试检查未注册因子。"""
        assert self.registry.is_registered("nonexistent") is False

    def test_is_registered_with_alias(self):
        """测试使用别名检查注册状态。"""
        def dummy_factor(*args, **kwargs):
            return 1.0

        self.registry.register("PE_ratio", dummy_factor)
        # 使用别名检查
        assert self.registry.is_registered("PE_ratio") is True
        # 使用标准名检查
        assert self.registry.is_registered("pe_ratio") is True

    def test_overwrite_registration(self):
        """测试覆盖注册因子。"""
        def factor_v1(*args, **kwargs):
            return 1.0

        def factor_v2(*args, **kwargs):
            return 2.0

        self.registry.register("test_factor", factor_v1)
        self.registry.register("test_factor", factor_v2)

        assert self.registry.get("test_factor") == factor_v2

    def test_multiple_registrations_preserve_metadata(self):
        """测试多次注册更新元信息。"""
        def dummy_factor(*args, **kwargs):
            return 1.0

        self.registry.register("test_factor", dummy_factor, window=10)
        self.registry.register("test_factor", dummy_factor, window=20, description="新描述")

        meta = self.registry.get_metadata("test_factor")
        assert meta["window"] == 20
        assert meta["description"] == "新描述"


class TestGlobalFactorRegistry:
    """测试全局因子注册表实例。"""

    def test_global_registry_exists(self):
        """测试全局注册表实例存在。"""
        assert global_factor_registry is not None
        assert isinstance(global_factor_registry, FactorRegistry)

    def test_global_registry_has_list_factors_method(self):
        """测试全局注册表有 list_factors 方法。"""
        factors = global_factor_registry.list_factors()
        assert isinstance(factors, list)


# =====================================================================
# safe_divide 测试
# =====================================================================


class TestSafeDivide:
    """测试 safe_divide 函数。"""

    def test_basic_division(self):
        """测试基本除法。"""
        result = safe_divide(10.0, 2.0)
        assert result == 5.0

    def test_divide_by_zero_scalar(self):
        """测试标量除以零。"""
        result = safe_divide(10.0, 0.0)
        assert np.isnan(result)

    def test_divide_by_nan_scalar(self):
        """测试标量除以 NaN。"""
        result = safe_divide(10.0, np.nan)
        assert np.isnan(result)

    def test_numpy_array_division(self):
        """测试 NumPy 数组除法。"""
        a = np.array([10.0, 20.0, 30.0])
        b = np.array([2.0, 4.0, 5.0])
        result = safe_divide(a, b)
        np.testing.assert_array_almost_equal(result, [5.0, 5.0, 6.0])

    def test_numpy_array_divide_by_zero(self):
        """测试 NumPy 数组除以零。"""
        a = np.array([10.0, 20.0, 30.0])
        b = np.array([2.0, 0.0, 5.0])
        result = safe_divide(a, b)
        assert result[0] == 5.0
        assert np.isnan(result[1])
        assert result[2] == 6.0

    def test_numpy_array_divide_by_nan(self):
        """测试 NumPy 数组除以 NaN。"""
        a = np.array([10.0, 20.0, 30.0])
        b = np.array([2.0, np.nan, 5.0])
        result = safe_divide(a, b)
        assert result[0] == 5.0
        assert np.isnan(result[1])
        assert result[2] == 6.0

    def test_pandas_series_division(self):
        """测试 pandas Series 除法。"""
        a = pd.Series([10.0, 20.0, 30.0])
        b = pd.Series([2.0, 4.0, 5.0])
        result = safe_divide(a, b)
        pd.testing.assert_series_equal(result, pd.Series([5.0, 5.0, 6.0]))

    def test_pandas_series_divide_by_zero(self):
        """测试 pandas Series 除以零。"""
        a = pd.Series([10.0, 20.0, 30.0])
        b = pd.Series([2.0, 0.0, 5.0])
        result = safe_divide(a, b)
        assert result.iloc[0] == 5.0
        assert pd.isna(result.iloc[1])
        assert result.iloc[2] == 6.0

    def test_zero_numerator(self):
        """测试分子为零。"""
        result = safe_divide(0.0, 5.0)
        assert result == 0.0

    def test_both_zero(self):
        """测试分子分母都为零。"""
        result = safe_divide(0.0, 0.0)
        assert np.isnan(result)


# =====================================================================
# fill_missing_with_warning 测试
# =====================================================================


class TestFillMissingWithWarning:
    """测试 fill_missing_with_warning 函数。"""

    def test_ffill_method(self):
        """测试前向填充。"""
        series = pd.Series([1.0, np.nan, 3.0, np.nan, 5.0])
        result = fill_missing_with_warning(series, method="ffill")
        pd.testing.assert_series_equal(result, pd.Series([1.0, 1.0, 3.0, 3.0, 5.0]))

    def test_bfill_method(self):
        """测试后向填充。"""
        series = pd.Series([1.0, np.nan, 3.0, np.nan, 5.0])
        result = fill_missing_with_warning(series, method="bfill")
        pd.testing.assert_series_equal(result, pd.Series([1.0, 3.0, 3.0, 5.0, 5.0]))

    def test_zero_method(self):
        """测试零填充。"""
        series = pd.Series([1.0, np.nan, 3.0, np.nan, 5.0])
        result = fill_missing_with_warning(series, method="zero")
        pd.testing.assert_series_equal(result, pd.Series([1.0, 0.0, 3.0, 0.0, 5.0]))

    def test_mean_method(self):
        """测试均值填充。"""
        series = pd.Series([1.0, np.nan, 3.0, np.nan, 5.0])
        result = fill_missing_with_warning(series, method="mean")
        # 均值为 (1 + 3 + 5) / 3 = 3.0
        pd.testing.assert_series_equal(result, pd.Series([1.0, 3.0, 3.0, 3.0, 5.0]))

    def test_unknown_method_returns_original(self):
        """测试未知方法返回原序列。"""
        series = pd.Series([1.0, np.nan, 3.0])
        result = fill_missing_with_warning(series, method="unknown")
        pd.testing.assert_series_equal(result, series)

    def test_no_missing_values(self):
        """测试无缺失值序列。"""
        series = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        result = fill_missing_with_warning(series, method="ffill")
        pd.testing.assert_series_equal(result, series)

    def test_empty_series(self):
        """测试空序列。"""
        series = pd.Series([], dtype=float)
        result = fill_missing_with_warning(series, method="ffill")
        assert len(result) == 0

    def test_warning_threshold_not_exceeded(self):
        """测试缺失率未超过阈值时不发出警告。"""
        # 缺失率 20% < 30% 阈值
        series = pd.Series([1.0, np.nan, 3.0, 4.0, 5.0])
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            fill_missing_with_warning(series, method="ffill", warn_threshold=0.3)
            assert len(w) == 0

    def test_warning_threshold_exceeded(self):
        """测试缺失率超过阈值时发出警告。"""
        # 缺失率 40% > 10% 阈值
        series = pd.Series([1.0, np.nan, np.nan, 4.0, 5.0])
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            fill_missing_with_warning(series, method="ffill", warn_threshold=0.1)
            assert len(w) == 1
            assert "缺失率" in str(w[0].message)

    def test_limit_parameter(self):
        """测试填充限制参数。"""
        series = pd.Series([1.0, np.nan, np.nan, np.nan, 5.0])
        result = fill_missing_with_warning(series, method="ffill", limit=2)
        # 只应填充前两个 NaN
        assert pd.isna(result.iloc[3])

    def test_all_missing_values(self):
        """测试全缺失值序列。"""
        series = pd.Series([np.nan, np.nan, np.nan])
        result = fill_missing_with_warning(series, method="ffill")
        # ffill 对全 NaN 不填充
        assert result.isna().all()


# =====================================================================
# get_trade_days 测试
# =====================================================================


class TestGetTradeDays:
    """测试 get_trade_days 函数。"""

    def test_fallback_to_business_days(self):
        """测试回退到工作日计算。"""
        # 由于 mock 了 get_all_trade_days_jq，会回退到工作日计算
        result = get_trade_days("2024-01-01", "2024-01-07")
        # 2024-01-01 是周一, 2024-01-07 是周日
        # 工作日: 1, 2, 3, 4, 5 (周一到周五)
        assert isinstance(result, list)
        assert len(result) == 5  # 周一到周五
        assert "2024-01-01" in result
        assert "2024-01-06" not in result  # 周六
        assert "2024-01-07" not in result  # 周日

    def test_with_trade_calendar_success(self):
        """测试 get_trade_days 返回正确格式。"""
        # 由于 mock，实际使用工作日计算
        result = get_trade_days("2024-01-02", "2024-01-05")
        assert isinstance(result, list)
        assert all(isinstance(d, str) for d in result)
        # 应包含这些日期（假设是工作日）
        assert len(result) >= 1

    def test_with_trade_calendar_exception_handling(self):
        """测试 get_trade_days 异常处理。"""
        # 在 mock 环境下测试基本功能
        result = get_trade_days("2024-01-01", "2024-01-05")
        assert isinstance(result, list)
        assert all(isinstance(d, str) for d in result)

    def test_empty_range_handling(self):
        """测试空范围处理。"""
        # 测试基本功能
        result = get_trade_days("2024-01-02", "2024-01-02")
        assert isinstance(result, list)


# =====================================================================
# slice_window 测试
# =====================================================================


class TestSliceWindow:
    """测试 slice_window 函数。"""

    def test_basic_slice(self):
        """测试基本切片功能。"""
        df = pd.DataFrame({
            "date": pd.date_range("2024-01-01", periods=10).strftime("%Y-%m-%d"),
            "value": range(10)
        })
        result = slice_window(df, "2024-01-05", 3)
        assert len(result) == 3
        assert result["date"].tolist() == ["2024-01-03", "2024-01-04", "2024-01-05"]

    def test_slice_with_larger_count_than_data(self):
        """测试窗口大于数据量。"""
        df = pd.DataFrame({
            "date": pd.date_range("2024-01-01", periods=3).strftime("%Y-%m-%d"),
            "value": range(3)
        })
        result = slice_window(df, "2024-01-03", 10)
        assert len(result) == 3

    def test_empty_dataframe(self):
        """测试空 DataFrame。"""
        df = pd.DataFrame()
        result = slice_window(df, "2024-01-05", 3)
        assert result.empty

    def test_none_dataframe(self):
        """测试 None DataFrame。"""
        result = slice_window(None, "2024-01-05", 3)
        assert result is None

    def test_custom_date_column(self):
        """测试自定义日期列名。"""
        df = pd.DataFrame({
            "trade_date": pd.date_range("2024-01-01", periods=10).strftime("%Y-%m-%d"),
            "value": range(10)
        })
        result = slice_window(df, "2024-01-05", 3, date_col="trade_date")
        assert len(result) == 3

    def test_no_date_column(self):
        """测试无日期列时按行数切片。"""
        df = pd.DataFrame({
            "value": range(10)
        })
        result = slice_window(df, "2024-01-05", 3)
        assert len(result) == 3
        assert result["value"].tolist() == [7, 8, 9]

    def test_end_date_filter(self):
        """测试截止日期过滤。"""
        df = pd.DataFrame({
            "date": pd.date_range("2024-01-01", periods=10).strftime("%Y-%m-%d"),
            "value": range(10)
        })
        result = slice_window(df, "2024-01-05", 10)
        # 只保留 <= 2024-01-05 的数据，然后取最后 10 条
        assert all(d <= "2024-01-05" for d in result["date"])


# =====================================================================
# align_to_trade_days 测试
# =====================================================================


class TestAlignToTradeDays:
    """测试 align_to_trade_days 函数。"""

    def test_basic_alignment(self):
        """测试基本对齐功能。"""
        df = pd.DataFrame({
            "date": ["2024-01-02", "2024-01-04", "2024-01-06"],  # 跳过了周末
            "value": [1, 2, 3]
        })
        result = align_to_trade_days(df, date_col="date", start_date="2024-01-01", end_date="2024-01-07")
        # 结果应包含日期列
        assert "date" in result.columns
        assert "value" in result.columns

    def test_empty_dataframe(self):
        """测试空 DataFrame。"""
        df = pd.DataFrame()
        result = align_to_trade_days(df)
        assert result.empty

    def test_none_dataframe(self):
        """测试 None DataFrame。"""
        result = align_to_trade_days(None)
        assert result is None

    def test_missing_date_column(self):
        """测试缺少日期列时返回原数据。"""
        df = pd.DataFrame({
            "value": [1, 2, 3]
        })
        result = align_to_trade_days(df)
        pd.testing.assert_frame_equal(result, df)

    def test_ffill_method(self):
        """测试前向填充方法。"""
        df = pd.DataFrame({
            "date": ["2024-01-02", "2024-01-04"],
            "value": [1.0, 2.0]
        })
        result = align_to_trade_days(df, fill_method="ffill")
        assert "date" in result.columns

    def test_bfill_method(self):
        """测试后向填充方法。"""
        df = pd.DataFrame({
            "date": ["2024-01-02", "2024-01-04"],
            "value": [1.0, 2.0]
        })
        result = align_to_trade_days(df, fill_method="bfill")
        assert "date" in result.columns

    def test_auto_date_range(self):
        """测试自动确定日期范围。"""
        df = pd.DataFrame({
            "date": ["2024-01-05", "2024-01-10"],
            "value": [1.0, 2.0]
        })
        # 不指定 start_date 和 end_date，应自动使用数据范围
        result = align_to_trade_days(df)
        assert "date" in result.columns


# =====================================================================
# 缓存工具测试
# =====================================================================


class TestCacheUtils:
    """测试缓存工具函数。"""

    def test_ensure_cache_dir(self):
        """测试创建缓存目录。"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = os.path.join(tmpdir, "test_cache")
            _ensure_cache_dir(cache_dir)
            assert os.path.exists(cache_dir)

    def test_ensure_cache_dir_already_exists(self):
        """测试已存在的缓存目录。"""
        with tempfile.TemporaryDirectory() as cache_dir:
            # 不应抛出异常
            _ensure_cache_dir(cache_dir)
            assert os.path.exists(cache_dir)

    def test_cache_key_basic(self):
        """测试基本缓存键生成。"""
        key = _cache_key("pe_ratio", "sh600519", "2024-01-01")
        assert "pe_ratio" in key
        assert "sh600519" in key
        assert "2024-01-01" in key
        assert key.endswith(".pkl")

    def test_cache_key_with_count(self):
        """测试带窗口长度的缓存键。"""
        key = _cache_key("pe_ratio", "sh600519", "2024-01-01", count=20)
        assert "_20" in key

    def test_cache_key_special_chars(self):
        """测试特殊字符处理。"""
        # 冒号和斜杠应被替换
        key = _cache_key("factor", "symbol:test/path", "2024-01-01")
        assert ":" not in key
        assert "/" not in key

    def test_save_and_load_factor_cache(self):
        """测试保存和加载因子缓存。"""
        with tempfile.TemporaryDirectory() as cache_dir:
            df = pd.DataFrame({
                "date": ["2024-01-01", "2024-01-02"],
                "value": [1.0, 2.0]
            })

            # 保存缓存
            save_factor_cache(df, "test_factor", "sh600519", "2024-01-02", cache_dir=cache_dir)

            # 加载缓存
            loaded = load_factor_cache("test_factor", "sh600519", "2024-01-02", cache_dir=cache_dir)

            assert loaded is not None
            pd.testing.assert_frame_equal(loaded, df)

    def test_load_factor_cache_not_found(self):
        """测试加载不存在的缓存。"""
        with tempfile.TemporaryDirectory() as cache_dir:
            result = load_factor_cache("nonexistent", "sh600519", "2024-01-01", cache_dir=cache_dir)
            assert result is None

    def test_load_factor_cache_corrupted(self):
        """测试加载损坏的缓存文件。"""
        with tempfile.TemporaryDirectory() as cache_dir:
            # 创建损坏的缓存文件
            _ensure_cache_dir(cache_dir)
            fname = _cache_key("corrupted", "sh600519", "2024-01-01")
            fpath = os.path.join(cache_dir, fname)
            with open(fpath, "w") as f:
                f.write("not a valid pickle file")

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = load_factor_cache("corrupted", "sh600519", "2024-01-01", cache_dir=cache_dir)
                assert result is None
                assert len(w) == 1
                assert "读取因子缓存失败" in str(w[0].message)

    def test_save_factor_cache_with_count(self):
        """测试带窗口长度的缓存保存。"""
        with tempfile.TemporaryDirectory() as cache_dir:
            df = pd.DataFrame({"value": [1.0, 2.0]})

            save_factor_cache(df, "test_factor", "sh600519", "2024-01-01", count=20, cache_dir=cache_dir)

            # 验证文件名包含 count
            expected_fname = _cache_key("test_factor", "sh600519", "2024-01-01", count=20)
            assert os.path.exists(os.path.join(cache_dir, expected_fname))


# =====================================================================
# 类型检查测试
# =====================================================================


class TestTypeAnnotations:
    """测试类型注解。"""

    def test_normalize_factor_name_returns_str(self):
        """测试 normalize_factor_name 返回字符串。"""
        result = normalize_factor_name("PE_ratio")
        assert isinstance(result, str)

    def test_normalize_factor_names_returns_list(self):
        """测试 normalize_factor_names 返回列表。"""
        result = normalize_factor_names(["PE_ratio", "PB_ratio"])
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)

    def test_factor_registry_list_factors_returns_list(self):
        """测试 FactorRegistry.list_factors 返回列表。"""
        registry = FactorRegistry()
        result = registry.list_factors()
        assert isinstance(result, list)

    def test_safe_divide_preserves_input_type(self):
        """测试 safe_divide 保持输入类型。"""
        # 标量输入返回标量
        result = safe_divide(10.0, 2.0)
        assert isinstance(result, (float, np.floating)) or np.isnan(result)

        # NumPy 数组输入返回 NumPy 数组
        result = safe_divide(np.array([1.0]), np.array([2.0]))
        assert isinstance(result, np.ndarray)

        # pandas Series 输入返回 pandas Series
        result = safe_divide(pd.Series([1.0]), pd.Series([2.0]))
        assert isinstance(result, pd.Series)

    def test_fill_missing_with_warning_returns_series(self):
        """测试 fill_missing_with_warning 返回 Series。"""
        series = pd.Series([1.0, np.nan, 3.0])
        result = fill_missing_with_warning(series)
        assert isinstance(result, pd.Series)

    def test_get_trade_days_returns_list_of_str(self):
        """测试 get_trade_days 返回字符串列表。"""
        result = get_trade_days("2024-01-01", "2024-01-05")
        assert isinstance(result, list)
        assert all(isinstance(x, str) for x in result)

    def test_slice_window_returns_dataframe(self):
        """测试 slice_window 返回 DataFrame。"""
        df = pd.DataFrame({
            "date": ["2024-01-01", "2024-01-02"],
            "value": [1, 2]
        })
        result = slice_window(df, "2024-01-02", 1)
        assert isinstance(result, pd.DataFrame)


# =====================================================================
# 边界条件测试
# =====================================================================


class TestEdgeCases:
    """测试边界条件。"""

    def test_normalize_factor_name_with_spaces(self):
        """测试带空格的因子名。"""
        # 带空格的名称应原样返回（不在映射表中）
        result = normalize_factor_name("pe_ratio ")
        assert result == "pe_ratio "

    def test_normalize_factor_names_with_duplicate(self):
        """测试重复因子名。"""
        # 输入重复因子名，输出也应去重吗？
        result = normalize_factor_names(["PE_ratio", "pe_ratio"])
        # 目前不去重
        assert result == ["pe_ratio", "pe_ratio"]

    def test_factor_registry_empty_string_name(self):
        """测试空字符串因子名。"""
        registry = FactorRegistry()
        registry.register("", lambda x: x)
        assert registry.is_registered("")
        assert registry.get("") is not None

    def test_safe_divide_inf(self):
        """测试除以无穷小。"""
        result = safe_divide(10.0, np.inf)
        assert result == 0.0

    def test_safe_divide_by_inf(self):
        """测试除以无穷大。"""
        result = safe_divide(np.inf, np.inf)
        assert np.isnan(result)

    def test_slice_window_count_zero(self):
        """测试窗口长度为零。"""
        df = pd.DataFrame({
            "date": ["2024-01-01", "2024-01-02"],
            "value": [1, 2]
        })
        result = slice_window(df, "2024-01-02", 0)
        assert len(result) == 0

    def test_slice_window_count_negative(self):
        """测试窗口长度为负数时 DataFrame.tail 的实际行为。"""
        df = pd.DataFrame({
            "date": ["2024-01-01", "2024-01-02"],
            "value": [1, 2]
        })
        result = slice_window(df, "2024-01-02", -1)
        # DataFrame.tail(-n) 返回除前 n 行外的所有行
        # tail(-1) 返回除第一行外的所有行，即最后一行
        assert len(result) == 1

    def test_fill_missing_with_all_nan(self):
        """测试全 NaN 序列填充。"""
        series = pd.Series([np.nan, np.nan, np.nan])
        result = fill_missing_with_warning(series, method="zero")
        assert (result == 0.0).all()

    def test_get_trade_days_same_start_end(self):
        """测试起始日期等于截止日期。"""
        result = get_trade_days("2024-01-02", "2024-01-02")
        # 结果可能包含或不包含这一天，取决于是否是工作日
        assert isinstance(result, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])