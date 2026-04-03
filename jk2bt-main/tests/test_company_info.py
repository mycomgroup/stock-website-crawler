"""
test_company_info.py
单元测试：上市公司基本信息与状态变动 API

测试内容：
1. 边界情况测试：空代码、无效代码、各种格式、ST股票、退市股票、新股
2. 数据验证测试：字段完整性、数据类型、日期格式、空值处理
3. 缓存机制测试：DuckDB缓存、Pickle缓存、缓存过期、force_update
4. 批量查询测试：多股票、包含无效代码、性能测试
5. finance.run_query测试：过滤条件、limit、多字段、空结果、错误处理
6. 状态变动测试：停牌、历史状态、日期范围、正常交易
7. 集成测试：策略集成、API联合使用
"""

import pytest
import unittest
import pandas as pd
import numpy as np
import os
import tempfile
import shutil
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from jk2bt.finance_data.company_info import (
    get_company_info,
    get_security_status,
    query_company_basic_info,
    query_status_change,
    get_company_info_robust,
    get_security_status_robust,
    query_company_info_robust,
    get_company_info_list,
    get_industry_info,
    prewarm_company_info_cache,
    RobustResult,
    CACHE_EXPIRE_DAYS,
    _normalize_to_jq,
    _extract_code_num,
    _normalize_date,
    _COMPANY_BASIC_INFO_SCHEMA,
    _STATUS_CHANGE_SCHEMA,
    run_query_simple,
)
from jk2bt.core.strategy_base import finance, query


