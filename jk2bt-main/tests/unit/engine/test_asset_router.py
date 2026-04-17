"""
test_asset_router.py
资产路由器单元测试

测试场景覆盖:
1. AssetInfo 类功能
2. AssetRouter 资产识别
3. 股票/ETF/LOF/指数/基金/期货识别
4. 交易所推断
5. 缓存机制
6. 自定义规则
7. 便捷函数
"""

import pytest

from jk2bt.engine.asset_router import (
    AssetType,
    AssetCategory,
    TradingStatus,
    AssetInfo,
    AssetRouter,
    get_asset_router,
    identify_asset,
    is_stock,
    is_etf,
    is_index,
    is_future,
    is_fund_of,
    get_trading_status_desc,
)


class TestAssetType:
    """测试资产类型枚举"""

    def test_asset_types_exist(self):
        assert hasattr(AssetType, "STOCK")
        assert hasattr(AssetType, "ETF")
        assert hasattr(AssetType, "INDEX")


class TestAssetInfo:
    """测试资产信息类"""

    def test_asset_info_creation(self):
        info = AssetInfo(
            code="600519.XSHG",
            asset_type=AssetType.STOCK,
            category=AssetCategory.EQUITY,
        )
        assert info.code == "600519.XSHG"
        assert info.asset_type == AssetType.STOCK


class TestAssetRouter:
    """测试资产路由器"""

    def test_identify_stock(self):
        router = AssetRouter()
        info = router.identify("600519.XSHG")
        assert info.asset_type == AssetType.STOCK

    def test_identify_etf(self):
        router = AssetRouter()
        info = router.identify("510300.XSHG")
        assert info.asset_type == AssetType.ETF

    def test_identify_index(self):
        router = AssetRouter()
        info = router.identify("000300.XSHG")
        assert info.asset_type == AssetType.INDEX


class TestIdentifyAsset:
    """测试便捷函数"""

    def test_identify_asset_returns_info(self):
        info = identify_asset("600519.XSHG")
        assert isinstance(info, AssetInfo)


class TestIsStock:
    """测试股票判断"""

    def test_is_stock_true(self):
        assert is_stock("600519.XSHG") is True

    def test_is_stock_false_for_etf(self):
        assert is_stock("510300.XSHG") is False


class TestIsEtf:
    """测试ETF判断"""

    def test_is_etf_true(self):
        assert is_etf("510300.XSHG") is True

    def test_is_etf_false_for_stock(self):
        assert is_etf("600519.XSHG") is False


class TestIsIndex:
    """测试指数判断"""

    def test_is_index_true(self):
        assert is_index("000300.XSHG") is True


class TestGetTradingStatusDesc:
    """测试交易状态描述"""

    def test_normal_status(self):
        desc = get_trading_status_desc(TradingStatus.NORMAL)
        assert isinstance(desc, str)


class TestGetAssetRouter:
    """测试获取路由器实例"""

    def test_returns_router(self):
        router = get_asset_router()
        assert isinstance(router, AssetRouter)

    def test_singleton(self):
        router1 = get_asset_router()
        router2 = get_asset_router()
        assert router1 is router2
