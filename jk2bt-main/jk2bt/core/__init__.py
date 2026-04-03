"""
core 模块
聚宽策略本地运行核心组件。

模块结构：
- strategy_base.py : 策略基类定义（主入口）
- securities_utils.py : 证券代码工具函数、指数常量
- data_proxies.py : 数据代理类
- timer_manager.py : 定时器管理器
- global_state.py : 全局状态类
- api_wrappers.py : API 封装函数
- runner.py : 策略运行器（主入口函数）
- strategy_wrapper.py : JQStrategyWrapper 策略包装器类
- executor.py : 数据加载、股票池发现
- io.py : 运行时IO
- validator.py : 参数验证
- asset_router.py : 资产路由
- exceptions.py : 自定义异常类

异常类使用示例:
    from jk2bt.core.exceptions import (
        JK2BTError,
        DataSourceError,
        NetworkError,
        ValuationDataError,
        IndexNotSupportedError,
        CacheError,
        ValidationError,
        MarketDataError,
    )

    # 捕获特定异常
    try:
        df = get_valuation_data(symbol)
    except NetworkError as e:
        logger.error(f"网络错误: {e}")
    except ValuationDataError as e:
        logger.warning(f"估值数据不可用: {e}")
"""

# 导出异常类供外部使用
from jk2bt.core.exceptions import (
    JK2BTError,
    DataSourceError,
    NetworkError,
    CacheError,
    ValidationError,
    StrategyError,
    APICompatibilityError,
    IndexNotSupportedError,
    ValuationDataError,
    FinancialDataError,
    MarketDataError,
    DatabaseError,
    ConfigurationError,
    wrap_exception,
    log_and_raise,
    safe_call,
)

# 从 strategy_base 重新导出所有公共接口
from .strategy_base import *

# 显式导出子模块中的关键组件
from .securities_utils import (
    format_stock_symbol_for_akshare,
    jq_code_to_ak,
    ak_code_to_jq,
    RobustResult,
    SUPPORTED_INDEXES,
)

from .data_proxies import (
    SecurityInfo,
    valuation,
    income,
    cash_flow,
    balance,
    indicator,
    _QueryBuilder,
    _TableProxy,
    _FieldProxy,
)

from .timer_manager import TimerManager

from .global_state import (
    log,
    JQLogAdapter,
    GlobalState,
    FundOFPosition,
    ContextProxy,
    set_current_strategy,
)

from .api_wrappers import (
    get_price,
    get_price_jq,
    get_price_unified,
    get_index_weights,
    get_index_stocks,
    get_fundamentals,
    get_history_fundamentals,
    get_all_securities,
    get_security_info,
    get_all_trade_days,
    get_current_data,
    get_current_tick,
    query,
    analyze_performance,
)

# 导入运行器和相关模块
from .runner import (
    run_jq_strategy,
    load_jq_strategy,
)

from .strategy_wrapper import (
    JQStrategyWrapper,
    _set_current_strategy_instance,
    _get_current_strategy,
)

from .executor import (
    _load_stock_data_from_cache,
    _load_minute_data,
    _discover_strategy_stocks,
    _static_analyze_stock_pool,
)

__all__ = [
    # 异常类
    'JK2BTError',
    'DataSourceError',
    'NetworkError',
    'CacheError',
    'ValidationError',
    'StrategyError',
    'APICompatibilityError',
    'IndexNotSupportedError',
    'ValuationDataError',
    'FinancialDataError',
    'MarketDataError',
    'DatabaseError',
    'ConfigurationError',
    # 辅助函数
    'wrap_exception',
    'log_and_raise',
    'safe_call',
    # 工具函数
    'format_stock_symbol_for_akshare',
    'jq_code_to_ak',
    'ak_code_to_jq',
    # 常量
    'SUPPORTED_INDEXES',
    # 类
    'RobustResult',
    'SecurityInfo',
    'valuation',
    'income',
    'cash_flow',
    'balance',
    'indicator',
    '_QueryBuilder',
    '_TableProxy',
    '_FieldProxy',
    'TimerManager',
    'JQLogAdapter',
    'log',
    'GlobalState',
    'FundOFPosition',
    'ContextProxy',
    'set_current_strategy',
    # API 函数
    'get_price',
    'get_price_jq',
    'get_price_unified',
    'get_index_weights',
    'get_index_stocks',
    'get_fundamentals',
    'get_history_fundamentals',
    'get_all_securities',
    'get_security_info',
    'get_all_trade_days',
    'get_current_data',
    'get_current_tick',
    'query',
    'analyze_performance',
    # 运行器
    'run_jq_strategy',
    'load_jq_strategy',
    # 策略包装器
    'JQStrategyWrapper',
    '_set_current_strategy_instance',
    '_get_current_strategy',
    # 执行器
    '_load_stock_data_from_cache',
    '_load_minute_data',
    '_discover_strategy_stocks',
    '_static_analyze_stock_pool',
]