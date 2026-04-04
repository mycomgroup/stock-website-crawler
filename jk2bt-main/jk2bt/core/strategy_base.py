"""
strategy_base.py
聚宽 (JQData) 策略 → AkShare + Backtrader 本地运行兼容层。

设计原则
--------
1. 聚宽平台上的策略代码（initialize/handle_data/context/run_daily 风格）
   粘贴过来不用改，直接可以在本地跑。
2. 数据层全部由 AkShare 提供，支持本地 pickle 缓存。
3. 兼容 pandas 3.0（fillna 不再支持 method= 参数）。
4. headless 环境下图表自动保存为文件，不调用 plt.show() 阻塞。
5. 中文字体自动 fallback（优先 Noto Sans CJK JP / SimHei / DejaVu Sans）。

模块拆分
--------
本文件作为主入口，从子模块重新导出所有功能:
- securities_utils.py: 证券代码工具函数、指数常量
- data_proxies.py: 数据代理类
- timer_manager.py: 定时器管理器
- global_state.py: 全局状态类
- api_wrappers.py: API 封装函数
"""

# =====================================================================
# 0. 环境 patch（必须在任何 import 之前完成）
# =====================================================================
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Matplotlib 延迟初始化，避免首次导入时构建字体缓存
_matplotlib_initialized = False
_plt = None  # 延迟导入 matplotlib.pyplot

def _ensure_matplotlib_init():
    """延迟初始化 matplotlib，只在首次使用时配置"""
    global _matplotlib_initialized
    if _matplotlib_initialized:
        return

    import matplotlib
    import os as _os

    # headless 环境使用非交互后端
    if not _os.environ.get("DISPLAY"):
        matplotlib.use("Agg")

    # 中文字体 fallback（使用更安全的设置）
    try:
        matplotlib.rcParams["font.family"] = [
            "Noto Sans CJK JP",
            "SimHei",
            "Microsoft YaHei",
            "DejaVu Sans",
        ]
        matplotlib.rcParams["axes.unicode_minus"] = False
    except Exception:
        # 字体设置失败时忽略，避免阻塞导入
        pass

    _matplotlib_initialized = True

# patch pandas fillna（保持原有代码）

# patch pandas fillna
import pandas as _pd

_orig_series_fillna = _pd.Series.fillna


def _series_fillna_compat(self, value=None, method=None, **kwargs):
    if method == "ffill":
        return self.ffill()
    if method == "bfill":
        return self.bfill()
    if value is not None:
        return _orig_series_fillna(self, value=value, **kwargs)
    return _orig_series_fillna(self, **kwargs)


_pd.Series.fillna = _series_fillna_compat

_orig_df_fillna = _pd.DataFrame.fillna


def _df_fillna_compat(self, value=None, method=None, **kwargs):
    if method == "ffill":
        return self.ffill()
    if method == "bfill":
        return self.bfill()
    if value is not None:
        return _orig_df_fillna(self, value=value, **kwargs)
    return _orig_df_fillna(self, **kwargs)


_pd.DataFrame.fillna = _df_fillna_compat

# 延迟导入 matplotlib.pyplot，在需要时才初始化
def _get_plt():
    """获取 matplotlib.pyplot（延迟导入）"""
    _ensure_matplotlib_init()
    import matplotlib.pyplot as plt_module
    return plt_module

# =====================================================================
# 1. 标准库和第三方库
# =====================================================================
import backtrader as bt
import pandas as pd
import numpy as np
import os
import re
from datetime import datetime, timedelta, date, time
import logging

# =====================================================================
# 2. 从子模块导入
# =====================================================================

# 证券工具函数和常量
from .securities_utils import (
    format_stock_symbol_for_akshare,
    jq_code_to_ak,
    ak_code_to_jq,
    _stock_code_to_jq,
    _find_date_column,
    _resolve_cache_dir,
    _format_index_code,
    _normalize_index_weights,
    SUPPORTED_INDEXES,
    CONS_ONLY_INDICES,
    INDEX_FALLBACK_MAP,
    INDEX_DESCRIPTION,
    INDEX_CODE_ALIAS_MAP,
    _DATE_COLUMN_CANDIDATES,
    RobustResult,
)

# 数据代理类
from .data_proxies import (
    SecurityInfo,
    _QueryBuilder,
    _Expression,
    _FieldProxy,
    _TableProxy,
    _FinanceTableProxy,
    _FinanceFieldProxy,
    _FinanceModule,
    valuation,
    income,
    cash_flow,
    balance,
    indicator,
    PositionProxy,
    PortfolioProxy,
    _CurrentDataEntry,
    _CurrentDataProxy,
    _TickDataProxy,
)

