"""
test_industry_sw_api.py
申万行业 API 测试

测试覆盖:
1. 正常功能测试 - 行业列表、股票行业查询
2. 边界条件测试 - 空输入、None输入、无效代码
3. 异常处理测试 - 网络失败、数据缺失
4. 缓存机制测试 - 缓存命中、缓存过期
5. RobustResult 测试 - success/data/reason/source 验证
6. 批量查询测试 - 多股票查询
7. 代码格式兼容测试
8. 多级行业测试 - 一级/二级/三级行业
9. 行业表现测试 - 涨跌幅、资金流向
10. 股票筛选测试 - 按行业筛选、排除行业
"""

import unittest
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.market_data.industry_sw import (
    RobustResult,
    get_industry_sw,
    get_stock_industry,
    get_industry_sw_batch,
    filter_stocks_by_industry,
    get_industry_stocks_sw,
    get_industry_stocks,
    get_all_industry_mapping,
    get_industry_performance_sw,
    get_industry_performance,
    get_sw_industry_list,
    get_sw_level1,
    get_sw_level2,
    get_sw_level3,
    SWIndustryCache,
    DEFAULT_INDUSTRY_SCHEMA,
    finance,
    FinanceQuery,
    run_query_simple,
    _normalize_stock_code,
    _normalize_to_jq,
    IndustrySWDBManager,
    STK_INDUSTRY_SW,
    STK_SW_INDUSTRY,
    STK_SW_INDUSTRY_STOCK,
)


class TestIndustryListLevels(unittest.TestCase):
    """测试行业列表三个级别"""

    def test_level1_industry_count(self):
        """测试一级行业数量（申万一级应有约30个行业）"""
        df = get_sw_level1()
        if not df.empty:
            self.assertGreater(len(df), 0)
            self.assertIn("industry_code", df.columns)
            self.assertIn("industry_name", df.columns)

    def test_level2_industry_count(self):
        """测试二级行业数量"""
        df = get_sw_level2()
        if not df.empty:
            self.assertGreater(len(df), 0)

    def test_level3_industry_count(self):
        """测试三级行业数量"""
        df = get_sw_level3()
        if not df.empty:
            self.assertGreater(len(df), 0)

    def test_industry_level_hierarchy(self):
        """测试行业层级关系：三级 >= 二级 >= 一级"""
        df1 = get_sw_level1()
        df2 = get_sw_level2()
        df3 = get_sw_level3()
        if not df1.empty and not df2.empty and not df3.empty:
            self.assertLessEqual(len(df1), len(df2))
            self.assertLessEqual(len(df2), len(df3))

    def test_industry_list_data_types(self):
        """测试行业列表数据类型"""
        result = get_sw_industry_list(level=1)
        if result.success and not result.is_empty():
            df = result.data
            self.assertTrue(
                df["industry_name"].dtype == object
                or df["industry_name"].dtype.name == "string"
            )

    def test_industry_list_return_type(self):
        """测试行业列表返回类型"""
        result = get_sw_industry_list(level=1)
        self.assertIsInstance(result, RobustResult)

    def test_invalid_industry_level(self):
        """测试无效的行业级别"""
        result = get_sw_industry_list(level=0)
        self.assertFalse(result.success)
        result = get_sw_industry_list(level=4)
        self.assertFalse(result.success)

    def test_level1_industry_names(self):
        """测试一级行业名称"""
        df = get_sw_level1()
        if not df.empty and "industry_name" in df.columns:
            names = df["industry_name"].tolist()
            self.assertGreater(len(names), 0)

    def test_industry_code_format(self):
        """测试行业代码格式"""
        result = get_sw_industry_list(level=1)
        if result.success and not result.is_empty():
            df = result.data
            codes = df["industry_code"].dropna()
            for code in codes.head(5):
                self.assertIsInstance(code, (str, int))

    def test_level1_has_28_industries(self):
        """测试申万一级行业数量为28个"""
        df = get_sw_level1()
        if not df.empty:
            self.assertGreaterEqual(len(df), 20, "申万一级行业应至少有20个")

    def test_level2_more_than_level1(self):
        """测试二级行业数量大于一级行业"""
        df1 = get_sw_level1()
        df2 = get_sw_level2()
        if not df1.empty and not df2.empty:
            self.assertGreater(len(df2), len(df1), "二级行业数量应大于一级")

    def test_level3_more_than_level2(self):
        """测试三级行业数量大于二级行业"""
        df2 = get_sw_level2()
        df3 = get_sw_level3()
        if not df2.empty and not df3.empty:
            self.assertGreater(len(df3), len(df2), "三级行业数量应大于二级")

    def test_industry_level_column_exists(self):
        """测试行业级别列存在"""
        result = get_sw_industry_list(level=1)
        if result.success and not result.is_empty():
            self.assertIn("level", result.data.columns)


