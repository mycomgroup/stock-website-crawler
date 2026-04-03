---
id: "url-720517a9"
type: "api"
title: "K线推送(不支持)"
url: "https://apis.alltick.co/websocket-api/stock-websocket-interface-api/ping-pong-1"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T03:34:13.866Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["Websocket APIchevron-right","Websocket接口API"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"K线推送说明","content":[{"type":"text","value":"Alltick的WebSocket接口不支持K线数据的推送。由于许多客户对此有疑问，特此说明：无论是历史K线还是实时K线，目前仅支持通过HTTP接口直接获取。推荐的实现方式如下："},{"type":"text","value":"实现方式建议（仅供参考）："},{"type":"text","value":"1、定时拉取K线：为了实现K线的快速更新，建议购买高请求频率的套餐，以提高拉取频率。"},{"type":"text","value":"2、结合使用HTTP接口：建议客户将/kline和/batch-kline两个接口结合使用，具体步骤如下："},{"type":"code","language":"text","value":"/batch-kline"},{"type":"list","ordered":false,"items":["首先，通过/kline接口轮询请求历史数据并存储到本地数据库。后续的历史数据可直接从客户的数据库获取，无需再次通过接口请求。","然后，持续使用/batch-kline接口批量请求多个产品的最新两根K线，并将数据更新到数据库。"]},{"type":"code","language":"text","value":"/batch-kline"},{"type":"text","value":"这种方式能够快速更新最新的K线，同时避免频繁请求历史K线导致请求频率受到限制。"}]}
    - {"type":"heading","level":2,"title":"涨跌幅说明","content":[{"type":"text","value":"Alltick的接口不提供涨跌幅或24小时涨跌幅字段。客户可以通过获取Alltick的数据自行计算涨跌幅。"},{"type":"text","value":"1、每日涨跌幅计算方法："},{"type":"list","ordered":false,"items":["方法一：使用HTTP接口获取当天的日K线收盘价和前一日的日K线收盘价，计算公式如下："]},{"type":"text","value":"涨跌幅 = (当天收盘价 - 前一日收盘价) / 前一日收盘价 * 100%"},{"type":"list","ordered":false,"items":["方法二：使用WebSocket接口获取最新价格，并通过HTTP接口获取当天的日K线收盘价，计算公式如下："]},{"type":"text","value":"涨跌幅 = (最新价格 - 前一日收盘价) / 前一日收盘价 * 100%"},{"type":"text","value":"2、24小时涨跌幅计算方法："},{"type":"list","ordered":false,"items":["使用WebSocket的最新成交价格接口（请求-协议号：22004），实时接收逐笔成交价格（tick数据）。","需自行存储WebSocket接口推送的24小时前的最新价格，以便进行后续计算。","计算公式："]},{"type":"text","value":"24小时涨跌幅 = (最新价格 - 24小时前的最新价格) / 24小时前的最新价格 * 100%"}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于12个月前"}]}
  codeExamples:
    - {"type":"code","language":"text","value":"/batch-kline"}
    - {"type":"code","language":"text","value":"/batch-kline"}
  tables: []
  parameters: []
  markdownContent: "# K线推送(不支持)\n\n1. Websocket APIchevron-right\n1. Websocket接口API\n\nEnglish / 中文\n\n\n## K线推送说明\n\nAlltick的WebSocket接口不支持K线数据的推送。由于许多客户对此有疑问，特此说明：无论是历史K线还是实时K线，目前仅支持通过HTTP接口直接获取。推荐的实现方式如下：\n\n实现方式建议（仅供参考）：\n\n1、定时拉取K线：为了实现K线的快速更新，建议购买高请求频率的套餐，以提高拉取频率。\n\n2、结合使用HTTP接口：建议客户将/kline和/batch-kline两个接口结合使用，具体步骤如下：\n\n```text\n/batch-kline\n```\n\n- 首先，通过/kline接口轮询请求历史数据并存储到本地数据库。后续的历史数据可直接从客户的数据库获取，无需再次通过接口请求。\n- 然后，持续使用/batch-kline接口批量请求多个产品的最新两根K线，并将数据更新到数据库。\n\n```text\n/batch-kline\n```\n\n这种方式能够快速更新最新的K线，同时避免频繁请求历史K线导致请求频率受到限制。\n\n\n## 涨跌幅说明\n\nAlltick的接口不提供涨跌幅或24小时涨跌幅字段。客户可以通过获取Alltick的数据自行计算涨跌幅。\n\n1、每日涨跌幅计算方法：\n\n- 方法一：使用HTTP接口获取当天的日K线收盘价和前一日的日K线收盘价，计算公式如下：\n\n涨跌幅 = (当天收盘价 - 前一日收盘价) / 前一日收盘价 * 100%\n\n- 方法二：使用WebSocket接口获取最新价格，并通过HTTP接口获取当天的日K线收盘价，计算公式如下：\n\n涨跌幅 = (最新价格 - 前一日收盘价) / 前一日收盘价 * 100%\n\n2、24小时涨跌幅计算方法：\n\n- 使用WebSocket的最新成交价格接口（请求-协议号：22004），实时接收逐笔成交价格（tick数据）。\n- 需自行存储WebSocket接口推送的24小时前的最新价格，以便进行后续计算。\n- 计算公式：\n\n24小时涨跌幅 = (最新价格 - 24小时前的最新价格) / 24小时前的最新价格 * 100%\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于12个月前\n"
  rawContent: "复制\nWEBSOCKET API\nWEBSOCKET接口API\nK线推送(不支持)\n\nEnglish / 中文\n\nK线推送说明\n\nAlltick的WebSocket接口不支持K线数据的推送。由于许多客户对此有疑问，特此说明：无论是历史K线还是实时K线，目前仅支持通过HTTP接口直接获取。推荐的实现方式如下：\n\n实现方式建议（仅供参考）：\n\n1、定时拉取K线：为了实现K线的快速更新，建议购买高请求频率的套餐，以提高拉取频率。\n\n2、结合使用HTTP接口：建议客户将/kline和/batch-kline两个接口结合使用，具体步骤如下：\n\n首先，通过/kline接口轮询请求历史数据并存储到本地数据库。后续的历史数据可直接从客户的数据库获取，无需再次通过接口请求。\n\n然后，持续使用/batch-kline接口批量请求多个产品的最新两根K线，并将数据更新到数据库。\n\n这种方式能够快速更新最新的K线，同时避免频繁请求历史K线导致请求频率受到限制。\n\n涨跌幅说明\n\nAlltick的接口不提供涨跌幅或24小时涨跌幅字段。客户可以通过获取Alltick的数据自行计算涨跌幅。\n\n1、每日涨跌幅计算方法：\n\n方法一：使用HTTP接口获取当天的日K线收盘价和前一日的日K线收盘价，计算公式如下：\n\n涨跌幅 = (当天收盘价 - 前一日收盘价) / 前一日收盘价 * 100%\n\n方法二：使用WebSocket接口获取最新价格，并通过HTTP接口获取当天的日K线收盘价，计算公式如下：\n\n涨跌幅 = (最新价格 - 前一日收盘价) / 前一日收盘价 * 100%\n\n2、24小时涨跌幅计算方法：\n\n使用WebSocket的最新成交价格接口（请求-协议号：22004），实时接收逐笔成交价格（tick数据）。\n\n需自行存储WebSocket接口推送的24小时前的最新价格，以便进行后续计算。\n\n计算公式：\n\n24小时涨跌幅 = (最新价格 - 24小时前的最新价格) / 24小时前的最新价格 * 100%\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\n心跳\n下一页\n基础使用\n\n最后更新于12个月前"
  suggestedFilename: "websocket-api_stock-websocket-interface-api_ping-pong-1"
---

# K线推送(不支持)

## 源URL

https://apis.alltick.co/websocket-api/stock-websocket-interface-api/ping-pong-1

## 文档正文

1. Websocket APIchevron-right
1. Websocket接口API

English / 中文

## K线推送说明

Alltick的WebSocket接口不支持K线数据的推送。由于许多客户对此有疑问，特此说明：无论是历史K线还是实时K线，目前仅支持通过HTTP接口直接获取。推荐的实现方式如下：

实现方式建议（仅供参考）：

1、定时拉取K线：为了实现K线的快速更新，建议购买高请求频率的套餐，以提高拉取频率。

2、结合使用HTTP接口：建议客户将/kline和/batch-kline两个接口结合使用，具体步骤如下：

```text
/batch-kline
```

- 首先，通过/kline接口轮询请求历史数据并存储到本地数据库。后续的历史数据可直接从客户的数据库获取，无需再次通过接口请求。
- 然后，持续使用/batch-kline接口批量请求多个产品的最新两根K线，并将数据更新到数据库。

```text
/batch-kline
```

这种方式能够快速更新最新的K线，同时避免频繁请求历史K线导致请求频率受到限制。

## 涨跌幅说明

Alltick的接口不提供涨跌幅或24小时涨跌幅字段。客户可以通过获取Alltick的数据自行计算涨跌幅。

1、每日涨跌幅计算方法：

- 方法一：使用HTTP接口获取当天的日K线收盘价和前一日的日K线收盘价，计算公式如下：

涨跌幅 = (当天收盘价 - 前一日收盘价) / 前一日收盘价 * 100%

- 方法二：使用WebSocket接口获取最新价格，并通过HTTP接口获取当天的日K线收盘价，计算公式如下：

涨跌幅 = (最新价格 - 前一日收盘价) / 前一日收盘价 * 100%

2、24小时涨跌幅计算方法：

- 使用WebSocket的最新成交价格接口（请求-协议号：22004），实时接收逐笔成交价格（tick数据）。
- 需自行存储WebSocket接口推送的24小时前的最新价格，以便进行后续计算。
- 计算公式：

24小时涨跌幅 = (最新价格 - 24小时前的最新价格) / 24小时前的最新价格 * 100%

#### AllTick网站

官方网站：https://alltick.co/

最后更新于12个月前
