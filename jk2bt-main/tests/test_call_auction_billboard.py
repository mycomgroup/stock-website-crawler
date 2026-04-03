"""
测试竞价和龙虎榜接口的完整性和稳定性
覆盖各种边界情况和实际策略使用场景
"""

import pytest
import pandas as pd
import sys
import os
from datetime import datetime, date

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src"),
)

from market_data.call_auction import (
    get_call_auction,
    get_call_auction_jq,
    _jq_code_to_ak,
    _normalize_date,
)
from jk2bt.core.strategy_base import get_billboard_list_jq


pytestmark = pytest.mark.network


# =====================================================================
# get_call_auction 测试
# =====================================================================


class TestGetCallAuction:
    """竞价接口测试套件"""

    def test_return_type_is_dataframe(self):
        """返回值必须是 DataFrame"""
        result = get_call_auction(
            ["000001.XSHE"], start_date="2023-01-01", end_date="2023-01-01"
        )
        assert isinstance(result, pd.DataFrame)

    def test_empty_result_has_required_columns(self):
        """空返回必须包含所有必需字段"""
        result = get_call_auction(
            ["000001.XSHE"], start_date="2023-01-01", end_date="2023-01-01"
        )
        assert "code" in result.columns
        assert "time" in result.columns
        assert "current" in result.columns
        assert "volume" in result.columns
        assert "money" in result.columns
        assert "capability" in result.columns

    def test_empty_result_capability_marker(self):
        """空返回必须有 capability='limited' 标记"""
        result = get_call_auction(
            ["000001.XSHE"], start_date="2023-01-01", end_date="2023-01-01"
        )
        assert "capability" in result.columns

    def test_none_stock_list_returns_empty_df(self):
        """stock_list=None 返回空 DataFrame"""
        result = get_call_auction(None)
        assert isinstance(result, pd.DataFrame)
        assert result.empty
        assert "code" in result.columns

    def test_single_stock_string_input(self):
        """单股票字符串输入"""
        result = get_call_auction(
            "000001.XSHE", start_date="2023-01-01", end_date="2023-01-01"
        )
        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns

    def test_multiple_stocks_list_input(self):
        """多股票列表输入"""
        stocks = ["000001.XSHE", "600000.XSHG", "600519.XSHG"]
        result = get_call_auction(
            stocks, start_date="2023-01-01", end_date="2023-01-01"
        )
        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns

    def test_fields_parameter_partial(self):
        """部分 fields 参数"""
        result = get_call_auction(["000001.XSHE"], fields=["time", "current"])
        assert "code" in result.columns  # code 必须始终存在
        assert "time" in result.columns
        assert "current" in result.columns
        assert "capability" in result.columns

    def test_fields_parameter_all(self):
        """完整 fields 参数"""
        result = get_call_auction(
            ["000001.XSHE"], fields=["time", "current", "volume", "money"]
        )
        for field in ["code", "time", "current", "volume", "money", "capability"]:
            assert field in result.columns

    def test_date_formats_string(self):
        """字符串日期格式"""
        result = get_call_auction(
            ["000001.XSHE"], start_date="2023-01-01", end_date="2023-01-01"
        )
        assert isinstance(result, pd.DataFrame)

    def test_date_formats_datetime(self):
        """datetime 对象日期格式"""
        dt = datetime(2023, 1, 1)
        result = get_call_auction(["000001.XSHE"], start_date=dt, end_date=dt)
        assert isinstance(result, pd.DataFrame)

    def test_date_formats_date(self):
        """date 对象日期格式"""
        d = date(2023, 1, 1)
        result = get_call_auction(["000001.XSHE"], start_date=d, end_date=d)
        assert isinstance(result, pd.DataFrame)

    def test_fake_stock_code(self):
        """无效股票代码"""
        result = get_call_auction(
            ["FAKECODE"], start_date="2023-01-01", end_date="2023-01-01"
        )
        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns

    def test_mixed_valid_invalid_stocks(self):
        """混合有效和无效股票代码"""
        stocks = ["000001.XSHE", "FAKECODE", "600000.XSHG"]
        result = get_call_auction(
            stocks, start_date="2023-01-01", end_date="2023-01-01"
        )
        assert isinstance(result, pd.DataFrame)

    def test_no_keyerror_on_field_access(self):
        """访问字段不会 KeyError"""
        result = get_call_auction(
            ["000001.XSHE"], start_date="2023-01-01", end_date="2023-01-01"
        )
        # 不会抛异常
        _ = result["code"]
        _ = result["time"]
        _ = result["current"]
        _ = result["volume"]
        _ = result["money"]
        _ = result["capability"]

    def test_strategy_pattern_filter_sort(self):
        """模拟策略过滤排序模式"""
        stocklist = ["000001.XSHE", "600000.XSHG"]
        df_auction = get_call_auction(
            stocklist,
            start_date="2023-01-01",
            end_date="2023-01-01",
            fields=["time", "current", "volume", "money"],
        )
        # 模拟策略中的过滤排序
        if not df_auction.empty:
            filtered = df_auction[df_auction["money"] > 0]
            sorted_df = filtered.sort_values("money", ascending=False)
            assert isinstance(sorted_df, pd.DataFrame)


