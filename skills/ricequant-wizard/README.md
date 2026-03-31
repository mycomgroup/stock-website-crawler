# RiceQuant Wizard 策略工具

通过程序方式创建和运行 RiceQuant 向导式策略，支持完整的因子配置。

## 功能特性

- **向导式策略创建**：通过 JSON 配置创建策略，无需手写代码
- **完整因子支持**：基本面、量价、技术指标等
- **多期调仓**：支持单期和三期调仓模式
- **买卖分离**：独立配置买入和卖出条件
- **风控配置**：止盈止损、市场信号
- **回测运行**：直接运行回测并获取报告

## 快速开始

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant-wizard

# 安装依赖
npm install

# 创建策略
node run-skill.js --create --config examples/value-investing.json

# 运行回测
node run-skill.js --run --id <strategyId> --wait --full

# 列出策略
node run-skill.js --list --type wizard
```

## 命令详解

### 创建策略

```bash
node run-skill.js --create --config <config.json> [--run] [--wait] [--full]
```

选项：
- `--config` 策略配置文件路径
- `--run` 创建后立即运行回测
- `--wait` 等待回测完成
- `--full` 获取完整报告

### 运行回测

```bash
node run-skill.js --run --id <strategyId> [options]
```

选项：
- `--start` 开始日期 (默认: 2020-01-01)
- `--end` 结束日期 (默认: 2025-03-28)
- `--capital` 初始资金 (默认: 100000)
- `--benchmark` 基准 (默认: 000300.XSHG)
- `--wait` 等待回测完成
- `--full` 获取完整报告

### 其他命令

```bash
# 列出策略
node run-skill.js --list [--type wizard|code]

# 获取回测报告
node run-skill.js --report --id <backtestId>

# 删除策略
node run-skill.js --delete --id <strategyId>

# 验证配置
node run-skill.js --validate --config <config.json>

# 查看可用因子
node run-skill.js --factors
```

## 配置说明

### 基本结构

```json
{
  "name": "策略名称",
  "template": "single_period",
  "universe": ["000300.XSHG"],
  "industries": ["*"],
  "board": ["*"],
  "stOption": "exclude",
  "filters": [],
  "sorting": [],
  "maxHoldingNum": 10,
  "rebalanceInterval": 5,
  "risk": {},
  "backtest": {}
}
```

### 核心字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `template` | string | `single_period` 或 `three_periods` |
| `universe` | string[] | 股票池，如 `["000300.XSHG"]` 或 `["*"]` |
| `filters` | array | 筛选条件 |
| `sorting` | array | 排序规则 |
| `maxHoldingNum` | number | 最大持仓数 (1-50) |
| `rebalanceInterval` | number | 调仓周期 (天) |

### 筛选条件

```json
{
  "filters": [
    {
      "operator": "less_than",
      "factor": { "type": "fundamental", "name": "pe_ratio" },
      "rhs": 15
    }
  ]
}
```

支持的操作符：
- `greater_than` - 大于
- `less_than` - 小于
- `in_range` - 介于 [min, max]
- `rank_in_range` - 排名百分比介于 [min, max]

### 排序规则

```json
{
  "sorting": [
    {
      "factor": { "type": "fundamental", "name": "market_cap" },
      "ascending": false,
      "weight": 0.6
    }
  ]
}
```

### 三期调仓

```json
{
  "template": "three_periods",
  "buy": {
    "filters": [...],
    "rebalanceInterval": 1
  },
  "sell": {
    "filters": [...],
    "rebalanceInterval": 1
  },
  "maxHoldingPercent": 0.15
}
```

## 因子类型

### 基本面因子 (fundamental)

估值指标：`pe_ratio`, `pb_ratio`, `market_cap`
盈利能力：`roe`, `roa`, `gross_profit_margin`
成长能力：`revenue_growth_rate`, `net_profit_growth_rate`
财务健康：`debt_ratio`, `current_ratio`, `quick_ratio`
分红指标：`dividend_yield`, `dividend_payout_ratio`

### 量价因子 (pricing)

`open`, `close`, `high`, `low`, `volume`, `turnover`, `turnover_rate`

### 技术指标 (technical)

`MA`, `EMA`, `MACD`, `RSI`, `KDJ`, `BOLL`, `ATR`

### 元数据 (extra)

`listed_days`, `industry`, `board_type`

## 示例策略

| 文件 | 说明 |
|------|------|
| `examples/value-investing.json` | 低估值高股息 |
| `examples/quality-growth.json` | 高质量增长 |
| `examples/three-periods.json` | 三期调仓示例 |

## 注意事项

1. 需要 RiceQuant 账号，配置 `.env` 或复用 `ricequant_strategy` 的 session
2. 向导式策略会自动生成代码，无需手写
3. 策略保存后可在 RiceQuant 网页端查看和编辑
4. 回测结果保存在 `data/` 目录