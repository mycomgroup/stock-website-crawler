# Analysis V2 设计文档

## 一、背景与目标

### 1.1 当前问题

`analysis` 模块存在以下核心问题：

| 问题类别 | 具体问题 | 影响 |
|----------|----------|------|
| **架构分层** | signals/risk 依赖 factors，形成跨层依赖 | 无法独立使用各模块 |
| **功能重叠** | `indicators/` 与 `factors/technical.py` 重复实现 30+ 技术指标 | 代码冗余、维护困难 |
| **数据获取分散** | `_get_daily_ohlcv`、`_fetch_ohlcv`、`_history_adapter` 三处重复实现 | 接口不统一 |
| **紧耦合** | 多处直接 `from jk2bt.data.sources import get_adapter` | 无法独立抽取为库 |
| **重复代码** | RSI/KDJ/MACD 计算在多文件重复、`safe_divide` 多处定义 | 维护成本高 |
| **类型不完整** | 大量函数缺少类型注解 | 可读性差、IDE支持弱 |
| **错误处理宽泛** | `except Exception` 捕获所有异常 | 问题难以定位 |

### 1.2 设计目标

1. **独立性**: 模块可独立使用，不依赖 `jk2bt.data`
2. **解耦**: 通过数据接口抽象，实现计算逻辑与数据获取分离
3. **统一**: 统一技术指标实现、数据获取接口
4. **类型安全**: 完整的类型注解
5. **可测试**: 纯函数易于单元测试

---

## 二、架构设计

### 2.1 目录结构

```
analysis_v2/
├── __init__.py                    # 顶层入口，导出公共API
├── DESIGN.md                      # 本设计文档
│
├── core/                          # 核心基础设施（无外部依赖）
│   ├── __init__.py
│   ├── types.py                   # 类型定义、数据结构
│   ├── interface.py               # 数据源抽象接口
│   ├── indicators.py              # 纯技术指标计算函数
│   └── utils.py                   # 工具函数（safe_divide等）
│
├── data/                          # 数据适配器（依赖 jk2bt.data）
│   ├── __init__.py
│   ├── adapter.py                 # DataSource 实现，对接 jk2bt.data
│   └── fetcher.py                 # 统一数据获取函数
│
├── factors/                       # 因子计算（依赖 core + data）
│   ├── __init__.py
│   ├── base.py                    # 因子注册表、缓存
│   ├── registry.py                # 因子注册与别名管理
│   ├── valuation.py               # 估值因子
│   ├── technical.py               # 技术因子（调用 core.indicators）
│   ├── fundamentals.py            # 财务因子
│   ├── growth.py                  # 成长因子
│   ├── quality.py                 # 质量因子
│   ├── barra.py                   # Barra风格因子
│   ├── custom.py                  # 自定义因子
│   └── preprocess.py              # 因子预处理
│
├── signals/                       # 信号检测（依赖 core）
│   ├── __init__.py
│   ├── base.py                    # 信号基类、检测器
│   ├── cross.py                   # 交叉信号
│   ├── divergence.py              # 背离信号
│   ├── breakthrough.py            # 突破信号
│   ├── extreme.py                 # 极值信号
│   ├── rsrs.py                    # RSRS择时
│   └── sentiment.py               # 市场情绪
│
└── risk/                          # 风险管理（依赖 core）
    ├── __init__.py
    ├── volatility.py              # 波动率风控
    ├── drawdown.py                # 回撤风控
    └── position.py                # 仓位计算
```

### 2.2 分层依赖关系

```
┌─────────────────────────────────────────────────────────┐
│                      使用者代码                          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  factors/    signals/    risk/                           │
│  (因子计算)  (信号检测)  (风控管理)                        │
└─────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │  core/   │  │  data/   │  │ (可选)   │
        │ 纯计算    │  │ 数据适配  │  │ 缓存等   │
        └──────────┘  └──────────┘  └──────────┘
              │             │
              │             ▼
              │      ┌──────────────┐
              │      │  jk2bt.data  │
              │      └──────────────┘
              │
              ▼
        独立可测试
        (不依赖外部)
```