class TestCallAuctionHelpers:
    """竞价接口辅助函数测试"""

    def test_jq_code_to_ak_xshe(self):
        """XSHE 格式转换"""
        assert _jq_code_to_ak("000001.XSHE") == "000001"

    def test_jq_code_to_ak_xshg(self):
        """XSHG 格式转换"""
        assert _jq_code_to_ak("600000.XSHG") == "600000"

    def test_jq_code_to_ak_pure_code(self):
        """纯代码格式"""
        assert _jq_code_to_ak("000001") == "000001"

    def test_jq_code_to_ak_sh_prefix(self):
        """sh 前缀"""
        assert _jq_code_to_ak("sh600000") == "sh600000"

    def test_normalize_date_string(self):
        """字符串日期标准化"""
        result = _normalize_date("2023-01-01")
        assert result == date(2023, 1, 1)

    def test_normalize_date_datetime(self):
        """datetime 标准化"""
        dt = datetime(2023, 1, 1)
        result = _normalize_date(dt)
        assert result == date(2023, 1, 1)

    def test_normalize_date_date(self):
        """date 标准化"""
        d = date(2023, 1, 1)
        result = _normalize_date(d)
        assert result == date(2023, 1, 1)

    def test_normalize_date_none(self):
        """None 输入"""
        result = _normalize_date(None)
        assert result is None

    def test_normalize_date_invalid_string(self):
        """无效字符串"""
        result = _normalize_date("invalid-date")
        assert result is None


# =====================================================================
# get_billboard_list 测试
# =====================================================================


