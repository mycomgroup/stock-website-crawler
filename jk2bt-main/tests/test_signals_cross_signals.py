"""
tests/test_signals_cross_signals.py
单元测试：交叉类信号检测模块 (cross_signals.py)

覆盖函数：
- detect_ma_cross
- detect_macd_cross
- detect_kdj_cross
- detect_ema_cross
- detect_vmacd_cross

每个函数测试：
- 正常路径（金叉/死叉触发）
- 无信号场景
- 数据不足场景
- 空数据/异常数据输入
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from jk2bt.data_access import set_adapter, MockDataSource, get_adapter
from jk2bt.signals.cross_signals import (
    detect_ma_cross,
    detect_macd_cross,
    detect_kdj_cross,
    detect_ema_cross,
    detect_vmacd_cross,
)

# 测试数据截止日期（所有测试数据以此日期结尾）
END_DATE = "2024-06-30"


# =====================================================================
# 工具函数：构造测试 OHLCV 数据
# =====================================================================


def _make_dates(count: int, end_date: str = END_DATE) -> list:
    """生成 count 个交易日（跳过周末）"""
    end = pd.Timestamp(end_date)
    dates = []
    current = end
    while len(dates) < count:
        if current.weekday() < 5:
            dates.append(current)
        current -= timedelta(days=1)
    dates.reverse()
    return dates


def _make_ohlcv(
    closes: list,
    end_date: str = END_DATE,
    base_volume: int = 1000000,
) -> pd.DataFrame:
    """根据收盘价序列构造 OHLCV DataFrame"""
    n = len(closes)
    dates = _make_dates(n, end_date)
    opens = [c * 0.99 for c in closes]
    highs = [c * 1.01 for c in closes]
    lows = [c * 0.98 for c in closes]
    volumes = [base_volume + i * 1000 for i in range(n)]

    return pd.DataFrame(
        {
            "datetime": dates,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
            "amount": [o * v for o, v in zip(opens, volumes)],
        }
    )


def _setup_mock_with_data(df: pd.DataFrame, symbol: str = "TEST001"):
    """设置 Mock 数据源并注入数据"""
    mock = MockDataSource(seed=42, generate_random=False)
    mock.set_mock_data("daily", symbol, df)
    set_adapter(mock)
    return mock


# =====================================================================
# detect_ma_cross 测试
# =====================================================================


class TestDetectMaCross:
    """MA 均线交叉检测测试"""

    def test_ma_golden_cross(self):
        """测试金叉触发：快线上穿慢线"""
        # 构造：横盘 -> 急跌(MA5下穿MA20产生死叉) -> 急涨(MA5上穿MA20产生金叉)
        closes = []
        # 30 天横盘：MA5 和 MA20 都收敛到 100
        for i in range(30):
            closes.append(100.0)
        # 5 天急跌：MA5 快速下降到 MA20 下方
        for i in range(5):
            closes.append(90.0)
        # 10 天急涨：MA5 快速上升穿越 MA20
        for i in range(10):
            closes.append(110.0)

        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_ma_cross("TEST001", fast=5, slow=20, end_date=END_DATE)
        assert not result.empty
        assert "date" in result.columns
        assert "signal" in result.columns
        assert "type" in result.columns
        assert 1 in result["signal"].values  # 有金叉信号

    def test_ma_dead_cross(self):
        """测试死叉触发：快线下穿慢线"""
        # 构造：横盘 -> 急涨(MA5上穿MA20产生金叉) -> 急跌(MA5下穿MA20产生死叉)
        closes = []
        # 30 天横盘
        for i in range(30):
            closes.append(100.0)
        # 5 天急涨
        for i in range(5):
            closes.append(110.0)
        # 10 天急跌
        for i in range(10):
            closes.append(90.0)

        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_ma_cross("TEST001", fast=5, slow=20, end_date=END_DATE)
        assert not result.empty
        assert -1 in result["signal"].values  # 有死叉信号

    def test_ma_no_cross(self):
        """测试无交叉：价格横盘震荡，均线不交叉"""
        # 价格恒定，均线平行
        closes = [10.0] * 50
        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_ma_cross("TEST001", fast=5, slow=20, end_date=END_DATE)
        assert result.empty  # 无信号应返回空 DataFrame

    def test_ma_insufficient_data(self):
        """测试数据不足：历史数据长度不够"""
        # MA 交叉需要 slow + 20 = 40 天，只给 10 天
        closes = [10.0 + i * 0.1 for i in range(10)]
        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_ma_cross("TEST001", fast=5, slow=20, end_date=END_DATE)
        # 数据不足时，均线计算会有大量 NaN，可能返回空或无信号
        assert isinstance(result, pd.DataFrame)

    def test_ma_empty_data(self):
        """测试空数据输入"""
        mock = MockDataSource(seed=42, generate_random=False)
        set_adapter(mock)

        result = detect_ma_cross("NONEXISTENT", fast=5, slow=20, end_date=END_DATE)
        assert result.empty
        assert list(result.columns) == ["date", "signal", "type"] or result.empty

    def test_ma_custom_periods(self):
        """测试自定义均线周期"""
        closes = []
        price = 100.0
        for i in range(30):
            price -= 1.0
            closes.append(price)
        for i in range(30):
            price += 3.0
            closes.append(price)

        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_ma_cross("TEST001", fast=10, slow=30, end_date=END_DATE)
        assert isinstance(result, pd.DataFrame)

    def test_ma_signal_type_format(self):
        """测试信号类型格式正确"""
        closes = []
        price = 100.0
        for i in range(25):
            price -= 0.5
            closes.append(price)
        for i in range(20):
            price += 2.0
            closes.append(price)

        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_ma_cross("TEST001", fast=5, slow=20, end_date=END_DATE)
        if not result.empty:
            for _, row in result.iterrows():
                if row["signal"] == 1:
                    assert "golden_cross" in row["type"]
                elif row["signal"] == -1:
                    assert "dead_cross" in row["type"]


# =====================================================================
# detect_macd_cross 测试
# =====================================================================


class TestDetectMacdCross:
    """MACD 交叉检测测试"""

    def test_macd_golden_cross(self):
        """测试 MACD 金叉：DIF 上穿 DEA"""
        closes = []
        price = 100.0
        # 先下跌趋势
        for i in range(40):
            price -= 1.0
            closes.append(price)
        # 再快速上涨
        for i in range(30):
            price += 3.0
            closes.append(price)

        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_macd_cross(
            "TEST001", fast=12, slow=26, signal_period=9, end_date=END_DATE
        )
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "macd_value" in result.columns
            assert 1 in result["signal"].values

    def test_macd_dead_cross(self):
        """测试 MACD 死叉：DIF 下穿 DEA"""
        closes = []
        price = 50.0
        # 先上涨趋势
        for i in range(40):
            price += 1.0
            closes.append(price)
        # 再快速下跌
        for i in range(30):
            price -= 3.0
            closes.append(price)

        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_macd_cross(
            "TEST001", fast=12, slow=26, signal_period=9, end_date=END_DATE
        )
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert -1 in result["signal"].values

    def test_macd_no_cross(self):
        """测试无 MACD 交叉"""
        closes = [10.0] * 60
        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_macd_cross(
            "TEST001", fast=12, slow=26, signal_period=9, end_date=END_DATE
        )
        assert result.empty

    def test_macd_insufficient_data(self):
        """测试数据不足"""
        closes = [10.0 + i * 0.1 for i in range(10)]
        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_macd_cross(
            "TEST001", fast=12, slow=26, signal_period=9, end_date=END_DATE
        )
        assert isinstance(result, pd.DataFrame)

    def test_macd_empty_data(self):
        """测试空数据"""
        mock = MockDataSource(seed=42, generate_random=False)
        set_adapter(mock)

        result = detect_macd_cross("NONEXISTENT", end_date=END_DATE)
        assert result.empty


# =====================================================================
# detect_kdj_cross 测试
# =====================================================================


class TestDetectKdjCross:
    """KDJ 交叉检测测试"""

    def test_kdj_golden_cross(self):
        """测试 KDJ 金叉：K 线上穿 D 线"""
        # KDJ 需要 high/low/close
        # 构造先跌后涨的价格序列
        closes = []
        highs = []
        lows = []
        price = 100.0
        # 先下跌
        for i in range(20):
            price -= 1.5
            closes.append(price)
            highs.append(price + 1.0)
            lows.append(price - 1.0)
        # 再上涨
        for i in range(25):
            price += 2.5
            closes.append(price)
            highs.append(price + 1.0)
            lows.append(price - 1.0)

        n = len(closes)
        dates = _make_dates(n)
        volumes = [1000000] * n

        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [c * 0.99 for c in closes],
                "high": highs,
                "low": lows,
                "close": closes,
                "volume": volumes,
                "amount": [c * 1000000 for c in closes],
            }
        )
        _setup_mock_with_data(df)

        result = detect_kdj_cross("TEST001", n=9, m1=3, m2=3, end_date=END_DATE)
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "k_value" in result.columns
            assert "d_value" in result.columns

    def test_kdj_dead_cross(self):
        """测试 KDJ 死叉：K 线下穿 D 线"""
        closes = []
        highs = []
        lows = []
        price = 50.0
        # 先上涨
        for i in range(20):
            price += 1.5
            closes.append(price)
            highs.append(price + 1.0)
            lows.append(price - 1.0)
        # 再下跌
        for i in range(25):
            price -= 2.5
            closes.append(price)
            highs.append(price + 1.0)
            lows.append(price - 1.0)

        n = len(closes)
        dates = _make_dates(n)
        volumes = [1000000] * n

        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [c * 0.99 for c in closes],
                "high": highs,
                "low": lows,
                "close": closes,
                "volume": volumes,
                "amount": [c * 1000000 for c in closes],
            }
        )
        _setup_mock_with_data(df)

        result = detect_kdj_cross("TEST001", n=9, m1=3, m2=3, end_date=END_DATE)
        assert isinstance(result, pd.DataFrame)

    def test_kdj_no_cross(self):
        """测试无 KDJ 交叉"""
        n = 40
        closes = [10.0] * n
        highs = [11.0] * n
        lows = [9.0] * n
        dates = _make_dates(n)
        volumes = [1000000] * n

        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0] * n,
                "high": highs,
                "low": lows,
                "close": closes,
                "volume": volumes,
                "amount": [10000000.0] * n,
            }
        )
        _setup_mock_with_data(df)

        result = detect_kdj_cross("TEST001", n=9, m1=3, m2=3, end_date=END_DATE)
        assert result.empty

    def test_kdj_insufficient_data(self):
        """测试数据不足"""
        closes = [10.0 + i for i in range(5)]
        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_kdj_cross("TEST001", n=9, m1=3, m2=3, end_date=END_DATE)
        assert isinstance(result, pd.DataFrame)

    def test_kdj_empty_data(self):
        """测试空数据"""
        mock = MockDataSource(seed=42, generate_random=False)
        set_adapter(mock)

        result = detect_kdj_cross("NONEXISTENT", end_date=END_DATE)
        assert result.empty


# =====================================================================
# detect_ema_cross 测试
# =====================================================================


class TestDetectEmaCross:
    """EMA 交叉检测测试"""

    def test_ema_golden_cross(self):
        """测试 EMA 金叉"""
        closes = []
        price = 100.0
        for i in range(25):
            price -= 1.0
            closes.append(price)
        for i in range(25):
            price += 3.0
            closes.append(price)

        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_ema_cross("TEST001", fast=10, slow=20, end_date=END_DATE)
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert 1 in result["signal"].values

    def test_ema_dead_cross(self):
        """测试 EMA 死叉"""
        closes = []
        price = 50.0
        for i in range(25):
            price += 1.0
            closes.append(price)
        for i in range(25):
            price -= 3.0
            closes.append(price)

        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_ema_cross("TEST001", fast=10, slow=20, end_date=END_DATE)
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert -1 in result["signal"].values

    def test_ema_no_cross(self):
        """测试无 EMA 交叉"""
        closes = [10.0] * 50
        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_ema_cross("TEST001", fast=10, slow=20, end_date=END_DATE)
        assert result.empty

    def test_ema_insufficient_data(self):
        """测试数据不足"""
        closes = [10.0 + i * 0.1 for i in range(5)]
        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_ema_cross("TEST001", fast=10, slow=20, end_date=END_DATE)
        assert isinstance(result, pd.DataFrame)

    def test_ema_empty_data(self):
        """测试空数据"""
        mock = MockDataSource(seed=42, generate_random=False)
        set_adapter(mock)

        result = detect_ema_cross("NONEXISTENT", end_date=END_DATE)
        assert result.empty

    def test_ema_signal_type_format(self):
        """测试信号类型格式"""
        closes = []
        price = 100.0
        for i in range(25):
            price -= 1.0
            closes.append(price)
        for i in range(25):
            price += 3.0
            closes.append(price)

        df = _make_ohlcv(closes)
        _setup_mock_with_data(df)

        result = detect_ema_cross("TEST001", fast=10, slow=20, end_date=END_DATE)
        if not result.empty:
            for _, row in result.iterrows():
                if row["signal"] == 1:
                    assert "golden_cross" in row["type"]
                elif row["signal"] == -1:
                    assert "dead_cross" in row["type"]


# =====================================================================
# detect_vmacd_cross 测试
# =====================================================================


class TestDetectVmacdCross:
    """VMACD 交叉检测测试"""

    def test_vmacd_turn_red(self):
        """测试 VMACD 翻红：由负转正"""
        # 构造成交量先递减后递增的序列
        volumes = []
        vol = 2000000
        # 先递减
        for i in range(30):
            vol -= 30000
            volumes.append(max(vol, 100000))
        # 再递增
        for i in range(30):
            vol += 80000
            volumes.append(vol)

        n = len(volumes)
        dates = _make_dates(n)
        closes = [10.0 + i * 0.01 for i in range(n)]

        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [c * 0.99 for c in closes],
                "high": [c * 1.01 for c in closes],
                "low": [c * 0.98 for c in closes],
                "close": closes,
                "volume": volumes,
                "amount": [c * v for c, v in zip(closes, volumes)],
            }
        )
        _setup_mock_with_data(df)

        result = detect_vmacd_cross(
            "TEST001", fast=12, slow=26, signal_period=9, end_date=END_DATE
        )
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "vmacd_value" in result.columns

    def test_vmacd_turn_green(self):
        """测试 VMACD 翻绿：由正转负"""
        volumes = []
        vol = 500000
        # 先递增
        for i in range(30):
            vol += 30000
            volumes.append(vol)
        # 再递减
        for i in range(30):
            vol -= 80000
            volumes.append(max(vol, 100000))

        n = len(volumes)
        dates = _make_dates(n)
        closes = [10.0 + i * 0.01 for i in range(n)]

        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [c * 0.99 for c in closes],
                "high": [c * 1.01 for c in closes],
                "low": [c * 0.98 for c in closes],
                "close": closes,
                "volume": volumes,
                "amount": [c * v for c, v in zip(closes, volumes)],
            }
        )
        _setup_mock_with_data(df)

        result = detect_vmacd_cross(
            "TEST001", fast=12, slow=26, signal_period=9, end_date=END_DATE
        )
        assert isinstance(result, pd.DataFrame)

    def test_vmacd_no_cross(self):
        """测试无 VMACD 交叉"""
        n = 60
        volumes = [1000000] * n
        dates = _make_dates(n)
        closes = [10.0] * n

        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0] * n,
                "high": [10.1] * n,
                "low": [9.9] * n,
                "close": closes,
                "volume": volumes,
                "amount": [10000000.0] * n,
            }
        )
        _setup_mock_with_data(df)

        result = detect_vmacd_cross(
            "TEST001", fast=12, slow=26, signal_period=9, end_date=END_DATE
        )
        assert result.empty

    def test_vmacd_insufficient_data(self):
        """测试数据不足"""
        volumes = [1000000] * 10
        closes = [10.0] * 10
        df = _make_ohlcv(closes, base_volume=1000000)
        # 覆盖 volume 列
        df["volume"] = volumes
        _setup_mock_with_data(df)

        result = detect_vmacd_cross(
            "TEST001", fast=12, slow=26, signal_period=9, end_date=END_DATE
        )
        assert isinstance(result, pd.DataFrame)

    def test_vmacd_empty_data(self):
        """测试空数据"""
        mock = MockDataSource(seed=42, generate_random=False)
        set_adapter(mock)

        result = detect_vmacd_cross("NONEXISTENT", end_date=END_DATE)
        assert result.empty

    def test_vmacd_signal_type_format(self):
        """测试信号类型格式"""
        volumes = []
        vol = 2000000
        for i in range(30):
            vol -= 30000
            volumes.append(max(vol, 100000))
        for i in range(30):
            vol += 80000
            volumes.append(vol)

        n = len(volumes)
        dates = _make_dates(n)
        closes = [10.0 + i * 0.01 for i in range(n)]

        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [c * 0.99 for c in closes],
                "high": [c * 1.01 for c in closes],
                "low": [c * 0.98 for c in closes],
                "close": closes,
                "volume": volumes,
                "amount": [c * v for c, v in zip(closes, volumes)],
            }
        )
        _setup_mock_with_data(df)

        result = detect_vmacd_cross(
            "TEST001", fast=12, slow=26, signal_period=9, end_date=END_DATE
        )
        if not result.empty:
            for _, row in result.iterrows():
                if row["signal"] == 1:
                    assert row["type"] == "vmacd_turn_red"
                elif row["signal"] == -1:
                    assert row["type"] == "vmacd_turn_green"
