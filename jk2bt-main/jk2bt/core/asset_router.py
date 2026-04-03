"""
asset_router.py
资产类别识别路由器

支持识别:
- 股票 (stock)
- ETF/LOF (etf)
- 场外基金 (fund_of) - .OF 后缀
- 股指期货 (future_ccfx) - .CCFX 后缀
"""

from enum import Enum
from typing import Optional, Dict, Any, List
import re


class AssetType(Enum):
    STOCK = "stock"
    ETF = "etf"
    LOF = "lof"
    FUND_OF = "fund_of"
    FUTURE_CCFX = "future_ccfx"
    INDEX = "index"
    UNKNOWN = "unknown"


class AssetCategory(Enum):
    EQUITY = "equity"
    FUND = "fund"
    FUTURE = "future"
    INDEX = "index"
    UNKNOWN = "unknown"


class TradingStatus(Enum):
    SUPPORTED = "supported"
    DATA_AVAILABLE = "data_available"
    NETWORK_UNSTABLE = "network_unstable"
    IDENTIFIED_ONLY = "identified_only"
    NOT_SUPPORTED = "not_supported"


ETF_CODE_PATTERNS = [
    r"^51[0-9]{4}$",
    r"^52[0-9]{4}$",
    r"^15[0-9]{4}$",
    r"^16[0-9]{4}$",
    r"^50[0-9]{4}$",
    r"^56[0-9]{4}$",
    r"^58[0-9]{4}$",
]

LOF_CODE_PATTERNS = [
    r"^16[0-9]{4}$",
    r"^50[0-9]{4}$",
]

INDEX_CODE_PATTERNS = [
    r"^000[0-9]{3}$",
    r"^399[0-9]{3}$",
    r"^000300$",
    r"^000016$",
    r"^000905$",
    r"^000852$",
]


class AssetInfo:
    def __init__(
        self,
        code: str,
        asset_type: AssetType,
        category: AssetCategory,
        trading_status: TradingStatus,
        exchange: Optional[str] = None,
        normalized_code: Optional[str] = None,
        display_name: Optional[str] = None,
    ):
        self.code = code
        self.asset_type = asset_type
        self.category = category
        self.trading_status = trading_status
        self.exchange = exchange
        self.normalized_code = normalized_code or code
        self.display_name = display_name
        self._metadata: Dict[str, Any] = {}

    def is_supported(self) -> bool:
        return self.trading_status == TradingStatus.SUPPORTED

    def is_identified_only(self) -> bool:
        return self.trading_status == TradingStatus.IDENTIFIED_ONLY

    def set_metadata(self, key: str, value: Any) -> None:
        self._metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        return self._metadata.get(key, default)

    def __repr__(self) -> str:
        return (
            f"AssetInfo(code={self.code}, type={self.asset_type.value}, "
            f"status={self.trading_status.value})"
        )