### 2.3 模块职责

| 模块 | 职责 | 依赖 | 可独立使用 |
|------|------|------|------------|
| `core/` | 纯计算逻辑、类型定义、接口抽象 | 无 | ✅ |
| `data/` | 对接 jk2bt.data，实现数据获取 | jk2bt.data | ❌ |
| `factors/` | 选股因子计算 | core, data | ❌ |
| `signals/` | 择时信号检测 | core | ✅ (注入数据) |
| `risk/` | 风控计算 | core | ✅ (注入数据) |

---

## 三、核心模块设计

### 3.1 core/types.py - 类型定义

```python
from typing import TypedDict, Literal, Optional
import pandas as pd

class OHLCV(TypedDict):
    """标准OHLCV数据结构"""
    date: pd.Timestamp
    open: float
    high: float
    low: float
    close: float
    volume: float

class IndicatorResult(TypedDict):
    """指标计算结果"""
    value: float
    status: Literal["success", "insufficient_data", "error"]
    message: Optional[str]

class Signal(TypedDict):
    """信号结构"""
    date: pd.Timestamp
    signal_type: str
    direction: Literal["buy", "sell", "hold"]
    strength: float
    metadata: dict
```

### 3.2 core/interface.py - 数据源接口

```python
from abc import ABC, abstractmethod
from typing import Union, List, Optional
import pandas as pd
from datetime import datetime

class DataSource(ABC):
    """数据源抽象接口 - 核心解耦层"""
    
    @abstractmethod
    def get_ohlcv(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        count: Optional[int] = None
    ) -> pd.DataFrame:
        """获取OHLCV数据"""
        pass
    
    @abstractmethod
    def get_ohlcv_batch(
        self,
        symbols: List[str],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        count: Optional[int] = None
    ) -> dict[str, pd.DataFrame]:
        """批量获取OHLCV数据"""
        pass
    
    @abstractmethod
    def get_index_daily(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """获取指数日线数据"""
        pass
    
    @abstractmethod
    def get_valuation(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """获取估值数据 (PE/PB/市值等)"""
        pass
    
    @abstractmethod
    def get_financial(
        self,
        symbol: str,
        table: str  # "income", "balance", "cashflow"
    ) -> pd.DataFrame:
        """获取财务数据"""
        pass
    
    @abstractmethod
    def get_index_components(self, index_symbol: str) -> List[str]:
        """获取指数成分股"""
        pass


class DataSourceContext:
    """数据源上下文管理器 - 支持依赖注入"""
    _instance: Optional[DataSource] = None
    
    @classmethod
    def set_data_source(cls, data_source: DataSource) -> None:
        """设置全局数据源"""
        cls._instance = data_source
    
    @classmethod
    def get_data_source(cls) -> DataSource:
        """获取当前数据源"""
        if cls._instance is None:
            raise RuntimeError("DataSource not initialized. Call set_data_source() first.")
        return cls._instance
    
    @classmethod
    def clear(cls) -> None:
        """清除数据源（用于测试）"""
        cls._instance = None
```

### 3.3 core/indicators.py - 纯技术指标计算

