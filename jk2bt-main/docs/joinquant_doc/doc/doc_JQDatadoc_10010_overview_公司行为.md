---
id: "url-36497b02"
type: "website"
title: "公司行为"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10010"
description: "试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"
source: ""
tags: []
crawl_time: "2026-03-27T09:08:34.546Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10010"
  headings:
    - {"level":3,"text":"公司行为","id":""}
    - {"level":5,"text":"常见数据问题>>>","id":"httpsdocsqqcomdocdrwjyevdovfpmafpb"}
  paragraphs:
    - "试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"
    - "描述"
    - "1、STK_XR_XD 分红送股数据是怎么更新的?"
    - "A ： STK_XR_XD 表以报告期为维度，每个报告期为一条数据(特别分红等可以看作额外的报告期)，其中report_date和bonus_type对应， 一般为中期分红和年度分红;也存在季度分红，特别分红等。 分红送股信息的流程一般为 ： 董事会预案-->股东大会预案-->实施方案公告 ， 进度对应的字段会随着对应进度的公告数据及时更新 ， 进度未产生时对应的字段为空 ， 如果在某一进度取消分红，bonus_cancel_pub_date及plan_progress等会有相关更新进行说明。 如果要获取最新的，已确认进行实施分红的可以根据除权除息日(a_xr_date)进行排序筛选，而不是report_date。 如 from jqdata import finance finance.run_query(query(finance.STK_XR_XD).filter( finance.STK_XR_XD.a_xr_date< =\"2019-10-23\" ).order_by( finance.STK_XR_XD.a_xr_date.desc()))"
  lists:
    - {"type":"ul","items":["大股东增减持 —— 2005年至今，交易日24:00更新","上市公司股本变动 —— 2005年至今，交易日24:00更新","受限股份上市公告日期 —— 2005年至今，交易日24:00更新","受限股份实际解禁日期 —— 2005年至今，交易日24:00更新","限售解禁股 —— 2005年至今，交易日24:00更新","上市公司分红送股（除权除息）数据 —— 2005年至今，交易日24:00更新"]}
  tables: []
  codeBlocks: []
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"公司行为"}
    - {"type":"paragraph","content":"试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["大股东增减持 —— 2005年至今，交易日24:00更新","上市公司股本变动 —— 2005年至今，交易日24:00更新","受限股份上市公告日期 —— 2005年至今，交易日24:00更新","受限股份实际解禁日期 —— 2005年至今，交易日24:00更新","限售解禁股 —— 2005年至今，交易日24:00更新","上市公司分红送股（除权除息）数据 —— 2005年至今，交易日24:00更新"]}
    - {"type":"heading","level":5,"content":"常见数据问题>>>"}
    - {"type":"paragraph","content":"1、STK_XR_XD 分红送股数据是怎么更新的?"}
    - {"type":"paragraph","content":"A ： STK_XR_XD 表以报告期为维度，每个报告期为一条数据(特别分红等可以看作额外的报告期)，其中report_date和bonus_type对应， 一般为中期分红和年度分红;也存在季度分红，特别分红等。 分红送股信息的流程一般为 ： 董事会预案-->股东大会预案-->实施方案公告 ， 进度对应的字段会随着对应进度的公告数据及时更新 ， 进度未产生时对应的字段为空 ， 如果在某一进度取消分红，bonus_cancel_pub_date及plan_progress等会有相关更新进行说明。 如果要获取最新的，已确认进行实施分红的可以根据除权除息日(a_xr_date)进行排序筛选，而不是report_date。 如 from jqdata import finance finance.run_query(query(finance.STK_XR_XD).filter( finance.STK_XR_XD.a_xr_date< =\"2019-10-23\" ).order_by( finance.STK_XR_XD.a_xr_date.desc()))"}
  suggestedFilename: "doc_JQDatadoc_10010_overview_公司行为"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10010"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 公司行为

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10010

## 描述

试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制

## 内容

#### 公司行为

试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制

描述

- 大股东增减持 —— 2005年至今，交易日24:00更新
- 上市公司股本变动 —— 2005年至今，交易日24:00更新
- 受限股份上市公告日期 —— 2005年至今，交易日24:00更新
- 受限股份实际解禁日期 —— 2005年至今，交易日24:00更新
- 限售解禁股 —— 2005年至今，交易日24:00更新
- 上市公司分红送股（除权除息）数据 —— 2005年至今，交易日24:00更新

###### 常见数据问题>>>

1、STK_XR_XD 分红送股数据是怎么更新的?

A ： STK_XR_XD 表以报告期为维度，每个报告期为一条数据(特别分红等可以看作额外的报告期)，其中report_date和bonus_type对应， 一般为中期分红和年度分红;也存在季度分红，特别分红等。 分红送股信息的流程一般为 ： 董事会预案-->股东大会预案-->实施方案公告 ， 进度对应的字段会随着对应进度的公告数据及时更新 ， 进度未产生时对应的字段为空 ， 如果在某一进度取消分红，bonus_cancel_pub_date及plan_progress等会有相关更新进行说明。 如果要获取最新的，已确认进行实施分红的可以根据除权除息日(a_xr_date)进行排序筛选，而不是report_date。 如 from jqdata import finance finance.run_query(query(finance.STK_XR_XD).filter( finance.STK_XR_XD.a_xr_date< ="2019-10-23" ).order_by( finance.STK_XR_XD.a_xr_date.desc()))