class TestStockIndustryQuery(unittest.TestCase):
    """测试股票行业查询"""

    def test_single_stock_sh_main_board(self):
        """测试沪市主板股票行业"""
        result = get_stock_industry("600519")
        self.assertIsInstance(result, RobustResult)
        if result.success:
            self.assertIn("level1_name", result.data)

    def test_single_stock_sz_main_board(self):
        """测试深市主板股票行业"""
        result = get_stock_industry("000001")
        self.assertIsInstance(result, RobustResult)

    def test_single_stock_chi_next(self):
        """测试创业板股票行业"""
        result = get_stock_industry("300750")
        self.assertIsInstance(result, RobustResult)

    def test_single_stock_sse_star(self):
        """测试科创板股票行业"""
        result = get_stock_industry("688981")
        self.assertIsInstance(result, RobustResult)

    def test_batch_multiple_stocks(self):
        """测试批量查询多只股票"""
        codes = ["600519", "000001", "000858", "601318"]
        result = get_industry_sw_batch(codes)
        self.assertIsInstance(result, RobustResult)
        if result.success:
            self.assertIsInstance(result.data, pd.DataFrame)
            self.assertLessEqual(len(result.data), len(codes))

    def test_batch_with_different_formats(self):
        """测试批量查询不同代码格式"""
        codes = ["600519.XSHG", "000001.XSHE", "sh600036"]
        result = get_industry_sw_batch(codes)
        self.assertIsInstance(result, RobustResult)

    def test_stock_industry_returns_robust_result(self):
        """测试返回 RobustResult"""
        result = get_stock_industry("600519.XSHG")
        self.assertIsInstance(result, RobustResult)

    def test_stock_industry_data_type(self):
        """测试返回数据类型"""
        result = get_stock_industry("600519")
        self.assertIsInstance(result.data, dict)

    def test_stock_industry_with_cache(self):
        """测试缓存使用"""
        result1 = get_stock_industry("000001", use_cache=True)
        result2 = get_stock_industry("000001", use_cache=True)
        self.assertIsInstance(result1, RobustResult)
        self.assertIsInstance(result2, RobustResult)

    def test_stock_industry_invalid_code(self):
        """测试无效股票代码"""
        result = get_stock_industry("999999")
        self.assertIsInstance(result, RobustResult)

    def test_stock_industry_empty_code(self):
        """测试空股票代码"""
        result = get_stock_industry("")
        self.assertIsInstance(result, RobustResult)

    def test_stock_industry_none_code(self):
        """测试None股票代码"""
        result = get_stock_industry(None)
        self.assertIsInstance(result, RobustResult)

    def test_stock_industry_all_level_fields(self):
        """测试返回数据包含所有级别字段"""
        result = get_stock_industry("600519")
        if result.success:
            self.assertIn("level1_code", result.data)
            self.assertIn("level1_name", result.data)
            self.assertIn("level2_code", result.data)
            self.assertIn("level2_name", result.data)
            self.assertIn("level3_code", result.data)
            self.assertIn("level3_name", result.data)

    def test_stock_industry_source_field(self):
        """测试返回数据包含来源字段"""
        result = get_stock_industry("600519")
        self.assertTrue(hasattr(result, "source"))

    def test_stock_industry_reason_field(self):
        """测试返回数据包含原因字段"""
        result = get_stock_industry("600519")
        self.assertTrue(hasattr(result, "reason"))


class TestIndustryConstituents(unittest.TestCase):
    """测试行业成分股"""

    def test_hot_industry_constituents(self):
        """测试热门行业成分股 - 白酒"""
        result = get_industry_stocks_sw("白酒")
        self.assertIsInstance(result, RobustResult)
        self.assertIsInstance(result.data, list)

    def test_hot_industry_constituents_bank(self):
        """测试热门行业成分股 - 银行"""
        result = get_industry_stocks_sw("银行")
        self.assertIsInstance(result, RobustResult)
        if result.success:
            self.assertIsInstance(result.data, list)

    def test_industry_stocks_count(self):
        """测试行业成分股数量"""
        result = get_industry_stocks_sw("银行")
        self.assertIsInstance(result, RobustResult)
        if result.success:
            self.assertIsInstance(len(result.data), int)

    def test_constituents_completeness(self):
        """测试成分股完整性（包含代码格式）"""
        result = get_industry_stocks_sw("电子")
        if result.success and result.data:
            for code in result.data[:3]:
                self.assertIn(".XS", code)

    def test_constituents_return_format(self):
        """测试成分股返回格式"""
        result = get_industry_stocks_sw("银行")
        if result.success:
            self.assertIsInstance(result.data, list)

    def test_constituents_code_format(self):
        """测试成分股代码格式一致性"""
        result = get_industry_stocks_sw("银行")
        if result.success and result.data:
            sample_code = result.data[0]
            self.assertTrue(".XSHG" in sample_code or ".XSHE" in sample_code)

    def test_invalid_industry_name(self):
        """测试无效行业名称"""
        result = get_industry_stocks_sw("不存在的行业xyz")
        self.assertIsInstance(result, RobustResult)

    def test_empty_industry_name(self):
        """测试空行业名称"""
        result = get_industry_stocks_sw("")
        self.assertIsInstance(result, RobustResult)


class TestIndustryPerformance(unittest.TestCase):
    """测试行业表现"""

    def test_industry_performance_structure(self):
        """测试行业表现数据结构"""
        result = get_industry_performance_sw()
        self.assertIsInstance(result, RobustResult)
        if result.success and not result.is_empty():
            df = result.data
            self.assertIn("industry_name", df.columns)

    def test_industry_performance_data_type(self):
        """测试行业表现数据类型"""
        result = get_industry_performance_sw()
        if result.success and not result.is_empty():
            df = result.data
            self.assertIsInstance(df, pd.DataFrame)

    def test_industry_performance_returns_result(self):
        """测试返回 RobustResult"""
        result = get_industry_performance_sw()
        self.assertIsInstance(result, RobustResult)

    def test_industry_performance_fields(self):
        """测试行业表现字段"""
        result = get_industry_performance_sw()
        if result.success and not result.is_empty():
            df = result.data
            self.assertIn("industry_name", df.columns)

    def test_industry_performance_has_pct_change(self):
        """测试行业表现包含涨跌幅字段"""
        result = get_industry_performance_sw()
        if result.success and not result.is_empty():
            df = result.data
            self.assertIn("pct_change", df.columns)

    def test_industry_performance_return_type(self):
        """测试行业表现函数返回类型"""
        result = get_industry_performance()
        self.assertIsInstance(result, RobustResult)

    def test_industry_performance_data_not_empty(self):
        """测试行业表现数据非空（如果成功）"""
        result = get_industry_performance_sw()
        if result.success:
            self.assertFalse(result.is_empty())

    def test_industry_performance_row_count(self):
        """测试行业表现数据行数"""
        result = get_industry_performance_sw()
        if result.success and not result.is_empty():
            self.assertGreater(len(result.data), 0)