```python
"""
纯技术指标计算模块

设计原则:
1. 所有函数只接收 DataFrame/Series，不负责数据获取
2. 返回计算结果，不负责数据存储
3. 无外部依赖，可独立测试
"""
from typing import Optional
import pandas as pd
import numpy as np

def ma(series: pd.Series, window: int) -> pd.Series:
    """移动平均线"""
    return series.rolling(window=window).mean()

def ema(series: pd.Series, window: int) -> pd.Series:
    """指数移动平均线"""
    return series.ewm(span=window, adjust=False).mean()

def macd(
    close: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """MACD指标"""
    ema_fast = ema(close, fast)
    ema_slow = ema(close, slow)
    dif = ema_fast - ema_slow
    dea = ema(dif, signal)
    hist = (dif - dea) * 2
    return dif, dea, hist

def rsi(close: pd.Series, window: int = 14) -> pd.Series:
    """RSI相对强弱指标"""
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def kdj(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    n: int = 9,
    m1: int = 3,
    m2: int = 3
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """KDJ随机指标"""
    low_n = low.rolling(window=n).min()
    high_n = high.rolling(window=n).max()
    rsv = (close - low_n) / (high_n - low_n) * 100
    k = rsv.ewm(alpha=1/m1, adjust=False).mean()
    d = k.ewm(alpha=1/m2, adjust=False).mean()
    j = 3 * k - 2 * d
    return k, d, j

def boll(
    close: pd.Series,
    window: int = 20,
    num_std: int = 2
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """布林带"""
    mid = ma(close, window)
    std = close.rolling(window=window).std()
    upper = mid + num_std * std
    lower = mid - num_std * std
    return upper, mid, lower

def atr(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    window: int = 14
) -> pd.Series:
    """平均真实波幅"""
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return ma(tr, window)

def obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """能量潮指标 - 向量化实现"""
    direction = np.sign(close.diff())
    direction.iloc[0] = 1  # 第一个设为正
    return (volume * direction).cumsum()

# ... 其他30+指标
```

### 3.4 core/utils.py - 工具函数

```python
from typing import Union
import numpy as np
import pandas as pd

def safe_divide(
    a: Union[pd.Series, np.ndarray, float],
    b: Union[pd.Series, np.ndarray, float],
    fill_value: float = np.nan
) -> Union[pd.Series, np.ndarray, float]:
    """安全除法，避免除零错误"""
    with np.errstate(divide='ignore', invalid='ignore'):
        result = np.divide(a, b)
        if isinstance(result, np.ndarray):
            result = np.where(np.isfinite(result), result, fill_value)
        elif isinstance(result, pd.Series):
            result = result.where(np.isfinite(result), fill_value)
        elif not np.isfinite(result):
            result = fill_value
    return result

def validate_ohlcv(df: pd.DataFrame) -> bool:
    """验证OHLCV数据格式"""
    required_cols = {'open', 'high', 'low', 'close', 'volume'}
    return required_cols.issubset(set(df.columns.str.lower()))

def extract_ohlcv(df: pd.DataFrame) -> dict[str, pd.Series]:
    """从DataFrame提取OHLCV列，处理列名差异"""
    col_map = {}
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in ['open', 'high', 'low', 'close', 'volume']:
            col_map[col_lower] = df[col]
    return col_map

def normalize_date(date: Union[str, pd.Timestamp, datetime]) -> pd.Timestamp:
    """统一日期格式"""
    if isinstance(date, str):
        return pd.Timestamp(date)
    return pd.Timestamp(date)
```

---

## 四、数据适配层设计

### 4.1 data/adapter.py - 数据源适配器

