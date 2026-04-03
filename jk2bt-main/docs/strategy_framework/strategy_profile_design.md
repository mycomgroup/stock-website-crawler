# 策略画像层设计文档

## 1. 目标

策略画像层的目标是把大量 `.txt` 策略转换为统一的“策略资产档案”，供调度层、组合层、风控层使用。

策略画像层不负责执行策略，而是回答：

- 这是什么类型的策略？
- 它适合什么市场环境？
- 它风险如何？
- 它依赖哪些条件？
- 它和其他策略是否重复？

如果没有画像层，后面的“场景匹配”和“多策略并行分仓”几乎无法做好。

---

## 2. 为什么一定要做策略画像

你当前面对的是大量异构 `.txt` 策略，它们差异很大：

- 资产不同
- 频率不同
- 数据依赖不同
- 执行方式不同
- 风险收益特征不同

如果不先给每个策略做结构化画像，就只能靠人工记忆或经验拍脑袋调度，后期不可维护。

---

## 3. 画像层的职责

策略画像层负责 4 件事：

1. 识别策略类型
2. 记录策略行为特征
3. 量化策略风险收益特征
4. 记录策略运行依赖与可接入方式

---

## 4. 画像内容结构

每个策略至少要包含以下七类画像。

## 4.1 基本标识

- `strategy_id`
- `strategy_name`
- `source_path`
- `author` 或来源
- `version`
- `description`

---

## 4.2 资产类型

定义策略交易的主要资产。

### 建议标签

- `stock`
- `etf`
- `index`
- `lof`
- `fund_of`
- `future_ccfx`
- `mixed`

### 用途

- 决定是否能接入当前交易系统
- 决定使用哪个 broker / data backend

---

## 4.3 运行频率

定义策略的时钟粒度。

### 建议标签

- `daily`
- `minute`
- `mixed`
- `event_driven`

### 用途

- 决定是否能与当前回测引擎适配
- 决定调度刷新频率

---

## 4.4 风格标签

定义策略的 alpha 逻辑。

### 建议标签

- 趋势 `trend`
- 反转 `reversal`
- 价值 `value`
- 质量 `quality`
- 小市值 `small_cap`
- 事件 `event`
- 轮动 `rotation`
- 资金流 `flow`
- 情绪 `sentiment`
- 机器学习 `ml`
- 套利 `arbitrage`

### 注意

一个策略可以有多个风格标签，但要区分：

- 主风格
- 次风格

---

## 4.5 适用场景

这是与场景识别层直接对接的关键字段。

### 建议标签

- 上涨 `trend_up`
- 震荡 `rotation_range`
- 防守 `high_vol_defense`
- 流动性收缩 `liquidity_tight`
- 极端风险回避 `extreme_risk_avoid`

### 需要记录两个维度

#### A. 适用分

例如：

```python
{
    "trend_up": 0.9,
    "rotation_range": 0.4,
    "high_vol_defense": 0.2,
    "liquidity_tight": 0.3,
    "extreme_risk": 0.0
}
```

#### B. 禁用条件

例如：

- 波动率过高禁用
- 成交额过低禁用
- 流动性收缩时禁用

---

## 4.6 持仓与交易特征

这一层描述策略“怎么持仓、怎么交易”。

### 建议字段

- 持仓数量区间
- 集中度
- 平均换手率
- 调仓频率
- 是否择时
- 是否满仓
- 是否允许空仓
- 是否高交易成本敏感

### 典型标签

- `concentrated`
- `diversified`
- `high_turnover`
- `low_turnover`
- `timing_sensitive`
- `always_in_market`

### 用途

- 决定是否适合并行持有
- 决定资金容量与滑点估计

---

## 4.7 风险画像

这部分必须基于回测或历史样本，而不是只看代码。

### 建议字段

- 年化收益
- 最大回撤
- 波动率
- 夏普
- Calmar
- 胜率
- 盈亏比
- 月度回撤分布
- 与基准相关性
- 与其他策略相关性
- 容量估计

### 风险标签示例

- `high_drawdown`
- `low_vol`
- `crowded_style`
- `capacity_small`
- `benchmark_correlated`

---

## 4.8 依赖条件

这是把 `.txt` 策略真正接入系统时最重要的一块之一。

### 需要记录的依赖

- 必须 API
- 必须数据表
- 必须文件资源
- 必须训练模型
- 必须第三方依赖
- 必须账户类型

### 示例

