# 重试与超时策略

所有平台的 HTTP 客户端（`request/` 目录下的 `*-client.js`）均已实现统一的重试策略。

---

## 重试规则

| 错误类型 | 触发条件 | 第1次等待 | 第2次等待 | 第3次等待 |
|---------|---------|---------|---------|---------|
| 并发限制 | HTTP 429 / 503 | 60s | 120s | 300s |
| 服务端错误 | HTTP 5xx（非503） | 10s | 20s | 40s |
| 网络/超时 | AbortError / ECONN / ECONNRESET | 5s | 10s | 20s |
| 客户端错误 | HTTP 4xx（非429） | 不重试 | — | — |

最多重试 3 次，超过后抛出错误。

---

## 请求超时

每个请求默认 30 秒超时（通过 `AbortController` 实现）。超时后触发网络错误重试逻辑（5s/10s/20s）。

RiceQuant 支持自定义超时：
```javascript
await client.request(url, { timeoutMs: 60000 });
```

---

## 并发限制说明

各平台对同时运行的回测数量有限制：

| 平台 | 并发限制 | 处理方式 |
|------|---------|---------|
| RiceQuant | 约 3 个 | `--wait-if-full` 参数自动等待 |
| JoinQuant | 未知 | 429 时自动重试 |
| THSQuant | 未知 | 429/503 时自动重试 |
| BigQuant | 按资源规格 | 自动选择可用资源 |

---

## 实现位置

```
skills/ricequant_strategy/request/ricequant-client.js    → retryDelay() / networkRetryDelay()
skills/joinquant_strategy/request/joinquant-strategy-client.js
skills/thsquant_strategy/request/thsquant-client.js
skills/bigquant_strategy/request/bigquant-client.js
```

四个文件的重试逻辑完全一致，修改时需同步更新。

---

## 日志格式

重试时会打印：
```
[Retry 1/3] HTTP 429, waiting 60s...
[Retry 2/3] HTTP 429, waiting 120s...
[Retry 1/3] timeout(30000ms), waiting 5s...
```
