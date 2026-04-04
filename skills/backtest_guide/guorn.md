# GuornQuant（果仁网）回测指南

目录：`skills/guorn_strategy/`

---

## 核心限制

果仁网回测有两个重要限制：

1. **回测必须通过浏览器 JS 执行**：直接 HTTP POST 到 `/stock/runtest` 会返回 Server Error，必须通过页面内的 `scrat.utility.ajaxDispatch` 调用
2. **结果不持久化**：回测结果直接返回给前端，没有 backtestId，每次结果保存在本地 `output/backtest-{timestamp}.json`

---

## 环境配置

```bash
cd skills/guorn_strategy
npm install
```

`.env` 需要：
```
GUORN_USERNAME=your_username
GUORN_PASSWORD=your_password
```

账号限制：level=1 普通账号回测时间窗口约 1 年内。

---

## 运行回测

```bash
node run-skill.js
# 结果保存在 output/backtest-{timestamp}.json
```

回测配置在 `run-skill.js` 中修改，或通过 `strategyConfig` 传入：

```javascript
// 策略配置示例
const strategyConfig = {
  filters: [
    { id: '0.M.股票每日指标_市净率.0', min: 0, max: 2 }  // PB < 2
  ],
  ranks: [
    { id: '0.M.股票每日指标_中性ROE.0', order: 'desc' }  // ROE 降序
  ],
  pool: '',           // 股票池（空=全市场）
  count: '10',        // 持仓数量
  period: 5,          // 调仓周期（交易日）
};

const backtestConfig = {
  start: '2024-01-01',
  end: '2025-01-01',
  trade_cost: 0.002,
  benchmark: '000300',  // 沪深300
};
```

---

## 常用因子 ID

```javascript
// 从 /stock/meta 获取，格式：0.M.股票每日指标_{指标名}.0
const FACTOR_IDS = {
  ROA:      '0.M.股票每日指标_中性ROA.0',
  ROE:      '0.M.股票每日指标_中性ROE.0',
  PE:       '0.M.股票每日指标_市盈率.0',
  PB:       '0.M.股票每日指标_市净率.0',
  MOMENTUM: '0.M.股票每日指标_动量.0',
};
```

完整因子列表通过 API 获取：
```bash
# 在 browser 中执行
node browser/probe-backtest-api.js
```

---

## 查询历史结果

果仁网没有服务端持久化，历史结果只能查本地文件：

```bash
ls output/backtest-*.json | sort -r | head -5
# 查看最近 5 次结果

cat output/backtest-{timestamp}.json | node -e "
const d = JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
const s = d.data?.trade_summary || {};
console.log('年化收益:', s.winsorize_annual);
console.log('信息比率:', s.year_information_ratio);
console.log('最大回撤天数:', s.maxdrop_day);
"
```

---

## 文件结构

```
guorn_strategy/
├── .env                              # 账号配置
├── run-skill.js                      # 回测入口
├── request/
│   ├── guorn-strategy-client.js      # HTTP 客户端
│   ├── strategy-runner.js            # 完整工作流（含浏览器执行）
│   └── ensure-session.js             # Session 管理
├── browser/
│   └── probe-backtest-api.js         # 探测 API
└── output/                           # 回测结果（本地保存）
```

---

## 常见问题

**Q: 直接 HTTP POST 返回 Server Error**
果仁网的回测 API 必须通过浏览器 JS 调用，不能直接 HTTP POST。`strategy-runner.js` 已处理这个问题，使用 Playwright 在浏览器中执行。

**Q: 回测时间窗口限制**
level=1 账号只能回测约 1 年内的数据。如需更长时间窗口，需要升级账号。

**Q: 找不到历史回测结果**
果仁网结果不持久化，只有本地 `output/` 目录下的 JSON 文件。建议每次回测后立即记录关键指标。
