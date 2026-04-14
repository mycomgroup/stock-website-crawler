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
- [add_formula_condition] 添加流通市值小于50亿：score 2.2220 → 3.5209 ⭐ 大幅提升！回撤从11%→7%

### 已验证无效/崩溃（rollback/crash）
- [adjust_stop_loss] 止损 12% → 9%：rollback
- [adjust_trailing_stop] 追踪止损 10% → 8%：rollback
- [adjust_max_positions] 最大持仓 6 → 2：score 大幅下降到 -0.954
- [adjust_take_profit] 止盈 25% → 20%：rollback
- [adjust_days_for_sale] 持仓天数 2,4 → 2：rollback
- [add_formula_condition] 营业收入增长率大于15%：crash（问句回测失败）

### 待探索方向
1. ~~**添加估值保护**：市盈率小于30~~ ✓ 已keep
2. ~~**添加成交额条件**：成交额大于5000万~~ ✓ 已keep
3. ~~**移除非ST条件**：简化公式~~ ✓ 已keep
4. ~~**添加流通市值限制**：流通市值小于50亿~~ ✓ 大幅提升！
5. **添加换手率条件**：换手率大于5%
6. **进一步缩小市值**：流通市值小于30亿
7. **添加roe条件**：净资产收益率大于10%

### G树分支探索记录
- G1分支（业绩预增/扭亏）：
  - iter1: score=1.8711（追踪止损8%→10%）
  - iter2: score=2.2215（+市盈率小于30）
  - iter3-9: 多次rollback
  - iter10: score=2.2220（-非ST）
  - iter11: crash（+营业收入增长率>15%）
  - iter12: score=3.5209（+流通市值小于50亿）⭐
- G2-G5分支：待探索

### 规律总结
- champion_score: 3.5209（大幅提升！）
- 关键发现：流通市值小于50亿条件显著提升score，降低回撤
- 中小市值事件股弹性更大，效果更好
- 简化公式有效，但添加合适条件提升更显著

### 下一步方向
- 尝试进一步缩小市值（小于30亿）或添加ROE条件