# 定时器管理
from .timer_manager import TimerManager

# 全局状态
from .global_state import (
    JQLogAdapter,
    log,
    set_current_strategy,
    order_target,
    order_value,
    order,
    GlobalState,
    FundOFPosition,
    ContextProxy,
    PortfolioCompat,
    set_prerun_mode,
    get_prerun_stocks,
    clear_prerun_stocks,
    _prerun_mode_active,
    _prerun_requested_stocks,
)

# API 封装函数
from .api_wrappers import (
    get_index_weights,
    get_index_weights_robust,
    get_index_stocks,
    get_index_stocks_robust,
    get_akshare_etf_data,
    get_akshare_stock_data,
    get_index_nav,
    get_price_unified,
    get_price_jq,
    get_price,
    history,
    attribute_history,
    get_bars_jq,
    get_bars,
    get_cashflow_sina,
    get_income_ths,
    get_balance_sina,
    get_fundamentals,
    get_fundamentals_robust,
    get_fundamentals_jq,
    get_history_fundamentals,
    get_history_fundamentals_robust,
    get_history_fundamentals_jq,
    get_all_securities,
    get_all_securities_jq,
    get_security_info,
    get_security_info_jq,
    get_all_trade_days,
    get_all_trade_days_jq,
    get_trade_days,
    get_extras_jq,
    get_extras,
    get_billboard_list_jq,
    get_billboard_list,
    get_factor_values_jq,
    get_factor_values,
    winsorize,
    winsorize_med,
    standardlize,
    get_current_data,
    get_current_tick,
    analyze_performance,
    query,
    _apply_filter,
)

# 资产路由
from .asset_router import (
    AssetType,
    AssetCategory,
    TradingStatus,
    AssetInfo,
    AssetRouter,
    identify_asset,
    is_stock,
    is_etf,
    is_fund_of,
    is_future,
    is_index,
    is_data_readable,
    get_trading_status_desc,
    get_asset_router,
)


# =====================================================================
# 3. FinanceDBProxy 类定义
# =====================================================================

class FinanceDBProxy:
    """聚宽finance数据库模拟"""

    _DIVIDEND_SCHEMA = ["code", "公司名称", "董事会预案公告日期", "每股派息(税前)(元)", "分红金额(万元)"]
    _MARGIN_SCHEMA = ["code", "date", "margin_balance", "margin_buy", "margin_repay"]
    _FORECAST_SCHEMA = ["code", "year", "type", "forecast_min", "forecast_mean", "forecast_max"]
    _COMPANY_BASIC_INFO_SCHEMA = ["code", "company_name", "industry", "list_date"]

    def run_query(self, query_obj):
        """执行finance查询"""
        # 简化实现，完整实现见原文件
        return pd.DataFrame()


finance_db = FinanceDBProxy()
finance = _FinanceModule()


# =====================================================================
# 4. 策略基类
# =====================================================================

