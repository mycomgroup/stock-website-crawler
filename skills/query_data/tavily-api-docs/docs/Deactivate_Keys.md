---
id: "url-3bdb2741"
type: "website"
title: "Deactivate Keys"
url: "https://docs.tavily.com/documentation/enterprise/deactivate-keys"
description: "Deactivate API keys either in bulk by request_id or individually. Option A — Deactivate by request ID: Pass a request_id in the request body to deactivate all keys from that generation request. Option B — Deactivate individual key: Set the key you want to deactivate in the Authorization header. No request body is required."
source: ""
tags: []
crawl_time: "2026-03-18T07:13:08.138Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":5,"text":"API Reference"}
    - {"level":5,"text":"Enterprise API Reference"}
    - {"level":5,"text":"Python SDK"}
    - {"level":5,"text":"JavaScript SDK"}
    - {"level":5,"text":"Best Practices"}
    - {"level":1,"text":"Deactivate Keys"}
    - {"level":4,"text":"Authorizations"}
    - {"level":4,"text":"Body"}
    - {"level":4,"text":"Response"}
    - {"level":2,"text":"Privacy Preference Center"}
    - {"level":3,"text":"Manage Consent Preferences"}
    - {"level":4,"text":"Strictly Necessary Cookies"}
    - {"level":4,"text":"Functional Cookies"}
    - {"level":4,"text":"Performance Cookies"}
    - {"level":4,"text":"Targeting Cookies"}
    - {"level":3,"text":"Cookie List"}
  mainContent:
    - {"type":"list","listType":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"heading","level":5,"content":"API Reference"}
    - {"type":"list","listType":"ul","items":["[Introduction](https://docs.tavily.com/documentation/api-reference/introduction)","[POSTSearch](https://docs.tavily.com/documentation/api-reference/endpoint/search)","[POSTExtract](https://docs.tavily.com/documentation/api-reference/endpoint/extract)","[POSTCrawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl)","[POSTMap](https://docs.tavily.com/documentation/api-reference/endpoint/map)","Research[POSTCreate Research Task](https://docs.tavily.com/documentation/api-reference/endpoint/research)[GETGet Research Task Status](https://docs.tavily.com/documentation/api-reference/endpoint/research-get)[Streaming](https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming)","[POSTCreate Research Task](https://docs.tavily.com/documentation/api-reference/endpoint/research)","[GETGet Research Task Status](https://docs.tavily.com/documentation/api-reference/endpoint/research-get)","[Streaming](https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming)","[GETUsage](https://docs.tavily.com/documentation/api-reference/endpoint/usage)"]}
    - {"type":"heading","level":5,"content":"Enterprise API Reference"}
    - {"type":"list","listType":"ul","items":["API Key Generator[POSTGenerate Keys](https://docs.tavily.com/documentation/enterprise/generate-keys)[POSTDeactivate Keys](https://docs.tavily.com/documentation/enterprise/deactivate-keys)[GETKey Info](https://docs.tavily.com/documentation/enterprise/key-info)","[POSTGenerate Keys](https://docs.tavily.com/documentation/enterprise/generate-keys)","[POSTDeactivate Keys](https://docs.tavily.com/documentation/enterprise/deactivate-keys)","[GETKey Info](https://docs.tavily.com/documentation/enterprise/key-info)"]}
    - {"type":"heading","level":5,"content":"Python SDK"}
    - {"type":"list","listType":"ul","items":["[Quickstart](https://docs.tavily.com/sdk/python/quick-start)","[SDK Reference](https://docs.tavily.com/sdk/python/reference)"]}
    - {"type":"heading","level":5,"content":"JavaScript SDK"}
    - {"type":"list","listType":"ul","items":["[Quickstart](https://docs.tavily.com/sdk/javascript/quick-start)","[SDK Reference](https://docs.tavily.com/sdk/javascript/reference)"]}
    - {"type":"heading","level":5,"content":"Best Practices"}
    - {"type":"list","listType":"ul","items":["[Search](https://docs.tavily.com/documentation/best-practices/best-practices-search)","[Extract](https://docs.tavily.com/documentation/best-practices/best-practices-extract)","[Crawl](https://docs.tavily.com/documentation/best-practices/best-practices-crawl)","[Research](https://docs.tavily.com/documentation/best-practices/best-practices-research)","[API Key Management](https://docs.tavily.com/documentation/best-practices/api-key-management)"]}
    - {"type":"codeblock","language":"","content":"curl --request POST \\\n  --url https://api-key-generator.tavily.com/deactivate-keys \\\n  --header 'Authorization: Bearer <token>' \\\n  --header 'Content-Type: application/json' \\\n  --data '\n{\n  \"request_id\": \"550e5678-e29b-41d4-a716-446655441234\"\n}\n'"}
    - {"type":"codeblock","language":"","content":"{\n  \"message\": \"Successfully deactivated 5 key(s)\"\n}"}
    - {"type":"codeblock","language":"","content":"curl --request POST \\\n  --url https://api-key-generator.tavily.com/deactivate-keys \\\n  --header 'Authorization: Bearer <token>' \\\n  --header 'Content-Type: application/json' \\\n  --data '\n{\n  \"request_id\": \"550e5678-e29b-41d4-a716-446655441234\"\n}\n'"}
    - {"type":"codeblock","language":"","content":"{\n  \"message\": \"Successfully deactivated 5 key(s)\"\n}"}
    - {"type":"heading","level":4,"content":"Authorizations"}
    - {"type":"paragraph","content":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY)."}
    - {"type":"heading","level":4,"content":"Body"}
    - {"type":"paragraph","content":"Optionally provide a `request_id` to bulk-deactivate keys. If omitted, the key in the Authorization header is deactivated."}
    - {"type":"paragraph","content":"The request ID from a previous `/generate-keys` call. All keys from that request will be deactivated."}
    - {"type":"paragraph","content":"`\"550e5678-e29b-41d4-a716-446655441234\"`"}
    - {"type":"heading","level":4,"content":"Response"}
    - {"type":"paragraph","content":"Keys deactivated successfully."}
    - {"type":"paragraph","content":"A confirmation message."}
    - {"type":"paragraph","content":"`\"Successfully deactivated 5 key(s)\"`"}
    - {"type":"image","src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","alt":"tavily-logo","title":"","index":1,"localPath":"Deactivate_Keys_-_Tavily_Docs/image_1.png"}
    - {"type":"heading","level":2,"content":"Privacy Preference Center"}
    - {"type":"heading","level":3,"content":"Manage Consent Preferences"}
    - {"type":"heading","level":4,"content":"Strictly Necessary Cookies"}
    - {"type":"paragraph","content":"These cookies are necessary for the website to function and cannot be switched off in our systems. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, logging in or filling in forms. You can set your browser to block or alert you about these cookies, but some parts of the site will not then work. These cookies do not store any personally identifiable information."}
    - {"type":"heading","level":4,"content":"Functional Cookies"}
    - {"type":"paragraph","content":"These cookies enable the website to provide enhanced functionality and personalisation. They may be set by us or by third party providers whose services we have added to our pages. If you do not allow these cookies then some or all of these services may not function properly."}
    - {"type":"heading","level":4,"content":"Performance Cookies"}
    - {"type":"paragraph","content":"These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our site. They help us to know which pages are the most and least popular and see how visitors move around the site. All information these cookies collect is aggregated and therefore anonymous. If you do not allow these cookies we will not know when you have visited our site, and will not be able to monitor its performance."}
    - {"type":"heading","level":4,"content":"Targeting Cookies"}
    - {"type":"paragraph","content":"These cookies may be set through our site by our advertising partners. They may be used by those companies to build a profile of your interests and show you relevant adverts on other sites. They do not store directly personal information, but are based on uniquely identifying your browser and internet device. If you do not allow these cookies, you will experience less targeted advertising."}
    - {"type":"heading","level":3,"content":"Cookie List"}
    - {"type":"list","listType":"ul","items":["checkbox label label"]}
  paragraphs:
    - "cURL"
    - "Deactivate API keys either in bulk by `request_id` or individually."
    - "**Option A — Deactivate by request ID:** Pass a `request_id` in the request body to deactivate all keys from that generation request."
    - "**Option B — Deactivate individual key:** Set the key you want to deactivate in the `Authorization` header. No request body is required."
    - "cURL"
    - "Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY)."
    - "Optionally provide a `request_id` to bulk-deactivate keys. If omitted, the key in the Authorization header is deactivated."
    - "The request ID from a previous `/generate-keys` call. All keys from that request will be deactivated."
    - "`\"550e5678-e29b-41d4-a716-446655441234\"`"
    - "Keys deactivated successfully."
    - "A confirmation message."
    - "`\"Successfully deactivated 5 key(s)\"`"
    - "Resources"
    - "Legal"
    - "These cookies are necessary for the website to function and cannot be switched off in our systems. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, logging in or filling in forms. You can set your browser to block or alert you about these cookies, but some parts of the site will not then work. These cookies do not store any personally identifiable information."
    - "These cookies enable the website to provide enhanced functionality and personalisation. They may be set by us or by third party providers whose services we have added to our pages. If you do not allow these cookies then some or all of these services may not function properly."
    - "These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our site. They help us to know which pages are the most and least popular and see how visitors move around the site. All information these cookies collect is aggregated and therefore anonymous. If you do not allow these cookies we will not know when you have visited our site, and will not be able to monitor its performance."
    - "These cookies may be set through our site by our advertising partners. They may be used by those companies to build a profile of your interests and show you relevant adverts on other sites. They do not store directly personal information, but are based on uniquely identifying your browser and internet device. If you do not allow these cookies, you will experience less targeted advertising."
  lists:
    - {"type":"ul","items":["[Support](mailto:support@tavily.com)","[Get an API key](https://app.tavily.com/)","[Get an API key](https://app.tavily.com/)"]}
    - {"type":"ul","items":["[API Playground](https://app.tavily.com/playground)","[Community](https://discord.gg/TPu2gkaWp2)","[Blog](https://tavily.com/blog)"]}
    - {"type":"ul","items":["[Introduction](https://docs.tavily.com/documentation/api-reference/introduction)","[POSTSearch](https://docs.tavily.com/documentation/api-reference/endpoint/search)","[POSTExtract](https://docs.tavily.com/documentation/api-reference/endpoint/extract)","[POSTCrawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl)","[POSTMap](https://docs.tavily.com/documentation/api-reference/endpoint/map)","Research[POSTCreate Research Task](https://docs.tavily.com/documentation/api-reference/endpoint/research)[GETGet Research Task Status](https://docs.tavily.com/documentation/api-reference/endpoint/research-get)[Streaming](https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming)","[POSTCreate Research Task](https://docs.tavily.com/documentation/api-reference/endpoint/research)","[GETGet Research Task Status](https://docs.tavily.com/documentation/api-reference/endpoint/research-get)","[Streaming](https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming)","[GETUsage](https://docs.tavily.com/documentation/api-reference/endpoint/usage)"]}
    - {"type":"ul","items":["[POSTCreate Research Task](https://docs.tavily.com/documentation/api-reference/endpoint/research)","[GETGet Research Task Status](https://docs.tavily.com/documentation/api-reference/endpoint/research-get)","[Streaming](https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming)"]}
    - {"type":"ul","items":["API Key Generator[POSTGenerate Keys](https://docs.tavily.com/documentation/enterprise/generate-keys)[POSTDeactivate Keys](https://docs.tavily.com/documentation/enterprise/deactivate-keys)[GETKey Info](https://docs.tavily.com/documentation/enterprise/key-info)","[POSTGenerate Keys](https://docs.tavily.com/documentation/enterprise/generate-keys)","[POSTDeactivate Keys](https://docs.tavily.com/documentation/enterprise/deactivate-keys)","[GETKey Info](https://docs.tavily.com/documentation/enterprise/key-info)"]}
    - {"type":"ul","items":["[POSTGenerate Keys](https://docs.tavily.com/documentation/enterprise/generate-keys)","[POSTDeactivate Keys](https://docs.tavily.com/documentation/enterprise/deactivate-keys)","[GETKey Info](https://docs.tavily.com/documentation/enterprise/key-info)"]}
    - {"type":"ul","items":["[Quickstart](https://docs.tavily.com/sdk/python/quick-start)","[SDK Reference](https://docs.tavily.com/sdk/python/reference)"]}
    - {"type":"ul","items":["[Quickstart](https://docs.tavily.com/sdk/javascript/quick-start)","[SDK Reference](https://docs.tavily.com/sdk/javascript/reference)"]}
    - {"type":"ul","items":["[Search](https://docs.tavily.com/documentation/best-practices/best-practices-search)","[Extract](https://docs.tavily.com/documentation/best-practices/best-practices-extract)","[Crawl](https://docs.tavily.com/documentation/best-practices/best-practices-crawl)","[Research](https://docs.tavily.com/documentation/best-practices/best-practices-research)","[API Key Management](https://docs.tavily.com/documentation/best-practices/api-key-management)"]}
    - {"type":"ul","items":["checkbox label label"]}
  tables: []
  codeBlocks:
    - {"language":"text","code":"curl --request POST \\\n  --url https://api-key-generator.tavily.com/deactivate-keys \\\n  --header 'Authorization: Bearer <token>' \\\n  --header 'Content-Type: application/json' \\\n  --data '\n{\n  \"request_id\": \"550e5678-e29b-41d4-a716-446655441234\"\n}\n'"}
    - {"language":"text","code":"curl --request POST \\\n  --url https://api-key-generator.tavily.com/deactivate-keys \\\n  --header 'Authorization: Bearer <token>' \\\n  --header 'Content-Type: application/json' \\\n  --data '\n{\n  \"request_id\": \"550e5678-e29b-41d4-a716-446655441234\"\n}\n'"}
    - {"language":"json","code":"{\n  \"message\": \"Successfully deactivated 5 key(s)\"\n}"}
    - {"language":"json","code":"{\n  \"message\": \"Successfully deactivated 5 key(s)\"\n}"}
    - {"language":"text","code":"curl --request POST \\\n  --url https://api-key-generator.tavily.com/deactivate-keys \\\n  --header 'Authorization: Bearer <token>' \\\n  --header 'Content-Type: application/json' \\\n  --data '\n{\n  \"request_id\": \"550e5678-e29b-41d4-a716-446655441234\"\n}\n'"}
    - {"language":"text","code":"curl --request POST \\\n  --url https://api-key-generator.tavily.com/deactivate-keys \\\n  --header 'Authorization: Bearer <token>' \\\n  --header 'Content-Type: application/json' \\\n  --data '\n{\n  \"request_id\": \"550e5678-e29b-41d4-a716-446655441234\"\n}\n'"}
    - {"language":"json","code":"{\n  \"message\": \"Successfully deactivated 5 key(s)\"\n}"}
    - {"language":"json","code":"{\n  \"message\": \"Successfully deactivated 5 key(s)\"\n}"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Deactivate_Keys_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Deactivate_Keys_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Deactivate_Keys_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Deactivate_Keys_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Deactivate_Keys_-_Tavily_Docs/image_5.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Deactivate_Keys_-_Tavily_Docs/image_6.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":18,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":19,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_19.png","width":16,"height":16}
    - {"type":"svg","index":20,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_20.png","width":16,"height":16}
    - {"type":"svg","index":21,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_21.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_22.png","width":16,"height":16}
    - {"type":"svg","index":23,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_23.png","width":16,"height":16}
    - {"type":"svg","index":24,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_24.png","width":16,"height":16}
    - {"type":"svg","index":25,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_26.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_27.png","width":14,"height":14}
    - {"type":"svg","index":28,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_28.png","width":14,"height":14}
    - {"type":"svg","index":29,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_29.png","width":16,"height":16}
    - {"type":"svg","index":30,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_30.png","width":16,"height":16}
    - {"type":"svg","index":31,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_31.png","width":16,"height":16}
    - {"type":"svg","index":40,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_40.png","width":16,"height":16}
    - {"type":"svg","index":41,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_41.png","width":18,"height":18}
    - {"type":"svg","index":42,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_42.png","width":18,"height":18}
    - {"type":"svg","index":43,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_43.png","width":18,"height":18}
    - {"type":"svg","index":44,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_44.png","width":14,"height":14}
    - {"type":"svg","index":45,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_45.png","width":14,"height":14}
    - {"type":"svg","index":46,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_46.png","width":14,"height":14}
    - {"type":"svg","index":51,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_51.png","width":20,"height":20}
    - {"type":"svg","index":52,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_52.png","width":20,"height":20}
    - {"type":"svg","index":53,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_53.png","width":20,"height":20}
    - {"type":"svg","index":54,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_54.png","width":20,"height":20}
    - {"type":"svg","index":55,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_55.png","width":49,"height":14}
    - {"type":"svg","index":56,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_56.png","width":16,"height":16}
    - {"type":"svg","index":57,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_57.png","width":16,"height":16}
    - {"type":"svg","index":58,"filename":"Deactivate_Keys_-_Tavily_Docs/svg_58.png","width":16,"height":16}
  chartData: []
  blockquotes: []
  definitionLists: []
  horizontalRules: 0
  videos: []
  audios: []
  apiData: 0
  pageFeatures:
    suggestedType: "api-doc"
    confidence: 75
    signals:
      - "article-like"
      - "api-doc-like"
      - "api-endpoints"
  tabsAndDropdowns: []
  dateFilters: []
---

# Deactivate Keys

## 源URL

https://docs.tavily.com/documentation/enterprise/deactivate-keys

## 描述

Deactivate API keys either in bulk by request_id or individually. Option A — Deactivate by request ID: Pass a request_id in the request body to deactivate all keys from that generation request. Option B — Deactivate individual key: Set the key you want to deactivate in the Authorization header. No request body is required.

## 内容

- [API Playground](https://app.tavily.com/playground)
- [Community](https://discord.gg/TPu2gkaWp2)
- [Blog](https://tavily.com/blog)

###### API Reference

- [Introduction](https://docs.tavily.com/documentation/api-reference/introduction)
- [POSTSearch](https://docs.tavily.com/documentation/api-reference/endpoint/search)
- [POSTExtract](https://docs.tavily.com/documentation/api-reference/endpoint/extract)
- [POSTCrawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl)
- [POSTMap](https://docs.tavily.com/documentation/api-reference/endpoint/map)
- Research[POSTCreate Research Task](https://docs.tavily.com/documentation/api-reference/endpoint/research)[GETGet Research Task Status](https://docs.tavily.com/documentation/api-reference/endpoint/research-get)[Streaming](https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming)
- [POSTCreate Research Task](https://docs.tavily.com/documentation/api-reference/endpoint/research)
- [GETGet Research Task Status](https://docs.tavily.com/documentation/api-reference/endpoint/research-get)
- [Streaming](https://docs.tavily.com/documentation/api-reference/endpoint/research-streaming)
- [GETUsage](https://docs.tavily.com/documentation/api-reference/endpoint/usage)

###### Enterprise API Reference

- API Key Generator[POSTGenerate Keys](https://docs.tavily.com/documentation/enterprise/generate-keys)[POSTDeactivate Keys](https://docs.tavily.com/documentation/enterprise/deactivate-keys)[GETKey Info](https://docs.tavily.com/documentation/enterprise/key-info)
- [POSTGenerate Keys](https://docs.tavily.com/documentation/enterprise/generate-keys)
- [POSTDeactivate Keys](https://docs.tavily.com/documentation/enterprise/deactivate-keys)
- [GETKey Info](https://docs.tavily.com/documentation/enterprise/key-info)

###### Python SDK

- [Quickstart](https://docs.tavily.com/sdk/python/quick-start)
- [SDK Reference](https://docs.tavily.com/sdk/python/reference)

###### JavaScript SDK

- [Quickstart](https://docs.tavily.com/sdk/javascript/quick-start)
- [SDK Reference](https://docs.tavily.com/sdk/javascript/reference)

###### Best Practices

- [Search](https://docs.tavily.com/documentation/best-practices/best-practices-search)
- [Extract](https://docs.tavily.com/documentation/best-practices/best-practices-extract)
- [Crawl](https://docs.tavily.com/documentation/best-practices/best-practices-crawl)
- [Research](https://docs.tavily.com/documentation/best-practices/best-practices-research)
- [API Key Management](https://docs.tavily.com/documentation/best-practices/api-key-management)

```text
curl --request POST \
  --url https://api-key-generator.tavily.com/deactivate-keys \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "request_id": "550e5678-e29b-41d4-a716-446655441234"
}
'
```

```text
{
  "message": "Successfully deactivated 5 key(s)"
}
```

```text
curl --request POST \
  --url https://api-key-generator.tavily.com/deactivate-keys \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "request_id": "550e5678-e29b-41d4-a716-446655441234"
}
'
```

```text
{
  "message": "Successfully deactivated 5 key(s)"
}
```

##### Authorizations

Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).

##### Body

Optionally provide a `request_id` to bulk-deactivate keys. If omitted, the key in the Authorization header is deactivated.

The request ID from a previous `/generate-keys` call. All keys from that request will be deactivated.

`"550e5678-e29b-41d4-a716-446655441234"`

##### Response

Keys deactivated successfully.

A confirmation message.

`"Successfully deactivated 5 key(s)"`

![tavily-logo](Deactivate_Keys_-_Tavily_Docs/image_1.png)

### Privacy Preference Center

#### Manage Consent Preferences

##### Strictly Necessary Cookies

These cookies are necessary for the website to function and cannot be switched off in our systems. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, logging in or filling in forms. You can set your browser to block or alert you about these cookies, but some parts of the site will not then work. These cookies do not store any personally identifiable information.

##### Functional Cookies

These cookies enable the website to provide enhanced functionality and personalisation. They may be set by us or by third party providers whose services we have added to our pages. If you do not allow these cookies then some or all of these services may not function properly.

##### Performance Cookies

These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our site. They help us to know which pages are the most and least popular and see how visitors move around the site. All information these cookies collect is aggregated and therefore anonymous. If you do not allow these cookies we will not know when you have visited our site, and will not be able to monitor its performance.

##### Targeting Cookies

These cookies may be set through our site by our advertising partners. They may be used by those companies to build a profile of your interests and show you relevant adverts on other sites. They do not store directly personal information, but are based on uniquely identifying your browser and internet device. If you do not allow these cookies, you will experience less targeted advertising.

#### Cookie List

- checkbox label label

## 图片

![light logo](Deactivate_Keys_-_Tavily_Docs/image_1.svg)

![dark logo](Deactivate_Keys_-_Tavily_Docs/image_2.svg)

![light logo](Deactivate_Keys_-_Tavily_Docs/image_3.svg)

![dark logo](Deactivate_Keys_-_Tavily_Docs/image_4.svg)

![tavily-logo](Deactivate_Keys_-_Tavily_Docs/image_5.png)

![Powered by Onetrust](Deactivate_Keys_-_Tavily_Docs/image_6.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Deactivate_Keys_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Deactivate_Keys_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Deactivate_Keys_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Deactivate_Keys_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Deactivate_Keys_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Deactivate_Keys_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Deactivate_Keys_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 16](Deactivate_Keys_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 18](Deactivate_Keys_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 19](Deactivate_Keys_-_Tavily_Docs/svg_19.png)
*尺寸: 16x16px*

![SVG图表 20](Deactivate_Keys_-_Tavily_Docs/svg_20.png)
*尺寸: 16x16px*

![SVG图表 21](Deactivate_Keys_-_Tavily_Docs/svg_21.png)
*尺寸: 16x16px*

![SVG图表 22](Deactivate_Keys_-_Tavily_Docs/svg_22.png)
*尺寸: 16x16px*

![SVG图表 23](Deactivate_Keys_-_Tavily_Docs/svg_23.png)
*尺寸: 16x16px*

![SVG图表 24](Deactivate_Keys_-_Tavily_Docs/svg_24.png)
*尺寸: 16x16px*

![SVG图表 25](Deactivate_Keys_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](Deactivate_Keys_-_Tavily_Docs/svg_26.png)
*尺寸: 16x16px*

![SVG图表 27](Deactivate_Keys_-_Tavily_Docs/svg_27.png)
*尺寸: 14x14px*

![SVG图表 28](Deactivate_Keys_-_Tavily_Docs/svg_28.png)
*尺寸: 14x14px*

![SVG图表 29](Deactivate_Keys_-_Tavily_Docs/svg_29.png)
*尺寸: 16x16px*

![SVG图表 30](Deactivate_Keys_-_Tavily_Docs/svg_30.png)
*尺寸: 16x16px*

![SVG图表 31](Deactivate_Keys_-_Tavily_Docs/svg_31.png)
*尺寸: 16x16px*

![SVG图表 40](Deactivate_Keys_-_Tavily_Docs/svg_40.png)
*尺寸: 16x16px*

![SVG图表 41](Deactivate_Keys_-_Tavily_Docs/svg_41.png)
*尺寸: 18x18px*

![SVG图表 42](Deactivate_Keys_-_Tavily_Docs/svg_42.png)
*尺寸: 18x18px*

![SVG图表 43](Deactivate_Keys_-_Tavily_Docs/svg_43.png)
*尺寸: 18x18px*

![SVG图表 44](Deactivate_Keys_-_Tavily_Docs/svg_44.png)
*尺寸: 14x14px*

![SVG图表 45](Deactivate_Keys_-_Tavily_Docs/svg_45.png)
*尺寸: 14x14px*

![SVG图表 46](Deactivate_Keys_-_Tavily_Docs/svg_46.png)
*尺寸: 14x14px*

![SVG图表 51](Deactivate_Keys_-_Tavily_Docs/svg_51.png)
*尺寸: 20x20px*

![SVG图表 52](Deactivate_Keys_-_Tavily_Docs/svg_52.png)
*尺寸: 20x20px*

![SVG图表 53](Deactivate_Keys_-_Tavily_Docs/svg_53.png)
*尺寸: 20x20px*

![SVG图表 54](Deactivate_Keys_-_Tavily_Docs/svg_54.png)
*尺寸: 20x20px*

![SVG图表 55](Deactivate_Keys_-_Tavily_Docs/svg_55.png)
*尺寸: 49x14px*

![SVG图表 56](Deactivate_Keys_-_Tavily_Docs/svg_56.png)
*尺寸: 16x16px*

![SVG图表 57](Deactivate_Keys_-_Tavily_Docs/svg_57.png)
*尺寸: 16x16px*

![SVG图表 58](Deactivate_Keys_-_Tavily_Docs/svg_58.png)
*尺寸: 16x16px*