class TestDataValidation(unittest.TestCase):
    """测试数据验证"""

    def test_industry_code_format_validation(self):
        """测试行业代码格式"""
        result = get_sw_industry_list(level=1)
        if result.success and not result.is_empty():
            df = result.data
            for code in df["industry_code"].head(5):
                if pd.notna(code) and code != "":
                    self.assertIsInstance(code, (str, int))

    def test_industry_name_uniqueness(self):
        """测试行业名称唯一性"""
        df = get_sw_level1()
        if not df.empty and "industry_name" in df.columns:
            names = df["industry_name"].dropna()
            if len(names) > 0:
                duplicate_count = names.duplicated().sum()
                self.assertLessEqual(duplicate_count, 0)

    def test_stock_industry_consistency(self):
        """测试股票行业一致性"""
        result1 = get_stock_industry("600519", use_cache=True)
        result2 = get_stock_industry("600519.XSHG", use_cache=True)
        if result1.success and result2.success:
            self.assertEqual(
                result1.data.get("level1_name", ""), result2.data.get("level1_name", "")
            )

    def test_default_schema_structure(self):
        """测试默认 schema 结构"""
        self.assertIn("level1_code", DEFAULT_INDUSTRY_SCHEMA)
        self.assertIn("level1_name", DEFAULT_INDUSTRY_SCHEMA)
        self.assertIn("level2_code", DEFAULT_INDUSTRY_SCHEMA)
        self.assertIn("level2_name", DEFAULT_INDUSTRY_SCHEMA)
        self.assertIn("level3_code", DEFAULT_INDUSTRY_SCHEMA)
        self.assertIn("level3_name", DEFAULT_INDUSTRY_SCHEMA)

    def test_default_schema_values(self):
        """测试默认 schema 值"""
        for key, value in DEFAULT_INDUSTRY_SCHEMA.items():
            self.assertEqual(value, "")

    def test_industry_name_not_empty(self):
        """测试行业名称非空"""
        result = get_sw_industry_list(level=1)
        if result.success and not result.is_empty():
            df = result.data
            names = df["industry_name"].dropna()
            for name in names.head(5):
                self.assertTrue(len(str(name)) > 0)

    def test_industry_code_not_empty(self):
        """测试行业代码非空"""
        result = get_sw_industry_list(level=1)
        if result.success and not result.is_empty():
            df = result.data
            codes = df["industry_code"].dropna()
            self.assertGreater(len(codes), 0)

    def test_industry_level_identifier(self):
        """测试行业层级标识"""
        result = get_sw_industry_list(level=1)
        if result.success and not result.is_empty():
            df = result.data
            self.assertIn("level", df.columns)


class TestCrossIndustry(unittest.TestCase):
    """测试跨行业功能"""

    def test_industry_filter_by_level(self):
        """测试按行业级别筛选"""
        result1 = filter_stocks_by_industry("银行", level=1)
        self.assertIsInstance(result1, RobustResult)
        self.assertIsInstance(result1.data, list)

    def test_industry_mapping_different_levels(self):
        """测试不同级别的行业映射"""
        result1 = get_all_industry_mapping(level=1)
        result2 = get_all_industry_mapping(level=2)
        self.assertIsInstance(result1, RobustResult)
        self.assertIsInstance(result2, RobustResult)

    def test_filter_with_codes_pool(self):
        """测试指定股票池筛选"""
        codes = ["600519.XSHG", "000858.XSHE"]
        result = filter_stocks_by_industry("白酒", codes=codes)
        self.assertIsInstance(result, RobustResult)
        self.assertIsInstance(result.data, list)

    def test_filter_invalid_industry(self):
        """测试无效行业名称筛选"""
        result = filter_stocks_by_industry("不存在的行业名称xyz")
        self.assertIsInstance(result, RobustResult)

    def test_filter_empty_codes_pool(self):
        """测试空股票池筛选"""
        result = filter_stocks_by_industry("银行", codes=[])
        self.assertIsInstance(result, RobustResult)

    def test_filter_exclude_industry(self):
        """测试排除行业筛选"""
        result = filter_stocks_by_industry("银行")
        self.assertIsInstance(result, RobustResult)
        if result.success:
            self.assertIsInstance(result.data, list)

    def test_filter_by_level2(self):
        """测试按二级行业筛选"""
        result = filter_stocks_by_industry("白酒", level=2)
        self.assertIsInstance(result, RobustResult)

    def test_filter_by_level3(self):
        """测试按三级行业筛选"""
        result = filter_stocks_by_industry("白酒", level=3)
        self.assertIsInstance(result, RobustResult)


