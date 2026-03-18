# Web API 数据与页面比对说明文档 (EODHD API 示例)

## 1. 基本信息
- **任务类别**: API 接口数据验证
- **目标平台/站点**: EOD Historical Data (EODHD)
- **API 接口地址**: `[GET] https://eodhd.com/api/real-time/AAPL.US?api_token=demo&fmt=json`
- **对应 Web 页面**: `https://eodhd.com/financial-summary/AAPL.US` (股票详情与实时报价页)
- **测试时间**: 2026-03-17
- **测试人员**: Trae AI

## 2. 比对目标
通过直接调用 EODHD 的实时行情 API，提取核心数据结构，并与前端页面的图表/报价面板进行逐一比对，评估 API 数据的**全面性**、**可用性**。

## 3. 核心字段映射与比对

| Web 页面展示字段 | API 响应字段 (JSON Key) | 数据类型 | 比对结果 (一致/需转换/缺失) | 备注/转换规则说明 |
| :--- | :--- | :--- | :--- | :--- |
| **股票代码/名称** | `code` | String | 一致 | 返回如 "AAPL.US" |
| **最新价格 (Current Price)** | `close` | Number | 一致 | 直接对应页面的最新成交价 |
| **涨跌幅 (Change %)** | `change_p` | Number | 需转换 | 页面显示为 `+1.25%`，API 返回 `1.25`，需补充百分号和正负号 |
| **交易量 (Volume)** | `volume` | Number | 需转换 | 页面显示为 `54.2M`，API 返回 `54200000`，需进行单位换算 (K/M/B) |
| **更新时间 (Timestamp)** | `timestamp` | Long | 需转换 | API 返回 Unix 时间戳，前端显示为具体美东时间 (EST) |
| **日高/日低 (High/Low)** | `high` / `low` | Number | 一致 | |

## 4. API 隐藏高价值字段分析
*（记录页面上没有展示，但 API 返回的对分析有用的额外数据）*
- **隐藏字段 1**: `gmtoffset` - 用于确定数据所属时区的偏移量（如 0 代表 GMT）。这在页面上不可见，但对本地时间转换极其重要。
- **隐藏字段 2**: `previousClose` - 昨收价，API 显式提供此字段，方便快速计算各类技术指标，无需再发起历史数据请求。

## 5. 接口调用限制与反爬机制
- **鉴权要求 (Auth)**: 必需在 Query String 中携带 `api_token` 参数，否则返回 `401 Unauthorized`。
- **请求频次限制 (Rate Limit)**: 取决于订阅层级。普通版限制为 100000 次/天，并发请求不可过高（建议 < 10 req/sec）。
- **参数动态性**: 无动态加密参数，接口格式标准、稳定。

## 6. 结论与后续接入方案
### 6.1 结论概览
EODHD API 提供的数据**高度规整、结构化良好**，完全覆盖了前端页面的展示需求，甚至提供了诸如 `previousClose` 等便利的计算字段。无需处理复杂的反爬，是非常理想的数据获取途径。

### 6.2 接入策略建议 (Next Steps)
- [x] **纯 API 直接接入**: **推荐**。数据完整且鉴权简单，使用原生的 Node.js HTTP 客户端或 Axios 即可。
- [ ] **模拟浏览器抓取 API**: 不需要，官方开放了标准 API，无需拦截 Network。
- [ ] **需进一步逆向分析**: 不需要。

---
**附录：API 请求参数与响应结构示例**
### 响应体 (Response JSON)
```json
{
  "code": "AAPL.US",
  "timestamp": 1679058000,
  "gmtoffset": 0,
  "open": 150.5,
  "high": 153.2,
  "low": 149.8,
  "close": 152.4,
  "volume": 54200000,
  "previousClose": 150.0,
  "change": 2.4,
  "change_p": 1.6
}
```