```python
{
    "required_apis": ["get_fundamentals", "get_index_stocks"],
    "required_data": ["valuation", "balance_sheet"],
    "required_files": ["model.pkl"],
    "required_packages": ["xgboost", "sklearn"],
    "required_assets": ["stock"],
    "required_frequency": "daily"
}
```

### 用途

- 判断策略是否可运行
- 调度时判断当前环境是否满足

---

## 5. 画像的来源

策略画像不要只靠人工填写，建议三种来源结合。

## 5.1 静态代码分析

从源码中提取：

- 资产类型
- 频率
- 用到的 API
- 是否注册定时器
- 是否依赖模型文件
- 风格关键词

## 5.2 回测统计分析

从真实回测结果中提取：

- 收益回撤
- 交易频率
- 持仓数量
- 空仓时长
- 因子暴露

## 5.3 人工校验与修正

对自动标签做人工审核，尤其是：

- 风格定义
- 场景适用性
- 禁用条件

---

## 6. 数据模型设计

## 6.1 主画像表

```python
{
    "strategy_id": "...",
    "strategy_name": "...",
    "source_path": "...",
    "asset_type": "stock",
    "frequency": "daily",
    "style_tags": ["value", "rotation"],
    "primary_style": "value",
    "scenario_fit": {...},
    "holding_profile": {...},
    "risk_profile": {...},
    "dependencies": {...},
    "validation_status": "verified",
}
```

## 6.2 运行能力表

记录当前系统能否真正运行该策略：

- `loadable`
- `backtestable`
- `has_data_support`
- `has_api_support`
- `needs_manual_patch`

## 6.3 相似度表

用于组合层去重：

- `strategy_a`
- `strategy_b`
- `return_corr`
- `holding_overlap`
- `style_similarity`

---

## 7. 画像生成流程

建议流程如下：

1. 扫描 `.txt` 策略
2. 静态分析函数、API、依赖
3. 生成初始画像
4. 抽样回测补风险画像
5. 人工修正策略标签
6. 写入画像库

---

## 8. 如何把“所有策略都套入”

不是所有策略都能同样深度地纳入系统，建议分 4 级。

### A 类：完整接入

满足：

- 能加载
- 能回测
- 依赖齐全
- 风险特征明确

这类可以直接进入调度层。

### B 类：适配后接入

满足：

- 核心逻辑清晰
- 有少量依赖缺失或接口不兼容

这类适合优先补适配。

### C 类：信号源接入

满足：

- 可以提取候选标的或方向
- 但不能完整复现交易执行

这类只作为“研究信号”，不直接作为独立策略分配仓位。

### D 类：暂不接入

满足任一：

- 依赖大量聚宽私有环境
- 强依赖分钟或竞价而系统未支持
- 需要复杂外部模型文件
- 套利/期货机制尚不具备

---

## 9. 与调度层的接口

调度层不应该直接读策略源码，而应该消费策略画像。

输入示例：

```python
{
    "strategy_id": "s_023",
    "scenario_fit": {
        "trend_up": 0.8,
        "rotation_range": 0.4,
        "high_vol_defense": 0.2
    },
    "risk_profile": {
        "max_drawdown": 0.18,
        "volatility": 0.22,
        "capacity_score": 0.55
    },
    "holding_profile": {
        "turnover_level": "high",
        "concentration": "medium"
    },
    "dependencies": {
        "loadable": true,
        "backtestable": true
    }
}
```

---

## 10. 画像层的评估指标

### 10.1 覆盖率

- 已画像策略 / 总策略

### 10.2 正确率

- 自动标签与人工标签一致率

### 10.3 可接入率

- A/B 类策略数量占比

### 10.4 去重能力

- 能否识别高相似策略

---

## 11. 第一阶段 MVP 建议

先不要追求全量精确画像。

### MVP 先做这几项

- 资产类型
- 频率
- 主风格
- 适用场景粗标签
- 持仓特征粗标签
- 依赖条件
- 是否可运行

### 风险画像先用基础指标

- 年化收益
- 最大回撤
- 波动率
- 换手率

---

## 12. 常见错误

- 只凭策略名打标签
- 只看代码，不看真实回测
- 标签过细，导致没人会用
- 把“可加载”当成“可调度”
- 不记录依赖，导致上层误用

---

## 13. 总结

策略画像层是多策略系统的“档案馆”和“策略注册中心”。

它的作用不是美化策略描述，而是让系统具备以下能力：

- 看懂每个策略是什么
- 知道什么时候该用它
- 知道为什么不能用它
- 知道它和别的策略是不是重复

没有画像层，所有多策略调度最终都会退化成人工经验管理。