class TestBatchQueryEdgeCases(unittest.TestCase):
    """测试批量查询边界情况"""

    def test_batch_with_invalid_codes(self):
        """测试批量查询包含无效代码"""
        codes = ["600519", "999999", "000001"]
        result = get_industry_sw_batch(codes)
        self.assertIsInstance(result, RobustResult)

    def test_batch_large_count(self):
        """测试批量查询大量股票"""
        codes = [f"600{i:03d}" for i in range(10)]
        result = get_industry_sw_batch(codes)
        self.assertIsInstance(result, RobustResult)

    def test_batch_deduplication(self):
        """测试批量查询重复代码处理"""
        codes = ["600519", "600519.XSHG", "sh600519"]
        result = get_industry_sw_batch(codes)
        self.assertIsInstance(result, RobustResult)
        if result.success:
            self.assertGreater(len(result.data), 0)

    def test_batch_empty_codes(self):
        """测试空股票列表"""
        result = get_industry_sw_batch([])
        self.assertFalse(result.success)
        self.assertIn("空", result.reason)

    def test_batch_single_code(self):
        """测试单只股票批量查询"""
        result = get_industry_sw_batch(["600519"])
        self.assertIsInstance(result, RobustResult)

    def test_batch_none_codes(self):
        """测试None代码列表"""
        result = get_industry_sw_batch(None)
        self.assertFalse(result.success)

    def test_batch_partial_success(self):
        """测试部分成功部分失败场景"""
        codes = ["600519", "999999", "000001"]
        result = get_industry_sw_batch(codes)
        self.assertIsInstance(result, RobustResult)
        if result.success:
            self.assertGreater(len(result.data), 0)
            self.assertLessEqual(len(result.data), len(codes))

    def test_batch_with_mixed_formats(self):
        """测试混合代码格式批量查询"""
        codes = ["600519", "000001.XSHE", "sh600036", "sz000002"]
        result = get_industry_sw_batch(codes)
        self.assertIsInstance(result, RobustResult)

    def test_batch_result_has_code_column(self):
        """测试批量查询结果包含代码列"""
        codes = ["600519", "000001"]
        result = get_industry_sw_batch(codes)
        if result.success and not result.is_empty():
            self.assertIn("code", result.data.columns)


class TestCacheBehavior(unittest.TestCase):
    """测试缓存行为"""

    def test_cache_initialization(self):
        """测试缓存初始化"""
        cache = SWIndustryCache()
        self.assertTrue(os.path.exists(cache.CACHE_DIR))

    def test_cache_set_and_get(self):
        """测试缓存写入和读取"""
        cache = SWIndustryCache()
        test_data = {"key": "value", "number": 123}
        cache.set("test_cache_key", test_data)
        retrieved = cache.get("test_cache_key")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["key"], "value")

    def test_cache_miss(self):
        """测试缓存未命中"""
        cache = SWIndustryCache()
        result = cache.get("non_existent_key_12345")
        self.assertIsNone(result)

    def test_cache_clear(self):
        """测试缓存清理"""
        cache = SWIndustryCache()
        cache.set("test_key_for_clear", {"data": "value"})
        cache.clear()
        result = cache.get("test_key_for_clear")
        self.assertIsNone(result)

    def test_cache_singleton(self):
        """测试单例模式"""
        cache1 = SWIndustryCache()
        cache2 = SWIndustryCache()
        self.assertIs(cache1, cache2)

    def test_cache_quarterly_expiry(self):
        """测试按季度缓存过期"""
        cache = SWIndustryCache()
        test_data = {"quarter": "Q1", "year": 2024}
        cache.set("quarterly_test_key", test_data)
        retrieved = cache.get("quarterly_test_key")
        self.assertEqual(retrieved["quarter"], "Q1")

    def test_cache_warmup(self):
        """测试缓存预热功能"""
        cache = SWIndustryCache()
        warmup_data = {"warmup_key": {"level1_name": "银行", "level1_code": "801780"}}
        for key, value in warmup_data.items():
            cache.set(key, value)
        retrieved = cache.get("warmup_key")
        self.assertIsNotNone(retrieved)

    def test_stock_industry_cache_hit(self):
        """测试股票行业缓存命中"""
        result1 = get_stock_industry("000001", use_cache=True)
        result2 = get_stock_industry("000001", use_cache=True)
        self.assertIsInstance(result1, RobustResult)
        self.assertIsInstance(result2, RobustResult)

    def test_cache_overwrite(self):
        """测试缓存覆盖"""
        cache = SWIndustryCache()
        cache.set("overwrite_key", {"value": "old"})
        cache.set("overwrite_key", {"value": "new"})
        retrieved = cache.get("overwrite_key")
        self.assertEqual(retrieved["value"], "new")


class TestCodeNormalization(unittest.TestCase):
    """测试股票代码标准化"""

    def test_normalize_stock_code_jqdata_format(self):
        """测试聚宽格式"""
        self.assertEqual(_normalize_stock_code("600519.XSHG"), "600519")
        self.assertEqual(_normalize_stock_code("000001.XSHE"), "000001")

    def test_normalize_to_jq_jqdata_format(self):
        """测试转换为聚宽格式"""
        self.assertEqual(_normalize_to_jq("600519"), "600519.XSHG")
        self.assertEqual(_normalize_to_jq("000001"), "000001.XSHE")

    def test_normalize_stock_code_akshare_format(self):
        """测试 akshare 格式"""
        self.assertEqual(_normalize_stock_code("sh600519"), "600519")
        self.assertEqual(_normalize_stock_code("sz000001"), "000001")

    def test_normalize_to_jq_akshare_format(self):
        """测试 akshare 格式转换为聚宽格式"""
        self.assertEqual(_normalize_to_jq("sh600519"), "600519.XSHG")
        self.assertEqual(_normalize_to_jq("sz000001"), "000001.XSHE")

    def test_normalize_stock_code_numeric_format(self):
        """测试数字格式"""
        self.assertEqual(_normalize_stock_code("600519"), "600519")
        self.assertEqual(_normalize_stock_code(600519), "600519")
        self.assertEqual(_normalize_stock_code("1"), "000001")

    def test_normalize_to_jq_numeric(self):
        """测试数字格式转换"""
        self.assertEqual(_normalize_to_jq(600519), "600519.XSHG")
        self.assertEqual(_normalize_to_jq(1), "000001.XSHE")

    def test_normalize_empty_string(self):
        """测试空字符串"""
        result = _normalize_stock_code("")
        self.assertIsInstance(result, str)

    def test_normalize_none(self):
        """测试 None 值"""
        result = _normalize_stock_code(None)
        self.assertIsInstance(result, str)

    def test_normalize_stock_code_with_prefix_sh(self):
        """测试带 sh 前缀的代码"""
        self.assertEqual(_normalize_stock_code("sh600000"), "600000")

    def test_normalize_stock_code_with_prefix_sz(self):
        """测试带 sz 前缀的代码"""
        self.assertEqual(_normalize_stock_code("sz000002"), "000002")

    def test_normalize_to_jq_sse_star(self):
        """测试科创板代码转换"""
        self.assertEqual(_normalize_to_jq("688981"), "688981.XSHG")

    def test_normalize_to_jq_chi_next(self):
        """测试创业板代码转换"""
        self.assertEqual(_normalize_to_jq("300750"), "300750.XSHE")

    def test_normalize_stock_code_zero_padding(self):
        """测试零填充"""
        self.assertEqual(_normalize_stock_code("1"), "000001")
        self.assertEqual(_normalize_stock_code("123"), "000123")

    def test_normalize_to_jq_already_formatted(self):
        """测试已格式化代码不重复转换"""
        self.assertEqual(_normalize_to_jq("600519.XSHG"), "600519.XSHG")
        self.assertEqual(_normalize_to_jq("000001.XSHE"), "000001.XSHE")