```python
"""
数据源适配器 - 对接 jk2bt.data

此模块是唯一依赖 jk2bt.data 的地方，
其他模块通过 DataSource 接口使用数据。
"""
from typing import List, Optional
import pandas as pd
from datetime import datetime

from ..core.interface import DataSource

class Jk2btDataAdapter(DataSource):
    """聚宽风格数据适配器"""
    
    def __init__(self):
        from jk2bt.data.sources import get_adapter
        self._adapter = get_adapter()
    
    def get_ohlcv(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        count: Optional[int] = None
    ) -> pd.DataFrame:
        """获取OHLCV数据"""
        from jk2bt.data.market.stock import get_stock_daily
        df = get_stock_daily(symbol, start_date=start_date, end_date=end_date, count=count)
        return self._normalize_ohlcv(df)
    
    def get_ohlcv_batch(
        self,
        symbols: List[str],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        count: Optional[int] = None
    ) -> dict[str, pd.DataFrame]:
        """批量获取OHLCV数据"""
        result = {}
        for symbol in symbols:
            try:
                result[symbol] = self.get_ohlcv(symbol, start_date, end_date, count)
            except Exception as e:
                result[symbol] = pd.DataFrame()
        return result
    
    def get_index_daily(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """获取指数日线"""
        return self._adapter.get_index_daily(symbol, start_date=start_date, end_date=end_date)
    
    def get_valuation(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """获取估值数据"""
        return self._adapter.get_stock_valuation_baidu(
            symbol,
            indicators=['pe_ratio', 'pb_ratio', 'market_cap', 'circulating_market_cap']
        )
    
    def get_financial(
        self,
        symbol: str,
        table: str
    ) -> pd.DataFrame:
        """获取财务数据"""
        table_map = {
            "income": "get_income_statement",
            "balance": "get_balance_sheet",
            "cashflow": "get_cashflow_statement"
        }
        method = getattr(self._adapter, table_map.get(table, ""), None)
        if method:
            return method(symbol)
        raise ValueError(f"Unknown financial table: {table}")
    
    def get_index_components(self, index_symbol: str) -> List[str]:
        """获取指数成分股"""
        return self._adapter.get_index_stocks(index_symbol)
    
    def _normalize_ohlcv(self, df: pd.DataFrame) -> pd.DataFrame:
        """标准化OHLCV列名"""
        df = df.copy()
        df.columns = df.columns.str.lower()
        return df


def init_data_source() -> None:
    """初始化默认数据源"""
    from ..core.interface import DataSourceContext
    DataSourceContext.set_data_source(Jk2btDataAdapter())
```

### 4.2 data/fetcher.py - 统一数据获取

```python
"""
统一数据获取函数

提供便捷的数据获取接口，内部使用 DataSourceContext
"""
from typing import List, Optional, Union
import pandas as pd
from datetime import datetime

from ..core.interface import DataSourceContext

def get_ohlcv(
    symbol: str,
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None,
    count: Optional[int] = None
) -> pd.DataFrame:
    """获取单只股票OHLCV数据"""
    ds = DataSourceContext.get_data_source()
    if isinstance(start_date, str):
        start_date = pd.Timestamp(start_date)
    if isinstance(end_date, str):
        end_date = pd.Timestamp(end_date)
    return ds.get_ohlcv(symbol, start_date, end_date, count)

def get_ohlcv_batch(
    symbols: List[str],
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None,
    count: Optional[int] = None
) -> dict[str, pd.DataFrame]:
    """批量获取OHLCV数据"""
    ds = DataSourceContext.get_data_source()
    if isinstance(start_date, str):
        start_date = pd.Timestamp(start_date)
    if isinstance(end_date, str):
        end_date = pd.Timestamp(end_date)
    return ds.get_ohlcv_batch(symbols, start_date, end_date, count)

def get_index_daily(
    symbol: str,
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None
) -> pd.DataFrame:
    """获取指数日线数据"""
    ds = DataSourceContext.get_data_source()
    return ds.get_index_daily(symbol, start_date, end_date)

def get_valuation(
    symbol: str,
    start_date: Optional[Union[str, datetime]] = None,
    end_date: Optional[Union[str, datetime]] = None
) -> pd.DataFrame:
    """获取估值数据"""
    ds = DataSourceContext.get_data_source()
    return ds.get_valuation(symbol, start_date, end_date)
```

---

## 五、因子模块设计

### 5.1 factors/base.py - 因子基类

