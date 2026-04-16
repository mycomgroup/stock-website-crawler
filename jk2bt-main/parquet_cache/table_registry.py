from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class CacheTable:
    name: str
    partition_by: str | None
    ttl_hours: int
    schema: dict[str, str]
    primary_key: list[str]
    aggregation_enabled: bool = True
    compaction_threshold: int = 20
    priority: str = "P0"
    storage_layer: str = "daily"


@dataclass
class TableInfo:
    name: str
    file_count: int
    total_size_bytes: int
    last_updated: datetime | None
    partition_count: int
    priority: str


class TableRegistry:
    def __init__(self) -> None:
        self._tables: dict[str, CacheTable] = {}

    def register(self, table: CacheTable) -> None:
        self._tables[table.name] = table

    def get(self, name: str) -> CacheTable:
        return self._tables[name]

    def get_or_none(self, name: str) -> CacheTable | None:
        return self._tables.get(name)

    def list_all(self) -> dict[str, CacheTable]:
        return dict(self._tables)

    def list_by_priority(self, priority: str) -> list[CacheTable]:
        return [t for t in self._tables.values() if t.priority == priority]

    def list_by_layer(self, layer: str) -> list[CacheTable]:
        return [t for t in self._tables.values() if t.storage_layer == layer]

    def has(self, name: str) -> bool:
        return name in self._tables


STOCK_DAILY = CacheTable(
    name="stock_daily",
    partition_by="date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "date": "date",
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "float64",
        "amount": "float64",
        "adjust": "string",
    },
    primary_key=["symbol", "date", "adjust"],
    storage_layer="daily",
)

ETF_DAILY = CacheTable(
    name="etf_daily",
    partition_by="date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "date": "date",
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "float64",
        "amount": "float64",
    },
    primary_key=["symbol", "date"],
    storage_layer="daily",
)

INDEX_DAILY = CacheTable(
    name="index_daily",
    partition_by="date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "date": "date",
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "float64",
        "amount": "float64",
    },
    primary_key=["symbol", "date"],
    storage_layer="daily",
)

FUTURES_DAILY = CacheTable(
    name="futures_daily",
    partition_by="date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "date": "date",
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "float64",
        "open_interest": "float64",
    },
    primary_key=["symbol", "date"],
    storage_layer="daily",
)

CONVERSION_BOND_DAILY = CacheTable(
    name="conversion_bond_daily",
    partition_by="date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "date": "date",
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "float64",
        "amount": "float64",
    },
    primary_key=["symbol", "date"],
    storage_layer="daily",
)

INDEX_COMPONENTS = CacheTable(
    name="index_components",
    partition_by="date",
    ttl_hours=720,
    schema={
        "index_code": "string",
        "date": "date",
        "symbol": "string",
        "weight": "float64",
    },
    primary_key=["index_code", "date", "symbol"],
    storage_layer="daily",
)

FINANCE_INDICATOR = CacheTable(
    name="finance_indicator",
    partition_by="report_date",
    ttl_hours=2160,
    schema={
        "symbol": "string",
        "report_date": "date",
        "pe": "float64",
        "pb": "float64",
        "ps": "float64",
        "roe": "float64",
        "net_profit": "float64",
        "revenue": "float64",
    },
    primary_key=["symbol", "report_date"],
    compaction_threshold=5,
    storage_layer="daily",
)

MONEY_FLOW = CacheTable(
    name="money_flow",
    partition_by="date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "date": "date",
        "main_net_inflow": "float64",
        "super_large_net_inflow": "float64",
        "large_net_inflow": "float64",
        "medium_net_inflow": "float64",
        "small_net_inflow": "float64",
    },
    primary_key=["symbol", "date"],
    priority="P1",
    storage_layer="daily",
)

NORTH_FLOW = CacheTable(
    name="north_flow",
    partition_by="date",
    ttl_hours=0,
    schema={
        "date": "date",
        "net_flow": "float64",
        "buy_amount": "float64",
        "sell_amount": "float64",
    },
    primary_key=["date"],
    priority="P1",
    storage_layer="daily",
)

INDUSTRY_COMPONENTS = CacheTable(
    name="industry_components",
    partition_by="date",
    ttl_hours=720,
    schema={
        "industry_code": "string",
        "date": "date",
        "symbol": "string",
        "industry_name": "string",
    },
    primary_key=["industry_code", "date", "symbol"],
    priority="P1",
    storage_layer="daily",
)