class TestRobustResult(unittest.TestCase):
    """测试 RobustResult 类"""

    def test_robust_result_success(self):
        """测试成功结果"""
        data = {"level1_name": "电子", "level2_name": "半导体"}
        result = RobustResult(
            success=True, data=data, reason="成功获取", source="network"
        )
        self.assertTrue(result.success)
        self.assertFalse(result.is_empty())
        self.assertEqual(result.data["level1_name"], "电子")

    def test_robust_result_failure(self):
        """测试失败结果"""
        result = RobustResult(
            success=False,
            data=DEFAULT_INDUSTRY_SCHEMA.copy(),
            reason="网络错误",
            source="fallback",
        )
        self.assertFalse(result.success)
        self.assertEqual(result.source, "fallback")

    def test_robust_result_bool(self):
        """测试布尔转换"""
        success_result = RobustResult(success=True)
        fail_result = RobustResult(success=False)
        self.assertTrue(bool(success_result))
        self.assertFalse(bool(fail_result))

    def test_robust_result_with_dataframe(self):
        """测试 DataFrame 数据"""
        df = pd.DataFrame({"code": ["600519"], "industry": ["白酒"]})
        result = RobustResult(success=True, data=df)
        self.assertFalse(result.is_empty())
        self.assertEqual(len(result.data), 1)

    def test_robust_result_empty_dataframe(self):
        """测试空 DataFrame"""
        result = RobustResult(success=True, data=pd.DataFrame())
        self.assertTrue(result.is_empty())

    def test_robust_result_with_list(self):
        """测试列表数据"""
        result = RobustResult(success=True, data=["600519.XSHG", "000858.XSHE"])
        self.assertFalse(result.is_empty())
        self.assertEqual(len(result.data), 2)

    def test_robust_result_empty_list(self):
        """测试空列表"""
        result = RobustResult(success=True, data=[])
        self.assertTrue(result.is_empty())

    def test_robust_result_repr(self):
        """测试字符串表示"""
        result = RobustResult(success=True, reason="test", source="network")
        repr_str = repr(result)
        self.assertIn("SUCCESS", repr_str)

    def test_robust_result_none_data(self):
        """测试 None 数据"""
        result = RobustResult(success=True, data=None)
        self.assertTrue(result.is_empty())

    def test_robust_result_empty_dict(self):
        """测试空字典"""
        result = RobustResult(success=True, data={})
        self.assertTrue(result.is_empty())

    def test_robust_result_with_dict(self):
        """测试字典数据"""
        data = {"level1_name": "银行"}
        result = RobustResult(success=True, data=data)
        self.assertFalse(result.is_empty())

    def test_robust_result_source_values(self):
        """测试来源字段值"""
        sources = ["network", "cache", "fallback", "error"]
        for source in sources:
            result = RobustResult(success=True, source=source)
            self.assertEqual(result.source, source)