```python
"""
因子计算基类与注册表
"""
from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Optional, Any
import pandas as pd

from ..core.interface import DataSourceContext

class FactorBase(ABC):
    """因子基类"""
    
    name: str = ""
    category: str = ""
    description: str = ""
    
    @abstractmethod
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        """计算因子值"""
        pass
    
    @property
    def data_source(self):
        """获取数据源"""
        return DataSourceContext.get_data_source()


class FactorRegistry:
    """因子注册表"""
    
    _factors: Dict[str, FactorBase] = {}
    _aliases: Dict[str, str] = {}
    
    @classmethod
    def register(cls, name: str, aliases: Optional[List[str]] = None):
        """注册装饰器"""
        def decorator(factor_class: type) -> type:
            factor = factor_class()
            cls._factors[name] = factor
            if aliases:
                for alias in aliases:
                    cls._aliases[alias] = name
            return factor_class
        return decorator
    
    @classmethod
    def get(cls, name: str) -> Optional[FactorBase]:
        """获取因子"""
        name = cls._aliases.get(name, name)
        return cls._factors.get(name)
    
    @classmethod
    def list_factors(cls, category: Optional[str] = None) -> List[str]:
        """列出所有因子"""
        factors = list(cls._factors.keys())
        if category:
            factors = [f for f in factors if cls._factors[f].category == category]
        return factors


def compute_factor(
    factor_name: str,
    symbol: str,
    end_date: Optional[str] = None,
    **kwargs
) -> pd.Series:
    """计算单个因子"""
    factor = FactorRegistry.get(factor_name)
    if factor is None:
        raise ValueError(f"Unknown factor: {factor_name}")
    return factor.compute(symbol, end_date, **kwargs)


def compute_factors(
    factor_names: List[str],
    symbol: str,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """计算多个因子"""
    result = {}
    for name in factor_names:
        try:
            result[name] = compute_factor(name, symbol, end_date)
        except Exception as e:
            result[name] = pd.Series(dtype=float)
    return pd.DataFrame(result)
```

### 5.2 factors/technical.py - 技术因子示例

```python
"""
技术因子 - 基于 core.indicators 实现
"""
import pandas as pd
from typing import Optional

from .base import FactorBase, FactorRegistry
from ..core import indicators
from ..data.fetcher import get_ohlcv

@FactorRegistry.register("ma_5", aliases=["MA5", "ma5"])
class MA5Factor(FactorBase):
    name = "ma_5"
    category = "technical"
    description = "5日移动平均线"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.Series:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.Series(dtype=float)
        return indicators.ma(df['close'], 5)


@FactorRegistry.register("macd", aliases=["MACD"])
class MACDFactor(FactorBase):
    name = "macd"
    category = "technical"
    description = "MACD指标"
    
    def compute(self, symbol: str, end_date: Optional[str] = None, **kwargs) -> pd.DataFrame:
        df = get_ohlcv(symbol, end_date=end_date, count=100)
        if df.empty:
            return pd.DataFrame()
        
        dif, dea, hist = indicators.macd(df['close'])
        return pd.DataFrame({
            'macd_dif': dif,
            'macd_dea': dea,
            'macd_hist': hist
        })
```

---

## 六、信号模块设计

### 6.1 signals/base.py - 信号基类

```python
"""
信号检测基类
"""
from abc import ABC, abstractmethod
from typing import Optional, List
import pandas as pd

from ..core.interface import DataSource

class SignalBase(ABC):
    """信号基类"""
    
    name: str = ""
    signal_type: str = ""
    description: str = ""
    
    def __init__(self, data_source: Optional[DataSource] = None):
        self._data_source = data_source
    
    @abstractmethod
    def detect(self, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        """检测信号"""
        pass
    
    @property
    def data_source(self) -> DataSource:
        if self._data_source is None:
            from ..core.interface import DataSourceContext
            return DataSourceContext.get_data_source()
        return self._data_source


class SignalDetector:
    """信号检测器"""
    
    def __init__(self):
        self._signals: dict[str, SignalBase] = {}
    
    def register(self, signal: SignalBase) -> None:
        self._signals[signal.name] = signal
    
    def detect(self, signal_name: str, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        signal = self._signals.get(signal_name)
        if signal is None:
            raise ValueError(f"Unknown signal: {signal_name}")
        return signal.detect(symbol, end_date)
    
    def detect_all(self, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        results = []
        for name, signal in self._signals.items():
            try:
                df = signal.detect(symbol, end_date)
                if not df.empty:
                    df['signal_name'] = name
                    results.append(df)
            except Exception:
                pass
        if results:
            return pd.concat(results, ignore_index=True)
        return pd.DataFrame()
```

