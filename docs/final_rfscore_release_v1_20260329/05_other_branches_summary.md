# RFScore 主线之外仍值得保留的分支总结

## 目的

这份文档用于把当前已经跑过、但没有进入第三轮 `RFScore PB10` 主线的分支单独保留下来，防止后续因为注意力集中到单主线而丢掉次优但仍有研究价值的方向。

这些分支不是“当前最该打穿”的主线，但它们里有几条很适合后续独立开线继续研究。

## 当前最值得保留的分支

### 红利小盘防守线

- 当前结论：`Go`
- 主要依据：
  - [03_红利小盘防守线实盘化报告_2026-03-28.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/03_红利小盘防守线实盘化报告_2026-03-28.md)
  - [05_红利价值质量三分支验证报告.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/05_红利价值质量三分支验证报告.md)

保留理由：
- 它是价值/红利线里唯一真正跑出防守特征的分支。
- 熊市表现优于其他价值分支。
- 与 `RFScore PB10` 风格互补，适合后续单独开“股票防守层”研究线。

### 纯 A ETF 动量线

- 当前结论：`Watch / Worth Trying`
- 主要依据：
  - [02_etf_baseline_report.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/02_etf_baseline_report.md)
  - [06_etf_timing_v2_purea_tiered_report.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/06_etf_timing_v2_purea_tiered_report.md)

保留理由：
- 纯 A 池 + 分级仓位后，它已经从“证伪”回到了“可再试”。
- 它更适合做低摩擦趋势线，而不是主 alpha，但仍值得保留。

### 防守底仓线

- 当前结论：`有价值，但证据还不够硬`
- 主要依据：
  - [防守底仓策略验证报告_2026-03-28.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/防守底仓策略验证报告_2026-03-28.md)
  - [10_压力测试结果_20260328.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/10_压力测试结果_20260328.md)

保留理由：
- 方向是对的，但正式回测还没完全补硬。
- 很适合后续开“绝对收益 / 防守底仓”独立线。

### 宏观 + 状态路由器

- 当前结论：`保留，但定位为风控层/解释层`
- 主要依据：
  - [11_macro_regime_router_validation.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/11_macro_regime_router_validation.md)
  - [09_regime_router_v2_backtest_2026-03-28.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/09_regime_router_v2_backtest_2026-03-28.md)

保留理由：
- 它更适合作为“风险控制层”和“解释层”，不是核心 alpha。
- 方向没错，后续值得单独做成状态机系统工程。

### 机器学习多因子线

- 当前结论：`Watch`
- 主要依据：
  - [07_ML_MultiFactor_Validation_Report.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/07_ML_MultiFactor_Validation_Report.md)

保留理由：
- 没有明确打赢 RFScore 主线，但也没有彻底失效。
- 逻辑回归仍值得作为对照模型保留。

### 国九条小市值线

- 当前结论：`Watch`
- 主要依据：
  - [07_small_cap_branches_verification_report.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/07_small_cap_branches_verification_report.md)

保留理由：
- 小市值大类里它是唯一值得继续观察的母线。
- 当前不适合主仓，但风格恢复时适合独立开线。

## 当前不建议优先继续投入的方向

### 行业增强轮动

- 当前结论：`可解释，但不是必选层`
- 主要依据：
  - [task04_industry_enhancement_report.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/task04_industry_enhancement_report.md)

### 新因子探索

- 当前结论：`暂不工程化`
- 主要依据：
  - [09_factor_innovation_lab_validation_report.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/09_factor_innovation_lab_validation_report.md)
  - [09_factor_innovation_lab_v2_validation_report.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/09_factor_innovation_lab_v2_validation_report.md)

## 建议的独立开线优先级

### 第一优先级

1. 红利小盘防守线
2. 防守底仓线
3. 纯 A ETF 动量线

### 第二优先级

1. 宏观 + 状态路由器
2. 机器学习多因子线
3. 国九条小市值线

### 第三优先级

1. 行业增强轮动
2. 新因子探索

## 一句话总结

如果 `RFScore PB10` 之外只保留几条最不该丢的线，我建议保留：

- `红利小盘`
- `纯 A ETF 动量`
- `防守底仓`
- `状态路由器`
- `ML 对照线`
- `国九条小市值观察线`