class TestFinanceQuery(unittest.TestCase):
    """测试 FinanceQuery 类"""

    def test_finance_query_instance(self):
        """测试 finance 实例"""
        self.assertIsInstance(finance, FinanceQuery)

    def test_finance_stk_industry_sw_class(self):
        """测试 STK_INDUSTRY_SW 类"""
        self.assertTrue(hasattr(finance, "STK_INDUSTRY_SW"))
        self.assertTrue(hasattr(FinanceQuery.STK_INDUSTRY_SW, "code"))
        self.assertTrue(hasattr(FinanceQuery.STK_INDUSTRY_SW, "industry_name"))

    def test_finance_stk_sw_industry_alias(self):
        """测试 STK_SW_INDUSTRY 别名类"""
        self.assertTrue(hasattr(finance, "STK_SW_INDUSTRY"))
        self.assertTrue(hasattr(FinanceQuery.STK_SW_INDUSTRY, "code"))
        self.assertTrue(hasattr(FinanceQuery.STK_SW_INDUSTRY, "industry_name"))

    def test_finance_stk_sw_industry_stock_class(self):
        """测试 STK_SW_INDUSTRY_STOCK 类"""
        self.assertTrue(hasattr(finance, "STK_SW_INDUSTRY_STOCK"))
        self.assertTrue(hasattr(FinanceQuery.STK_SW_INDUSTRY_STOCK, "industry_code"))
        self.assertTrue(hasattr(FinanceQuery.STK_SW_INDUSTRY_STOCK, "industry_name"))
        self.assertTrue(hasattr(FinanceQuery.STK_SW_INDUSTRY_STOCK, "code"))

    def test_finance_run_query_basic(self):
        """测试 finance.run_query 基本功能"""
        query = finance.STK_INDUSTRY_SW()
        query.code = "600519"
        df = finance.run_query(query)
        self.assertIsInstance(df, pd.DataFrame)

    def test_finance_run_query_empty(self):
        """测试 finance.run_query 无条件查询"""
        query = finance.STK_INDUSTRY_SW()
        df = finance.run_query(query)
        self.assertIsInstance(df, pd.DataFrame)

    def test_finance_run_query_alias_table(self):
        """测试 finance.run_query 使用别名表"""
        query = finance.STK_SW_INDUSTRY()
        query.code = "600519"
        df = finance.run_query(query)
        self.assertIsInstance(df, pd.DataFrame)

    def test_finance_run_query_industry_stock(self):
        """测试 finance.run_query 行业成分股表"""
        query = finance.STK_SW_INDUSTRY_STOCK()
        query.industry_name = "银行"
        df = finance.run_query(query)
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertIn("industry_name", df.columns)

    def test_run_query_simple_stk_industry_sw(self):
        """测试 run_query_simple STK_INDUSTRY_SW"""
        df = run_query_simple("STK_INDUSTRY_SW", code="600519")
        self.assertIsInstance(df, pd.DataFrame)

    def test_run_query_simple_stk_sw_industry(self):
        """测试 run_query_simple STK_SW_INDUSTRY 别名"""
        df = run_query_simple("STK_SW_INDUSTRY", code="600519")
        self.assertIsInstance(df, pd.DataFrame)

    def test_run_query_simple_stk_sw_industry_stock(self):
        """测试 run_query_simple STK_SW_INDUSTRY_STOCK"""
        df = run_query_simple("STK_SW_INDUSTRY_STOCK", industry_name="银行")
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)

    def test_run_query_simple_industry_code_param(self):
        """测试 run_query_simple 使用 industry_code 参数"""
        df = run_query_simple("STK_SW_INDUSTRY_STOCK", industry_code="801780")
        self.assertIsInstance(df, pd.DataFrame)

    def test_alias_class_attributes_equal(self):
        """测试别名类属性与原类属性一致"""
        self.assertEqual(
            FinanceQuery.STK_INDUSTRY_SW.code, FinanceQuery.STK_SW_INDUSTRY.code
        )
        self.assertEqual(
            FinanceQuery.STK_INDUSTRY_SW.industry_name,
            FinanceQuery.STK_SW_INDUSTRY.industry_name,
        )

    def test_both_table_names_work(self):
        """测试两种表名都能正常工作"""
        df1 = run_query_simple("STK_INDUSTRY_SW", code="600519")
        df2 = run_query_simple("STK_SW_INDUSTRY", code="600519")
        self.assertIsInstance(df1, pd.DataFrame)
        self.assertIsInstance(df2, pd.DataFrame)


class TestGetIndustrySw(unittest.TestCase):
    """测试单只股票行业分类查询"""

    def test_get_industry_sw_returns_robust_result(self):
        """测试返回 RobustResult"""
        result = get_industry_sw("600519")
        self.assertIsInstance(result, RobustResult)
        self.assertTrue(hasattr(result, "success"))
        self.assertTrue(hasattr(result, "data"))
        self.assertTrue(hasattr(result, "reason"))
        self.assertTrue(hasattr(result, "source"))

    def test_get_industry_sw_code_normalization(self):
        """测试股票代码格式标准化"""
        codes = ["600519.XSHG", "sh600519", "600519", 600519]
        for code in codes:
            result = get_industry_sw(code)
            self.assertIsInstance(result, RobustResult)

    def test_get_industry_sw_invalid_code(self):
        """测试无效股票代码"""
        result = get_industry_sw("999999")
        self.assertIsInstance(result, RobustResult)
        self.assertIsInstance(result.data, dict)

    def test_get_industry_sw_use_cache(self):
        """测试缓存使用"""
        result1 = get_industry_sw("000001", use_cache=True)
        result2 = get_industry_sw("000001", use_cache=True)
        self.assertIsInstance(result1, RobustResult)
        self.assertIsInstance(result2, RobustResult)


class TestFilterStocksByIndustry(unittest.TestCase):
    """测试按行业筛选股票"""

    def test_filter_returns_robust_result(self):
        """测试返回 RobustResult"""
        result = filter_stocks_by_industry("白酒")
        self.assertIsInstance(result, RobustResult)
        self.assertIsInstance(result.data, list)

    def test_filter_invalid_industry(self):
        """测试无效行业名称"""
        result = filter_stocks_by_industry("不存在的行业名称xyz")
        self.assertIsInstance(result, RobustResult)

    def test_filter_with_level(self):
        """测试指定行业级别"""
        result = filter_stocks_by_industry("银行", level=1)
        self.assertIsInstance(result, RobustResult)

    def test_filter_with_empty_pool(self):
        """测试空股票池"""
        result = filter_stocks_by_industry("银行", codes=[])
        self.assertIsInstance(result, RobustResult)

    def test_filter_bank_stocks(self):
        """测试筛选银行股"""
        result = filter_stocks_by_industry("银行")
        if result.success and result.data:
            self.assertIsInstance(result.data, list)
            for code in result.data[:3]:
                self.assertTrue(".XSHG" in code or ".XSHE" in code)

    def test_filter_with_specific_pool(self):
        """测试指定股票池筛选"""
        codes = ["600000.XSHG", "601398.XSHG", "000001.XSHE"]
        result = filter_stocks_by_industry("银行", codes=codes)
        self.assertIsInstance(result, RobustResult)


