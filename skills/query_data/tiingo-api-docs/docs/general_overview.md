---
id: "url-3b7f597"
type: "api"
title: "1.1 Overview"
url: "https://www.tiingo.com/documentation/general/overview"
description: "Tiingo's APIs are built to be performant, consistent, and also support extensive filters to speed up your development time."
source: ""
tags: []
crawl_time: "2026-03-18T02:52:14.704Z"
metadata:
  sections:
    - {"title":"1.1 Overview","content":[{"type":"text","content":"Tiingo's APIs are built to be performant, consistent, and also support extensive filters to speed up your development time."},{"type":"text","content":"Because of this, we hope you will take the time to read the documentation and learn about all of our features, but we also understand you may want to jump right in. So if you want to jump right in, click on any endpoint link, which are located on the sidebar to your left."}]}
    - {"title":"1.1.1 Introduction","content":[{"type":"text","content":"The endpoints are broken up into two different types:"},{"type":"text","content":"To navigate and see how to query data using each of the above methods, use the sidebar on the left and choose an endpoint that interests you."},{"type":"text","content":"Additionally, there are a number of third-party packages that interface with our data and make it even easier to get up and running with our data. You can check them out here:"},{"type":"list","items":["REST Endpoints which provide a RESTful interface to querying data, especially historical data for end-of-day data feeds.","Websocket which provide a websocket interface and are used to stream real-time data. If you are looking for access to a raw firehose of data, the websocket endpoint is how you get it."]}]}
    - {"title":"1.1.2 Authentication","content":[{"type":"text","content":"In order to use the API, you must sign-up to create an account. All accounts are free and if you need higher usage limits, or you have a commercial use case, you can upgade to the Power and/or Commercial plan."},{"type":"text","content":"Once you create an account, your account with be assigned an authentication token. This token is used in place of your username & password throughout the API, so keep it safe like you would your password."},{"type":"text","content":"You can find your API token by clicking here, or to make it easy, your token will be shown below if you are logged in."},{"type":"text","content":"Your API Token is:"},{"type":"text","content":"To see how to use your token to make requests, you can use the code examples throughout the documentation, or check out the section on connecting: 1.2.1 Connecting."},{"type":"code","content":"Not logged-in or registered. Please login or register to see your API Token"}]}
    - {"title":"1.1.3 Usage Limits","content":[{"type":"text","content":"To keep the API affordable to all, each account is given generous rate-limits. We limit based on:"},{"type":"text","content":"We do not rate limit to minute or second, so you are free to make your requests as you desire."},{"type":"text","content":"The basic, power, and commercial power plans offer different levels of rate limits. To see what these rate limits are, visit the pricing page."},{"type":"text","content":"If you need custom limits set you can E-mail our sales team, who will give you a fair and reasonable price. Chances are, if you've been with us for some time and the request is reasonable, we will increase your limits at no charge. Do not hesitate to reach out, we are here for you."},{"type":"list","items":["Hourly Requests - Reset every hour.","Daily Requests - Reset every day at midnight EST.","Monthly Bandwidth - Reset the first of every month at midnight EST."]}]}
    - {"title":"1.1.4 Response Formats","content":[{"type":"text","content":"For most of our REST endpoints, we allow you, the user, to choose which format the data data can be returned in. We support two different return formats:"},{"type":"text","content":"To return data in a particular format, you may pass the format parameter, which can take both \"json\" and \"csv\"."},{"type":"text","content":"When browsing the documentation, you will see at the top of the page which return formats are supported."},{"type":"list","items":["JSON - The data is returned in the JSON data structure. This format allows the most flexibility as we can append meta data as well as debugging data. The downside to this data type is that it requires more bandwidth, which means it may be slower since more data has to be downloaded and parsed by the client side.","CSV - This is a \"bare-bones\" data return type that is often 4-5x faster than JSON. The data is returned in comma-separated-format, which is helpful when importing the data in spreadsheet programs like Excel."]}]}
    - {"title":"1.1.5 Symbology","content":[{"type":"text","content":"Tiingo's symbol format uses dashes (\"-\") instead of periods (\".\") to denote share classes. Our API covers both common share classes and preferred share classes. For example Berkshire class A shares would be \"BRK-A\" and Simon Property Group's Preferred J series shares would be \"SPG-P-J\"."},{"type":"text","content":"More details can be found on the Symbology Appendix page and a full list of tickers can be found in supported_tickers.zip, which is updated daily."}]}
    - {"title":"1.1.6 Permitted Use of Our Data","content":[{"type":"text","content":"For Basic and Power accounts, data is for internal and personal use only. You may not redistribute the data in any form."},{"type":"text","content":"For Commercial accounts, data is licensed for internal commercial usage. You may not redistribute the data in any form."},{"type":"text","content":"If you would like to redistribute the data for commercial or personal use, for example: a presentation, a proposal, a website or app, or any other usage case, please E-mail sales@tiingo.com and include the following:"},{"type":"text","content":"All of our redistributable pricing is based on a flat rate, so it is predictable, simple, and easy. Additionally, redistributable licenses come with substantially higher usage limits to help you save storage costs and speed up loading of our data."},{"type":"text","content":"If you are a developer and are building software for your audience that requires users to submit their own Tiingo API token in order to use your software, and your software is not distributing our data, you do not need to contact us regarding licensing. Please read about our developer program if you are interesting in building software that integrates into Tiingo."},{"type":"list","items":["The use case for the data.","A website link to your firm or academic affiliation.","Whether your company is a start-up (less than 5 employees) or enterprise (5 or more employees)."]}]}
  codeExamples:
    - "Not logged-in or registered. Please login or register to see your API Token"
  tables: []
  tabContents: []
  rawContent: "1. GENERAL\n1.1 Overview\n\nTiingo's APIs are built to be performant, consistent, and also support extensive filters to speed up your development time.\n\nBecause of this, we hope you will take the time to read the documentation and learn about all of our features, but we also understand you may want to jump right in. So if you want to jump right in, click on any endpoint link, which are located on the sidebar to your left.\n\n1.1 GENERAL - OVERVIEW\n1.1.1 Introduction\n\nThe endpoints are broken up into two different types:\n\nREST Endpoints which provide a RESTful interface to querying data, especially historical data for end-of-day data feeds.\nWebsocket which provide a websocket interface and are used to stream real-time data. If you are looking for access to a raw firehose of data, the websocket endpoint is how you get it.\n\nTo navigate and see how to query data using each of the above methods, use the sidebar on the left and choose an endpoint that interests you.\n\nAdditionally, there are a number of third-party packages that interface with our data and make it even easier to get up and running with our data. You can check them out here:\n\n1.1 GENERAL - OVERVIEW\n1.1.2 Authentication\n\nIn order to use the API, you must sign-up to create an account. All accounts are free and if you need higher usage limits, or you have a commercial use case, you can upgade to the Power and/or Commercial plan.\n\nOnce you create an account, your account with be assigned an authentication token. This token is used in place of your username & password throughout the API, so keep it safe like you would your password.\n\nYou can find your API token by clicking here, or to make it easy, your token will be shown below if you are logged in.\n\nYour API Token is:\n\nNot logged-in or registered. Please login or register to see your API Token\n\nTo see how to use your token to make requests, you can use the code examples throughout the documentation, or check out the section on connecting: 1.2.1 Connecting.\n\n1.1 GENERAL - OVERVIEW\n1.1.3 Usage Limits\n\nTo keep the API affordable to all, each account is given generous rate-limits. We limit based on:\n\nHourly Requests - Reset every hour.\nDaily Requests - Reset every day at midnight EST.\nMonthly Bandwidth - Reset the first of every month at midnight EST.\n\nWe do not rate limit to minute or second, so you are free to make your requests as you desire.\n\nThe basic, power, and commercial power plans offer different levels of rate limits. To see what these rate limits are, visit the pricing page.\n\nIf you need custom limits set you can E-mail our sales team, who will give you a fair and reasonable price. Chances are, if you've been with us for some time and the request is reasonable, we will increase your limits at no charge. Do not hesitate to reach out, we are here for you.\n\n1.1 GENERAL - OVERVIEW\n1.1.4 Response Formats\n\nFor most of our REST endpoints, we allow you, the user, to choose which format the data data can be returned in. We support two different return formats:\n\nJSON - The data is returned in the JSON data structure. This format allows the most flexibility as we can append meta data as well as debugging data. The downside to this data type is that it requires more bandwidth, which means it may be slower since more data has to be downloaded and parsed by the client side.\nCSV - This is a \"bare-bones\" data return type that is often 4-5x faster than JSON. The data is returned in comma-separated-format, which is helpful when importing the data in spreadsheet programs like Excel.\n\nTo return data in a particular format, you may pass the format parameter, which can take both \"json\" and \"csv\".\n\nWhen browsing the documentation, you will see at the top of the page which return formats are supported.\n\n1.1 GENERAL - OVERVIEW\n1.1.5 Symbology\n\nTiingo's symbol format uses dashes (\"-\") instead of periods (\".\") to denote share classes. Our API covers both common share classes and preferred share classes. For example Berkshire class A shares would be \"BRK-A\" and Simon Property Group's Preferred J series shares would be \"SPG-P-J\".\n\nMore details can be found on the Symbology Appendix page and a full list of tickers can be found in supported_tickers.zip, which is updated daily.\n\n1.1 GENERAL - OVERVIEW\n1.1.6 Permitted Use of Our Data\n\nFor Basic and Power accounts, data is for internal and personal use only. You may not redistribute the data in any form.\n\nFor Commercial accounts, data is licensed for internal commercial usage. You may not redistribute the data in any form.\n\nIf you would like to redistribute the data for commercial or personal use, for example: a presentation, a proposal, a website or app, or any other usage case, please E-mail sales@tiingo.com and include the following:\n\nThe use case for the data.\nA website link to your firm or academic affiliation.\nWhether your company is a start-up (less than 5 employees) or enterprise (5 or more employees).\n\nAll of our redistributable pricing is based on a flat rate, so it is predictable, simple, and easy. Additionally, redistributable licenses come with substantially higher usage limits to help you save storage costs and speed up loading of our data.\n\nIf you are a developer and are building software for your audience that requires users to submit their own Tiingo API token in order to use your software, and your software is not distributing our data, you do not need to contact us regarding licensing. Please read about our developer program if you are interesting in building software that integrates into Tiingo."
  suggestedFilename: "general_overview"
