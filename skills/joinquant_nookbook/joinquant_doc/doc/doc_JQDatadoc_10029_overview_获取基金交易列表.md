---
id: "url-36497ada"
type: "website"
title: "获取基金交易列表"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10029"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:49:23.295Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10029"
  headings:
    - {"level":3,"text":"获取基金交易列表","id":""}
    - {"level":5,"text":"参数","id":"-1"}
    - {"level":5,"text":"返回结果","id":"-2"}
    - {"level":5,"text":"示例","id":"-3"}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["历史范围：2005年至今；"]}
    - {"type":"ul","items":["获取平台支持的基金信息"]}
    - {"type":"ul","items":["返回dataframe","display_name: 中文名称","name: 缩写简称","start_date: 上市日期","end_date: 退市日期，如果没有退市则为2200-01-01","type: 细分类型，其中场内基金(fund)含有以下分类 : etf(ETF基金)，lof(上市型开放式基金)，mmf(场内交易的货币基金)，reits(基础设施基金)，fja(分级A)，fjb(分级B)，fjm(分级母基金)。场外基金(open_fund/QDII_FUND)含有以下分类 : bond_fund(债券基金)，stock_fund(股票基金)，money_market_fund(场外交易的货币基金)，mixture_fund(混合式基金)，closed_fund(封闭式基金)，fund_fund(联接基金)；其中 mmf，reits，fjm， closed_fund ，fund_fund不可作为参数传递给get_all_securities，只能通过传递fund/open_fund后根据返回的type字段过滤。其他细分类型均可作为参数传递给get_all_securities;见下方例子"]}
    - {"type":"ul","items":["获得所有场内基金"]}
    - {"type":"ul","items":["获得所有场外基金"]}
  tables:
    - {"caption":"","headers":["参数","类型","说明"],"rows":[["types","list","list或str,用来过滤securities的类型, 元素可选:'fund'(场内基金),'open_fund'(场外基金(含QDII)),'QDII_fund'(QDII基金)。也可指定为细分类型，支持的细分类型见下方返回说明"],["date","一个字符串或者 [datetime.datetime]/[datetime.date]","用于获取某日期还在上市的股票信息. 默认值为 None， 表示获取所有日期的股票信息"]]}
  codeBlocks:
    - {"language":"python","code":"get_all_securities(types=[], date=None)"}
    - {"language":"python","code":"df=get_all_securities(types=['fund'])\nprint(df)\n            display_name    name start_date   end_date type\n150008.XSHE         瑞和小康    RHXK 2009-11-19 2020-09-02  fja\n150009.XSHE         瑞和远见    RHYJ 2009-11-19 2020-09-02  fjb\n150012.XSHE       中证100A  ZZ100A 2010-06-18 2020-12-01  fja\n150013.XSHE       中证100B  ZZ100B 2010-06-18 2020-12-01  fjb\n150016.XSHE          合润A     HRA 2010-05-31 2020-12-31  fja\n...                  ...     ...        ...        ...  ...\n588330.XSHG         双创龙头    SCLT 2021-07-06 2200-01-01  etf\n588360.XSHG        创创ETF   CCETF 2021-07-06 2200-01-01  etf\n588380.XSHG       创50ETF  C50ETF 2021-07-06 2200-01-01  etf\n588390.XSHG         科创创业    KCCY 2021-08-30 2200-01-01  etf\n588400.XSHG         双创50    SC50 2021-07-05 2200-01-01  etf\n\n[1608 rows x 5 columns]"}
    - {"language":"python","code":"df=get_all_securities(types=['open_fund'])\nprint(df)\n\n\n                     display_name                name start_date   end_date  \\\n000001.OF              华夏成长证券投资基金                华夏成长 2001-12-18 2200-01-01   \n000003.OF      中海可转换债券债券型证券投资基金A类              中海可转债A 2013-03-20 2200-01-01   \n000004.OF      中海可转换债券债券型证券投资基金C类              中海可转债C 2013-03-20 2200-01-01   \n000005.OF     嘉实增强信用定期开放债券型证券投资基金              嘉实增强信用 2013-03-08 2200-01-01   \n000006.OF  西部利得量化成长混合型发起式证券投资基金A类         西部利得量化成长混合A 2019-03-19 2200-01-01   \n...                           ...                 ...        ...        ...   \n968083.OF     汇丰亚洲高入息债券基金BM2类–人民币   汇丰亚洲高入息债券BM2类–人民币 2020-04-15 2200-01-01   \n968084.OF    汇丰亚洲高入息债券基金BM3O类–人民币  汇丰亚洲高入息债券BM3O类–人民币 2020-04-15 2200-01-01   \n968085.OF       汇丰亚洲高入息债券基金BC类–港元     汇丰亚洲高入息债券BC类–港元 2020-04-15 2200-01-01   \n968086.OF      汇丰亚洲高入息债券基金BM2类–港元    汇丰亚洲高入息债券BM2类–港元 2020-04-15 2200-01-01   \n968087.OF     汇丰亚洲高入息债券基金BM3O类–澳元   汇丰亚洲高入息债券BM3O类–澳元 2020-04-15 2200-01-01   \n\n                   type  \n000001.OF  mixture_fund  \n000003.OF     bond_fund  \n000004.OF     bond_fund  \n000005.OF     bond_fund  \n000006.OF  mixture_fund  \n...                 ...  \n968083.OF     bond_fund  \n968084.OF     bond_fund  \n968085.OF     bond_fund  \n968086.OF     bond_fund  \n968087.OF     bond_fund  \n\n[17085 rows x 5 columns]"}
    - {"language":"python","code":"# 获取reits基金\n\ndf = get_all_securities(['fund'])\nprint(df[df.type.str.contains(\"reits\") ])\n​\n            display_name        name start_date   end_date   type\n180101.XSHE   博时蛇口产园REIT        SKCY 2021-06-21 2200-01-01  reits\n180201.XSHE   平安广州广河REIT        GZGH 2021-06-21 2200-01-01  reits\n180202.XSHE   华夏越秀高速REIT  HXYXGSREIT 2021-12-14 2200-01-01  reits\n180301.XSHE    红土盐田港REIT      YGREIT 2021-06-21 2200-01-01  reits\n180801.XSHE   中航首钢绿能REIT        SGLN 2021-06-21 2200-01-01  reits\n508000.XSHG       张江REIT      ZJREIT 2021-06-21 2200-01-01  reits\n508001.XSHG         浙江杭徽        ZJHH 2021-06-21 2200-01-01  reits\n508006.XSHG         首创水务        SCSW 2021-06-21 2200-01-01  reits\n508008.XSHG       铁建REIT      TJREIT 2022-07-08 2200-01-01  reits\n508018.XSHG       中交REIT      ZJREIT 2022-04-28 2200-01-01  reits\n508027.XSHG         东吴苏园        DWSY 2021-06-21 2200-01-01  reits\n508056.XSHG          普洛斯         PLS 2021-06-21 2200-01-01  reits\n508099.XSHG          中关村         ZGC 2021-12-17 2200-01-01  reits"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取基金交易列表"}
    - {"type":"list","listType":"ul","items":["历史范围：2005年至今；"]}
    - {"type":"codeblock","language":"python","content":"get_all_securities(types=[], date=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取平台支持的基金信息"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["参数","类型","说明"],"rows":[["types","list","list或str,用来过滤securities的类型, 元素可选:'fund'(场内基金),'open_fund'(场外基金(含QDII)),'QDII_fund'(QDII基金)。也可指定为细分类型，支持的细分类型见下方返回说明"],["date","一个字符串或者 [datetime.datetime]/[datetime.date]","用于获取某日期还在上市的股票信息. 默认值为 None， 表示获取所有日期的股票信息"]]}
    - {"type":"heading","level":5,"content":"返回结果"}
    - {"type":"list","listType":"ul","items":["返回dataframe","display_name: 中文名称","name: 缩写简称","start_date: 上市日期","end_date: 退市日期，如果没有退市则为2200-01-01","type: 细分类型，其中场内基金(fund)含有以下分类 : etf(ETF基金)，lof(上市型开放式基金)，mmf(场内交易的货币基金)，reits(基础设施基金)，fja(分级A)，fjb(分级B)，fjm(分级母基金)。场外基金(open_fund/QDII_FUND)含有以下分类 : bond_fund(债券基金)，stock_fund(股票基金)，money_market_fund(场外交易的货币基金)，mixture_fund(混合式基金)，closed_fund(封闭式基金)，fund_fund(联接基金)；其中 mmf，reits，fjm， closed_fund ，fund_fund不可作为参数传递给get_all_securities，只能通过传递fund/open_fund后根据返回的type字段过滤。其他细分类型均可作为参数传递给get_all_securities;见下方例子"]}
    - {"type":"heading","level":5,"content":"示例"}
    - {"type":"list","listType":"ul","items":["获得所有场内基金"]}
    - {"type":"codeblock","language":"python","content":"df=get_all_securities(types=['fund'])\nprint(df)\n            display_name    name start_date   end_date type\n150008.XSHE         瑞和小康    RHXK 2009-11-19 2020-09-02  fja\n150009.XSHE         瑞和远见    RHYJ 2009-11-19 2020-09-02  fjb\n150012.XSHE       中证100A  ZZ100A 2010-06-18 2020-12-01  fja\n150013.XSHE       中证100B  ZZ100B 2010-06-18 2020-12-01  fjb\n150016.XSHE          合润A     HRA 2010-05-31 2020-12-31  fja\n...                  ...     ...        ...        ...  ...\n588330.XSHG         双创龙头    SCLT 2021-07-06 2200-01-01  etf\n588360.XSHG        创创ETF   CCETF 2021-07-06 2200-01-01  etf\n588380.XSHG       创50ETF  C50ETF 2021-07-06 2200-01-01  etf\n588390.XSHG         科创创业    KCCY 2021-08-30 2200-01-01  etf\n588400.XSHG         双创50    SC50 2021-07-05 2200-01-01  etf\n\n[1608 rows x 5 columns]"}
    - {"type":"list","listType":"ul","items":["获得所有场外基金"]}
    - {"type":"codeblock","language":"python","content":"df=get_all_securities(types=['open_fund'])\nprint(df)\n\n\n                     display_name                name start_date   end_date  \\\n000001.OF              华夏成长证券投资基金                华夏成长 2001-12-18 2200-01-01   \n000003.OF      中海可转换债券债券型证券投资基金A类              中海可转债A 2013-03-20 2200-01-01   \n000004.OF      中海可转换债券债券型证券投资基金C类              中海可转债C 2013-03-20 2200-01-01   \n000005.OF     嘉实增强信用定期开放债券型证券投资基金              嘉实增强信用 2013-03-08 2200-01-01   \n000006.OF  西部利得量化成长混合型发起式证券投资基金A类         西部利得量化成长混合A 2019-03-19 2200-01-01   \n...                           ...                 ...        ...        ...   \n968083.OF     汇丰亚洲高入息债券基金BM2类–人民币   汇丰亚洲高入息债券BM2类–人民币 2020-04-15 2200-01-01   \n968084.OF    汇丰亚洲高入息债券基金BM3O类–人民币  汇丰亚洲高入息债券BM3O类–人民币 2020-04-15 2200-01-01   \n968085.OF       汇丰亚洲高入息债券基金BC类–港元     汇丰亚洲高入息债券BC类–港元 2020-04-15 2200-01-01   \n968086.OF      汇丰亚洲高入息债券基金BM2类–港元    汇丰亚洲高入息债券BM2类–港元 2020-04-15 2200-01-01   \n968087.OF     汇丰亚洲高入息债券基金BM3O类–澳元   汇丰亚洲高入息债券BM3O类–澳元 2020-04-15 2200-01-01   \n\n                   type  \n000001.OF  mixture_fund  \n000003.OF     bond_fund  \n000004.OF     bond_fund  \n000005.OF     bond_fund  \n000006.OF  mixture_fund  \n...                 ...  \n968083.OF     bond_fund  \n968084.OF     bond_fund  \n968085.OF     bond_fund  \n968086.OF     bond_fund  \n968087.OF     bond_fund  \n\n[17085 rows x 5 columns]"}
    - {"type":"codeblock","language":"python","content":"# 获取reits基金\n\ndf = get_all_securities(['fund'])\nprint(df[df.type.str.contains(\"reits\") ])\n​\n            display_name        name start_date   end_date   type\n180101.XSHE   博时蛇口产园REIT        SKCY 2021-06-21 2200-01-01  reits\n180201.XSHE   平安广州广河REIT        GZGH 2021-06-21 2200-01-01  reits\n180202.XSHE   华夏越秀高速REIT  HXYXGSREIT 2021-12-14 2200-01-01  reits\n180301.XSHE    红土盐田港REIT      YGREIT 2021-06-21 2200-01-01  reits\n180801.XSHE   中航首钢绿能REIT        SGLN 2021-06-21 2200-01-01  reits\n508000.XSHG       张江REIT      ZJREIT 2021-06-21 2200-01-01  reits\n508001.XSHG         浙江杭徽        ZJHH 2021-06-21 2200-01-01  reits\n508006.XSHG         首创水务        SCSW 2021-06-21 2200-01-01  reits\n508008.XSHG       铁建REIT      TJREIT 2022-07-08 2200-01-01  reits\n508018.XSHG       中交REIT      ZJREIT 2022-04-28 2200-01-01  reits\n508027.XSHG         东吴苏园        DWSY 2021-06-21 2200-01-01  reits\n508056.XSHG          普洛斯         PLS 2021-06-21 2200-01-01  reits\n508099.XSHG          中关村         ZGC 2021-12-17 2200-01-01  reits"}
  suggestedFilename: "doc_JQDatadoc_10029_overview_获取基金交易列表"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10029"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取基金交易列表

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10029

## 描述

描述

## 内容

#### 获取基金交易列表

- 历史范围：2005年至今；

```python
get_all_securities(types=[], date=None)
```

描述

- 获取平台支持的基金信息

###### 参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| types | list | list或str,用来过滤securities的类型, 元素可选:'fund'(场内基金),'open_fund'(场外基金(含QDII)),'QDII_fund'(QDII基金)。也可指定为细分类型，支持的细分类型见下方返回说明 |
| date | 一个字符串或者 [datetime.datetime]/[datetime.date] | 用于获取某日期还在上市的股票信息. 默认值为 None， 表示获取所有日期的股票信息 |

###### 返回结果

- 返回dataframe
- display_name: 中文名称
- name: 缩写简称
- start_date: 上市日期
- end_date: 退市日期，如果没有退市则为2200-01-01
- type: 细分类型，其中场内基金(fund)含有以下分类 : etf(ETF基金)，lof(上市型开放式基金)，mmf(场内交易的货币基金)，reits(基础设施基金)，fja(分级A)，fjb(分级B)，fjm(分级母基金)。场外基金(open_fund/QDII_FUND)含有以下分类 : bond_fund(债券基金)，stock_fund(股票基金)，money_market_fund(场外交易的货币基金)，mixture_fund(混合式基金)，closed_fund(封闭式基金)，fund_fund(联接基金)；其中 mmf，reits，fjm， closed_fund ，fund_fund不可作为参数传递给get_all_securities，只能通过传递fund/open_fund后根据返回的type字段过滤。其他细分类型均可作为参数传递给get_all_securities;见下方例子

###### 示例

- 获得所有场内基金

```python
df=get_all_securities(types=['fund'])
print(df)
            display_name    name start_date   end_date type
150008.XSHE         瑞和小康    RHXK 2009-11-19 2020-09-02  fja
150009.XSHE         瑞和远见    RHYJ 2009-11-19 2020-09-02  fjb
150012.XSHE       中证100A  ZZ100A 2010-06-18 2020-12-01  fja
150013.XSHE       中证100B  ZZ100B 2010-06-18 2020-12-01  fjb
150016.XSHE          合润A     HRA 2010-05-31 2020-12-31  fja
...                  ...     ...        ...        ...  ...
588330.XSHG         双创龙头    SCLT 2021-07-06 2200-01-01  etf
588360.XSHG        创创ETF   CCETF 2021-07-06 2200-01-01  etf
588380.XSHG       创50ETF  C50ETF 2021-07-06 2200-01-01  etf
588390.XSHG         科创创业    KCCY 2021-08-30 2200-01-01  etf
588400.XSHG         双创50    SC50 2021-07-05 2200-01-01  etf

[1608 rows x 5 columns]
```

- 获得所有场外基金

```python
df=get_all_securities(types=['open_fund'])
print(df)

                     display_name                name start_date   end_date  \
000001.OF              华夏成长证券投资基金                华夏成长 2001-12-18 2200-01-01   
000003.OF      中海可转换债券债券型证券投资基金A类              中海可转债A 2013-03-20 2200-01-01   
000004.OF      中海可转换债券债券型证券投资基金C类              中海可转债C 2013-03-20 2200-01-01   
000005.OF     嘉实增强信用定期开放债券型证券投资基金              嘉实增强信用 2013-03-08 2200-01-01   
000006.OF  西部利得量化成长混合型发起式证券投资基金A类         西部利得量化成长混合A 2019-03-19 2200-01-01   
...                           ...                 ...        ...        ...   
968083.OF     汇丰亚洲高入息债券基金BM2类–人民币   汇丰亚洲高入息债券BM2类–人民币 2020-04-15 2200-01-01   
968084.OF    汇丰亚洲高入息债券基金BM3O类–人民币  汇丰亚洲高入息债券BM3O类–人民币 2020-04-15 2200-01-01   
968085.OF       汇丰亚洲高入息债券基金BC类–港元     汇丰亚洲高入息债券BC类–港元 2020-04-15 2200-01-01   
968086.OF      汇丰亚洲高入息债券基金BM2类–港元    汇丰亚洲高入息债券BM2类–港元 2020-04-15 2200-01-01   
968087.OF     汇丰亚洲高入息债券基金BM3O类–澳元   汇丰亚洲高入息债券BM3O类–澳元 2020-04-15 2200-01-01   

                   type  
000001.OF  mixture_fund  
000003.OF     bond_fund  
000004.OF     bond_fund  
000005.OF     bond_fund  
000006.OF  mixture_fund  
...                 ...  
968083.OF     bond_fund  
968084.OF     bond_fund  
968085.OF     bond_fund  
968086.OF     bond_fund  
968087.OF     bond_fund  

[17085 rows x 5 columns]
```

```python
# 获取reits基金

df = get_all_securities(['fund'])
print(df[df.type.str.contains("reits") ])

            display_name        name start_date   end_date   type
180101.XSHE   博时蛇口产园REIT        SKCY 2021-06-21 2200-01-01  reits
180201.XSHE   平安广州广河REIT        GZGH 2021-06-21 2200-01-01  reits
180202.XSHE   华夏越秀高速REIT  HXYXGSREIT 2021-12-14 2200-01-01  reits
180301.XSHE    红土盐田港REIT      YGREIT 2021-06-21 2200-01-01  reits
180801.XSHE   中航首钢绿能REIT        SGLN 2021-06-21 2200-01-01  reits
508000.XSHG       张江REIT      ZJREIT 2021-06-21 2200-01-01  reits
508001.XSHG         浙江杭徽        ZJHH 2021-06-21 2200-01-01  reits
508006.XSHG         首创水务        SCSW 2021-06-21 2200-01-01  reits
508008.XSHG       铁建REIT      TJREIT 2022-07-08 2200-01-01  reits
508018.XSHG       中交REIT      ZJREIT 2022-04-28 2200-01-01  reits
508027.XSHG         东吴苏园        DWSY 2021-06-21 2200-01-01  reits
508056.XSHG          普洛斯         PLS 2021-06-21 2200-01-01  reits
508099.XSHG          中关村         ZGC 2021-12-17 2200-01-01  reits
```