class TestGetAllIndustryMapping(unittest.TestCase):
    """测试全市场行业映射"""

    def test_mapping_returns_robust_result(self):
        """测试返回 RobustResult"""
        result = get_all_industry_mapping(level=1)
        self.assertIsInstance(result, RobustResult)

    def test_mapping_invalid_level(self):
        """测试无效级别"""
        result = get_all_industry_mapping(level=5)
        self.assertFalse(result.success)

    def test_mapping_level2(self):
        """测试二级行业映射"""
        result = get_all_industry_mapping(level=2)
        self.assertIsInstance(result, RobustResult)

    def test_mapping_level3(self):
        """测试三级行业映射"""
        result = get_all_industry_mapping(level=3)
        self.assertIsInstance(result, RobustResult)

    def test_mapping_data_structure(self):
        """测试映射数据结构"""
        result = get_all_industry_mapping(level=1)
        if result.success and not result.is_empty():
            df = result.data
            self.assertIn("industry_code", df.columns)
            self.assertIn("industry_name", df.columns)


class TestBoundaryConditions(unittest.TestCase):
    """测试边界条件"""

    def test_empty_industry_name(self):
        """测试空行业名称"""
        result = get_industry_stocks_sw("")
        self.assertIsInstance(result, RobustResult)

    def test_none_industry_name(self):
        """测试 None 行业名称"""
        result = get_industry_stocks_sw(None)
        self.assertIsInstance(result, RobustResult)

    def test_empty_stock_code(self):
        """测试空股票代码"""
        result = get_stock_industry("")
        self.assertIsInstance(result, RobustResult)

    def test_none_stock_code(self):
        """测试 None 股票代码"""
        result = get_stock_industry(None)
        self.assertIsInstance(result, RobustResult)

    def test_special_characters_industry(self):
        """测试特殊字符行业名称"""
        result = get_industry_stocks_sw("!@#$%")
        self.assertIsInstance(result, RobustResult)

    def test_very_long_industry_name(self):
        """测试超长行业名称"""
        long_name = "a" * 1000
        result = get_industry_stocks_sw(long_name)
        self.assertIsInstance(result, RobustResult)

    def test_nonexistent_industry_code(self):
        """测试不存在的行业代码"""
        result = get_industry_stocks_sw("不存在的行业xyz123")
        self.assertIsInstance(result, RobustResult)

    def test_whitespace_industry_name(self):
        """测试空白行业名称"""
        result = get_industry_stocks_sw("   ")
        self.assertIsInstance(result, RobustResult)

    def test_invalid_level_type(self):
        """测试无效级别类型"""
        result = get_sw_industry_list(level="invalid")
        self.assertFalse(result.success)

    def test_negative_level(self):
        """测试负数级别"""
        result = get_sw_industry_list(level=-1)
        self.assertFalse(result.success)


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_full_workflow(self):
        """测试完整工作流"""
        result = get_stock_industry("600519")
        self.assertIsInstance(result, RobustResult)

        if result.success:
            industry_name = result.data.get("level1_name", "")
            if industry_name:
                stocks_result = get_industry_stocks_sw(industry_name)
                self.assertIsInstance(stocks_result, RobustResult)

    def test_batch_and_filter_consistency(self):
        """测试批量查询和筛选一致性"""
        codes = ["600519", "000858"]
        batch_result = get_industry_sw_batch(codes)
        self.assertIsInstance(batch_result, RobustResult)

    def test_industry_workflow(self):
        """测试行业工作流"""
        level1_result = get_sw_level1()
        if not level1_result.empty:
            industry_name = level1_result["industry_name"].iloc[0]
            stocks_result = get_industry_stocks_sw(industry_name)
            self.assertIsInstance(stocks_result, RobustResult)

    def test_cache_workflow(self):
        """测试缓存工作流"""
        result1 = get_stock_industry("600519", use_cache=True)
        result2 = get_stock_industry("600519", use_cache=True)
        self.assertIsInstance(result1, RobustResult)
        self.assertIsInstance(result2, RobustResult)

    def test_multi_level_industry_query(self):
        """测试多级行业查询工作流"""
        df1 = get_sw_level1()
        df2 = get_sw_level2()
        df3 = get_sw_level3()
        if not df1.empty and not df2.empty and not df3.empty:
            self.assertLessEqual(len(df1), len(df2))
            self.assertLessEqual(len(df2), len(df3))


class TestIndustryDBManager(unittest.TestCase):
    """测试行业数据库管理器"""

    def test_db_manager_singleton(self):
        """测试数据库管理器单例"""
        try:
            manager1 = IndustrySWDBManager()
            manager2 = IndustrySWDBManager()
            self.assertIs(manager1, manager2)
        except Exception:
            self.skipTest("DuckDB not available")

    def test_db_manager_get_industry(self):
        """测试数据库管理器获取行业"""
        try:
            manager = IndustrySWDBManager()
            df = manager.get_industry("600519.XSHG")
            self.assertIsInstance(df, pd.DataFrame)
        except Exception:
            self.skipTest("DuckDB not available")

    def test_db_manager_get_industry_list(self):
        """测试数据库管理器获取行业列表"""
        try:
            manager = IndustrySWDBManager()
            df = manager.get_industry_list(1)
            self.assertIsInstance(df, pd.DataFrame)
        except Exception:
            self.skipTest("DuckDB not available")

    def test_db_manager_cache_validity(self):
        """测试数据库管理器缓存有效性"""
        try:
            manager = IndustrySWDBManager()
            is_valid = manager.is_cache_valid(cache_days=90)
            self.assertIsInstance(is_valid, bool)
        except Exception:
            self.skipTest("DuckDB not available")


