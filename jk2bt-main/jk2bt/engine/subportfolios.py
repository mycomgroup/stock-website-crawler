"""
subportfolios.py
子账户模型实现

为多资产策略提供独立的子账户:
- 每个子账户有独立的现金视图
- 支持子账户间资金划转
- 为期货、基金等资产类策略预留扩展点

设计原则:
- 不退化成同一个 portfolio 的浅包装
- 主账户与子账户现金独立核算
- 为后续期货撮合系统预留接口
"""

from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SubportfolioType(Enum):
    STOCK = "stock"
    ETF = "etf"
    FUTURE = "future"
    FUND = "fund"
    MIXED = "mixed"


@dataclass
class SubportfolioConfig:
    name: str
    type: SubportfolioType
    initial_cash: float = 0.0
    max_cash: Optional[float] = None
    allow_negative: bool = False
    asset_filter: Optional[Callable[[str], bool]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class SubportfolioPosition:
    def __init__(self, code: str, size: int, price: float, subportfolio_id: int):
        self.code = code
        self.size = size
        self.price = price
        self.subportfolio_id = subportfolio_id
        self._value_cache: Optional[float] = None

    @property
    def value(self) -> float:
        if self._value_cache is None:
            self._value_cache = self.size * self.price
        return self._value_cache

    def update_price(self, new_price: float) -> None:
        self.price = new_price
        self._value_cache = None

    def __repr__(self) -> str:
        return f"SubportfolioPosition(code={self.code}, size={self.size}, price={self.price:.2f})"


class SubportfolioCashAccount:
    def __init__(
        self, initial_cash: float, subportfolio_id: int, allow_negative: bool = False
    ):
        self._cash = initial_cash
        self._initial_cash = initial_cash
        self._subportfolio_id = subportfolio_id
        self._allow_negative = allow_negative
        self._transactions: List[Dict[str, Any]] = []

    @property
    def cash(self) -> float:
        return self._cash

    @property
    def available_cash(self) -> float:
        return self._cash

    @property
    def initial_cash(self) -> float:
        return self._initial_cash

    def deposit(self, amount: float, reason: str = "") -> bool:
        if amount < 0:
            logger.warning(f"子账户{self._subportfolio_id}存款金额不能为负: {amount}")
            return False
        self._cash += amount
        self._transactions.append(
            {
                "type": "deposit",
                "amount": amount,
                "balance_after": self._cash,
                "reason": reason,
            }
        )
        return True

    def withdraw(self, amount: float, reason: str = "") -> bool:
        if amount < 0:
            logger.warning(f"子账户{self._subportfolio_id}取款金额不能为负: {amount}")
            return False
        if not self._allow_negative and self._cash < amount:
            logger.warning(
                f"子账户{self._subportfolio_id}现金不足: 当前{self._cash}, 需要{amount}"
            )
            return False
        self._cash -= amount
        self._transactions.append(
            {
                "type": "withdraw",
                "amount": amount,
                "balance_after": self._cash,
                "reason": reason,
            }
        )
        return True

    def get_transactions(self) -> List[Dict[str, Any]]:
        return self._transactions.copy()

    def reset(self, new_cash: Optional[float] = None) -> None:
        self._cash = new_cash if new_cash is not None else self._initial_cash
        self._transactions.clear()


class SubportfolioProxy:
    def __init__(
        self,
        config: SubportfolioConfig,
        subportfolio_id: int,
        parent_strategy: Any = None,
    ):
        self._config = config
        self._id = subportfolio_id
        self._parent = parent_strategy
        self._cash_account = SubportfolioCashAccount(
            config.initial_cash, subportfolio_id, config.allow_negative
        )
        self._positions: Dict[str, SubportfolioPosition] = {}
        self._type = config.type

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._config.name

    @property
    def type(self) -> SubportfolioType:
        return self._type

    @property
    def cash(self) -> float:
        return self._cash_account.cash

    @property
    def available_cash(self) -> float:
        return self._cash_account.available_cash

    @property
    def initial_cash(self) -> float:
        return self._cash_account.initial_cash

    @property
    def positions(self) -> Dict[str, SubportfolioPosition]:
        return self._positions.copy()

    @property
    def positions_value(self) -> float:
        return sum(p.value for p in self._positions.values())

    @property
    def total_value(self) -> float:
        return self.cash + self.positions_value

    @property
    def returns(self) -> float:
        if self._cash_account.initial_cash > 0:
            return self.total_value / self._cash_account.initial_cash - 1
        return 0.0

    def add_position(self, code: str, size: int, price: float) -> None:
        if code in self._positions:
            existing = self._positions[code]
            new_size = existing.size + size
            if new_size == 0:
                del self._positions[code]
            else:
                total_cost = existing.size * existing.price + size * price
                avg_price = total_cost / new_size
                self._positions[code] = SubportfolioPosition(
                    code, new_size, avg_price, self._id
                )
        else:
            if size != 0:
                self._positions[code] = SubportfolioPosition(
                    code, size, price, self._id
                )

    def update_position_price(self, code: str, new_price: float) -> None:
        if code in self._positions:
            self._positions[code].update_price(new_price)

    def remove_position(self, code: str) -> None:
        if code in self._positions:
            del self._positions[code]

    def deposit_cash(self, amount: float, reason: str = "") -> bool:
        return self._cash_account.deposit(amount, reason)

    def withdraw_cash(self, amount: float, reason: str = "") -> bool:
        return self._cash_account.withdraw(amount, reason)

    def can_trade(self, code: str) -> bool:
        if self._config.asset_filter is not None:
            return self._config.asset_filter(code)
        return True

    def get_transactions(self) -> List[Dict[str, Any]]:
        return self._cash_account.get_transactions()

    def reset_cash(self, new_cash: Optional[float] = None) -> None:
        self._cash_account.reset(new_cash)
        self._positions.clear()

    def __repr__(self) -> str:
        return (
            f"SubportfolioProxy(id={self._id}, name={self.name}, "
            f"cash={self.cash:.2f}, total_value={self.total_value:.2f})"
        )


class SubportfolioManager:
    def __init__(self, parent_strategy: Any = None):
        self._subportfolios: List[SubportfolioProxy] = []
        self._parent = parent_strategy
        self._main_cash_account: Optional[SubportfolioCashAccount] = None
        self._initialized = False

    def initialize(self, main_cash: float) -> None:
        if self._initialized:
            return
        self._main_cash_account = SubportfolioCashAccount(
            main_cash, -1, allow_negative=False
        )
        self._initialized = True

    @property
    def subportfolios(self) -> List[SubportfolioProxy]:
        return self._subportfolios

    @property
    def main_cash(self) -> float:
        if self._main_cash_account is None:
            return 0.0
        return self._main_cash_account.cash

    @property
    def total_cash(self) -> float:
        return self.main_cash + sum(sp.cash for sp in self._subportfolios)

    def set_subportfolios(
        self, configs: List[SubportfolioConfig]
    ) -> List[SubportfolioProxy]:
        self._subportfolios.clear()
        for i, config in enumerate(configs):
            sp = SubportfolioProxy(config, i, self._parent)
            self._subportfolios.append(sp)
        logger.info(
            f"设置了 {len(self._subportfolios)} 个子账户: {[sp.name for sp in self._subportfolios]}"
        )
        return self._subportfolios

    def add_subportfolio(self, config: SubportfolioConfig) -> SubportfolioProxy:
        new_id = len(self._subportfolios)
        sp = SubportfolioProxy(config, new_id, self._parent)
        self._subportfolios.append(sp)
        return sp

    def get_subportfolio(self, index: int) -> Optional[SubportfolioProxy]:
        if 0 <= index < len(self._subportfolios):
            return self._subportfolios[index]
        return None

    def get_subportfolio_by_name(self, name: str) -> Optional[SubportfolioProxy]:
        for sp in self._subportfolios:
            if sp.name == name:
                return sp
        return None

    def transfer_cash(
        self,
        from_index: int,
        to_index: int,
        amount: float,
        reason: str = "",
    ) -> bool:
        if amount <= 0:
            logger.warning(f"划转金额必须为正: {amount}")
            return False

        from_sp = self.get_subportfolio(from_index)
        to_sp = self.get_subportfolio(to_index)

        if from_sp is None or to_sp is None:
            logger.warning(f"子账户索引无效: from={from_index}, to={to_index}")
            return False

        if from_sp.withdraw_cash(amount, f"划转至{to_sp.name}: {reason}"):
            if to_sp.deposit_cash(amount, f"来自{from_sp.name}: {reason}"):
                logger.info(
                    f"资金划转成功: {from_sp.name} -> {to_sp.name}, 金额={amount:.2f}"
                )
                return True
            else:
                from_sp.deposit_cash(amount, f"划转失败回退: {reason}")
                logger.warning(f"资金划转失败: 接收方存款失败")
                return False
        else:
            logger.warning(f"资金划转失败: 发送方取款失败")
            return False

    def transfer_from_main(
        self,
        to_index: int,
        amount: float,
        reason: str = "",
    ) -> bool:
        if self._main_cash_account is None:
            logger.warning("主账户未初始化")
            return False

        if amount <= 0:
            logger.warning(f"划转金额必须为正: {amount}")
            return False

        to_sp = self.get_subportfolio(to_index)
        if to_sp is None:
            logger.warning(f"子账户索引无效: {to_index}")
            return False

        if self._main_cash_account.withdraw(amount, f"划转至{to_sp.name}: {reason}"):
            if to_sp.deposit_cash(amount, f"来自主账户: {reason}"):
                logger.info(f"主账户资金划转成功: -> {to_sp.name}, 金额={amount:.2f}")
                return True
            else:
                self._main_cash_account.deposit(amount, f"划转失败回退: {reason}")
                return False
        return False

    def transfer_to_main(
        self,
        from_index: int,
        amount: float,
        reason: str = "",
    ) -> bool:
        if self._main_cash_account is None:
            logger.warning("主账户未初始化")
            return False

        from_sp = self.get_subportfolio(from_index)
        if from_sp is None:
            logger.warning(f"子账户索引无效: {from_index}")
            return False

        if from_sp.withdraw_cash(amount, f"划转至主账户: {reason}"):
            if self._main_cash_account.deposit(amount, f"来自{from_sp.name}: {reason}"):
                logger.info(
                    f"子账户资金划转成功: {from_sp.name} -> 主账户, 金额={amount:.2f}"
                )
                return True
            else:
                from_sp.deposit_cash(amount, f"划转失败回退: {reason}")
                return False
        return False

    def get_total_value(self) -> float:
        main_value = self.main_cash
        sub_values = sum(sp.total_value for sp in self._subportfolios)
        return main_value + sub_values

    def get_summary(self) -> Dict[str, Any]:
        return {
            "main_cash": self.main_cash,
            "subportfolios": [
                {
                    "id": sp.id,
                    "name": sp.name,
                    "type": sp.type.value,
                    "cash": sp.cash,
                    "positions_value": sp.positions_value,
                    "total_value": sp.total_value,
                    "returns": sp.returns,
                }
                for sp in self._subportfolios
            ],
            "total_value": self.get_total_value(),
        }

    def reset_all(self) -> None:
        if self._main_cash_account:
            self._main_cash_account.reset()
        for sp in self._subportfolios:
            sp.reset_cash()

    def __getitem__(self, index: int) -> SubportfolioProxy:
        return self._subportfolios[index]

    def __len__(self) -> int:
        return len(self._subportfolios)

    def __repr__(self) -> str:
        return f"SubportfolioManager(count={len(self._subportfolios)}, main_cash={self.main_cash:.2f})"


def set_subportfolios(
    context: Any,
    configs: List[SubportfolioConfig],
) -> List[SubportfolioProxy]:
    manager = getattr(context, "_subportfolio_manager", None)
    if manager is None:
        manager = SubportfolioManager()
        context._subportfolio_manager = manager
    return manager.set_subportfolios(configs)


def transfer_cash(
    context: Any,
    from_index: int,
    to_index: int,
    amount: float,
    reason: str = "",
) -> bool:
    manager = getattr(context, "_subportfolio_manager", None)
    if manager is None:
        logger.warning("context 未设置 subportfolio_manager")
        return False
    return manager.transfer_cash(from_index, to_index, amount, reason)


def get_subportfolio_summary(context: Any) -> Dict[str, Any]:
    manager = getattr(context, "_subportfolio_manager", None)
    if manager is None:
        return {"error": "未设置子账户管理器"}
    return manager.get_summary()
