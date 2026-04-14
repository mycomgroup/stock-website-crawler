# G1 业绩预增/扭亏 - 搜索地图

## 当前探索分支：G1

### 策略定位
- 核心假设：业绩超预期会带来股价上涨，特别是预增幅度大、股价未充分反应的情况
- 主事件条件：中报预增/季报预增 + 净利润预增上限大于X%
- 辅助条件：股价近20日涨幅小于15%（防止追高）

### 已验证有效（keep）
- [adjust_trailing_stop] 追踪止损 8% → 10%：score 0.0 → 1.8711
- [add_formula_condition] 添加市盈率小于30：score 1.8711 → 2.2215
- [add_formula_condition] 添加成交额大于5000万：score 2.2215 → 2.2219
- [remove_formula_condition] 移除非ST条件：score 2.2219 → 2.2220
- [add_formula_condition] 添加流通市值小于50亿：score 2.2220 → 3.5209 ⭐
- [adjust_trailing_stop] 追踪止损 10% → 5%：score 3.5209 → 3.5214
- [adjust_formula_threshold] 市盈率 30 → 38.9：score 3.5214 → 4.9519 ⭐⭐ 年化收益翻倍！

### 已验证无效/崩溃（rollback/crash）
- [adjust_stop_loss] 止损 12% → 9%：rollback
- [adjust_trailing_stop] 追踪止损 10% → 8%：rollback
- [adjust_max_positions] 最大持仓 6 → 2：score 大幅下降到 -0.954
- [adjust_take_profit] 止盈 25% → 20%：rollback
- [adjust_days_for_sale] 持仓天数 2,4 → 2：rollback
- [add_formula_condition] 营业收入增长率大于15%：crash
- [add_formula_condition] 市盈率 30 → 22.4：crash
- [add_formula_condition] 净利润增长率大于30%：rollback（score略降）

### 待探索方向
1. ~~**市盈率阈值调整**：30 → 38.9~~ ✓ 大幅提升！
2. **进一步提升市盈率阈值**：尝试50或更高
3. **添加其他条件**：换手率、ROE等
4. **调整持仓参数**：maxPositions、dailyBuyCount等

### G树分支探索记录
- G1分支（业绩预增/扭亏）：
  - iter1-10: 逐步优化到 score=2.2220
  - iter11: crash
  - iter12: score=3.5209（+流通市值<50亿）⭐
  - iter13-17: 多次失败后 score=3.5214
  - iter18: rollback（+净利润增长率>30%）
  - iter19: score=4.9519（市盈率30→38.9）⭐⭐
- G2-G5分支：待探索

### 规律总结
- champion_score: 4.9519（大幅提升！）
- 关键发现：市盈率阈值提升到38.9显著提升score
- 年化收益从100%提升到200%
- 市盈率放宽反而有效，说明事件股成长性强，应给予更高估值容忍度

### 下一步方向
- 尝试进一步提升市盈率阈值到50
- 或尝试添加其他有效条件
