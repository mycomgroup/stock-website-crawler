---
id: "url-36495c57"
type: "website"
title: "JQData使用指南"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10868"
description: "试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"
source: ""
tags: []
crawl_time: "2026-03-27T07:44:16.200Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10868"
  headings:
    - {"level":3,"text":"JQData使用指南","id":""}
    - {"level":4,"text":"新接口","id":""}
  paragraphs:
    - "试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"
    - "学习材料"
    - "描述"
  lists:
    - {"type":"ul","items":["聚宽-get_price和get_bars处理规则","聚宽-复权说明"]}
    - {"type":"ul","items":["JQData的申请试用流程","登录/安装/流量查询/账号权限说明","JQDara查询账号权限（新）","JQData数据范围及接口更新时间","JQData的试用规则","保密协议","链接的定义","使用sdk常见报错","官网VIP和本地数据的区别"]}
    - {"type":"ul","items":["注意：query函数的更多用法详见：Query的简单教程","run_query 查询数据库中的数据：为了防止返回数据量过大, 我们每次最多返回5000行，不支持进行连表查询，即同时查询多张表的数据；","但我们为了方便用户批量获取，提供了run_offset_query的获取方法，最多返回20万条数据；不过随着offset值的增大，查询性能是递减的 ，如查询超过上限，返回数据可能不完整。","查询财务数据时如果提示没有定义，请在最上面添加：from jqdatasdk import *"]}
  tables:
    - {"caption":"","headers":["模块","数据名称","API接口","是否支持试用"],"rows":[["通用接口","批量查询股票/期货/基金/期权/债券/宏观数据库","run_offset_query","✓"],["股票","股票1天/分钟行情数据","get_price(round参数)","✓"],["基金","基金1天/分钟行情数据","get_price(round参数)","✓"],["股票单季度","获取多个季度/年度的历史财务数据","get_history_fundamentals","✓"],["获取多个标的在指定交易日范围内的市值表数据","get_valuation","✓"],["期货","获取期货合约的信息","get_futures_info","✓"],["风险模型","获取因子看板列表数据","get_factor_kanban_values","✗"],["获取因子看板分位数历史收益率","get_factor_stats"],["获取风格因子暴露收益率","get_factor_style_returns"],["获取特异收益率（无法被风格因子解释的收益）","get_factor_specific_returns"],["alpha因子","批量获取alpha101因子","get_all_alpha_101"],["批量获取alpha191因子","get_all_alpha_191"],["债券","可转债交易标的列表","get_all_securities"],["1天/分钟行情数据","get_price"],["指定时间周期的分钟/日行情","get_bars"],["可转债Tick数据","get_ticks"]]}
  codeBlocks: []
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"JQData使用指南"}
    - {"type":"paragraph","content":"试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制"}
    - {"type":"paragraph","content":"学习材料"}
    - {"type":"list","listType":"ul","items":["聚宽-get_price和get_bars处理规则","聚宽-复权说明"]}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["JQData的申请试用流程","登录/安装/流量查询/账号权限说明","JQDara查询账号权限（新）","JQData数据范围及接口更新时间","JQData的试用规则","保密协议","链接的定义","使用sdk常见报错","官网VIP和本地数据的区别"]}
    - {"type":"list","listType":"ul","items":["注意：query函数的更多用法详见：Query的简单教程","run_query 查询数据库中的数据：为了防止返回数据量过大, 我们每次最多返回5000行，不支持进行连表查询，即同时查询多张表的数据；","但我们为了方便用户批量获取，提供了run_offset_query的获取方法，最多返回20万条数据；不过随着offset值的增大，查询性能是递减的 ，如查询超过上限，返回数据可能不完整。","查询财务数据时如果提示没有定义，请在最上面添加：from jqdatasdk import *"]}
    - {"type":"heading","level":4,"content":"新接口"}
    - {"type":"table","headers":["模块","数据名称","API接口","是否支持试用"],"rows":[["通用接口","批量查询股票/期货/基金/期权/债券/宏观数据库","run_offset_query","✓"],["股票","股票1天/分钟行情数据","get_price(round参数)","✓"],["基金","基金1天/分钟行情数据","get_price(round参数)","✓"],["股票单季度","获取多个季度/年度的历史财务数据","get_history_fundamentals","✓"],["获取多个标的在指定交易日范围内的市值表数据","get_valuation","✓"],["期货","获取期货合约的信息","get_futures_info","✓"],["风险模型","获取因子看板列表数据","get_factor_kanban_values","✗"],["获取因子看板分位数历史收益率","get_factor_stats"],["获取风格因子暴露收益率","get_factor_style_returns"],["获取特异收益率（无法被风格因子解释的收益）","get_factor_specific_returns"],["alpha因子","批量获取alpha101因子","get_all_alpha_101"],["批量获取alpha191因子","get_all_alpha_191"],["债券","可转债交易标的列表","get_all_securities"],["1天/分钟行情数据","get_price"],["指定时间周期的分钟/日行情","get_bars"],["可转债Tick数据","get_ticks"]]}
  suggestedFilename: "doc_JQDatadoc_10868_overview_JQData使用指南"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10868"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# JQData使用指南

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10868

## 描述

试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制

## 内容

#### JQData使用指南

试用账号历史范围：前15个月~前3个月 ; 正式账号历史范围：不限制

学习材料

- 聚宽-get_price和get_bars处理规则
- 聚宽-复权说明

描述

- JQData的申请试用流程
- 登录/安装/流量查询/账号权限说明
- JQDara查询账号权限（新）
- JQData数据范围及接口更新时间
- JQData的试用规则
- 链接的定义
- 使用sdk常见报错
- 官网VIP和本地数据的区别

- 注意：query函数的更多用法详见：Query的简单教程
- run_query 查询数据库中的数据：为了防止返回数据量过大, 我们每次最多返回5000行，不支持进行连表查询，即同时查询多张表的数据；
- 但我们为了方便用户批量获取，提供了run_offset_query的获取方法，最多返回20万条数据；不过随着offset值的增大，查询性能是递减的 ，如查询超过上限，返回数据可能不完整。
- 查询财务数据时如果提示没有定义，请在最上面添加：from jqdatasdk import *

##### 新接口

| 模块 | 数据名称 | API接口 | 是否支持试用 |
| --- | --- | --- | --- |
| 通用接口 | 批量查询股票/期货/基金/期权/债券/宏观数据库 | run_offset_query | ✓ |
| 股票 | 股票1天/分钟行情数据 | get_price(round参数) | ✓ |
| 基金 | 基金1天/分钟行情数据 | get_price(round参数) | ✓ |
| 股票单季度 | 获取多个季度/年度的历史财务数据 | get_history_fundamentals | ✓ |
| 获取多个标的在指定交易日范围内的市值表数据 | get_valuation | ✓ |
| 期货 | 获取期货合约的信息 | get_futures_info | ✓ |
| 风险模型 | 获取因子看板列表数据 | get_factor_kanban_values | ✗ |
| 获取因子看板分位数历史收益率 | get_factor_stats |
| 获取风格因子暴露收益率 | get_factor_style_returns |
| 获取特异收益率（无法被风格因子解释的收益） | get_factor_specific_returns |
| alpha因子 | 批量获取alpha101因子 | get_all_alpha_101 |
| 批量获取alpha191因子 | get_all_alpha_191 |
| 债券 | 可转债交易标的列表 | get_all_securities |
| 1天/分钟行情数据 | get_price |
| 指定时间周期的分钟/日行情 | get_bars |
| 可转债Tick数据 | get_ticks |
