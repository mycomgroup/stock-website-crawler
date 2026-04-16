# 另类数据因子生成 Pipeline — 工业级设计文档

> **版本**: v2.0 · **状态**: Production-Ready 参考架构 · **适用范围**: 股票多因子策略 / 量化对冲基金

---

## 目录

1. [架构总览](#1-架构总览)
2. [Layer 0 — 数据源接入层](#2-layer-0--数据源接入层)
3. [Layer 1 — 原始存储层 (Raw Lake)](#3-layer-1--原始存储层-raw-lake)
4. [Layer 2 — Point-in-Time 校正层](#4-layer-2--point-in-time-校正层)
5. [Layer 3 — 多频率对齐层](#5-layer-3--多频率对齐层)
6. [Layer 4 — 特征工程层](#6-layer-4--特征工程层)
7. [Layer 5 — 因子中性化层](#7-layer-5--因子中性化层)
8. [Layer 6 — 质量检验门](#8-layer-6--质量检验门)
9. [Layer 7 — 回测验证层](#9-layer-7--回测验证层)
10. [Layer 8 — 因子库管理层](#10-layer-8--因子库管理层)
11. [Layer 9 — 生产监控层](#11-layer-9--生产监控层)
12. [推荐技术栈](#12-推荐技术栈)
13. [编排与调度设计](#13-编排与调度设计)
14. [数据治理与合规](#14-数据治理与合规)
15. [典型另类数据源处理 SOP](#15-典型另类数据源处理-sop)
16. [常见陷阱与 Anti-Pattern](#16-常见陷阱与-anti-pattern)
17. [附录：关键代码模板](#17-附录关键代码模板)

---

## 1. 架构总览

### 1.1 Pipeline 全景图

```
┌─────────────────────────────────────────────────────────────────┐
│                    另类数据因子生成 Pipeline                       │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┤
│ Layer 0  │ Layer 1  │ Layer 2  │ Layer 3  │ Layer 4  │ Layer 5  │
│ 数据源   │ 原始存储 │ PIT校正  │ 频率对齐 │ 特征工程 │ 因子中性 │
│ 接入层   │ Raw Lake │ 时间戳层 │ 日频化层 │ 信号提取 │ 化层     │
├──────────┴──────────┴──────────┴──────────┴──────────┴──────────┤
│               ↓ 通过质检门 (Layer 6)                             │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┤
│ Layer 6  │ Layer 7  │ Layer 8  │ Layer 9  │          │          │
│ 质量检验 │ 回测验证 │ 因子库   │ 生产监控 │          │          │
│ 门       │ 层       │ 管理层   │ 层       │          │          │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
```

### 1.2 设计原则

| 原则 | 说明 |
|------|------|
| **Immutability First** | 原始数据不可变，所有变换生成新版本 |
| **PIT Strict** | 回测中严格禁止使用未来数据，所有数据附带可得时间 |
| **Schema-on-Write** | 入库时强制 Schema 校验，而非读取时推断 |
| **Lineage Tracking** | 每个因子值可追溯到原始数据记录 |
| **Idempotent Pipeline** | 任何阶段重跑不产生副作用，支持幂等重算 |
| **Fail-Fast** | 数据质量异常立刻阻断下游，而非静默传播 |

---

## 2. Layer 0 — 数据源接入层

### 2.1 支持的另类数据类型

| 数据类型 | 代表供应商 | 频率 | 延迟特征 |
|----------|-----------|------|---------|
| 卫星图像 / 地理信息 | Orbital Insight, Spire | 日 / 周 | 1–3 天 |
| 信用卡 / 支付流水 | Earnest Research, Yodlee | 日 / 周 | 3–7 天 |
| 网络爬虫 / 舆情 | Quandl, Refinitiv | 实时 / 日 | < 1 小时 |
| 招聘 / 职位数据 | Burning Glass, LinkUp | 日 | 1–2 天 |
| ESG / 供应链 | Truvalue Labs, Preqin | 日 / 周 | 1–5 天 |
| 专利 / 学术论文 | PatentsView, Semantic Scholar | 月 / 季 | 30–90 天 |
| 航运 / 物流 | MarineTraffic, Descartes | 实时 / 日 | < 4 小时 |
| App 使用数据 | Apptopia, Sensor Tower | 日 / 周 | 3–7 天 |
| 新闻 / 事件 | RavenPack, Bloomberg | 实时 | < 15 分钟 |

### 2.2 接入适配器设计

每类数据源需实现统一接口：

```python
class AltDataConnector(ABC):
    """所有另类数据接入适配器的基类"""

    @abstractmethod
    def fetch(
        self,
        start_date: date,
        end_date: date,
        symbols: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        返回字段必须包含:
          - symbol        : 证券标识符 (统一为 ISIN 或内部 ID)
          - event_time    : 数据发生时间 (数据本身声称的时间)
          - received_at   : 拉取到数据的时间 (系统时间, UTC)
          - as_of         : 数据对外公布的声明时间
          - raw_value     : 原始字段值 (JSON 或具体值)
          - source        : 数据源标识
          - schema_version: 当前 Schema 版本号
        """
        ...

    @abstractmethod
    def validate_schema(self, df: pd.DataFrame) -> ValidationResult:
        """入库前 Schema 校验"""
        ...

    @abstractmethod
    def get_publication_lag_days(self) -> int:
        """硬编码该数据源的典型 publication lag"""
        ...
```

### 2.3 统一标识符映射

```
外部 Symbol → 内部 Entity ID
─────────────────────────────────────────────
Ticker (可变)    →  CUSIP / ISIN (稳定)
ISIN             →  内部 entity_id (永久)
```

**关键**: 必须维护 symbol 历史映射表，支持公司更名、合并、分拆后的回溯映射。

---

## 3. Layer 1 — 原始存储层 (Raw Lake)

### 3.1 存储格式规范

**文件格式**: Apache Parquet  
**表格式**: Apache Iceberg (推荐) 或 Delta Lake  
**存储后端**: S3 / GCS / ADLS

```
raw_lake/
├── {source_name}/
│   ├── {data_type}/
│   │   ├── year=2024/month=01/day=15/
│   │   │   └── part-00000.parquet
│   │   └── ...
│   └── _metadata/
│       ├── schema_history.json
│       └── ingestion_log.parquet
```

### 3.2 必备时间戳字段

| 字段 | 类型 | 说明 | 是否必须 |
|------|------|------|--------|
| `event_time` | TIMESTAMP UTC | 数据描述的事件发生时间 | ✅ |
| `as_of` | TIMESTAMP UTC | 数据声称有效的截止时间 | ✅ |
| `received_at` | TIMESTAMP UTC | 系统实际拿到数据的时间 | ✅ |
| `ingested_at` | TIMESTAMP UTC | 写入数据湖的时间 | ✅ |
| `source_version` | STRING | 供应商数据版本/批次 | ✅ |
| `schema_version` | INT | 内部 Schema 版本 | ✅ |

> **延迟计算**: `publication_lag = received_at - as_of`  
> 这是后续 PIT 校正的基础输入。

### 3.3 数据不可变原则

```
禁止操作:
  ❌ UPDATE / DELETE 原始记录
  ❌ 覆盖写入 (overwrite)
  ❌ 就地修改 Parquet 文件

允许操作:
  ✅ 追加写入 (append-only)
  ✅ 标记逻辑删除 (is_retracted = true)
  ✅ 在新分区写入修订版本
```

### 3.4 Schema 演化策略

使用 Iceberg / Delta Lake 的 Schema Evolution 能力：

- **新增字段**: 允许，旧数据该字段为 NULL
- **字段重命名**: 通过 Schema Registry 记录映射，不物理重命名
- **字段类型变更**: 禁止，通过新版本 Schema 创建新列
- **字段删除**: 禁止，标记为 deprecated

---

## 4. Layer 2 — Point-in-Time 校正层

> ⚠️ **最容易翻车的地方。这一层做错，整个因子在生产中失效。**

### 4.1 三个时间维度的严格区分

```
时间轴示意:
─────────────────────────────────────────────────────────▶ 时间

  T0              T1              T2              T3
  │               │               │               │
  ▼               ▼               ▼               ▼
  事件发生        数据供应商      你实际           数据写入
  (event_time)   对外发布        收到数据         数据库
                 (as_of)         (received_at)    (ingested_at)

  ← 事件延迟 → ← publication lag → ← 传输延迟 →
```

**回测使用规则**: 在模拟日期 `D` 时，只能使用满足以下条件的数据：

```python
# PIT 可用性判断
def is_available_at(record: DataRecord, sim_date: date) -> bool:
    """
    判断某条记录在模拟日期 sim_date 的收盘时是否已可得
    """
    # 方法一：使用实际 received_at（更精确，需要历史接收记录）
    if record.received_at is not None:
        return record.received_at.date() <= sim_date

    # 方法二：使用 as_of + hardcoded lag（当 received_at 缺失时的保守估计）
    safe_available_date = record.as_of + timedelta(
        days=DATA_SOURCE_LAGS[record.source]  # 硬编码 lag
    )
    return safe_available_date.date() <= sim_date
```

### 4.2 各数据源 Publication Lag 配置

```yaml
# config/publication_lags.yaml
data_source_lags:
  satellite_imagery:
    typical_lag_days: 2
    conservative_lag_days: 5    # 保守估计，用于回测
    comment: "图像处理 + 特征提取需要额外时间"

  credit_card:
    typical_lag_days: 5
    conservative_lag_days: 7
    comment: "交易结算 + 匿名化处理"

  web_scraping:
    typical_lag_days: 0
    conservative_lag_days: 1
    comment: "实时爬取，但存在服务器时差"

  earnings_release:
    typical_lag_days: 0
    conservative_lag_days: 1
    comment: "使用 earnings release date，非 fiscal quarter end"

  job_postings:
    typical_lag_days: 1
    conservative_lag_days: 2

  shipping_data:
    typical_lag_days: 1
    conservative_lag_days: 2
```

### 4.3 PIT 数据集构建

```python
def build_pit_snapshot(
    raw_df: pd.DataFrame,
    as_of_date: date,
    source: str,
) -> pd.DataFrame:
    """
    构建截止 as_of_date 收盘时的 PIT 快照。
    对每个 (entity_id, data_field) 取最新可用值。
    """
    lag_days = DATA_SOURCE_LAGS[source]["conservative_lag_days"]

    # 筛选在 as_of_date 已可得的记录
    available = raw_df[
        raw_df["as_of"] + pd.Timedelta(days=lag_days)
        <= pd.Timestamp(as_of_date)
    ].copy()

    # 每个实体取最新的一条
    pit_snapshot = (
        available
        .sort_values("as_of", ascending=False)
        .groupby(["entity_id", "data_field"])
        .first()
        .reset_index()
    )

    pit_snapshot["pit_date"] = as_of_date
    return pit_snapshot
```

### 4.4 回测陷阱检查清单

- [ ] 财报数据使用 earnings release date，而非 fiscal quarter end date
- [ ] 分析师预期修正使用修正发布日期，而非修正所指向的报告期
- [ ] 卫星数据使用图像处理完成日期，而非卫星过境日期
- [ ] 新闻情感分数使用新闻发布时间，而非爬取时间
- [ ] 指数成分股使用历史成分，避免幸存者偏差
- [ ] 价格数据使用复权因子的历史版本（不是当前复权）

---

## 5. Layer 3 — 多频率对齐层

### 5.1 频率对齐策略矩阵

| 原始频率 | 目标 | 对齐策略 | 注意事项 |
|---------|------|---------|---------|
| 分钟 / Tick | 日频 | VWAP / TWAP 聚合 | 截止时间统一为 15:30 收盘 |
| 小时 | 日频 | 取收盘前最后一条 | 跨时区需统一为标的市场时区 |
| 日频 | 日频 | 直接使用 | 确认截止时间一致 |
| 周频 | 日频 | Forward-fill | 直到下次更新前保持不变 |
| 月频 | 日频 | Forward-fill | 注意月末对齐规则 |
| 季频（财报） | 日频 | 使用 earnings release date 对齐 | **绝不使用** fiscal quarter end |

### 5.2 Forward-Fill 规则

```python
def forward_fill_to_trading_days(
    df: pd.DataFrame,
    trading_calendar: TradingCalendar,
    max_fill_days: int = 63,  # 约 3 个月，超过则置 NaN
) -> pd.DataFrame:
    """
    将低频数据 forward-fill 到每个交易日。
    max_fill_days 防止过期数据污染因子。
    """
    all_trading_days = trading_calendar.trading_days(
        df["pit_date"].min(), df["pit_date"].max()
    )

    result = (
        df
        .set_index(["entity_id", "pit_date"])
        .reindex(
            pd.MultiIndex.from_product(
                [df["entity_id"].unique(), all_trading_days]
            )
        )
        .groupby(level=0)
        .ffill(limit=max_fill_days)
        .reset_index()
    )
    return result
```

### 5.3 截面日期统一化

**规则**: 所有数据源的日频因子，在同一交易日截面上必须使用同一时点（如 16:00 ET）之前已可得的数据。

```python
# 交易日截止时间配置
CUTOFF_TIMES = {
    "US_EQUITY": "16:00 America/New_York",  # NYSE 收盘
    "HK_EQUITY": "16:00 Asia/Hong_Kong",
    "CN_A_SHARE": "15:00 Asia/Shanghai",
}
```

---

## 6. Layer 4 — 特征工程层

### 6.1 特征提取框架

```python
class FeatureExtractor(ABC):
    """
    特征提取基类。
    每个另类数据源实现自己的 extractor。
    """
    source_name: str
    feature_names: List[str]

    @abstractmethod
    def extract(
        self,
        pit_df: pd.DataFrame,   # PIT 校正后的数据
        lookback_days: int = 90,
    ) -> pd.DataFrame:
        """
        输出: entity_id × date 的因子值矩阵
        每列对应一个 feature_name
        """
        ...

    def transform_to_zscore(
        self, series: pd.Series, window: int = 252
    ) -> pd.Series:
        """滚动 Z-score 标准化"""
        mu = series.rolling(window, min_periods=60).mean()
        sigma = series.rolling(window, min_periods=60).std()
        return (series - mu) / sigma.clip(lower=1e-8)
```

### 6.2 常用信号转化模式

| 原始信号 | 转化方式 | 因子含义 |
|---------|---------|---------|
| 绝对访问量 | YoY 增速 | 增长动能 |
| 情感分数 | 短期均值 vs 长期均值 | 情感动量 |
| 招聘数量 | 相对行业 Z-score | 行业内超额扩张 |
| 卫星停车场占用率 | 月环比变化 | 客流量变化信号 |
| 信用卡消费 | 按品类 YoY | 消费增长 |

### 6.3 Winsorization 与鲁棒化

```python
def robust_winsorize(
    series: pd.Series,
    method: Literal["mad", "percentile"] = "mad",
    n_mad: float = 3.0,
    pct_bounds: Tuple[float, float] = (0.01, 0.99),
) -> pd.Series:
    """
    截面 Winsorization，防止极端值污染截面排名。
    优先使用 MAD（对异常值更鲁棒）。
    """
    if method == "mad":
        median = series.median()
        mad = (series - median).abs().median()
        lower = median - n_mad * 1.4826 * mad
        upper = median + n_mad * 1.4826 * mad
    else:
        lower = series.quantile(pct_bounds[0])
        upper = series.quantile(pct_bounds[1])

    return series.clip(lower=lower, upper=upper)
```

---

## 7. Layer 5 — 因子中性化层

> **核心目的**: 剔除因子中的市值效应、行业效应和已知风格暴露，确保因子承载的是真正的"另类信息"。

### 7.1 标准中性化流程

**Step 1: 市值 + 行业中性化**（必做）

```python
import statsmodels.api as sm

def neutralize_factor(
    factor_values: pd.Series,          # 截面因子值 (entity_id 为 index)
    market_caps: pd.Series,            # 对数市值
    industry_dummies: pd.DataFrame,    # 行业哑变量矩阵
) -> pd.Series:
    """
    对截面因子做 OLS 回归，取残差作为中性化后的因子。
    残差 = 因子中扣除市值效应和行业效应后的纯净信号。
    """
    # 对齐索引
    common_idx = factor_values.dropna().index
    X = pd.concat([
        np.log(market_caps[common_idx]),
        industry_dummies.loc[common_idx],
    ], axis=1)
    X = sm.add_constant(X)

    model = sm.OLS(factor_values[common_idx], X).fit()
    residuals = model.resid

    return residuals
```

**Step 2: 风格因子正交化**（推荐）

对动量、价值、质量等已知风格因子额外正交化，验证因子的**增量信息价值**：

```python
def orthogonalize_against_style_factors(
    factor_residuals: pd.Series,
    style_factors: pd.DataFrame,  # 列: momentum, value, quality, ...
) -> pd.Series:
    """
    在市值+行业中性化基础上，进一步对风格因子正交化。
    如果残差仍显著，说明因子有超越风格因子的增量信号。
    """
    X = sm.add_constant(style_factors.loc[factor_residuals.index])
    model = sm.OLS(factor_residuals, X).fit()
    return model.resid  # 这才是真正的另类 alpha
```

### 7.2 截面排名标准化

```python
def cross_section_rank_normalize(factor: pd.Series) -> pd.Series:
    """
    转为截面百分位排名 [-0.5, +0.5]。
    对非正态分布鲁棒，是因子合成前的标准做法。
    """
    ranked = factor.rank(pct=True)
    return ranked - 0.5
```

### 7.3 中性化有效性验证

中性化后，验证因子对市值/行业的暴露接近零：

```python
def verify_neutralization(
    neutralized_factor: pd.Series,
    market_caps: pd.Series,
    industry_dummies: pd.DataFrame,
    threshold: float = 0.05,  # R² < 5% 视为有效中性化
) -> bool:
    X = pd.concat([np.log(market_caps), industry_dummies], axis=1)
    model = sm.OLS(neutralized_factor, sm.add_constant(X)).fit()
    return model.rsquared < threshold
```

---

## 8. Layer 6 — 质量检验门

> 因子必须通过所有门槛才能进入回测层。任何一项不达标，因子回流到特征工程层重新处理。

### 8.1 质检指标标准

| 指标 | 最低门槛 | 优质门槛 | 说明 |
|------|---------|---------|------|
| **Rank IC 均值** | \|IC\| ≥ 0.03 | \|IC\| ≥ 0.05 | IC = 因子值与下期收益的截面 Spearman 相关 |
| **ICIR** | ≥ 0.5 | ≥ 0.8 | IC 均值 / IC 标准差 |
| **IC 正负一致性** | 同向比例 ≥ 55% | ≥ 60% | IC 符号稳定性 |
| **Q1-Q5 多空收益** | t-stat ≥ 2.0 | t-stat ≥ 3.0 | 最高分组 vs 最低分组年化收益差 |
| **覆盖率** | ≥ 60% | ≥ 80% | 有效值的股票数 / 股票池总数 |
| **日均换手率** | 5%-40% | 10%-25% | 过低无用，过高成本过大 |
| **最大回撤** | < 40% | < 25% | 多空组合最大回撤 |

### 8.2 IC 计算实现

```python
def compute_rank_ic(
    factor_df: pd.DataFrame,   # columns: entity_id, date, factor_value
    returns_df: pd.DataFrame,  # columns: entity_id, date, fwd_return (下期收益)
    forward_period: int = 1,   # 预测周期 (交易日)
) -> pd.Series:
    """
    计算每个截面日期的 Rank IC。
    """
    merged = factor_df.merge(returns_df, on=["entity_id", "date"])

    ic_series = merged.groupby("date").apply(
        lambda g: g["factor_value"].corr(
            g["fwd_return"], method="spearman"
        )
    )
    return ic_series.dropna()

def compute_ic_stats(ic_series: pd.Series) -> dict:
    return {
        "ic_mean": ic_series.mean(),
        "ic_std": ic_series.std(),
        "icir": ic_series.mean() / ic_series.std(),
        "ic_positive_ratio": (ic_series > 0).mean(),
        "t_stat": ic_series.mean() / (ic_series.std() / np.sqrt(len(ic_series))),
    }
```

### 8.3 多重检验校正 (FDR)

当同时测试多个候选因子时，必须做 FDR 校正，防止数据挖掘。

```python
from statsmodels.stats.multitest import fdrcorrection

def apply_fdr_correction(
    factor_pvalues: Dict[str, float],
    alpha: float = 0.05,
) -> Dict[str, bool]:
    """
    Benjamini-Hochberg FDR 校正。
    只有通过校正的因子才进入下一阶段。
    """
    names = list(factor_pvalues.keys())
    pvals = list(factor_pvalues.values())

    rejected, corrected_pvals = fdrcorrection(pvals, alpha=alpha)

    return {
        name: bool(rejected[i])
        for i, name in enumerate(names)
    }
```

---

## 9. Layer 7 — 回测验证层

### 9.1 Walk-Forward 框架（必须，禁用全样本）

```
时间轴:
─────────────────────────────────────────────────────▶

[  训练窗口 1  ][验证1][  训练窗口 2  ][验证2][  训练窗口 3  ][验证3]
     252日        63日      252日         63日      252日        63日

规则:
- 训练窗口: 参数优化 / 因子选择
- 验证窗口: OOS 性能评估
- 两者不重叠
- 报告验证窗口的 IC 和 Sharpe，而非训练窗口
```

### 9.2 交易成本建模

```python
@dataclass
class TransactionCostModel:
    """
    另类数据因子通常容量小，交易成本是关键约束。
    """
    commission_bps: float = 5.0         # 佣金 (bps)
    bid_ask_bps: float = 3.0            # 买卖价差
    market_impact_bps_per_pct: float = 10.0  # 每 1% ADV 的市场冲击成本

    def estimate_total_cost(
        self,
        trade_size_usd: float,
        adv_usd: float,          # 平均日成交额
    ) -> float:
        """
        估算单笔交易的总成本 (bps)
        """
        participation_rate = trade_size_usd / adv_usd
        impact_cost = self.market_impact_bps_per_pct * participation_rate * 100

        total_bps = self.commission_bps + self.bid_ask_bps + impact_cost
        return total_bps
```

### 9.3 回测指标报告模板

| 指标 | 计算方式 | 备注 |
|------|---------|------|
| 年化 Sharpe | 多空组合年化超额收益 / 年化波动率 | 目标 > 0.8 |
| 年化 IC | 年度 Rank IC 均值 × 252^0.5 | 参考 |
| 最大回撤 | 多空净值曲线最大跌幅 | |
| 换手率 | 每日 (买入+卖出) / 2 / 总持仓 | |
| 容量估算 | 换手 × 最大参与率 × ADV | 实际可投资规模 |
| 成本调整 Sharpe | 扣除交易成本后的 Sharpe | **最终决策依据** |

---

## 10. Layer 8 — 因子库管理层

### 10.1 因子注册元数据

每个入库因子必须记录完整元数据：

```json
{
  "factor_id": "alt_cc_spend_yoy_sector_neutral_v3",
  "display_name": "信用卡消费 YoY 增速 (行业中性化)",
  "data_source": "credit_card_vendor_A",
  "version": 3,
  "created_at": "2024-03-15",
  "author": "quant_team",

  "construction": {
    "lookback_window": 252,
    "forward_fill_max_days": 30,
    "neutralization": ["market_cap", "sector"],
    "winsorization": "mad_3sigma",
    "normalization": "cross_section_rank"
  },

  "publication_lag_days": 7,
  "effective_from": "2018-01-01",
  "coverage_universe": "SP500_HISTORICAL",

  "validation_results": {
    "rank_ic_mean": 0.047,
    "icir": 0.82,
    "coverage_ratio": 0.91,
    "oos_period": "2022-01 to 2024-03",
    "fdr_corrected_pvalue": 0.021
  },

  "status": "PRODUCTION",
  "decay_threshold_ic": 0.02,
  "review_frequency_days": 30
}
```

### 10.2 版本控制规则

| 变更类型 | 版本更新 | 说明 |
|---------|---------|------|
| 参数微调 | Minor (v3 → v3.1) | 窗口长度等参数变化 |
| 中性化方式变更 | Major (v3 → v4) | 回测结果不可直接对比 |
| 数据源切换 | Major + 新 ID | 与旧版本分开追踪 |
| Bug 修复 | Patch + 回溯重算 | 需记录修复原因 |

---

## 11. Layer 9 — 生产监控层

### 11.1 监控指标体系

```
监控维度
├── 数据层监控
│   ├── 数据延迟告警 (actual_lag > expected_lag × 1.5)
│   ├── 数据量异常 (日记录数 < 历史均值 × 50%)
│   ├── 空值率监控 (null_rate > 20%)
│   └── 分布漂移检测 (KS 检验 p-value < 0.05)
│
├── 因子层监控
│   ├── 滚动 IC 衰减告警 (30日滚动 IC < 阈值)
│   ├── 因子值分布漂移 (均值/方差异常)
│   ├── 覆盖率下降告警 (coverage < 60%)
│   └── 换手率突变告警
│
└── 系统层监控
    ├── Pipeline 运行时长超时
    ├── 计算资源使用率
    └── 存储容量预警
```

### 11.2 滚动 IC 衰减检测

```python
def detect_ic_decay(
    ic_series: pd.Series,
    window: int = 63,           # 滚动窗口 (约 3 个月)
    baseline_window: int = 252,  # 基准期 (约 1 年)
    decay_threshold: float = 0.5,  # 当前 IC < 历史 IC × 50% 时告警
) -> MonitoringAlert:
    """
    检测因子 IC 是否发生显著衰减。
    """
    recent_ic = ic_series.tail(window).mean()
    baseline_ic = ic_series.tail(baseline_window).head(
        baseline_window - window
    ).mean()

    decay_ratio = abs(recent_ic) / (abs(baseline_ic) + 1e-8)

    if decay_ratio < decay_threshold:
        return MonitoringAlert(
            level="WARNING",
            factor_id=ic_series.name,
            message=f"IC 衰减至历史基准的 {decay_ratio:.1%}",
            action="触发人工复查，暂停因子权重提升",
        )
    return MonitoringAlert(level="OK", factor_id=ic_series.name)
```

### 11.3 数据分布漂移检测

```python
from scipy.stats import ks_2samp

def detect_distribution_drift(
    current_values: pd.Series,
    reference_values: pd.Series,
    significance_level: float = 0.01,
) -> bool:
    """
    使用 Kolmogorov-Smirnov 检验检测分布漂移。
    返回 True 表示检测到显著漂移，需告警。
    """
    stat, pvalue = ks_2samp(
        current_values.dropna(),
        reference_values.dropna()
    )
    return pvalue < significance_level
```

### 11.4 Grafana 告警配置示意

```yaml
# monitoring/alerts/factor_ic_decay.yaml
alert:
  name: "Factor IC Decay Alert"
  condition: rolling_ic_30d < ic_decay_threshold
  severity: WARNING
  channels:
    - slack: "#quant-alerts"
    - email: quant-team@firm.com
  message: |
    因子 {{ factor_id }} IC 衰减告警
    当前 30日滚动 IC: {{ rolling_ic_30d:.4f }}
    历史基准 IC: {{ baseline_ic:.4f }}
    衰减比例: {{ decay_ratio:.1%}}
    建议: 暂停该因子的权重，触发人工复查
```

---

## 12. 推荐技术栈

### 12.1 完整技术栈

| 层级 | 组件 | 推荐选型 | 备选 | 选择理由 |
|------|------|---------|------|---------|
| **编排调度** | Pipeline 编排 | Prefect 2.x | Airflow 2.x | Prefect 部署更轻量，支持动态 DAG |
| **原始存储** | 数据湖格式 | Apache Iceberg | Delta Lake | 更好的多引擎兼容性 |
| **原始存储** | 对象存储 | S3 / R2 | GCS, ADLS | 成本与生态 |
| **分析存储** | OLAP 数据库 | ClickHouse | DuckDB | 高并发查询性能 |
| **因子计算** | 数据处理 | Polars | Pandas + Numba | Polars 性能优越，内存效率高 |
| **机器学习** | 特征管理 | Feast | Hopsworks | 开源轻量，PIT 支持完善 |
| **实验追踪** | 实验管理 | MLflow | W&B | 自托管，数据不出境 |
| **回测** | 向量化回测 | 自建 | Zipline Reloaded | 自建可控 PIT 逻辑 |
| **监控** | 指标可视化 | Grafana + Prometheus | Datadog | 开源可定制 |
| **数据质量** | 数据验证 | Great Expectations | Pandera | 声明式规则，易维护 |
| **Schema Registry** | Schema 管理 | Confluent Schema Registry | AWS Glue | 多数据源 Schema 统一管理 |
| **CI/CD** | 因子测试 | GitHub Actions + pytest | Jenkins | 自动化因子回归测试 |

### 12.2 本地开发环境

```bash
# 轻量开发栈 (本地 / CI)
DuckDB          # 替代 ClickHouse，零依赖的嵌入式 OLAP
Parquet files   # 替代 Iceberg，本地文件系统
Polars          # 数据处理，与生产一致
pytest + pandera # 数据质量测试

# 一键启动开发环境
docker-compose up -d airflow clickhouse grafana mlflow
```

---

## 13. 编排与调度设计

### 13.1 多频率调度策略

```python
# prefect/flows/alt_data_pipeline.py

@flow(name="alt-data-ingest-realtime")
def realtime_ingest_flow():
    """实时数据 (新闻、舆情): 每 15 分钟"""
    ...

@flow(name="alt-data-ingest-daily")
def daily_ingest_flow():
    """日频数据: 每个工作日 18:00 ET (市场收盘后充足时间)"""
    ...

@flow(name="alt-data-factor-compute")
def daily_factor_compute_flow():
    """因子计算: 每个工作日 20:00 ET (数据入库后)"""
    ...

@flow(name="alt-data-factor-validate")
def weekly_validation_flow():
    """因子质检: 每周一 06:00 ET"""
    ...

@flow(name="alt-data-monitor-ic")
def ic_monitoring_flow():
    """IC 监控: 每个工作日 22:00 ET"""
    ...
```

### 13.2 依赖关系与 SLA

```
数据接入 (18:00 ET, SLA: 30min)
    ↓
PIT 校正 (18:30 ET, SLA: 15min)
    ↓
频率对齐 (18:45 ET, SLA: 15min)
    ↓
特征工程 (19:00 ET, SLA: 30min)
    ↓
中性化 (19:30 ET, SLA: 15min)
    ↓
质检门 (19:45 ET, SLA: 10min)
    ↓
因子库更新 (20:00 ET, SLA: 10min)  ← 下游策略依赖此时间
```

---

## 14. 数据治理与合规

### 14.1 MNPI (重要非公开信息) 风险控制

| 控制点 | 措施 |
|-------|------|
| 数据合法性 | 所有数据源需提供 MNPI Clean 认证或合规意见书 |
| 数据隔离 | 潜在敏感数据与策略信号物理隔离 |
| 使用审计 | 每次数据访问记录完整审计日志 |
| 合规检查 | 季度数据使用合规审查 |

### 14.2 数据血缘 (Lineage) 追踪

```python
@dataclass
class FactorLineage:
    """追踪因子值的完整数据血缘"""
    factor_id: str
    computation_date: date
    input_data_sources: List[str]      # 使用的原始数据源
    input_record_ids: List[str]        # 关联的原始数据记录 ID
    transformation_steps: List[str]    # 变换步骤序列
    code_version: str                  # Git commit hash
    pipeline_run_id: str               # 可重现特定计算
```

---

## 15. 典型另类数据源处理 SOP

### 15.1 卫星图像 (停车场占用率)

```
原始图像 (GeoTIFF)
    ↓ 目标检测模型 (内部或供应商提供)
车辆计数 (received_at: 图像处理完成时)
    ↓ PIT 校正 (lag = 2 天保守)
    ↓ 相对历史基线 Z-score
    ↓ 行业内截面中性化
停车场占用率因子
```

**关键风险**: 图像质量受天气影响，需增加云覆盖率过滤，缺失值不 forward-fill（宁缺毋滥）。

### 15.2 信用卡消费数据

```
原始交易流水 (供应商聚合)
    ↓ 按商户类别 + 上市公司 mapping
    ↓ YoY / QoQ 增速计算 (至少需要 1 年历史)
    ↓ PIT 校正 (lag = 7 天保守)
    ↓ 截面 Winsorization (MAD 3σ)
    ↓ 行业 + 市值中性化
信用卡消费增速因子
```

**关键风险**: 商户-公司 mapping 准确率有限；消费数据可能因面板样本变化产生人为趋势。

---

## 16. 常见陷阱与 Anti-Pattern

### 16.1 PIT 相关

| ❌ 错误做法 | ✅ 正确做法 |
|-----------|-----------|
| 使用 fiscal quarter end 对齐财报 | 使用 earnings release date |
| 直接用 `received_at` 作为 `as_of` | 区分这两个时间戳，分别记录 |
| 回测用当前可得的历史数据 | 使用历史 snapshot（包含修订前的版本）|
| 忽略供应商数据修订 (revision) | 保存每次数据修订，用最初版本回测 |
| 用当天 16:01 才发布的数据做当天信号 | 严格检查截止时间 |

### 16.2 统计相关

| ❌ 错误做法 | ✅ 正确做法 |
|-----------|-----------|
| 全样本回测参数调优后再评估 | Walk-Forward OOS 评估 |
| 测试 100 个因子不做多重检验校正 | FDR / Bonferroni 校正 |
| IC 用 Pearson 相关 | IC 用 Spearman 排名相关（对异常值鲁棒）|
| 回测忽略交易成本 | 建模冲击成本，按实际 ADV 估算容量 |
| 幸存者偏差（只回测现存股票）| 使用历史指数成分 + 退市股票 |

### 16.3 工程相关

| ❌ 错误做法 | ✅ 正确做法 |
|-----------|-----------|
| 直接覆盖写入原始数据 | Append-only，逻辑删除 |
| 因子计算逻辑散落在多处 | 统一 FeatureExtractor 基类 |
| 硬编码日期范围 | 参数化，支持幂等重算 |
| 不记录代码版本与因子值的关联 | 每个因子值关联 git commit |
| 监控只看有没有数据到来 | 同时监控 IC 衰减和分布漂移 |

---

## 17. 附录：关键代码模板

### 17.1 完整 PIT 数据集构建

```python
# 完整的 PIT 日历生成器
class PITDatasetBuilder:
    def __init__(
        self,
        raw_lake_path: str,
        trading_calendar: TradingCalendar,
        lag_config: Dict[str, int],
    ):
        self.raw_lake_path = raw_lake_path
        self.calendar = trading_calendar
        self.lag_config = lag_config

    def build_panel(
        self,
        source: str,
        start_date: date,
        end_date: date,
    ) -> pd.DataFrame:
        """
        构建 (entity_id × date) 的 PIT 因子面板。
        每个单元格只使用 date 当天收盘前已可得的最新数据。
        """
        raw_df = self._load_raw(source, start_date, end_date)
        trading_days = self.calendar.trading_days(start_date, end_date)

        panels = []
        for td in trading_days:
            snapshot = self._pit_snapshot(raw_df, source, td)
            snapshot["date"] = td
            panels.append(snapshot)

        panel_df = pd.concat(panels, ignore_index=True)
        return panel_df

    def _pit_snapshot(
        self, raw_df: pd.DataFrame, source: str, as_of: date
    ) -> pd.DataFrame:
        lag = self.lag_config[source]
        cutoff = pd.Timestamp(as_of) - pd.Timedelta(days=lag)

        available = raw_df[raw_df["as_of"] <= cutoff]
        latest = (
            available
            .sort_values("as_of")
            .groupby("entity_id")
            .last()
            .reset_index()
        )
        return latest
```

### 17.2 Great Expectations 数据质量规则

```python
# data_quality/expectations/alt_data_suite.py
import great_expectations as ge

def build_expectation_suite(source_name: str) -> ExpectationSuite:
    suite = ge.ExpectationSuite(expectation_suite_name=f"{source_name}_suite")

    # 必填字段不为空
    for col in ["entity_id", "as_of", "received_at", "factor_value"]:
        suite.add_expectation(
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_not_be_null",
                kwargs={"column": col, "mostly": 0.95},
            )
        )

    # received_at 必须晚于 as_of
    suite.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_pair_values_A_to_be_greater_than_B",
            kwargs={"column_A": "received_at", "column_B": "as_of"},
        )
    )

    # 因子值在合理范围内（需按 source 配置）
    suite.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_between",
            kwargs={"column": "factor_value", "min_value": -100, "max_value": 100},
        )
    )

    return suite
```

### 17.3 MLflow 因子实验追踪

```python
import mlflow

def log_factor_experiment(
    factor_id: str,
    construction_params: dict,
    ic_stats: dict,
    backtest_results: dict,
):
    with mlflow.start_run(run_name=factor_id):
        # 记录构建参数
        mlflow.log_params(construction_params)

        # 记录质检指标
        mlflow.log_metrics({
            "rank_ic_mean": ic_stats["ic_mean"],
            "icir": ic_stats["icir"],
            "ic_positive_ratio": ic_stats["ic_positive_ratio"],
            "q1_q5_spread_annualized": backtest_results["q1_q5_spread"],
            "long_short_sharpe": backtest_results["sharpe"],
            "max_drawdown": backtest_results["max_drawdown"],
            "coverage_ratio": backtest_results["coverage"],
            "avg_daily_turnover": backtest_results["turnover"],
            "cost_adjusted_sharpe": backtest_results["sharpe_after_cost"],
        })

        # 记录 IC 时间序列图
        mlflow.log_artifact("ic_time_series.png")
        mlflow.log_artifact("quintile_returns.png")

        # 记录代码版本
        mlflow.set_tag("git_commit", get_git_commit_hash())
        mlflow.set_tag("status", "PENDING_REVIEW")
```

---

*文档维护: Quant Research Team*  
*最后更新: 2024 Q4*  
*下次复审: 因子上线后每季度复审一次*