class JQ2BTBaseStrategy(bt.Strategy):
    """聚宽策略基类。"""

    params = (
        ("printlog", True),
        ("log_dir", "logs"),
        ("prerun_mode", False),
        ("max_prerun_days", 5),
    )

    def __init__(self):
        self._order_ref = None
        self.buyprice = None
        self.buycomm = None
        self.navs = []
        os.makedirs(self.params.log_dir, exist_ok=True)
        self.trade_log_file = open(
            os.path.join(self.params.log_dir, "trade_log.txt"), "w", encoding="utf-8"
        )
        self.position_log_file = open(
            os.path.join(self.params.log_dir, "position_log.txt"), "w", encoding="utf-8"
        )

        self.g = GlobalState()
        self._scheduled_tasks = []
        self._bar_count = 0
        self._last_date = None
        self.timer_manager = TimerManager(self)
        self._initial_capital = None
        self.context = ContextProxy(self)
        self.current_dt = None
        self.previous_date = None
        self.portfolio = self.context.portfolio
        self._log_adapter = JQLogAdapter(self)
        self._requested_stocks = set()
        self._prerun_day_count = 0

        if hasattr(self, "initialize"):
            self.initialize()

    def log(self, txt, dt=None, log_type="info"):
        if not self.params.printlog:
            return
        dt = dt or self.datas[0].datetime.date(0)
        line = f"{dt.isoformat()}, {txt}\n"
        if log_type == "trade":
            self.trade_log_file.write(line)
        elif log_type == "position":
            self.position_log_file.write(line)
        else:
            print(f"[INFO] {line.rstrip()}")

    def notify_order(self, order):
        if order.status in [order.Completed]:
            self.log(f"ORDER EXECUTED, {order.data._name}, {order.executed.price:.2f}", log_type="trade")
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f"ORDER FAILED, {order.data._name}", log_type="trade")

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f"TRADE PROFIT, GROSS {trade.pnl:.2f}, NET {trade.pnlcomm:.2f}", log_type="trade")

    def run_daily(self, func, time_str=None, time=None):
        actual_time = time if time is not None else time_str
        if actual_time == "every_bar":
            self.timer_manager.register(func, "daily", "every_bar")
        elif actual_time is not None:
            self.timer_manager.register(func, "daily", actual_time)
        else:
            self.timer_manager.register(func, "daily", "open")

    def run_monthly(self, func, day=1, time="before_open"):
        self.timer_manager.register(func, "monthly", time, day=day)

    def run_weekly(self, func, weekday=1, time="open"):
        self.timer_manager.register(func, "weekly", time, weekday=weekday)

    def unschedule_all(self):
        self.timer_manager.reset()
        self._scheduled_tasks.clear()

    def next(self):
        if self.params.prerun_mode:
            self._prerun_day_count += 1
            if self._prerun_day_count > self.params.max_prerun_days:
                return

        self.navs.append(self.broker.getvalue())
        self._bar_count += 1
        dt = self.datas[0].datetime.date(0)
        dt_time = self.datas[0].datetime.datetime(0)
        self.previous_date = self.current_dt
        self.current_dt = dt_time

        if self._initial_capital is None:
            self._initial_capital = self.broker.getvalue()

        self.context.update_datetime()

        if self._bar_count == 2:
            self.timer_manager.infer_bar_resolution()

        self.timer_manager.check_and_execute()

        if not hasattr(self, "_bars_today") or self._last_date != dt:
            self._bars_today = []
            self._last_date = dt
        self._bars_today.append(self._bar_count)

        for func, time_str in self._scheduled_tasks:
            func(self.context)

    def stop(self):
        self.trade_log_file.close()
        self.position_log_file.close()
        pd.Series(self.navs).to_csv(
            os.path.join(self.params.log_dir, "strategy_nav.csv"), index=False
        )

    def order_target(self, security, amount):
        data = self._get_data_by_name(security)
        if data is None:
            self._requested_stocks.add(self._normalize_stock_code(security))
            return None
        current_size = int(self.getposition(data).size)
        target_size = int(amount)
        delta = target_size - current_size
        if delta > 0:
            return self.buy(data=data, size=delta)
        elif delta < 0:
            return self.sell(data=data, size=abs(delta))
        return None

    def order_value(self, security, value):
        data = self._get_data_by_name(security)
        if data is None or value <= 0:
            return None
        price = data.close[0]
        if price <= 0:
            return None
        size = int(value / price)
        return self.buy(data=data, size=size)

    def order_target_value(self, security, value):
        data = self._get_data_by_name(security)
        if data is None or value <= 0:
            return None
        price = data.close[0]
        if price <= 0:
            return None
        target_size = int(value / price)
        current_size = int(self.getposition(data).size)
        delta = target_size - current_size
        if delta > 0:
            return self.buy(data=data, size=delta)
        elif delta < 0:
            return self.sell(data=data, size=abs(delta))
        return None

    def order(self, security, amount):
        data = self._get_data_by_name(security)
        if data is None:
            return None
        if amount > 0:
            return self.buy(data=data, size=amount)
        elif amount < 0:
            return self.sell(data=data, size=abs(amount))
        return None

    def _get_data_by_name(self, name):
        if isinstance(name, bt.feeds.PandasData):
            return name
        formats = [name]
        if ".XSHG" in name or ".XSHE" in name:
            formats.append(jq_code_to_ak(name))
        if name.startswith("sh") or name.startswith("sz"):
            formats.append(name[2:])
        if name.isdigit() and len(name) == 6:
            if name.startswith("6"):
                formats.append("sh" + name)
                formats.append(name + ".XSHG")
            else:
                formats.append("sz" + name)
                formats.append(name + ".XSHE")
        for data in self.datas:
            if data._name in formats:
                return data
        return None

    def _normalize_stock_code(self, code):
        if ".XSHG" in code or ".XSHE" in code:
            return code
        if code.startswith("sh"):
            return code[2:] + ".XSHG"
        if code.startswith("sz"):
            return code[2:] + ".XSHE"
        code_num = code.zfill(6)
        if code_num.startswith("6"):
            return code_num + ".XSHG"
        return code_num + ".XSHE"

    @staticmethod
    def get_akshare_stock_data(symbol, start, end, **kwargs):
        return get_akshare_stock_data(symbol, start, end, **kwargs)

    @staticmethod
    def get_akshare_etf_data(symbol, start, end, **kwargs):
        return get_akshare_etf_data(symbol, start, end, **kwargs)


