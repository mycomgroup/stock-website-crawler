---
id: "url-685817ef"
type: "api"
title: "Websocket 接口限制"
url: "https://apis.alltick.co/integration-process/interface-restriction-description/websocket-interface-limitations"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T05:20:30.334Z"
metadata:
  sections:
    - {"type":"list","ordered":true,"items":["接入流程chevron-right","接口限制说明"]}
    - {"type":"text","value":"English / 中文"}
    - {"type":"heading","level":2,"title":"WebSocket接口限制","content":[]}
    - {"type":"heading","level":2,"title":"1、IP类限制","content":[]}
    - {"type":"heading","level":4,"title":"1.1 Websocket的连接数是根据Token允许的连接数做限制的，不针对IP地址限制。","content":[{"type":"list","ordered":false,"items":["例如：基础计划规定一个Token只允许一个websocket连接，IP地址A已经发起了一个websocket连接的情况下，1、如果您使用相同的IP地址A尝试发起第二个websocket连接将会被拒绝；2、如果您使用IP地址B尝试发起第二个websocket连接也将会被拒绝；原因都是因为基础计划只允许一个websocket连接。","例如：高级计划规定一个Token只允许三个websocket连接，可以通过IP地址A同时发起三个websocket连接，也可以IP地址A、IP地址B、IP地址C各自发起一个websocket连接，只要总的连接数不超过三个即可。"]}]}
    - {"type":"heading","level":4,"title":"1.2 「股票大盘类数据」 和 「外汇贵金属原油类数据」 的请求url不同，两类数据同时连接计算为一个websocket连接，两类数据可同时请求。","content":[{"type":"list","ordered":false,"items":["例如：基础计划规定一个Token只允许一个websocket连接，IP地址A已经对股票数据发起了一个websocket连接的情况下，依然可以再次用IP地址A或者IP地址B发起外汇贵金属类数据的一个websocket连接。"]}]}
    - {"type":"heading","level":2,"title":"2、接口调用频率限制","content":[]}
    - {"type":"heading","level":4,"title":"2.1 每个接口的频率限制","content":[{"type":"list","ordered":false,"items":["最新成交价(逐笔Tick)接口：每1秒，只能1次请求。","盘口(Order Book)接口：每1秒，只能1次请求。"]}]}
    - {"type":"heading","level":4,"title":"2.2 在同一个WebSocket连接中，同时请求多个接口时，请求发送的间隔至少需要1秒","content":[{"type":"list","ordered":false,"items":["例如，如果用户A在28分30秒时通过WebSocket发送了一个【最新成交价接口，请求协议号22004】的请求，并在相同秒数内尝试发送另一个【最新盘口，请求协议号22002】请求，那么第二次请求将会被系统拒绝。"]}]}
    - {"type":"heading","level":4,"title":"2.3 在多个WebSocket连接中，用户需同时发起多个WebSocket请求时，请注意每个WebSocket请求间隔至少3秒","content":[{"type":"list","ordered":false,"items":["例如，用户A购买了高级计划，高级计划支持同时连接3WebSocket，如果用户A在28分30秒时发起了第一个WebSocket，则需间隔3秒，在28分34秒时可发起第二个WebSocket的订阅，当2个WebSocket订阅成功后，持续保持10秒发送一次心跳即可，接口将实时推送数据。"]}]}
    - {"type":"heading","level":4,"title":"2.4 当连接断开需要反复重连时：","content":[{"type":"list","ordered":false,"items":["免费计划用户：两次重连尝试之间需间隔至少10秒。","付费用户（包括基础、高级、专业、全港股、全A股、全美计划）：两次重连尝试之间需间隔至少3秒。"]}]}
    - {"type":"heading","level":2,"title":"3、连接数限制","content":[{"type":"list","ordered":false,"items":["不同的计划，限制的连接数是不同的，详情如下图。","如果尝试建立的连接数超过规定的限制，超出部分的连接尝试将会被直接断开。"]},{"type":"text","value":"免费"},{"type":"text","value":"只能建立1个websocket连接"},{"type":"text","value":"基础"},{"type":"text","value":"只能建立1个websocket连接"},{"type":"text","value":"高级"},{"type":"text","value":"可建立3个websocket连接"},{"type":"text","value":"专业"},{"type":"text","value":"可建立10个websocket连接"},{"type":"text","value":"全部港股"},{"type":"text","value":"可建立10个websocket连接"},{"type":"text","value":"全部A股"},{"type":"text","value":"可建立10个websocket连接"},{"type":"text","value":"全部美股"},{"type":"text","value":"可建立10个websocket连接"}]}
    - {"type":"heading","level":2,"title":"4、产品代码（code）订阅限制","content":[{"type":"list","ordered":false,"items":["通过单一WebSocket连接，用户一次最多只能订阅的产品代码（codes）的是有限制的，详细见下图。","如果试图订阅超过规定的订阅上限，系统将只处理限制数量内的最前面的请求数据，忽略其他的数据。"]},{"type":"text","value":"免费"},{"type":"text","value":"最新成交价(逐笔Tick)接口：最大同时请求5个产品 盘口(Order Book)接口：最大同时请求5个产品"},{"type":"text","value":"基础"},{"type":"text","value":"最新成交价(逐笔Tick)接口：最大同时请求100个产品 盘口(Order Book)接口：最大同时请求100个产品"},{"type":"text","value":"高级"},{"type":"text","value":"最新成交价(逐笔Tick)接口：最大同时请求200个产品 盘口(Order Book)接口：最大同时请求200个产品"},{"type":"text","value":"专业"},{"type":"text","value":"最新成交价(逐笔Tick)接口：最大同时请求3000个产品 盘口(Order Book)接口：最大同时请求3000个产品"},{"type":"text","value":"全部港股"},{"type":"text","value":"最新成交价(逐笔Tick)接口：最大同时请求3000个产品 盘口(Order Book)接口：最大同时请求3000个产品"},{"type":"text","value":"全部A股"},{"type":"text","value":"最新成交价(逐笔Tick)接口：最大同时请求3000个产品 盘口(Order Book)接口：最大同时请求3000个产品"},{"type":"text","value":"全部美股"},{"type":"text","value":"最新成交价(逐笔Tick)接口：最大同时请求3000个产品 盘口(Order Book)接口：最大同时请求3000个产品"}]}
    - {"type":"heading","level":4,"title":"注意事项","content":[{"type":"list","ordered":false,"items":["请根据这些限制合理规划您的WebSocket连接和请求策略，避免不必要的服务中断。","这些限制旨在确保所有用户都能公平且高效地访问服务，同时保护后端服务不受不当负荷的影响。","遇到任何问题或需要进一步的帮助时，请及时联系技术支持团队。"]}]}
    - {"type":"heading","level":4,"title":"AllTick网站","content":[{"type":"text","value":"官方网站：https://alltick.co/"},{"type":"text","value":"最后更新于10个月前"}]}
  codeExamples: []
  tables: []
  parameters: []
  markdownContent: "# Websocket 接口限制\n\n1. 接入流程chevron-right\n1. 接口限制说明\n\nEnglish / 中文\n\n\n## WebSocket接口限制\n\n\n## 1、IP类限制\n\n\n#### 1.1 Websocket的连接数是根据Token允许的连接数做限制的，不针对IP地址限制。\n\n- 例如：基础计划规定一个Token只允许一个websocket连接，IP地址A已经发起了一个websocket连接的情况下，1、如果您使用相同的IP地址A尝试发起第二个websocket连接将会被拒绝；2、如果您使用IP地址B尝试发起第二个websocket连接也将会被拒绝；原因都是因为基础计划只允许一个websocket连接。\n- 例如：高级计划规定一个Token只允许三个websocket连接，可以通过IP地址A同时发起三个websocket连接，也可以IP地址A、IP地址B、IP地址C各自发起一个websocket连接，只要总的连接数不超过三个即可。\n\n\n#### 1.2 「股票大盘类数据」 和 「外汇贵金属原油类数据」 的请求url不同，两类数据同时连接计算为一个websocket连接，两类数据可同时请求。\n\n- 例如：基础计划规定一个Token只允许一个websocket连接，IP地址A已经对股票数据发起了一个websocket连接的情况下，依然可以再次用IP地址A或者IP地址B发起外汇贵金属类数据的一个websocket连接。\n\n\n## 2、接口调用频率限制\n\n\n#### 2.1 每个接口的频率限制\n\n- 最新成交价(逐笔Tick)接口：每1秒，只能1次请求。\n- 盘口(Order Book)接口：每1秒，只能1次请求。\n\n\n#### 2.2 在同一个WebSocket连接中，同时请求多个接口时，请求发送的间隔至少需要1秒\n\n- 例如，如果用户A在28分30秒时通过WebSocket发送了一个【最新成交价接口，请求协议号22004】的请求，并在相同秒数内尝试发送另一个【最新盘口，请求协议号22002】请求，那么第二次请求将会被系统拒绝。\n\n\n#### 2.3 在多个WebSocket连接中，用户需同时发起多个WebSocket请求时，请注意每个WebSocket请求间隔至少3秒\n\n- 例如，用户A购买了高级计划，高级计划支持同时连接3WebSocket，如果用户A在28分30秒时发起了第一个WebSocket，则需间隔3秒，在28分34秒时可发起第二个WebSocket的订阅，当2个WebSocket订阅成功后，持续保持10秒发送一次心跳即可，接口将实时推送数据。\n\n\n#### 2.4 当连接断开需要反复重连时：\n\n- 免费计划用户：两次重连尝试之间需间隔至少10秒。\n- 付费用户（包括基础、高级、专业、全港股、全A股、全美计划）：两次重连尝试之间需间隔至少3秒。\n\n\n## 3、连接数限制\n\n- 不同的计划，限制的连接数是不同的，详情如下图。\n- 如果尝试建立的连接数超过规定的限制，超出部分的连接尝试将会被直接断开。\n\n免费\n\n只能建立1个websocket连接\n\n基础\n\n只能建立1个websocket连接\n\n高级\n\n可建立3个websocket连接\n\n专业\n\n可建立10个websocket连接\n\n全部港股\n\n可建立10个websocket连接\n\n全部A股\n\n可建立10个websocket连接\n\n全部美股\n\n可建立10个websocket连接\n\n\n## 4、产品代码（code）订阅限制\n\n- 通过单一WebSocket连接，用户一次最多只能订阅的产品代码（codes）的是有限制的，详细见下图。\n- 如果试图订阅超过规定的订阅上限，系统将只处理限制数量内的最前面的请求数据，忽略其他的数据。\n\n免费\n\n最新成交价(逐笔Tick)接口：最大同时请求5个产品 盘口(Order Book)接口：最大同时请求5个产品\n\n基础\n\n最新成交价(逐笔Tick)接口：最大同时请求100个产品 盘口(Order Book)接口：最大同时请求100个产品\n\n高级\n\n最新成交价(逐笔Tick)接口：最大同时请求200个产品 盘口(Order Book)接口：最大同时请求200个产品\n\n专业\n\n最新成交价(逐笔Tick)接口：最大同时请求3000个产品 盘口(Order Book)接口：最大同时请求3000个产品\n\n全部港股\n\n最新成交价(逐笔Tick)接口：最大同时请求3000个产品 盘口(Order Book)接口：最大同时请求3000个产品\n\n全部A股\n\n最新成交价(逐笔Tick)接口：最大同时请求3000个产品 盘口(Order Book)接口：最大同时请求3000个产品\n\n全部美股\n\n最新成交价(逐笔Tick)接口：最大同时请求3000个产品 盘口(Order Book)接口：最大同时请求3000个产品\n\n\n#### 注意事项\n\n- 请根据这些限制合理规划您的WebSocket连接和请求策略，避免不必要的服务中断。\n- 这些限制旨在确保所有用户都能公平且高效地访问服务，同时保护后端服务不受不当负荷的影响。\n- 遇到任何问题或需要进一步的帮助时，请及时联系技术支持团队。\n\n\n#### AllTick网站\n\n官方网站：https://alltick.co/\n\n最后更新于10个月前\n"
  rawContent: "复制\n接入流程\n接口限制说明\nWebsocket 接口限制\n\nEnglish / 中文\n\nWebSocket接口限制\n1、IP类限制\n1.1  Websocket的连接数是根据Token允许的连接数做限制的，不针对IP地址限制。\n\n例如：基础计划规定一个Token只允许一个websocket连接，IP地址A已经发起了一个websocket连接的情况下，1、如果您使用相同的IP地址A尝试发起第二个websocket连接将会被拒绝；2、如果您使用IP地址B尝试发起第二个websocket连接也将会被拒绝；原因都是因为基础计划只允许一个websocket连接。\n\n例如：高级计划规定一个Token只允许三个websocket连接，可以通过IP地址A同时发起三个websocket连接，也可以IP地址A、IP地址B、IP地址C各自发起一个websocket连接，只要总的连接数不超过三个即可。\n\n1.2  「股票大盘类数据」 和 「外汇贵金属原油类数据」 的请求url不同，两类数据同时连接计算为一个websocket连接，两类数据可同时请求。\n\n例如：基础计划规定一个Token只允许一个websocket连接，IP地址A已经对股票数据发起了一个websocket连接的情况下，依然可以再次用IP地址A或者IP地址B发起外汇贵金属类数据的一个websocket连接。\n\n2、接口调用频率限制\n2.1  每个接口的频率限制\n\n最新成交价(逐笔Tick)接口：每1秒，只能1次请求。\n\n盘口(Order Book)接口：每1秒，只能1次请求。\n\n2.2  在同一个WebSocket连接中，同时请求多个接口时，请求发送的间隔至少需要1秒\n\n例如，如果用户A在28分30秒时通过WebSocket发送了一个【最新成交价接口，请求协议号22004】的请求，并在相同秒数内尝试发送另一个【最新盘口，请求协议号22002】请求，那么第二次请求将会被系统拒绝。\n\n2.3 在多个WebSocket连接中，用户需同时发起多个WebSocket请求时，请注意每个WebSocket请求间隔至少3秒\n\n例如，用户A购买了高级计划，高级计划支持同时连接3WebSocket，如果用户A在28分30秒时发起了第一个WebSocket，则需间隔3秒，在28分34秒时可发起第二个WebSocket的订阅，当2个WebSocket订阅成功后，持续保持10秒发送一次心跳即可，接口将实时推送数据。\n\n2.4 当连接断开需要反复重连时：\n\n免费计划用户：两次重连尝试之间需间隔至少10秒。\n\n付费用户（包括基础、高级、专业、全港股、全A股、全美计划）：两次重连尝试之间需间隔至少3秒。\n\n3、连接数限制\n\n不同的计划，限制的连接数是不同的，详情如下图。\n\n如果尝试建立的连接数超过规定的限制，超出部分的连接尝试将会被直接断开。\n\n计划\nwebsocket连接数\n\n免费\n\n只能建立1个websocket连接\n\n基础\n\n只能建立1个websocket连接\n\n高级\n\n可建立3个websocket连接\n\n专业\n\n可建立10个websocket连接\n\n全部港股\n\n可建立10个websocket连接\n\n全部A股\n\n可建立10个websocket连接\n\n全部美股\n\n可建立10个websocket连接\n\n4、产品代码（code）订阅限制\n\n通过单一WebSocket连接，用户一次最多只能订阅的产品代码（codes）的是有限制的，详细见下图。\n\n如果试图订阅超过规定的订阅上限，系统将只处理限制数量内的最前面的请求数据，忽略其他的数据。\n\n计划\ncode订阅数限制\n\n免费\n\n最新成交价(逐笔Tick)接口：最大同时请求5个产品\n盘口(Order Book)接口：最大同时请求5个产品\n\n基础\n\n最新成交价(逐笔Tick)接口：最大同时请求100个产品\n盘口(Order Book)接口：最大同时请求100个产品\n\n高级\n\n最新成交价(逐笔Tick)接口：最大同时请求200个产品\n盘口(Order Book)接口：最大同时请求200个产品\n\n专业\n\n最新成交价(逐笔Tick)接口：最大同时请求3000个产品\n盘口(Order Book)接口：最大同时请求3000个产品\n\n全部港股\n\n最新成交价(逐笔Tick)接口：最大同时请求3000个产品\n盘口(Order Book)接口：最大同时请求3000个产品\n\n全部A股\n\n最新成交价(逐笔Tick)接口：最大同时请求3000个产品\n盘口(Order Book)接口：最大同时请求3000个产品\n\n全部美股\n\n最新成交价(逐笔Tick)接口：最大同时请求3000个产品\n盘口(Order Book)接口：最大同时请求3000个产品\n\n注意事项\n\n请根据这些限制合理规划您的WebSocket连接和请求策略，避免不必要的服务中断。\n\n这些限制旨在确保所有用户都能公平且高效地访问服务，同时保护后端服务不受不当负荷的影响。\n\n遇到任何问题或需要进一步的帮助时，请及时联系技术支持团队。\n\nAllTick网站\n\n官方网站：https://alltick.co/\n\n上一页\nHTTP 接口限制\n下一页\n错误码说明\n\n最后更新于10个月前"
  suggestedFilename: "integration-process_interface-restriction-description_websocket-interface-limitations"
