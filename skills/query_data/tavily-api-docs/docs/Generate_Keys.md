---
id: "url-eeda8de"
type: "website"
title: "Generate Keys"
url: "https://docs.tavily.com/documentation/enterprise/generate-keys"
description: "Generate one or more API keys with custom configuration."
source: ""
tags: []
crawl_time: "2026-03-18T07:11:46.139Z"
metadata:
  subtype: "api-doc"
  headings:
    - {"level":5,"text":"API Reference"}
    - {"level":5,"text":"Enterprise API Reference"}
    - {"level":5,"text":"Python SDK"}
    - {"level":5,"text":"JavaScript SDK"}
    - {"level":5,"text":"Best Practices"}
    - {"level":1,"text":"Generate Keys"}
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
    - {"type":"codeblock","language":"","content":"curl --request POST \\\n  --url https://api-key-generator.tavily.com/generate-keys \\\n  --header 'Authorization: Bearer <token>' \\\n  --header 'Content-Type: application/json' \\\n  --data '\n{\n  \"permission_level\": \"user\",\n  \"name\": \"projectA\",\n  \"scope\": [\n    \"api:generate_keys\"\n  ],\n  \"key_type\": \"development\",\n  \"key_limit\": 200,\n  \"ttl_hours\": 10,\n  \"count\": 2\n}\n'"}
    - {"type":"codeblock","language":"","content":"{\n  \"keys\": [\n    \"tvly-dev-MI9p6...\",\n    \"tvly-dev-f7Wrr...\"\n  ],\n  \"expires_at\": \"2026-02-25T01:14:45Z\",\n  \"created\": \"2026-02-24T15:14:45\",\n  \"message\": \"2 keys generated successfully with 200 credits each. These keys will be automatically deactivated after 10 hours\",\n  \"request_id\": \"949297ca-d123-4267-8041-45398a0b847d\"\n}"}
    - {"type":"codeblock","language":"","content":"curl --request POST \\\n  --url https://api-key-generator.tavily.com/generate-keys \\\n  --header 'Authorization: Bearer <token>' \\\n  --header 'Content-Type: application/json' \\\n  --data '\n{\n  \"permission_level\": \"user\",\n  \"name\": \"projectA\",\n  \"scope\": [\n    \"api:generate_keys\"\n  ],\n  \"key_type\": \"development\",\n  \"key_limit\": 200,\n  \"ttl_hours\": 10,\n  \"count\": 2\n}\n'"}
    - {"type":"codeblock","language":"","content":"{\n  \"keys\": [\n    \"tvly-dev-MI9p6...\",\n    \"tvly-dev-f7Wrr...\"\n  ],\n  \"expires_at\": \"2026-02-25T01:14:45Z\",\n  \"created\": \"2026-02-24T15:14:45\",\n  \"message\": \"2 keys generated successfully with 200 credits each. These keys will be automatically deactivated after 10 hours\",\n  \"request_id\": \"949297ca-d123-4267-8041-45398a0b847d\"\n}"}
    - {"type":"heading","level":4,"content":"Authorizations"}
    - {"type":"paragraph","content":"Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY)."}
    - {"type":"heading","level":4,"content":"Body"}
    - {"type":"paragraph","content":"Parameters for generating API keys."}
    - {"type":"paragraph","content":"The permission level for the key."}
    - {"type":"paragraph","content":"The name of the key(s). Auto-generated in the format `{key_type}-{expiration}-#{index}`"}
    - {"type":"paragraph","content":"Permission scopes for the key. Only applicable when `permission_level` is `\"user\"`."}
    - {"type":"paragraph","content":"The type of key."}
    - {"type":"paragraph","content":"The number of credits for the generated keys."}
    - {"type":"paragraph","content":"Number of hours before the keys become deactivated."}
    - {"type":"paragraph","content":"The total number of keys to generate."}
    - {"type":"heading","level":4,"content":"Response"}
    - {"type":"paragraph","content":"Keys generated successfully."}
    - {"type":"paragraph","content":"The generated API keys."}
    - {"type":"codeblock","language":"","content":"[\"tvly-dev-MI9p6...\", \"tvly-dev-f7Wrr...\"]"}
    - {"type":"paragraph","content":"The expiration timestamp for the keys."}
    - {"type":"paragraph","content":"`\"2026-02-25T01:14:45Z\"`"}
    - {"type":"paragraph","content":"The creation timestamp."}
    - {"type":"paragraph","content":"`\"2026-02-24T15:14:45\"`"}
    - {"type":"paragraph","content":"A summary message about the generated keys."}
    - {"type":"paragraph","content":"`\"2 keys generated successfully with 200 credits each. These keys will be automatically deactivated after 10 hours\"`"}
    - {"type":"paragraph","content":"Unique identifier for this generation request. Use this to bulk-deactivate the keys later."}
    - {"type":"paragraph","content":"`\"949297ca-d123-4267-8041-45398a0b847d\"`"}
    - {"type":"image","src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","alt":"tavily-logo","title":"","index":1,"localPath":"Generate_Keys_-_Tavily_Docs/image_1.png"}
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
    - "Generate one or more API keys with custom configuration."
    - "cURL"
    - "Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY)."
    - "Parameters for generating API keys."
    - "The permission level for the key."
    - "The name of the key(s). Auto-generated in the format `{key_type}-{expiration}-#{index}`"
    - "Permission scopes for the key. Only applicable when `permission_level` is `\"user\"`."
    - "The type of key."
    - "The number of credits for the generated keys."
    - "Number of hours before the keys become deactivated."
    - "The total number of keys to generate."
    - "Keys generated successfully."
    - "The generated API keys."
    - "The expiration timestamp for the keys."
    - "`\"2026-02-25T01:14:45Z\"`"
    - "The creation timestamp."
    - "`\"2026-02-24T15:14:45\"`"
    - "A summary message about the generated keys."
    - "`\"2 keys generated successfully with 200 credits each. These keys will be automatically deactivated after 10 hours\"`"
    - "Unique identifier for this generation request. Use this to bulk-deactivate the keys later."
    - "`\"949297ca-d123-4267-8041-45398a0b847d\"`"
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
    - {"language":"text","code":"curl --request POST \\\n  --url https://api-key-generator.tavily.com/generate-keys \\\n  --header 'Authorization: Bearer <token>' \\\n  --header 'Content-Type: application/json' \\\n  --data '\n{\n  \"permission_level\": \"user\",\n  \"name\": \"projectA\",\n  \"scope\": [\n    \"api:generate_keys\"\n  ],\n  \"key_type\": \"development\",\n  \"key_limit\": 200,\n  \"ttl_hours\": 10,\n  \"count\": 2\n}\n'"}
    - {"language":"text","code":"curl --request POST \\\n  --url https://api-key-generator.tavily.com/generate-keys \\\n  --header 'Authorization: Bearer <token>' \\\n  --header 'Content-Type: application/json' \\\n  --data '\n{\n  \"permission_level\": \"user\",\n  \"name\": \"projectA\",\n  \"scope\": [\n    \"api:generate_keys\"\n  ],\n  \"key_type\": \"development\",\n  \"key_limit\": 200,\n  \"ttl_hours\": 10,\n  \"count\": 2\n}\n'"}
    - {"language":"json","code":"{\n  \"keys\": [\n    \"tvly-dev-MI9p6...\",\n    \"tvly-dev-f7Wrr...\"\n  ],\n  \"expires_at\": \"2026-02-25T01:14:45Z\",\n  \"created\": \"2026-02-24T15:14:45\",\n  \"message\": \"2 keys generated successfully with 200 credits each. These keys will be automatically deactivated after 10 hours\",\n  \"request_id\": \"949297ca-d123-4267-8041-45398a0b847d\"\n}"}
    - {"language":"json","code":"{\n  \"keys\": [\n    \"tvly-dev-MI9p6...\",\n    \"tvly-dev-f7Wrr...\"\n  ],\n  \"expires_at\": \"2026-02-25T01:14:45Z\",\n  \"created\": \"2026-02-24T15:14:45\",\n  \"message\": \"2 keys generated successfully with 200 credits each. These keys will be automatically deactivated after 10 hours\",\n  \"request_id\": \"949297ca-d123-4267-8041-45398a0b847d\"\n}"}
    - {"language":"text","code":"curl --request POST \\\n  --url https://api-key-generator.tavily.com/generate-keys \\\n  --header 'Authorization: Bearer <token>' \\\n  --header 'Content-Type: application/json' \\\n  --data '\n{\n  \"permission_level\": \"user\",\n  \"name\": \"projectA\",\n  \"scope\": [\n    \"api:generate_keys\"\n  ],\n  \"key_type\": \"development\",\n  \"key_limit\": 200,\n  \"ttl_hours\": 10,\n  \"count\": 2\n}\n'"}
    - {"language":"text","code":"curl --request POST \\\n  --url https://api-key-generator.tavily.com/generate-keys \\\n  --header 'Authorization: Bearer <token>' \\\n  --header 'Content-Type: application/json' \\\n  --data '\n{\n  \"permission_level\": \"user\",\n  \"name\": \"projectA\",\n  \"scope\": [\n    \"api:generate_keys\"\n  ],\n  \"key_type\": \"development\",\n  \"key_limit\": 200,\n  \"ttl_hours\": 10,\n  \"count\": 2\n}\n'"}
    - {"language":"json","code":"{\n  \"keys\": [\n    \"tvly-dev-MI9p6...\",\n    \"tvly-dev-f7Wrr...\"\n  ],\n  \"expires_at\": \"2026-02-25T01:14:45Z\",\n  \"created\": \"2026-02-24T15:14:45\",\n  \"message\": \"2 keys generated successfully with 200 credits each. These keys will be automatically deactivated after 10 hours\",\n  \"request_id\": \"949297ca-d123-4267-8041-45398a0b847d\"\n}"}
    - {"language":"json","code":"{\n  \"keys\": [\n    \"tvly-dev-MI9p6...\",\n    \"tvly-dev-f7Wrr...\"\n  ],\n  \"expires_at\": \"2026-02-25T01:14:45Z\",\n  \"created\": \"2026-02-24T15:14:45\",\n  \"message\": \"2 keys generated successfully with 200 credits each. These keys will be automatically deactivated after 10 hours\",\n  \"request_id\": \"949297ca-d123-4267-8041-45398a0b847d\"\n}"}
    - {"language":"json","code":"[\"tvly-dev-MI9p6...\", \"tvly-dev-f7Wrr...\"]"}
    - {"language":"json","code":"[\"tvly-dev-MI9p6...\", \"tvly-dev-f7Wrr...\"]"}
  images:
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Generate_Keys_-_Tavily_Docs/image_1.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Generate_Keys_-_Tavily_Docs/image_2.svg","alt":"dark logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/light.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=c5c878011f13d458af0997f3a540eb4f","localPath":"Generate_Keys_-_Tavily_Docs/image_3.svg","alt":"light logo","title":""}
    - {"src":"https://mintcdn.com/tavilyai/HY1Rnt85q4usR4-R/logo/dark.svg?fit=max&auto=format&n=HY1Rnt85q4usR4-R&q=85&s=1521677768a1f26b34a9ad86d04c62cc","localPath":"Generate_Keys_-_Tavily_Docs/image_4.svg","alt":"dark logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/f511015a-a7df-4ef8-b5f1-b3097a2e8b5a/019a509d-3ef2-7496-b855-4b8618e86334/5e89a087-01b9-4763-bbc6-6f7a4b155b65/Dark_Tavily_Logo.png","localPath":"Generate_Keys_-_Tavily_Docs/image_5.png","alt":"tavily-logo","title":""}
    - {"src":"https://cdn.cookielaw.org/logos/static/powered_by_logo.svg","localPath":"Generate_Keys_-_Tavily_Docs/image_6.svg","alt":"Powered by Onetrust","title":"Powered by OneTrust Opens in a new Tab"}
  charts:
    - {"type":"svg","index":1,"filename":"Generate_Keys_-_Tavily_Docs/svg_1.png","width":16,"height":16}
    - {"type":"svg","index":2,"filename":"Generate_Keys_-_Tavily_Docs/svg_2.png","width":16,"height":16}
    - {"type":"svg","index":4,"filename":"Generate_Keys_-_Tavily_Docs/svg_4.png","width":14,"height":16}
    - {"type":"svg","index":11,"filename":"Generate_Keys_-_Tavily_Docs/svg_11.png","width":16,"height":16}
    - {"type":"svg","index":12,"filename":"Generate_Keys_-_Tavily_Docs/svg_12.png","width":16,"height":16}
    - {"type":"svg","index":13,"filename":"Generate_Keys_-_Tavily_Docs/svg_13.png","width":16,"height":16}
    - {"type":"svg","index":14,"filename":"Generate_Keys_-_Tavily_Docs/svg_14.png","width":16,"height":16}
    - {"type":"svg","index":16,"filename":"Generate_Keys_-_Tavily_Docs/svg_16.png","width":16,"height":16}
    - {"type":"svg","index":18,"filename":"Generate_Keys_-_Tavily_Docs/svg_18.png","width":16,"height":16}
    - {"type":"svg","index":19,"filename":"Generate_Keys_-_Tavily_Docs/svg_19.png","width":16,"height":16}
    - {"type":"svg","index":20,"filename":"Generate_Keys_-_Tavily_Docs/svg_20.png","width":16,"height":16}
    - {"type":"svg","index":21,"filename":"Generate_Keys_-_Tavily_Docs/svg_21.png","width":16,"height":16}
    - {"type":"svg","index":22,"filename":"Generate_Keys_-_Tavily_Docs/svg_22.png","width":16,"height":16}
    - {"type":"svg","index":23,"filename":"Generate_Keys_-_Tavily_Docs/svg_23.png","width":16,"height":16}
    - {"type":"svg","index":24,"filename":"Generate_Keys_-_Tavily_Docs/svg_24.png","width":16,"height":16}
    - {"type":"svg","index":25,"filename":"Generate_Keys_-_Tavily_Docs/svg_25.png","width":16,"height":16}
    - {"type":"svg","index":26,"filename":"Generate_Keys_-_Tavily_Docs/svg_26.png","width":16,"height":16}
    - {"type":"svg","index":27,"filename":"Generate_Keys_-_Tavily_Docs/svg_27.png","width":14,"height":14}
    - {"type":"svg","index":28,"filename":"Generate_Keys_-_Tavily_Docs/svg_28.png","width":14,"height":14}
    - {"type":"svg","index":29,"filename":"Generate_Keys_-_Tavily_Docs/svg_29.png","width":16,"height":16}
    - {"type":"svg","index":30,"filename":"Generate_Keys_-_Tavily_Docs/svg_30.png","width":16,"height":16}
    - {"type":"svg","index":31,"filename":"Generate_Keys_-_Tavily_Docs/svg_31.png","width":16,"height":16}
    - {"type":"svg","index":40,"filename":"Generate_Keys_-_Tavily_Docs/svg_40.png","width":16,"height":16}
    - {"type":"svg","index":41,"filename":"Generate_Keys_-_Tavily_Docs/svg_41.png","width":18,"height":18}
    - {"type":"svg","index":42,"filename":"Generate_Keys_-_Tavily_Docs/svg_42.png","width":18,"height":18}
    - {"type":"svg","index":43,"filename":"Generate_Keys_-_Tavily_Docs/svg_43.png","width":18,"height":18}
    - {"type":"svg","index":44,"filename":"Generate_Keys_-_Tavily_Docs/svg_44.png","width":18,"height":18}
    - {"type":"svg","index":45,"filename":"Generate_Keys_-_Tavily_Docs/svg_45.png","width":18,"height":18}
    - {"type":"svg","index":46,"filename":"Generate_Keys_-_Tavily_Docs/svg_46.png","width":18,"height":18}
    - {"type":"svg","index":47,"filename":"Generate_Keys_-_Tavily_Docs/svg_47.png","width":18,"height":18}
    - {"type":"svg","index":48,"filename":"Generate_Keys_-_Tavily_Docs/svg_48.png","width":18,"height":18}
    - {"type":"svg","index":49,"filename":"Generate_Keys_-_Tavily_Docs/svg_49.png","width":18,"height":18}
    - {"type":"svg","index":50,"filename":"Generate_Keys_-_Tavily_Docs/svg_50.png","width":18,"height":18}
    - {"type":"svg","index":51,"filename":"Generate_Keys_-_Tavily_Docs/svg_51.png","width":18,"height":18}
    - {"type":"svg","index":52,"filename":"Generate_Keys_-_Tavily_Docs/svg_52.png","width":18,"height":18}
    - {"type":"svg","index":53,"filename":"Generate_Keys_-_Tavily_Docs/svg_53.png","width":18,"height":18}
    - {"type":"svg","index":54,"filename":"Generate_Keys_-_Tavily_Docs/svg_54.png","width":14,"height":14}
    - {"type":"svg","index":55,"filename":"Generate_Keys_-_Tavily_Docs/svg_55.png","width":14,"height":14}
    - {"type":"svg","index":56,"filename":"Generate_Keys_-_Tavily_Docs/svg_56.png","width":14,"height":14}
    - {"type":"svg","index":61,"filename":"Generate_Keys_-_Tavily_Docs/svg_61.png","width":20,"height":20}
    - {"type":"svg","index":62,"filename":"Generate_Keys_-_Tavily_Docs/svg_62.png","width":20,"height":20}
    - {"type":"svg","index":63,"filename":"Generate_Keys_-_Tavily_Docs/svg_63.png","width":20,"height":20}
    - {"type":"svg","index":64,"filename":"Generate_Keys_-_Tavily_Docs/svg_64.png","width":20,"height":20}
    - {"type":"svg","index":65,"filename":"Generate_Keys_-_Tavily_Docs/svg_65.png","width":49,"height":14}
    - {"type":"svg","index":66,"filename":"Generate_Keys_-_Tavily_Docs/svg_66.png","width":16,"height":16}
    - {"type":"svg","index":67,"filename":"Generate_Keys_-_Tavily_Docs/svg_67.png","width":16,"height":16}
    - {"type":"svg","index":68,"filename":"Generate_Keys_-_Tavily_Docs/svg_68.png","width":16,"height":16}
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

