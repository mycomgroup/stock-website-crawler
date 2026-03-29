# RFScore PB10 Final Master Release V1

## 一句话结论

`RFScore PB10` 的最终极版本，不是旧版 `PB20 + 20只`，也不是继续发散调研，而是：

> **PB10 主池 + PB20 次级池 + RFScore7 不降级 + 15/12/10/0 四档持仓 + PE/ROA 硬过滤 + 行业上限 + 候选不足留现金 + 研究/监控/正式策略三端完全统一口径。**

## 当前正式版定义

- 正式版名称：`RFScore7 PB10 Release V1`
- 正式版主文件：`/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py`
- 当前最终参数口径：见 [03_official_release_v1.md](/Users/fengzhi/Downloads/git/testlixingren/docs/final_rfscore_release_v1_20260329/03_official_release_v1.md)

## 当前最可靠的结论

### 1. 主线已经明确

- `PB10` 优于 `PB20`
- `RFScore7` 本体有效，但必须叠加估值增强
- `Score 6` 补位不应进入正式版
- 泛化 fallback 补仓不应进入正式版

### 2. 当前最佳正式版结构

- 主池：`RFScore == 7` 且 `PB10`
- 次级池：`RFScore == 7` 且 `PB20`
- 不足则留现金
- 行业约束生效
- 不靠复杂插件堆叠

### 3. 当前最重要的上线升级点

这次 review 后，最重要的升级不是新 alpha，而是：

- **验证脚本**
- **质量监控脚本**
- **行业分析脚本**
- **正式策略**

必须使用同一套候选口径。

否则你在文档里看到的“候选股”，很可能不是策略实际会买的股票。

## 唯一正式版参数摘要

### 选股

- 股票池：`沪深300 + 中证500`
- 排除：`688 / ST / 停牌 / 次新(180天)`
- 主池：`RFScore == 7 and pb_group == 1`
- 次级池：`RFScore == 7 and pb_group == 2`
- 排序：`RFScore / ROA / OCFOA / DELTA_MARGIN / DELTA_TURN / pb_ratio`

### 硬过滤

- `pb_ratio > 0`
- `pe_ratio > 0 and < 100`
- `ROA > 0.5`
- 关键字段非空

### 持仓规则

- `breadth < 0.15` -> `0`
- `0.15 <= breadth < 0.25` -> `10`
- `0.25 <= breadth < 0.35 and trend_off` -> `12`
- 其他 -> `15`

### 行业约束

- 单行业上限：目标持仓的 `30%`
- 超限不补别的低质量股票
- 不足部分留现金

## 明确不进入 V1 的东西

- `Turnover Filter`
- `CGO Filter`
- `Combined Filter`
- `PB5%` 模式
- `RFScore >= 6` 补位
- fallback 补仓
- 自动容量联动

## 这次需要改的文件

### 生产代码

- [rfscore7_pb10_final.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py)

### 必须统一口径的研究/监控工具

这些虽然已经归档进 `docs/research_archive_20260329`，但如果你还要继续拿来做上线核对，就必须按正式版重写或复用正式版逻辑：

- [validate-rfscore-candidates.js](/Users/fengzhi/Downloads/git/testlixingren/docs/research_archive_20260329/skills_joinquant_nookbook/validate-rfscore-candidates.js)
- [rfscore_quality_monitor.py](/Users/fengzhi/Downloads/git/testlixingren/docs/research_archive_20260329/skills_joinquant_nookbook/rfscore_quality_monitor.py)
- [rfscore_monitor_full.py](/Users/fengzhi/Downloads/git/testlixingren/docs/research_archive_20260329/skills_joinquant_nookbook/rfscore_monitor_full.py)
- [rfscore_sector_analysis.py](/Users/fengzhi/Downloads/git/testlixingren/docs/research_archive_20260329/skills_joinquant_nookbook/rfscore_sector_analysis.py)
- [test_rfscore_backup_pool.py](/Users/fengzhi/Downloads/git/testlixingren/docs/research_archive_20260329/skills_joinquant_nookbook/test_rfscore_backup_pool.py)

## 上线前最后检查

### 必须满足

1. 正式策略不再出现 `Score 6` 补位
2. 正式策略不再出现 fallback 补仓
3. 候选不足时留现金
4. 四档持仓规则已落地：`15 / 12 / 10 / 0`
5. 候选验证和正式策略同日输出一致
6. 质量监控和正式策略同日输出一致
7. 行业分析和正式策略同日输出一致
8. 同日候选不存在 `PE > 100` 或 `ROA <= 0.5`

### 建议满足

1. 工具输出同时提供：
   - `raw research candidates`
   - `release_v1 final candidates`
2. 所有临时实验脚本标注为 `legacy`
3. 重新跑一版 `Release V1` 全回测

## 当前非主线保留项

如果主线以外还要保留观察线：

- 第一保留：`红利小盘`
- 第二保留：`国债固收+`
- 其他方向暂不影响主线封版

详见 [05_other_branches_summary.md](/Users/fengzhi/Downloads/git/testlixingren/docs/final_rfscore_release_v1_20260329/05_other_branches_summary.md)

## 最终建议

如果你现在要往上线走，最值钱的动作已经不是再写研究文档，而是：

1. 按 [03_official_release_v1.md](/Users/fengzhi/Downloads/git/testlixingren/docs/final_rfscore_release_v1_20260329/03_official_release_v1.md) 改正式策略
2. 把验证/监控/行业分析工具统一到同一口径
3. 跑一版 `Release V1`
4. 再上模拟盘或上线

## 最终极版本定义

**最终极版本 = 正式版参数表 + review 结论 + 元复核 + 分支保留结论 + 统一后的上线口径。**
