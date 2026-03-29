# ETF 基线标准接口说明

## 1. 设计目标

为后续择时、行业增强、组合层任务提供统一、可复用的接口。

---

## 2. 候选池接口

### 2.1 输入

无 (或可选: 截止日期)

### 2.2 输出

```python
@dataclass
class ETFPoolItem:
    code: str           # ETF 代码, 如 "510300.XSHG"
    name: str           # ETF 名称, 如 "沪深300ETF"
    category: str       # 资产类别: "宽基"|"海外"|"行业"|"商品"|"固收"
    start_date: date    # 上市日期
    avg_volume: float   # 近500日日均成交额 (亿元)
    cluster_id: int     # KMeans 聚类标签
    corr_removed: bool  # 是否因相关性被剔除
    in_pool: bool       # 是否入池
    reason: str         # 入池/出池理由

def get_etf_pool(pool_version: str = "v1.0") -> List[ETFPoolItem]:
    """
    获取指定版本的 ETF 候选池
    
    Args:
        pool_version: 候选池版本号, 如 "v1.0"
    
    Returns:
        List[ETFPoolItem]: 候选池 ETF 列表
    """
    pass
```

### 2.3 版本管理

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0 | 2026-03-28 | 初始版本, 12只 ETF |

---

## 3. 动量因子接口

### 3.1 输入

- prices: pd.DataFrame, 行为日期, 列为 ETF 代码, 值为收盘价
- window: int, 动量计算窗口 (日)

### 3.2 输出

```python
def calc_momentum(
    prices: pd.DataFrame,
    window: int = 20,
    method: str = "simple"  # "simple" | "regression"
) -> pd.Series:
    """
    计算 ETF 动量因子
    
    Args:
        prices: 收盘价 DataFrame, index=日期, columns=ETF代码
        window: 动量窗口 (日)
        method: 计算方法
            - "simple": (close[-1] / close[-window] - 1)
            - "regression": 线性回归斜率 * R^2
    
    Returns:
        pd.Series: 动量值, index=ETF代码
    """
    if method == "simple":
        return prices.iloc[-1] / prices.iloc[-window] - 1
    elif method == "regression":
        # 参考 notebook 43 和策略 05/17
        pass
```

---

## 4. 选股接口

### 4.1 输入

- momentum: pd.Series, 动量因子值
- top_n: int, 选取数量

### 4.2 输出

```python
def select_etf(
    momentum: pd.Series,
    top_n: int = 3
) -> List[str]:
    """
    选取动量最高的 n 只 ETF
    
    Args:
        momentum: 动量因子 Series
        top_n: 选取数量
    
    Returns:
        List[str]: 选中的 ETF 代码列表
    """
    return momentum.nlargest(top_n).index.tolist()
```

---

## 5. 择时接口 (供后续任务使用)

### 5.1 输入

- market_data: 市场数据 (价格、成交量等)
- timing_method: 择时方法

### 5.2 输出

```python
def timing_signal(
    market_data: pd.DataFrame,
    timing_method: str = "none"  # "none" | "rsrs" | "breadth" | "combined"
) -> str:
    """
    生成择时信号
    
    Args:
        market_data: 市场数据
        timing_method: 择时方法
            - "none": 不择时, 始终返回 "BUY"
            - "rsrs": RSRS 择时
            - "breadth": 市场宽度择时
            - "combined": RSRS + 市场宽度联合择时
    
    Returns:
        str: "BUY" | "SELL" | "KEEP"
    """
    if timing_method == "none":
        return "BUY"
    # 其他方法待实现
```

---

## 6. 回测接口

### 6.1 输入

- pool_version: 候选池版本
- momentum_window: 动量窗口
- hold_days: 持有周期
- top_n: 持仓数量
- timing_method: 择时方法
- start_date: 回测开始日期
- end_date: 回测结束日期
- cost: 单边交易成本

### 6.2 输出

```python
@dataclass
class BacktestResult:
    ann_return: float       # 扣费年化收益
    max_drawdown: float     # 最大回撤
    sharpe: float           # 夏普比率
    win_rate: float         # 胜率
    turnover: float         # 年化换手率
    net_value: pd.Series    # 净值序列
    holdings: pd.DataFrame  # 每期持仓记录

def run_backtest(
    pool_version: str = "v1.0",
    momentum_window: int = 20,
    hold_days: int = 10,
    top_n: int = 3,
    timing_method: str = "none",
    start_date: str = "2020-01-01",
    end_date: str = "2025-12-31",
    cost: float = 0.001
) -> BacktestResult:
    """
    运行 ETF 动量轮动回测
    
    Returns:
        BacktestResult: 回测结果
    """
    pass
```

---

## 7. 使用示例

```python
# 获取候选池
pool = get_etf_pool("v1.0")
codes = [item.code for item in pool if item.in_pool]

# 获取价格数据
prices = get_price(codes, start_date="2020-01-01", end_date="2025-12-31")

# 计算动量
momentum = calc_momentum(prices, window=20, method="simple")

# 选股
selected = select_etf(momentum, top_n=3)

# 生成择时信号
signal = timing_signal(market_data, timing_method="none")

# 执行交易
if signal == "BUY":
    # 买入 selected 中的 ETF
    pass
elif signal == "SELL":
    # 卖出所有持仓
    pass
```