### 6.2 signals/cross.py - 交叉信号示例

```python
"""
交叉信号检测 - 依赖 core.indicators，不依赖 factors
"""
import pandas as pd
from typing import Optional

from .base import SignalBase
from ..core import indicators
from ..data.fetcher import get_ohlcv

class MACrossSignal(SignalBase):
    """均线交叉信号"""
    
    name = "ma_cross"
    signal_type = "cross"
    description = "均线交叉信号"
    
    def __init__(self, fast: int = 5, slow: int = 20, data_source=None):
        super().__init__(data_source)
        self.fast = fast
        self.slow = slow
    
    def detect(self, symbol: str, end_date: Optional[str] = None) -> pd.DataFrame:
        df = get_ohlcv(symbol, end_date=end_date, count=self.slow + 10)
        if df.empty:
            return pd.DataFrame()
        
        fast_ma = indicators.ma(df['close'], self.fast)
        slow_ma = indicators.ma(df['close'], self.slow)
        
        cross_up = (fast_ma > slow_ma) & (fast_ma.shift(1) <= slow_ma.shift(1))
        cross_down = (fast_ma < slow_ma) & (fast_ma.shift(1) >= slow_ma.shift(1))
        
        signals = []
        for i in range(len(df)):
            if cross_up.iloc[i]:
                signals.append({
                    'date': df.index[i],
                    'type': 'ma_cross_up',
                    'direction': 'buy',
                    'strength': 1.0
                })
            elif cross_down.iloc[i]:
                signals.append({
                    'date': df.index[i],
                    'type': 'ma_cross_down',
                    'direction': 'sell',
                    'strength': 1.0
                })
        
        return pd.DataFrame(signals)
```

---

## 七、风控模块设计

### 7.1 risk/volatility.py - 波动率风控

```python
"""
波动率风控 - 依赖 core.indicators，不依赖 factors
"""
import pandas as pd
import numpy as np
from typing import Optional

from ..core import indicators
from ..data.fetcher import get_ohlcv

def compute_volatility(
    symbol: str,
    window: int = 20,
    end_date: Optional[str] = None
) -> dict:
    """计算波动率指标"""
    df = get_ohlcv(symbol, end_date=end_date, count=window + 10)
    if df.empty or len(df) < window:
        return {'volatility': np.nan, 'atr': np.nan}
    
    close = df['close']
    high = df['high']
    low = df['low']
    
    returns = close.pct_change()
    volatility = returns.rolling(window).std().iloc[-1] * np.sqrt(252)
    atr = indicators.atr(high, low, close, window).iloc[-1]
    
    return {
        'volatility': volatility,
        'atr': atr,
        'atr_ratio': atr / close.iloc[-1] if close.iloc[-1] > 0 else np.nan
    }


def compute_volatility_adjusted_position(
    symbol: str,
    target_volatility: float = 0.15,
    end_date: Optional[str] = None
) -> float:
    """波动率调整仓位"""
    vol_data = compute_volatility(symbol, end_date=end_date)
    current_vol = vol_data['volatility']
    
    if np.isnan(current_vol) or current_vol == 0:
        return 0.0
    
    position = target_volatility / current_vol
    return min(max(position, 0.0), 1.0)  # 限制在 0-1 之间
```

---

## 八、迁移计划

### 8.1 阶段一：基础设施（1-2天）