---

# 1.1 Overview

## 源URL

https://www.tiingo.com/documentation/general/overview

## 描述

Tiingo's APIs are built to be performant, consistent, and also support extensive filters to speed up your development time.

## 代码示例

```text
Not logged-in or registered. Please login or register to see your API Token
```

## 文档正文

Tiingo's APIs are built to be performant, consistent, and also support extensive filters to speed up your development time.

1. GENERAL
1.1 Overview

Tiingo's APIs are built to be performant, consistent, and also support extensive filters to speed up your development time.

Because of this, we hope you will take the time to read the documentation and learn about all of our features, but we also understand you may want to jump right in. So if you want to jump right in, click on any endpoint link, which are located on the sidebar to your left.

1.1 GENERAL - OVERVIEW
1.1.1 Introduction

The endpoints are broken up into two different types:

REST Endpoints which provide a RESTful interface to querying data, especially historical data for end-of-day data feeds.
Websocket which provide a websocket interface and are used to stream real-time data. If you are looking for access to a raw firehose of data, the websocket endpoint is how you get it.

To navigate and see how to query data using each of the above methods, use the sidebar on the left and choose an endpoint that interests you.

Additionally, there are a number of third-party packages that interface with our data and make it even easier to get up and running with our data. You can check them out here:

1.1 GENERAL - OVERVIEW
1.1.2 Authentication