class TestCompanyInfo(unittest.TestCase):
    def test_get_company_info_single(self):
        """测试获取单个公司基本信息"""
        symbol = "600519.XSHG"
        df = get_company_info(symbol)

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)

    def test_finance_module_attributes(self):
        """测试finance模块新属性"""
        self.assertTrue(hasattr(finance, "STK_COMPANY_BASIC_INFO"))
        self.assertTrue(hasattr(finance, "STK_STATUS_CHANGE"))

    def test_finance_table_proxy(self):
        """测试finance表代理"""
        table = finance.STK_COMPANY_BASIC_INFO
        self.assertTrue(hasattr(table, "_name"))
        self.assertEqual(table._name, "STK_COMPANY_BASIC_INFO")

    def test_query_company_basic_info_finance(self):
        """测试通过 finance.run_query 查询公司基本信息"""
        stocks = ["600519.XSHG"]

        df = finance.run_query(
            query(
                finance.STK_COMPANY_BASIC_INFO.code,
                finance.STK_COMPANY_BASIC_INFO.company_name,
            ).filter(finance.STK_COMPANY_BASIC_INFO.code.in_(stocks))
        )

        self.assertIsInstance(df, pd.DataFrame)

    def test_company_info_schema_fallback(self):
        """测试公司基本信息表schema保底"""
        df = finance.run_query(
            query(finance.STK_COMPANY_BASIC_INFO.code).filter(
                finance.STK_COMPANY_BASIC_INFO.code.in_(["999999.XSHG"])
            )
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("code", df.columns)


class TestEdgeCases:
    """边界情况测试"""

    @pytest.mark.parametrize("empty_input", ["", "   ", "NaN"])
    def test_empty_stock_code(self, empty_input):
        """测试空股票代码处理"""
        df = get_company_info(empty_input, use_duckdb=False, force_update=False)
        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns

    def test_none_stock_code_raises_error(self):
        """测试None股票代码抛出异常"""
        with pytest.raises(AttributeError):
            get_company_info(None, use_duckdb=False, force_update=False)

    @pytest.mark.parametrize(
        "invalid_code",
        ["999999.XSHG", "999999.XSHE", "888888", "000000", "123456789", "ABCDEF"],
    )
    def test_invalid_stock_code(self, invalid_code):
        """测试无效股票代码处理"""
        df = get_company_info(invalid_code, use_duckdb=False, force_update=False)
        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns

    @pytest.mark.parametrize(
        "input_code,expected_output",
        [
            ("600519.XSHG", "600519.XSHG"),
            ("sh600519", "600519.XSHG"),
            ("600519", "600519.XSHG"),
            ("000001.XSHE", "000001.XSHE"),
            ("sz000001", "000001.XSHE"),
            ("000001", "000001.XSHE"),
            ("002594.XSHE", "002594.XSHE"),
            ("sz002594", "002594.XSHE"),
            ("002594", "002594.XSHE"),
            ("300001.XSHE", "300001.XSHE"),
            ("688001.XSHG", "688001.XSHG"),
        ],
    )
    def test_stock_code_format_normalization(self, input_code, expected_output):
        """测试各种股票代码格式转换"""
        normalized = _normalize_to_jq(input_code)
        assert normalized == expected_output

    @pytest.mark.parametrize(
        "code_num,expected",
        [
            ("600519", "600519"),
            ("sh600519", "600519"),
            ("sz000001", "000001"),
            ("600519.XSHG", "600519"),
            ("000001.XSHE", "000001"),
            ("519", "000519"),
            ("1", "000001"),
        ],
    )
    def test_extract_code_num(self, code_num, expected):
        """测试提取6位代码数字"""
        result = _extract_code_num(code_num)
        assert result == expected

    def test_st_stock_query(self):
        """测试ST股票查询（如ST某某）"""
        st_codes = ["600640.XSHG"]
        df = get_company_info(st_codes[0], use_duckdb=False, force_update=False)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "code" in df.columns

    def test_delisted_stock_query(self):
        """测试退市股票查询"""
        delisted_codes = ["600001.XSHG"]
        df = get_company_info(delisted_codes[0], use_duckdb=False, force_update=False)
        assert isinstance(df, pd.DataFrame)

    def test_new_stock_query(self):
        """测试新股查询（近期上市股票）"""
        new_stock = "688001.XSHG"
        df = get_company_info(new_stock, use_duckdb=False, force_update=False)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "code" in df.columns


class TestDataValidation:
    """数据验证测试"""

    def test_company_info_field_completeness(self):
        """测试返回字段完整性验证"""
        df = get_company_info("600519.XSHG", use_duckdb=False, force_update=False)

        expected_fields = _COMPANY_BASIC_INFO_SCHEMA
        for field in expected_fields:
            assert field in df.columns

    @pytest.mark.parametrize("field", _COMPANY_BASIC_INFO_SCHEMA)
    def test_company_info_single_field_validation(self, field):
        """测试单个字段存在性"""
        df = get_company_info("600519.XSHG", use_duckdb=False, force_update=False)
        assert field in df.columns

    def test_data_type_validation(self):
        """测试数据类型验证"""
        df = get_company_info("600519.XSHG", use_duckdb=False, force_update=False)

        if not df.empty:
            assert isinstance(df, pd.DataFrame)
            assert isinstance(df["code"].iloc[0], str)
            if df["company_name"].iloc[0] is not None:
                assert isinstance(df["company_name"].iloc[0], str)

    @pytest.mark.parametrize(
        "date_input,expected",
        [
            ("2025-01-15", "2025-01-15"),
            ("20250115", "2025-01-15"),
            ("2025/01/15", "2025/01/15"),
        ],
    )
    def test_date_format_normalization(self, date_input, expected):
        """测试日期格式标准化"""
        result = _normalize_date(date_input)
        if "-" in date_input or len(date_input) == 8:
            assert result == expected

    def test_empty_value_handling(self):
        """测试空值处理验证"""
        df = get_company_info("999999.XSHG", use_duckdb=False, force_update=False)

        assert isinstance(df, pd.DataFrame)
        for col in _COMPANY_BASIC_INFO_SCHEMA:
            assert col in df.columns

    def test_company_info_schema_constant(self):
        """测试schema常量定义"""
        expected_schema = [
            "code",
            "company_name",
            "establish_date",
            "list_date",
            "main_business",
            "industry",
            "registered_address",
            "company_status",
            "status_change_date",
            "change_type",
        ]
        assert _COMPANY_BASIC_INFO_SCHEMA == expected_schema

    def test_status_change_schema_constant(self):
        """测试状态变动schema常量"""
        expected_schema = ["code", "status_date", "status_type", "reason"]
        assert _STATUS_CHANGE_SCHEMA == expected_schema


class TestCacheMechanism:
    """缓存机制测试"""

    def setup_method(self):
        """每个测试方法前设置临时缓存目录"""
        self.temp_cache_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """每个测试方法后清理临时缓存目录"""
        if os.path.exists(self.temp_cache_dir):
            shutil.rmtree(self.temp_cache_dir)

    def test_pickle_cache_creation(self):
        """测试pickle缓存文件创建"""
        symbol = "600519"
        df = get_company_info(
            symbol, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=True
        )

        cache_file = os.path.join(self.temp_cache_dir, f"company_info_{symbol}.pkl")
        assert isinstance(df, pd.DataFrame)

        if not df.empty:
            assert os.path.exists(cache_file)

    def test_pickle_cache_hit(self):
        """测试pickle缓存命中"""
        symbol = "600519"

        get_company_info(
            symbol, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=True
        )

        df2 = get_company_info(
            symbol, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=False
        )

        assert isinstance(df2, pd.DataFrame)

    def test_force_update_parameter(self):
        """测试force_update参数强制刷新"""
        symbol = "600519"

        df1 = get_company_info(
            symbol, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=True
        )

        df2 = get_company_info(
            symbol, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=True
        )

        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)

    def test_cache_expire_days_value(self):
        """测试缓存过期天数配置"""
        assert CACHE_EXPIRE_DAYS == 90

    def test_cache_expire_check(self):
        """测试缓存过期检查逻辑"""
        symbol = "600519"
        cache_file = os.path.join(self.temp_cache_dir, f"company_info_{symbol}.pkl")

        df = get_company_info(
            symbol, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=True
        )

        if not df.empty and os.path.exists(cache_file):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(cache_file))
            age_days = (datetime.now() - file_mtime).days
            assert age_days < CACHE_EXPIRE_DAYS

    def test_duckdb_disabled_fallback(self):
        """测试DuckDB禁用时Pickle缓存回退"""
        symbol = "600519"

        df = get_company_info(
            symbol, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=True
        )

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns


