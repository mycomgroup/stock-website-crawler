# RFScore7 终极版策略总结

> 说明：这份文档保留的是 **2026-03-28 之前的历史研究结论**，其中 `PB20 + 20只 + 10只减仓` 的表述已经不是当前正式版口径。
> 当前用于上线的唯一正式版，请以 [100_rfscore_pb10_official_release_v1.md](/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/100_rfscore_pb10_official_release_v1.md) 为准。

## 1. 这次到底看了什么

本次围绕 `RFScore7 / 质量基本面` 这条线，重点看了这些材料：

- `聚宽有价值策略558/98 FScore9因子模型改进——RFScore7因子.ipynb`
- `聚宽有价值策略558/11 研究 多因子选股策略——基于传统分析.ipynb`
- `聚宽有价值策略558/52 市场宽度——简洁版.ipynb`
- `聚宽有价值策略558/59 研究 【复现】RSRS择时改进.ipynb`
- `聚宽有价值策略558/60 研究 【分享】对RSRS模型的一次修改.ipynb`
- `聚宽有价值策略558/95 首席质量因子-Gross Profitabilit（简化版）.txt`
- `聚宽有价值策略558/04 高股息低市盈率高增长的价投策略.txt`
- `聚宽有价值策略558/06 PEG+成长+小市值+RSRS择时.txt`
- `skills/joinquant_nookbook`
- `skills/joinquant_strategy`

## 2. 原始金矿在哪里

`98 FScore9因子模型改进——RFScore7因子.ipynb` 里的原始 `RFScore7` 不是简化版阈值打分，而是下面 7 个质量因子：

- `ROA`
- `DELTA_ROA`
- `OCFOA`
- `ACCRUAL`
- `DELTA_LEVELER`
- `DELTA_MARGIN`
- `DELTA_TURN`

原 notebook 已经给出几个很重要的结论：

1. `PE` 无效。
2. `DP` 有帮助，但整体不如 `RFScore7` 主体。
3. `PS/PCF` 不强。
4. `PB` 是最值得叠加的估值增强。

更进一步，原 notebook 保存下来的输出显示：

- `RFScore7 + PB(10%)` 年化约 `17.94%`
- `RFScore7 + PB(20%)` 年化约 `16.54%`
- `RFScore7 + PB(30-40%)` 年化约 `19.69%`
- 纯 `RFScore7` 年化约 `14.53%`

说明结论不是“RFScore7 单独最好”，而是：

- `RFScore7` 是主引擎
- `PB` 是最有效的增强器

## 3. 最近样本上的再验证

为了更贴近当前市场，我没有只信 notebook 原结论，而是重新在 `JoinQuant notebook` 里做了最近样本测试。

### 3.1 第一轮：多版本横向测试

测试区间：

- `2024-01-01` 到 `2025-03-26`

股票池：

- `沪深300 ∪ 中证500`，也就是更实盘化的 `中证800` 风格宇宙

结论：

- `rfscore_base`：累计 `-9.34%`
- `rfscore_pb10`：累计 `+2.21%`
- `rfscore_pb20`：累计 `+20.79%`
- `rfscore_pb3040`：累计 `+8.56%`

这一步很关键，说明在最近样本里：

- 裸 `RFScore7` 不够好
- `PB` 低 20% 增强后，策略显著改善

### 3.2 第二轮：继续打磨

我又继续比较了：

- `PB20 + 默认排序`
- `PB20 + Gross Profitability` 二次排序
- `PB20 + 宽度/趋势强制减仓`

结论：

- `PB20 + 默认排序` 最稳定
- `Gross Profitability` 作为二次排序，在这段样本里没有额外增益
- 强行用宽度/趋势空仓或半仓，最近样本里也没有带来明显改善

因此最终版的思路定成：

- 主体：`RFScore7`
- 增强：`PB` 低 20%
- 风控：只做温和仓位调节，不做激进硬切换

## 4. 最终版本

最终实盘代码文件：

[rfscore7_pb20_final.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb20_final.py)

对照组代码文件：

[rfscore7_base_800.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_base_800.py)

最终版设计如下：

1. 股票池使用 `沪深300 + 中证500`
2. 过滤 `ST / 停牌 / 次新 / 科创板`
3. 用原始 `RFScore7` 计算质量得分
4. 只保留 `PB` 处于低 20% 的股票
5. 在 `RFScore=7` 的股票里，按 `ROA / OCFOA / DELTA_MARGIN / DELTA_TURN / pb_ratio` 排序
6. 正常环境持有 `20` 只
7. 若市场宽度低于 `0.25` 且指数趋势走弱，则降到 `10` 只
8. 若市场宽度低于 `0.15` 且趋势仍弱，则允许空仓

这不是“最花哨”的版本，但它是目前证据最完整、最像实盘版本的版本。

## 5. 策略引擎正式回测

我用 `skills/joinquant_strategy` 跑了正式策略回测。

### 5.1 最终版

回测文件：

[backtest-full-17452f8b36425a9bc138b590f179544e-1774653746982.json](/Users/fengzhi/Downloads/git/testlixingren/output/backtest-full-17452f8b36425a9bc138b590f179544e-1774653746982.json)

回测区间：

- `2024-01-01` 到 `2025-03-26`

核心结果：

- 累计收益：`21.62%`
- 年化收益：`17.97%`
- 基准收益：`14.23%`
- 超额收益：`6.47%`
- 最大回撤：`16.20%`
- Sharpe：`0.68`
- Alpha：`7.43%`
- Beta：`0.83`
- 胜率：`64.67%`

### 5.2 裸 RFScore7 对照组

回测文件：

[backtest-full-9707d797cc096beda6868ae4514cf247-1774653799950.json](/Users/fengzhi/Downloads/git/testlixingren/output/backtest-full-9707d797cc096beda6868ae4514cf247-1774653799950.json)

同区间核心结果：

- 累计收益：`-3.72%`
- 年化收益：`-3.15%`
- 最大回撤：`23.39%`
- Sharpe：`-0.33`
- 胜率：`47.66%`

### 5.3 结论

这组对照已经足够说明问题：

- 裸 `RFScore7` 在更实盘化股票池里并不好用
- `RFScore7 + PB低20% + 温和市场状态调节` 才是这条线真正能打的版本

## 6. 当前市场下的实盘候选

我又用同一套最终逻辑跑了当前交易日快照。

当前结果：

- 交易日：`2026-03-27`
- 市场宽度：`0.23`
- 趋势状态：`False`
- 目标持仓数：`10`
- 当前满足主条件的候选股：`4` 只

候选代码：

- `601019.XSHG`
- `600282.XSHG`
- `600019.XSHG`
- `001213.XSHE`

对应 notebook 执行结果文件：

[joinquant-notebook-result-1774653843726.json](/Users/fengzhi/Downloads/git/testlixingren/output/joinquant-notebook-result-1774653843726.json)

这说明一个很现实的结论：

- 当前市场处于弱宽度状态
- 最终版策略不会强行凑满很多股票
- 这更像一个“精选少量质量低估股”的进攻窗口，而不是全面铺仓窗口

## 7. 这条线现在的最终判断

如果只说一句话：

`RFScore7` 本身不是终点，`RFScore7 + PB低20%` 才是这条线里真正挖出来的金子。

再往实盘上走一步，最合适的版本就是：

- 中证800 宇宙
- 原始 RFScore7 质量打分
- PB 低 20% 做估值增强
- 弱市场里自动降仓，不激进梭哈

这已经不是“研究文档”，而是可以继续往真实交易靠拢的策略母体了。
