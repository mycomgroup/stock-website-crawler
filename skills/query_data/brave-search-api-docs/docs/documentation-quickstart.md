---
id: "url-bd68030"
type: "api"
title: "Quickstart"
url: "https://api-dashboard.search.brave.com/documentation/quickstart"
description: "This guide will walk you through everything you need to perform your first search using the Brave Search API. From creating your account to making your first API request, you’ll be up and running in just a few minutes."
source: ""
tags: []
crawl_time: "2026-03-18T02:31:30.621Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/web/search?q=artificial+intelligence"
  method: "GET"
  sections:
    - {"level":"H2","title":"Introduction","content":["This guide will walk you through everything you need to perform your first search using the Brave Search API. From creating your account to making your first API request, you’ll be up and running in just a few minutes."],"codeBlocks":[]}
    - {"level":"H2","title":"Prerequisites","content":["Before you begin, make sure you have:","• A valid email address for account registration\n• A credit card for plan subscription\n• Basic familiarity with making HTTP requests"],"codeBlocks":[]}
    - {"level":"H2","title":"Step 1: Create Your Account","content":["Go to Brave Search API Dashboard to create your account:","• Enter your email address and create a secure password\n• Verify your email address by clicking the confirmation link sent to your inbox\n• Log in and you are ready for Step 2.","Account creation is free and only takes a minute."],"codeBlocks":[]}
    - {"level":"H2","title":"Step 2: Subscribe to a Plan","content":["Once your account is created, you’ll need to subscribe to a plan to access the API:","• Navigate to the Available plans section in your dashboard\n• Review the available plans and select one that fits your needs\n• Enter your credit card information"],"codeBlocks":[]}
    - {"level":"H2","title":"Step 3: Create an API Key","content":["After subscribing to a plan, generate your API key:","• Go to the API Keys section in your dashboard\n• Click on Add API Key\n• Give your key a descriptive name (e.g., “Production App” or “Development”)\n• Copy your API key and store it securely","Your API key is confidential. Never share it publicly, commit it to version\ncontrol, or expose it in client-side code. Treat it like a password."],"codeBlocks":[]}
    - {"level":"H2","title":"Step 4: Make Your First Search Request","content":["Now you’re ready to make your first search! The Brave Search API uses a simple REST architecture. All requests require your API key in the X-Subscription-Token header.","Here’s how to perform a basic web search:","A successful search returns a JSON object with various result types:","Full documentation of responses at API Reference page.","Keep track of your API usage in the dashboard to:","• Stay within your plan limits\n• Optimize your query patterns\n• Plan for scaling needs"],"codeBlocks":["{\n  \"type\": \"search\",\n  \"query\": {\n    \"original\": \"artificial intelligence\"\n  },\n  \"web\": {\n    \"results\": [\n      {\n        \"title\": \"Artificial Intelligence - Overview\",\n        \"url\": \"https://example.com/ai\",\n        \"description\": \"Learn about artificial intelligence...\",\n        \"age\": \"2024-10-08T10:30:00.000Z\"\n      }\n    ]\n  }\n}"]}
    - {"level":"H3","title":"Basic Web Search","content":["Here’s how to perform a basic web search:"],"codeBlocks":[]}
    - {"level":"H3","title":"Understanding the Response","content":["A successful search returns a JSON object with various result types:","Full documentation of responses at API Reference page."],"codeBlocks":["{\n  \"type\": \"search\",\n  \"query\": {\n    \"original\": \"artificial intelligence\"\n  },\n  \"web\": {\n    \"results\": [\n      {\n        \"title\": \"Artificial Intelligence - Overview\",\n        \"url\": \"https://example.com/ai\",\n        \"description\": \"Learn about artificial intelligence...\",\n        \"age\": \"2024-10-08T10:30:00.000Z\"\n      }\n    ]\n  }\n}"]}
    - {"level":"H3","title":"Monitor Your Usage","content":["Keep track of your API usage in the dashboard to:","• Stay within your plan limits\n• Optimize your query patterns\n• Plan for scaling needs"],"codeBlocks":[]}
    - {"level":"H2","title":"Next Steps","content":["Congratulations! You’ve made your first search with the Brave Search API. Here’s what to explore next:","Authentication Guide Learn more about securing your API requests    API Reference Explore all available endpoints and parameters    Rate Limiting Understand rate limits and how to optimize requests    API Versioning Learn about API versions and backward compatibility"],"codeBlocks":[]}
    - {"level":"H2","title":"Authentication Guide","content":["Learn more about securing your API requests"],"codeBlocks":[]}
    - {"level":"H2","title":"API Reference","content":["Explore all available endpoints and parameters"],"codeBlocks":[]}
    - {"level":"H2","title":"Rate Limiting","content":["Understand rate limits and how to optimize requests"],"codeBlocks":[]}
    - {"level":"H2","title":"API Versioning","content":["Learn about API versions and backward compatibility"],"codeBlocks":[]}
    - {"level":"H2","title":"Need Help?","content":["If you run into any issues or have questions:","• Check our API Documentation for detailed endpoint information\n• Review our Security Guidelines for best practices\n• See the common questions and answers or contact our support team at Help & Feedback page"],"codeBlocks":[]}
  tables: []
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=artificial+intelligence\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=artificial+intelligence\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"search\",\n  \"query\": {\n    \"original\": \"artificial intelligence\"\n  },\n  \"web\": {\n    \"results\": [\n      {\n        \"title\": \"Artificial Intelligence - Overview\",\n        \"url\": \"https://example.com/ai\",\n        \"description\": \"Learn about artificial intelligence...\",\n        \"age\": \"2024-10-08T10:30:00.000Z\"\n      }\n    ]\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"search\",\n  \"query\": {\n    \"original\": \"artificial intelligence\"\n  },\n  \"web\": {\n    \"results\": [\n      {\n        \"title\": \"Artificial Intelligence - Overview\",\n        \"url\": \"https://example.com/ai\",\n        \"description\": \"Learn about artificial intelligence...\",\n        \"age\": \"2024-10-08T10:30:00.000Z\"\n      }\n    ]\n  }\n}"}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nGetting started\n\nGet started with the Brave Search API in minutes\n\nIntroduction\n\nThis guide will walk you through everything you need to perform your first search using the Brave Search API. From creating your account to making your first API request, you’ll be up and running in just a few minutes.\n\nPrerequisites\n\nBefore you begin, make sure you have:\n\nA valid email address for account registration\n\nA credit card for plan subscription\n\nBasic familiarity with making HTTP requests\n\nStep 1: Create Your Account\n\nGo to Brave Search API Dashboard to create your account:\n\nEnter your email address and create a secure password\n\nVerify your email address by clicking the confirmation link sent to your inbox\n\nLog in and you are ready for Step 2.\n\nAccount creation is free and only takes a minute.\n\nStep 2: Subscribe to a Plan\n\nOnce your account is created, you’ll need to subscribe to a plan to access the API:\n\nNavigate to the Available plans section in your dashboard\n\nReview the available plans and select one that fits your needs\n\nEnter your credit card information\n\nStep 3: Create an API Key\n\nAfter subscribing to a plan, generate your API key:\n\nGo to the API Keys section in your dashboard\n\nClick on Add API Key\n\nGive your key a descriptive name (e.g., “Production App” or “Development”)\n\nCopy your API key and store it securely\n\nYour API key is confidential. Never share it publicly, commit it to version\ncontrol, or expose it in client-side code. Treat it like a password.\n\nStep 4: Make Your First Search Request\n\nNow you’re ready to make your first search! The Brave Search API uses a simple REST architecture. All requests require your API key in the X-Subscription-Token header.\n\nBasic Web Search\n\nHere’s how to perform a basic web search:\n\nPython\n\nNode.js\n\nUnderstanding the Response\n\nA successful search returns a JSON object with various result types:\n\nFull documentation of responses at API Reference page.\n\nMonitor Your Usage\n\nKeep track of your API usage in the dashboard to:\n\nStay within your plan limits\n\nOptimize your query patterns\n\nPlan for scaling needs\n\nNext Steps\n\nCongratulations! You’ve made your first search with the Brave Search API. Here’s what to explore next:\n\nAuthentication Guide\n\nLearn more about securing your API requests\n\nAPI Reference\n\nExplore all available endpoints and parameters\n\nRate Limiting\n\nUnderstand rate limits and how to optimize requests\n\nAPI Versioning\n\nLearn about API versions and backward compatibility\n\nNeed Help?\n\nIf you run into any issues or have questions:\n\nCheck our API Documentation for detailed endpoint information\n\nReview our Security Guidelines for best practices\n\nSee the common questions and answers or contact our support team at Help & Feedback page\n\nOn this page\n\nAuthentication Guide Learn more about securing your API requests\n\nAPI Reference Explore all available endpoints and parameters\n\nRate Limiting Understand rate limits and how to optimize requests\n\nAPI Versioning Learn about API versions and backward compatibility"
  suggestedFilename: "documentation-quickstart"