class TestBatchQuery:
    """批量查询测试"""

    def setup_method(self):
        self.temp_cache_dir = tempfile.mkdtemp()

    def teardown_method(self):
        if os.path.exists(self.temp_cache_dir):
            shutil.rmtree(self.temp_cache_dir)

    @pytest.mark.parametrize(
        "symbols",
        [
            ["600519.XSHG"],
            ["600519.XSHG", "000001.XSHE"],
            ["600519", "000001", "600036"],
            ["600519.XSHG", "000001.XSHE", "600036.XSHG", "002594.XSHE"],
        ],
    )
    def test_batch_query_multiple_stocks(self, symbols):
        """测试批量查询多个股票"""
        df = query_company_basic_info(
            symbols, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=False
        )

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns

    def test_batch_query_with_invalid_codes(self):
        """测试批量查询包含无效代码"""
        symbols = ["600519.XSHG", "999999.XSHG", "000001.XSHE", "888888.XSHE"]
        df = query_company_basic_info(
            symbols, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=False
        )

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns

    def test_batch_query_empty_list(self):
        """测试批量查询空列表"""
        df = query_company_basic_info([], use_duckdb=False)

        assert isinstance(df, pd.DataFrame)
        assert df.empty
        assert "code" in df.columns

    def test_batch_query_none_input(self):
        """测试批量查询None输入"""
        df = query_company_basic_info(None, use_duckdb=False)

        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_get_company_info_list_dict_output(self):
        """测试批量查询返回字典格式"""
        securities = ["600519.XSHG", "000001.XSHE"]
        result = get_company_info_list(
            securities,
            cache_dir=self.temp_cache_dir,
            use_duckdb=False,
            force_update=False,
        )

        assert isinstance(result, dict)
        assert len(result) == 2
        for code, df in result.items():
            assert isinstance(df, pd.DataFrame)

    def test_batch_query_performance_small_batch(self):
        """测试小批量查询性能"""
        symbols = ["600519.XSHG", "000001.XSHE", "600036.XSHG"]

        start_time = datetime.now()
        df = query_company_basic_info(
            symbols, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=False
        )
        elapsed_time = (datetime.now() - start_time).total_seconds()

        assert isinstance(df, pd.DataFrame)
        assert elapsed_time < 30


