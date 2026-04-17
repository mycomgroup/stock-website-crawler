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

import sys
import types
import importlib.util
import pytest
from pathlib import Path
from unittest.mock import MagicMock

project_root = Path(__file__).parent.parent.parent.parent

# 直接加载模块，绕过 jk2bt.__init__.py 的复杂导入链
_symbol_spec = importlib.util.spec_from_file_location(
    "symbol", str(project_root / "jk2bt/utils/symbol.py")
)
_symbol_mod = importlib.util.module_from_spec(_symbol_spec)
_symbol_spec.loader.exec_module(_symbol_mod)

_jk2bt_utils = types.ModuleType("jk2bt.utils")
_jk2bt_utils.symbol = _symbol_mod

_jk2bt = types.ModuleType("jk2bt")
_jk2bt.utils = _jk2bt_utils

sys.modules["jk2bt"] = _jk2bt
sys.modules["jk2bt.utils"] = _jk2bt_utils
sys.modules["jk2bt.utils.symbol"] = _symbol_mod

_asset_router_spec = importlib.util.spec_from_file_location(
    "asset_router", str(project_root / "jk2bt/engine/asset_router.py")
)
_asset_router_mod = importlib.util.module_from_spec(_asset_router_spec)
sys.modules["jk2bt.engine.asset_router"] = _asset_router_mod
_asset_router_spec.loader.exec_module(_asset_router_mod)

# 导出测试需要的类
AssetType = _asset_router_mod.AssetType
AssetCategory = _asset_router_mod.AssetCategory
TradingStatus = _asset_router_mod.TradingStatus
AssetInfo = _asset_router_mod.AssetInfo
AssetRouter = _asset_router_mod.AssetRouter
get_asset_router = _asset_router_mod.get_asset_router
identify_asset = _asset_router_mod.identify_asset
is_etf = _asset_router_mod.is_etf
is_stock = _asset_router_mod.is_stock
is_fund_of = _asset_router_mod.is_fund_of
is_future = _asset_router_mod.is_future
is_index = _asset_router_mod.is_index
get_trading_status_desc = _asset_router_mod.get_trading_status_desc
is_data_readable = _asset_router_mod.is_data_readable


class TestAssetInfo:
    """测试 AssetInfo 类"""

    def test_init_basic(self):
        info = AssetInfo(
            code="600519",
            asset_type=AssetType.STOCK,
            category=AssetCategory.EQUITY,
            trading_status=TradingStatus.SUPPORTED,
        )
        assert info.code == "600519"
        assert info.asset_type == AssetType.STOCK
        assert info.category == AssetCategory.EQUITY
        assert info.trading_status == TradingStatus.SUPPORTED

    def test_init_with_optional_fields(self):
        info = AssetInfo(
            code="600519.XSHG",
            asset_type=AssetType.STOCK,
            category=AssetCategory.EQUITY,
            trading_status=TradingStatus.SUPPORTED,
            exchange="XSHG",
            normalized_code="600519",
            display_name="贵州茅台",
        )
        assert info.exchange == "XSHG"
        assert info.normalized_code == "600519"
        assert info.display_name == "贵州茅台"

    def test_is_supported(self):
        info = AssetInfo(
            code="600519",
            asset_type=AssetType.STOCK,
            category=AssetCategory.EQUITY,
            trading_status=TradingStatus.SUPPORTED,
        )
        assert info.is_supported() is True

    def test_is_not_supported(self):
        info = AssetInfo(
            code="000300",
            asset_type=AssetType.INDEX,
            category=AssetCategory.INDEX,
            trading_status=TradingStatus.IDENTIFIED_ONLY,
        )
        assert info.is_supported() is False

    def test_is_identified_only(self):
        info = AssetInfo(
            code="000300",
            asset_type=AssetType.INDEX,
            category=AssetCategory.INDEX,
            trading_status=TradingStatus.IDENTIFIED_ONLY,
        )
        assert info.is_identified_only() is True

    def test_is_not_identified_only(self):
        info = AssetInfo(
            code="600519",
            asset_type=AssetType.STOCK,
            category=AssetCategory.EQUITY,
            trading_status=TradingStatus.SUPPORTED,
        )
        assert info.is_identified_only() is False

    def test_metadata_set_and_get(self):
        info = AssetInfo(
            code="600519",
            asset_type=AssetType.STOCK,
            category=AssetCategory.EQUITY,
            trading_status=TradingStatus.SUPPORTED,
        )
        info.set_metadata("sector", "消费")
        info.set_metadata("market_cap", 1000000000)
        assert info.get_metadata("sector") == "消费"
        assert info.get_metadata("market_cap") == 1000000000

    def test_metadata_default(self):
        info = AssetInfo(
            code="600519",
            asset_type=AssetType.STOCK,
            category=AssetCategory.EQUITY,
            trading_status=TradingStatus.SUPPORTED,
        )
        assert info.get_metadata("nonexistent", "default") == "default"

    def test_repr(self):
        info = AssetInfo(
            code="600519",
            asset_type=AssetType.STOCK,
            category=AssetCategory.EQUITY,
            trading_status=TradingStatus.SUPPORTED,
        )
        repr_str = repr(info)
        assert "600519" in repr_str
        assert "stock" in repr_str
        assert "supported" in repr_str


