# AllTick API 使用指南

## 简介

AllTick 提供完整的金融市场Tick数据解决方案，涵盖外汇、港股CFD、美股CFD、商品和加密货币等领域的行情数据接口。

**官方网站**: https://alltick.co/
**GitHub**: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api

## 免费使用说明

### 免费试用
- 注册后获得 **7 天免费试用期**
- 试用期内可无限制访问所有 API 接口
- 试用期结束后可联系客服申请延长

### 免费计划（长期可用）
免费计划包含 **9 个核心接口**，覆盖主要行情数据需求：

#### HTTP 接口（6个）
| 接口 | 功能 | 免费限制 |
|------|------|----------|
| `/kline` | 单产品历史K线查询 | 每10秒1次，最多500根K线 |
| `/batch-kline` | 批量查询最新2根K线 | 每10秒1次，最多5组产品 |
| `/depth-tick` | 最新盘口深度查询 | 每10秒1次，最多5个code |
| `/trade-tick` | 最新成交价查询 | 每10秒1次，最多5个code |
| `/static_info` | 产品基础信息查询 | 每10秒1次，最多5个code |
| `/api/suspension/*` | 停牌信息查询 | 每1分钟1次 |

#### WebSocket 接口（3个）
| cmd_id | 功能 | 免费限制 |
|--------|------|----------|
| 22000 | 心跳(Ping/Pong) | 每10秒发送一次 |
| 22002 | 盘口订阅(深度数据) | 最多订阅5个产品 |
| 22004 | 成交订阅(实时Tick) | 最多订阅5个产品 |

#### 免费计划总体限制
- **HTTP**: 所有接口相加，1分钟最大10次，每天最多14,400次
- **WebSocket**: 只能建立1个连接
- **数据覆盖**: 支持外汇、贵金属、加密货币、港股、美股等全品类

### 付费计划对比
如需更高频率或更多产品订阅，可升级至：
- **基础计划**: 每秒1次请求，1个WebSocket连接
- **高级计划**: 每秒10次请求，3个WebSocket连接
- **专业计划**: 每秒20次请求，10个WebSocket连接
- **全市场计划**: 港股/A股/美股全部数据，每秒20次请求

## 支持的产品类型

1. **外汇**: USDJPY、EURUSD等
2. **股票CFD**: AAPL、TSLA等美股/港股
3. **贵金属**: GOLD、USOIL、Silver等
4. **加密货币**: BTCUSDT、ETHUSDT等
5. **全球指数**: 道琼斯指数、标普500等

## 接入流程

