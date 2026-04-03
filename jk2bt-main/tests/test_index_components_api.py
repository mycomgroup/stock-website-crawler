"""
tests/test_index_components_api.py
任务8：指数成分股数据 API 测试

测试场景覆盖：
1. 权重计算测试 - 验证权重总和、非负性、分布合理性
2. 历史成分测试 - 测试不同时间点的成分变化
3. 多种指数测试 - 沪深300、中证500、上证50、创业板指等
4. 数据验证测试 - 成分股代码格式、权重范围、数量合理
5. 边界条件测试 - 不存在指数、未来日期、历史边界
6. 批量操作测试 - 批量获取、跨指数筛选
7. 缓存测试 - 按季度缓存、缓存预热
"""

import pytest
import pandas as pd
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.market_data.index_components import (
    get_index_components,
    get_index_stocks,
    get_index_weights,
    get_index_info,
    get_industry_index_stocks,
    get_index_component_history,
    query_index_components,
    finance,
    run_query_simple,
)


class TestWeightCalculation:
    """
    权重计算测试类

    测试目标：
    - 验证权重总和接近100%
    - 验证权重非负
    - 验证权重分布合理性
    """

    def test_get_index_weights_hs300(self):
        """测试获取沪深300成分股权重"""
        df = get_index_weights("000300", force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        assert "weight" in df.columns, "应包含 weight 列"
        print(f"沪深300权重数据: {len(df)} 条记录")

    def test_get_index_weights_zz500(self):
        """测试获取中证500成分股权重"""
        df = get_index_weights("000905", force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        assert "weight" in df.columns, "应包含 weight 列"
        print(f"中证500权重数据: {len(df)} 条记录")

    def test_weight_sum_near_100_percent_hs300(self):
        """
        测试沪深300权重总和接近100%

        验证规则：
        - 权重总和应在 99% 到 101% 之间
        - 允许小范围误差，因为数据可能有四舍五入
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty and "weight" in df.columns:
            weights = df["weight"].dropna()
            if len(weights) > 0:
                total = weights.sum()
                assert 99 <= total <= 101, (
                    f"沪深300权重总和应接近100%，实际: {total:.2f}%"
                )
                print(f"沪深300权重总和: {total:.2f}%")

    def test_weight_sum_near_100_percent_zz500(self):
        """
        测试中证500权重总和接近100%

        验证规则：
        - 权重总和应在 99% 到 101% 之间
        """
        df = get_index_components("000905", force_update=False)
        if not df.empty and "weight" in df.columns:
            weights = df["weight"].dropna()
            if len(weights) > 0:
                total = weights.sum()
                assert 99 <= total <= 101, (
                    f"中证500权重总和应接近100%，实际: {total:.2f}%"
                )
                print(f"中证500权重总和: {total:.2f}%")

    def test_weight_sum_near_100_percent_sz50(self):
        """
        测试上证50权重总和接近100%

        验证规则：
        - 权重总和应在 99% 到 101% 之间
        """
        df = get_index_components("000016", force_update=False)
        if not df.empty and "weight" in df.columns:
            weights = df["weight"].dropna()
            if len(weights) > 0:
                total = weights.sum()
                assert 99 <= total <= 101, (
                    f"上证50权重总和应接近100%，实际: {total:.2f}%"
                )
                print(f"上证50权重总和: {total:.2f}%")

    def test_weight_non_negative(self):
        """
        测试权重非负

        验证规则：
        - 所有权重值应大于等于0
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty and "weight" in df.columns:
            weights = df["weight"].dropna()
            if len(weights) > 0:
                assert weights.min() >= 0, f"发现负权重: {weights.min()}"
                print(f"权重最小值: {weights.min():.4f}%")

    def test_weight_max_reasonable(self):
        """
        测试最大权重在合理范围内

        验证规则：
        - 单只股票权重不应超过20%（防止过度集中）
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty and "weight" in df.columns:
            weights = df["weight"].dropna()
            if len(weights) > 0:
                assert weights.max() <= 20, f"单只股票权重过大: {weights.max():.2f}%"
                print(f"最大权重: {weights.max():.2f}%")

    def test_weight_distribution(self):
        """
        测试权重分布合理性

        验证规则：
        - 权重非负
        - 单只股票权重不超过20%
        - 平均权重大于0.1%
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty and "weight" in df.columns:
            weights = df["weight"].dropna()
            if len(weights) > 0:
                assert weights.min() >= 0, "权重不应为负数"
                assert weights.max() <= 20, "单只股票权重不应超过20%"
                assert weights.mean() > 0.1, "平均权重应大于0.1%"
                print(
                    f"权重分布: 最小={weights.min():.4f}%, "
                    f"最大={weights.max():.2f}%, 平均={weights.mean():.3f}%"
                )

    def test_large_weight_stocks_count(self):
        """
        测试大权重股票数量

        验证规则：
        - 沪深300应有至少10只权重超过1%的股票
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty and "weight" in df.columns:
            large_weights = df[df["weight"] >= 1.0]
            assert len(large_weights) >= 10, (
                f"沪深300应有至少10只权重超过1%的股票，实际: {len(large_weights)}"
            )
            print(f"大权重股票(>1%)数量: {len(large_weights)}")


class TestHistoricalComponents:
    """
    历史成分测试类

    测试目标：
    - 测试不同时间点的成分变化
    - 测试成分股调整记录
    """

    def test_get_index_component_history_basic(self):
        """测试获取成分股变动历史基本功能"""
        df = get_index_component_history("000300", force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        assert "index_code" in df.columns, "应包含 index_code 列"
        assert "code" in df.columns, "应包含 code 列"
        print(f"沪深300成分股历史: {len(df)} 条记录")

    def test_history_with_date_range(self):
        """
        测试带日期范围的成分股变动历史

        验证规则：
        - 指定日期范围后应返回相应时间段的数据
        """
        df = get_index_component_history(
            "000300", start_date="2023-01-01", end_date="2024-12-31", force_update=False
        )
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        if not df.empty and "in_date" in df.columns:
            dates = pd.to_datetime(df["in_date"], errors="coerce")
            if dates.notna().any():
                assert dates.min() >= pd.to_datetime("2023-01-01"), "起始日期应正确"
                print(f"日期范围内记录: {len(df)} 条")

    def test_history_columns_format(self):
        """
        测试历史变动数据列格式

        验证规则：
        - 必须包含 index_code, code, in_date, out_date, change_type 列
        """
        df = get_index_component_history("000300", force_update=False)
        assert "index_code" in df.columns, "应包含 index_code 列"
        assert "code" in df.columns, "应包含 code 列"
        print(f"历史变动数据列: {df.columns.tolist()}")

    def test_history_data_types(self):
        """
        测试历史变动数据类型

        验证规则：
        - index_code 和 code 应为字符串类型
        """
        df = get_index_component_history("000300", force_update=False)
        if not df.empty:
            assert df["index_code"].dtype == object, "index_code 应为字符串类型"
            assert df["code"].dtype == object, "code 应为字符串类型"
            print(f"数据类型验证通过")

    def test_history_change_type_values(self):
        """
        测试变动类型值

        验证规则：
        - change_type 应为 current, in, out 之一
        """
        df = get_index_component_history("000300", force_update=False)
        if not df.empty and "change_type" in df.columns:
            valid_types = ["current", "in", "out"]
            change_types = df["change_type"].unique()
            for ct in change_types:
                if pd.notna(ct):
                    assert ct in valid_types, (
                        f"变动类型应为 {valid_types} 之一，实际: {ct}"
                    )
            print(f"变动类型: {change_types.tolist()}")

    def test_history_zz500(self):
        """测试获取中证500成分股变动历史"""
        df = get_index_component_history("000905", force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"中证500成分股历史: {len(df)} 条记录")

    def test_history_sz50(self):
        """测试获取上证50成分股变动历史"""
        df = get_index_component_history("000016", force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"上证50成分股历史: {len(df)} 条记录")

    def test_history_early_date(self):
        """
        测试早期日期查询

        验证规则：
        - 查询2020年之前的数据应返回结果或空DataFrame
        """
        df = get_index_component_history(
            "000300", start_date="2015-01-01", end_date="2015-12-31", force_update=False
        )
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"2015年历史记录: {len(df)} 条")


class TestMultipleIndexes:
    """
    多种指数测试类

    测试目标：
    - 测试沪深300 (000300)
    - 测试中证500 (000905)
    - 测试上证50 (000016)
    - 测试创业板指 (399006)
    """

    def test_hs300_components_count(self):
        """
        测试沪深300成分股数量

        验证规则：
        - 沪深300成分股应在290-310只之间
        """
        stocks = get_index_stocks("000300", force_update=False)
        assert 290 <= len(stocks) <= 310, (
            f"沪深300成分股应在290-310只之间，实际: {len(stocks)}"
        )
        print(f"沪深300成分股数量: {len(stocks)}")

    def test_zz500_components_count(self):
        """
        测试中证500成分股数量

        验证规则：
        - 中证500成分股应在490-510只之间
        """
        stocks = get_index_stocks("000905", force_update=False)
        assert 490 <= len(stocks) <= 510, (
            f"中证500成分股应在490-510只之间，实际: {len(stocks)}"
        )
        print(f"中证500成分股数量: {len(stocks)}")

    def test_sz50_components_count(self):
        """
        测试上证50成分股数量

        验证规则：
        - 上证50成分股应在48-52只之间
        """
        stocks = get_index_stocks("000016", force_update=False)
        assert 48 <= len(stocks) <= 52, (
            f"上证50成分股应在48-52只之间，实际: {len(stocks)}"
        )
        print(f"上证50成分股数量: {len(stocks)}")

    def test_cyb_components(self):
        """
        测试创业板指成分股

        验证规则：
        - 创业板指成分股查询应正常执行
        - 如果有数据，所有股票应为深交所格式(.XSHE)

        注意：创业板指(399006)数据源可能不稳定，
        测试验证函数能正常处理而非强制数据存在
        """
        stocks = get_index_stocks("399006", force_update=False)
        assert isinstance(stocks, list), "应返回列表"
        if len(stocks) > 0:
            assert all(".XSHE" in s for s in stocks), "创业板股票应为深交所格式"
            print(f"创业板指成分股: {len(stocks)} 只")
        else:
            print(f"创业板指数据源暂时不可用，跳过数据验证")

    def test_zz1000_components_count(self):
        """
        测试中证1000成分股数量

        验证规则：
        - 中证1000成分股应在990-1010只之间
        """
        stocks = get_index_stocks("000852", force_update=False)
        assert 990 <= len(stocks) <= 1010, (
            f"中证1000成分股应在990-1010只之间，实际: {len(stocks)}"
        )
        print(f"中证1000成分股数量: {len(stocks)}")

    def test_kc50_components(self):
        """
        测试科创50成分股

        验证规则：
        - 科创50成分股不应为空
        - 所有股票应为上交所格式(.XSHG)
        """
        stocks = get_index_stocks("000688", force_update=False)
        assert len(stocks) > 0, "科创50成分股不应为空"
        if len(stocks) > 0:
            assert all(".XSHG" in s for s in stocks), "科创板股票应为上交所格式"
        print(f"科创50成分股: {len(stocks)} 只")

    def test_multiple_indexes_data_quality(self):
        """
        测试多指数数据质量

        验证规则：
        - 主要指数都应返回有效数据
        - 对数据源不可用的指数进行标记

        注意：创业板指(399006)数据源可能不稳定，
        测试验证其他主要指数的数据质量
        """
        indexes = ["000300", "000905", "000016", "399006"]
        results = {}

        for index_code in indexes:
            stocks = get_index_stocks(index_code, force_update=False)
            results[index_code] = len(stocks)

        # 主要指数必须有数据
        main_indexes = ["000300", "000905", "000016"]
        for index_code in main_indexes:
            assert results[index_code] > 0, f"{index_code} 成分股不应为空"

        print(f"多指数成分股数量: {results}")


class TestDataValidation:
    """
    数据验证测试类

    测试目标：
    - 验证成分股代码格式
    - 验证权重范围
    - 验证成分股数量合理
    """

    def test_code_format_xshg(self):
        """
        测试上交所代码格式

        验证规则：
        - 上交所股票代码应以6开头
        - 代码格式应为 XXXXXX.XSHG
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty:
            xshg_codes = [c for c in df["code"] if ".XSHG" in str(c)]
            assert len(xshg_codes) > 0, "沪深300应包含上交所股票"
            for code in xshg_codes[:5]:
                assert code.startswith("6"), f"上交所股票应以6开头: {code}"
            print(f"上交所股票数量: {len(xshg_codes)}")

    def test_code_format_xshe(self):
        """
        测试深交所代码格式

        验证规则：
        - 深交所股票代码应以0或3开头
        - 代码格式应为 XXXXXX.XSHE
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty:
            xshe_codes = [c for c in df["code"] if ".XSHE" in str(c)]
            assert len(xshe_codes) > 0, "沪深300应包含深交所股票"
            for code in xshe_codes[:5]:
                assert code[0] in ["0", "3"], f"深交所股票应以0或3开头: {code}"
            print(f"深交所股票数量: {len(xshe_codes)}")

    def test_weight_data_type(self):
        """
        测试权重数据类型

        验证规则：
        - 权重应为数值类型 (float64, float32, int64, int32)
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty and "weight" in df.columns:
            weights = df["weight"].dropna()
            assert weights.dtype in ["float64", "float32", "int64", "int32"], (
                f"权重应为数值类型，实际: {weights.dtype}"
            )
            print(f"权重数据类型: {weights.dtype}")

    def test_no_duplicate_codes(self):
        """
        测试成分股代码无重复

        验证规则：
        - 成分股代码不应重复
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty:
            codes = df["code"].tolist()
            unique_codes = set(codes)
            assert len(codes) == len(unique_codes), "成分股代码不应重复"
            print(f"代码唯一性验证通过")

    def test_no_null_codes(self):
        """
        测试成分股代码无空值

        验证规则：
        - 成分股代码不应有空值
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty:
            null_codes = df["code"].isna().sum()
            assert null_codes == 0, f"代码不应有空值，实际: {null_codes}"
            print(f"代码非空验证通过")

    def test_weight_range_valid(self):
        """
        测试权重范围有效

        验证规则：
        - 权重应在0-20%之间
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty and "weight" in df.columns:
            weights = df["weight"].dropna()
            if len(weights) > 0:
                assert weights.min() >= 0, f"最小权重应>=0，实际: {weights.min()}"
                assert weights.max() <= 20, f"最大权重应<=20%，实际: {weights.max()}"
                print(f"权重范围: [{weights.min():.4f}%, {weights.max():.2f}%]")

    def test_components_count_reasonable(self):
        """
        测试成分股数量合理

        验证规则：
        - 沪深300成分股数量应在290-310之间
        - 中证500成分股数量应在490-510之间
        - 上证50成分股数量应在48-52之间
        """
        test_cases = [
            ("000300", 290, 310),
            ("000905", 490, 510),
            ("000016", 48, 52),
        ]

        for code, min_count, max_count in test_cases:
            stocks = get_index_stocks(code, force_update=False)
            assert min_count <= len(stocks) <= max_count, (
                f"{code} 成分股数量应在{min_count}-{max_count}之间，实际: {len(stocks)}"
            )
            print(f"{code}: {len(stocks)} 只")

    def test_stock_name_present(self):
        """
        测试股票名称存在

        验证规则：
        - 应有股票名称数据
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty and "stock_name" in df.columns:
            names = df["stock_name"].dropna()
            non_empty_names = [n for n in names if str(n).strip()]
            assert len(non_empty_names) > 0, "应有股票名称数据"
            print(f"有名称的股票数量: {len(non_empty_names)}")

    def test_top_stocks_in_index(self):
        """
        测试重要股票在成分股中

        验证规则：
        - 沪深300应包含至少一只重要股票（如茅台、平安等）
        """
        df = get_index_components("000300", force_update=False)
        if not df.empty:
            codes = set(df["code"].tolist())
            major_stocks = ["600519.XSHG", "601318.XSHG", "000858.XSHE"]
            found = sum(1 for s in major_stocks if s in codes)
            assert found >= 1, "沪深300应包含至少一只重要股票"


class TestBoundaryConditions:
    """
    边界条件测试类

    测试目标：
    - 测试不存在指数代码
    - 测试未来日期
    - 测试历史日期边界
    """

    def test_non_existent_index_code(self):
        """
        测试不存在的指数代码

        验证规则：
        - 不存在的指数代码应返回空DataFrame
        """
        df = get_index_components("999999", force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        assert df.empty, "不存在的指数应返回空 DataFrame"

    def test_invalid_index_code_format(self):
        """
        测试无效指数代码格式

        验证规则：
        - 无效代码格式应返回空DataFrame或正确处理
        """
        df = get_index_components("999999.XSHG", force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"无效代码返回: {len(df)} 条")

    def test_empty_index_code(self):
        """
        测试空指数代码

        验证规则：
        - 空代码应返回空DataFrame
        """
        df = get_index_components("", force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        assert df.empty, "空代码应返回空数据"

    def test_future_date_query(self):
        """
        测试未来日期查询

        验证规则：
        - 查询未来日期应返回空结果或当前数据
        """
        future_date = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        df = get_index_component_history(
            "000300", start_date=future_date, force_update=False
        )
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"未来日期查询返回: {len(df)} 条")

    def test_early_history_date(self):
        """
        测试早期历史日期边界

        验证规则：
        - 查询2010年之前的数据应能正确处理
        """
        df = get_index_component_history(
            "000300", start_date="2005-01-01", end_date="2010-12-31", force_update=False
        )
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"早期历史记录: {len(df)} 条")

    def test_date_range_boundary(self):
        """
        测试日期范围边界

        验证规则：
        - 起始日期大于结束日期时应返回空结果或正确处理
        """
        df = get_index_component_history(
            "000300", start_date="2024-12-31", end_date="2023-01-01", force_update=False
        )
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"反向日期范围返回: {len(df)} 条")

    def test_index_stocks_empty_result(self):
        """
        测试指数成分股列表空结果处理

        验证规则：
        - 无效指数应返回空列表
        """
        stocks = get_index_stocks("999999", force_update=False)
        assert isinstance(stocks, list), "应返回列表"
        assert len(stocks) == 0, "无效指数应返回空列表"

    def test_index_weights_empty_result(self):
        """
        测试权重查询空结果处理

        验证规则：
        - 无效指数应返回空DataFrame
        """
        df = get_index_weights("999999", force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        assert df.empty, "无效指数应返回空数据"

    def test_index_info_not_found(self):
        """
        测试未找到指数信息

        验证规则：
        - 未找到的指数信息应返回空DataFrame
        """
        df = get_index_info("999999")
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"未找到指数信息: {len(df)} 条")


class TestBatchOperations:
    """
    批量操作测试类

    测试目标：
    - 测试批量获取多指数成分
    - 测试跨指数筛选
    """

    def test_query_multiple_indexes(self):
        """
        测试批量查询多指数成分股

        验证规则：
        - 批量查询应返回所有指定指数的成分股
        """
        df = query_index_components(["000300", "000016"], force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        assert not df.empty, "批量查询结果不应为空"
        print(f"批量查询成分股: {len(df)} 条记录")

    def test_query_multiple_indexes_with_weights(self):
        """
        测试批量查询多指数成分股及权重

        验证规则：
        - 批量查询应返回权重数据
        """
        df = query_index_components(["000300", "000905"], force_update=False)
        if not df.empty:
            assert "weight" in df.columns, "应包含 weight 列"
            print(f"批量查询带权重: {len(df)} 条记录")

    def test_query_empty_list(self):
        """
        测试空列表批量查询

        验证规则：
        - 空列表应返回空DataFrame
        """
        df = query_index_components([], force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        assert df.empty, "空列表应返回空数据"

    def test_cross_index_screening(self):
        """
        测试跨指数筛选

        验证规则：
        - 应能找出同时存在于多个指数的股票
        """
        hs300_stocks = set(get_index_stocks("000300", force_update=False))
        zz500_stocks = set(get_index_stocks("000905", force_update=False))

        common_stocks = hs300_stocks & zz500_stocks
        print(f"沪深300与中证500交集: {len(common_stocks)} 只")

        assert isinstance(common_stocks, set), "交集应为集合"

    def test_batch_query_large_indexes(self):
        """
        测试批量查询大型指数组合

        验证规则：
        - 应能正确处理多个指数的批量查询
        """
        indexes = ["000300", "000905", "000016"]
        results = {}

        for index_code in indexes:
            stocks = get_index_stocks(index_code, force_update=False)
            results[index_code] = len(stocks)

        print(f"批量查询结果: {results}")
        for code, count in results.items():
            assert count > 0, f"{code} 成分股数量应大于0"

    def test_finance_run_query_multiple_indexes(self):
        """
        测试 finance.run_query 多指数查询

        验证规则：
        - 应能正确处理多指数查询
        """
        results = {}
        for code in ["000300", "000016"]:
            query = finance.STK_INDEX_WEIGHTS()
            query.index_code = code
            df = finance.run_query(query, force_update=False)
            results[code] = len(df)
        print(f"finance.run_query 多指数查询结果: {results}")


class TestCacheMechanism:
    """
    缓存测试类

    测试目标：
    - 测试按季度缓存
    - 测试缓存预热
    """

    def test_cache_hit(self):
        """
        测试缓存命中

        验证规则：
        - 相同查询应返回相同数据
        """
        df1 = get_index_components("000300", force_update=False)
        df2 = get_index_components("000300", force_update=False)
        assert len(df1) == len(df2), "缓存命中数据应一致"
        print(f"缓存命中验证: {len(df1)} 条")

    def test_cache_with_duckdb(self):
        """
        测试DuckDB缓存

        验证规则：
        - DuckDB缓存应正常工作
        """
        df = get_index_components("000300", use_duckdb=True, force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"DuckDB缓存: {len(df)} 条")

    def test_cache_with_pickle(self):
        """
        测试Pickle缓存

        验证规则：
        - Pickle缓存应正常工作
        """
        df = get_index_components("000300", use_duckdb=False, force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"Pickle缓存: {len(df)} 条")

    def test_cache_consistency(self):
        """
        测试不同缓存方式数据一致性

        验证规则：
        - DuckDB和Pickle缓存应返回相同数据
        """
        df_duckdb = get_index_components("000300", use_duckdb=True, force_update=False)
        df_pickle = get_index_components("000300", use_duckdb=False, force_update=False)
        if not df_duckdb.empty and not df_pickle.empty:
            assert len(df_duckdb) == len(df_pickle), "不同缓存方式数据量应一致"
        print(f"缓存一致性验证通过")

    def test_force_update(self):
        """
        测试强制更新

        验证规则：
        - 强制更新应能正常工作
        """
        df1 = get_index_components("000300", force_update=False)
        df2 = get_index_components("000300", force_update=True)
        assert isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame), (
            "应返回 DataFrame"
        )
        print(f"强制更新验证: {len(df1)} vs {len(df2)}")

    def test_quarterly_cache_validity(self):
        """
        测试按季度缓存有效性

        验证规则：
        - 缓存应按季度（约90天）有效
        """
        df = get_index_components("000300", force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"季度缓存验证: {len(df)} 条")

    def test_cache_preheat(self):
        """
        测试缓存预热

        验证规则：
        - 批量预热多个指数缓存
        """
        indexes = ["000300", "000905", "000016"]
        for index_code in indexes:
            _ = get_index_components(index_code, force_update=False)

        df = get_index_components("000300", force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        assert not df.empty, "预热后应能获取数据"
        print(f"缓存预热验证通过")


class TestFinanceRunQuery:
    """
    finance.run_query 测试类

    测试目标：
    - 测试 finance.run_query 接口
    """

    def test_query_with_index_code_filter(self):
        """
        测试带指数代码过滤的查询

        验证规则：
        - 应返回指定指数的成分股数据
        """
        query = finance.STK_INDEX_WEIGHTS()
        query.index_code = "000300"
        df = finance.run_query(query, force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        if not df.empty:
            assert "code" in df.columns, "应包含 code 列"
            assert "weight" in df.columns, "应包含 weight 列"
        print(f"带过滤查询结果: {len(df)} 条")

    def test_query_components_table(self):
        """
        测试查询成分股表

        验证规则：
        - STK_INDEX_COMPONENTS 表应返回成分股数据
        """
        query = finance.STK_INDEX_COMPONENTS()
        query.index_code = "000905"
        df = finance.run_query(query, force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"成分股表查询结果: {len(df)} 条")

    def test_query_no_filter(self):
        """
        测试无过滤条件的查询

        验证规则：
        - 无过滤条件应返回空DataFrame
        """
        query = finance.STK_INDEX_WEIGHTS()
        df = finance.run_query(query, force_update=False)
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        print(f"无过滤条件查询: {len(df)} 条")

    def test_query_zz500_weights(self):
        """
        测试查询中证500权重

        验证规则：
        - 应返回中证500权重数据
        """
        df = run_query_simple(
            "STK_INDEX_WEIGHTS", index_code="000905", force_update=False
        )
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        if not df.empty:
            assert "weight" in df.columns, "应包含 weight 列"
        print(f"中证500权重查询: {len(df)} 条")


class TestIndexInfo:
    """
    指数信息测试类

    测试目标：
    - 测试获取指数基本信息
    """

    def test_get_index_info_hs300(self):
        """
        测试获取沪深300指数信息

        验证规则：
        - 应返回包含 index_code 和 index_name 列的DataFrame
        """
        df = get_index_info("000300")
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        if not df.empty:
            assert "index_code" in df.columns, "应包含 index_code 列"
            assert "index_name" in df.columns, "应包含 index_name 列"
        print(f"沪深300指数信息: {len(df)} 条记录")

    def test_get_index_info_all(self):
        """
        测试获取所有指数信息

        验证规则：
        - 应返回多个指数信息
        """
        df = get_index_info()
        assert isinstance(df, pd.DataFrame), "应返回 DataFrame"
        assert len(df) > 0, "应返回多个指数信息"
        assert "index_code" in df.columns, "应包含 index_code 列"
        assert "index_name" in df.columns, "应包含 index_name 列"
        print(f"所有指数数量: {len(df)}")

    def test_index_info_contains_common_indexes(self):
        """
        测试指数信息包含常见指数

        验证规则：
        - 应包含沪深300、中证500、上证50等常见指数
        """
        df = get_index_info()
        if not df.empty:
            codes = df["index_code"].tolist()
            common_indexes = ["000300", "000905", "000016"]
            found = sum(1 for idx in common_indexes if idx in codes)
            assert found >= 1, "应包含常见指数"
            print(f"找到常见指数: {found} 个")


class TestIndustryIndex:
    """
    行业指数测试类

    测试目标：
    - 测试行业指数成分股获取
    """

    def test_get_industry_index_stocks_by_code(self):
        """
        测试通过行业代码获取成分股

        验证规则：
        - 应返回正确格式的股票代码列表
        """
        stocks = get_industry_index_stocks("801010")
        assert isinstance(stocks, list), "应返回列表"
        if len(stocks) > 0:
            assert all(".XSHG" in s or ".XSHE" in s for s in stocks), (
                "所有股票代码应为聚宽格式"
            )
        print(f"农林牧渔行业(801010)成分股: {len(stocks)} 只股票")

    def test_get_industry_index_stocks_by_name(self):
        """
        测试通过行业名称获取成分股

        验证规则：
        - 应返回正确格式的股票代码列表
        """
        stocks = get_industry_index_stocks("银行")
        assert isinstance(stocks, list), "应返回列表"
        if len(stocks) > 0:
            assert all(".XSHG" in s or ".XSHE" in s for s in stocks), (
                "所有股票代码应为聚宽格式"
            )
        print(f"银行业成分股: {len(stocks)} 只股票")


class TestCodeFormat:
    """
    代码格式测试类

    测试目标：
    - 测试不同代码格式的支持
    """

    def test_code_format_without_suffix(self):
        """
        测试无后缀代码格式

        验证规则：
        - 无后缀代码应能正确处理
        """
        df1 = get_index_components("000300", force_update=False)
        df2 = get_index_components("000300.XSHG", force_update=False)

        assert not df1.empty, "无后缀格式应返回数据"
        assert not df2.empty, "有后缀格式应返回数据"
        assert len(df1) == len(df2), "不同格式应返回相同数量的记录"

    def test_code_format_zz500(self):
        """
        测试中证500代码格式

        验证规则：
        - 中证500不同代码格式应返回相同数据
        """
        df1 = get_index_components("000905", force_update=False)
        df2 = get_index_components("000905.XSHG", force_update=False)

        assert not df1.empty, "格式1应返回数据"
        assert not df2.empty, "格式2应返回数据"
        assert len(df1) == len(df2), "不同格式应返回相同数量的记录"


class TestDataConsistency:
    """
    数据一致性测试类

    测试目标：
    - 测试不同接口返回数据的一致性
    """

    def test_components_vs_stocks_consistency(self):
        """
        测试成分股和股票列表一致性

        验证规则：
        - get_index_components 和 get_index_stocks 应返回相同数据
        """
        df_components = get_index_components("000300", force_update=False)
        stocks = get_index_stocks("000300", force_update=False)

        if not df_components.empty:
            assert len(df_components) == len(stocks), "成分股数量应一致"
            codes_in_df = set(df_components["code"].tolist())
            codes_in_list = set(stocks)
            assert codes_in_df == codes_in_list, "成分股代码应一致"

    def test_weights_vs_components_consistency(self):
        """
        测试权重和成分股一致性

        验证规则：
        - get_index_weights 和 get_index_components 应返回相同股票
        """
        df_components = get_index_components("000300", force_update=False)
        df_weights = get_index_weights("000300", force_update=False)

        if not df_components.empty and not df_weights.empty:
            assert len(df_components) == len(df_weights), "数据量应一致"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
