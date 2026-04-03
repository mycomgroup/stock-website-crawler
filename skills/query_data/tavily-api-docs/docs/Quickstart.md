---
id: "url-7b0a29f1"
type: "website"
title: "Quickstart"
url: "https://docs.tavily.com/sdk"
description: "Integrate Tavily's powerful APIs natively in your Python apps."
source: ""
tags: []
crawl_time: "2026-03-18T04:14:14.906Z"
metadata:
  subtype: "article"
  headings:
    - {"level":5,"text":"API Reference"}
    - {"level":5,"text":"Enterprise API Reference"}
    - {"level":5,"text":"Python SDK"}
    - {"level":5,"text":"JavaScript SDK"}
    - {"level":5,"text":"Best Practices"}
    - {"level":1,"text":"Quickstart"}
    - {"level":2,"text":"[​](https://docs.tavily.com/sdk/python/quick-start#introduction)Introduction"}
    - {"level":2,"text":"GitHub"}
    - {"level":2,"text":"PyPI"}
    - {"level":2,"text":"[​](https://docs.tavily.com/sdk/python/quick-start#quickstart)Quickstart"}
    - {"level":2,"text":"Get your free API key"}
    - {"level":3,"text":"[​](https://docs.tavily.com/sdk/python/quick-start#installation)Installation"}
    - {"level":3,"text":"[​](https://docs.tavily.com/sdk/python/quick-start#usage)Usage"}
    - {"level":2,"text":"[​](https://docs.tavily.com/sdk/python/quick-start#features)Features"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/sdk/python/quick-start#introduction)Introduction"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/sdk/python/quick-start#quickstart)Quickstart"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/sdk/python/quick-start#installation)Installation"}
    - {"type":"codeblock","language":"","content":"pip install tavily-python"}
    - {"type":"heading","level":3,"content":"[​](https://docs.tavily.com/sdk/python/quick-start#usage)Usage"}
    - {"type":"codeblock","language":"","content":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.search(\"Who is Leo Messi?\")\n\nprint(response)"}
    - {"type":"codeblock","language":"","content":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.extract(\"https://en.wikipedia.org/wiki/Lionel_Messi\")\n\nprint(response)"}
    - {"type":"codeblock","language":"","content":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.crawl(\"https://docs.tavily.com\", instructions=\"Find all pages on the Python SDK\")\n\nprint(response)"}
    - {"type":"heading","level":2,"content":"[​](https://docs.tavily.com/sdk/python/quick-start#features)Features"}
    - {"type":"list","listType":"ul","items":["The `search` function lets you harness the full power of Tavily Search.","The `extract` function allows you to easily retrieve web content with Tavily Extract.","The `crawl` and `map`functions allow you to intelligently traverse websites and extract content."]}
  paragraphs: []
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Introduction](https://docs.tavily.com/documentation/api-reference/introduction)","[POSTSearch](https://docs.tavily.com/documentation/api-reference/endpoint/search)","[POSTExtract](https://docs.tavily.com/documentation/api-reference/endpoint/extract)","[POSTCrawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl)","[POSTMap](https://docs.tavily.com/documentation/api-reference/endpoint/map)","Research[POSTCreate Research Task](https://docs.tavily.com/documentation/api-reference/endpoint/research)[GETGet Research Task Status](https://docs.tavily.com/documentation/api-reference/endpoint/research-get)[Streaming](https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming)","[POSTCreate Research Task](https://docs.tavily.com/documentation/api-reference/endpoint/research)","[GETGet Research Task Status](https://docs.tavily.com/documentation/api-reference/endpoint/research-get)","[Streaming](https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming)","[GETUsage](https://docs.tavily.com/documentation/api-reference/endpoint/usage)"]}
    - {"type":"ul","items":["[POSTCreate Research Task](https://docs.tavily.com/documentation/api-reference/endpoint/research)","[GETGet Research Task Status](https://docs.tavily.com/documentation/api-reference/endpoint/research-get)","[Streaming](https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming)"]}
    - {"type":"ul","items":["API Key Generator"]}
    - {"type":"ul","items":["[Quickstart](https://docs.tavily.com/sdk/python/quick-start)","[SDK Reference](https://docs.tavily.com/sdk/python/reference)"]}
    - {"type":"ul","items":["[Quickstart](https://docs.tavily.com/sdk/javascript/quick-start)","[SDK Reference](https://docs.tavily.com/sdk/javascript/reference)"]}
    - {"type":"ul","items":["[Search](https://docs.tavily.com/documentation/best-practices/best-practices-search)","[Extract](https://docs.tavily.com/documentation/best-practices/best-practices-extract)","[Crawl](https://docs.tavily.com/documentation/best-practices/best-practices-crawl)","[Research](https://docs.tavily.com/documentation/best-practices/best-practices-research)","[API Key Management](https://docs.tavily.com/documentation/best-practices/api-key-management)"]}
    - {"type":"ul","items":["[Introduction](https://docs.tavily.com/sdk/python/quick-start#introduction)","[Quickstart](https://docs.tavily.com/sdk/python/quick-start#quickstart)","[Installation](https://docs.tavily.com/sdk/python/quick-start#installation)","[Usage](https://docs.tavily.com/sdk/python/quick-start#usage)","[Features](https://docs.tavily.com/sdk/python/quick-start#features)"]}
    - {"type":"ul","items":["The search function lets you harness the full power of Tavily Search.","The extract function allows you to easily retrieve web content with Tavily Extract.","The crawl and mapfunctions allow you to intelligently traverse websites and extract content."]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"pip install tavily-python"}
    - {"language":"text","code":"pip install tavily-python"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.search(\"Who is Leo Messi?\")\n\nprint(response)"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.search(\"Who is Leo Messi?\")\n\nprint(response)"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.extract(\"https://en.wikipedia.org/wiki/Lionel_Messi\")\n\nprint(response)"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.extract(\"https://en.wikipedia.org/wiki/Lionel_Messi\")\n\nprint(response)"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.crawl(\"https://docs.tavily.com\", instructions=\"Find all pages on the Python SDK\")\n\nprint(response)"}
    - {"language":"text","code":"from tavily import TavilyClient\n\ntavily_client = TavilyClient(api_key=\"tvly-YOUR_API_KEY\")\nresponse = tavily_client.crawl(\"https://docs.tavily.com\", instructions=\"Find all pages on the Python SDK\")\n\nprint(response)"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Quickstart_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Quickstart_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://img.shields.io/github/stars/tavily-ai/tavily-python?style=social","localPath":"Quickstart_-_Tavily_Docs/image_3.jpg","alt":"GitHub Repo stars","title":""}
    - {"src":"https://img.shields.io/pypi/dm/tavily-python","localPath":"Quickstart_-_Tavily_Docs/image_4.jpg","alt":"PyPI downloads","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Quickstart_-_Tavily_Docs/image_5.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Quickstart_-_Tavily_Docs/image_6.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Quickstart_-_Tavily_Docs/image_7.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Quickstart_-_Tavily_Docs/image_8.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Quickstart_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Quickstart_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Quickstart_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Quickstart_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Quickstart_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Quickstart_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Quickstart_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Quickstart_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":18,"filename":"Quickstart_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":19,"filename":"Quickstart_-_Tavily_Docs/svg_19.png","width":16,"height":16}
    - {"type":"svg","index":20,"filename":"Quickstart_-_Tavily_Docs/svg_20.png","width":16,"height":16}
    - {"type":"svg","index":21,"filename":"Quickstart_-_Tavily_Docs/svg_21.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Quickstart_-_Tavily_Docs/svg_22.png","width":16,"height":16}
    - {"type":"svg","index":23,"filename":"Quickstart_-_Tavily_Docs/svg_23.png","width":16,"height":16}
    - {"type":"svg","index":24,"filename":"Quickstart_-_Tavily_Docs/svg_24.png","width":16,"height":16}
    - {"type":"svg","index":25,"filename":"Quickstart_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"Quickstart_-_Tavily_Docs/svg_26.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"Quickstart_-_Tavily_Docs/svg_27.png","width":12,"height":12}
    - {"type":"svg","index":28,"filename":"Quickstart_-_Tavily_Docs/svg_28.png","width":16,"height":16}
    - {"type":"svg","index":32,"filename":"Quickstart_-_Tavily_Docs/svg_32.png","width":14,"height":18}
    - {"type":"svg","index":33,"filename":"Quickstart_-_Tavily_Docs/svg_33.png","width":14,"height":12}
    - {"type":"svg","index":34,"filename":"Quickstart_-_Tavily_Docs/svg_34.png","width":16,"height":16}
    - {"type":"svg","index":35,"filename":"Quickstart_-_Tavily_Docs/svg_35.png","width":24,"height":24}
    - {"type":"svg","index":36,"filename":"Quickstart_-_Tavily_Docs/svg_36.png","width":16,"height":16}
    - {"type":"svg","index":37,"filename":"Quickstart_-_Tavily_Docs/svg_37.png","width":24,"height":24}
    - {"type":"svg","index":38,"filename":"Quickstart_-_Tavily_Docs/svg_38.png","width":14,"height":12}
    - {"type":"svg","index":39,"filename":"Quickstart_-_Tavily_Docs/svg_39.png","width":16,"height":16}
    - {"type":"svg","index":40,"filename":"Quickstart_-_Tavily_Docs/svg_40.png","width":24,"height":24}
    - {"type":"svg","index":41,"filename":"Quickstart_-_Tavily_Docs/svg_41.png","width":14,"height":12}
    - {"type":"svg","index":42,"filename":"Quickstart_-_Tavily_Docs/svg_42.png","width":16,"height":16}
    - {"type":"svg","index":43,"filename":"Quickstart_-_Tavily_Docs/svg_43.png","width":16,"height":16}
    - {"type":"svg","index":44,"filename":"Quickstart_-_Tavily_Docs/svg_44.png","width":14,"height":12}
    - {"type":"svg","index":45,"filename":"Quickstart_-_Tavily_Docs/svg_45.png","width":16,"height":16}
    - {"type":"svg","index":46,"filename":"Quickstart_-_Tavily_Docs/svg_46.png","width":16,"height":16}
    - {"type":"svg","index":47,"filename":"Quickstart_-_Tavily_Docs/svg_47.png","width":16,"height":16}
    - {"type":"svg","index":48,"filename":"Quickstart_-_Tavily_Docs/svg_48.png","width":16,"height":16}
    - {"type":"svg","index":49,"filename":"Quickstart_-_Tavily_Docs/svg_49.png","width":16,"height":16}
    - {"type":"svg","index":50,"filename":"Quickstart_-_Tavily_Docs/svg_50.png","width":16,"height":16}
    - {"type":"svg","index":51,"filename":"Quickstart_-_Tavily_Docs/svg_51.png","width":14,"height":12}
    - {"type":"svg","index":52,"filename":"Quickstart_-_Tavily_Docs/svg_52.png","width":14,"height":14}
    - {"type":"svg","index":53,"filename":"Quickstart_-_Tavily_Docs/svg_53.png","width":14,"height":14}
    - {"type":"svg","index":54,"filename":"Quickstart_-_Tavily_Docs/svg_54.png","width":14,"height":14}
    - {"type":"svg","index":59,"filename":"Quickstart_-_Tavily_Docs/svg_59.png","width":20,"height":20}
    - {"type":"svg","index":60,"filename":"Quickstart_-_Tavily_Docs/svg_60.png","width":20,"height":20}
    - {"type":"svg","index":61,"filename":"Quickstart_-_Tavily_Docs/svg_61.png","width":20,"height":20}
    - {"type":"svg","index":62,"filename":"Quickstart_-_Tavily_Docs/svg_62.png","width":20,"height":20}
    - {"type":"svg","index":63,"filename":"Quickstart_-_Tavily_Docs/svg_63.png","width":49,"height":14}
    - {"type":"svg","index":64,"filename":"Quickstart_-_Tavily_Docs/svg_64.png","width":16,"height":16}
    - {"type":"svg","index":65,"filename":"Quickstart_-_Tavily_Docs/svg_65.png","width":16,"height":16}
    - {"type":"svg","index":66,"filename":"Quickstart_-_Tavily_Docs/svg_66.png","width":16,"height":16}
    - {"type":"svg","index":76,"filename":"Quickstart_-_Tavily_Docs/svg_76.png","width":16,"height":16}
    - {"type":"svg","index":77,"filename":"Quickstart_-_Tavily_Docs/svg_77.png","width":14,"height":14}
    - {"type":"svg","index":78,"filename":"Quickstart_-_Tavily_Docs/svg_78.png","width":16,"height":16}
    - {"type":"svg","index":79,"filename":"Quickstart_-_Tavily_Docs/svg_79.png","width":12,"height":12}
    - {"type":"svg","index":80,"filename":"Quickstart_-_Tavily_Docs/svg_80.png","width":14,"height":14}
    - {"type":"svg","index":81,"filename":"Quickstart_-_Tavily_Docs/svg_81.png","width":16,"height":16}
    - {"type":"svg","index":82,"filename":"Quickstart_-_Tavily_Docs/svg_82.png","width":12,"height":12}
    - {"type":"svg","index":83,"filename":"Quickstart_-_Tavily_Docs/svg_83.png","width":14,"height":14}
    - {"type":"svg","index":84,"filename":"Quickstart_-_Tavily_Docs/svg_84.png","width":16,"height":16}
    - {"type":"svg","index":85,"filename":"Quickstart_-_Tavily_Docs/svg_85.png","width":12,"height":12}
    - {"type":"svg","index":86,"filename":"Quickstart_-_Tavily_Docs/svg_86.png","width":14,"height":14}
  chartData: []
  blockquotes: []
  definitionLists: []
  horizontalRules: 0
  videos: []
  audios: []
  apiData: 0
  pageFeatures:
    suggestedType: "article"
    confidence: 45
    signals:
      - "article-like"
      - "api-doc-like"
  tabsAndDropdowns: []
  dateFilters: []
---

# Quickstart

## 源URL

https://docs.tavily.com/sdk

## 描述

Integrate Tavily's powerful APIs natively in your Python apps.

## 内容

### Introduction

### Quickstart

#### Installation

```text
pip install tavily-python
```

#### Usage

```text
from tavily import TavilyClient

tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = tavily_client.search("Who is Leo Messi?")

print(response)
```

```text
from tavily import TavilyClient

tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = tavily_client.extract("https://en.wikipedia.org/wiki/Lionel_Messi")

print(response)
```

```text
from tavily import TavilyClient

tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")
response = tavily_client.crawl("https://docs.tavily.com", instructions="Find all pages on the Python SDK")

print(response)
```

### Features

- The `search` function lets you harness the full power of Tavily Search.
- The `extract` function allows you to easily retrieve web content with Tavily Extract.
- The `crawl` and `map`functions allow you to intelligently traverse websites and extract content.

## 图片

![light logo](Quickstart_-_Tavily_Docs/image_1.svg)

![dark logo](Quickstart_-_Tavily_Docs/image_2.svg)

![GitHub Repo stars](Quickstart_-_Tavily_Docs/image_3.jpg)

![PyPI downloads](Quickstart_-_Tavily_Docs/image_4.jpg)

![light logo](Quickstart_-_Tavily_Docs/image_5.svg)

![dark logo](Quickstart_-_Tavily_Docs/image_6.svg)

![tavily-logo](Quickstart_-_Tavily_Docs/image_7.png)

![Powered by Onetrust](Quickstart_-_Tavily_Docs/image_8.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Quickstart_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Quickstart_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Quickstart_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Quickstart_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Quickstart_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Quickstart_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Quickstart_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 16](Quickstart_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 18](Quickstart_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 19](Quickstart_-_Tavily_Docs/svg_19.png)
*尺寸: 16x16px*

![SVG图表 20](Quickstart_-_Tavily_Docs/svg_20.png)
*尺寸: 16x16px*

![SVG图表 21](Quickstart_-_Tavily_Docs/svg_21.png)
*尺寸: 16x16px*

![SVG图表 22](Quickstart_-_Tavily_Docs/svg_22.png)
*尺寸: 16x16px*

![SVG图表 23](Quickstart_-_Tavily_Docs/svg_23.png)
*尺寸: 16x16px*

![SVG图表 24](Quickstart_-_Tavily_Docs/svg_24.png)
*尺寸: 16x16px*

![SVG图表 25](Quickstart_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](Quickstart_-_Tavily_Docs/svg_26.png)
*尺寸: 16x16px*

![SVG图表 27](Quickstart_-_Tavily_Docs/svg_27.png)
*尺寸: 12x12px*

![SVG图表 28](Quickstart_-_Tavily_Docs/svg_28.png)
*尺寸: 16x16px*

![SVG图表 32](Quickstart_-_Tavily_Docs/svg_32.png)
*尺寸: 14x18px*

![SVG图表 33](Quickstart_-_Tavily_Docs/svg_33.png)
*尺寸: 14x12px*

![SVG图表 34](Quickstart_-_Tavily_Docs/svg_34.png)
*尺寸: 16x16px*

![SVG图表 35](Quickstart_-_Tavily_Docs/svg_35.png)
*尺寸: 24x24px*

![SVG图表 36](Quickstart_-_Tavily_Docs/svg_36.png)
*尺寸: 16x16px*

![SVG图表 37](Quickstart_-_Tavily_Docs/svg_37.png)
*尺寸: 24x24px*

![SVG图表 38](Quickstart_-_Tavily_Docs/svg_38.png)
*尺寸: 14x12px*

![SVG图表 39](Quickstart_-_Tavily_Docs/svg_39.png)
*尺寸: 16x16px*

![SVG图表 40](Quickstart_-_Tavily_Docs/svg_40.png)
*尺寸: 24x24px*

![SVG图表 41](Quickstart_-_Tavily_Docs/svg_41.png)
*尺寸: 14x12px*

![SVG图表 42](Quickstart_-_Tavily_Docs/svg_42.png)
*尺寸: 16x16px*

![SVG图表 43](Quickstart_-_Tavily_Docs/svg_43.png)
*尺寸: 16x16px*

![SVG图表 44](Quickstart_-_Tavily_Docs/svg_44.png)
*尺寸: 14x12px*

![SVG图表 45](Quickstart_-_Tavily_Docs/svg_45.png)
*尺寸: 16x16px*

![SVG图表 46](Quickstart_-_Tavily_Docs/svg_46.png)
*尺寸: 16x16px*

![SVG图表 47](Quickstart_-_Tavily_Docs/svg_47.png)
*尺寸: 16x16px*

![SVG图表 48](Quickstart_-_Tavily_Docs/svg_48.png)
*尺寸: 16x16px*

![SVG图表 49](Quickstart_-_Tavily_Docs/svg_49.png)
*尺寸: 16x16px*

![SVG图表 50](Quickstart_-_Tavily_Docs/svg_50.png)
*尺寸: 16x16px*

![SVG图表 51](Quickstart_-_Tavily_Docs/svg_51.png)
*尺寸: 14x12px*

![SVG图表 52](Quickstart_-_Tavily_Docs/svg_52.png)
*尺寸: 14x14px*

![SVG图表 53](Quickstart_-_Tavily_Docs/svg_53.png)
*尺寸: 14x14px*

![SVG图表 54](Quickstart_-_Tavily_Docs/svg_54.png)
*尺寸: 14x14px*

![SVG图表 59](Quickstart_-_Tavily_Docs/svg_59.png)
*尺寸: 20x20px*

![SVG图表 60](Quickstart_-_Tavily_Docs/svg_60.png)
*尺寸: 20x20px*

![SVG图表 61](Quickstart_-_Tavily_Docs/svg_61.png)
*尺寸: 20x20px*

![SVG图表 62](Quickstart_-_Tavily_Docs/svg_62.png)
*尺寸: 20x20px*

![SVG图表 63](Quickstart_-_Tavily_Docs/svg_63.png)
*尺寸: 49x14px*

![SVG图表 64](Quickstart_-_Tavily_Docs/svg_64.png)
*尺寸: 16x16px*

![SVG图表 65](Quickstart_-_Tavily_Docs/svg_65.png)
*尺寸: 16x16px*

![SVG图表 66](Quickstart_-_Tavily_Docs/svg_66.png)
*尺寸: 16x16px*

![SVG图表 76](Quickstart_-_Tavily_Docs/svg_76.png)
*尺寸: 16x16px*

![SVG图表 77](Quickstart_-_Tavily_Docs/svg_77.png)
*尺寸: 14x14px*

![SVG图表 78](Quickstart_-_Tavily_Docs/svg_78.png)
*尺寸: 16x16px*

![SVG图表 79](Quickstart_-_Tavily_Docs/svg_79.png)
*尺寸: 12x12px*

![SVG图表 80](Quickstart_-_Tavily_Docs/svg_80.png)
*尺寸: 14x14px*

![SVG图表 81](Quickstart_-_Tavily_Docs/svg_81.png)
*尺寸: 16x16px*

![SVG图表 82](Quickstart_-_Tavily_Docs/svg_82.png)
*尺寸: 12x12px*

![SVG图表 83](Quickstart_-_Tavily_Docs/svg_83.png)
*尺寸: 14x14px*

![SVG图表 84](Quickstart_-_Tavily_Docs/svg_84.png)
*尺寸: 16x16px*

![SVG图表 85](Quickstart_-_Tavily_Docs/svg_85.png)
*尺寸: 12x12px*

![SVG图表 86](Quickstart_-_Tavily_Docs/svg_86.png)
*尺寸: 14x14px*