# Generate Keys

## 源URL

https://docs.tavily.com/documentation/enterprise/generate-keys

## 描述

Generate one or more API keys with custom configuration.

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
  --url https://api-key-generator.tavily.com/generate-keys \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "permission_level": "user",
  "name": "projectA",
  "scope": [
    "api:generate_keys"
  ],
  "key_type": "development",
  "key_limit": 200,
  "ttl_hours": 10,
  "count": 2
}
'
```

```text
{
  "keys": [
    "tvly-dev-MI9p6...",
    "tvly-dev-f7Wrr..."
  ],
  "expires_at": "2026-02-25T01:14:45Z",
  "created": "2026-02-24T15:14:45",
  "message": "2 keys generated successfully with 200 credits each. These keys will be automatically deactivated after 10 hours",
  "request_id": "949297ca-d123-4267-8041-45398a0b847d"
}
```

```text
curl --request POST \
  --url https://api-key-generator.tavily.com/generate-keys \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '
{
  "permission_level": "user",
  "name": "projectA",
  "scope": [
    "api:generate_keys"
  ],
  "key_type": "development",
  "key_limit": 200,
  "ttl_hours": 10,
  "count": 2
}
'
```

```text
{
  "keys": [
    "tvly-dev-MI9p6...",
    "tvly-dev-f7Wrr..."
  ],
  "expires_at": "2026-02-25T01:14:45Z",
  "created": "2026-02-24T15:14:45",
  "message": "2 keys generated successfully with 200 credits each. These keys will be automatically deactivated after 10 hours",
  "request_id": "949297ca-d123-4267-8041-45398a0b847d"
}
```

##### Authorizations

Bearer authentication header in the form Bearer , where  is your Tavily API key (e.g., Bearer tvly-YOUR_API_KEY).

##### Body

Parameters for generating API keys.

The permission level for the key.

The name of the key(s). Auto-generated in the format `{key_type}-{expiration}-#{index}`