HOLDER = CacheTable(
    name="holder",
    partition_by="report_date",
    ttl_hours=2160,
    schema={
        "symbol": "string",
        "report_date": "date",
        "holder_name": "string",
        "hold_count": "float64",
        "hold_ratio": "float64",
        "holder_type": "string",
    },
    primary_key=["symbol", "report_date", "holder_name"],
    compaction_threshold=5,
    priority="P1",
    storage_layer="daily",
)

DIVIDEND = CacheTable(
    name="dividend",
    partition_by="announce_date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "announce_date": "date",
        "dividend_cash": "float64",
        "dividend_stock": "float64",
        "record_date": "date",
        "ex_date": "date",
    },
    primary_key=["symbol", "announce_date"],
    compaction_threshold=5,
    priority="P1",
    storage_layer="daily",
)

VALUATION = CacheTable(
    name="valuation",
    partition_by="date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "date": "date",
        "pe": "float64",
        "pb": "float64",
        "ps": "float64",
        "market_cap": "float64",
        "circulating_cap": "float64",
    },
    primary_key=["symbol", "date"],
    priority="P1",
    storage_layer="daily",
)

UNLOCK = CacheTable(
    name="unlock",
    partition_by="announce_date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "announce_date": "date",
        "unlock_date": "date",
        "unlock_count": "float64",
        "unlock_ratio": "float64",
        "unlock_type": "string",
    },
    primary_key=["symbol", "announce_date"],
    compaction_threshold=5,
    priority="P1",
    storage_layer="daily",
)

SPOT_SNAPSHOT = CacheTable(
    name="spot_snapshot",
    partition_by="date",
    ttl_hours=168,
    schema={
        "symbol": "string",
        "date": "date",
        "price": "float64",
        "change_pct": "float64",
        "volume": "float64",
        "amount": "float64",
        "turnover_rate": "float64",
        "pe": "float64",
        "pb": "float64",
        "market_cap": "float64",
    },
    primary_key=["symbol", "date"],
    compaction_threshold=1,
    storage_layer="snapshot",
    priority="P0",
)

SECTOR_FLOW_SNAPSHOT = CacheTable(
    name="sector_flow_snapshot",
    partition_by="date",
    ttl_hours=168,
    schema={
        "date": "date",
        "sector_name": "string",
        "sector_type": "string",
        "change_pct": "float64",
        "net_inflow": "float64",
        "stock_count": "int64",
    },
    primary_key=["date", "sector_name", "sector_type"],
    compaction_threshold=1,
    storage_layer="snapshot",
    priority="P0",
)

HSGT_HOLD_SNAPSHOT = CacheTable(
    name="hsgt_hold_snapshot",
    partition_by="date",
    ttl_hours=168,
    schema={
        "symbol": "string",
        "date": "date",
        "hold_count": "float64",
        "hold_ratio": "float64",
        "change_count": "float64",
    },
    primary_key=["symbol", "date"],
    compaction_threshold=1,
    storage_layer="snapshot",
    priority="P0",
)

STOCK_MINUTE = CacheTable(
    name="stock_minute",
    partition_by="week",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "datetime": "timestamp",
        "period": "string",
        "adjust": "string",
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "float64",
        "amount": "float64",
    },
    primary_key=["symbol", "datetime", "period", "adjust"],
    compaction_threshold=50,
    storage_layer="minute",
    priority="P2",
)

ETF_MINUTE = CacheTable(
    name="etf_minute",
    partition_by="week",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "datetime": "timestamp",
        "period": "string",
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "float64",
        "amount": "float64",
    },
    primary_key=["symbol", "datetime", "period"],
    compaction_threshold=50,
    storage_layer="minute",
    priority="P2",
)

SECURITIES = CacheTable(
    name="securities",
    partition_by=None,
    ttl_hours=0,
    schema={
        "symbol": "string",
        "name": "string",
        "type": "string",
        "list_date": "date",
        "delist_date": "date",
        "exchange": "string",
    },
    primary_key=["symbol"],
    aggregation_enabled=False,
    compaction_threshold=0,
    storage_layer="meta",
    priority="P2",
)

