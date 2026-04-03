"""
global_state.py
全局状态管理类和日志对象。

包含:
- GlobalState: 聚宽 g 对象模拟
- FundOFPosition: 场外基金持仓模拟类
- JQLogAdapter: 聚宽 log 对象模拟
- ContextProxy: 聚宽 context 对象模拟
- PortfolioCompat: 兼容聚宽 context.portfolio 风格
"""

import logging
import pandas as pd

from .data_proxies import PositionProxy, PortfolioProxy

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


# =====================================================================
# JQLogAdapter - 聚宽 log 对象模拟
# =====================================================================


class JQLogAdapter:
    """
    聚宽log对象模拟

    支持方法:
        log.info(*args) - 信息日志
        log.warn(*args) - 警告日志
        log.error(*args) - 错误日志
        log.debug(*args) - 调试日志
        log.set_level(module, level) - 设置日志级别
    """

    def __init__(self, strategy=None):
        self._strategy = strategy
        self._log_levels = {
            "order": "info",
            "trade": "info",
            "debug": "info",
        }

    def info(self, *args, **kwargs):
        msg = self._format_message(args, kwargs)
        if self._strategy is not None:
            self._strategy.log(msg)
        else:
            print(f"[INFO] {msg}")

    def warn(self, *args, **kwargs):
        msg = self._format_message(args, kwargs)
        if self._strategy is not None:
            self._strategy.log(f"[WARN] {msg}")
        else:
            print(f"[WARN] {msg}")

    def error(self, *args, **kwargs):
        msg = self._format_message(args, kwargs)
        if self._strategy is not None:
            self._strategy.log(f"[ERROR] {msg}")
        else:
            print(f"[ERROR] {msg}")

    def debug(self, *args, **kwargs):
        level = self._log_levels.get("debug", "info")
        if level == "debug":
            msg = self._format_message(args, kwargs)
            if self._strategy is not None:
                self._strategy.log(f"[DEBUG] {msg}")
            else:
                print(f"[DEBUG] {msg}")

    def set_level(self, module, level):
        self._log_levels[module] = level

    def _format_message(self, args, kwargs):
        parts = []
        for arg in args:
            if isinstance(arg, pd.DataFrame):
                parts.append("\n" + str(arg))
            elif isinstance(arg, pd.Series):
                parts.append("\n" + str(arg))
            else:
                parts.append(str(arg))
        msg = " ".join(parts)
        if kwargs:
            kwargs_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
            if msg:
                msg += " " + kwargs_str
            else:
                msg = kwargs_str
        return msg


# 全局 log 对象
log = JQLogAdapter(None)

# 当前策略实例
_current_strategy = None


def set_current_strategy(strategy):
    """设置当前运行的策略实例"""
    global _current_strategy, log
    _current_strategy = strategy
    log = JQLogAdapter(strategy)


def order_target(security, amount):
    """全局order_target函数"""
    if _current_strategy:
        return _current_strategy.order_target(security, amount)
    return None


def order_value(security, value):
    """全局order_value函数"""
    if _current_strategy:
        return _current_strategy.order_value(security, value)
    return None


def order(security, amount):
    """全局order函数"""
    if _current_strategy:
        return _current_strategy.order(security, amount)
    return None


# =====================================================================
# GlobalState - 聚宽 g 对象模拟
# =====================================================================


class GlobalState:
    """
    聚宽g对象模拟，用于存储全局状态

    使用示例:
        self.g.index = '000300.XSHG'
        self.g.stocks = []
        self.g.num = 10
    """

    def __init__(self):
        self._state = {}

    def __getattr__(self, name):
        if name.startswith("_"):
            return super().__getattribute__(name)
        return self._state.get(name, None)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._state[name] = value

    def __delattr__(self, name):
        if name in self._state:
            del self._state[name]

    def __contains__(self, name):
        """支持 'name' in g 语法"""
        return name in self._state

    def get(self, name, default=None):
        """获取属性值，支持默认值"""
        return self._state.get(name, default)

    def set(self, name, value):
        """设置属性值"""
        self._state[name] = value

    def items(self):
        """返回所有属性"""
        return self._state.items()

    def clear(self):
        """清空所有属性"""
        self._state.clear()


