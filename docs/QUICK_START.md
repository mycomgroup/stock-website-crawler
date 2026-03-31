# 快速开始 - RiceQuant 策略迁移

## 🎯 立即开始

### 步骤 1: 配置环境

```bash
# 编辑 .env 文件
vim /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy/.env
```

添加以下内容：
```env
RICEQUANT_USERNAME=your_username
RICEQUANT_PASSWORD=your_password
RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research
```

### 步骤 2: 运行第一个策略

```bash
# 进入目录
cd /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy

# 运行小市值策略（最简单）
node run-strategy.js --strategy ../../strategies/Ricequant/migrated/01_small_cap_strategy.py
```

### 步骤 3: 查看结果

```bash
# 查看最新结果
ls -lt data/ricequant-notebook-result-*.json | head -1

# 查看内容
cat data/ricequant-notebook-result-*.json | grep -A 5 "executions"
```

---

## 📋 可用的 5 个策略

```bash
# 1. 小市值成长股策略（推荐新手）
node run-strategy.js --strategy ../../strategies/Ricequant/migrated/01_small_cap_strategy.py

# 2. 股息率价值策略
node run-strategy.js --strategy ../../strategies/Ricequant/migrated/02_dividend_strategy.py

# 3. ETF动量轮动策略
node run-strategy.js --strategy ../../strategies/Ricequant/migrated/03_etf_momentum.py

# 4. 龙头底分型战法
node run-strategy.js --strategy ../../strategies/Ricequant/migrated/04_leader_fractal.py

# 5. 首板低开策略
node run-strategy.js --strategy ../../strategies/Ricequant/migrated/05_first_board_low_open.py
```

---

## 🚀 一键运行所有策略

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/strategies/Ricequant/migrated
./run_all.sh
```

---

## 📊 查看结果

### 方式 1: 命令行查看

```bash
# 列出所有结果文件
ls -lt data/ricequant-notebook-result-*.json

# 查看最新结果
cat data/ricequant-notebook-result-*.json | jq '.executions[0].textOutput'
```

### 方式 2: RiceQuant 平台查看

1. 访问 https://www.ricequant.com/research
2. 查看自动创建的 notebook
3. 点击查看详细结果

---

## 📚 文档资源

| 文档 | 位置 |
|------|------|
| API 能力 | `/docs/ricequant_api_summary.md` |
| 迁移计划 | `/docs/migration_plan.md` |
| 迁移总结 | `/docs/migration_summary.md` |
| 策略指南 | `/strategies/Ricequant/migrated/README.md` |

---

## ⚡ 常见问题

### Q: Session 过期怎么办？
**A**: 自动处理，无需手动干预。如果登录失败会自动重新登录。

### Q: 运行很慢怎么办？
**A**: 策略中已经限制了股票数量（通常100只），如果还是很慢可以减少到50只。

### Q: 没有输出结果？
**A**: 检查 `.env` 文件配置是否正确，确保账号密码无误。

---

## 💡 提示

- ✅ 推荐从 **小市值策略** 开始测试
- ✅ 每次运行会自动创建新的 notebook
- ✅ 结果文件包含完整执行日志
- ✅ Session 自动管理，无需手动登录

---

**现在就开始**: 复制并运行第一行命令！