TRADE_CALENDAR = CacheTable(
    name="trade_calendar",
    partition_by=None,
    ttl_hours=0,
    schema={
        "date": "date",
        "is_trading_day": "bool",
    },
    primary_key=["date"],
    aggregation_enabled=False,
    compaction_threshold=0,
    storage_layer="meta",
    priority="P2",
)

INDUSTRY_LIST = CacheTable(
    name="industry_list",
    partition_by=None,
    ttl_hours=720,
    schema={
        "industry_code": "string",
        "industry_name": "string",
        "source": "string",
    },
    primary_key=["industry_code"],
    aggregation_enabled=False,
    compaction_threshold=0,
    storage_layer="meta",
    priority="P2",
)

CONCEPT_LIST = CacheTable(
    name="concept_list",
    partition_by=None,
    ttl_hours=720,
    schema={
        "concept_code": "string",
        "concept_name": "string",
        "source": "string",
    },
    primary_key=["concept_code"],
    aggregation_enabled=False,
    compaction_threshold=0,
    storage_layer="meta",
    priority="P2",
)

COMPANY_INFO = CacheTable(
    name="company_info",
    partition_by=None,
    ttl_hours=720,
    schema={
        "symbol": "string",
        "name": "string",
        "industry": "string",
        "area": "string",
        "list_date": "date",
        "market": "string",
    },
    primary_key=["symbol"],
    aggregation_enabled=False,
    compaction_threshold=0,
    storage_layer="meta",
    priority="P2",
)

FACTOR_CACHE = CacheTable(
    name="factor_cache",
    partition_by="factor_name",
    ttl_hours=0,
    schema={
        "factor_name": "string",
        "symbol": "string",
        "date": "date",
        "value": "float64",
    },
    primary_key=["factor_name", "symbol", "date"],
    compaction_threshold=10,
    storage_layer="daily",
    priority="P1",
)

# 财务报表（P0）
FINANCIAL_REPORT = CacheTable(
    name="financial_report",
    partition_by="report_date",
    ttl_hours=2160,  # 90天
    schema={
        "symbol": "string",
        "report_date": "date",
        "report_type": "string",  # 现金流量表/资产负债表/利润表
        "item_name": "string",
        "item_value": "float64",
    },
    primary_key=["symbol", "report_date", "report_type", "item_name"],
    compaction_threshold=5,
    storage_layer="daily",
    priority="P0",
)

# 财务效益（P0）
FINANCIAL_BENEFIT = CacheTable(
    name="financial_benefit",
    partition_by="report_date",
    ttl_hours=2160,
    schema={
        "symbol": "string",
        "report_date": "date",
        "indicator": "string",
        "value": "float64",
    },
    primary_key=["symbol", "report_date", "indicator"],
    compaction_threshold=5,
    storage_layer="daily",
    priority="P0",
)

# 行业映射（P1）
INDUSTRY_MAPPING = CacheTable(
    name="industry_mapping",
    partition_by=None,
    ttl_hours=720,  # 30天
    schema={
        "symbol": "string",
        "industry_code": "string",
        "industry_name": "string",
        "level": "int64",
    },
    primary_key=["symbol"],
    aggregation_enabled=False,
    compaction_threshold=0,
    storage_layer="meta",
    priority="P1",
)

# 概念成分（P1）
CONCEPT_COMPONENTS = CacheTable(
    name="concept_components",
    partition_by="date",
    ttl_hours=720,
    schema={
        "concept_code": "string",
        "concept_name": "string",
        "date": "date",
        "symbol": "string",
    },
    primary_key=["concept_code", "date", "symbol"],
    storage_layer="daily",
    priority="P1",
)

# 基金持仓（P1）
FUND_PORTFOLIO = CacheTable(
    name="fund_portfolio",
    partition_by="report_date",
    ttl_hours=2160,
    schema={
        "fund_code": "string",
        "report_date": "date",
        "symbol": "string",
        "hold_count": "float64",
        "hold_ratio": "float64",
        "market_value": "float64",
    },
    primary_key=["fund_code", "report_date", "symbol"],
    compaction_threshold=5,
    storage_layer="daily",
    priority="P1",
)

# 股本变动（P2）
SHARE_CHANGE = CacheTable(
    name="share_change",
    partition_by="announce_date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "announce_date": "date",
        "total_shares": "float64",
        "circulating_shares": "float64",
        "change_type": "string",
    },
    primary_key=["symbol", "announce_date"],
    compaction_threshold=5,
    storage_layer="daily",
    priority="P2",
)

