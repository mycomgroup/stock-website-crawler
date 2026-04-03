"""
test_money_flow.py
资金流接口测试

测试覆盖：
1. 单标的资金流查询
2. 多标的资金流查询
3. 日期区间和 count 参数
4. 字段过滤
5. 离线/失败时返回稳定 schema
6. 不同股票代码格式兼容
"""

import pytest
import pandas as pd

pytestmark = pytest.mark.network


class TestBasicQuery:
    """基础查询测试"""

    def test_single_stock(self):
        """单标的查询"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("sh600519", count=1)
        assert isinstance(df, pd.DataFrame)
        assert "sec_code" in df.columns
        assert "date" in df.columns

    def test_multiple_stocks(self):
        """多标的查询"""
        from jk2bt.market_data import get_money_flow

        stocks = ["sh600519", "sz000001"]
        df = get_money_flow(stocks, count=1)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert len(df["sec_code"].unique()) >= 1

    def test_default_fields(self):
        """默认字段返回"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("sh600519", count=1)
        expected_fields = [
            "sec_code",
            "date",
            "change_pct",
            "net_amount_main",
            "net_pct_main",
        ]
        for field in expected_fields:
            assert field in df.columns, f"Missing field: {field}"


class TestFieldsFilter:
    """字段过滤测试"""

    def test_single_field(self):
        """单个字段"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("sh600519", count=1, fields="change_pct")
        assert isinstance(df, pd.DataFrame)
        assert "sec_code" in df.columns
        assert "change_pct" in df.columns

    def test_multiple_fields_list(self):
        """多字段列表"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow(
            "sh600519",
            count=1,
            fields=["sec_code", "date", "change_pct", "net_pct_main"],
        )
        assert isinstance(df, pd.DataFrame)
        assert "sec_code" in df.columns
        assert "change_pct" in df.columns
        assert "net_pct_main" in df.columns

    def test_all_main_fields(self):
        """所有主力相关字段"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow(
            "sh600519",
            count=1,
            fields=[
                "sec_code",
                "date",
                "change_pct",
                "net_amount_main",
                "net_pct_main",
                "net_amount_xl",
                "net_pct_xl",
                "net_amount_l",
                "net_pct_l",
                "net_amount_m",
                "net_pct_m",
                "net_amount_s",
                "net_pct_s",
            ],
        )
        assert isinstance(df, pd.DataFrame)
        assert "net_amount_main" in df.columns
        assert "net_pct_main" in df.columns
        assert "net_amount_xl" in df.columns
        assert "net_amount_l" in df.columns


class TestDateRangeAndCount:
    """日期区间和 count 参数测试"""

    def test_count_parameter(self):
        """count 参数"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("sh600519", count=5)
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert len(df) <= 5

    def test_end_date_parameter(self):
        """end_date 参数"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("sh600519", end_date="2024-01-15", count=1)
        assert isinstance(df, pd.DataFrame)

    def test_start_end_date_range(self):
        """日期区间"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("sh600519", start_date="2024-01-01", end_date="2024-01-31")
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert df["date"].min() >= pd.to_datetime("2024-01-01")
            assert df["date"].max() <= pd.to_datetime("2024-01-31")