Permission scopes for the key. Only applicable when `permission_level` is `"user"`.

The type of key.

The number of credits for the generated keys.

Number of hours before the keys become deactivated.

The total number of keys to generate.

##### Response

Keys generated successfully.

The generated API keys.

```text
["tvly-dev-MI9p6...", "tvly-dev-f7Wrr..."]
```

The expiration timestamp for the keys.

`"2026-02-25T01:14:45Z"`

The creation timestamp.

`"2026-02-24T15:14:45"`

A summary message about the generated keys.

`"2 keys generated successfully with 200 credits each. These keys will be automatically deactivated after 10 hours"`

Unique identifier for this generation request. Use this to bulk-deactivate the keys later.

`"949297ca-d123-4267-8041-45398a0b847d"`

![tavily-logo](Generate_Keys_-_Tavily_Docs/image_1.png)

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

![light logo](Generate_Keys_-_Tavily_Docs/image_1.svg)

![dark logo](Generate_Keys_-_Tavily_Docs/image_2.svg)

![light logo](Generate_Keys_-_Tavily_Docs/image_3.svg)

![dark logo](Generate_Keys_-_Tavily_Docs/image_4.svg)

![tavily-logo](Generate_Keys_-_Tavily_Docs/image_5.png)

![Powered by Onetrust](Generate_Keys_-_Tavily_Docs/image_6.svg)
*Powered by OneTrust Opens in a new Tab*