# 股东增减持（P2）
HOLDING_CHANGE = CacheTable(
    name="holding_change",
    partition_by="announce_date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "announce_date": "date",
        "holder_name": "string",
        "change_count": "float64",
        "change_ratio": "float64",
        "change_type": "string",  # 增持/减持
    },
    primary_key=["symbol", "announce_date", "holder_name"],
    compaction_threshold=5,
    storage_layer="daily",
    priority="P2",
)

# 宏观数据（P2）
MACRO_DATA = CacheTable(
    name="macro_data",
    partition_by=None,
    ttl_hours=720,
    schema={
        "indicator": "string",  # pmi/cpi/ppi/gdp/m2/interest_rate/exchange_rate
        "date": "date",
        "value": "float64",
        "change_pct": "float64",
    },
    primary_key=["indicator", "date"],
    aggregation_enabled=False,
    compaction_threshold=0,
    storage_layer="meta",
    priority="P2",
)

# 融资融券明细（P2）
MARGIN_DETAIL = CacheTable(
    name="margin_detail",
    partition_by="date",
    ttl_hours=720,
    schema={
        "market": "string",  # sh/sz
        "date": "date",
        "symbol": "string",
        "margin_balance": "float64",
        "short_balance": "float64",
    },
    primary_key=["market", "date", "symbol"],
    storage_layer="daily",
    priority="P2",
)

# 两融标的（P2）
MARGIN_UNDERLYING = CacheTable(
    name="margin_underlying",
    partition_by="date",
    ttl_hours=720,
    schema={
        "market": "string",
        "date": "date",
        "symbol": "string",
        "stock_name": "string",
    },
    primary_key=["market", "date", "symbol"],
    storage_layer="daily",
    priority="P2",
)

# 期权日线（P3）
OPTION_DAILY = CacheTable(
    name="option_daily",
    partition_by="date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "date": "date",
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64",
        "volume": "float64",
        "open_interest": "float64",
    },
    primary_key=["symbol", "date"],
    storage_layer="daily",
    priority="P3",
)

# 集合竞价（P3）
STATUS_CHANGE = CacheTable(
    name="status_change",
    partition_by=None,
    ttl_hours=720,
    schema={
        "symbol": "string",
        "status_date": "date",
        "status_type": "string",
        "reason": "string",
    },
    primary_key=["symbol", "status_date"],
    aggregation_enabled=False,
    compaction_threshold=0,
    storage_layer="meta",
    priority="P2",
)

CALL_AUCTION = CacheTable(
    name="call_auction",
    partition_by="date",
    ttl_hours=0,
    schema={
        "symbol": "string",
        "datetime": "timestamp",
        "price": "float64",
        "volume": "float64",
        "amount": "float64",
    },
    primary_key=["symbol", "datetime"],
    compaction_threshold=50,
    storage_layer="daily",
    priority="P3",
)


DEFAULT_REGISTRY = TableRegistry()

for _table in (
    STOCK_DAILY,
    ETF_DAILY,
    INDEX_DAILY,
    FUTURES_DAILY,
    CONVERSION_BOND_DAILY,
    INDEX_COMPONENTS,
    FINANCE_INDICATOR,
    MONEY_FLOW,
    NORTH_FLOW,
    INDUSTRY_COMPONENTS,
    HOLDER,
    DIVIDEND,
    VALUATION,
    UNLOCK,
    SPOT_SNAPSHOT,
    SECTOR_FLOW_SNAPSHOT,
    HSGT_HOLD_SNAPSHOT,
    STOCK_MINUTE,
    ETF_MINUTE,
    SECURITIES,
    TRADE_CALENDAR,
    INDUSTRY_LIST,
    CONCEPT_LIST,
    COMPANY_INFO,
    FACTOR_CACHE,
    FINANCIAL_REPORT,
    FINANCIAL_BENEFIT,
    INDUSTRY_MAPPING,
    CONCEPT_COMPONENTS,
    FUND_PORTFOLIO,
    SHARE_CHANGE,
    HOLDING_CHANGE,
    MACRO_DATA,
    MARGIN_DETAIL,
    MARGIN_UNDERLYING,
    STATUS_CHANGE,
    OPTION_DAILY,
    CALL_AUCTION,
):
    DEFAULT_REGISTRY.register(_table)

del _table