---

# Websocket 接口限制

## 源URL

https://apis.alltick.co/integration-process/interface-restriction-description/websocket-interface-limitations

## 文档正文

1. 接入流程chevron-right
1. 接口限制说明

English / 中文

## WebSocket接口限制

## 1、IP类限制

#### 1.1 Websocket的连接数是根据Token允许的连接数做限制的，不针对IP地址限制。

- 例如：基础计划规定一个Token只允许一个websocket连接，IP地址A已经发起了一个websocket连接的情况下，1、如果您使用相同的IP地址A尝试发起第二个websocket连接将会被拒绝；2、如果您使用IP地址B尝试发起第二个websocket连接也将会被拒绝；原因都是因为基础计划只允许一个websocket连接。
- 例如：高级计划规定一个Token只允许三个websocket连接，可以通过IP地址A同时发起三个websocket连接，也可以IP地址A、IP地址B、IP地址C各自发起一个websocket连接，只要总的连接数不超过三个即可。

#### 1.2 「股票大盘类数据」 和 「外汇贵金属原油类数据」 的请求url不同，两类数据同时连接计算为一个websocket连接，两类数据可同时请求。

- 例如：基础计划规定一个Token只允许一个websocket连接，IP地址A已经对股票数据发起了一个websocket连接的情况下，依然可以再次用IP地址A或者IP地址B发起外汇贵金属类数据的一个websocket连接。