## 图表

![SVG图表 1](Generate_Keys_-_Tavily_Docs/svg_1.png)
*尺寸: 16x16px*

![SVG图表 2](Generate_Keys_-_Tavily_Docs/svg_2.png)
*尺寸: 16x16px*

![SVG图表 4](Generate_Keys_-_Tavily_Docs/svg_4.png)
*尺寸: 14x16px*

![SVG图表 11](Generate_Keys_-_Tavily_Docs/svg_11.png)
*尺寸: 16x16px*

![SVG图表 12](Generate_Keys_-_Tavily_Docs/svg_12.png)
*尺寸: 16x16px*

![SVG图表 13](Generate_Keys_-_Tavily_Docs/svg_13.png)
*尺寸: 16x16px*

![SVG图表 14](Generate_Keys_-_Tavily_Docs/svg_14.png)
*尺寸: 16x16px*

![SVG图表 16](Generate_Keys_-_Tavily_Docs/svg_16.png)
*尺寸: 16x16px*

![SVG图表 18](Generate_Keys_-_Tavily_Docs/svg_18.png)
*尺寸: 16x16px*

![SVG图表 19](Generate_Keys_-_Tavily_Docs/svg_19.png)
*尺寸: 16x16px*

![SVG图表 20](Generate_Keys_-_Tavily_Docs/svg_20.png)
*尺寸: 16x16px*

