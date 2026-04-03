# 技术指标系统设计文档

## 一、架构总览

```
src/
├── factors/                    # 因子模块（连续值，选股打分用）
│   ├── technical.py           # 技术因子 ✅已有基础
│   ├── fundamentals.py        # 财务因子 ✅已有
│   ├── valuation.py           # 估值因子 ✅已有
│   ├── indicators.py          # 指标因子 ✅新实现
│   └── ...
│
├── signals/                    # 信号模块（离散事件，择时用）❌需新建
│   ├── __init__.py
│   ├── cross_signals.py       # 交叉类信号
│   ├── breakthrough_signals.py # 突破类信号
│   ├── extreme_signals.py     # 极值类信号
│   └── divergence_signals.py  # 背离类信号
│
├── risk/                       # 风控模块（风险度量，仓位控制用）❌需新建
│   ├── __init__.py
│   ├── volatility.py          # 波动率风控
│   ├── drawdown.py            # 回撤风控
│   └── position_sizing.py     # 仓位计算
│
└── indicators/                 # 指标计算层（底层计算）
    ├── fields.py              # 指标字段映射 ✅已有
    ├── rsrs.py                # RSRS指标 ✅已有
    └── market_sentiment.py    # 市场情绪 ✅已有
```

---

## 二、因子模块完善清单

### 2.1 已实现的因子 ✅

| 类别 | 因子 | 状态 |
|------|------|------|
| **动量/趋势** | BIAS5/10/20/60 | ✅ technical.py |
| | ROC6/12/20/60/120 | ✅ technical.py |
| | EMAC10/20/26/60 | ✅ technical.py |
| | Price1M/3M/1Y | ✅ technical.py |
| | PLRC6/12/24 | ✅ technical.py |
| **反转/均值回归** | CCI10/15/20/88 | ✅ technical.py |
| | AR/BR/ARBR | ✅ technical.py |
| | bear_power/bull_power | ✅ technical.py |
| | CR20 | ✅ technical.py |
| **波动/风险** | ATR6/14 | ✅ technical.py |
| | Variance20/60/120 | ✅ technical.py |
| | boll_up/boll_down | ✅ technical.py |
| | VSTD10/20 | ✅ technical.py |
| **量能** | VOL5/10/20/60/120/240 | ✅ technical.py |
| | VROC6/12 | ✅ technical.py |
| | VMACD | ✅ technical.py (compute_macd) |
| | money_flow_20 | ✅ technical.py |
| | share_turnover_monthly | ✅ technical.py |
| **新增** | RSI6/12/14/24 | ✅ 新实现 |
| | KDJ_K/D/J | ✅ 新实现 |
| | zscore/zscore_slope | ✅ 新实现 |

### 2.2 需补充的因子 ⚠️

| 因子 | 说明 | 优先级 | 实现位置 |
|------|------|--------|----------|
| `boll_width` | 布林带宽度 | 高 | technical.py |
| `VOL_ratio` | 量比（当日量/均量） | 高 | technical.py |
| `amount_ratio` | 换手率比 | 中 | technical.py |
| `VWAP` | 成交量加权均价 | 中 | technical.py |
| `OBV` | 能量潮指标 | 低 | technical.py |

---

## 三、信号模块设计（需新建）

### 3.1 交叉类信号 `signals/cross_signals.py`

```python
"""
交叉类信号：从"没交叉"变"交叉"的状态变化

信号返回值：
- 1: 金叉/上穿（看涨信号）
- -1: 死叉/下穿（看跌信号）
- 0: 无交叉

输出格式：DataFrame
- date: 日期
- signal: 信号值 (1/-1/0)
- type: 信号类型 ('ma_golden_cross', 'ma_dead_cross', ...)
"""

def detect_ma_cross(symbol, fast=5, slow=20, **kwargs) -> pd.DataFrame:
    """MA金叉/死叉检测"""
    # 快线上穿慢线 = 金叉
    # 快线下穿慢线 = 死叉
    pass

def detect_macd_cross(symbol, **kwargs) -> pd.DataFrame:
    """MACD金叉/死叉检测"""
    # DIF上穿DEA = 金叉
    # DIF下穿DEA = 死叉
    pass

def detect_kdj_cross(symbol, n=9, m1=3, m2=3, **kwargs) -> pd.DataFrame:
    """KDJ金叉/死叉检测"""
    # K上穿D = 金叉
    # K下穿D = 死叉
    pass

def detect_vmacd_cross(symbol, **kwargs) -> pd.DataFrame:
    """VMACD翻红/翻绿检测"""
    # VMACD柱由负转正 = 翻红
    # VMACD柱由正转负 = 翻绿
    pass

def detect_emac_cross(symbol, fast=10, slow=20, **kwargs) -> pd.DataFrame:
    """EMAC交叉检测"""
    pass
```