class TestAssetRouterIdentify:
    """测试 AssetRouter 资产识别"""

    @pytest.fixture
    def router(self):
        return AssetRouter()

    def test_identify_stock_sh(self, router):
        info = router.identify("600519.XSHG")
        assert info.asset_type == AssetType.STOCK
        assert info.category == AssetCategory.EQUITY
        assert info.exchange == "XSHG"

    def test_identify_stock_sz(self, router):
        info = router.identify("000001.XSHE")
        assert info.asset_type == AssetType.STOCK
        assert info.category == AssetCategory.EQUITY
        assert info.exchange == "XSHE"

    def test_identify_stock_with_sh_prefix(self, router):
        info = router.identify("sh600519")
        assert info.asset_type == AssetType.STOCK
        assert info.exchange == "XSHG"

    def test_identify_stock_with_sz_prefix(self, router):
        info = router.identify("sz000001")
        assert info.asset_type == AssetType.STOCK
        assert info.exchange == "XSHE"

    def test_identify_etf_51(self, router):
        info = router.identify("510300.XSHG")
        assert info.asset_type == AssetType.ETF
        assert info.category == AssetCategory.FUND

    def test_identify_etf_159(self, router):
        info = router.identify("159919.XSHE")
        assert info.asset_type == AssetType.ETF
        assert info.category == AssetCategory.FUND

    def test_identify_lof(self, router):
        info = router.identify("160001.XSHE")
        assert info.asset_type == AssetType.LOF
        assert info.category == AssetCategory.FUND

    def test_identify_index_xshg(self, router):
        info = router.identify("000300.XSHG")
        assert info.asset_type == AssetType.INDEX
        assert info.category == AssetCategory.INDEX

    def test_identify_index_xshe(self, router):
        info = router.identify("399001.XSHE")
        assert info.asset_type == AssetType.INDEX
        assert info.category == AssetCategory.INDEX

    def test_identify_fund_of(self, router):
        info = router.identify("159001.OF")
        assert info.asset_type == AssetType.FUND_OF
        assert info.category == AssetCategory.FUND
        assert info.exchange == "OF"

    def test_identify_future_ccfx(self, router):
        info = router.identify("IF2301.CCFX")
        assert info.asset_type == AssetType.FUTURE_CCFX
        assert info.category == AssetCategory.FUTURE
        assert info.exchange == "CCFX"

    def test_identify_unknown(self, router):
        info = router.identify("INVALID")
        assert info.asset_type == AssetType.UNKNOWN
        assert info.category == AssetCategory.UNKNOWN

    def test_identify_caches_result(self, router):
        info1 = router.identify("600519.XSHG")
        info2 = router.identify("600519.XSHG")
        assert info1 is info2

    def test_clear_cache(self, router):
        router.identify("600519.XSHG")
        assert len(router._code_cache) > 0
        router.clear_cache()
        assert len(router._code_cache) == 0


class TestAssetRouterTradingStatus:
    """测试交易状态"""

    @pytest.fixture
    def router(self):
        return AssetRouter()

    def test_stock_is_tradable(self, router):
        assert router.is_tradable("600519.XSHG") is True

    def test_etf_is_tradable(self, router):
        assert router.is_tradable("510300.XSHG") is True

    def test_index_not_tradable(self, router):
        assert router.is_tradable("000300.XSHG") is False

    def test_lof_network_unstable(self, router):
        info = router.identify("160001.XSHE")
        assert info.trading_status == TradingStatus.NETWORK_UNSTABLE

    def test_fund_of_identified_only(self, router):
        info = router.identify("159001.OF")
        assert info.trading_status == TradingStatus.IDENTIFIED_ONLY