![SVG图表 21](Generate_Keys_-_Tavily_Docs/svg_21.png)
*尺寸: 16x16px*

![SVG图表 22](Generate_Keys_-_Tavily_Docs/svg_22.png)
*尺寸: 16x16px*

![SVG图表 23](Generate_Keys_-_Tavily_Docs/svg_23.png)
*尺寸: 16x16px*

![SVG图表 24](Generate_Keys_-_Tavily_Docs/svg_24.png)
*尺寸: 16x16px*

![SVG图表 25](Generate_Keys_-_Tavily_Docs/svg_25.png)
*尺寸: 16x16px*

![SVG图表 26](Generate_Keys_-_Tavily_Docs/svg_26.png)
*尺寸: 16x16px*

![SVG图表 27](Generate_Keys_-_Tavily_Docs/svg_27.png)
*尺寸: 14x14px*

![SVG图表 28](Generate_Keys_-_Tavily_Docs/svg_28.png)
*尺寸: 14x14px*

![SVG图表 29](Generate_Keys_-_Tavily_Docs/svg_29.png)
*尺寸: 16x16px*

![SVG图表 30](Generate_Keys_-_Tavily_Docs/svg_30.png)
*尺寸: 16x16px*

![SVG图表 31](Generate_Keys_-_Tavily_Docs/svg_31.png)
*尺寸: 16x16px*

