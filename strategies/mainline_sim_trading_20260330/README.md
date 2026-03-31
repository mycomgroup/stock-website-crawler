# 主线模拟盘实盘化工具包

> 日期：2026-03-30
> 策略：首板低开 + 情绪开关
> 用途：30天模拟盘执行与监控

---

## 一、目录结构

```
mainline_sim_trading_20260330/
├── README.md                 # 使用说明
├── data/                     # 数据目录
│   ├── 30day_template.csv    # 30天记录模板
│   ├── sentiment_daily.csv   # 每日情绪数据（自动生成）
│   └── trade_records.csv     # 交易记录（自动生成）
├── scripts/                  # 脚本目录
│   ├── get_sentiment_data.py # 情绪数据获取
│   ├── execute_trade.py      # 实盘执行脚本
│   ├── pause_manager.py      # 停手机制管理
│   └── monitor_30day.py      # 30天监控脚本
└── docs/                     # 文档目录
    ├── 执行手册.md            # 详细执行手册
    └── 数据字典.md            # 数据字段说明
```

---

## 二、快速开始

### 2.1 情绪数据获取

```bash
cd strategies/mainline_sim_trading_20260330/scripts
python get_sentiment_data.py --date 2026-04-01
```

**输出**：
- `data/sentiment_daily.csv` - 每日情绪数据
- 控制台显示：涨停家数、最高连板、涨跌停比

### 2.2 交易执行

```bash
python execute_trade.py --mode buy --date 2026-04-01
python execute_trade.py --mode sell --date 2026-04-02
```

### 2.3 停手机制管理

```bash
python pause_manager.py --action record --pnl -0.03
python pause_manager.py --action check
```

### 2.4 30天监控

```bash
python monitor_30day.py --day 15
```

---

## 三、核心脚本说明

### 3.1 情绪数据获取（get_sentiment_data.py）

**数据源**：
- 东方财富涨停统计（推荐）
- 同花顺涨停复盘（备用）
- 通达信本地数据（可选）

**输出字段**：
| 字段 | 说明 |
|------|------|
| date | 日期 |
| zt_count | 涨停家数 |
| dt_count | 跌停家数 |
| zt_dt_ratio | 涨跌停比 |
| max_lianban | 最高连板数 |
| allow_buy | 是否允许买入（True/False） |

### 3.2 实盘执行脚本（execute_trade.py）

**买入模式**：
- 检查情绪开关
- 检查停手状态
- 筛选假弱高开股票
- 记录买入信息

**卖出模式**：
- 检查持仓状态
- 执行次日开盘卖出
- 记录卖出盈亏

**输出字段**：
| 字段 | 说明 |
|------|------|
| trade_id | 交易编号 |
| stock_code | 股票代码 |
| buy_date | 买入日期 |
| buy_price | 买入价格 |
| sell_date | 卖出日期 |
| sell_price | 卖出价格 |
| pnl | 盈亏比例 |
| status | 状态（holding/sold） |

### 3.3 停手机制管理（pause_manager.py）

**功能**：
- 记录交易盈亏
- 统计连亏次数
- 管理停手天数
- 判断是否可交易

**输出**：
| 字段 | 说明 |
|------|------|
| loss_count | 连亏次数 |
| pause_days | 剩余停手天数 |
| can_trade | 是否可交易 |

### 3.4 30天监控脚本（monitor_30day.py）

**功能**：
- 统计核心指标
- 生成监控报告
- 对比回测预期

**输出指标**：
| 指标 | 说明 |
|------|------|
| trade_count | 交易次数 |
| win_rate | 胜率 |
| avg_pnl | 平均收益 |
| max_loss | 最大单笔亏损 |
| max_drawdown | 最大回撤 |
| max_consecutive_loss | 最大连亏次数 |

---

## 四、数据记录模板

### 4.1 30天模拟盘记录模板

见 `data/30day_template.csv`

**必填字段**：
- 日期
- 情绪状态（涨停家数）
- 停手状态
- 操作（买入/卖出/空仓）
- 股票代码
- 开盘涨幅
- 买入价
- 卖出价
- 盈亏比例
- 备注

### 4.2 每日情绪数据

见 `data/sentiment_daily.csv`

**自动生成字段**：
- 日期
- 涨停家数
- 跌停家数
- 涨跌停比
- 最高连板
- 是否开仓

---

## 五、执行流程

### 5.1 盘前（08:30）

```bash
# 1. 获取昨日情绪数据
python get_sentiment_data.py --date 2026-04-01

# 2. 检查停手状态
python pause_manager.py --action check

# 3. 输出决策建议
# 查看控制台：是否开仓、涨停家数、停手状态
```

### 5.2 开盘（09:35）

```bash
# 1. 确定买入目标（手动筛选假弱高开）
# 2. 执行买入
python execute_trade.py --mode buy --stock 000001 --price 12.50

# 3. 记录买入信息
```

### 5.3 收盘（15:00）

```bash
# 1. 记录当日交易结果
python execute_trade.py --mode record --pnl -0.02

# 2. 更新停手状态
python pause_manager.py --action update
```

### 5.4 次日开盘（09:35）

```bash
# 1. 执行卖出
python execute_trade.py --mode sell --stock 000001

# 2. 记录盈亏
python pause_manager.py --action record --pnl 0.01
```

---

## 六、监控与复盘

### 6.1 每周复盘

```bash
# 统计本周数据
python monitor_30day.py --day 7

# 输出：
# - 交易次数
# - 胜率
# - 平均收益
# - 最大回撤
```

### 6.2 30天总结

```bash
# 生成30天报告
python monitor_30day.py --day 30 --report

# 输出：
# - 核心指标对比回测预期
# - 异常交易分析
# - 策略有效性判断
```

---

## 七、注意事项

### 7.1 数据源选择

| 数据源 | 优点 | 缺点 |
|--------|------|------|
| 东方财富 | 免费、实时 | 需联网 |
| 同花顺 | 专业、准确 | 需付费 |
| 通达信 | 本地数据 | 需手动更新 |

### 7.2 执行偏差

| 偏差来源 | 影响 | 应对 |
|----------|------|------|
| 涨停买不到 | 交易数少于预期 | 手动记录 |
| 跌停卖不出 | 亏损大于预期 | 标记异常 |
| 滑点误差 | 收益低于预期 | 实际价格记录 |

### 7.3 异常处理

| 异常 | 处理 | 记录方式 |
|------|------|----------|
| 情绪数据缺失 | 保守空仓 | 备注"数据缺失" |
| 无法成交 | 放弃交易 | 备注"涨停买不到" |
| 系统错误 | 手动记录 | Excel补录 |

---

## 八、联系方式

- 策略文档：`/docs/opportunity_strategies_20260330/result_06_mainline_sim_readiness.md`
- 问题反馈：记录在 `data/trade_records.csv` 备注
- 30天报告：`/docs/opportunity_strategies_20260330/30day_report.md`

---

**文档版本**：v1.0
**创建时间**：2026-03-30
**适用策略**：首板低开 + 情绪开关