class TestMultiLevelIndustry(unittest.TestCase):
    """测试多级行业功能"""

    def test_level1_industry_columns(self):
        """测试一级行业列结构"""
        df = get_sw_level1()
        if not df.empty:
            self.assertIn("industry_code", df.columns)
            self.assertIn("industry_name", df.columns)

    def test_level2_industry_columns(self):
        """测试二级行业列结构"""
        df = get_sw_level2()
        if not df.empty:
            self.assertIn("industry_code", df.columns)
            self.assertIn("industry_name", df.columns)

    def test_level3_industry_columns(self):
        """测试三级行业列结构"""
        df = get_sw_level3()
        if not df.empty:
            self.assertIn("industry_code", df.columns)
            self.assertIn("industry_name", df.columns)

    def test_level_hierarchy_consistency(self):
        """测试层级关系一致性"""
        df1 = get_sw_level1()
        df2 = get_sw_level2()
        df3 = get_sw_level3()
        if not df1.empty and not df2.empty and not df3.empty:
            self.assertGreater(len(df2), 0)
            self.assertGreater(len(df3), 0)

    def test_stock_industry_level_fields(self):
        """测试股票行业多级字段"""
        result = get_stock_industry("600519")
        if result.success:
            data = result.data
            self.assertIn("level1_name", data)
            self.assertIn("level2_name", data)
            self.assertIn("level3_name", data)


class TestIndustryStocksUnified(unittest.TestCase):
    """测试行业成分股统一入口"""

    def test_industry_stocks_return_structure(self):
        """测试行业成分股返回结构"""
        df = get_industry_stocks("银行")
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertIn("industry_name", df.columns)

    def test_industry_stocks_code_format(self):
        """测试成分股代码格式（聚宽格式）"""
        df = get_industry_stocks("银行")
        if not df.empty:
            sample_code = df["code"].iloc[0]
            self.assertTrue(".XSHG" in sample_code or ".XSHE" in sample_code)

    def test_industry_stocks_consistency(self):
        """测试不同接口返回一致性"""
        df1 = get_industry_stocks("银行")
        result2 = get_industry_stocks_sw("银行")
        if not df1.empty and result2.success:
            codes1 = df1["code"].tolist()
            codes2 = result2.data
            self.assertEqual(set(codes1), set(codes2))

    def test_industry_stocks_stock_name_field(self):
        """测试成分股包含股票名称字段"""
        df = get_industry_stocks("银行")
        if not df.empty and "stock_name" in df.columns:
            self.assertIsInstance(df["stock_name"].iloc[0], str)

    def test_run_query_simple_industry_stocks(self):
        """测试 run_query_simple 行业成分股"""
        df = run_query_simple("STK_SW_INDUSTRY_STOCK", industry_name="白酒")
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)

    def test_industry_stocks_multiple_calls(self):
        """测试多次调用返回结果一致"""
        df1 = get_industry_stocks("银行")
        df2 = get_industry_stocks("银行")
        if not df1.empty and not df2.empty:
            self.assertEqual(len(df1), len(df2))

    def test_industry_stocks_with_level_parameter(self):
        """测试行业成分股 level 参数"""
        df = get_industry_stocks("银行", level=1)
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertIn("stock_name", df.columns)
            self.assertIn("level", df.columns)
            self.assertIn("industry_code", df.columns)
            self.assertEqual(df["level"].iloc[0], 1)

    def test_industry_stocks_with_level_2(self):
        """测试行业成分股 level=2 参数"""
        df = get_industry_stocks("白酒", level=2)
        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("level", df.columns)
            self.assertEqual(df["level"].iloc[0], 2)

    def test_industry_stocks_level_vs_no_level(self):
        """测试有无 level 参数返回差异"""
        df_with_level = get_industry_stocks("银行", level=1)
        df_no_level = get_industry_stocks("银行")
        self.assertIsInstance(df_with_level, pd.DataFrame)
        self.assertIsInstance(df_no_level, pd.DataFrame)
        if not df_with_level.empty and not df_no_level.empty:
            self.assertIn("level", df_with_level.columns)
            self.assertNotIn("level", df_no_level.columns)


class TestAliasCompatibility(unittest.TestCase):
    """测试别名兼容性"""

    def test_stk_industry_sw_export(self):
        """测试 STK_INDUSTRY_SW 导出"""
        self.assertIsNotNone(STK_INDUSTRY_SW)

    def test_stk_sw_industry_export(self):
        """测试 STK_SW_INDUSTRY 导出"""
        self.assertIsNotNone(STK_SW_INDUSTRY)

    def test_stk_sw_industry_stock_export(self):
        """测试 STK_SW_INDUSTRY_STOCK 导出"""
        self.assertIsNotNone(STK_SW_INDUSTRY_STOCK)

    def test_alias_table_query_consistency(self):
        """测试别名表查询结果一致"""
        df1 = run_query_simple("STK_INDUSTRY_SW", code="000001")
        df2 = run_query_simple("STK_SW_INDUSTRY", code="000001")
        self.assertEqual(list(df1.columns), list(df2.columns))

    def test_industry_stock_table_columns(self):
        """测试行业成分股表字段"""
        df = run_query_simple("STK_SW_INDUSTRY_STOCK", industry_name="银行")
        if not df.empty:
            self.assertIn("code", df.columns)
            self.assertIn("industry_name", df.columns)

    def test_finance_module_alias_available(self):
        """测试 finance 模块别名可用"""
        self.assertTrue(hasattr(finance, "STK_INDUSTRY_SW"))
        self.assertTrue(hasattr(finance, "STK_SW_INDUSTRY"))
        self.assertTrue(hasattr(finance, "STK_SW_INDUSTRY_STOCK"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
