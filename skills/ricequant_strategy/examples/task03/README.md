# 任务03：二板接力卖出规则测试 - 执行指南

**执行方式**: 四阶段流程（优先 RiceQuant Notebook）⭐

---

## 一、策略阶段判断

**当前阶段**: 阶段2 - 新策略开发

**判断依据**:
- ✅ 因子简单：市值、涨停数、开盘价、收盘价等基础数据
- ✅ 新策略开发：测试不同卖出规则
- ✅ 推荐平台：**RiceQuant Notebook** ⭐

**平台优势**:
- Session 自动管理（无需手动抓取）
- Notebook 格式简单（直接执行 + print）
- 快速验证（测试2024年Q1数据）

---

## 二、执行步骤

### 步骤1: 确认文件准备

```bash
# 查看测试脚本
ls -la skills/ricequant_strategy/examples/task03/

# 应该看到5个文件：
# - sell_timing_test.py       (卖出时机测试)
# - profit_target_test.py     (止盈规则测试)
# - stop_loss_test.py         (止损规则测试)
# - holding_period_test.py    (持仓周期测试)
# - circuit_breaker_test.py   (熔断规则测试)
```

### 步骤2: 进入 RiceQuant Skill 目录

```bash
cd skills/ricequant_strategy
```

### 步骤3: 确认环境配置

```bash
# 检查 .env 文件
cat .env

# 应该包含：
# RICEQUANT_USERNAME=your_username
# RICEQUANT_PASSWORD=your_password
```

### 步骤4: 运行测试脚本

#### 4.1 卖出时机测试（预计5分钟）

```bash
node run-strategy.js \
  --strategy ./examples/task03/sell_timing_test.py \
  --create-new \
  --timeout-ms 300000
```

**预期输出**:
```
任务03-提示词3.1：卖出时机对比测试（RiceQuant Notebook）
测试期间: 2024年Q1, 共X个交易日
进度: 10/50
进度: 20/50
...
| 卖出时机 | 交易数 | 胜率 | 平均收益 | 最大收益 | 最小收益 |
|---------|--------|------|---------|---------|---------|
| 开盘卖出 | X | X% | X% | X% | X% |
| 收盘卖出 | X | X% | X% | X% | X% |
| 最高价卖出 | X | X% | X% | X% | X% |
```

#### 4.2 止盈规则测试（预计5分钟）

```bash
node run-strategy.js \
  --strategy ./examples/task03/profit_target_test.py \
  --create-new \
  --timeout-ms 300000
```

#### 4.3 止损规则测试（预计5分钟）

```bash
node run-strategy.js \
  --strategy ./examples/task03/stop_loss_test.py \
  --create-new \
  --timeout-ms 300000
```

#### 4.4 持仓周期测试（预计5分钟）

```bash
node run-strategy.js \
  --strategy ./examples/task03/holding_period_test.py \
  --create-new \
  --timeout-ms 300000
```

#### 4.5 熔断规则测试（预计5分钟）

```bash
node run-strategy.js \
  --strategy ./examples/task03/circuit_breaker_test.py \
  --create-new \
  --timeout-ms 300000
```

### 步骤5: 查看结果

```bash
# 查看最新结果
cat data/ricequant-notebook-result-*.json | tail -n 100

# 或查看特定时间的结果
ls -lt data/ricequant-notebook-result-*.json | head -n 5
```

---

## 三、测试内容总结

### 1. 卖出时机测试
- 次日开盘卖出
- 次日收盘卖出
- 次日最高价卖出（理想上限）

### 2. 止盈规则测试
- 无止盈
- +5%止盈
- +10%止盈

### 3. 止损规则测试
- 无止损
- -5%止损
- -10%止损

### 4. 持仓周期测试
- T+1卖出
- T+2卖出
- T+1或T+2（涨停持有）

### 5. 熔断规则测试
- 无熔断
- 单票亏损10%熔断
- 近10日胜率<50%降仓

---

## 四、预期时间

| 测试项目 | 预计时间 | 累计时间 |
|---------|---------|---------|
| 卖出时机测试 | 5分钟 | 5分钟 |
| 止盈规则测试 | 5分钟 | 10分钟 |
| 止损规则测试 | 5分钟 | 15分钟 |
| 持仓周期测试 | 5分钟 | 20分钟 |
| 熔断规则测试 | 5分钟 | 25分钟 |

**总计**: 约25分钟

---

## 五、常见问题

### Q1: 超时怎么办？
**A**: 增加 `--timeout-ms` 参数
```bash
node run-strategy.js --strategy ./test.py --timeout-ms 600000  # 10分钟
```

### Q2: 无输出怎么办？
**A**: 检查脚本是否包含足够的 print 语句

### Q3: API 报错怎么办？
**A**: 确认使用的是 RiceQuant API，不是 JoinQuant API

### Q4: Session 过期怎么办？
**A**: RiceQuant 会自动处理 Session，无需手动抓取

---

## 六、下一步计划

### 阶段2（当前）
1. ✅ 创建测试脚本
2. ⏳ 运行5个测试
3. ⏳ 分析测试结果

### 阶段3（后续）
1. 将最佳方案转换为策略编辑器格式
2. 运行完整回测（2021-2024年）
3. 获取完整风险指标

### 阶段4（最终验证）
1. 在 JoinQuant 网页平台运行
2. 验证最终结果

---

## 七、参考文档

- 回测平台指南: `skills/backtest_guide/SKILL.md`
- RiceQuant API: `skills/ricequant_strategy/README.md`
- JQ→RQ 迁移指南: `skills/backtest_guide/reference/jq_to_rq_migration.md`

---

**创建时间**: 2026-04-01
**预计完成**: 25分钟
**状态**: 准备就绪 ⭐