# =====================================================================
# FundOFPosition - 场外基金持仓模拟类
# =====================================================================


class FundOFPosition:
    """场外基金持仓模拟类

    支持申购、赎回、份额管理、费用计算等场外基金特有机制。

    示例:
        pos = FundOFPosition('000001')
        pos.subscribe(10000, nav=1.5)  # 申购1万元，净值1.5
        value = pos.get_value(current_nav=1.6)  # 当前市值
        pos.redeem(5000, nav=1.6)  # 赎回5000份
    """

    def __init__(self, fund_code: str, shares: float = 0, cost: float = 0):
        self.fund_code = fund_code
        self.shares = shares
        self.cost = cost
        self.transactions = []
        self._purchase_fee_rate = 0.0015
        self._redeem_fee_rate = 0.005

    def subscribe(
        self, amount: float, nav: float, fee_rate: float = None, date=None
    ) -> tuple:
        """申购基金

        参数:
            amount: 申购金额（元）
            nav: 申购当日净值
            fee_rate: 申购费率，默认0.15%
            date: 申购日期

        返回:
            (new_shares, fee) 新增份额和费用
        """
        from datetime import datetime

        if fee_rate is None:
            fee_rate = self._purchase_fee_rate

        fee = amount * fee_rate
        actual_amount = amount - fee
        new_shares = actual_amount / nav

        self.shares += new_shares
        self.cost += amount

        transaction = {
            "type": "subscribe",
            "amount": amount,
            "nav": nav,
            "shares": new_shares,
            "fee": fee,
            "fee_rate": fee_rate,
            "date": date or datetime.now(),
        }
        self.transactions.append(transaction)

        logger.info(
            f"基金 {self.fund_code} 申购: 金额{amount:.2f}, 净值{nav:.4f}, 份额{new_shares:.2f}, 费用{fee:.2f}"
        )

        return new_shares, fee

    def redeem(
        self,
        shares: float,
        nav: float,
        fee_rate: float = None,
        holding_days: int = 0,
        date=None,
    ) -> tuple:
        """赎回基金

        参数:
            shares: 赎回份额
            nav: 赎回当日净值
            fee_rate: 赎回费率，默认根据持有天数计算
            holding_days: 持有天数（影响赎回费率）
            date: 赎回日期

        返回:
            (actual_amount, fee) 实际到账金额和费用
        """
        from datetime import datetime

        if shares > self.shares:
            raise ValueError(f"赎回份额 {shares} 超过持有份额 {self.shares:.2f}")

        if fee_rate is None:
            if holding_days >= 365:
                fee_rate = 0
            elif holding_days > 180:
                fee_rate = 0.0025
            elif holding_days > 30:
                fee_rate = 0.005
            else:
                fee_rate = 0.0075

        amount = shares * nav
        fee = amount * fee_rate
        actual_amount = amount - fee

        self.shares -= shares

        if self.shares > 0:
            avg_cost_per_share = self.cost / (self.shares + shares)
            self.cost -= shares * avg_cost_per_share
        else:
            self.cost = 0

        transaction = {
            "type": "redeem",
            "shares": shares,
            "nav": nav,
            "amount": amount,
            "actual_amount": actual_amount,
            "fee": fee,
            "fee_rate": fee_rate,
            "holding_days": holding_days,
            "date": date or datetime.now(),
        }
        self.transactions.append(transaction)

        logger.info(
            f"基金 {self.fund_code} 赎回: 份额{shares:.2f}, 净值{nav:.4f}, 到账{actual_amount:.2f}, 费用{fee:.2f}"
        )

        return actual_amount, fee

    def get_value(self, current_nav: float) -> float:
        """获取当前市值"""
        return self.shares * current_nav

    def get_profit(self, current_nav: float) -> float:
        """获取浮动收益"""
        if self.cost == 0:
            return 0
        current_value = self.get_value(current_nav)
        return current_value - self.cost

    def get_profit_rate(self, current_nav: float) -> float:
        """获取收益率"""
        if self.cost == 0:
            return 0
        return self.get_profit(current_nav) / self.cost

    def get_avg_cost(self) -> float:
        """获取平均成本"""
        if self.shares == 0:
            return 0
        return self.cost / self.shares

    def get_transactions(self) -> list:
        """获取交易记录"""
        return self.transactions.copy()

    def __repr__(self) -> str:
        return f"FundOFPosition(fund={self.fund_code}, shares={self.shares:.2f}, cost={self.cost:.2f})"


