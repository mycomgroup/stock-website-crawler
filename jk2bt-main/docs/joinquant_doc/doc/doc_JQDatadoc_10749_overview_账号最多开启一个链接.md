---
id: "url-36496055"
type: "website"
title: "账号最多开启一个链接"
url: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10749"
description: "JQData目前的服务器地址：39.107.190.114，端口号：7000"
source: ""
tags: []
crawl_time: "2026-03-27T07:44:12.295Z"
metadata:
  parser: "JoinquantHelpParser"
  actualUrl: "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10749"
  headings:
    - {"level":3,"text":"账号最多开启一个链接","id":""}
    - {"level":3,"text":"常见报错解决方法","id":""}
    - {"level":3,"text":"有关pandas的版本说明","id":""}
  paragraphs:
    - "描述"
    - "JQData目前的服务器地址：39.107.190.114，端口号：7000"
    - "这个报错一般是由您网络问题造成的，常见解决方法如下:"
  lists:
    - {"type":"ul","items":["这是同时打开了多个链接造成的；每次auth之后会创建新的链接，是长连接的（thrift长连接,不支持在其他进程/线程中共享）；使用logout()或者关闭进程后会断开；默认同时最多存在一个链接，如果A链接被创建，之后再创建B链接时(也就是在其他进程/线程中进行登录)，A链接会失效，再使用A链接就会报这个错误。","对于多个链接的简单解释: 如果不了解进程/线程的概念，可以这样简单的理解, 每个独立的cmd窗口是一个独立的进程，每个独立的jupyter也是一个独立的进程 ,每auth一次就是建立一个新的链接。","目前jqdatasdk不支持超过1个链接，不支持多线程；","建议每次获取数据不要超过10w条(防止进程假死)；","建议获取数据后使用logout()退出；","升级jqdatasdk到最新版本；","使用pycharm注意关闭 run with console 选项或者每次运行后关闭控制台界面(每个开启的控制台都相当于一个进程); 使用控制台时注意设置控制台变量加载策略为\"按需\" ，否则易引发多个链接及输出异常的问题","需要更多的链接数，可付费升级为正式账号"]}
    - {"type":"ul","items":["检查下网络是否正常/稳定；","请检查下您是否使用代理或者网络被禁止了，目前不支持代理；","是否您公司对网络或者端口有限制；","尝试使用其他网络；","升级JQData至最新版本；","不建议高频的login和logout；"]}
    - {"type":"ul","items":["Pandas不同版本间的兼容性较低，我们也在持续的优化适应Pandas的新特性，1.8.6及之后的版本支持pandas 0.25.3以上的版本。","如遇到类似 AttributeError: 'DataFrame' object has no attribute '_attrs' 的报错，可使用命令 `pip install jqdatasdk -U `升级jqdatasdk至最新版本。","Pandas为0.25.0及以上时，受panel影响的接口(get_price, get_fundamentals_continuously等)，强制设置panel=False"]}
  tables: []
  codeBlocks: []
  blockquotes: []
  mainContent:
    - {"type":"heading","level":3,"content":"账号最多开启一个链接"}
    - {"type":"paragraph","content":"描述"}
    - {"type":"list","listType":"ul","items":["这是同时打开了多个链接造成的；每次auth之后会创建新的链接，是长连接的（thrift长连接,不支持在其他进程/线程中共享）；使用logout()或者关闭进程后会断开；默认同时最多存在一个链接，如果A链接被创建，之后再创建B链接时(也就是在其他进程/线程中进行登录)，A链接会失效，再使用A链接就会报这个错误。","对于多个链接的简单解释: 如果不了解进程/线程的概念，可以这样简单的理解, 每个独立的cmd窗口是一个独立的进程，每个独立的jupyter也是一个独立的进程 ,每auth一次就是建立一个新的链接。","目前jqdatasdk不支持超过1个链接，不支持多线程；","建议每次获取数据不要超过10w条(防止进程假死)；","建议获取数据后使用logout()退出；","升级jqdatasdk到最新版本；","使用pycharm注意关闭 run with console 选项或者每次运行后关闭控制台界面(每个开启的控制台都相当于一个进程); 使用控制台时注意设置控制台变量加载策略为\"按需\" ，否则易引发多个链接及输出异常的问题","需要更多的链接数，可付费升级为正式账号"]}
    - {"type":"heading","level":3,"content":"常见报错解决方法"}
    - {"type":"paragraph","content":"JQData目前的服务器地址：39.107.190.114，端口号：7000"}
    - {"type":"paragraph","content":"这个报错一般是由您网络问题造成的，常见解决方法如下:"}
    - {"type":"list","listType":"ul","items":["检查下网络是否正常/稳定；","请检查下您是否使用代理或者网络被禁止了，目前不支持代理；","是否您公司对网络或者端口有限制；","尝试使用其他网络；","升级JQData至最新版本；","不建议高频的login和logout；"]}
    - {"type":"heading","level":3,"content":"有关pandas的版本说明"}
    - {"type":"list","listType":"ul","items":["Pandas不同版本间的兼容性较低，我们也在持续的优化适应Pandas的新特性，1.8.6及之后的版本支持pandas 0.25.3以上的版本。","如遇到类似 AttributeError: 'DataFrame' object has no attribute '_attrs' 的报错，可使用命令 `pip install jqdatasdk -U `升级jqdatasdk至最新版本。","Pandas为0.25.0及以上时，受panel影响的接口(get_price, get_fundamentals_continuously等)，强制设置panel=False"]}
  suggestedFilename: "doc_JQDatadoc_10749_overview_账号最多开启一个链接"
  pageKind: "doc"
  pageName: "JQDatadoc"
  pageId: "10749"
  sectionHash: ""
  sourceTitle: "JQData使用说明"
  treeRootTitle: ""
---

# 账号最多开启一个链接

## 源URL

https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10749

## 描述

JQData目前的服务器地址：39.107.190.114，端口号：7000

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
- 需要更多的链接数，可付费升级为正式账号

#### 常见报错解决方法

JQData目前的服务器地址：39.107.190.114，端口号：7000

这个报错一般是由您网络问题造成的，常见解决方法如下:

- 检查下网络是否正常/稳定；
- 请检查下您是否使用代理或者网络被禁止了，目前不支持代理；
- 是否您公司对网络或者端口有限制；
- 尝试使用其他网络；
- 升级JQData至最新版本；
- 不建议高频的login和logout；

#### 有关pandas的版本说明

- Pandas不同版本间的兼容性较低，我们也在持续的优化适应Pandas的新特性，1.8.6及之后的版本支持pandas 0.25.3以上的版本。
- 如遇到类似 AttributeError: 'DataFrame' object has no attribute '_attrs' 的报错，可使用命令 `pip install jqdatasdk -U `升级jqdatasdk至最新版本。
- Pandas为0.25.0及以上时，受panel影响的接口(get_price, get_fundamentals_continuously等)，强制设置panel=False