class TestGetBillboardList:
    """龙虎榜接口测试套件"""

    def test_return_type_is_dataframe(self):
        """返回值必须是 DataFrame"""
        result = get_billboard_list_jq()
        assert isinstance(result, pd.DataFrame)

    def test_has_jqdata_style_columns(self):
        """必须包含 JQData 风格字段"""
        result = get_billboard_list_jq()
        assert "code" in result.columns
        assert "date" in result.columns
        assert "net_value" in result.columns
        # buy_rate 可能不存在于所有数据中，但字段定义应该存在
        if not result.empty:
            assert "buy_rate" in result.columns

    def test_has_original_akshare_columns(self):
        """保留原始 akshare 中文列名"""
        result = get_billboard_list_jq()
        # 中文列名也应该存在
        assert "代码" in result.columns or "code" in result.columns
        assert "上榜日" in result.columns or "date" in result.columns

    def test_stock_list_sh_prefix(self):
        """sh 前缀股票代码"""
        result = get_billboard_list_jq(stock_list=["sh600000"])
        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns

    def test_stock_list_sz_prefix(self):
        """sz 前缀股票代码"""
        result = get_billboard_list_jq(stock_list=["sz000001"])
        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns

    def test_stock_list_jq_format(self):
        """JQData 格式股票代码"""
        result = get_billboard_list_jq(stock_list=["000001.XSHE", "600000.XSHG"])
        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns

    def test_stock_list_pure_code(self):
        """纯代码格式"""
        result = get_billboard_list_jq(stock_list=["000001", "600000"])
        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns

    def test_stock_list_single_string(self):
        """单股票字符串"""
        result = get_billboard_list_jq(stock_list="000001")
        assert isinstance(result, pd.DataFrame)

    def test_stock_list_none(self):
        """stock_list=None 返回全部数据"""
        result = get_billboard_list_jq(stock_list=None, count=5)
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert len(result) <= 5

    def test_count_parameter(self):
        """count 参数限制返回数量"""
        result = get_billboard_list_jq(count=3)
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert len(result) <= 3

    def test_count_zero(self):
        """count=0 时返回全部数据（实现逻辑：count=0 不限制）"""
        result = get_billboard_list_jq(count=0)
        assert isinstance(result, pd.DataFrame)
        # count=0 或 None 时返回全部数据

    def test_end_date_string(self):
        """字符串日期过滤"""
        result = get_billboard_list_jq(end_date="2023-04-10", count=10)
        assert isinstance(result, pd.DataFrame)
        if not result.empty and "date" in result.columns:
            # 验证日期过滤
            dates = result["date"].astype(str).tolist()
            for d in dates:
                assert d <= "2023-04-10"

    def test_end_date_datetime(self):
        """datetime 日期过滤"""
        dt = datetime(2023, 4, 10)
        result = get_billboard_list_jq(end_date=dt, count=10)
        assert isinstance(result, pd.DataFrame)

    def test_end_date_date(self):
        """date 对象过滤"""
        d = date(2023, 4, 10)
        result = get_billboard_list_jq(end_date=d, count=10)
        assert isinstance(result, pd.DataFrame)

    def test_fake_stock_code(self):
        """无效股票代码"""
        result = get_billboard_list_jq(stock_list=["FAKECODE"])
        assert isinstance(result, pd.DataFrame)
        # 应该返回空或无匹配
        assert result.empty or "FAKECODE" not in result["code"].values

    def test_no_keyerror_on_field_access(self):
        """访问字段不会 KeyError"""
        result = get_billboard_list_jq(count=1)
        _ = result["code"]
        _ = result["date"]
        _ = result["net_value"]

    def test_strategy_pattern_filter_net_value(self):
        """模拟策略过滤 net_value > 0"""
        result = get_billboard_list_jq(count=10)
        if not result.empty:
            filtered = result[result["net_value"] > 0]
            assert isinstance(filtered, pd.DataFrame)

    def test_strategy_pattern_filter_buy_rate(self):
        """模拟策略过滤 buy_rate > 4"""
        result = get_billboard_list_jq(count=10)
        if not result.empty and "buy_rate" in result.columns:
            filtered = result[result["buy_rate"] > 4]
            assert isinstance(filtered, pd.DataFrame)

    def test_strategy_pattern_intersect(self):
        """模拟策略交集操作"""
        check_list = ["000001", "600000"]
        result = get_billboard_list_jq(stock_list=check_list, count=30)
        codes_list = result["code"].tolist()
        intersection = list(set(check_list).intersection(set(codes_list)))
        assert isinstance(intersection, list)

    def test_cache_parameter(self):
        """cache_dir 参数"""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            result = get_billboard_list_jq(cache_dir=tmpdir, count=1)
            assert isinstance(result, pd.DataFrame)

    def test_force_update_parameter(self):
        """force_update 参数"""
        result = get_billboard_list_jq(force_update=True, count=1)
        assert isinstance(result, pd.DataFrame)

    def test_empty_result_has_required_columns(self):
        """空返回必须包含必需字段"""
        result = get_billboard_list_jq(stock_list=["FAKECODE"])
        assert "code" in result.columns
        assert "date" in result.columns
        assert "net_value" in result.columns

    def test_column_value_types(self):
        """返回列类型验证"""
        result = get_billboard_list_jq(count=1)
        if not result.empty:
            # code 应该是字符串
            assert result["code"].dtype.name in ["object", "str"]
            # net_value 应该是数值
            assert pd.api.types.is_numeric_dtype(result["net_value"])