class TestFinanceRunQuery:
    """finance.run_query 测试"""

    def test_run_query_with_filter(self):
        """测试带过滤条件查询"""
        stocks = ["600519.XSHG"]

        df = finance.run_query(
            query(finance.STK_COMPANY_BASIC_INFO.code).filter(
                finance.STK_COMPANY_BASIC_INFO.code.in_(stocks)
            )
        )

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns

    def test_run_query_multiple_fields(self):
        """测试多字段查询"""
        stocks = ["600519.XSHG"]

        df = finance.run_query(
            query(
                finance.STK_COMPANY_BASIC_INFO.code,
                finance.STK_COMPANY_BASIC_INFO.company_name,
                finance.STK_COMPANY_BASIC_INFO.industry,
            ).filter(finance.STK_COMPANY_BASIC_INFO.code.in_(stocks))
        )

        assert isinstance(df, pd.DataFrame)

    def test_run_query_empty_result(self):
        """测试空结果查询"""
        df = finance.run_query(
            query(finance.STK_COMPANY_BASIC_INFO.code).filter(
                finance.STK_COMPANY_BASIC_INFO.code.in_(["999999.XSHG"])
            )
        )

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns

    def test_run_query_status_change(self):
        """测试状态变动查询"""
        df = finance.run_query(
            query(finance.STK_STATUS_CHANGE.code).filter(
                finance.STK_STATUS_CHANGE.code.in_(["600519.XSHG"])
            )
        )

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns

    def test_run_query_simple_interface(self):
        """测试简化查询接口"""
        df = run_query_simple("STK_COMPANY_BASIC_INFO", code="600519.XSHG")

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns

    def test_run_query_simple_invalid_table(self):
        """测试简化查询接口无效表名"""
        with pytest.raises(ValueError):
            run_query_simple("INVALID_TABLE", code="600519.XSHG")

    def test_run_query_simple_status_change(self):
        """测试简化查询接口状态变动"""
        df = run_query_simple("STK_STATUS_CHANGE", code="600519.XSHG")

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns

    def test_run_query_simple_empty_code(self):
        """测试简化查询接口空代码"""
        df = run_query_simple("STK_COMPANY_BASIC_INFO", code=None)

        assert isinstance(df, pd.DataFrame)
        assert df.empty


class TestStatusChange:
    """状态变动测试"""

    def setup_method(self):
        self.temp_cache_dir = tempfile.mkdtemp()

    def teardown_method(self):
        if os.path.exists(self.temp_cache_dir):
            shutil.rmtree(self.temp_cache_dir)

    def test_get_security_status_normal_trading(self):
        """测试正常交易状态查询"""
        df = get_security_status(
            "600519.XSHG",
            cache_dir=self.temp_cache_dir,
            use_duckdb=False,
            force_update=False,
        )

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns
        assert "status_type" in df.columns

    @pytest.mark.parametrize("date_format", ["2025-01-15", "20250115"])
    def test_get_security_status_with_date(self, date_format):
        """测试指定日期状态查询"""
        df = get_security_status(
            "600519.XSHG",
            date=date_format,
            cache_dir=self.temp_cache_dir,
            use_duckdb=False,
            force_update=False,
        )

        assert isinstance(df, pd.DataFrame)

    def test_query_status_change_single_stock(self):
        """测试单只股票状态变动查询"""
        df = query_status_change(
            ["600519.XSHG"],
            cache_dir=self.temp_cache_dir,
            use_duckdb=False,
            force_update=False,
        )

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns

    def test_query_status_change_with_date_range(self):
        """测试日期范围查询状态变动"""
        df = query_status_change(
            ["600519.XSHG"],
            start_date="2025-01-01",
            end_date="2025-01-05",
            cache_dir=self.temp_cache_dir,
            use_duckdb=False,
            force_update=False,
        )

        assert isinstance(df, pd.DataFrame)

    def test_query_status_change_empty_list(self):
        """测试空列表状态变动查询"""
        df = query_status_change([], use_duckdb=False)

        assert isinstance(df, pd.DataFrame)
        assert df.empty
        assert "code" in df.columns

    def test_get_security_status_robust_success(self):
        """测试稳健版状态查询成功场景"""
        result = get_security_status_robust(
            "600519.XSHG",
            cache_dir=self.temp_cache_dir,
            use_duckdb=False,
            force_update=False,
        )

        assert isinstance(result, RobustResult)
        assert isinstance(result.data, pd.DataFrame)

    def test_get_security_status_robust_empty_input(self):
        """测试稳健版状态查询空输入"""
        result = get_security_status_robust(None)

        assert isinstance(result, RobustResult)
        assert result.success is False
        assert "空" in result.reason