### 3.2 突破类信号 `signals/breakthrough_signals.py`

```python
"""
突破类信号：从"没突破"变"突破"的状态变化

信号返回值：
- 1: 突破信号
- 0: 无突破
"""

def detect_price_breakout(symbol, window=20, **kwargs) -> pd.DataFrame:
    """价格突破N日新高/新低"""
    # 收盘价 > 过去N天最高价 = 突破新高
    # 收盘价 < 过去N天最低价 = 跌破新低
    pass

def detect_volume_breakout(symbol, window=20, multiplier=2.0, **kwargs) -> pd.DataFrame:
    """放量/缩量检测"""
    # 成交量 > N日均量 × multiplier = 放量
    # 成交量 < N日均量 / multiplier = 缩量
    pass

def detect_boll_breakout(symbol, window=20, num_std=2.0, **kwargs) -> pd.DataFrame:
    """布林带突破检测"""
    # 收盘价上穿布林上轨
    # 收盘价下穿布林下轨
    pass
```

### 3.3 极值类信号 `signals/extreme_signals.py`

```python
"""
极值类信号：从"正常"变"极端"的状态变化

信号返回值：
- 1: 进入超买区
- -1: 进入超卖区
- 0: 正常区域
"""

def detect_rsi_extreme(symbol, window=14, upper=70, lower=30, **kwargs) -> pd.DataFrame:
    """RSI超买超卖检测"""
    # RSI上穿70 = 超买
    # RSI下穿30 = 超卖
    pass

def detect_cci_extreme(symbol, window=10, upper=100, lower=-100, **kwargs) -> pd.DataFrame:
    """CCI极端超买超卖检测"""
    # CCI上穿100 = 极端超买
    # CCI下穿-100 = 极端超卖
    pass

def detect_bias_extreme(symbol, window=10, upper=5, lower=-5, **kwargs) -> pd.DataFrame:
    """BIAS极端偏离检测"""
    # BIAS穿越+N% = 严重超买
    # BIAS穿越-N% = 严重超卖
    pass
```

### 3.4 背离类信号 `signals/divergence_signals.py`

```python
"""
背离类信号：从"同步"变"背离"的状态变化

信号返回值：
- 1: 底背离（看涨）
- -1: 顶背离（看跌）
- 0: 无背离
"""

def detect_macd_divergence(symbol, window=20, **kwargs) -> pd.DataFrame:
    """MACD背离检测"""
    # 价格创新低，MACD没创新低 = 底背离
    # 价格创新高，MACD没创新高 = 顶背离
    pass

def detect_rsi_divergence(symbol, window=14, **kwargs) -> pd.DataFrame:
    """RSI背离检测"""
    pass

def detect_bear_power_divergence(symbol, **kwargs) -> pd.DataFrame:
    """空头力量背离检测"""
    pass
```

### 3.5 信号聚合器 `signals/__init__.py`

```python
"""
信号模块入口

提供统一的信号检测接口
"""

class SignalDetector:
    """信号检测器"""
    
    def __init__(self, signal_types: List[str] = None):
        """
        Parameters
        ----------
        signal_types : list of str
            需要检测的信号类型
            ['ma_cross', 'macd_cross', 'rsi_extreme', 'price_breakout', ...]
        """
        pass
    
    def detect(self, symbol: str, end_date: str = None) -> pd.DataFrame:
        """
        检测所有配置的信号
        
        Returns
        -------
        pd.DataFrame
            columns: date, signal_type, signal_value, description
        """
        pass
    
    def get_combined_signal(self, symbol: str, method: str = 'vote') -> int:
        """
        获取聚合后的综合信号
        
        Parameters
        ----------
        method : str
            'vote': 多数投票
            'weighted': 加权平均
            'any': 任一信号触发
        """
        pass


def get_all_signals(symbol: str, end_date: str = None) -> pd.DataFrame:
    """获取某股票所有可用信号"""
    pass
```