In order to use the API, you must sign-up to create an account. All accounts are free and if you need higher usage limits, or you have a commercial use case, you can upgade to the Power and/or Commercial plan.

Once you create an account, your account with be assigned an authentication token. This token is used in place of your username & password throughout the API, so keep it safe like you would your password.

You can find your API token by clicking here, or to make it easy, your token will be shown below if you are logged in.

Your API Token is:

Not logged-in or registered. Please login or register to see your API Token

To see how to use your token to make requests, you can use the code examples throughout the documentation, or check out the section on connecting: 1.2.1 Connecting.

1.1 GENERAL - OVERVIEW
1.1.3 Usage Limits

To keep the API affordable to all, each account is given generous rate-limits. We limit based on:

Hourly Requests - Reset every hour.
Daily Requests - Reset every day at midnight EST.
Monthly Bandwidth - Reset the first of every month at midnight EST.

We do not rate limit to minute or second, so you are free to make your requests as you desire.

The basic, power, and commercial power plans offer different levels of rate limits. To see what these rate limits are, visit the pricing page.

If you need custom limits set you can E-mail our sales team, who will give you a fair and reasonable price. Chances are, if you've been with us for some time and the request is reasonable, we will increase your limits at no charge. Do not hesitate to reach out, we are here for you.

1.1 GENERAL - OVERVIEW
1.1.4 Response Formats

For most of our REST endpoints, we allow you, the user, to choose which format the data data can be returned in. We support two different return formats:

JSON - The data is returned in the JSON data structure. This format allows the most flexibility as we can append meta data as well as debugging data. The downside to this data type is that it requires more bandwidth, which means it may be slower since more data has to be downloaded and parsed by the client side.
CSV - This is a "bare-bones" data return type that is often 4-5x faster than JSON. The data is returned in comma-separated-format, which is helpful when importing the data in spreadsheet programs like Excel.

To return data in a particular format, you may pass the format parameter, which can take both "json" and "csv".

When browsing the documentation, you will see at the top of the page which return formats are supported.

1.1 GENERAL - OVERVIEW
1.1.5 Symbology

Tiingo's symbol format uses dashes ("-") instead of periods (".") to denote share classes. Our API covers both common share classes and preferred share classes. For example Berkshire class A shares would be "BRK-A" and Simon Property Group's Preferred J series shares would be "SPG-P-J".

More details can be found on the Symbology Appendix page and a full list of tickers can be found in supported_tickers.zip, which is updated daily.

1.1 GENERAL - OVERVIEW
1.1.6 Permitted Use of Our Data

For Basic and Power accounts, data is for internal and personal use only. You may not redistribute the data in any form.

For Commercial accounts, data is licensed for internal commercial usage. You may not redistribute the data in any form.

If you would like to redistribute the data for commercial or personal use, for example: a presentation, a proposal, a website or app, or any other usage case, please E-mail sales@tiingo.com and include the following:

The use case for the data.
A website link to your firm or academic affiliation.
Whether your company is a start-up (less than 5 employees) or enterprise (5 or more employees).

All of our redistributable pricing is based on a flat rate, so it is pr
