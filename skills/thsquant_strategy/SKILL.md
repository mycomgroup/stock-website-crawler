# 同花顺量化 (THSQuant) 策略运行器

## 快速开始

```bash
# 1. 配置环境变量（.env）
THSQUANT_USERNAME=mx_kj1ku00qp
THSQUANT_PASSWORD=f09173228552

# 2. 运行策略
node run-skill.js --id <strategyId> --file path/to/strategy.py

# 3. 查看结果
cat data/thsquant-backtest-*.json
```

## 参数说明

```bash
node run-skill.js --id <strategyId> --file <path> [options]

必需参数：
  --id <id>          策略 ID
  --file <path>      本地策略文件路径

可选参数：
  --start <date>     回测开始日期 (YYYY-MM-DD)，默认: 2023-01-01
  --end <date>       回测结束日期 (YYYY-MM-DD)，默认: 2024-12-31
  --capital <num>    初始资金，默认: 100000
  --freq <string>    频率 (1d/1h/1m)，默认: 1d
  --benchmark <id>   基准指数，默认: 000001.SH
```

## API 端点

同花顺量化使用以下端点：
- `GET /api/user/info` - 获取用户信息
- `GET /api/strategy/list` - 获取策略列表
- `GET /api/strategy/{id}` - 获取策略详情
- `POST /api/strategy/{id}/save` - 保存策略代码
- `POST /api/backtest/run` - 运行回测
- `GET /api/backtest/{id}/result` - 获取回测结果
- `GET /api/backtest/{id}/risk` - 获取风险指标

## 文件结构

```
thsquant_strategy/
├── .env                    # 账号配置
├── browser/
│   ├── capture-session.js  # Session 捕获
│   └── session-manager.js  # Session 管理
├── request/
│   └── thsquant-client.js  # HTTP 客户端
├── examples/
│   ├── simple_strategy.py  # 简单策略示例
│   └── ma_strategy.py      # 双均线策略
├── data/
│   └── session.json        # 保存的 session
├── run-skill.js            # CLI: 运行回测
├── list-strategies.js      # CLI: 列出策略
├── fetch-report.js         # CLI: 获取报告
└── SKILL.md               # 本文档
```

## Session 管理

系统会自动管理 session：
1. 检查现有 session 是否有效
2. 如果无效，自动启动浏览器登录
3. 登录成功后保存 session
4. 后续运行自动复用 session（7天有效期）

测试 session 状态：
```bash
npm run test-session
```

## 示例策略

| 文件 | 说明 |
|------|------|
| `examples/simple_strategy.py` | 基础策略测试 |
| `examples/ma_strategy.py` | 双均线策略 |

## 注意事项

- 同花顺量化平台可能有每日回测时间限制
- Session 有效期约 7 天，过期后自动重新登录
- 支持的频率：1d (日线), 1h (小时线), 1m (分钟线)
- 基准指数：000001.SH (上证指数), 399001.SZ (深证成指), 000300.SH (沪深300)