---

## 四、风控模块设计（需新建）

### 4.1 波动率风控 `risk/volatility.py`

```python
"""
波动率风控模块

用途：根据波动率调整仓位
"""

def compute_volatility_adjusted_position(
    symbol: str,
    base_position: float = 1.0,
    target_vol: float = 0.15,
    window: int = 20,
) -> float:
    """
    根据波动率调整仓位
    
    公式：adjusted_position = base_position * (target_vol / current_vol)
    
    Parameters
    ----------
    symbol : str
        股票代码
    base_position : float
        基础仓位比例
    target_vol : float
        目标年化波动率
    window : int
        波动率计算窗口
    
    Returns
    -------
    float
        调整后的仓位比例
    """
    pass

def compute_atr_based_stop_loss(
    symbol: str,
    atr_window: int = 14,
    atr_multiplier: float = 2.0,
) -> Dict:
    """
    基于ATR计算止损价
    
    Returns
    -------
    dict
        {
            'stop_loss_price': 止损价,
            'atr_value': ATR值,
            'risk_per_share': 每股风险
        }
    """
    pass
```

### 4.2 回撤风控 `risk/drawdown.py`

```python
"""
回撤风控模块

用途：监控回撤，触发风控动作
"""

def compute_max_drawdown(prices: pd.Series) -> float:
    """计算最大回撤"""
    pass

def compute_drawdown(prices: pd.Series) -> pd.Series:
    """计算时点回撤序列"""
    pass

def check_drawdown_alert(
    prices: pd.Series,
    warning_level: float = 0.10,
    critical_level: float = 0.20,
) -> Dict:
    """
    回撤预警检测
    
    Returns
    -------
    dict
        {
            'current_drawdown': 当前回撤,
            'max_drawdown': 最大回撤,
            'status': 'normal' / 'warning' / 'critical'
        }
    """
    pass
```

### 4.3 仓位管理 `risk/position_sizing.py`

```python
"""
仓位管理模块

用途：计算各标的的目标仓位
"""

def kelly_criterion(
    win_rate: float,
    win_loss_ratio: float,
) -> float:
    """
    凯利公式计算最优仓位
    
    f = p - (1-p)/b
    其中 p=胜率, b=盈亏比
    """
    pass

def risk_parity_position(
    volatilities: Dict[str, float],
    target_vol: float = 0.10,
) -> Dict[str, float]:
    """
    风险平价仓位计算
    
    Parameters
    ----------
    volatilities : dict
        {symbol: volatility}
    
    Returns
    -------
    dict
        {symbol: position_weight}
    """
    pass

def equal_risk_contribution(
    symbols: List[str],
    end_date: str = None,
) -> Dict[str, float]:
    """等风险贡献仓位"""
    pass
```

---

## 五、现有代码整合

### 5.1 已有信号函数（需迁移到signals模块）

| 函数 | 位置 | 动作 |
|------|------|------|
| `compute_rsrs_signal()` | indicators/rsrs.py | 迁移到 signals/ |
| `compute_north_money_signal()` | market_data/north_money.py | 迁移到 signals/ |

### 5.2 接口统一

```python
# 新增统一入口 src/__init__.py 或 src/api/__init__.py

# 因子接口
from src.factors import get_factor_values_jq

# 信号接口
from src.signals import SignalDetector, get_all_signals

# 风控接口  
from src.risk import compute_volatility_adjusted_position, check_drawdown_alert
```

---

## 六、实现状态

### ✅ 已实现