## 2、接口调用频率限制

#### 2.1 每个接口的频率限制

- 最新成交价(逐笔Tick)接口：每1秒，只能1次请求。
- 盘口(Order Book)接口：每1秒，只能1次请求。

#### 2.2 在同一个WebSocket连接中，同时请求多个接口时，请求发送的间隔至少需要1秒

- 例如，如果用户A在28分30秒时通过WebSocket发送了一个【最新成交价接口，请求协议号22004】的请求，并在相同秒数内尝试发送另一个【最新盘口，请求协议号22002】请求，那么第二次请求将会被系统拒绝。

#### 2.3 在多个WebSocket连接中，用户需同时发起多个WebSocket请求时，请注意每个WebSocket请求间隔至少3秒

- 例如，用户A购买了高级计划，高级计划支持同时连接3WebSocket，如果用户A在28分30秒时发起了第一个WebSocket，则需间隔3秒，在28分34秒时可发起第二个WebSocket的订阅，当2个WebSocket订阅成功后，持续保持10秒发送一次心跳即可，接口将实时推送数据。

#### 2.4 当连接断开需要反复重连时：

- 免费计划用户：两次重连尝试之间需间隔至少10秒。
- 付费用户（包括基础、高级、专业、全港股、全A股、全美计划）：两次重连尝试之间需间隔至少3秒。

