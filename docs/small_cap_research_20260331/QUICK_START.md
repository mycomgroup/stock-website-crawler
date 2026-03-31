# 快速开始指南

## 一、环境准备

### 1. 配置RiceQuant账号

创建 `.env` 文件：

```bash
cd skills/ricequant_strategy
cat > .env << EOF
RICEQUANT_USERNAME=your_username
RICEQUANT_PASSWORD=your_password
RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research
EOF
```

### 2. 安装依赖

```bash
cd skills/ricequant_strategy
npm install
```

## 二、执行方式

### 方式1：一键执行所有步骤

```bash
cd docs/small_cap_research_20260331
./run_all_steps.sh
```

### 方式2：单独执行某个步骤

```bash
cd skills/ricequant_strategy

# Step 1: 国九条筛选验证
node run-strategy.js \
    --strategy "../docs/small_cap_research_20260331/step1_guojutiao_filter.py" \
    --timeout-ms 300000 \
    --create-new

# Step 2: 因子有效性测试
node run-strategy.js \
    --strategy "../docs/small_cap_research_20260331/step2_factor_test.py" \
    --timeout-ms 600000 \
    --create-new

# Step 3: 机器学习模型
node run-strategy.js \
    --strategy "../docs/small_cap_research_20260331/step3_ml_model.py" \
    --timeout-ms 600000 \
    --create-new

# Step 4: 策略回测
node run-strategy.js \
    --strategy "../docs/small_cap_research_20260331/step4_backtest.py" \
    --timeout-ms 600000 \
    --create-new
```

## 三、查看结果

执行完成后，结果保存在：

```bash
# RiceQuant Notebook输出
ls -la skills/ricequant_strategy/data/ricequant-notebook-result-*.json

# Notebook快照
ls -la skills/ricequant_strategy/data/ricequant-notebook-*.ipynb
```

### 查看JSON结果

```bash
cat skills/ricequant_strategy/data/ricequant-notebook-result-*.json | jq .
```

## 四、预期时间

| 步骤 | 内容 | 预计时间 |
|------|------|---------|
| Step 1 | 国九条筛选 | 1-2分钟 |
| Step 2 | 因子测试 | 3-5分钟 |
| Step 3 | 机器学习 | 3-5分钟 |
| Step 4 | 策略回测 | 5-10分钟 |
| **总计** | - | **12-22分钟** |

## 五、常见问题

### Q1: Session过期怎么办？

RiceQuant会自动处理session，如果过期会自动重新登录。

### Q2: 执行超时怎么办？

增加timeout参数：

```bash
node run-strategy.js --strategy step2_factor_test.py --timeout-ms 900000
```

### Q3: 如何调试？

查看Notebook快照：

```bash
# Notebook文件在
skills/ricequant_strategy/data/ricequant-notebook-*.ipynb
```

### Q4: API差异？

RiceQuant API与JoinQuant略有不同：

| 功能 | JoinQuant | RiceQuant |
|------|-----------|-----------|
| 获取所有股票 | `get_all_securities("stock", date)` | `get_all_securities(["stock"])` |
| 指数成分股 | `get_index_stocks(index, date)` | `index_components(index)` |
| 历史行情 | `get_price(stocks, end_date, count)` | `history_bars(stock, bar_count, frequency, fields)` |

## 六、下一步

1. 分析各步骤输出结果
2. 根据因子IC值优化因子选择
3. 调整策略参数
4. 在RiceQuant策略编辑器中进行精确回测
5. 实盘模拟验证

---

**祝研究顺利！**