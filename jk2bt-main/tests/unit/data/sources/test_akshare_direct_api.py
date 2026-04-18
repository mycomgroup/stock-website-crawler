"""
test_akshare_direct_api.py
直接测试 akshare API 连通性（不连缓存）

目的：
1. 验证 akshare API 本身是否可用
2. 最小量数据测试（减少网络请求时间）
3. 排除缓存层问题，直接定位 API 问题

外部依赖：
- akshare（唯一的数据源）
- pandas（数据处理）
- 标准库（无其他第三方依赖）
"""

import pytest
import pandas as pd
import akshare as ak
from datetime import datetime


def _skip_on_network_error(func, *args, **kwargs):
    """网络错误时跳过，不标记为失败"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_msg = str(e)
        if any(
            keyword in error_msg
            for keyword in [
                "Connection",
                "Timeout",
                "Remote",
                "Network",
                "aborted",
                "disconnected",
                "refused",
            ]
        ):
            pytest.skip(f"网络问题: {e}")
        raise


class TestAkShareDirectAPI:
    """直接测试 akshare API（不连缓存）"""

    # ── 股票日线 ──

    def test_stock_zh_a_hist(self):
        """股票日线（东方财富）"""
        df = _skip_on_network_error(
            ak.stock_zh_a_hist,
            symbol="600519",
            period="daily",
            start_date="20240101",
            end_date="20240105",
            adjust="qfq",
        )
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_stock_zh_a_hist_min(self):
        """股票分钟线"""
        df = _skip_on_network_error(
            ak.stock_zh_a_hist_min_em,
            symbol="600519",
            period="5",
            adjust="qfq",
        )
        assert isinstance(df, pd.DataFrame)

    # ── 指数 ──

    def test_index_zh_a_hist(self):
        """指数日线"""
        df = _skip_on_network_error(
            ak.index_zh_a_hist,
            symbol="000300",
            period="daily",
            start_date="20240101",
            end_date="20240105",
        )
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_index_stock_cons(self):
        """指数成分股"""
        df = _skip_on_network_error(
            ak.index_stock_cons,
            symbol="000300",
        )
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_index_stock_cons_weight(self):
        """指数成分股权重"""
        df = _skip_on_network_error(
            ak.index_stock_cons_weight_csindex,
            symbol="000300",
        )
        assert isinstance(df, pd.DataFrame)

    # ── 行业 ──

    def test_index_component_sw(self):
        """申万行业成分股"""
        df = _skip_on_network_error(
            ak.index_component_sw,
            symbol="801010",
        )
        assert isinstance(df, pd.DataFrame)

    def test_stock_board_industry_name_em(self):
        """行业列表"""
        df = _skip_on_network_error(
            ak.stock_board_industry_name_em,
        )
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_stock_individual_info_em(self):
        """股票信息"""
        df = _skip_on_network_error(
            ak.stock_individual_info_em,
            symbol="600519",
        )
        assert isinstance(df, pd.DataFrame)

    # ── 财务 ──

    def test_stock_financial_analysis_indicator(self):
        """财务分析指标"""
        df = _skip_on_network_error(
            ak.stock_financial_analysis_indicator,
            symbol="600519",
        )
        assert isinstance(df, pd.DataFrame)

    def test_stock_financial_report_sina(self):
        """财务报表"""
        df = _skip_on_network_error(
            ak.stock_financial_report_sina,
            stock="600519",
            symbol="资产负债表",
        )
        assert isinstance(df, pd.DataFrame)

    def test_stock_balance_sheet_by_report_em(self):
        """资产负债表"""
        df = _skip_on_network_error(
            ak.stock_balance_sheet_by_report_em,
            symbol="SH600519",
        )
        assert isinstance(df, pd.DataFrame)

    # ── 资金流 ──

    def test_stock_individual_fund_flow(self):
        """个股资金流"""
        df = _skip_on_network_error(
            ak.stock_individual_fund_flow,
            stock="600519",
            market="sh",
        )
        assert isinstance(df, pd.DataFrame)

    def test_stock_fund_flow_individual(self):
        """个股资金流向（东方财富）"""
        df = _skip_on_network_error(
            ak.stock_individual_fund_flow,
            stock="600519",
            market="sh",
        )
        assert isinstance(df, pd.DataFrame)

    # ── 分红 ──

    def test_stock_fhps_em(self):
        """分红送股（按日期）"""
        df = _skip_on_network_error(
            ak.stock_fhps_em,
            date="20231231",
        )
        assert isinstance(df, pd.DataFrame)

    def test_stock_dividend_cninfo(self):
        """分红信息"""
        df = _skip_on_network_error(
            ak.stock_dividend_cninfo,
            symbol="600519",
        )
        assert isinstance(df, pd.DataFrame)

    # ── 股东 ──

    def test_stock_zh_a_gdhs(self):
        """股东户数"""
        df = _skip_on_network_error(
            ak.stock_zh_a_gdhs,
            symbol="20230930",
        )
        assert isinstance(df, pd.DataFrame)

    def test_stock_share_change_cninfo(self):
        """股本变动"""
        df = _skip_on_network_error(
            ak.stock_share_change_cninfo,
            symbol="600519",
        )
        assert isinstance(df, pd.DataFrame)

    # ── 质押/解禁 ──

    def test_stock_gpzy_pledge_ratio_em(self):
        """股权质押比例"""
        df = _skip_on_network_error(
            ak.stock_gpzy_pledge_ratio_em,
            date="20240105",
        )
        assert isinstance(df, pd.DataFrame)

    def test_stock_restricted_release_detail_em(self):
        """解禁计划"""
        df = _skip_on_network_error(
            ak.stock_restricted_release_detail_em,
            start_date="20240101",
            end_date="20240301",
        )
        assert isinstance(df, pd.DataFrame)

    # ── 估值 ──

    def test_stock_a_all_pb(self):
        """全市场 PE/PB"""
        df = _skip_on_network_error(
            ak.stock_a_all_pb,
        )
        assert isinstance(df, pd.DataFrame)

    def test_stock_financial_analysis_indicator_em(self):
        """财务指标（东方财富）"""
        df = _skip_on_network_error(
            ak.stock_financial_analysis_indicator_em,
            symbol="600519.SH",
        )
        assert isinstance(df, pd.DataFrame)

    def test_stock_zh_index_value_csindex(self):
        """指数估值"""
        df = _skip_on_network_error(
            ak.stock_zh_index_value_csindex,
            symbol="H30374",
        )
        assert isinstance(df, pd.DataFrame)

    # ── 宏观 ──

    def test_macro_china_gdp(self):
        """GDP"""
        df = _skip_on_network_error(
            ak.macro_china_gdp,
        )
        assert isinstance(df, pd.DataFrame)

    # ── 融资融券 ──

    def test_stock_margin_detail_sse(self):
        """上交所融资融券"""
        df = _skip_on_network_error(
            ak.stock_margin_detail_sse,
            date="20240105",
        )
        assert isinstance(df, pd.DataFrame)

    def test_stock_margin_underlying_info_szse(self):
        """深交所融资融券标的"""
        df = _skip_on_network_error(
            ak.stock_margin_underlying_info_szse,
        )
        assert isinstance(df, pd.DataFrame)

    # ── 交易日 ──

    def test_tool_trade_date_hist_sina(self):
        """交易日历"""
        df = _skip_on_network_error(
            ak.tool_trade_date_hist_sina,
        )
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    # ── 证券列表 ──

    def test_stock_info_a_code_name(self):
        """A股代码名称"""
        df = _skip_on_network_error(
            ak.stock_info_a_code_name,
        )
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_stock_sh_a_spot_em(self):
        """沪市实时行情"""
        df = _skip_on_network_error(
            ak.stock_sh_a_spot_em,
        )
        assert isinstance(df, pd.DataFrame)


class TestAkShareAPIAvailability:
    """测试 akshare API 是否存在"""

    def test_api_count(self):
        """统计 akshare API 数量"""
        apis = [name for name in dir(ak) if not name.startswith("_")]
        print(f"\nakshare API 数量: {len(apis)}")
        assert len(apis) > 100, "akshare 应有大量 API"

    def test_version(self):
        """检查 akshare 版本"""
        version = ak.__version__
        print(f"\nakshare 版本: {version}")
        assert version, "应有版本号"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--timeout=120"])