![SVG图表 40](Generate_Keys_-_Tavily_Docs/svg_40.png)
*尺寸: 16x16px*

![SVG图表 41](Generate_Keys_-_Tavily_Docs/svg_41.png)
*尺寸: 18x18px*

![SVG图表 42](Generate_Keys_-_Tavily_Docs/svg_42.png)
*尺寸: 18x18px*

![SVG图表 43](Generate_Keys_-_Tavily_Docs/svg_43.png)
*尺寸: 18x18px*

![SVG图表 44](Generate_Keys_-_Tavily_Docs/svg_44.png)
*尺寸: 18x18px*

![SVG图表 45](Generate_Keys_-_Tavily_Docs/svg_45.png)
*尺寸: 18x18px*

![SVG图表 46](Generate_Keys_-_Tavily_Docs/svg_46.png)
*尺寸: 18x18px*

![SVG图表 47](Generate_Keys_-_Tavily_Docs/svg_47.png)
*尺寸: 18x18px*

![SVG图表 48](Generate_Keys_-_Tavily_Docs/svg_48.png)
*尺寸: 18x18px*

![SVG图表 49](Generate_Keys_-_Tavily_Docs/svg_49.png)
*尺寸: 18x18px*

![SVG图表 50](Generate_Keys_-_Tavily_Docs/svg_50.png)
*尺寸: 18x18px*

