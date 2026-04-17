---
id: "url-28f9cf93"
type: "website"
title: "登录JQData"
url: "https://www.joinquant.com/help/api/doc?name=logon&id=9833"
description: "登录JQData"
source: ""
tags: []
crawl_time: "2026-03-27T07:14:02.774Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=logon&id=9833"
  headings:
    - {"level":3,"text":"登录JQData","id":"jqdata"}
  paragraphs:
    - "登录JQData"
  lists:
    - {"type":"ul","items":["打开代码编辑器（第三方编辑器请指定运行环境为已安装JQData的Python环境），输入如下代码认证用户身份。认证完毕后显示“auth success”即可开始调用数据，认证步骤如下："]}
    - {"type":"ul","items":["注意:JQData支持开启一个连接数，即登录一次账号算一个连接；如遇到连接数超限情况，可使用logout()函数退出已有连接后再开启新的连接。"]}
  tables: []
  codeBlocks:
    - {"language":"python","code":"from jqdatasdk import *\nauth('ID','Password') #ID是申请时所填写的手机号；Password为聚宽官网登录密码"}
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"登录JQData"}
    - {"type":"paragraph","content":"登录JQData"}
    - {"type":"list","listType":"ul","items":["打开代码编辑器（第三方编辑器请指定运行环境为已安装JQData的Python环境），输入如下代码认证用户身份。认证完毕后显示“auth success”即可开始调用数据，认证步骤如下："]}
    - {"type":"list","listType":"ul","items":["注意:JQData支持开启一个连接数，即登录一次账号算一个连接；如遇到连接数超限情况，可使用logout()函数退出已有连接后再开启新的连接。"]}
    - {"type":"codeblock","language":"python","content":"from jqdatasdk import *\nauth('ID','Password') #ID是申请时所填写的手机号；Password为聚宽官网登录密码"}
  suggestedFilename: "doc_logon_9833_overview_登录JQData"
  pageKind: "doc"
  pageName: "logon"
  pageId: "9833"
  sectionHash: ""
  sourceTitle: "试用和购买说明"
  treeRootTitle: ""
---

# 登录JQData

## 源URL

https://www.joinquant.com/help/api/doc?name=logon&id=9833

## 描述

登录JQData

## 内容

#### 登录JQData

登录JQData

- 打开代码编辑器（第三方编辑器请指定运行环境为已安装JQData的Python环境），输入如下代码认证用户身份。认证完毕后显示“auth success”即可开始调用数据，认证步骤如下：

- 注意:JQData支持开启一个连接数，即登录一次账号算一个连接；如遇到连接数超限情况，可使用logout()函数退出已有连接后再开启新的连接。

```python
from jqdatasdk import *
auth('ID','Password') #ID是申请时所填写的手机号；Password为聚宽官网登录密码
```