#### signals 模块（信号检测）
| 文件 | 函数 | 状态 |
|------|------|------|
| `cross_signals.py` | detect_ma_cross | ✅ |
| | detect_macd_cross | ✅ |
| | detect_kdj_cross | ✅ |
| | detect_ema_cross | ✅ |
| | detect_vmacd_cross | ✅ |
| | detect_all_cross_signals | ✅ |
| `extreme_signals.py` | detect_rsi_extreme | ✅ |
| | detect_cci_extreme | ✅ |
| | detect_bias_extreme | ✅ |
| | detect_kdj_extreme | ✅ |
| | detect_all_extreme_signals | ✅ |
| `breakthrough_signals.py` | detect_price_breakout | ✅ |
| | detect_volume_breakout | ✅ |
| | detect_boll_breakout | ✅ |
| | detect_ma_breakout | ✅ |
| | detect_all_breakthrough_signals | ✅ |
| `divergence_signals.py` | detect_macd_divergence | ✅ |
| | detect_rsi_divergence | ✅ |
| | detect_bear_power_divergence | ✅ |
| | detect_kdj_divergence | ✅ |
| | detect_all_divergence_signals | ✅ |
| `__init__.py` | SignalDetector | ✅ |
| | get_all_signals | ✅ |
| | get_signal_summary | ✅ |

#### risk 模块（风控）
| 文件 | 函数 | 状态 |
|------|------|------|
| `volatility.py` | compute_volatility | ✅ |
| | compute_volatility_adjusted_position | ✅ |
| | compute_atr_based_stop_loss | ✅ |
| | detect_volatility_regime_change | ✅ |
| `drawdown.py` | compute_max_drawdown | ✅ |
| | compute_drawdown | ✅ |
| | check_drawdown_alert | ✅ |
| | monitor_stock_drawdown | ✅ |
| | compute_recovery_time | ✅ |
| | compute_drawdown_statistics | ✅ |
| `position_sizing.py` | kelly_criterion | ✅ |
| | risk_parity_position | ✅ |
| | equal_risk_contribution | ✅ |
| | atr_based_position_size | ✅ |
| | optimize_portfolio_positions | ✅ |

#### factors 模块（补充因子）
| 因子 | 说明 | 状态 |
|------|------|------|
| `boll_width` | 布林带宽度 | ✅ |
| `VOL_ratio` | 量比 | ✅ |
| `VWAP` | 成交量加权均价 | ✅ |
| `OBV` | 能量潮指标 | ✅ |
| `amount_ratio` | 换手率比 | ✅ |

#### finance_tables 模块
| 数据表 | 说明 | 状态 |
|------|------|------|
| `STK_AH_PRICE_COMP` | AH股价格对比 | ✅ |

### ⚠️ 待实现

暂无待实现功能。

---

## 七、使用示例

### 7.1 因子选股
```python
from src.factors import get_factor_values_jq

# 多因子选股
factors = get_factor_values_jq(
    securities=['sh600519', 'sz000001', ...],
    factors=['BIAS10', 'ROC120', 'natural_log_of_market_cap', 'roa'],
    end_date='2024-12-31'
)

# 打分排序
scores = factors['BIAS10'] * 0.3 + factors['ROC120'] * 0.2 + ...
selected = scores.nlargest(10)
```

### 7.2 信号择时
```python
from src.signals import SignalDetector

detector = SignalDetector(['ma_cross', 'macd_cross', 'rsi_extreme'])
signals = detector.detect('sh600519', end_date='2024-12-31')

# 获取综合信号
combined = detector.get_combined_signal('sh600519', method='vote')
if combined > 0:
    print("看涨信号")
elif combined < 0:
    print("看跌信号")
```

### 7.3 风控仓位
```python
from src.risk import compute_volatility_adjusted_position

# 根据波动率调整仓位
position = compute_volatility_adjusted_position(
    symbol='sh600519',
    base_position=1.0,
    target_vol=0.15,
    window=20
)
print(f"建议仓位: {position:.2%}")
```

---

## 八、测试用例

每个模块需要包含：
1. 单元测试：验证计算正确性
2. 集成测试：验证模块间协作
3. 回测测试：验证历史表现

测试文件位置：
- `tests/factors/test_*.py`
- `tests/signals/test_*.py`
- `tests/risk/test_*.py`