---
id: "url-28f9cf94"
type: "website"
title: "如何安装使用JQData"
url: "https://www.joinquant.com/help/api/doc?name=logon&id=9832"
description: "安装/升级/使用jqdatasdk包"
source: ""
tags: []
crawl_time: "2026-03-27T09:09:34.795Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=logon&id=9832"
  headings:
    - {"level":3,"text":"如何安装使用JQData","id":"jqdata"}
    - {"level":5,"text":"安装JQData","id":"jqdata-1"}
    - {"level":5,"text":"升级JQData：","id":"jqdata-2"}
    - {"level":5,"text":"登录JQData","id":"jqdata-3"}
  paragraphs:
    - "安装/升级/使用jqdatasdk包"
    - "使用细则"
  lists:
    - {"type":"ul","items":["申请试用，开通权限后，您可以在本地安装和使用JQData。","Python用户请按以下教程安装使用，如在使用中遇到问题，可以联系官网在线客服或在社区问答板块留言，有专门的技术顾问跟进。"]}
    - {"type":"ul","items":["调用数据:详见下一步任务[登录JQData]","每天可访问数据条数:由于用户访问数据会给服务器造成一定的压力，JQData开放给试用账号的每天可访问数据为50万条，基本上能够满足大部分用户的需要；如需更多的访问条数，可以付费升级为正式账号，将获得每天2亿条数据的访问权限。个人用户咨询邮箱sunping@joinquant.com，机构服务咨询添加微信号JQData02。","因子数据和特色数据:如果您还想使用Alpha特色因子，技术指标因子，tick数据，您可以将账号升级到正式版、标准版或专业版，详情请联系我们的运营同事。个人用户咨询邮箱：sunping@joinquant.com，机构服务咨询添加微信号JQData02。","问题反馈和其他数据需求:如果您在使用JQData的过程中遇到问题，或者希望JQData能够加入更多的数据，请您通过[社区提问](/community)的方式或者联系官网右下角的在线客服。"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"pip install jqdatasdk"}
    - {"language":"python","code":"pip install -U jqdatasdk"}
    - {"language":"python","code":"C:\\JQData>python.exe -m pip install jqdatasdk"}
    - {"language":"python","code":"from jqdatasdk import *\nauth('账号','密码') #账号是申请时所填写的手机号；密码为聚宽官网登录密码"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"如何安装使用JQData"}
    - {"type":"paragraph","content":"安装/升级/使用jqdatasdk包"}
    - {"type":"list","listType":"ul","items":["申请试用，开通权限后，您可以在本地安装和使用JQData。","Python用户请按以下教程安装使用，如在使用中遇到问题，可以联系官网在线客服或在社区问答板块留言，有专门的技术顾问跟进。"]}
    - {"type":"heading","level":5,"content":"安装JQData"}
    - {"type":"codeblock","language":"python","content":"pip install jqdatasdk"}
    - {"type":"heading","level":5,"content":"升级JQData："}
    - {"type":"codeblock","language":"python","content":"pip install -U jqdatasdk"}
    - {"type":"codeblock","language":"python","content":"C:\\JQData>python.exe -m pip install jqdatasdk"}
    - {"type":"heading","level":5,"content":"登录JQData"}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import *\nauth('账号','密码') #账号是申请时所填写的手机号；密码为聚宽官网登录密码"}
    - {"type":"paragraph","content":"使用细则"}
    - {"type":"list","listType":"ul","items":["调用数据:详见下一步任务[登录JQData]","每天可访问数据条数:由于用户访问数据会给服务器造成一定的压力，JQData开放给试用账号的每天可访问数据为50万条，基本上能够满足大部分用户的需要；如需更多的访问条数，可以付费升级为正式账号，将获得每天2亿条数据的访问权限。个人用户咨询邮箱sunping@joinquant.com，机构服务咨询添加微信号JQData02。","因子数据和特色数据:如果您还想使用Alpha特色因子，技术指标因子，tick数据，您可以将账号升级到正式版、标准版或专业版，详情请联系我们的运营同事。个人用户咨询邮箱：sunping@joinquant.com，机构服务咨询添加微信号JQData02。","问题反馈和其他数据需求:如果您在使用JQData的过程中遇到问题，或者希望JQData能够加入更多的数据，请您通过[社区提问](/community)的方式或者联系官网右下角的在线客服。"]}
  suggestedFilename: "doc_logon_9832_overview_如何安装使用JQData"
  pageKind: "doc"
  pageName: "logon"
  pageId: "9832"
  sectionHash: ""
  sourceTitle: "试用和购买说明"
  treeRootTitle: ""
---

# 如何安装使用JQData

## 源URL

https://www.joinquant.com/help/api/doc?name=logon&id=9832

## 描述

安装/升级/使用jqdatasdk包

## 内容

#### 如何安装使用JQData

安装/升级/使用jqdatasdk包

- 申请试用，开通权限后，您可以在本地安装和使用JQData。
- Python用户请按以下教程安装使用，如在使用中遇到问题，可以联系官网在线客服或在社区问答板块留言，有专门的技术顾问跟进。

###### 安装JQData

```python
pip install jqdatasdk
```

###### 升级JQData：

```python
pip install -U jqdatasdk
```

```python
C:\JQData>python.exe -m pip install jqdatasdk
```

###### 登录JQData

```python
from jqdatasdk import *
auth('账号','密码') #账号是申请时所填写的手机号；密码为聚宽官网登录密码
```

使用细则

- 调用数据:详见下一步任务[登录JQData]
- 每天可访问数据条数:由于用户访问数据会给服务器造成一定的压力，JQData开放给试用账号的每天可访问数据为50万条，基本上能够满足大部分用户的需要；如需更多的访问条数，可以付费升级为正式账号，将获得每天2亿条数据的访问权限。个人用户咨询邮箱sunping@joinquant.com，机构服务咨询添加微信号JQData02。
- 因子数据和特色数据:如果您还想使用Alpha特色因子，技术指标因子，tick数据，您可以将账号升级到正式版、标准版或专业版，详情请联系我们的运营同事。个人用户咨询邮箱：sunping@joinquant.com，机构服务咨询添加微信号JQData02。
- 问题反馈和其他数据需求:如果您在使用JQData的过程中遇到问题，或者希望JQData能够加入更多的数据，请您通过[社区提问](/community)的方式或者联系官网右下角的在线客服。
