---
id: "url-364963d8"
type: "website"
title: "交易所指数"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10669"
description: "normalize_code(code)：将标的代码转化成聚宽标准格式"
source: ""
tags: []
crawl_time: "2026-03-27T07:50:45.835Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10669"
  headings:
    - {"level":2,"text":"交易所指数","id":""}
  paragraphs:
    - "normalize_code(code)：将标的代码转化成聚宽标准格式"
  lists: []
  tables:
    - {"caption":"","headers":["数据名称","API接口","历史范围","更新时间"],"rows":[["交易所指数"],["获取交易所指数列表","get_all_securities()","上市至今","8:00更新"],["交易所指数成分股及权重"],["交易所指数成分股数据","get_index_stocks()","上市至今","8:00更新"],["交易所指数成分股权重(月度)","get_index_weights()","上市至今","8:00更新"],["交易所指数行情"],["get_price 移动窗口","get_price()","2020年至今","盘后15点更新，24点入库"],["get_bars 固定窗口","get_bars()","2020年至今","盘后15点更新，24点入库"],["获取指数集合竞价","get_call_auction()","2020年至今","盘后15点更新，24点入库"],["交易所指数tick数据","get_ticks()","2020年至今","盘后15点更新，24点入库"]]}
    - {"caption":"","headers":["交易市场","代码后缀","示例代码","证券简称"],"rows":[["上海证券交易所",".XSHG","600519.XSHG","贵州茅台"],["深圳证券交易所",".XSHE","000001.XSHE","平安银行"],["中金所",".CCFX","IC9999.CCFX","中证500主力合约"],["大商所",".XDCE","A9999.XDCE","豆一主力合约"],["上期所",".XSGE","AU9999.XSGE","黄金主力合约"],["郑商所",".XZCE","CY8888.XZCE","棉纱期货指数"],["上海国际能源期货交易所",".XINE","SC9999.XINE","原油主力合约"],["广州期货交易所",".GFEX","SI9999.GFEX","工业硅主力合约"],["场外基金",".OF","398051.OF","中海环保新能源混合"]]}
  codeBlocks: []
  blockquotes: []
  mainContent:
    - {"type":"heading","level":2,"content":"交易所指数"}
    - {"type":"table","headers":["数据名称","API接口","历史范围","更新时间"],"rows":[["交易所指数"],["获取交易所指数列表","get_all_securities()","上市至今","8:00更新"],["交易所指数成分股及权重"],["交易所指数成分股数据","get_index_stocks()","上市至今","8:00更新"],["交易所指数成分股权重(月度)","get_index_weights()","上市至今","8:00更新"],["交易所指数行情"],["get_price 移动窗口","get_price()","2020年至今","盘后15点更新，24点入库"],["get_bars 固定窗口","get_bars()","2020年至今","盘后15点更新，24点入库"],["获取指数集合竞价","get_call_auction()","2020年至今","盘后15点更新，24点入库"],["交易所指数tick数据","get_ticks()","2020年至今","盘后15点更新，24点入库"]]}
    - {"type":"paragraph","content":"normalize_code(code)：将标的代码转化成聚宽标准格式"}
    - {"type":"table","headers":["交易市场","代码后缀","示例代码","证券简称"],"rows":[["上海证券交易所",".XSHG","600519.XSHG","贵州茅台"],["深圳证券交易所",".XSHE","000001.XSHE","平安银行"],["中金所",".CCFX","IC9999.CCFX","中证500主力合约"],["大商所",".XDCE","A9999.XDCE","豆一主力合约"],["上期所",".XSGE","AU9999.XSGE","黄金主力合约"],["郑商所",".XZCE","CY8888.XZCE","棉纱期货指数"],["上海国际能源期货交易所",".XINE","SC9999.XINE","原油主力合约"],["广州期货交易所",".GFEX","SI9999.GFEX","工业硅主力合约"],["场外基金",".OF","398051.OF","中海环保新能源混合"]]}
  suggestedFilename: "doc_JQDatadoc_10669_overview_交易所指数"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10669"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 交易所指数

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10669

## 描述

normalize_code(code)：将标的代码转化成聚宽标准格式

## 内容

### 交易所指数

| 数据名称 | API接口 | 历史范围 | 更新时间 |
| --- | --- | --- | --- |
| 交易所指数 |
| 获取交易所指数列表 | get_all_securities() | 上市至今 | 8:00更新 |
| 交易所指数成分股及权重 |
| 交易所指数成分股数据 | get_index_stocks() | 上市至今 | 8:00更新 |
| 交易所指数成分股权重(月度) | get_index_weights() | 上市至今 | 8:00更新 |
| 交易所指数行情 |
| get_price 移动窗口 | get_price() | 2020年至今 | 盘后15点更新，24点入库 |
| get_bars 固定窗口 | get_bars() | 2020年至今 | 盘后15点更新，24点入库 |
| 获取指数集合竞价 | get_call_auction() | 2020年至今 | 盘后15点更新，24点入库 |
| 交易所指数tick数据 | get_ticks() | 2020年至今 | 盘后15点更新，24点入库 |

normalize_code(code)：将标的代码转化成聚宽标准格式

| 交易市场 | 代码后缀 | 示例代码 | 证券简称 |
| --- | --- | --- | --- |
| 上海证券交易所 | .XSHG | 600519.XSHG | 贵州茅台 |
| 深圳证券交易所 | .XSHE | 000001.XSHE | 平安银行 |
| 中金所 | .CCFX | IC9999.CCFX | 中证500主力合约 |
| 大商所 | .XDCE | A9999.XDCE | 豆一主力合约 |
| 上期所 | .XSGE | AU9999.XSGE | 黄金主力合约 |
| 郑商所 | .XZCE | CY8888.XZCE | 棉纱期货指数 |
| 上海国际能源期货交易所 | .XINE | SC9999.XINE | 原油主力合约 |
| 广州期货交易所 | .GFEX | SI9999.GFEX | 工业硅主力合约 |
| 场外基金 | .OF | 398051.OF | 中海环保新能源混合 |