class AssetRouter:
    SUPPORTED_TYPES = {
        AssetType.STOCK: TradingStatus.SUPPORTED,
        AssetType.ETF: TradingStatus.SUPPORTED,
        AssetType.LOF: TradingStatus.NETWORK_UNSTABLE,
        AssetType.INDEX: TradingStatus.IDENTIFIED_ONLY,
        AssetType.FUND_OF: TradingStatus.IDENTIFIED_ONLY,
        AssetType.FUTURE_CCFX: TradingStatus.IDENTIFIED_ONLY,
    }

    TYPE_TO_CATEGORY = {
        AssetType.STOCK: AssetCategory.EQUITY,
        AssetType.ETF: AssetCategory.FUND,
        AssetType.LOF: AssetCategory.FUND,
        AssetType.FUND_OF: AssetCategory.FUND,
        AssetType.FUTURE_CCFX: AssetCategory.FUTURE,
        AssetType.INDEX: AssetCategory.INDEX,
        AssetType.UNKNOWN: AssetCategory.UNKNOWN,
    }

    def __init__(self):
        self._custom_rules: List[Dict[str, Any]] = []
        self._code_cache: Dict[str, AssetInfo] = {}

    def identify(self, code: str) -> AssetInfo:
        if code in self._code_cache:
            return self._code_cache[code]

        normalized = self._normalize_code(code)
        asset_type = self._identify_type(code, normalized)
        category = self.TYPE_TO_CATEGORY.get(asset_type, AssetCategory.UNKNOWN)
        trading_status = self.SUPPORTED_TYPES.get(
            asset_type, TradingStatus.NOT_SUPPORTED
        )
        exchange = self._get_exchange(code, normalized)

        info = AssetInfo(
            code=code,
            asset_type=asset_type,
            category=category,
            trading_status=trading_status,
            exchange=exchange,
            normalized_code=normalized,
        )

        self._code_cache[code] = info
        return info

    def _normalize_code(self, code: str) -> str:
        code = code.strip()
        if code.startswith("sh") or code.startswith("sz"):
            return code[2:].zfill(6)
        if ".XSHG" in code:
            return code.split(".")[0].zfill(6)
        if ".XSHE" in code:
            return code.split(".")[0].zfill(6)
        if ".OF" in code:
            return code.split(".")[0].zfill(6)
        if ".CCFX" in code:
            return code.split(".")[0]
        return code.zfill(6)

    def _identify_type(self, original_code: str, normalized_code: str) -> AssetType:
        if ".OF" in original_code.upper():
            return AssetType.FUND_OF

        if ".CCFX" in original_code.upper():
            return AssetType.FUTURE_CCFX

        if ".XSHG" in original_code or ".XSHE" in original_code:
            pure_code = normalized_code
            return self._identify_by_code_pattern(pure_code, original_code)

        if original_code.startswith("sh") or original_code.startswith("sz"):
            pure_code = normalized_code
            return self._identify_by_code_pattern(pure_code, original_code)

        return self._identify_by_code_pattern(normalized_code, original_code)

    def _identify_by_code_pattern(
        self, code: str, original_code: str = ""
    ) -> AssetType:
        if code.startswith("16"):
            return AssetType.LOF

        for pattern in ETF_CODE_PATTERNS:
            if re.match(pattern, code):
                return AssetType.ETF

        known_index_codes_xshg = {
            "000001",
            "000300",
            "000016",
            "000905",
            "000852",
            "000903",
            "000922",
            "000925",
        }
        known_index_codes_xshe = {
            "399001",
            "399006",
            "399102",
            "399300",
        }
        if code in known_index_codes_xshg and ".XSHG" in original_code:
            return AssetType.INDEX
        if code in known_index_codes_xshe and ".XSHE" in original_code:
            return AssetType.INDEX

        has_exchange_suffix = ".XSHG" in original_code or ".XSHE" in original_code
        has_prefix = original_code.startswith("sh") or original_code.startswith("sz")

        if has_exchange_suffix or has_prefix:
            if re.match(r"^6[0-9]{5}$", code):
                return AssetType.STOCK
            if re.match(r"^[03][0-9]{5}$", code):
                return AssetType.STOCK
            if re.match(r"^00[0-9]{4}$", code):
                return AssetType.STOCK

        for pattern in INDEX_CODE_PATTERNS:
            if re.match(pattern, code):
                return AssetType.INDEX

        if re.match(r"^6[0-9]{5}$", code):
            return AssetType.STOCK

        if re.match(r"^[03][0-9]{5}$", code):
            return AssetType.STOCK

        if re.match(r"^00[0-9]{4}$", code):
            return AssetType.STOCK

        return AssetType.UNKNOWN

    def _get_exchange(self, original_code: str, normalized_code: str) -> Optional[str]:
        if ".XSHG" in original_code:
            return "XSHG"
        if ".XSHE" in original_code:
            return "XSHE"
        if ".OF" in original_code.upper():
            return "OF"
        if ".CCFX" in original_code.upper():
            return "CCFX"
        if original_code.startswith("sh"):
            return "XSHG"
        if original_code.startswith("sz"):
            return "XSHE"
        if (
            normalized_code.startswith("6")
            or normalized_code.startswith("51")
            or normalized_code.startswith("52")
        ):
            return "XSHG"
        if (
            normalized_code.startswith("0")
            or normalized_code.startswith("3")
            or normalized_code.startswith("15")
        ):
            return "XSHE"
        return None

    def add_custom_rule(
        self, pattern: str, asset_type: AssetType, trading_status: TradingStatus = None
    ) -> None:
        rule = {
            "pattern": pattern,
            "asset_type": asset_type,
            "trading_status": trading_status
            or self.SUPPORTED_TYPES.get(asset_type, TradingStatus.NOT_SUPPORTED),
        }
        self._custom_rules.append(rule)

    def is_tradable(self, code: str) -> bool:
        info = self.identify(code)
        return info.is_supported()

    def get_supported_assets(self, codes: List[str]) -> List[str]:
        return [c for c in codes if self.is_tradable(c)]

    def group_by_type(self, codes: List[str]) -> Dict[AssetType, List[str]]:
        groups: Dict[AssetType, List[str]] = {}
        for code in codes:
            info = self.identify(code)
            if info.asset_type not in groups:
                groups[info.asset_type] = []
            groups[info.asset_type].append(code)
        return groups

    def clear_cache(self) -> None:
        self._code_cache.clear()


_router_instance: Optional[AssetRouter] = None


def get_asset_router() -> AssetRouter:
    global _router_instance
    if _router_instance is None:
        _router_instance = AssetRouter()
    return _router_instance


def identify_asset(code: str) -> AssetInfo:
    return get_asset_router().identify(code)


def is_etf(code: str) -> bool:
    info = identify_asset(code)
    return info.asset_type in (AssetType.ETF, AssetType.LOF)


def is_stock(code: str) -> bool:
    info = identify_asset(code)
    return info.asset_type == AssetType.STOCK


def is_fund_of(code: str) -> bool:
    info = identify_asset(code)
    return info.asset_type == AssetType.FUND_OF


def is_future(code: str) -> bool:
    info = identify_asset(code)
    return info.asset_type == AssetType.FUTURE_CCFX


def is_index(code: str) -> bool:
    info = identify_asset(code)
    return info.asset_type == AssetType.INDEX


def get_trading_status_desc(code: str) -> str:
    info = identify_asset(code)
    if info.is_supported():
        return "支持交易"
    if info.trading_status == TradingStatus.DATA_AVAILABLE:
        return "数据可读(非交易行情)"
    if info.trading_status == TradingStatus.NETWORK_UNSTABLE:
        return "接口不稳定(可能失败)"
    if info.is_identified_only():
        return "已识别(暂不支持)"
    return "不支持"


def is_data_readable(code: str) -> bool:
    info = identify_asset(code)
    return info.trading_status in (
        TradingStatus.SUPPORTED,
        TradingStatus.DATA_AVAILABLE,
        TradingStatus.NETWORK_UNSTABLE,
    )
