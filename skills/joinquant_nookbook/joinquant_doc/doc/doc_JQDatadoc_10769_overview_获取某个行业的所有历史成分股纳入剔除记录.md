---
id: "url-36496017"
type: "website"
title: "获取某个行业的所有历史成分股纳入剔除记录"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10769"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:48:40.185Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10769"
  headings:
    - {"level":3,"text":"获取某个行业的所有历史成分股纳入剔除记录","id":""}
    - {"level":5,"text":"参数","id":""}
    - {"level":5,"text":"代码示例","id":""}
  paragraphs:
    - "描述"
    - "返回"
    - "备注"
  lists:
    - {"type":"ul","items":["历史范围：,提供上市至今的数据；8:00更新"]}
    - {"type":"ul","items":["获取某个行业的所有历史成分股纳入剔除记录，支持sw_l1、sw_l2、sw_l3、jq11、jq_12、zjw 行业"]}
    - {"type":"ul","items":["DataFrame, 包含成分股标的纳入剔除日期,当未被剔除时end_date为Nan"]}
    - {"type":"ul","items":["证监会行业 : 原证监会行业分类标准已废弃,自2024-02-08已切换为中国上市公司协会上市公司行业分类标准 申万行业 : 历史上有更改过两次行业分类标准, 分别为2021-12-11 和 2014-02-20 聚宽行业 : 在 2021-12-13 有变更过行业分类标准 上述时间点对应的行业出入信息,可能因分类标准的变化导致成分股大规模变动或者剔除后重新纳入的现象,是正常的"]}
    - {"type":"ul","items":["获取某个标的的所有历史成分股纳入剔除记录"]}
    - {"type":"ul","items":["获取证监会行业所有历史成分股纳入剔除记录"]}
  tables:
    - {"caption":"","headers":["参数","备注"],"rows":[["name","行业名称, 如 zjw, sw_l1 等"],["securities","标的代码, 默认为所有"]]}
  codeBlocks:
    - {"language":"python","code":"get_history_industry(name, securities=None)"}
    - {"language":"python","code":"get_history_industry('zjw','000001.XSHE')\n\n  code  start_date    end_date        stock\n0  J66  1991-04-03  2024-02-07  000001.XSHE\n1  J66  2024-02-08         NaN  000001.XSHE"}
    - {"language":"python","code":"get_history_industry('zjw')[:5]\n\n  code  start_date    end_date        stock\n0  A01  1997-12-02  2007-12-30  000829.XSHE\n1  A01  2000-09-26  2006-12-30  000972.XSHE\n2  A01  2000-12-11  2024-02-07  000998.XSHE\n3  A01  2005-04-18  2024-02-07  002041.XSHE\n4  A01  2015-06-10  2024-02-07  002772.XSHE"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"获取某个行业的所有历史成分股纳入剔除记录"}
    - {"type":"list","listType":"ul","items":["历史范围：,提供上市至今的数据；8:00更新"]}
    - {"type":"codeblock","language":"python","content":"get_history_industry(name, securities=None)"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["获取某个行业的所有历史成分股纳入剔除记录，支持sw_l1、sw_l2、sw_l3、jq11、jq_12、zjw 行业"]}
    - {"type":"paragraph","content":"返回"}
    - {"type":"list","listType":"ul","items":["DataFrame, 包含成分股标的纳入剔除日期,当未被剔除时end_date为Nan"]}
    - {"type":"paragraph","content":"备注"}
    - {"type":"list","listType":"ul","items":["证监会行业 : 原证监会行业分类标准已废弃,自2024-02-08已切换为中国上市公司协会上市公司行业分类标准 申万行业 : 历史上有更改过两次行业分类标准, 分别为2021-12-11 和 2014-02-20 聚宽行业 : 在 2021-12-13 有变更过行业分类标准 上述时间点对应的行业出入信息,可能因分类标准的变化导致成分股大规模变动或者剔除后重新纳入的现象,是正常的"]}
    - {"type":"heading","level":5,"content":"参数"}
    - {"type":"table","headers":["参数","备注"],"rows":[["name","行业名称, 如 zjw, sw_l1 等"],["securities","标的代码, 默认为所有"]]}
    - {"type":"heading","level":5,"content":"代码示例"}
    - {"type":"list","listType":"ul","items":["获取某个标的的所有历史成分股纳入剔除记录"]}
    - {"type":"codeblock","language":"python","content":"get_history_industry('zjw','000001.XSHE')\n\n  code  start_date    end_date        stock\n0  J66  1991-04-03  2024-02-07  000001.XSHE\n1  J66  2024-02-08         NaN  000001.XSHE"}
    - {"type":"list","listType":"ul","items":["获取证监会行业所有历史成分股纳入剔除记录"]}
    - {"type":"codeblock","language":"python","content":"get_history_industry('zjw')[:5]\n\n  code  start_date    end_date        stock\n0  A01  1997-12-02  2007-12-30  000829.XSHE\n1  A01  2000-09-26  2006-12-30  000972.XSHE\n2  A01  2000-12-11  2024-02-07  000998.XSHE\n3  A01  2005-04-18  2024-02-07  002041.XSHE\n4  A01  2015-06-10  2024-02-07  002772.XSHE"}
  suggestedFilename: "doc_JQDatadoc_10769_overview_获取某个行业的所有历史成分股纳入剔除记录"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10769"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 获取某个行业的所有历史成分股纳入剔除记录

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10769

## 描述

描述

## 内容

#### 获取某个行业的所有历史成分股纳入剔除记录

- 历史范围：,提供上市至今的数据；8:00更新

```python
get_history_industry(name, securities=None)
```

描述

- 获取某个行业的所有历史成分股纳入剔除记录，支持sw_l1、sw_l2、sw_l3、jq11、jq_12、zjw 行业

返回

- DataFrame, 包含成分股标的纳入剔除日期,当未被剔除时end_date为Nan

备注

- 证监会行业 : 原证监会行业分类标准已废弃,自2024-02-08已切换为中国上市公司协会上市公司行业分类标准 申万行业 : 历史上有更改过两次行业分类标准, 分别为2021-12-11 和 2014-02-20 聚宽行业 : 在 2021-12-13 有变更过行业分类标准 上述时间点对应的行业出入信息,可能因分类标准的变化导致成分股大规模变动或者剔除后重新纳入的现象,是正常的

###### 参数

| 参数 | 备注 |
| --- | --- |
| name | 行业名称, 如 zjw, sw_l1 等 |
| securities | 标的代码, 默认为所有 |

###### 代码示例

- 获取某个标的的所有历史成分股纳入剔除记录

```python
get_history_industry('zjw','000001.XSHE')

  code  start_date    end_date        stock
0  J66  1991-04-03  2024-02-07  000001.XSHE
1  J66  2024-02-08         NaN  000001.XSHE
```

- 获取证监会行业所有历史成分股纳入剔除记录

```python
get_history_industry('zjw')[:5]

  code  start_date    end_date        stock
0  A01  1997-12-02  2007-12-30  000829.XSHE
1  A01  2000-09-26  2006-12-30  000972.XSHE
2  A01  2000-12-11  2024-02-07  000998.XSHE
3  A01  2005-04-18  2024-02-07  002041.XSHE
4  A01  2015-06-10  2024-02-07  002772.XSHE
```