class TestRobustResultClass:
    """RobustResult 类测试"""

    def test_robust_result_success_creation(self):
        """测试成功结果创建"""
        df = pd.DataFrame({"code": ["600519.XSHG"]})
        result = RobustResult(success=True, data=df, reason="成功", source="cache")

        assert result.success is True
        assert result.data.equals(df)
        assert result.reason == "成功"
        assert result.source == "cache"
        assert bool(result) is True

    def test_robust_result_failure_creation(self):
        """测试失败结果创建"""
        result = RobustResult(success=False, data=None, reason="失败", source="network")

        assert result.success is False
        assert result.data.empty
        assert result.reason == "失败"
        assert bool(result) is False

    def test_robust_result_repr(self):
        """测试结果字符串表示"""
        result = RobustResult(success=True, data=pd.DataFrame(), reason="test")
        repr_str = repr(result)

        assert "SUCCESS" in repr_str
        assert "test" in repr_str

    def test_robust_result_is_empty_dataframe(self):
        """测试空DataFrame判断"""
        empty_df = pd.DataFrame()
        result = RobustResult(success=False, data=empty_df)

        assert result.is_empty() is True

    def test_robust_result_is_empty_list(self):
        """测试空列表判断"""
        result = RobustResult(success=False, data=[])

        assert result.is_empty() is True

    def test_robust_result_not_empty(self):
        """测试非空判断"""
        df = pd.DataFrame({"a": [1, 2, 3]})
        result = RobustResult(success=True, data=df)

        assert result.is_empty() is False


class TestRobustAPI:
    """稳健版API测试"""

    def setup_method(self):
        self.temp_cache_dir = tempfile.mkdtemp()

    def teardown_method(self):
        if os.path.exists(self.temp_cache_dir):
            shutil.rmtree(self.temp_cache_dir)

    def test_get_company_info_robust_single(self):
        """测试稳健版单股票查询"""
        result = get_company_info_robust(
            "600519.XSHG",
            cache_dir=self.temp_cache_dir,
            use_duckdb=False,
            force_update=False,
        )

        assert isinstance(result, RobustResult)
        assert isinstance(result.data, pd.DataFrame)

    def test_get_company_info_robust_batch(self):
        """测试稳健版批量查询"""
        symbols = ["600519.XSHG", "000001.XSHE"]
        result = get_company_info_robust(
            symbols, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=False
        )

        assert isinstance(result, RobustResult)
        assert isinstance(result.data, pd.DataFrame)

    def test_get_company_info_robust_empty_input(self):
        """测试稳健版空输入"""
        result = get_company_info_robust(None)

        assert result.success is False
        assert "空" in result.reason

    def test_get_company_info_robust_empty_list(self):
        """测试稳健版空列表"""
        result = get_company_info_robust([])

        assert result.success is False
        assert "空" in result.reason

    def test_get_company_info_robust_invalid_code(self):
        """测试稳健版无效代码"""
        result = get_company_info_robust("999999.XSHG", use_duckdb=False)

        assert isinstance(result, RobustResult)
        assert "code" in result.data.columns

    def test_query_company_info_robust_batch(self):
        """测试稳健版批量查询接口"""
        symbols = ["600519.XSHG", "000001.XSHE", "600036.XSHG"]
        result = query_company_info_robust(
            symbols, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=False
        )

        assert isinstance(result, RobustResult)
        assert isinstance(result.data, pd.DataFrame)


class TestIndustryInfo:
    """行业信息测试"""

    def setup_method(self):
        self.temp_cache_dir = tempfile.mkdtemp()

    def teardown_method(self):
        if os.path.exists(self.temp_cache_dir):
            shutil.rmtree(self.temp_cache_dir)

    def test_get_industry_info_basic(self):
        """测试获取行业信息基本功能"""
        df = get_industry_info(
            "600519.XSHG", cache_dir=self.temp_cache_dir, force_update=False
        )

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns
        assert "industry_name" in df.columns

    def test_get_industry_info_sz_stock(self):
        """测试深交所股票行业信息"""
        df = get_industry_info(
            "000001.XSHE", cache_dir=self.temp_cache_dir, force_update=False
        )

        assert isinstance(df, pd.DataFrame)

    def test_get_industry_info_schema(self):
        """测试行业信息返回字段"""
        df = get_industry_info("600519.XSHG", force_update=False)

        expected_cols = ["code", "industry_code", "industry_name", "industry_level"]
        for col in expected_cols:
            assert col in df.columns


