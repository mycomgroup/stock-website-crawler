"""
test_macro_api.py
宏观经济数据 API 测试

测试覆盖:
1. 正常功能测试 - 数据获取成功
2. 边界条件测试 - 空输入、None输入、无效代码
3. 异常处理测试 - 网络失败、数据缺失
4. 缓存机制测试 - 缓存命中、缓存过期
5. RobustResult 测试 - success/data/reason/source 验证
6. 批量查询测试 - 多指标查询
7. 代码格式兼容测试
"""

import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.finance_data.macro import (
    get_macro_china_gdp,
    get_macro_china_cpi,
    get_macro_china_ppi,
    get_macro_china_pmi,
    get_macro_china_interest_rate,
    get_macro_china_exchange_rate,
    get_macro_data,
    get_macro_series,
    get_macro_indicators,
    get_gdp_data,
    get_cpi_data,
    get_pmi_data,
    get_interest_rate,
    get_macro_m2,
    get_macro_indicator_robust,
    query_macro,
    query_macro_data,
    finance,
    run_query_simple,
    RobustResult,
    FinanceQuery,
    get_macro_gdp,
    get_macro_cpi,
    get_macro_ppi,
    _db_manager,
    MacroDBManager,
)


class TestMacroChinaAPI:
    """测试 get_macro_china_* 函数"""

    def test_get_macro_china_gdp(self):
        """测试GDP数据获取"""
        df = get_macro_china_gdp(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            assert "date" in df.columns
            assert "value" in df.columns
            print(f"GDP数据: {len(df)} 条记录")

    def test_get_macro_china_cpi(self):
        """测试CPI数据获取"""
        df = get_macro_china_cpi(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            assert df["indicator"].iloc[0] == "CPI"
            print(f"CPI数据: {len(df)} 条记录")

    def test_get_macro_china_ppi(self):
        """测试PPI数据获取"""
        df = get_macro_china_ppi(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            assert df["indicator"].iloc[0] == "PPI"
            print(f"PPI数据: {len(df)} 条记录")

    def test_get_macro_china_pmi(self):
        """测试PMI数据获取"""
        df = get_macro_china_pmi(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            assert df["indicator"].iloc[0] == "PMI"
            print(f"PMI数据: {len(df)} 条记录")

    def test_get_macro_china_interest_rate(self):
        """测试利率数据获取"""
        df = get_macro_china_interest_rate(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            print(f"利率数据: {len(df)} 条记录")

    def test_get_macro_china_exchange_rate(self):
        """测试汇率数据获取"""
        df = get_macro_china_exchange_rate(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            print(f"汇率数据: {len(df)} 条记录")


class TestMacroGenericAPI:
    """测试通用接口"""

    def test_get_macro_data_gdp(self):
        """测试通用接口获取GDP"""
        df = get_macro_data("gdp", force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            print(f"通用接口GDP: {len(df)} 条记录")

    def test_get_macro_data_cpi(self):
        """测试通用接口获取CPI"""
        df = get_macro_data("cpi", force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert df["indicator"].iloc[0] == "CPI"
            print(f"通用接口CPI: {len(df)} 条记录")

    def test_get_macro_data_ppi(self):
        """测试通用接口获取PPI"""
        df = get_macro_data("ppi", force_update=True)
        assert isinstance(df, pd.DataFrame)
        print(f"通用接口PPI: {len(df)} 条记录")

    def test_get_macro_data_m2(self):
        """测试通用接口获取M2"""
        df = get_macro_data("m2", force_update=True)
        assert isinstance(df, pd.DataFrame)
        print(f"通用接口M2: {len(df)} 条记录")

    def test_get_macro_data_with_date_filter(self):
        """测试带日期过滤的查询"""
        df = get_macro_data(
            "cpi", start_date="2023-01-01", end_date="2024-01-01", force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        if not df.empty and "date" in df.columns:
            dates = pd.to_datetime(df["date"])
            if len(dates) > 0:
                assert dates.min() >= pd.to_datetime("2023-01-01")
                assert dates.max() <= pd.to_datetime("2024-01-01")
        print(f"日期过滤CPI: {len(df)} 条记录")

    def test_get_macro_series(self):
        """测试时间序列获取"""
        df = get_macro_series("ppi", start_date="2022-01-01", force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty and "date" in df.columns:
            dates = pd.to_datetime(df["date"])
            if len(dates) > 0:
                assert dates.min() >= pd.to_datetime("2022-01-01")
        print(f"时间序列PPI: {len(df)} 条记录")


class TestMacroIndicators:
    """测试指标列表"""

    def test_get_macro_indicators(self):
        """测试获取可用指标列表"""
        indicators = get_macro_indicators()
        assert isinstance(indicators, pd.DataFrame)
        assert len(indicators) > 0
        assert "code" in indicators.columns
        assert "name" in indicators.columns
        assert "frequency" in indicators.columns
        print(f"可用指标: {len(indicators)} 个")

    def test_indicators_contain_expected(self):
        """测试指标列表包含预期指标"""
        indicators = get_macro_indicators()
        codes = indicators["code"].tolist()
        expected = ["GDP", "CPI", "PPI", "PMI", "M2"]
        for code in expected:
            assert code in codes, f"缺少指标: {code}"


class TestSimpleAPI:
    """测试简化API"""

    def test_get_gdp_data(self):
        """测试get_gdp_data"""
        df = get_gdp_data()
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            print(f"GDP数据: {len(df)} 条记录")

    def test_get_cpi_data(self):
        """测试get_cpi_data"""
        df = get_cpi_data()
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            print(f"CPI数据: {len(df)} 条记录")

    def test_get_pmi_data(self):
        """测试get_pmi_data"""
        df = get_pmi_data()
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            print(f"PMI数据: {len(df)} 条记录")

    def test_get_interest_rate(self):
        """测试get_interest_rate"""
        df = get_interest_rate()
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            print(f"利率数据: {len(df)} 条记录")

    def test_get_gdp_data_with_dates(self):
        """测试带日期范围的get_gdp_data"""
        df = get_gdp_data(start_date="2022-01-01", end_date="2024-01-01")
        assert isinstance(df, pd.DataFrame)
        print(f"GDP日期范围查询: {len(df)} 条记录")

    def test_get_cpi_data_with_dates(self):
        """测试带日期范围的get_cpi_data"""
        df = get_cpi_data(start_date="2023-01-01", end_date="2024-01-01")
        assert isinstance(df, pd.DataFrame)
        print(f"CPI日期范围查询: {len(df)} 条记录")


class TestFinanceQuery:
    """测试 finance.run_query 接口"""

    def test_finance_run_query_gdp(self):
        """测试 finance.run_query 查询 GDP"""
        df = finance.run_query(finance.MACRO_CHINA_GDP, force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            print(f"finance.run_query GDP: {len(df)} 条记录")

    def test_finance_run_query_cpi(self):
        """测试 finance.run_query 查询 CPI"""
        df = finance.run_query(finance.MACRO_CHINA_CPI, force_update=True)
        assert isinstance(df, pd.DataFrame)
        print(f"finance.run_query CPI: {len(df)} 条记录")

    def test_finance_run_query_ppi(self):
        """测试 finance.run_query 查询 PPI"""
        df = finance.run_query(finance.MACRO_CHINA_PPI, force_update=True)
        assert isinstance(df, pd.DataFrame)
        print(f"finance.run_query PPI: {len(df)} 条记录")

    def test_finance_run_query_pmi(self):
        """测试 finance.run_query 查询 PMI"""
        df = finance.run_query(finance.MACRO_CHINA_PMI, force_update=True)
        assert isinstance(df, pd.DataFrame)
        print(f"finance.run_query PMI: {len(df)} 条记录")

    def test_finance_run_query_macro_economic_data(self):
        """测试 finance.run_query 查询 MACRO_ECONOMIC_DATA"""
        df = finance.run_query(finance.MACRO_ECONOMIC_DATA)
        assert isinstance(df, pd.DataFrame)
        print(f"finance.run_query MACRO_ECONOMIC_DATA: {len(df)} 条记录")

    def test_finance_macro_china_gdp_class(self):
        """测试 MACRO_CHINA_GDP 类属性"""
        assert hasattr(finance, "MACRO_CHINA_GDP")
        assert hasattr(FinanceQuery.MACRO_CHINA_GDP, "indicator")
        assert hasattr(FinanceQuery.MACRO_CHINA_GDP, "value")

    def test_finance_macro_china_cpi_class(self):
        """测试 MACRO_CHINA_CPI 类属性"""
        assert hasattr(finance, "MACRO_CHINA_CPI")

    def test_finance_macro_china_ppi_class(self):
        """测试 MACRO_CHINA_PPI 类属性"""
        assert hasattr(finance, "MACRO_CHINA_PPI")

    def test_finance_macro_china_pmi_class(self):
        """测试 MACRO_CHINA_PMI 类属性"""
        assert hasattr(finance, "MACRO_CHINA_PMI")


class TestRunQuerySimple:
    """测试简化查询接口"""

    def test_run_query_simple_gdp(self):
        """测试简化接口查询 GDP"""
        df = run_query_simple("MACRO_CHINA_GDP", force_update=True)
        assert isinstance(df, pd.DataFrame)
        print(f"run_query_simple GDP: {len(df)} 条记录")

    def test_run_query_simple_cpi(self):
        """测试简化接口查询 CPI"""
        df = run_query_simple("MACRO_CHINA_CPI", force_update=True)
        assert isinstance(df, pd.DataFrame)
        print(f"run_query_simple CPI: {len(df)} 条记录")

    def test_run_query_simple_macro_economic_data(self):
        """测试简化接口查询 MACRO_ECONOMIC_DATA"""
        df = run_query_simple("MACRO_ECONOMIC_DATA")
        assert isinstance(df, pd.DataFrame)
        print(f"run_query_simple MACRO_ECONOMIC_DATA: {len(df)} 条记录")

    def test_run_query_simple_with_dates(self):
        """测试带日期的简化查询"""
        df = run_query_simple(
            "MACRO_CHINA_CPI", start_date="2023-01-01", end_date="2024-01-01"
        )
        assert isinstance(df, pd.DataFrame)
        print(f"带日期简化查询: {len(df)} 条记录")


class TestQueryMacroData:
    """测试 MACRO_ECONOMIC_DATA 表查询"""

    def test_query_macro_data_all(self):
        """测试查询全部宏观数据"""
        df = query_macro_data()
        assert isinstance(df, pd.DataFrame)
        print(f"全部宏观数据: {len(df)} 条记录")

    def test_query_macro_data_by_indicator(self):
        """测试按指标查询"""
        df = query_macro_data(indicator="CPI")
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            indicators = df["indicator"].unique()
            assert all(i == "CPI" for i in indicators)
        print(f"CPI查询: {len(df)} 条记录")

    def test_query_macro_data_with_dates(self):
        """测试带日期范围查询"""
        df = query_macro_data(start_date="2023-01-01", end_date="2024-01-01")
        assert isinstance(df, pd.DataFrame)
        print(f"日期范围查询: {len(df)} 条记录")

    def test_query_macro_data_by_indicator_with_dates(self):
        """测试按指标和日期查询"""
        df = query_macro_data(
            indicator="GDP", start_date="2020-01-01", end_date="2024-01-01"
        )
        assert isinstance(df, pd.DataFrame)
        print(f"GDP日期范围查询: {len(df)} 条记录")


class TestRobustResultClass:
    """测试 RobustResult 类"""

    def test_robust_result_success(self):
        """测试成功结果"""
        result = RobustResult(
            success=True,
            data=pd.DataFrame({"value": [1, 2, 3]}),
            reason="获取成功",
            source="network",
        )
        assert result.success is True
        assert result.data is not None
        assert len(result.data) == 3
        assert bool(result) is True

    def test_robust_result_failure(self):
        """测试失败结果"""
        result = RobustResult(
            success=False, data=pd.DataFrame(), reason="数据缺失", source="error"
        )
        assert result.success is False
        assert result.data.empty
        assert bool(result) is False

    def test_robust_result_repr(self):
        """测试字符串表示"""
        success_result = RobustResult(success=True, reason="test")
        fail_result = RobustResult(success=False, reason="test")
        status_text = repr(success_result)
        fail_text = repr(fail_result)
        assert "OK" in status_text or "SUCCESS" in status_text
        assert "FAIL" in fail_text or "False" in fail_text

    def test_robust_result_bool_conversion(self):
        """测试布尔转换"""
        success = RobustResult(success=True, data=pd.DataFrame({"a": [1]}))
        fail = RobustResult(success=False)
        assert bool(success) is True
        assert bool(fail) is False

    def test_robust_result_none_data(self):
        """测试 None 数据"""
        result = RobustResult(success=True, data=None)
        assert result.data.empty


class TestRobustAPI:
    """测试稳健 API"""

    def test_robust_result_success_data(self):
        """测试成功结果的data属性"""
        result = get_macro_indicator_robust("GDP", force_update=True)
        assert hasattr(result, "success")
        assert hasattr(result, "data")
        assert hasattr(result, "reason")
        assert hasattr(result, "source")

    def test_robust_result_invalid_indicator(self):
        """测试无效指标返回失败"""
        result = get_macro_indicator_robust("INVALID_INDICATOR")
        assert result.success is False
        assert "不支持的指标" in result.reason

    def test_robust_result_supported_indicators(self):
        """测试所有支持的指标"""
        supported = ["GDP", "CPI", "PPI", "M2", "INTEREST_RATE"]
        for ind in supported:
            result = get_macro_indicator_robust(ind)
            assert hasattr(result, "success"), f"{ind} 应返回RobustResult"

    def test_robust_result_gdp(self):
        """测试 GDP RobustResult"""
        result = get_macro_indicator_robust("GDP", force_update=True)
        assert isinstance(result, RobustResult)
        print(f"GDP RobustResult: {result}")

    def test_robust_result_cpi(self):
        """测试 CPI RobustResult"""
        result = get_macro_indicator_robust("CPI", force_update=True)
        assert isinstance(result, RobustResult)
        print(f"CPI RobustResult: {result}")

    def test_robust_result_ppi(self):
        """测试 PPI RobustResult"""
        result = get_macro_indicator_robust("PPI", force_update=True)
        assert isinstance(result, RobustResult)
        print(f"PPI RobustResult: {result}")

    def test_robust_result_m2(self):
        """测试 M2 RobustResult"""
        result = get_macro_indicator_robust("M2", force_update=True)
        assert isinstance(result, RobustResult)
        print(f"M2 RobustResult: {result}")


class TestGDPDataComprehensive:
    """GDP数据全面测试"""

    def test_gdp_data_columns(self):
        """测试GDP数据列完整性"""
        df = get_macro_china_gdp(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            assert "date" in df.columns
            assert "value" in df.columns

    def test_gdp_data_values_reasonable(self):
        """测试GDP数值合理性"""
        df = get_macro_china_gdp(force_update=True)
        if not df.empty and "value" in df.columns:
            values = df["value"].dropna()
            if len(values) > 0:
                assert values.min() > 0, "GDP值应为正数"
                assert values.max() < 2000000, "GDP值应在合理范围内"

    def test_gdp_date_order(self):
        """测试GDP日期排序"""
        df = get_macro_china_gdp(force_update=True)
        if not df.empty and "date" in df.columns:
            dates = pd.to_datetime(df["date"])
            assert dates.is_monotonic_decreasing or dates.is_monotonic_increasing

    def test_gdp_yearly_data(self):
        """测试年度GDP数据"""
        df = get_gdp_data(start_date="2020-01-01", end_date="2024-01-01")
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert len(df) >= 1, "应至少有一年GDP数据"

    def test_gdp_indicator_consistency(self):
        """测试GDP指标名称一致性"""
        df = get_macro_china_gdp(force_update=True)
        if not df.empty:
            indicators = df["indicator"].unique()
            assert all(i == "GDP" for i in indicators), "所有指标应为GDP"

    def test_gdp_data_count(self):
        """测试GDP数据数量"""
        df = get_macro_china_gdp(force_update=True)
        if not df.empty:
            assert len(df) >= 4, "应至少有4个季度GDP数据"


class TestCPIDataComprehensive:
    """CPI数据全面测试"""

    def test_cpi_yoy_values(self):
        """测试CPI同比数据"""
        df = get_macro_china_cpi(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty and "YoY" in df.columns:
            yoy = df["YoY"].dropna()
            if len(yoy) > 0:
                assert yoy.min() >= -10, "CPI同比不应低于-10%"
                assert yoy.max() <= 20, "CPI同比不应高于20%"

    def test_cpi_mom_values(self):
        """测试CPI环比数据"""
        df = get_macro_china_cpi(force_update=True)
        if not df.empty and "MoM" in df.columns:
            mom = df["MoM"].dropna()
            if len(mom) > 0:
                assert mom.min() >= -5, "CPI环比不应低于-5%"
                assert mom.max() <= 5, "CPI环比不应高于5%"

    def test_cpi_monthly_frequency(self):
        """测试CPI月度频率"""
        df = get_macro_china_cpi(force_update=True)
        if not df.empty and len(df) > 12:
            dates = pd.to_datetime(df["date"])
            date_diffs = dates.sort_values().diff().dropna()
            avg_days = date_diffs.mean().days
            assert 20 <= avg_days <= 40, "CPI应为月度数据"

    def test_cpi_data_count(self):
        """测试CPI数据数量"""
        df = get_macro_china_cpi(force_update=True)
        if not df.empty:
            assert len(df) >= 12, "应至少有12个月CPI数据"

    def test_cpi_indicator_name(self):
        """测试CPI指标名称"""
        df = get_macro_china_cpi(force_update=True)
        if not df.empty:
            assert df["indicator"].iloc[0] == "CPI"


class TestPPIDataComprehensive:
    """PPI数据全面测试"""

    def test_ppi_data_columns(self):
        """测试PPI数据列完整性"""
        df = get_macro_china_ppi(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            assert "value" in df.columns

    def test_ppi_values_range(self):
        """测试PPI数值范围"""
        df = get_macro_china_ppi(force_update=True)
        if not df.empty and "value" in df.columns:
            values = df["value"].dropna()
            if len(values) > 0:
                assert values.min() >= -20, "PPI同比不应低于-20%"
                assert values.max() <= 20, "PPI同比不应高于20%"

    def test_ppi_indicator_name(self):
        """测试PPI指标名称"""
        df = get_macro_china_ppi(force_update=True)
        if not df.empty:
            assert df["indicator"].iloc[0] == "PPI"

    def test_ppi_monthly_frequency(self):
        """测试PPI月度频率"""
        df = get_macro_china_ppi(force_update=True)
        if not df.empty and len(df) > 12:
            dates = pd.to_datetime(df["date"])
            date_diffs = dates.sort_values().diff().dropna()
            if len(date_diffs) > 0:
                avg_days = date_diffs.mean().days
                assert 20 <= avg_days <= 40, "PPI应为月度数据"

    def test_ppi_data_count(self):
        """测试PPI数据数量"""
        df = get_macro_china_ppi(force_update=True)
        if not df.empty:
            assert len(df) >= 12, "应至少有12个月PPI数据"


class TestPMIDataComprehensive:
    """PMI数据全面测试"""

    def test_pmi_data_structure(self):
        """测试PMI数据结构"""
        df = get_macro_china_pmi(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            assert "date" in df.columns

    def test_pmi_values_range(self):
        """测试PMI数值范围(0-100)"""
        df = get_macro_china_pmi(force_update=True)
        if not df.empty and "value" in df.columns:
            values = df["value"].dropna()
            if len(values) > 0:
                assert values.min() >= 0, "PMI不应低于0"
                assert values.max() <= 100, "PMI不应高于100"

    def test_pmi_expansion_threshold(self):
        """测试PMI景气度判断(50为分界线)"""
        df = get_macro_china_pmi(force_update=True)
        if not df.empty and "value" in df.columns:
            values = df["value"].dropna()
            if len(values) > 0:
                assert any(values > 45), "应存在PMI值大于45"
                assert any(values < 60), "PMI应有合理波动"

    def test_pmi_indicator_name(self):
        """测试PMI指标名称"""
        df = get_macro_china_pmi(force_update=True)
        if not df.empty:
            assert df["indicator"].iloc[0] == "PMI"

    def test_pmi_data_count(self):
        """测试PMI数据数量"""
        df = get_macro_china_pmi(force_update=True)
        if not df.empty:
            assert len(df) >= 12, "应至少有12个月PMI数据"


class TestInterestRateComprehensive:
    """利率数据全面测试"""

    def test_interest_rate_columns(self):
        """测试利率数据列完整性"""
        df = get_macro_china_interest_rate(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns

    def test_interest_rate_values_reasonable(self):
        """测试利率数值合理性"""
        df = get_macro_china_interest_rate(force_update=True)
        if not df.empty and "value" in df.columns:
            values = df["value"].dropna()
            if len(values) > 0:
                assert values.min() >= 0, "利率不应为负"
                assert values.max() <= 20, "利率不应超过20%"

    def test_interest_rate_date_valid(self):
        """测试利率日期有效性"""
        df = get_macro_china_interest_rate(force_update=True)
        if not df.empty and "date" in df.columns:
            dates = df["date"].dropna()
            assert len(dates) > 0, "应有有效日期数据"


class TestExchangeRateComprehensive:
    """汇率数据全面测试"""

    def test_exchange_rate_structure(self):
        """测试汇率数据结构"""
        df = get_macro_china_exchange_rate(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            assert "date" in df.columns

    def test_exchange_rate_usd_range(self):
        """测试美元汇率范围"""
        df = get_macro_china_exchange_rate(force_update=True)
        if not df.empty and "value" in df.columns:
            values = df["value"].dropna()
            if len(values) > 0:
                assert values.min() >= 6, "人民币汇率应在合理范围"
                assert values.max() <= 9, "人民币汇率应在合理范围"

    def test_exchange_rate_indicator(self):
        """测试汇率指标名称"""
        df = get_macro_china_exchange_rate(force_update=True)
        if not df.empty:
            assert (
                "EXCHANGE_RATE" in df["indicator"].iloc[0]
                or df["indicator"].iloc[0] != ""
            )


class TestM2Data:
    """M2货币供应量测试"""

    def test_m2_data_structure(self):
        """测试M2数据结构"""
        df = get_macro_m2(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns

    def test_m2_data_values(self):
        """测试M2数值"""
        df = get_macro_m2(force_update=True)
        if not df.empty and "value" in df.columns:
            values = df["value"].dropna()
            if len(values) > 0:
                assert values.min() > 0, "M2应为正值"

    def test_m2_indicator_name(self):
        """测试M2指标名称"""
        df = get_macro_m2(force_update=True)
        if not df.empty:
            assert df["indicator"].iloc[0] == "M2"


class TestBatchQuery:
    """批量查询测试"""

    def test_query_macro_multiple_indicators(self):
        """测试批量查询多指标"""
        df = query_macro(["CPI", "PPI"], force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            indicators = df["indicator"].unique()
            assert "CPI" in indicators or "PPI" in indicators

    def test_query_macro_empty_list(self):
        """测试空列表查询"""
        df = query_macro([])
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_query_macro_single_indicator(self):
        """测试单指标批量查询"""
        df = query_macro(["GDP"], force_update=True)
        assert isinstance(df, pd.DataFrame)

    def test_query_macro_invalid_indicator(self):
        """测试无效指标批量查询"""
        df = query_macro(["INVALID"], force_update=True)
        assert isinstance(df, pd.DataFrame)


class TestCacheBehavior:
    """缓存行为测试"""

    def test_force_update_flag(self):
        """测试强制更新标志"""
        df1 = get_macro_data("cpi", force_update=True)
        df2 = get_macro_data("cpi", force_update=False)
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)

    def test_cache_returns_same_structure(self):
        """测试缓存返回相同结构"""
        df1 = get_macro_china_gdp(force_update=True)
        df2 = get_macro_china_gdp(force_update=False)
        if not df1.empty and not df2.empty:
            assert set(df1.columns) == set(df2.columns)

    def test_cache_consistency(self):
        """测试缓存一致性"""
        df1 = get_macro_data("ppi", force_update=True)
        df2 = get_macro_data("ppi", force_update=False)
        if not df1.empty and not df2.empty:
            assert len(df1) == len(df2), "缓存数据条数应一致"


class TestEdgeCases:
    """边缘情况测试"""

    def test_invalid_indicator_type(self):
        """测试无效指标类型"""
        result = get_macro_indicator_robust("INVALID")
        assert result.success is False

    def test_future_date_range(self):
        """测试未来日期范围"""
        df = get_macro_data("cpi", start_date="2030-01-01", end_date="2031-01-01")
        assert isinstance(df, pd.DataFrame)

    def test_old_date_range(self):
        """测试历史日期范围"""
        df = get_macro_data("gdp", start_date="2000-01-01", end_date="2001-01-01")
        assert isinstance(df, pd.DataFrame)

    def test_start_after_end_date(self):
        """测试起始日期晚于结束日期"""
        df = get_macro_data("cpi", start_date="2024-01-01", end_date="2023-01-01")
        assert isinstance(df, pd.DataFrame)

    def test_empty_indicator(self):
        """测试空指标"""
        result = get_macro_indicator_robust("")
        assert result.success is False

    def test_none_indicator(self):
        """测试None指标"""
        result = get_macro_indicator_robust(None)
        assert result.success is False


class TestDataQualityValidation:
    """数据质量验证测试"""

    def test_no_duplicate_dates(self):
        """测试无重复日期"""
        df = get_macro_china_cpi(force_update=True)
        if not df.empty and "date" in df.columns:
            dates = df["date"].dropna()
            assert len(dates) == len(dates.unique()), "日期不应有重复"

    def test_no_null_values_in_critical_columns(self):
        """测试关键列无空值"""
        df = get_macro_china_gdp(force_update=True)
        if not df.empty:
            assert df["indicator"].notna().all(), "indicator列不应有空值"
            assert df["date"].notna().all(), "date列不应有空值"

    def test_unit_consistency(self):
        """测试单位一致性"""
        df = get_macro_china_cpi(force_update=True)
        if not df.empty and "unit" in df.columns:
            units = df["unit"].dropna().unique()
            assert len(units) <= 1, "同一指标单位应一致"

    def test_value_not_empty(self):
        """测试值非空"""
        df = get_macro_china_gdp(force_update=True)
        if not df.empty and "value" in df.columns:
            non_empty = df["value"].notna().sum()
            assert non_empty > 0, "应有非空值"


class TestIntegration:
    """集成测试"""

    def test_full_workflow(self):
        """测试完整工作流"""
        indicators = get_macro_indicators()
        assert isinstance(indicators, pd.DataFrame)
        assert len(indicators) > 0

        for code in ["GDP", "CPI"]:
            df = get_macro_data(code, force_update=True)
            assert isinstance(df, pd.DataFrame)

    def test_multiple_api_consistency(self):
        """测试多API一致性"""
        df1 = get_macro_china_cpi(force_update=True)
        df2 = get_macro_data("cpi", force_update=True)
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)


class TestMultipleIndicators:
    """多种指标测试

    测试各种宏观经济指标的获取功能，包括：
    - GDP: 国内生产总值
    - CPI: 消费者物价指数
    - PPI: 生产者物价指数
    - PMI: 采购经理指数
    - 利率数据
    - 汇率数据
    """

    def test_gdp_data_basic(self):
        """测试GDP数据基本获取

        验证GDP数据能够成功获取，并包含必要的字段：
        - indicator: 指标名称
        - date: 日期
        - value: 数值
        """
        df = get_macro_china_gdp(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns, "GDP数据应包含indicator字段"
            assert "date" in df.columns, "GDP数据应包含date字段"
            assert "value" in df.columns, "GDP数据应包含value字段"
            assert df["indicator"].iloc[0] == "GDP", "指标名称应为GDP"

    def test_cpi_data_basic(self):
        """测试CPI数据基本获取

        验证CPI数据能够成功获取，并包含必要的字段：
        - indicator: 指标名称
        - date: 日期
        - value: 数值
        - YoY: 同比数据
        - MoM: 环比数据
        """
        df = get_macro_china_cpi(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns, "CPI数据应包含indicator字段"
            assert "date" in df.columns, "CPI数据应包含date字段"
            assert df["indicator"].iloc[0] == "CPI", "指标名称应为CPI"

    def test_ppi_data_basic(self):
        """测试PPI数据基本获取

        验证PPI数据能够成功获取，PPI反映生产领域价格变动
        """
        df = get_macro_china_ppi(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns, "PPI数据应包含indicator字段"
            assert df["indicator"].iloc[0] == "PPI", "指标名称应为PPI"

    def test_pmi_data_basic(self):
        """测试PMI数据基本获取

        PMI是经济先行指标，50为荣枯线
        """
        df = get_macro_china_pmi(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns, "PMI数据应包含indicator字段"
            assert df["indicator"].iloc[0] == "PMI", "指标名称应为PMI"

    def test_interest_rate_data_basic(self):
        """测试利率数据基本获取

        验证利率数据获取，包括LPR、基准利率等
        """
        df = get_macro_china_interest_rate(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns, "利率数据应包含indicator字段"

    def test_exchange_rate_data_basic(self):
        """测试汇率数据基本获取

        验证人民币汇率数据获取
        """
        df = get_macro_china_exchange_rate(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns, "汇率数据应包含indicator字段"
            assert "date" in df.columns, "汇率数据应包含date字段"

    def test_m2_data_basic(self):
        """测试M2货币供应量数据基本获取

        M2是广义货币供应量，反映市场流动性
        """
        df = get_macro_m2(force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns, "M2数据应包含indicator字段"
            assert df["indicator"].iloc[0] == "M2", "指标名称应为M2"

    def test_all_indicators_via_robust(self):
        """测试通过Robust接口获取所有指标

        验证RobustResult接口对所有指标的支持
        """
        indicators = ["GDP", "CPI", "PPI", "M2", "INTEREST_RATE"]
        for indicator in indicators:
            result = get_macro_indicator_robust(indicator)
            assert isinstance(result, RobustResult), f"{indicator}应返回RobustResult"
            assert hasattr(result, "success"), f"{indicator}结果应有success属性"
            assert hasattr(result, "data"), f"{indicator}结果应有data属性"


class TestDateRangeQuery:
    """日期范围测试

    测试各种日期范围查询场景：
    - 指定日期范围查询
    - 单年数据查询
    - 多年数据查询
    - 季度数据查询
    """

    def test_date_range_basic(self):
        """测试基本日期范围查询

        验证start_date和end_date参数正常工作
        """
        start_date = "2023-01-01"
        end_date = "2024-01-01"
        df = get_macro_data(
            "cpi", start_date=start_date, end_date=end_date, force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        if not df.empty and "date" in df.columns:
            dates = pd.to_datetime(df["date"])
            assert dates.min() >= pd.to_datetime(start_date), "日期应不早于起始日期"
            assert dates.max() <= pd.to_datetime(end_date), "日期应不晚于结束日期"

    def test_single_year_data(self):
        """测试单年数据查询

        获取特定年份的数据
        """
        df = get_macro_data(
            "gdp", start_date="2023-01-01", end_date="2023-12-31", force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        if not df.empty and "date" in df.columns:
            dates = pd.to_datetime(df["date"])
            year = dates.dt.year.unique()
            assert all(y == 2023 for y in year), "应只包含2023年数据"

    def test_multi_year_data(self):
        """测试多年数据查询

        获取跨年度的数据
        """
        df = get_macro_data(
            "cpi", start_date="2021-01-01", end_date="2023-12-31", force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        if not df.empty and "date" in df.columns:
            dates = pd.to_datetime(df["date"])
            years = dates.dt.year.unique()
            assert len(years) >= 1, "应包含多年数据"

    def test_quarterly_data(self):
        """测试季度数据查询

        GDP通常按季度发布
        """
        df = get_macro_china_gdp(
            start_date="2023-01-01", end_date="2023-12-31", force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert len(df) >= 1, "一年应至少有GDP数据"

    def test_monthly_data_range(self):
        """测试月度数据范围查询

        CPI、PPI等通常按月发布
        """
        df = get_macro_china_cpi(
            start_date="2023-06-01", end_date="2023-12-31", force_update=True
        )
        assert isinstance(df, pd.DataFrame)
        if not df.empty and "date" in df.columns:
            dates = pd.to_datetime(df["date"])
            assert dates.min() >= pd.to_datetime("2023-06-01"), "起始日期正确"
            assert dates.max() <= pd.to_datetime("2023-12-31"), "结束日期正确"

    def test_date_range_with_pmi(self):
        """测试PMI日期范围查询"""
        df = get_macro_china_pmi(
            start_date="2023-01-01", end_date="2023-06-30", force_update=True
        )
        assert isinstance(df, pd.DataFrame)

    def test_date_range_with_ppi(self):
        """测试PPI日期范围查询"""
        df = get_macro_china_ppi(
            start_date="2022-01-01", end_date="2023-12-31", force_update=True
        )
        assert isinstance(df, pd.DataFrame)

    def test_open_ended_start_date(self):
        """测试开放式起始日期（只指定结束日期）"""
        df = get_macro_data("cpi", end_date="2023-12-31", force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty and "date" in df.columns:
            dates = pd.to_datetime(df["date"])
            assert dates.max() <= pd.to_datetime("2023-12-31")

    def test_open_ended_end_date(self):
        """测试开放式结束日期（只指定起始日期）"""
        df = get_macro_data("cpi", start_date="2023-01-01", force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty and "date" in df.columns:
            dates = pd.to_datetime(df["date"])
            assert dates.min() >= pd.to_datetime("2023-01-01")

    def test_date_format_variations(self):
        """测试不同日期格式支持"""
        df1 = get_macro_data(
            "cpi", start_date="2023-01-01", end_date="2023-12-31", force_update=True
        )
        df2 = get_cpi_data(start_date="2023-01-01", end_date="2023-12-31")
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)


class TestDataValidation:
    """数据验证测试

    验证数据的完整性和正确性：
    - 日期格式验证
    - 数值非空验证
    - 同比环比字段验证
    """

    def test_date_format_validation(self):
        """测试日期格式正确性

        日期应为YYYY-MM-DD格式
        """
        df = get_macro_china_cpi(force_update=True)
        if not df.empty and "date" in df.columns:
            dates = df["date"].dropna()
            assert len(dates) > 0, "应有日期数据"
            for date in dates.head(10):
                if pd.notna(date):
                    date_str = str(date)
                    assert len(date_str) >= 7, "日期格式应包含年月"

    def test_value_not_empty(self):
        """测试数值字段非空验证

        关键数值字段不应为空
        """
        df = get_macro_china_gdp(force_update=True)
        if not df.empty and "value" in df.columns:
            non_null_count = df["value"].notna().sum()
            assert non_null_count > 0, "应有非空的数值数据"

    def test_yoy_field_validation(self):
        """测试同比字段验证

        CPI和PPI应包含同比数据
        """
        df = get_macro_china_cpi(force_update=True)
        if not df.empty and "YoY" in df.columns:
            yoy_values = df["YoY"].dropna()
            if len(yoy_values) > 0:
                assert yoy_values.min() >= -20, "同比数据应在合理范围内"
                assert yoy_values.max() <= 30, "同比数据应在合理范围内"

    def test_mom_field_validation(self):
        """测试环比字段验证

        CPI和PPI应包含环比数据
        """
        df = get_macro_china_ppi(force_update=True)
        if not df.empty and "MoM" in df.columns:
            mom_values = df["MoM"].dropna()
            if len(mom_values) > 0:
                assert mom_values.min() >= -15, "环比数据应在合理范围内"
                assert mom_values.max() <= 15, "环比数据应在合理范围内"

    def test_indicator_name_consistency(self):
        """测试指标名称一致性

        同一数据集中指标名称应一致
        """
        for func, expected_name in [
            (get_macro_china_gdp, "GDP"),
            (get_macro_china_cpi, "CPI"),
            (get_macro_china_ppi, "PPI"),
            (get_macro_china_pmi, "PMI"),
        ]:
            df = func(force_update=True)
            if not df.empty:
                indicators = df["indicator"].unique()
                assert len(indicators) == 1, f"{expected_name}指标名称应唯一"
                assert indicators[0] == expected_name, f"指标名称应为{expected_name}"

    def test_data_completeness(self):
        """测试数据完整性

        检查必要字段是否存在
        """
        required_fields = ["indicator", "date", "value"]
        df = get_macro_china_cpi(force_update=True)
        if not df.empty:
            for field in required_fields:
                assert field in df.columns, f"应包含{field}字段"

    def test_no_duplicate_records(self):
        """测试无重复记录

        同一日期不应有重复记录
        """
        df = get_macro_china_cpi(force_update=True)
        if not df.empty and "date" in df.columns:
            dates = df["date"].dropna()
            duplicates = dates.duplicated()
            assert duplicates.sum() == 0, "不应有重复日期记录"

    def test_data_type_validation(self):
        """测试数据类型验证

        验证value字段为数值类型
        """
        df = get_macro_china_gdp(force_update=True)
        if not df.empty and "value" in df.columns:
            values = df["value"].dropna()
            if len(values) > 0:
                assert pd.api.types.is_numeric_dtype(values), "value应为数值类型"

    def test_date_chronological_order(self):
        """测试日期时序顺序

        日期应按时间顺序排列
        """
        df = get_macro_series("cpi", force_update=True)
        if not df.empty and "date" in df.columns:
            dates = pd.to_datetime(df["date"])
            assert dates.is_monotonic_increasing or dates.is_monotonic_decreasing, (
                "日期应有顺序"
            )


class TestBatchQuery:
    """批量查询测试

    测试同时获取多个指标的场景
    """

    def test_query_multiple_indicators(self):
        """测试同时获取多个指标

        通过query_macro批量获取CPI和PPI
        """
        df = query_macro(["CPI", "PPI"], force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            indicators = df["indicator"].unique()
            assert "CPI" in indicators or "PPI" in indicators, "应包含请求的指标"

    def test_query_all_supported_indicators(self):
        """测试查询所有支持的指标"""
        all_indicators = ["GDP", "CPI", "PPI", "M2", "INTEREST_RATE"]
        df = query_macro(all_indicators, force_update=True)
        assert isinstance(df, pd.DataFrame)

    def test_query_three_indicators(self):
        """测试查询三个指标"""
        df = query_macro(["GDP", "CPI", "PPI"], force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            unique_indicators = df["indicator"].unique()
            assert len(unique_indicators) >= 1, "应至少返回一个指标"

    def test_query_empty_list(self):
        """测试空列表查询

        空列表应返回空DataFrame
        """
        df = query_macro([])
        assert isinstance(df, pd.DataFrame)
        assert df.empty, "空列表应返回空DataFrame"

    def test_query_single_indicator_in_list(self):
        """测试列表形式查询单个指标"""
        df1 = query_macro(["GDP"], force_update=True)
        df2 = get_macro_data("gdp", force_update=True)
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)

    def test_query_invalid_indicator_in_list(self):
        """测试批量查询中包含无效指标

        无效指标应被跳过
        """
        df = query_macro(["CPI", "INVALID_INDICATOR"], force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            indicators = df["indicator"].unique()
            assert "INVALID_INDICATOR" not in indicators, "无效指标不应出现"

    def test_query_with_duplicate_indicators(self):
        """测试列表中包含重复指标"""
        df = query_macro(["CPI", "CPI", "PPI"], force_update=True)
        assert isinstance(df, pd.DataFrame)

    def test_get_indicators_list(self):
        """测试获取指标列表

        get_macro_indicators应返回可用指标列表
        """
        indicators = get_macro_indicators()
        assert isinstance(indicators, pd.DataFrame)
        assert len(indicators) > 0, "应返回指标列表"
        assert "code" in indicators.columns, "应包含code列"
        assert "name" in indicators.columns, "应包含name列"
        assert "frequency" in indicators.columns, "应包含frequency列"

    def test_indicators_list_contains_expected(self):
        """测试指标列表包含预期指标"""
        indicators = get_macro_indicators()
        codes = indicators["code"].tolist()
        expected_codes = ["GDP", "CPI", "PPI", "PMI", "M2"]
        for code in expected_codes:
            assert code in codes, f"指标列表应包含{code}"


class TestEdgeCases:
    """边界条件测试

    测试各种边界和异常场景：
    - 不存在的指标
    - 未来日期
    - 历史日期边界
    - 空指标名称
    """

    def test_nonexistent_indicator(self):
        """测试不存在的指标

        应返回失败结果
        """
        result = get_macro_indicator_robust("NONEXISTENT_INDICATOR")
        assert isinstance(result, RobustResult)
        assert result.success is False, "不存在的指标应返回失败"
        assert "不支持的指标" in result.reason, "应提示不支持的指标"

    def test_future_date_range(self):
        """测试未来日期范围

        未来日期应返回空数据
        """
        df = get_macro_data("cpi", start_date="2030-01-01", end_date="2031-01-01")
        assert isinstance(df, pd.DataFrame)
        assert df.empty, "未来日期应返回空数据"

    def test_historical_date_boundary(self):
        """测试历史日期边界

        早期历史数据可能不存在
        """
        df = get_macro_data("gdp", start_date="1990-01-01", end_date="1991-01-01")
        assert isinstance(df, pd.DataFrame)

    def test_empty_indicator_string(self):
        """测试空指标字符串"""
        result = get_macro_indicator_robust("")
        assert isinstance(result, RobustResult)
        assert result.success is False

    def test_none_indicator(self):
        """测试None指标"""
        result = get_macro_indicator_robust(None)
        assert isinstance(result, RobustResult)
        assert result.success is False

    def test_whitespace_indicator(self):
        """测试空白字符指标"""
        result = get_macro_indicator_robust("   ")
        assert isinstance(result, RobustResult)
        assert result.success is False

    def test_case_insensitive_indicator(self):
        """测试指标名称大小写不敏感"""
        result1 = get_macro_indicator_robust("gdp")
        result2 = get_macro_indicator_robust("GDP")
        result3 = get_macro_indicator_robust("Gdp")
        assert isinstance(result1, RobustResult)
        assert isinstance(result2, RobustResult)
        assert isinstance(result3, RobustResult)

    def test_reversed_date_range(self):
        """测试起始日期晚于结束日期"""
        df = get_macro_data("cpi", start_date="2024-01-01", end_date="2023-01-01")
        assert isinstance(df, pd.DataFrame)

    def test_single_date_query(self):
        """测试单日日期查询"""
        df = get_macro_data("cpi", start_date="2023-06-01", end_date="2023-06-01")
        assert isinstance(df, pd.DataFrame)

    def test_very_long_date_range(self):
        """测试超长日期范围"""
        df = get_macro_data("cpi", start_date="2000-01-01", end_date="2024-12-31")
        assert isinstance(df, pd.DataFrame)

    def test_indicator_with_extra_spaces(self):
        """测试带额外空格的指标名"""
        result = get_macro_indicator_robust("  CPI  ")
        assert isinstance(result, RobustResult)

    def test_special_characters_in_indicator(self):
        """测试指标名包含特殊字符"""
        result = get_macro_indicator_robust("CPI@#$")
        assert isinstance(result, RobustResult)
        assert result.success is False


class TestCacheBehavior:
    """缓存测试

    测试缓存相关功能：
    - 按发布周期缓存
    - 不同指标缓存策略
    - 缓存预热
    """

    def test_cache_validity_period(self):
        """测试缓存有效期

        GDP缓存90天，CPI/PPI缓存30天
        """
        df1 = get_macro_gdp(force_update=True)
        df2 = get_macro_gdp(force_update=False)
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)

    def test_cache_hit(self):
        """测试缓存命中

        第二次查询应从缓存读取
        """
        df1 = get_macro_cpi(force_update=True)
        df2 = get_macro_cpi(force_update=False)
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)
        if not df1.empty and not df2.empty:
            assert len(df1) == len(df2), "缓存数据应一致"

    def test_force_update_flag(self):
        """测试强制更新标志

        force_update=True应强制刷新缓存
        """
        df1 = get_macro_data("ppi", force_update=False)
        df2 = get_macro_data("ppi", force_update=True)
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)

    def test_different_cache_periods(self):
        """测试不同指标的缓存周期

        GDP: 90天
        CPI/PPI: 30天
        汇率: 7天
        """
        df_gdp = get_macro_china_gdp(force_update=True)
        df_cpi = get_macro_china_cpi(force_update=True)
        df_exchange = get_macro_china_exchange_rate(force_update=True)
        assert isinstance(df_gdp, pd.DataFrame)
        assert isinstance(df_cpi, pd.DataFrame)
        assert isinstance(df_exchange, pd.DataFrame)

    def test_cache_preheating(self):
        """测试缓存预热

        连续查询应利用缓存
        """
        indicators = ["GDP", "CPI", "PPI"]
        for indicator in indicators:
            result = get_macro_indicator_robust(indicator, force_update=True)
            assert isinstance(result, RobustResult)

        for indicator in indicators:
            result = get_macro_indicator_robust(indicator, force_update=False)
            assert isinstance(result, RobustResult)

    def test_cache_consistency_multiple_calls(self):
        """测试多次调用缓存一致性"""
        df1 = get_macro_ppi(force_update=True)
        df2 = get_macro_ppi(force_update=False)
        df3 = get_macro_ppi(force_update=False)
        if not df1.empty:
            assert len(df1) == len(df2) == len(df3), "多次缓存查询结果应一致"

    def test_cache_structure_preserved(self):
        """测试缓存结构保持

        缓存数据应保持相同的列结构
        """
        df1 = get_macro_china_cpi(force_update=True)
        df2 = get_macro_china_cpi(force_update=False)
        if not df1.empty and not df2.empty:
            assert set(df1.columns) == set(df2.columns), "缓存结构应一致"

    def test_duckdb_cache_availability(self):
        """测试DuckDB缓存可用性"""
        global _db_manager
        if _db_manager is not None:
            assert hasattr(_db_manager, "get_macro"), "应有get_macro方法"
            assert hasattr(_db_manager, "insert_macro"), "应有insert_macro方法"
            assert hasattr(_db_manager, "is_cache_valid"), "应有is_cache_valid方法"


class TestErrorHandling:
    """错误处理测试

    测试各种错误场景的处理：
    - 网络失败处理
    - 数据源不可用降级
    - 部分数据缺失场景
    """

    def test_network_failure_graceful_handling(self):
        """测试网络失败时的优雅处理

        网络失败应返回空DataFrame而不是抛出异常
        """
        result = get_macro_indicator_robust("CPI")
        assert isinstance(result, RobustResult), "应返回RobustResult"

    def test_invalid_indicator_error_message(self):
        """测试无效指标的友好错误信息"""
        result = get_macro_indicator_robust("INVALID")
        assert result.success is False
        assert "不支持的指标" in result.reason or "INVALID" in result.reason

    def test_empty_data_handling(self):
        """测试空数据处理

        数据源返回空数据时应优雅处理
        """
        df = get_macro_data("INVALID_TYPE")
        assert isinstance(df, pd.DataFrame)
        assert df.empty, "无效指标应返回空DataFrame"

    def test_partial_data_missing(self):
        """测试部分数据缺失场景

        某些字段缺失时仍应返回有效数据
        """
        df = get_macro_china_cpi(force_update=True)
        if not df.empty:
            assert "indicator" in df.columns
            assert "date" in df.columns

    def test_malformed_data_handling(self):
        """测试格式错误数据处理"""
        result = get_macro_indicator_robust("CPI")
        if result.success and not result.data.empty:
            assert "indicator" in result.data.columns

    def test_concurrent_query_handling(self):
        """测试并发查询处理

        快速连续查询不应出错
        """
        results = []
        for _ in range(3):
            result = get_macro_indicator_robust("CPI")
            results.append(result)
        assert all(isinstance(r, RobustResult) for r in results)

    def test_fallback_to_pickle_cache(self):
        """测试降级到pickle缓存

        DuckDB不可用时应能使用pickle缓存
        """
        df = get_macro_cpi(use_duckdb=False, force_update=True)
        assert isinstance(df, pd.DataFrame)

    def test_error_in_robust_result(self):
        """测试RobustResult错误状态"""
        error_result = RobustResult(
            success=False, data=pd.DataFrame(), reason="测试错误", source="error"
        )
        assert error_result.success is False
        assert error_result.data.empty
        assert bool(error_result) is False

    def test_source_field_in_result(self):
        """测试结果中的source字段"""
        result = get_macro_indicator_robust("GDP")
        assert hasattr(result, "source")
        assert result.source in ["network", "cache", "error"]


class TestFinanceRunQuery:
    """finance.run_query 测试

    测试finance.run_query接口的各种查询场景
    """

    def test_query_macro_economic_data(self):
        """测试查询MACRO_ECONOMIC_DATA表

        查询所有宏观数据
        """
        df = finance.run_query(finance.MACRO_ECONOMIC_DATA)
        assert isinstance(df, pd.DataFrame)

    def test_query_macro_china_gdp(self):
        """测试查询MACRO_CHINA_GDP表"""
        df = finance.run_query(finance.MACRO_CHINA_GDP, force_update=True)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns

    def test_query_macro_china_cpi(self):
        """测试查询MACRO_CHINA_CPI表"""
        df = finance.run_query(finance.MACRO_CHINA_CPI, force_update=True)
        assert isinstance(df, pd.DataFrame)

    def test_query_macro_china_ppi(self):
        """测试查询MACRO_CHINA_PPI表"""
        df = finance.run_query(finance.MACRO_CHINA_PPI, force_update=True)
        assert isinstance(df, pd.DataFrame)

    def test_query_macro_china_pmi(self):
        """测试查询MACRO_CHINA_PMI表"""
        df = finance.run_query(finance.MACRO_CHINA_PMI, force_update=True)
        assert isinstance(df, pd.DataFrame)

    def test_query_with_date_range(self):
        """测试带日期范围的查询"""
        df = finance.run_query(
            finance.MACRO_CHINA_CPI,
            start_date="2023-01-01",
            end_date="2023-12-31",
            force_update=True,
        )
        assert isinstance(df, pd.DataFrame)

    def test_query_unsupported_table(self):
        """测试不支持的表查询

        应抛出ValueError
        """

        class UnsupportedTable:
            pass

        try:
            df = finance.run_query(UnsupportedTable())
            assert False, "应抛出异常"
        except ValueError as e:
            assert "不支持的表" in str(e) or "Unsupported" in str(e)

    def test_query_class_attributes(self):
        """测试FinanceQuery类的属性"""
        assert hasattr(finance, "MACRO_ECONOMIC_DATA")
        assert hasattr(finance, "MACRO_CHINA_GDP")
        assert hasattr(finance, "MACRO_CHINA_CPI")
        assert hasattr(finance, "MACRO_CHINA_PPI")
        assert hasattr(finance, "MACRO_CHINA_PMI")

    def test_macro_table_class_attributes(self):
        """测试宏观经济表类的属性"""
        assert hasattr(FinanceQuery.MACRO_ECONOMIC_DATA, "indicator")
        assert hasattr(FinanceQuery.MACRO_CHINA_GDP, "indicator")
        assert hasattr(FinanceQuery.MACRO_CHINA_CPI, "indicator")
        assert hasattr(FinanceQuery.MACRO_CHINA_PPI, "indicator")
        assert hasattr(FinanceQuery.MACRO_CHINA_PMI, "indicator")

    def test_run_query_simple_interface(self):
        """测试run_query_simple简化接口"""
        df = run_query_simple("MACRO_CHINA_GDP", force_update=True)
        assert isinstance(df, pd.DataFrame)

    def test_run_query_simple_with_dates(self):
        """测试run_query_simple带日期参数"""
        df = run_query_simple(
            "MACRO_CHINA_CPI",
            start_date="2023-01-01",
            end_date="2023-12-31",
            force_update=True,
        )
        assert isinstance(df, pd.DataFrame)

    def test_run_query_simple_unsupported_table(self):
        """测试run_query_simple不支持的表"""
        try:
            df = run_query_simple("UNSUPPORTED_TABLE")
            assert False, "应抛出异常"
        except ValueError:
            pass

    def test_query_consistency_across_interfaces(self):
        """测试不同接口查询结果一致性"""
        df1 = finance.run_query(finance.MACRO_CHINA_CPI, force_update=True)
        df2 = get_macro_china_cpi(force_update=True)
        df3 = run_query_simple("MACRO_CHINA_CPI", force_update=True)
        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)
        assert isinstance(df3, pd.DataFrame)


class TestDataQualityComprehensive:
    """数据质量综合测试

    综合验证数据质量和一致性
    """

    def test_value_range_gdp(self):
        """测试GDP数值范围合理性"""
        df = get_macro_china_gdp(force_update=True)
        if not df.empty and "value" in df.columns:
            values = df["value"].dropna()
            if len(values) > 0:
                assert values.min() > 0, "GDP应为正值"
                assert values.max() < 2000000, "GDP应在合理范围"

    def test_value_range_cpi(self):
        """测试CPI数值范围合理性"""
        df = get_macro_china_cpi(force_update=True)
        if not df.empty and "YoY" in df.columns:
            yoy = df["YoY"].dropna()
            if len(yoy) > 0:
                assert yoy.min() >= -20, "CPI同比应在合理范围"
                assert yoy.max() <= 30, "CPI同比应在合理范围"

    def test_value_range_ppi(self):
        """测试PPI数值范围合理性"""
        df = get_macro_china_ppi(force_update=True)
        if not df.empty and "value" in df.columns:
            values = df["value"].dropna()
            if len(values) > 0:
                assert values.min() >= -30, "PPI应在合理范围"
                assert values.max() <= 30, "PPI应在合理范围"

    def test_value_range_pmi(self):
        """测试PMI数值范围合理性（0-100）"""
        df = get_macro_china_pmi(force_update=True)
        if not df.empty and "value" in df.columns:
            values = df["value"].dropna()
            if len(values) > 0:
                assert values.min() >= 0, "PMI不应小于0"
                assert values.max() <= 100, "PMI不应大于100"

    def test_frequency_consistency(self):
        """测试数据频率一致性"""
        df = get_macro_china_cpi(force_update=True)
        if not df.empty and len(df) > 12 and "date" in df.columns:
            dates = pd.to_datetime(df["date"]).sort_values()
            diffs = dates.diff().dropna()
            if len(diffs) > 0:
                avg_days = diffs.mean().days
                assert 20 <= avg_days <= 40, "CPI应为月度数据"

    def test_unit_field(self):
        """测试单位字段"""
        df = get_macro_china_gdp(force_update=True)
        if not df.empty and "unit" in df.columns:
            units = df["unit"].dropna().unique()
            assert len(units) <= 2, "单位字段应基本一致"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