class TestAssetRouterBatchOperations:
    """测试批量操作"""

    @pytest.fixture
    def router(self):
        return AssetRouter()

    def test_get_supported_assets(self, router):
        codes = ["600519.XSHG", "000300.XSHG", "510300.XSHG", "INVALID"]
        supported = router.get_supported_assets(codes)
        assert "600519.XSHG" in supported
        assert "510300.XSHG" in supported
        assert "000300.XSHG" not in supported
        assert "INVALID" not in supported

    def test_group_by_type(self, router):
        codes = ["600519.XSHG", "000001.XSHE", "510300.XSHG", "000300.XSHG"]
        groups = router.group_by_type(codes)
        assert AssetType.STOCK in groups
        assert AssetType.ETF in groups
        assert AssetType.INDEX in groups
        assert len(groups[AssetType.STOCK]) == 2
        assert len(groups[AssetType.ETF]) == 1

    def test_group_by_type_empty(self, router):
        groups = router.group_by_type([])
        assert groups == {}


class TestAssetRouterCustomRules:
    """测试自定义规则"""

    @pytest.fixture
    def router(self):
        return AssetRouter()

    def test_add_custom_rule(self, router):
        router.add_custom_rule(r"^88[0-9]{4}$", AssetType.STOCK)
        assert len(router._custom_rules) == 1
        assert router._custom_rules[0]["pattern"] == r"^88[0-9]{4}$"
        assert router._custom_rules[0]["asset_type"] == AssetType.STOCK

    def test_add_custom_rule_with_status(self, router):
        router.add_custom_rule(
            r"^88[0-9]{4}$", AssetType.STOCK, TradingStatus.DATA_AVAILABLE
        )
        assert router._custom_rules[0]["trading_status"] == TradingStatus.DATA_AVAILABLE


class TestAssetRouterExchange:
    """测试交易所推断"""

    @pytest.fixture
    def router(self):
        return AssetRouter()

    def test_exchange_xshg_by_code_starting_with_6(self, router):
        info = router.identify("600000")
        assert info.exchange == "XSHG"

    def test_exchange_xshe_by_code_starting_with_0(self, router):
        info = router.identify("000001")
        assert info.exchange == "XSHE"

    def test_exchange_xshg_by_sh_prefix(self, router):
        info = router.identify("sh600000")
        assert info.exchange == "XSHG"

    def test_exchange_xshe_by_sz_prefix(self, router):
        info = router.identify("sz000001")
        assert info.exchange == "XSHE"


class TestConvenienceFunctions:
    """测试便捷函数"""

    def setup_method(self):
        _asset_router_mod._router_instance = None

    def teardown_method(self):
        _asset_router_mod._router_instance = None

    def test_get_asset_router_singleton(self):
        r1 = get_asset_router()
        r2 = get_asset_router()
        assert r1 is r2

    def test_identify_asset(self):
        info = identify_asset("600519.XSHG")
        assert info.asset_type == AssetType.STOCK

    def test_is_etf_true(self):
        assert is_etf("510300.XSHG") is True

    def test_is_etf_lof_also_true(self):
        assert is_etf("160001.XSHE") is True

    def test_is_etf_false_for_stock(self):
        assert is_etf("600519.XSHG") is False

    def test_is_stock_true(self):
        assert is_stock("600519.XSHG") is True

    def test_is_stock_false_for_etf(self):
        assert is_stock("510300.XSHG") is False

    def test_is_fund_of_true(self):
        assert is_fund_of("159001.OF") is True

    def test_is_fund_of_false_for_stock(self):
        assert is_fund_of("600519.XSHG") is False

    def test_is_future_true(self):
        assert is_future("IF2301.CCFX") is True

    def test_is_future_false_for_stock(self):
        assert is_future("600519.XSHG") is False

    def test_is_index_true(self):
        assert is_index("000300.XSHG") is True

    def test_is_index_false_for_stock(self):
        assert is_index("600519.XSHG") is False

    def test_get_trading_status_desc_supported(self):
        desc = get_trading_status_desc("600519.XSHG")
        assert desc == "支持交易"

    def test_get_trading_status_desc_identified_only(self):
        desc = get_trading_status_desc("000300.XSHG")
        assert desc == "已识别(暂不支持)"

    def test_is_data_readable_supported(self):
        assert is_data_readable("600519.XSHG") is True

    def test_is_data_readable_network_unstable(self):
        assert is_data_readable("160001.XSHE") is True