## 3、连接数限制

- 不同的计划，限制的连接数是不同的，详情如下图。
- 如果尝试建立的连接数超过规定的限制，超出部分的连接尝试将会被直接断开。

免费

只能建立1个websocket连接

基础

只能建立1个websocket连接

高级

可建立3个websocket连接

专业

可建立10个websocket连接

全部港股

可建立10个websocket连接

全部A股

可建立10个websocket连接

全部美股

可建立10个websocket连接

## 4、产品代码（code）订阅限制

- 通过单一WebSocket连接，用户一次最多只能订阅的产品代码（codes）的是有限制的，详细见下图。
- 如果试图订阅超过规定的订阅上限，系统将只处理限制数量内的最前面的请求数据，忽略其他的数据。

免费

最新成交价(逐笔Tick)接口：最大同时请求5个产品 盘口(Order Book)接口：最大同时请求5个产品

基础

最新成交价(逐笔Tick)接口：最大同时请求100个产品 盘口(Order Book)接口：最大同时请求100个产品

高级

最新成交价(逐笔Tick)接口：最大同时请求200个产品 盘口(Order Book)接口：最大同时请求200个产品

专业

最新成交价(逐笔Tick)接口：最大同时请求3000个产品 盘口(Order Book)接口：最大同时请求3000个产品

全部港股

最新成交价(逐笔Tick)接口：最大同时请求3000个产品 盘口(Order Book)接口：最大同时请求3000个产品

全部A股

最新成交价(逐笔Tick)接口：最大同时请求3000个产品 盘口(Order Book)接口：最大同时请求3000个产品

全部美股

最新成交价(逐笔Tick)接口：最大同时请求3000个产品 盘口(Order Book)接口：最大同时请求3000个产品

#### 注意事项

- 请根据这些限制合理规划您的WebSocket连接和请求策略，避免不必要的服务中断。
- 这些限制旨在确保所有用户都能公平且高效地访问服务，同时保护后端服务不受不当负荷的影响。
- 遇到任何问题或需要进一步的帮助时，请及时联系技术支持团队。

#### AllTick网站

官方网站：https://alltick.co/

最后更新于10个月前