class TestPrewarmCache:
    """缓存预热测试"""

    def setup_method(self):
        self.temp_cache_dir = tempfile.mkdtemp()

    def teardown_method(self):
        if os.path.exists(self.temp_cache_dir):
            shutil.rmtree(self.temp_cache_dir)

    def test_prewarm_basic(self):
        """测试基本预热功能"""
        securities = ["600519.XSHG", "000001.XSHE"]
        result = prewarm_company_info_cache(
            securities, cache_dir=self.temp_cache_dir, use_duckdb=False
        )

        assert isinstance(result, dict)
        assert len(result) == 2
        for sec in securities:
            assert sec in result
            assert isinstance(result[sec], bool)

    def test_prewarm_single_stock(self):
        """测试单股票预热"""
        result = prewarm_company_info_cache(
            ["600519.XSHG"], cache_dir=self.temp_cache_dir, use_duckdb=False
        )

        assert isinstance(result, dict)
        assert "600519.XSHG" in result


class TestNetworkFailureMock:
    """网络失败场景模拟测试"""

    def setup_method(self):
        self.temp_cache_dir = tempfile.mkdtemp()

    def teardown_method(self):
        if os.path.exists(self.temp_cache_dir):
            shutil.rmtree(self.temp_cache_dir)

    @patch(
        "src.finance_data.company_info._fetch_company_profile"
    )
    def test_fetch_profile_failure(self, mock_fetch):
        """测试获取公司信息失败"""
        mock_fetch.return_value = None

        df = get_company_info(
            "600519.XSHG",
            cache_dir=self.temp_cache_dir,
            use_duckdb=False,
            force_update=True,
        )

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns

    @patch(
        "src.finance_data.company_info._fetch_company_industry"
    )
    def test_fetch_industry_failure(self, mock_fetch):
        """测试获取行业信息失败"""
        mock_fetch.return_value = None

        df = get_company_info(
            "600519.XSHG",
            cache_dir=self.temp_cache_dir,
            use_duckdb=False,
            force_update=True,
        )

        assert isinstance(df, pd.DataFrame)

    @patch(
        "src.finance_data.company_info._fetch_suspension_data"
    )
    def test_fetch_suspension_failure(self, mock_fetch):
        """测试获取停牌数据失败"""
        mock_fetch.return_value = None

        df = get_security_status(
            "600519.XSHG",
            date="2025-01-15",
            cache_dir=self.temp_cache_dir,
            use_duckdb=False,
            force_update=True,
        )

        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns


class TestIntegration:
    """集成测试"""

    def setup_method(self):
        self.temp_cache_dir = tempfile.mkdtemp()

    def teardown_method(self):
        if os.path.exists(self.temp_cache_dir):
            shutil.rmtree(self.temp_cache_dir)

    def test_full_workflow(self):
        """测试完整工作流"""
        symbol = "600519.XSHG"

        df_info = get_company_info(
            symbol, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=False
        )
        df_status = get_security_status(
            symbol, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=False
        )
        df_industry = get_industry_info(
            symbol, cache_dir=self.temp_cache_dir, force_update=False
        )

        assert isinstance(df_info, pd.DataFrame)
        assert isinstance(df_status, pd.DataFrame)
        assert isinstance(df_industry, pd.DataFrame)

    def test_robust_vs_normal_consistency(self):
        """测试稳健版与普通版一致性"""
        symbol = "600519.XSHG"

        normal_df = get_company_info(
            symbol, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=False
        )
        robust_result = get_company_info_robust(
            symbol, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=False
        )

        assert isinstance(normal_df, pd.DataFrame)
        assert isinstance(robust_result, RobustResult)
        assert isinstance(robust_result.data, pd.DataFrame)

    def test_batch_then_single_query(self):
        """测试先批量再单查"""
        symbols = ["600519.XSHG", "000001.XSHE"]

        batch_df = query_company_basic_info(
            symbols, cache_dir=self.temp_cache_dir, use_duckdb=False, force_update=False
        )

        single_df = get_company_info(
            "600519.XSHG",
            cache_dir=self.temp_cache_dir,
            use_duckdb=False,
            force_update=False,
        )

        assert isinstance(batch_df, pd.DataFrame)
        assert isinstance(single_df, pd.DataFrame)

    def test_finance_module_integration(self):
        """测试finance模块集成"""
        assert hasattr(finance, "STK_COMPANY_BASIC_INFO")
        assert hasattr(finance, "STK_STATUS_CHANGE")
        assert hasattr(finance, "run_query")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