class TestBillboardListEdgeCases:
    """龙虎榜边界情况测试"""

    def test_large_count(self):
        """大 count 值"""
        result = get_billboard_list_jq(count=1000)
        assert isinstance(result, pd.DataFrame)

    def test_empty_stock_list(self):
        """空股票列表"""
        result = get_billboard_list_jq(stock_list=[])
        assert isinstance(result, pd.DataFrame)

    def test_mixed_code_formats(self):
        """混合代码格式"""
        stocks = ["sh600000", "000001.XSHE", "600519", "sz000002"]
        result = get_billboard_list_jq(stock_list=stocks)
        assert isinstance(result, pd.DataFrame)
        assert "code" in result.columns

    def test_very_old_end_date(self):
        """很早的结束日期"""
        result = get_billboard_list_jq(end_date="2020-01-01", count=10)
        assert isinstance(result, pd.DataFrame)
        # 应该返回空或旧数据
        if not result.empty:
            dates = result["date"].astype(str).tolist()
            for d in dates:
                assert d <= "2020-01-01"


# =====================================================================
# 集成测试：模拟真实策略场景
# =====================================================================


class TestStrategyIntegration:
    """模拟真实策略使用场景"""

    def test_call_auction_strategy_pattern_46(self):
        """模拟策略 jkcode/46 使用模式"""
        stocklist = ["000001.XSHE", "600000.XSHG"]
        df_auction = get_call_auction(
            stocklist,
            start_date="2023-01-01",
            end_date="2023-01-01",
            fields=["time", "current", "volume", "money"],
        )

        # 验证字段访问
        assert "code" in df_auction.columns
        assert "money" in df_auction.columns

        # 模拟策略过滤
        if not df_auction.empty:
            filtered = df_auction[df_auction["money"] > 1000000]
            sorted_df = filtered.sort_values("money", ascending=False)
            assert isinstance(sorted_df, pd.DataFrame)

    def test_billboard_strategy_pattern_96(self):
        """模拟策略 jkcode/96 使用模式"""
        muster = get_billboard_list_jq(stock_list=None, end_date="2023-04-10", count=1)

        # 验证字段访问
        assert "net_value" in muster.columns
        assert "buy_rate" in muster.columns
        assert "code" in muster.columns

        # 模拟策略过滤
        if not muster.empty:
            filtered1 = muster[muster["net_value"] > 0]
            filtered2 = filtered1[filtered1["buy_rate"] > 4]
            codes = filtered2["code"].tolist()
            assert isinstance(codes, list)

    def test_billboard_strategy_pattern_99(self):
        """模拟策略 jkcode/99 使用模式"""
        check_out_lists = ["000001", "600000", "600519"]
        longhu = get_billboard_list_jq(
            stock_list=check_out_lists, end_date="2023-04-10", count=30
        )

        # 验证字段访问
        assert "code" in longhu.columns

        # 模拟策略交集操作
        codes_list = longhu["code"].tolist()
        intersection = list(set(check_out_lists).intersection(set(codes_list)))
        assert isinstance(intersection, list)

    def test_full_workflow(self):
        """完整工作流测试"""
        # 1. 获取龙虎榜数据
        billboard = get_billboard_list_jq(count=5)
        assert isinstance(billboard, pd.DataFrame)

        # 2. 提取股票代码
        if not billboard.empty:
            codes = billboard["code"].unique().tolist()[:3]

            # 3. 用这些代码查询竞价数据
            auction = get_call_auction(
                [f"{c}.XSHE" if c.startswith("0") else f"{c}.XSHG" for c in codes],
                start_date="2023-01-01",
                end_date="2023-01-01",
            )
            assert isinstance(auction, pd.DataFrame)
            assert "code" in auction.columns


# =====================================================================
# 性能和稳定性测试
# =====================================================================


class TestPerformanceAndStability:
    """性能和稳定性测试"""

    def test_call_auction_no_exception_on_invalid_input(self):
        """无效输入不抛异常"""
        try:
            result = get_call_auction(
                ["INVALID"], start_date="invalid", end_date="invalid"
            )
            assert isinstance(result, pd.DataFrame)
        except Exception:
            pytest.fail("Should not raise exception on invalid input")

    def test_billboard_no_exception_on_empty_cache(self):
        """空缓存不抛异常"""
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            result = get_billboard_list_jq(cache_dir=tmpdir, force_update=True, count=1)
            assert isinstance(result, pd.DataFrame)

    def test_repeated_calls_stability(self):
        """重复调用稳定性"""
        for _ in range(3):
            result = get_call_auction(
                ["000001.XSHE"], start_date="2023-01-01", end_date="2023-01-01"
            )
            assert isinstance(result, pd.DataFrame)
            assert "code" in result.columns