# =====================================================================
# ContextProxy - 聚宽 context 对象模拟
# =====================================================================


class ContextProxy:
    """聚宽 context 对象模拟，支持子账户模型"""

    def __init__(self, strategy):
        self._strategy = strategy
        self.portfolio = PortfolioProxy(strategy)
        self.current_dt = None
        self._subportfolio_manager = None
        self._use_new_subportfolios = False

    @property
    def subportfolios(self) -> list:
        if self._use_new_subportfolios and self._subportfolio_manager is not None:
            return self._subportfolio_manager.subportfolios
        return [self.portfolio]

    def set_subportfolios(self, configs) -> list:
        try:
            from ..strategy.subportfolios import SubportfolioManager, SubportfolioConfig
        except ImportError:
            from jk2bt.strategy.subportfolios import (
                SubportfolioManager,
                SubportfolioConfig,
            )

        if not isinstance(configs, list):
            configs = [configs]

        normalized_configs = []
        for c in configs:
            if isinstance(c, dict):
                try:
                    from ..strategy.subportfolios import SubportfolioType
                except ImportError:
                    from jk2bt.strategy.subportfolios import SubportfolioType

                sp_type = SubportfolioType.MIXED
                if "type" in c:
                    type_str = c["type"]
                    for t in SubportfolioType:
                        if t.value == type_str or t.name.lower() == type_str.lower():
                            sp_type = t
                            break
                normalized_configs.append(
                    SubportfolioConfig(
                        name=c.get("name", f"subportfolio_{len(normalized_configs)}"),
                        type=sp_type,
                        initial_cash=c.get("initial_cash", 0.0),
                        max_cash=c.get("max_cash"),
                        allow_negative=c.get("allow_negative", False),
                        metadata=c.get("metadata", {}),
                    )
                )
            else:
                normalized_configs.append(c)

        if self._subportfolio_manager is None:
            self._subportfolio_manager = SubportfolioManager(self._strategy)
            main_cash = (
                self._strategy.broker.getcash()
                if hasattr(self._strategy, "broker")
                else 0.0
            )
            self._subportfolio_manager.initialize(main_cash)

        result = self._subportfolio_manager.set_subportfolios(normalized_configs)
        self._use_new_subportfolios = True
        return result

    def transfer_cash(
        self, from_index: int, to_index: int, amount: float, reason: str = ""
    ) -> bool:
        if self._subportfolio_manager is None:
            logger.warning("未设置子账户，无法划转资金")
            return False
        return self._subportfolio_manager.transfer_cash(
            from_index, to_index, amount, reason
        )

    def get_subportfolio(self, index: int):
        if self._subportfolio_manager is None:
            return None
        return self._subportfolio_manager.get_subportfolio(index)

    def get_subportfolio_by_name(self, name: str):
        if self._subportfolio_manager is None:
            return None
        return self._subportfolio_manager.get_subportfolio_by_name(name)

    def add_subportfolio(self, config):
        try:
            from .subportfolios import SubportfolioConfig, SubportfolioType
        except ImportError:
            from subportfolios import SubportfolioConfig, SubportfolioType

        if isinstance(config, dict):
            sp_type = SubportfolioType.MIXED
            if "type" in config:
                type_str = config["type"]
                for t in SubportfolioType:
                    if t.value == type_str or t.name.lower() == type_str.lower():
                        sp_type = t
                        break
            normalized_config = SubportfolioConfig(
                name=config.get("name", "new_subportfolio"),
                type=sp_type,
                initial_cash=config.get("initial_cash", 0.0),
                max_cash=config.get("max_cash"),
                allow_negative=config.get("allow_negative", False),
                metadata=config.get("metadata", {}),
            )
        else:
            normalized_config = config

        if self._subportfolio_manager is None:
            self._subportfolio_manager = SubportfolioManager(self._strategy)
            main_cash = (
                self._strategy.broker.getcash()
                if hasattr(self._strategy, "broker")
                else 0.0
            )
            self._subportfolio_manager.initialize(main_cash)

        result = self._subportfolio_manager.add_subportfolio(normalized_config)
        self._use_new_subportfolios = True
        return result

    def transfer_from_main(
        self, to_index: int, amount: float, reason: str = ""
    ) -> bool:
        if self._subportfolio_manager is None:
            logger.warning("未设置子账户，无法从主账户划转资金")
            return False
        return self._subportfolio_manager.transfer_from_main(to_index, amount, reason)

    def transfer_to_main(
        self, from_index: int, amount: float, reason: str = ""
    ) -> bool:
        if self._subportfolio_manager is None:
            logger.warning("未设置子账户，无法向主账户划转资金")
            return False
        return self._subportfolio_manager.transfer_to_main(from_index, amount, reason)

    def get_subportfolio_summary(self) -> dict:
        if self._subportfolio_manager is None:
            return {"error": "未设置子账户管理器"}
        return self._subportfolio_manager.get_summary()

    def update_datetime(self):
        """更新当前日期时间"""
        if self._strategy.datas:
            self.current_dt = self._strategy.datas[0].datetime.datetime(0)

    @property
    def run_params(self):
        """运行参数对象（兼容聚宽）"""
        # 返回一个模拟的 run_params 对象
        class RunParams:
            type = 'backtest'  # 模拟回测模式
        return RunParams()

    @property
    def previous_date(self):
        """前一个交易日（兼容）"""
        prev_date = getattr(self._strategy, "previous_date", None)
        # 如果 previous_date 为 None，返回 current_dt 作为默认值
        if prev_date is None:
            return getattr(self._strategy, "current_dt", None)
        return prev_date


