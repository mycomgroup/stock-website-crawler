---
id: "url-36496036"
type: "website"
title: "聚宽特色指数交易标的列表"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10759"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T09:09:22.611Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10759"
  headings:
    - {"level":3,"text":"聚宽特色指数交易标的列表","id":""}
    - {"level":5,"text":"参数","id":""}
    - {"level":5,"text":"返回结果","id":""}
    - {"level":4,"text":"指数概述","id":""}
  paragraphs:
    - "描述"
    - "指数编制规则"
    - "全A等权指数"
    - "小市值指数"
    - "微盘指数"
    - "聚宽一级行业指数"
    - "示例"
  lists:
    - {"type":"ul","items":["获取聚宽特色指数信息"]}
    - {"type":"ul","items":["基点为 1000点；加权方式为等权全收益指数"]}
    - {"type":"ul","items":["指数代码 : JQ0001.SPI","成分选取 : 每日调整 , 成分股只维护沪深交易所 , 剔除上市不足30日的新股","基日为 2010-01-01"]}
    - {"type":"ul","items":["指数代码 : JQ0002.SPI","成分选取 : 每月底调整 , 成分股在沪深交易所剔除上市不足30日或st及退市整理期股票中选取，选取市值小于100亿股票作为成分股 ,股票退市时从成分股中剔除","基日为 2010-01-01"]}
    - {"type":"ul","items":["指数代码 : 指数代码 : JQ0003.SPI","成分选取 : 每日调整 , 成分股只维护沪深交易所 ,剔除上市不足30日或st及退市整理期股票 , 成分股为剔除后总市值最小的400只标的","基日为 2010-01-01"]}
    - {"type":"ul","items":["指数代码 : S00001.SPI , S00002.SPI .... S00011.SPI 分别对应聚宽一级行业分类代码 HY001,HY002 ... HY011","成分选取 : 对应日期的行业分类的成分股","基日为 2016-12-12"]}
  tables:
    - {"caption":"","headers":["属性","名称","字段类型","备注"],"rows":[["types","类型","用list的形式过滤securities的类型,","list元素可选: 'spi'"],["date","日期","日期字符串或者 [datetime.datetime]/[datetime.date] 对象","用于获取某日期还在上市的证券信息. 默认值为 None, 表示获取所有日期的证券信息"]]}
    - {"caption":"","headers":["字段","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期",""],["end_date","退市日期","如果没有退市则为2200-01-01"],["type","类型","spi(聚宽特色指数)"]]}
    - {"caption":"","headers":["聚宽一级行业指数","对应的聚宽一级行业代码","中文名称"],"rows":[["S00001.SPI","HY001","能源指数"],["S00002.SPI","HY002","原材料指数"],["S00003.SPI","HY003","工业指数"],["S00004.SPI","HY004","可选消费"],["S00005.SPI","HY005","主要消费"],["S00006.SPI","HY006","医药卫生"],["S00007.SPI","HY007","金融"],["S00008.SPI","HY008","信息技术"],["S00009.SPI","HY009","通信服务"],["S00010.SPI","HY010","公用事业"],["S00011.SPI","HY011","房地产"]]}
  codeBlocks:
    - {"language":"python","code":"get_all_securities(types=['spi'], date=None)"}
    - {"language":"python","code":"get_all_securities(types=['spi'], date=None)[:5]\n\n\n           display_name   name start_date   end_date type\nJQ0001.SPI       全A等权指数   DQZS 2010-01-04 2200-01-01  spi\nJQ0002.SPI        小市值指数  XSZZS 2010-01-04 2200-01-01  spi\nJQ0003.SPI         微盘指数   WPZS 2010-01-04 2200-01-01  spi\nS00001.SPI         能源指数   NYZS 2016-12-13 2200-01-01  spi\nS00002.SPI        原材料指数  YCLZS 2016-12-13 2200-01-01  spi"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"聚宽特色指数交易标的列表"}
    - {"type":"codeblock","language":"python","content":"get_all_securities(types=['spi'], date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取聚宽特色指数信息"]}
    - {"type":"paragraph","content":"指数编制规则"}
    - {"type":"list","listType":"ul","items":["基点为 1000点；加权方式为等权全收益指数"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["属性","名称","字段类型","备注"],"rows":[["types","类型","用list的形式过滤securities的类型,","list元素可选: 'spi'"],["date","日期","日期字符串或者 [datetime.datetime]/[datetime.date] 对象","用于获取某日期还在上市的证券信息. 默认值为 None, 表示获取所有日期的证券信息"]]}
    - {"type":"heading","level":5,"content":"返回结果"}
    - {"type":"table","headers":["字段","名称","备注"],"rows":[["display_name","中文名称",""],["name","缩写简称",""],["start_date","上市日期",""],["end_date","退市日期","如果没有退市则为2200-01-01"],["type","类型","spi(聚宽特色指数)"]]}
    - {"type":"heading","level":4,"content":"指数概述"}
    - {"type":"paragraph","content":"全A等权指数"}
    - {"type":"list","listType":"ul","items":["指数代码 : JQ0001.SPI","成分选取 : 每日调整 , 成分股只维护沪深交易所 , 剔除上市不足30日的新股","基日为 2010-01-01"]}
    - {"type":"paragraph","content":"小市值指数"}
    - {"type":"list","listType":"ul","items":["指数代码 : JQ0002.SPI","成分选取 : 每月底调整 , 成分股在沪深交易所剔除上市不足30日或st及退市整理期股票中选取，选取市值小于100亿股票作为成分股 ,股票退市时从成分股中剔除","基日为 2010-01-01"]}
    - {"type":"paragraph","content":"微盘指数"}
    - {"type":"list","listType":"ul","items":["指数代码 : 指数代码 : JQ0003.SPI","成分选取 : 每日调整 , 成分股只维护沪深交易所 ,剔除上市不足30日或st及退市整理期股票 , 成分股为剔除后总市值最小的400只标的","基日为 2010-01-01"]}
    - {"type":"paragraph","content":"聚宽一级行业指数"}
    - {"type":"list","listType":"ul","items":["指数代码 : S00001.SPI , S00002.SPI .... S00011.SPI 分别对应聚宽一级行业分类代码 HY001,HY002 ... HY011","成分选取 : 对应日期的行业分类的成分股","基日为 2016-12-12"]}
    - {"type":"table","headers":["聚宽一级行业指数","对应的聚宽一级行业代码","中文名称"],"rows":[["S00001.SPI","HY001","能源指数"],["S00002.SPI","HY002","原材料指数"],["S00003.SPI","HY003","工业指数"],["S00004.SPI","HY004","可选消费"],["S00005.SPI","HY005","主要消费"],["S00006.SPI","HY006","医药卫生"],["S00007.SPI","HY007","金融"],["S00008.SPI","HY008","信息技术"],["S00009.SPI","HY009","通信服务"],["S00010.SPI","HY010","公用事业"],["S00011.SPI","HY011","房地产"]]}
    - {"type":"paragraph","content":"示例"}
    - {"type":"codeblock","language":"python","content":"get_all_securities(types=['spi'], date=None)[:5]\n\n\n           display_name   name start_date   end_date type\nJQ0001.SPI       全A等权指数   DQZS 2010-01-04 2200-01-01  spi\nJQ0002.SPI        小市值指数  XSZZS 2010-01-04 2200-01-01  spi\nJQ0003.SPI         微盘指数   WPZS 2010-01-04 2200-01-01  spi\nS00001.SPI         能源指数   NYZS 2016-12-13 2200-01-01  spi\nS00002.SPI        原材料指数  YCLZS 2016-12-13 2200-01-01  spi"}
  suggestedFilename: "doc_JQDatadoc_10759_overview_聚宽特色指数交易标的列表"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10759"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 聚宽特色指数交易标的列表

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10759

## 描述

描述

## 内容

#### 聚宽特色指数交易标的列表

```python
get_all_securities(types=['spi'], date=None)
```

描述

- 获取聚宽特色指数信息

指数编制规则

- 基点为 1000点；加权方式为等权全收益指数

###### 参数

| 属性 | 名称 | 字段类型 | 备注 |
| --- | --- | --- | --- |
| types | 类型 | 用list的形式过滤securities的类型, | list元素可选: 'spi' |
| date | 日期 | 日期字符串或者 [datetime.datetime]/[datetime.date] 对象 | 用于获取某日期还在上市的证券信息. 默认值为 None, 表示获取所有日期的证券信息 |

###### 返回结果

| 字段 | 名称 | 备注 |
| --- | --- | --- |
| display_name | 中文名称 |  |
| name | 缩写简称 |  |
| start_date | 上市日期 |  |
| end_date | 退市日期 | 如果没有退市则为2200-01-01 |
| type | 类型 | spi(聚宽特色指数) |

##### 指数概述

全A等权指数

- 指数代码 : JQ0001.SPI
- 成分选取 : 每日调整 , 成分股只维护沪深交易所 , 剔除上市不足30日的新股
- 基日为 2010-01-01

小市值指数

- 指数代码 : JQ0002.SPI
- 成分选取 : 每月底调整 , 成分股在沪深交易所剔除上市不足30日或st及退市整理期股票中选取，选取市值小于100亿股票作为成分股 ,股票退市时从成分股中剔除
- 基日为 2010-01-01

微盘指数

- 指数代码 : 指数代码 : JQ0003.SPI
- 成分选取 : 每日调整 , 成分股只维护沪深交易所 ,剔除上市不足30日或st及退市整理期股票 , 成分股为剔除后总市值最小的400只标的
- 基日为 2010-01-01

聚宽一级行业指数

- 指数代码 : S00001.SPI , S00002.SPI .... S00011.SPI 分别对应聚宽一级行业分类代码 HY001,HY002 ... HY011
- 成分选取 : 对应日期的行业分类的成分股
- 基日为 2016-12-12

| 聚宽一级行业指数 | 对应的聚宽一级行业代码 | 中文名称 |
| --- | --- | --- |
| S00001.SPI | HY001 | 能源指数 |
| S00002.SPI | HY002 | 原材料指数 |
| S00003.SPI | HY003 | 工业指数 |
| S00004.SPI | HY004 | 可选消费 |
| S00005.SPI | HY005 | 主要消费 |
| S00006.SPI | HY006 | 医药卫生 |
| S00007.SPI | HY007 | 金融 |
| S00008.SPI | HY008 | 信息技术 |
| S00009.SPI | HY009 | 通信服务 |
| S00010.SPI | HY010 | 公用事业 |
| S00011.SPI | HY011 | 房地产 |

示例

```python
get_all_securities(types=['spi'], date=None)[:5]

           display_name   name start_date   end_date type
JQ0001.SPI       全A等权指数   DQZS 2010-01-04 2200-01-01  spi
JQ0002.SPI        小市值指数  XSZZS 2010-01-04 2200-01-01  spi
JQ0003.SPI         微盘指数   WPZS 2010-01-04 2200-01-01  spi
S00001.SPI         能源指数   NYZS 2016-12-13 2200-01-01  spi
S00002.SPI        原材料指数  YCLZS 2016-12-13 2200-01-01  spi
```
