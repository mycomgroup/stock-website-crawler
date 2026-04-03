---
id: "url-65d79a75"
type: "api"
title: "Authentication"
url: "https://api-dashboard.search.brave.com/documentation/guides/authentication"
description: "The Brave Search API uses API key authentication to secure requests. Every API request must include your subscription token in the request header to authenticate and authorize access."
source: ""
tags: []
crawl_time: "2026-03-18T03:28:02.418Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/web/search?q=brave+search"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["The Brave Search API uses API key authentication to secure requests. Every API request must include your subscription token in the request header to authenticate and authorize access.","Your API key is confidential and should be kept secure. Never expose it in\nclient-side code, public repositories, or any public location."],"codeBlocks":[]}
    - {"level":"H2","title":"Obtaining Your API Key","content":["To get started with the Brave Search API, you’ll need a subscription token:","• Subscribe to a plan — Visit the Brave Search API page and choose a plan that fits your needs\n• Create an API key — Once subscribed, navigate to the API Keys section in your dashboard and create a new key\n• Copy your token — Your subscription token will be displayed. Copy it to use in your requests"],"codeBlocks":[]}
    - {"level":"H2","title":"Authentication Method","content":["All requests to the Brave Search API must include your subscription token in the X-Subscription-Token HTTP header."],"codeBlocks":["X-Subscription-Token: YOUR_API_KEY"]}
    - {"level":"H3","title":"Header Format","content":[],"codeBlocks":["X-Subscription-Token: YOUR_API_KEY"]}
    - {"level":"H2","title":"Code Examples","content":["Here are examples of how to authenticate your search queries:"],"codeBlocks":[]}
    - {"level":"H2","title":"Best Practices","content":["Never hardcode your API key directly in your source code. Instead, use environment variables or secure configuration management:","Regularly rotate your API keys as a security best practice. You can generate new and revoke old keys from the dashboard.","If you suspect your API key has been compromised, immediately revoke it from\nyour dashboard and generate a new one.","To learn more about best practises, see OWASP Cheat Sheet for Secrets Management."],"codeBlocks":[]}
    - {"level":"H3","title":"Secure Storage","content":["Never hardcode your API key directly in your source code. Instead, use environment variables or secure configuration management:"],"codeBlocks":[]}
    - {"level":"H3","title":"Key Rotation","content":["Regularly rotate your API keys as a security best practice. You can generate new and revoke old keys from the dashboard.","If you suspect your API key has been compromised, immediately revoke it from\nyour dashboard and generate a new one."],"codeBlocks":[]}
    - {"level":"H3","title":"More","content":["To learn more about best practises, see OWASP Cheat Sheet for Secrets Management."],"codeBlocks":[]}
    - {"level":"H2","title":"Next Steps","content":["API Overview Learn about available endpoints and features    API Reference Explore detailed API documentation"],"codeBlocks":[]}
    - {"level":"H2","title":"API Overview","content":["Learn about available endpoints and features"],"codeBlocks":[]}
    - {"level":"H2","title":"API Reference","content":["Explore detailed API documentation"],"codeBlocks":[]}
  tables: []
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=brave+search\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=brave+search\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nBasics\n\nLearn how to authenticate your requests to the Brave Search API using subscription tokens\n\nOverview\n\nThe Brave Search API uses API key authentication to secure requests. Every API request must include your subscription token in the request header to authenticate and authorize access.\n\nYour API key is confidential and should be kept secure. Never expose it in\nclient-side code, public repositories, or any public location.\n\nObtaining Your API Key\n\nTo get started with the Brave Search API, you’ll need a subscription token:\n\nSubscribe to a plan — Visit the Brave Search API page and choose a plan that fits your needs\n\nCreate an API key — Once subscribed, navigate to the API Keys section in your dashboard and create a new key\n\nCopy your token — Your subscription token will be displayed. Copy it to use in your requests\n\nAuthentication Method\n\nAll requests to the Brave Search API must include your subscription token in the X-Subscription-Token HTTP header.\n\nHeader Format\n\nCode Examples\n\nHere are examples of how to authenticate your search queries:\n\nPython\n\nNode.js\n\nBest Practices\n\nSecure Storage\n\nNever hardcode your API key directly in your source code. Instead, use environment variables or secure configuration management:\n\nEnvironment Variable\n\nKey Rotation\n\nRegularly rotate your API keys as a security best practice. You can generate new and revoke old keys from the dashboard.\n\nIf you suspect your API key has been compromised, immediately revoke it from\nyour dashboard and generate a new one.\n\nTo learn more about best practises, see OWASP Cheat Sheet for Secrets Management.\n\nNext Steps\n\nAPI Overview\n\nLearn about available endpoints and features\n\nAPI Reference\n\nExplore detailed API documentation\n\nOn this page\n\nAPI Overview Learn about available endpoints and features\n\nAPI Reference Explore detailed API documentation"
  suggestedFilename: "guides-authentication"
---

# Authentication

## 源URL

https://api-dashboard.search.brave.com/documentation/guides/authentication

## 描述

The Brave Search API uses API key authentication to secure requests. Every API request must include your subscription token in the request header to authenticate and authorize access.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/web/search?q=brave+search`

## 代码示例

```bash
curl "https://api.search.brave.com/res/v1/web/search?q=brave+search" \
  -H "X-Subscription-Token: YOUR_API_KEY"
```

## 文档正文

The Brave Search API uses API key authentication to secure requests. Every API request must include your subscription token in the request header to authenticate and authorize access.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/web/search?q=brave+search`

Quickstart

Pricing

Authentication

Versioning

Rate limiting

Web search

LLM Context New

News search

Video search

Image search

Summarizer search

Place search New

Answers

Autosuggest

Spellcheck

Skills

Help & Feedback

Goggles

Search operators

Status updates

Security

Privacy notice

Terms of service

Basics

Learn how to authenticate your requests to the Brave Search API using subscription tokens

Overview

The Brave Search API uses API key authentication to secure requests. Every API request must include your subscription token in the request header to authenticate and authorize access.

Your API key is confidential and should be kept secure. Never expose it in
client-side code, public repositories, or any public location.

Obtaining Your API Key

To get started with the Brave Search API, you’ll need a subscription token:

Subscribe to a plan — Visit the Brave Search API page and choose a plan that fits your needs

Create an API key — Once subscribed, navigate to the API Keys section in your dashboard and create a new key

Copy your token — Your subscription token will be displayed. Copy it to use in your requests

Authentication Method

All requests to the Brave Search API must include your subscription token in the X-Subscription-Token HTTP header.

Header Format

Code Examples

Here are examples of how to authenticate your search queries:

Python

Node.js

Best Practices

Secure Storage

Never hardcode your API key directly in your source code. Instead, use environment variables or secure configuration management:

Environment Variable

Key Rotation

Regularly rotate your API keys as a security best practice. You can generate new and revoke old keys from the dashboard.

If you suspect your API key has been compromised, immediately revoke it from
your dashboard and generate a new one.

To learn more about best practises, see OWASP Cheat Sheet for Secrets Management.

Next Steps

API Overview

Learn about available endpoints and features

API Reference

Explore detailed API documentation

On this page

API Overview Learn about available endpoints and features

API Reference Explore detailed API documentation
