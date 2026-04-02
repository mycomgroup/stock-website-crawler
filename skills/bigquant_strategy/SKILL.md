---
name: bigquant-strategy
description: 在 BigQuant AIStudio 中运行策略代码和回测
---

# BigQuant AIStudio 策略运行器

**核心功能：AI量化策略开发与回测**

## 快速开始

```bash
# 1. 配置环境变量（.env）
BIGQUANT_USERNAME=your_username
BIGQUANT_PASSWORD=your_password
BIGQUANT_STUDIO_URL=https://bigquant.com/aistudio/studios/xxx

# 2. 安装依赖
npm install

# 3. 运行策略回测
node run-skill.js --id <strategyId> --file examples/simple_backtest.py

# 4. 查看结果
cat data/bigquant-backtest-*.json
```

## Session 自动管理

**系统会自动处理 session，无需手动干预：**

1. **自动检查**：运行时检查现有 session 是否有效
2. **自动登录**：如果 session 无效，自动后台登录（headless模式）
3. **自动保存**：登录成功后自动保存 session
4. **自动复用**：后续运行自动复用有效 session

**首次运行时会自动登录，后续运行会自动复用 session（7天有效期）。**

手动捕获 session：
```bash
node browser/capture-session.js --headed
```

## 使用方式

### 1. 运行策略回测

```bash
# 使用策略ID和本地文件运行回测
node run-skill.js --id <strategyId> --file path/to/strategy.py

# 自定义回测参数
node run-skill.js --id <strategyId> --file path/to/strategy.py \
  --start 2022-01-01 \
  --end 2025-03-28 \
  --capital 200000 \
  --freq day \
  --benchmark 000300.XSHG
```

### 2. 列出所有策略

```bash
node list-strategies.js
```

### 3. 查看回测报告

```bash
node fetch-report.js --id <backtestId>
```

## 参数说明

```bash
node run-skill.js [参数]

必需参数：
  --id <strategyId>         策略ID
  --file <path>             本地策略文件路径

可选参数：
  --start <date>            回测开始日期（默认：2021-01-01）
  --end <date>              回测结束日期（默认：2025-03-28）
  --capital <num>           初始资金（默认：100000）
  --freq <string>           回测频率 day/minute（默认：day）
  --benchmark <id>          基准指数（默认：000300.XSHG）
  --headed                  使用可视化浏览器登录
```

## 示例策略

| 文件 | 说明 |
|------|------|
| `examples/simple_backtest.py` | 基础买入策略测试 |
| `examples/ma_strategy.py` | 双均线交叉策略 |

## 输出文件

```bash
data/
├── session.json                       # Session cookies
├── bigquant-backtest-<id>-<ts>.json   # 回测详细报告
└── login-*.png                        # 登录过程截图（调试用）
```

## API Endpoints

BigQuant 使用以下端点：
- `GET /api/user/current` - 获取用户信息
- `GET /api/aistudio/studios` - 获取 Studio 列表
- `GET /api/aistudio/studios/{id}/notebooks` - 列出策略
- `PUT /api/aistudio/studios/{id}/notebooks/{nbId}` - 保存策略
- `POST /api/backtest/run` - 运行回测
- `GET /api/backtest/results/{btId}` - 获取回测结果

## 文件结构

```
bigquant_strategy/
├── .env                    # 账号凭证
├── browser/
│   ├── capture-session.js  # Session 捕获
│   └── session-manager.js  # Session 管理
├── request/
│   └── bigquant-client.js  # HTTP API 客户端
├── examples/
│   ├── simple_backtest.py  # 简单策略示例
│   └── ma_strategy.py      # 双均线策略示例
├── data/
│   └── session.json        # 保存的 session
├── run-skill.js            # CLI: 运行回测
├── list-strategies.js      # CLI: 列出策略
├── paths.js                # 路径配置
├── load-env.js             # 环境变量加载
├── package.json            # 依赖配置
└── SKILL.md                # 本文档
```

## BigQuant API 特点

与 JoinQuant/RiceQuant 的差异：

| 特性 | BigQuant | JoinQuant | RiceQuant |
|------|----------|-----------|-----------|
| 初始化函数 | initialize() | initialize() | init() |
| 数据函数 | history() | attribute_history() | get_price() |
| 订单函数 | order_target_percent() | order_target_value() | order_shares() |
| 回测频率 | day/minute | day/minute | day/minute |
| Session管理 | 浏览器 | 浏览器 | API+浏览器 |

## 常见问题

### Session 过期

```bash
node browser/capture-session.js --headed
```

### 执行超时

增加等待时间或检查网络连接。

### API 端点变化

BigQuant API 可能更新，如遇错误请查看响应内容。

## 对接其他平台

参考本 skill 结构，可类似对接：
- `skills/joinquant_strategy` - 聚宽
- `skills/ricequant_strategy` - 米筐

## Notes

- BigQuant 使用 SPA 架构，需要浏览器登录
- Session cookies 存储在 `data/session.json`
- BigQuant 策略语法类似 JoinQuant
- 支持 AI 量化特性（机器学习等）

## 相关链接

- BigQuant 官网: https://bigquant.com
- API 文档: https://bigquant.com/wiki
- 策略社区: https://bigquant.com/alpha