# =====================================================================
# PortfolioCompat - 兼容聚宽 context.portfolio 风格
# =====================================================================


class PortfolioCompat:
    """兼容聚宽 context.portfolio 风格（保留向后兼容）。"""

    def __init__(self, strategy):
        self._s = strategy

    @property
    def positions(self):
        pos = {}
        for data in self._s.datas:
            p = self._s.getposition(data)
            if p.size != 0:
                pos[data._name] = p
        return pos

    @property
    def cash(self):
        return self._s.broker.getcash()

    @property
    def available_cash(self):
        return self._s.broker.getcash()

    @property
    def total_value(self):
        return self._s.broker.getvalue()

    @property
    def positions_value(self):
        return sum(p.size * p.price for p in self.positions.values())


# 预运行模式全局状态
_prerun_requested_stocks = set()
_prerun_mode_active = False


def set_prerun_mode(active):
    """设置预运行模式"""
    global _prerun_mode_active, _prerun_requested_stocks
    _prerun_mode_active = active
    if active:
        _prerun_requested_stocks = set()


def get_prerun_stocks():
    """获取预运行期间请求的股票"""
    return _prerun_requested_stocks.copy()


def clear_prerun_stocks():
    """清空预运行股票集合"""
    global _prerun_requested_stocks
    _prerun_requested_stocks = set()


__all__ = [
    'JQLogAdapter',
    'log',
    'set_current_strategy',
    'order_target',
    'order_value',
    'order',
    'GlobalState',
    'FundOFPosition',
    'ContextProxy',
    'PortfolioCompat',
    'set_prerun_mode',
    'get_prerun_stocks',
    'clear_prerun_stocks',
]