![SVG图表 51](Generate_Keys_-_Tavily_Docs/svg_51.png)
*尺寸: 18x18px*

![SVG图表 52](Generate_Keys_-_Tavily_Docs/svg_52.png)
*尺寸: 18x18px*

![SVG图表 53](Generate_Keys_-_Tavily_Docs/svg_53.png)
*尺寸: 18x18px*

![SVG图表 54](Generate_Keys_-_Tavily_Docs/svg_54.png)
*尺寸: 14x14px*

![SVG图表 55](Generate_Keys_-_Tavily_Docs/svg_55.png)
*尺寸: 14x14px*

![SVG图表 56](Generate_Keys_-_Tavily_Docs/svg_56.png)
*尺寸: 14x14px*

![SVG图表 61](Generate_Keys_-_Tavily_Docs/svg_61.png)
*尺寸: 20x20px*

![SVG图表 62](Generate_Keys_-_Tavily_Docs/svg_62.png)
*尺寸: 20x20px*

![SVG图表 63](Generate_Keys_-_Tavily_Docs/svg_63.png)
*尺寸: 20x20px*

![SVG图表 64](Generate_Keys_-_Tavily_Docs/svg_64.png)
*尺寸: 20x20px*

![SVG图表 65](Generate_Keys_-_Tavily_Docs/svg_65.png)
*尺寸: 49x14px*

![SVG图表 66](Generate_Keys_-_Tavily_Docs/svg_66.png)
*尺寸: 16x16px*

![SVG图表 67](Generate_Keys_-_Tavily_Docs/svg_67.png)
*尺寸: 16x16px*

![SVG图表 68](Generate_Keys_-_Tavily_Docs/svg_68.png)
*尺寸: 16x16px*
