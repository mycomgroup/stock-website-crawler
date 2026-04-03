"""
test_multi_asset_data.py
多资产数据接入验证测试。

验证 LOF、场外基金、股指期货的数据可读性。
"""

import pytest
import pandas as pd

# 只导入实际存在的函数
try:
    from jk2bt.market_data import (
        get_lof_daily,
        get_lof_spot,
    )

    HAS_LOF = True
except ImportError:
    HAS_LOF = False

try:
    from jk2bt.asset_router import (
        identify_asset,
        AssetType,
        TradingStatus,
    )

    HAS_ASSET_ROUTER = True
except ImportError:
    HAS_ASSET_ROUTER = False

pytestmark = pytest.mark.skipif(
    not (HAS_LOF and HAS_ASSET_ROUTER), reason="Required modules not available"
)


@pytest.mark.skipif(not HAS_ASSET_ROUTER, reason="Asset router not available")
class TestAssetRouter:
    def test_identify_lof(self):
        info = identify_asset("161725")
        assert info.asset_type == AssetType.LOF
        assert info.trading_status in (
            TradingStatus.NETWORK_UNSTABLE,
            TradingStatus.SUPPORTED,
        )

    def test_identify_fund_of(self):
        info = identify_asset("000001.OF")
        assert info.asset_type == AssetType.FUND_OF
        assert info.is_identified_only()

    def test_identify_future_ccfx(self):
        info = identify_asset("IF2401.CCFX")
        assert info.asset_type == AssetType.FUTURE_CCFX
        assert info.is_identified_only()

    def test_is_data_readable(self):
        assert is_data_readable("IF2401.CCFX") == False
        assert is_data_readable("000001.OF") == False
        assert is_data_readable("161725") == True


class TestFundOfData:
    def test_get_fund_of_nav_success(self):
        df = get_fund_of_nav("000001", start="2024-01-01", end="2024-01-31")

        assert df is not None
        assert not df.empty
        assert "datetime" in df.columns
        assert "unit_nav" in df.columns
        assert "acc_nav" in df.columns
        assert len(df) > 0

    def test_get_fund_of_nav_sample2(self):
        df = get_fund_of_nav("110022")

        assert df is not None
        assert not df.empty
        assert "unit_nav" in df.columns

    def test_get_fund_of_daily_list(self):
        df = get_fund_of_daily_list()

        assert df is not None
        assert not df.empty
        assert "基金代码" in df.columns


class TestFutureCcfxData:
    def test_get_future_ccfx_daily_success(self):
        df = get_future_ccfx_daily("IF2401", start="2024-01-01", end="2024-01-31")

        assert df is not None
        assert not df.empty
        assert "datetime" in df.columns
        assert "open" in df.columns
        assert "high" in df.columns
        assert "low" in df.columns
        assert "close" in df.columns
        assert len(df) > 0

    def test_get_future_ccfx_daily_sample2(self):
        df = get_future_ccfx_daily("IC2401")

        assert df is not None
        assert not df.empty

    def test_list_future_ccfx_contracts(self):
        contracts = list_future_ccfx_contracts("IF")

        assert contracts is not None
        assert len(contracts) > 0
        assert any("IF" in c for c in contracts)


class TestLofData:
    @pytest.mark.skip(reason="LOF接口网络不稳定，可能失败")
    def test_get_lof_daily(self):
        try:
            df = get_lof_daily("161725", start="2024-01-01", end="2024-01-31")

            assert df is not None
            assert not df.empty
            assert "datetime" in df.columns
            assert "open" in df.columns
            assert "close" in df.columns
        except ValueError as e:
            pytest.skip(f"LOF接口失败: {str(e)}")

    @pytest.mark.skip(reason="LOF接口网络不稳定，可能失败")
    def test_get_lof_spot(self):
        try:
            df = get_lof_spot()
            assert df is not None
        except Exception as e:
            pytest.skip(f"LOF实时行情失败: {str(e)}")


class TestDataStandardization:
    def test_future_ohlcv_has_openinterest(self):
        df = get_future_ccfx_daily("IF2401")

        if not df.empty:
            assert "openinterest" in df.columns

    def test_fund_nav_datetime_sorted(self):
        df = get_fund_of_nav("000001")

        if not df.empty:
            assert df["datetime"].is_monotonic_increasing


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
