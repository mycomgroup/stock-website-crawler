# RiceQuant 向导式策略方法论

## 核心原则

向导式策略适合快速验证投资逻辑，无需编写代码。关键是用好筛选和排序的组合。

---

## 参数分工

**universe** — 先定股票池，后续条件都在这个池子里跑

| 字段 | 说明 |
|------|------|
| `["000300.XSHG"]` | 沪深300 |
| `["000905.XSHG"]` | 中证500 |
| `["*"]` | 全市场 |

**filters** — 筛选条件，层层过滤

**sorting** — 排序决定买谁

**maxHoldingNum** — 持仓数量，建议 10-20

**rebalanceInterval** — 调仓频率，建议 5-20 天

---

## 推荐工作流

1. 先用 `--validate` 验证配置
2. 创建策略并用 `--run --wait --full` 运行回测
3. 查看风险指标，调整参数
4. 重复验证

```bash
# 第一步：验证
node run-skill.js --validate --config my-strategy.json

# 第二步：创建并运行
node run-skill.js --create --config my-strategy.json --run --wait --full

# 第三步：调整参数，重复
```

---

## 三套经典策略模板

### 第一套：低估值高股息

最安全，适合入门。

```json
{
  "filters": [
    { "operator": "less_than", "factor": {"type": "fundamental", "name": "pe_ratio"}, "rhs": 15 },
    { "operator": "less_than", "factor": {"type": "fundamental", "name": "pb_ratio"}, "rhs": 1.5 },
    { "operator": "greater_than", "factor": {"type": "fundamental", "name": "dividend_yield"}, "rhs": 3 }
  ],
  "sorting": [
    { "factor": {"type": "fundamental", "name": "dividend_yield"}, "ascending": false, "weight": 0.6 },
    { "factor": {"type": "fundamental", "name": "pe_ratio"}, "ascending": true, "weight": 0.4 }
  ]
}
```

逻辑：PE < 15 且 PB < 1.5 且股息率 > 3%，按股息率优先排序。

### 第二套：高质量增长

成长性好，适合牛市。

```json
{
  "filters": [
    { "operator": "in_range", "factor": {"type": "fundamental", "name": "pe_ratio"}, "rhs": [10, 30] },
    { "operator": "greater_than", "factor": {"type": "fundamental", "name": "roe"}, "rhs": 15 },
    { "operator": "greater_than", "factor": {"type": "fundamental", "name": "revenue_growth_rate"}, "rhs": 10 },
    { "operator": "less_than", "factor": {"type": "fundamental", "name": "debt_ratio"}, "rhs": 50 }
  ],
  "sorting": [
    { "factor": {"type": "fundamental", "name": "roe"}, "ascending": false, "weight": 0.5 },
    { "factor": {"type": "fundamental", "name": "revenue_growth_rate"}, "ascending": false, "weight": 0.5 }
  ]
}
```

逻辑：PE 10-30，ROE > 15%，营收增长 > 10%，负债率 < 50%。

### 第三套：三期调仓

买卖条件分离。

```json
{
  "template": "three_periods",
  "filters": [
    { "operator": "less_than", "factor": {"type": "fundamental", "name": "pe_ratio"}, "rhs": 20 }
  ],
  "buy": {
    "filters": [
      { "operator": "greater_than", "factor": {"type": "pricing", "name": "turnover_rate"}, "rhs": 2 }
    ]
  },
  "sell": {
    "filters": [
      { "operator": "greater_than", "factor": {"type": "fundamental", "name": "pe_ratio"}, "rhs": 30 }
    ]
  }
}
```

逻辑：基础筛选 PE < 20，买入要求换手率 > 2%，卖出条件 PE > 30。

---

## 关键参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `maxHoldingNum` | 持仓数量 | 10-20 |
| `rebalanceInterval` | 调仓天数 | 5-20 |
| `profitTaking` | 止盈比例 | 0.1-0.2 |
| `stopLoss` | 止损比例 | -0.05 ~ -0.1 |

---

## 迭代技巧

- 结果太多：收紧筛选条件，如 PE 从 15 改到 10
- 结果太少：放宽条件，或扩大股票池
- 夏普低：增加风控配置，如止盈止损
- 回撤大：减少持仓数，增加止损

---

## 常见问题

**Q: 向导式策略和代码策略有什么区别？**

A: 向导式通过配置生成代码，无需编程。代码策略灵活性更高，适合复杂逻辑。

**Q: 三期调仓什么时候用？**

A: 当买入和卖出需要不同条件时，比如"放量买入、估值过高卖出"。

**Q: 因子权重如何设置？**

A: 权重和应为 1，重要因子给更高权重。如股息率 0.6、PE 0.4。