class TestSymbolFormatCompatibility:
    """股票代码格式兼容测试"""

    def test_jq_format_xshg(self):
        """聚宽格式 XSHG"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("600519.XSHG", count=1, fields=["sec_code", "change_pct"])
        assert isinstance(df, pd.DataFrame)
        assert "sec_code" in df.columns

    def test_jq_format_xshe(self):
        """聚宽格式 XSHE"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("000001.XSHE", count=1, fields=["sec_code", "change_pct"])
        assert isinstance(df, pd.DataFrame)
        assert "sec_code" in df.columns

    def test_sh_prefix(self):
        """sh 前缀格式"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("sh600519", count=1, fields=["sec_code", "change_pct"])
        assert isinstance(df, pd.DataFrame)
        assert "sec_code" in df.columns

    def test_sz_prefix(self):
        """sz 前缀格式"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("sz000001", count=1, fields=["sec_code", "change_pct"])
        assert isinstance(df, pd.DataFrame)
        assert "sec_code" in df.columns

    def test_pure_code(self):
        """纯数字格式"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("600519", count=1, fields=["sec_code", "change_pct"])
        assert isinstance(df, pd.DataFrame)
        assert "sec_code" in df.columns


class TestStableSchema:
    """稳定 schema 测试"""

    def test_empty_security_list(self):
        """空 security_list 返回稳定 schema"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow(None)
        assert isinstance(df, pd.DataFrame)
        assert df.empty
        assert "sec_code" in df.columns
        assert "date" in df.columns
        assert "change_pct" in df.columns
        assert "net_amount_main" in df.columns
        assert "net_pct_main" in df.columns

    def test_empty_security_list_with_fields(self):
        """空 security_list 指定字段返回稳定 schema"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow(None, fields=["sec_code", "change_pct"])
        assert isinstance(df, pd.DataFrame)
        assert df.empty
        assert "sec_code" in df.columns
        assert "change_pct" in df.columns

    def test_invalid_symbol_returns_stable_schema(self):
        """无效股票代码返回稳定 schema"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("INVALID999999", count=1, fields=["sec_code", "change_pct"])
        assert isinstance(df, pd.DataFrame)
        assert "sec_code" in df.columns
        assert "change_pct" in df.columns

    def test_offline_mode_returns_stable_schema(self):
        """离线模式返回稳定 schema（模拟 akshare 不可用）"""
        from jk2bt.market_data.money_flow import _get_empty_dataframe

        df = _get_empty_dataframe(["sec_code", "change_pct"])
        assert isinstance(df, pd.DataFrame)
        assert df.empty
        assert "sec_code" in df.columns
        assert "change_pct" in df.columns


class TestDataFrameOperations:
    """DataFrame 操作测试"""

    def test_filtering(self):
        """数据筛选"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow(
            ["sh600519", "sz000001"], count=5, fields=["sec_code", "change_pct"]
        )
        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            filtered = df[df["change_pct"] > 0]
            assert isinstance(filtered, pd.DataFrame)

    def test_groupby(self):
        """分组聚合"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow(
            ["sh600519", "sz000001"],
            count=5,
            fields=["sec_code", "net_amount_main", "net_amount_xl"],
        )
        assert isinstance(df, pd.DataFrame)
        if not df.empty and len(df["sec_code"].unique()) > 1:
            grouped = df.groupby("sec_code").sum()
            assert isinstance(grouped, pd.DataFrame)

    def test_pivot(self):
        """Pivot 操作"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow(
            ["sh600519", "sz000001"], count=2, fields=["sec_code", "date", "change_pct"]
        )
        assert isinstance(df, pd.DataFrame)
        if not df.empty and len(df) >= 2:
            pivot_df = df.pivot(index="sec_code", columns="date", values="change_pct")
            assert isinstance(pivot_df, pd.DataFrame)


class TestPositionalArguments:
    """位置参数兼容测试"""

    def test_positional_args_call(self):
        """位置参数调用方式"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow(
            "sh600519", None, "2024-01-15", ["sec_code", "change_pct"], 1
        )
        assert isinstance(df, pd.DataFrame)
        assert "sec_code" in df.columns
        assert "change_pct" in df.columns


class TestIntegrationWithStrategy:
    """策略集成测试"""

    def test_strategy_like_call(self):
        """模拟策略调用"""
        from jk2bt.market_data import get_money_flow

        stock_list = ["sh600519", "sz000001"]
        df = get_money_flow(
            security_list=stock_list,
            end_date="2024-01-15",
            fields=["sec_code", "date", "change_pct", "net_pct_main"],
            count=1,
        )
        assert isinstance(df, pd.DataFrame)
        assert all(
            f in df.columns for f in ["sec_code", "date", "change_pct", "net_pct_main"]
        )

    def test_signal_generation_from_flow(self):
        """从资金流数据生成信号"""
        from jk2bt.market_data import get_money_flow

        df = get_money_flow("sh600519", count=5, fields=["sec_code", "net_pct_main"])
        assert isinstance(df, pd.DataFrame)
        if not df.empty and "net_pct_main" in df.columns:
            avg_main_flow = df["net_pct_main"].mean()
            signal = 1 if avg_main_flow > 0 else -1
            assert signal in [1, -1, 0]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