| 任务 | 文件 | 来源 |
|------|------|------|
| 创建类型定义 | `core/types.py` | 新建 |
| 创建数据接口 | `core/interface.py` | 新建 |
| 提取技术指标 | `core/indicators.py` | `indicators/technical_analysis.py` + `factors/technical.py` |
| 提取工具函数 | `core/utils.py` | `signals/base.py` + `factors/base.py` |
| 创建数据适配器 | `data/adapter.py` | 新建，对接 `jk2bt.data` |
| 创建数据获取函数 | `data/fetcher.py` | 统一 `_get_daily_ohlcv` |

### 8.2 阶段二：因子模块（2-3天）

| 任务 | 文件 | 来源 |
|------|------|------|
| 创建因子基类 | `factors/base.py` | `analysis/factors/base.py` 重构 |
| 创建因子注册表 | `factors/registry.py` | `analysis/factors/base.py` 提取 |
| 迁移技术因子 | `factors/technical.py` | `analysis/factors/technical.py` 简化 |
| 迁移估值因子 | `factors/valuation.py` | `analysis/factors/valuation.py` |
| 迁移财务因子 | `factors/fundamentals.py` | `analysis/factors/fundamentals.py` |
| 迁移预处理 | `factors/preprocess.py` | `analysis/factors/preprocess.py` |

### 8.3 阶段三：信号模块（1-2天）

| 任务 | 文件 | 来源 |
|------|------|------|
| 创建信号基类 | `signals/base.py` | `analysis/signals/base.py` 重构 |
| 迁移交叉信号 | `signals/cross.py` | `analysis/signals/cross.py` |
| 迁移背离信号 | `signals/divergence.py` | `analysis/signals/divergence.py` |
| 迁移突破信号 | `signals/breakthrough.py` | `analysis/signals/breakthrough.py` |
| 迁移RSRS信号 | `signals/rsrs.py` | `analysis/signals/rsrs.py` |

### 8.4 阶段四：风控模块（1天）

| 任务 | 文件 | 来源 |
|------|------|------|
| 迁移波动率风控 | `risk/volatility.py` | `analysis/risk/volatility.py` |
| 迁移回撤风控 | `risk/drawdown.py` | `analysis/risk/drawdown.py` |
| 迁移仓位计算 | `risk/position.py` | `analysis/risk/position.py` |

### 8.5 阶段五：测试与文档（1-2天）

| 任务 | 说明 |
|------|------|
| 单元测试 | 为 `core/` 模块编写测试 |
| 集成测试 | 验证数据流正确性 |
| API文档 | 编写使用文档 |
| 示例代码 | 提供使用示例 |

---

## 九、使用示例

### 9.1 初始化

```python
from analysis_v2.data.adapter import init_data_source

# 初始化数据源（只需一次）
init_data_source()
```

### 9.2 计算因子

```python
from analysis_v2.factors import compute_factor, compute_factors

# 计算单个因子
ma5 = compute_factor("ma_5", "000001.SZ")
print(ma5)

# 计算多个因子
factors = compute_factors(["ma_5", "rsi_14", "macd"], "000001.SZ")
print(factors.tail())
```

### 9.3 检测信号

```python
from analysis_v2.signals import SignalDetector, MACrossSignal

# 创建检测器
detector = SignalDetector()
detector.register(MACrossSignal(fast=5, slow=20))

# 检测信号
signals = detector.detect("ma_cross", "000001.SZ")
print(signals)
```

### 9.4 风控计算

```python
from analysis_v2.risk import compute_volatility, compute_volatility_adjusted_position

# 计算波动率
vol = compute_volatility("000001.SZ")
print(f"年化波动率: {vol['volatility']:.2%}")

# 计算建议仓位
position = compute_volatility_adjusted_position("000001.SZ", target_volatility=0.15)
print(f"建议仓位: {position:.2%}")
```

### 9.5 使用自定义数据源（测试场景）

