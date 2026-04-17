"""
data - 数据层

包含数据源抽象、行情数据、财务数据、数据持久化
"""

# Sources
try:
    from jk2bt.data.sources import get_adapter, set_adapter, DataSource
except ImportError:
    pass

# Market
try:
    from jk2bt.data.market import get_stock_daily
except ImportError:
    pass

try:
    from jk2bt.data.market import get_etf_daily
except ImportError:
    pass

try:
    from jk2bt.data.market import get_index_daily
except ImportError:
    pass

# Finance
try:
    from jk2bt.data.finance import get_company_info
except ImportError:
    pass

try:
    from jk2bt.data.finance import get_shareholders
except ImportError:
    pass

# Storage
try:
    from jk2bt.data.storage import get_cache_manager
except ImportError:
    pass

__all__ = [
    # Sources
    "get_adapter",
    "set_adapter",
    "DataSource",
    # Market
    "get_stock_daily",
    "get_etf_daily",
    "get_index_daily",
    # Finance
    "get_company_info",
    "get_shareholders",
    # Storage
    "get_cache_manager",
]