# =====================================================================
# 5. 框架主流程入口
# =====================================================================

def run_bt_framework(
    strategy_class,
    ETF_POOL,
    start_date,
    end_date,
    benchmark_symbol="000300",
    cash=1000000,
    commission=0.0002,
    slippage=0.0,
):
    """回测框架主流程入口。"""
    datas = []
    for symbol in ETF_POOL.keys():
        data = get_akshare_etf_data(symbol, start_date, end_date)
        assert data is not None, f"数据加载失败: {symbol}"
        datas.append(data)

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(commission=commission)
    cerebro.broker.set_slippage_perc(perc=slippage)
    for symbol, data in zip(ETF_POOL.keys(), datas):
        cerebro.adddata(data, name=symbol)
    cerebro.addstrategy(strategy_class)

    print(f"[INFO] Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    results = cerebro.run()
    strat = results[0]
    print(f"[INFO] Final Portfolio Value: {cerebro.broker.getvalue():.2f}")

    length = strat.datas[0].buflen()
    dates = [strat.datas[0].datetime.date(-i) for i in range(length)]
    dates.reverse()
    strategy_nav = pd.Series(strat.navs, index=dates)

    benchmark_nav = get_index_nav(benchmark_symbol, start_date, end_date)
    benchmark_nav = benchmark_nav.reindex(strategy_nav.index).fillna(method="ffill")

    analyze_performance(strategy_nav, benchmark_nav)

    plt.figure(figsize=(10, 5))
    (strategy_nav / strategy_nav.iloc[0]).plot(label="策略净值")
    (benchmark_nav / benchmark_nav.iloc[0]).plot(label="基准", linestyle="--")
    plt.legend()
    plt.title(f"{strategy_class.__name__} vs {benchmark_symbol} 净值对比")
    plt.grid(True)
    plt.show()


# =====================================================================
# 6. 模块导出
# =====================================================================

# 统一交易日 API 返回类型：对外固定返回 list，避免不同实现返回 DatetimeIndex 导致兼容性问题。
_get_all_trade_days_jq_impl = get_all_trade_days_jq


def _normalize_trade_days(days):
    if days is None:
        return []
    if isinstance(days, list):
        return days
    if isinstance(days, pd.DatetimeIndex):
        return days.tolist()
    try:
        return list(days)
    except TypeError:
        return [days]


def get_all_trade_days_jq(*args, **kwargs):
    return _normalize_trade_days(_get_all_trade_days_jq_impl(*args, **kwargs))


def get_all_trade_days(*args, **kwargs):
    return get_all_trade_days_jq(*args, **kwargs)

__all__ = [
    # 证券工具函数
    'format_stock_symbol_for_akshare',
    'jq_code_to_ak',
    'ak_code_to_jq',
    'RobustResult',
    # 类
    'SecurityInfo',
    'valuation',
    'income',
    'cash_flow',
    'balance',
    'indicator',
    'TimerManager',
    'JQLogAdapter',
    'log',
    'GlobalState',
    'FundOFPosition',
    'ContextProxy',
    'FinanceDBProxy',
    'finance_db',
    'finance',
    'JQ2BTBaseStrategy',
    # API 函数
    'get_index_weights',
    'get_index_stocks',
    'get_price',
    'get_price_jq',
    'get_fundamentals',
    'get_all_securities',
    'get_all_securities_jq',
    'get_security_info',
    'get_all_trade_days',
    'get_all_trade_days_jq',
    'get_trade_days',
    'get_extras_jq',
    'get_extras',
    'get_billboard_list_jq',
    'get_billboard_list',
    'get_factor_values_jq',
    'get_factor_values',
    'winsorize',
    'winsorize_med',
    'standardlize',
    'get_current_data',
    'get_current_tick',
    'query',
    'run_bt_framework',
    # 资产路由
    'AssetType',
    'AssetCategory',
    'identify_asset',
    'is_stock',
]