---

# Quickstart

## 源URL

https://api-dashboard.search.brave.com/documentation/quickstart

## 描述

This guide will walk you through everything you need to perform your first search using the Brave Search API. From creating your account to making your first API request, you’ll be up and running in just a few minutes.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/web/search?q=artificial+intelligence`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/web/search?q=artificial+intelligence" \
  -H "X-Subscription-Token: YOUR_API_KEY"
```

### 示例 2 (json)

```json
{
  "type": "search",
  "query": {
    "original": "artificial intelligence"
  },
  "web": {
    "results": [
      {
        "title": "Artificial Intelligence - Overview",
        "url": "https://example.com/ai",
        "description": "Learn about artificial intelligence...",
        "age": "2024-10-08T10:30:00.000Z"
      }
    ]
  }
}
```

## 文档正文

This guide will walk you through everything you need to perform your first search using the Brave Search API. From creating your account to making your first API request, you’ll be up and running in just a few minutes.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/web/search?q=artificial+intelligence`

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

Getting started

Get started with the Brave Search API in minutes

Introduction

This guide will walk you through everything you need to perform your first search using the Brave Search API. From creating your account to making your first API request, you’ll be up and running in just a few minutes.

Prerequisites

Before you begin, make sure you have:

A valid email address for account registration

A credit card for plan subscription

Basic familiarity with making HTTP requests

Step 1: Create Your Account

Go to Brave Search API Dashboard to create your account:

Enter your email address and create a secure password

Verify your email address by clicking the confirmation link sent to your inbox

Log in and you are ready for Step 2.

Account creation is free and only takes a minute.

Step 2: Subscribe to a Plan

Once your account is created, you’ll need to subscribe to a plan to access the API:

Navigate to the Available plans section in your dashboard

Review the available plans and select one that fits your needs

Enter your credit card information

Step 3: Create an API Key

After subscribing to a plan, generate your API key:

Go to the API Keys section in your dashboard

Click on Add API Key

Give your key a descriptive name (e.g., “Production App” or “Development”)

Copy your API key and store it securely

Your API key is confidential. Never share it publicly, commit it to version
control, or expose it in client-side code. Treat it like a password.

Step 4: Make Your First Search Request

Now you’re ready to make your first search! The Brave Search API uses a simple REST architecture. All requests require your API key in the X-Subscription-Token header.

Basic Web Search

Here’s how to perform a basic web search:

Python

Node.js

Understanding the Response

A successful search returns a JSON object with various result types:

Full documentation of responses at API Reference page.

Monitor Your Usage

Keep track of your API usage in the dashboard to:

Stay within your plan limits

Optimize your query patterns

Plan for scaling needs

Next Steps

Congratulations! You’ve made your first search with the Brave Search API. Here’s what to explore next:

Authentication Guide

Learn more about securing your API requests

API Reference

Explore all available endpoints and parameters

Rate Limiting

Understand rate limits and how to optimize requests

API Versioning

Learn about API versions and backward compatibility

Need Help?

If you run into any issues or have questions:

Check our API Documentation for detailed endpoint information

Review our Security Guidelines for best practices

See the common questions and answers or contact our support team at Help & Feedback page

On this page

Authentication Guide Learn more about securing your API requests

API Reference Explore all available endpoints and parameters

Rate Limiting Understand rate limits and how to optimize requests

API Versioning Learn about API versions and backward compatibility
