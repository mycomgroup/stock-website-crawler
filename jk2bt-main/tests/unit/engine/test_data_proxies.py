"""
test_data_proxies.py
data_proxies.py 单元测试

测试场景覆盖:
1. SecurityInfo 证券信息类
2. _QueryBuilder 查询构建器
3. _Expression 表达式类
4. _FieldProxy 字段代理
5. _TableProxy 表代理
6. PositionProxy 持仓代理
7. PortfolioProxy 组合代理
8. _CurrentDataEntry 当前数据条目
9. _CurrentDataProxy 当前数据代理
10. _TickDataProxy tick数据代理
11. valuation/income/cash_flow/balance/indicator 表对象
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

try:
    from jk2bt.engine.data_proxies import (
        SecurityInfo,
        _QueryBuilder,
        _Expression,
        _FieldProxy,
        _TableProxy,
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
except ImportError:
    pytest.skip("data_proxies module not available", allow_module_level=True)


class TestSecurityInfo:
    """测试 SecurityInfo 证券信息类"""

    def test_basic_creation(self):
        """测试基本创建"""
        info = SecurityInfo(
            {
                "code": "600519.XSHG",
                "display_name": "贵州茅台",
                "start_date": "2024-01-01",
            }
        )
        assert info.code == "600519.XSHG"
        assert info.display_name == "贵州茅台"

    def test_name_fallback(self):
        """测试name回退到display_name"""
        info = SecurityInfo({"code": "600519.XSHG", "name": "贵州茅台"})
        assert info.display_name == "贵州茅台"

    def test_getitem(self):
        """测试字典式访问"""
        info = SecurityInfo({"code": "600519", "pe": 30})
        assert info["pe"] == 30

    def test_repr(self):
        """测试字符串表示"""
        info = SecurityInfo({"code": "600519", "display_name": "贵州茅台"})
        r = repr(info)
        assert "600519" in r
        assert "贵州茅台" in r


class TestQueryBuilder:
    """测试 _QueryBuilder 查询构建器"""

    def test_basic_creation(self):
        """测试基本创建"""
        qb = _QueryBuilder("valuation")
        assert qb._tables == ["valuation"]

    def test_accepts_multiple_tables(self):
        """测试接受多个表"""
        qb = _QueryBuilder(["valuation", "income"])
        assert qb._tables == ["valuation", "income"]

    def test_filter_returns_self(self):
        """测试filter返回自身"""
        qb = _QueryBuilder("valuation")
        result = qb.filter(MagicMock())
        assert result is qb

    def test_order_by_returns_self(self):
        """测试order_by返回自身"""
        qb = _QueryBuilder("valuation")
        result = qb.order_by("code")
        assert result is qb

    def test_limit_returns_self(self):
        """测试limit返回自身"""
        qb = _QueryBuilder("valuation")
        result = qb.limit(10)
        assert result is qb

    def test_repr(self):
        """测试字符串表示"""
        qb = _QueryBuilder("valuation")
        r = repr(qb)
        assert "valuation" in r


class TestExpression:
    """测试 _Expression 表达式类"""

    def test_basic_expression(self):
        """测试基本表达式"""
        expr = _Expression("a", "+", "b")
        assert expr.left == "a"
        assert expr.op == "+"
        assert expr.right == "b"

    def test_multiplication_expression(self):
        """测试乘法表达式"""
        expr = _Expression("a", "*", "b")
        assert expr.op == "*"


class TestFieldProxy:
    """测试 _FieldProxy 字段代理"""

    def test_in_operation(self):
        """测试in操作"""
        fp = _FieldProxy("valuation", "code")
        result = fp.in_(["600519", "000001"])
        assert fp._symbols == ["600519", "000001"]
        assert result is fp

    def test_comparison_operators(self):
        """测试比较运算符"""
        fp = _FieldProxy("valuation", "pe_ratio")

        assert fp.__gt__(10)._operator == ">"
        assert fp.__lt__(10)._operator == "<"
        assert fp.__ge__(10)._operator == ">="
        assert fp.__le__(10)._operator == "<="
        assert fp.__eq__(10)._operator == "=="

    def test_arithmetic_operators(self):
        """测试算术运算符"""
        fp = _FieldProxy("valuation", "pe_ratio")

        expr = fp * 2
        assert isinstance(expr, _Expression)

        expr = fp / 2
        assert isinstance(expr, _Expression)

        expr = fp + 2
        assert isinstance(expr, _Expression)

        expr = fp - 2
        assert isinstance(expr, _Expression)


class TestTableProxy:
    """测试 _TableProxy 表代理"""

    def test_getattr_returns_field_proxy(self):
        """测试__getattr__返回字段代理"""
        tp = _TableProxy("valuation")
        fp = tp.code
        assert isinstance(fp, _FieldProxy)
        assert fp._field == "code"

    def test_multiple_fields(self):
        """测试多个字段"""
        tp = _TableProxy("valuation")
        fp1 = tp.code
        fp2 = tp.pe_ratio
        assert fp1._field == "code"
        assert fp2._field == "pe_ratio"


class TestTableObjects:
    """测试表对象"""

    def test_valuation_exists(self):
        """测试valuation表存在"""
        assert isinstance(valuation, _TableProxy)
        assert valuation._name == "valuation"

    def test_income_exists(self):
        """测试income表存在"""
        assert isinstance(income, _TableProxy)
        assert income._name == "income"

    def test_cash_flow_exists(self):
        """测试cash_flow表存在"""
        assert isinstance(cash_flow, _TableProxy)
        assert cash_flow._name == "cash_flow"

    def test_balance_exists(self):
        """测试balance表存在"""
        assert isinstance(balance, _TableProxy)
        assert balance._name == "balance"

    def test_indicator_exists(self):
        """测试indicator表存在"""
        assert isinstance(indicator, _TableProxy)
        assert indicator._name == "indicator"


class TestPositionProxy:
    """测试 PositionProxy 持仓代理"""

    def test_total_amount(self):
        """测试持股数量"""
        mock_pos = MagicMock()
        mock_pos.size = 1000
        mock_data = MagicMock()
        mock_data.close = [50.0]

        pos = PositionProxy(mock_pos, mock_data)
        assert pos.total_amount == 1000

    def test_value(self):
        """测试持仓市值"""
        mock_pos = MagicMock()
        mock_pos.size = 1000
        mock_data = MagicMock()
        mock_data.close = [50.0]

        pos = PositionProxy(mock_pos, mock_data)
        assert pos.value == 50000.0

    def test_price(self):
        """测试成本价"""
        mock_pos = MagicMock()
        mock_pos.size = 1000
        mock_pos.price = 45.0
        mock_data = MagicMock()

        pos = PositionProxy(mock_pos, mock_data)
        assert pos.price == 45.0

    def test_closeable_amount(self):
        """测试可卖数量"""
        mock_pos = MagicMock()
        mock_pos.size = 1000
        mock_data = MagicMock()

        pos = PositionProxy(mock_pos, mock_data)
        assert pos.closeable_amount == 1000


class TestPortfolioProxy:
    """测试 PortfolioProxy 组合代理"""

    def test_positions_property(self):
        """测试持仓属性"""
        mock_data = MagicMock()
        mock_data._name = "600519.XSHG"
        mock_data.close = [100.0]

        mock_strategy = MagicMock()
        mock_strategy.datas = [mock_data]
        mock_strategy.getposition.return_value = MagicMock(size=100)

        portfolio = PortfolioProxy(mock_strategy)
        positions = portfolio.positions
        assert isinstance(positions, dict)

    def test_total_value_property(self):
        """测试总资产属性"""
        mock_strategy = MagicMock()
        mock_strategy.broker.getvalue.return_value = 1000000.0

        portfolio = PortfolioProxy(mock_strategy)
        assert portfolio.total_value == 1000000.0

    def test_available_cash_property(self):
        """测试可用现金属性"""
        mock_strategy = MagicMock()
        mock_strategy.broker.getcash.return_value = 500000.0

        portfolio = PortfolioProxy(mock_strategy)
        assert portfolio.available_cash == 500000.0

    def test_market_value_property(self):
        """测试持仓市值属性"""
        mock_strategy = MagicMock()
        mock_strategy.broker.getvalue.return_value = 1000000.0
        mock_strategy.broker.getcash.return_value = 400000.0

        portfolio = PortfolioProxy(mock_strategy)
        assert portfolio.market_value == 600000.0


class TestCurrentDataEntry:
    """测试 _CurrentDataEntry 当前数据条目"""

    def test_single_code(self):
        """测试单个代码"""
        entry = _CurrentDataEntry("600519.XSHG")
        assert entry.codes == ["600519.XSHG"]
        assert entry._single is True

    def test_multiple_codes(self):
        """测试多个代码"""
        entry = _CurrentDataEntry(["600519.XSHG", "000001.XSHE"])
        assert len(entry.codes) == 2
        assert entry._single is False

    def test_last_price_with_bt_strategy(self):
        """测试有策略时的最新价"""
        mock_strategy = MagicMock()
        mock_data = MagicMock()
        mock_data.close = [100.0]
        mock_strategy.datas = [mock_data]
        mock_data._name = "600519.XSHG"

        entry = _CurrentDataEntry("600519.XSHG", bt_strategy=mock_strategy)
        assert entry.last_price == 100.0

    def test_day_open(self):
        """测试开盘价"""
        mock_strategy = MagicMock()
        mock_data = MagicMock()
        mock_data.open = [98.0]
        mock_strategy.datas = [mock_data]
        mock_data._name = "600519.XSHG"

        entry = _CurrentDataEntry("600519.XSHG", bt_strategy=mock_strategy)
        assert entry.day_open == 98.0

    def test_high(self):
        """测试最高价"""
        mock_strategy = MagicMock()
        mock_data = MagicMock()
        mock_data.high = [105.0]
        mock_strategy.datas = [mock_data]
        mock_data._name = "600519.XSHG"

        entry = _CurrentDataEntry("600519.XSHG", bt_strategy=mock_strategy)
        assert entry.high == 105.0

    def test_low(self):
        """测试最低价"""
        mock_strategy = MagicMock()
        mock_data = MagicMock()
        mock_data.low = [95.0]
        mock_strategy.datas = [mock_data]
        mock_data._name = "600519.XSHG"

        entry = _CurrentDataEntry("600519.XSHG", bt_strategy=mock_strategy)
        assert entry.low == 95.0

    def test_volume(self):
        """测试成交量"""
        mock_strategy = MagicMock()
        mock_data = MagicMock()
        mock_data.volume = [1000000]
        mock_strategy.datas = [mock_data]
        mock_data._name = "600519.XSHG"

        entry = _CurrentDataEntry("600519.XSHG", bt_strategy=mock_strategy)
        assert entry.volume == 1000000


class TestCurrentDataProxy:
    """测试 _CurrentDataProxy 当前数据代理"""

    def test_getitem_single_code(self):
        """测试获取单个代码"""
        proxy = _CurrentDataProxy()
        entry = proxy["600519.XSHG"]
        assert isinstance(entry, _CurrentDataEntry)
        assert "600519.XSHG" in entry.codes

    def test_getitem_list_of_codes(self):
        """测试获取代码列表"""
        proxy = _CurrentDataProxy()
        entry = proxy[["600519.XSHG", "000001.XSHE"]]
        assert isinstance(entry, _CurrentDataEntry)

    def test_caching(self):
        """测试缓存"""
        proxy = _CurrentDataProxy()
        entry1 = proxy["600519.XSHG"]
        entry2 = proxy["600519.XSHG"]
        assert entry1 is entry2


class TestTickDataProxy:
    """测试 _TickDataProxy tick数据代理"""

    def test_basic_creation(self):
        """测试基本创建"""
        tick = _TickDataProxy("600519.XSHG")
        assert tick._code == "600519.XSHG"

    def test_current_property(self):
        """测试current属性"""
        mock_strategy = MagicMock()
        mock_data = MagicMock()
        mock_data.close = [100.0]
        mock_data._name = "600519.XSHG"
        mock_strategy.datas = [mock_data]

        tick = _TickDataProxy("600519.XSHG", bt_strategy=mock_strategy)
        assert tick.current == 100.0

    def test_last_price_property(self):
        """测试last_price属性"""
        mock_strategy = MagicMock()
        mock_data = MagicMock()
        mock_data.close = [100.0]
        mock_data._name = "600519.XSHG"
        mock_strategy.datas = [mock_data]

        tick = _TickDataProxy("600519.XSHG", bt_strategy=mock_strategy)
        assert tick.last_price == 100.0

    def test_day_open_property(self):
        """测试day_open属性"""
        mock_strategy = MagicMock()
        mock_data = MagicMock()
        mock_data.open = [98.0]
        mock_data._name = "600519.XSHG"
        mock_strategy.datas = [mock_data]

        tick = _TickDataProxy("600519.XSHG", bt_strategy=mock_strategy)
        assert tick.day_open == 98.0