1. **熟悉接口地址和参数**
2. **申请Token** (https://alltick.co/register)
3. **了解接口调用限制**
4. **掌握请求与响应格式**
5. **选择目标产品代码**
6. **执行请求并获取数据**

## API 基础地址

### HTTP API

**外汇/加密货币/贵金属**:
- API地址: `https://quote.alltick.co/quote-b-api`

**股票**:
- API地址: `https://quote.alltick.co/quote-stock-b-api`

### WebSocket API

**外汇/加密货币/贵金属**:
- WebSocket地址: `wss://quote.alltick.co/quote-b-ws-api`

**股票**:
- WebSocket地址: `wss://quote.alltick.co/quote-stock-b-ws-api`

## HTTP API 接口

### 通用请求格式

所有HTTP请求使用GET方法，URL参数包含：
- `token`: 您的API Token
- `query`: URL编码的JSON查询参数

### 主要接口

#### 1. 单产品历史K线查询
- **URL**: `/{base_url}/kline`
- **方法**: GET
- **查询参数**:
  ```json
  {
    "trace": "request_id",
    "data": {
      "code": "700.HK",
      "kline_type": 1,
      "kline_timestamp_end": 0,
      "query_kline_num": 10,
      "adjust_type": 0
    }
  }
  ```

#### 2. 最新盘口(深度)查询
- **URL**: `/{base_url}/depth-tick`
- **方法**: GET
- **查询参数**:
  ```json
  {
    "trace": "request_id",
    "data": {
      "symbol_list": [
        {"code": "700.HK"},
        {"code": "UNH.US"}
      ]
    }
  }
  ```

#### 3. 最新成交价查询
- **URL**: `/{base_url}/trade-tick`
- **方法**: GET
- **查询参数**:
  ```json
  {
    "trace": "request_id",
    "data": {
      "symbol_list": [
        {"code": "700.HK"},
        {"code": "UNH.US"}
      ]
    }
  }
  ```

## WebSocket API 接口

### 连接方式

```
wss://quote.alltick.co/quote-stock-b-ws-api?token=YOUR_TOKEN
```

### 消息格式

所有消息使用JSON格式：

```json
{
  "cmd_id": 22002,
  "seq_id": 123,
  "trace": "uuid_trace_id",
  "data": {
    "symbol_list": [
      {"code": "700.HK", "depth_level": 5}
    ]
  }
}
```

### 主要命令

| cmd_id | 功能 |
|--------|------|
| 22000 | 心跳(Ping/Pong) |
| 22002 | 盘口订阅(深度数据) |
| 22003 | 成交订阅(实时Tick) |
| 22004 | 取消订阅 |

### WebSocket 心跳

必须每10秒发送一次心跳以保持连接：

```json
{
  "cmd_id": 22000,
  "seq_id": 123,
  "trace": "trace_id",
  "data": {}
}
```

## 请求示例

### Python HTTP 示例

```python
import requests
import json

# 构建查询参数
query = {
    "trace": "python_http_test1",
    "data": {
        "code": "AAPL.US",
        "kline_type": 1,
        "kline_timestamp_end": 0,
        "query_kline_num": 10,
        "adjust_type": 0
    }
}

# 编码查询参数
import urllib.parse
query_str = urllib.parse.quote(json.dumps(query))

# 发送请求
url = f'https://quote.alltick.co/quote-stock-b-api/kline?token=YOUR_TOKEN&query={query_str}'
response = requests.get(url)
data = response.json()
```

### Python WebSocket 示例

```python
import websocket
import json

def on_open(ws):
    # 发送订阅请求
    sub_param = {
        "cmd_id": 22002,
        "seq_id": 123,
        "trace": "trace_id",
        "data": {
            "symbol_list": [
                {"code": "700.HK", "depth_level": 5}
            ]
        }
    }
    ws.send(json.dumps(sub_param))

def on_message(ws, message):
    print(f"Received: {message}")

# 连接WebSocket
ws = websocket.WebSocketApp(
    'wss://quote.alltick.co/quote-stock-b-ws-api?token=YOUR_TOKEN',
    on_open=on_open,
    on_message=on_message
)
ws.run_forever()
```

### cURL HTTP 示例

```bash
# 单产品K线查询
curl -X GET "https://quote.alltick.co/quote-stock-b-api/kline?token=YOUR_TOKEN&query=%7B%22trace%22%3A%22test%22%2C%22data%22%3A%7B%22code%22%3A%22AAPL.US%22%2C%22kline_type%22%3A1%2C%22kline_timestamp_end%22%3A0%2C%22query_kline_num%22%3A10%2C%22adjust_type%22%3A0%7D%7D"

# 盘口查询
curl -X GET "https://quote.alltick.co/quote-stock-b-api/depth-tick?token=YOUR_TOKEN&query=%7B%22trace%22%3A%22test%22%2C%22data%22%3A%7B%22symbol_list%22%3A%5B%7B%22code%22%3A%22700.HK%22%7D%5D%7D%7D"
```

## K线类型说明

| kline_type | 说明 |
|------------|------|
| 1 | 1分钟K线 |
| 2 | 5分钟K线 |
| 3 | 15分钟K线 |
| 4 | 30分钟K线 |
| 5 | 1小时K线 |
| 6 | 2小时K线 |
| 7 | 4小时K线 |
| 8 | 日K线 |
| 9 | 周K线 |
| 10 | 月K线 |

## 产品代码格式

- **美股**: `AAPL.US`, `TSLA.US`, `UNH.US`
- **港股**: `700.HK`, `3690.HK`
- **加密货币**: `BTCUSDT`, `ETHUSDT`
- **外汇**: `EURUSD`, `USDJPY`
- **贵金属**: `GOLD`, `SILVER`, `USOIL`

## 接口限制

- **HTTP接口**: 需要注意请求频率限制
- **WebSocket接口**: 需要定期发送心跳(每10秒)
- 具体限制请参考官方文档

## 响应格式

### 成功响应

```json
{
  "ret": 200,
  "msg": "ok",
  "trace": "request_id",
  "data": {
    // 具体数据
  }
}
```

### 错误响应

```json
{
  "ret": 400,
  "msg": "error_message",
  "trace": "request_id"
}
```

## 最佳实践

1. **保护Token**: 不要在前端代码中暴露Token
2. **错误处理**: 始终检查响应中的 `ret` 字段
3. **心跳维护**: WebSocket连接需要定期发送心跳
4. **请求频率**: 遵守接口调用限制，避免被封禁
5. **数据验证**: 验证返回数据的完整性和有效性

## 调试技巧

1. 使用curl命令快速测试API
2. 在浏览器开发者工具中查看WebSocket消息
3. 检查返回的错误码和错误信息
4. 使用 `trace` 字段追踪请求链路

## 常见问题

1. **连接断开**: 检查是否按时发送心跳
2. **数据为空**: 检查产品代码是否正确
3. **认证失败**: 检查Token是否有效
4. **请求被拒绝**: 检查是否超出频率限制

## 文档参考

- **API文档**: https://apis.alltick.co/
- **Token申请**: https://alltick.co/register
- **GitHub示例**: https://github.com/alltick/realtime-forex-crypto-stock-tick-finance-websocket-api

---

*最后更新: 2026-03-25*
