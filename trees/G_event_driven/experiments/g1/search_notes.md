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
- [adjust_formula_threshold] 市盈率 30 → 38.9：score 3.5214 → 4.9519 ⭐⭐
- [adjust_formula_threshold] 市盈率 38 → 49：score 4.9519 → 7.0946 ⭐⭐⭐

### 已验证无效/崩溃（rollback/crash）
- [adjust_stop_loss] 止损 12% → 9%：rollback
- [adjust_trailing_stop] 追踪止损 10% → 8%：rollback
- [adjust_max_positions] 最大持仓 6 → 2：score 大幅下降到 -0.954
- [adjust_take_profit] 止盈 25% → 20%：rollback
- [adjust_days_for_sale] 持仓天数 2,4 → 2：rollback
- [add_formula_condition] 营业收入增长率大于15%：crash
- [add_formula_condition] 市盈率 30 → 22.4：crash
- [add_formula_condition] 净利润增长率大于30%：rollback
- [筛选阈值] 市盈率 49 → 51.8：rollback（PE 49为最优）
- 多处crash：请求太频繁（rate limit）

### 待探索方向
1. ~~**市盈率阈值调整**：30 → 38.9 → 49~~ ✓ 最优区间
2. ~~**流通市值限制**：小于50亿~~ ✓ 已验证有效
3. **调整持仓参数**：trailing stop, stop loss等
4. **尝试添加其他条件**：需避免与现有条件冲突
5. ~~**移除股价近20日涨幅小于15%**~~ ✓ 移除后 score 7.0946 → 12.4522 ⭐⭐⭐⭐

### 新发现（iter29）
- 移除"股价近20日涨幅小于15%"条件后，score 大幅提升 7.0946 → 12.4522
- 说明追涨事件股并未如预期导致收益下降，反而提供了更大的上涨空间

### G树分支探索记录
- G1分支（业绩预增/扭亏）：
  - iter1-10: 逐步优化到 score=2.2220
  - iter12: score=3.5209（+流通市值<50亿）⭐
  - iter17: score=3.5214
  - iter19: score=4.9519（市盈率30→38.9）⭐⭐
  - iter20: score=7.0946（市盈率38→49）⭐⭐⭐
  - iter21: rollback（市盈率49→51.8）
  - iter22-27: 多处crash（rate limit）
- G2-G5分支：待探索

### 规律总结
- champion_score: 7.0946
- 市盈率阈值49为最优
- 流通市值小于50亿条件有效
- trailing stop 5%最优
- rate limiting严重，多次crash

### 当前配置（champion）
- formula: 中报预增, 净利润预增上限大于50%, 市盈率小于49.0, 成交额大于5000万, 流通市值小于50亿, 股价近20日涨幅小于15%
- trailingStopLoss: 5%
- stopLoss: 12%
- takeProfit: 25%
- daysForSaleStrategy: 2,4
- maxPositions: 6
- dailyBuyCount: 3
