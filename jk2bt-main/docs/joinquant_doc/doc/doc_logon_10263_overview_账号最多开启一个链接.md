---
id: "url-94b7b02"
type: "website"
title: "账号最多开启一个链接"
url: "https://www.joinquant.com/help/api/doc?name=logon&id=10263"
description: "描述"
source: ""
tags: []
crawl_time: "2026-03-27T07:14:34.248Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=logon&id=10263"
  headings:
    - {"level":3,"text":"账号最多开启一个链接","id":""}
  paragraphs:
    - "描述"
  lists:
    - {"type":"ul","items":["这是同时打开了多个链接造成的；每次auth之后会创建新的链接，是长连接的（thrift长连接,不支持在其他进程/线程中共享）；使用logout()或者关闭进程后会断开；默认同时最多存在一个链接，如果A链接被创建，之后再创建B链接时(也就是在其他进程/线程中进行登录)，A链接会失效，再使用A链接就会报这个错误。","对于多个链接的简单解释: 如果不了解进程/线程的概念，可以这样简单的理解, 每个独立的cmd窗口是一个独立的进程，每个独立的jupyter也是一个独立的进程 ,每auth一次就是建立一个新的链接。","目前jqdatasdk不支持超过1个链接，不支持多线程；","建议每次获取数据不要超过10w条(防止进程假死)；","建议获取数据后使用logout()退出；","升级jqdatasdk到最新版本；","使用pycharm注意关闭 run with console 选项或者每次运行后关闭控制台界面(每个开启的控制台都相当于一个进程); 使用控制台时注意设置控制台变量加载策略为\"按需\" ，否则易引发多个链接及输出异常的问题","需要更多的链接数，可付费升级为正式账号，为了更高品质展开服务，个人用户咨询【邮箱：sunping@joinquant.com】，机构服务咨询添加微信号JQData02"]}
  tables: []
  codeBlocks: []
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"账号最多开启一个链接"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["这是同时打开了多个链接造成的；每次auth之后会创建新的链接，是长连接的（thrift长连接,不支持在其他进程/线程中共享）；使用logout()或者关闭进程后会断开；默认同时最多存在一个链接，如果A链接被创建，之后再创建B链接时(也就是在其他进程/线程中进行登录)，A链接会失效，再使用A链接就会报这个错误。","对于多个链接的简单解释: 如果不了解进程/线程的概念，可以这样简单的理解, 每个独立的cmd窗口是一个独立的进程，每个独立的jupyter也是一个独立的进程 ,每auth一次就是建立一个新的链接。","目前jqdatasdk不支持超过1个链接，不支持多线程；","建议每次获取数据不要超过10w条(防止进程假死)；","建议获取数据后使用logout()退出；","升级jqdatasdk到最新版本；","使用pycharm注意关闭 run with console 选项或者每次运行后关闭控制台界面(每个开启的控制台都相当于一个进程); 使用控制台时注意设置控制台变量加载策略为\"按需\" ，否则易引发多个链接及输出异常的问题","需要更多的链接数，可付费升级为正式账号，为了更高品质展开服务，个人用户咨询【邮箱：sunping@joinquant.com】，机构服务咨询添加微信号JQData02"]}
  suggestedFilename: "doc_logon_10263_overview_账号最多开启一个链接"
  pageKind: "doc"
  pageName: "logon"
  pageId: "10263"
  sectionHash: ""
  sourceTitle: "试用和购买说明"
  treeRootTitle: ""
---

# 账号最多开启一个链接

## 源URL

https://www.joinquant.com/help/api/doc?name=logon&id=10263

## 描述

描述

## 内容

#### 账号最多开启一个链接

描述

- 这是同时打开了多个链接造成的；每次auth之后会创建新的链接，是长连接的（thrift长连接,不支持在其他进程/线程中共享）；使用logout()或者关闭进程后会断开；默认同时最多存在一个链接，如果A链接被创建，之后再创建B链接时(也就是在其他进程/线程中进行登录)，A链接会失效，再使用A链接就会报这个错误。
- 对于多个链接的简单解释: 如果不了解进程/线程的概念，可以这样简单的理解, 每个独立的cmd窗口是一个独立的进程，每个独立的jupyter也是一个独立的进程 ,每auth一次就是建立一个新的链接。
- 目前jqdatasdk不支持超过1个链接，不支持多线程；
- 建议每次获取数据不要超过10w条(防止进程假死)；
- 建议获取数据后使用logout()退出；
- 升级jqdatasdk到最新版本；
- 使用pycharm注意关闭 run with console 选项或者每次运行后关闭控制台界面(每个开启的控制台都相当于一个进程); 使用控制台时注意设置控制台变量加载策略为"按需" ，否则易引发多个链接及输出异常的问题
- 需要更多的链接数，可付费升级为正式账号，为了更高品质展开服务，个人用户咨询【邮箱：sunping@joinquant.com】，机构服务咨询添加微信号JQData02