```python
from analysis_v2.core.interface import DataSource, DataSourceContext
from analysis_v2.signals import MACrossSignal

# 自定义测试数据源
class MockDataSource(DataSource):
    def get_ohlcv(self, symbol, start_date=None, end_date=None, count=None):
        # 返回测试数据
        return pd.DataFrame({
            'close': [10, 11, 12, 11, 10, 9, 10, 11, 12, 13]
        })

# 注入数据源
DataSourceContext.set_data_source(MockDataSource())

# 现在可以独立测试
signal = MACrossSignal()
result = signal.detect("TEST")
```

---

## 十、对比总结

| 维度 | V1 (analysis) | V2 (analysis_v2) |
|------|---------------|------------------|
| 数据依赖 | 紧耦合 `jk2bt.data` | 通过接口抽象，可替换 |
| 模块独立性 | signals/risk 依赖 factors | 模块独立，只依赖 core |
| 技术指标 | 3处重复实现 | 统一在 core.indicators |
| 数据获取 | 3个不同函数 | 统一在 data.fetcher |
| 类型安全 | 不完整 | 完整类型注解 |
| 可测试性 | 需要真实数据源 | 可注入 Mock 数据源 |
| 错误处理 | 宽泛捕获 | 结构化错误处理 |

---

## 十一、当前完成状态

### ✅ 已完成

| 模块 | 文件 | 状态 |
|------|------|------|
| **core/** | `types.py` | ✅ 完成 - 类型定义 |
| | `interface.py` | ✅ 完成 - 数据源接口 |
| | `indicators.py` | ✅ 完成 - 30+技术指标纯函数 |
| | `utils.py` | ✅ 完成 - 工具函数 |
| **data/** | `adapter.py` | ✅ 完成 - 数据适配器 |
| | `fetcher.py` | ✅ 完成 - 统一数据获取 |
| **factors/** | `base.py` | ✅ 完成 - 因子基类与注册表 |
| | `technical.py` | ✅ 完成 - 20+技术因子 |
| **signals/** | `base.py` | ✅ 完成 - 信号基类与检测器 |
| | `cross.py` | ✅ 完成 - MA/MACD/RSI交叉信号 |
| | `breakthrough.py` | ✅ 完成 - 突破信号 |
| | `divergence.py` | ✅ 完成 - RSI/MACD背离信号 |
| | `extreme.py` | ✅ 完成 - KDJ/WR/CCI极值信号 |
| | `rsrs.py` | ✅ 完成 - RSRS择时信号 |
| **risk/** | `volatility.py` | ✅ 完成 - 波动率风控 |
| | `drawdown.py` | ✅ 完成 - 回撤风控 |
| | `position.py` | ✅ 完成 - 仓位计算 |

### 📋 待完成（后续迁移）

| 模块 | 来源 | 说明 |
|------|------|------|
| **factors/valuation.py** | `analysis/factors/valuation.py` | 估值因子（PE/PB/市值） |
| **factors/fundamentals.py** | `analysis/factors/fundamentals.py` | 财务因子 |
| **factors/growth.py** | `analysis/factors/growth.py` | 成长因子 |
| **factors/quality.py** | `analysis/factors/quality.py` | 质量因子 |
| **factors/barra.py** | `analysis/factors/barra.py` | Barra风格因子 |
| **factors/preprocess.py** | `analysis/factors/preprocess.py` | 因子预处理 |
| **signals/sentiment.py** | `analysis/signals/sentiment.py` | 市场情绪信号 |
| **测试用例** | 新建 | 单元测试和集成测试 |

---

## 十二、风险与注意事项

1. **兼容性**: V2 不保证与 V1 完全兼容，需要逐步迁移
2. **数据格式**: V2 统一列名为小写，V1 可能存在大小写不一致
3. **缓存机制**: V2 暂不实现缓存，后续可扩展
4. **性能**: 初期优先保证正确性，后续可优化向量化计算