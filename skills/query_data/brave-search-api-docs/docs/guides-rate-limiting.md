---
id: "url-27e0f4f7"
type: "api"
title: "Rate limiting"
url: "https://api-dashboard.search.brave.com/documentation/guides/rate-limiting"
description: "The API implements rate limiting to ensure fair usage and system stability. Rate limits are enforced using a 1-second sliding window to count requests per subscription. This means your request count is evaluated in real-time over the most recent second."
source: ""
tags: []
crawl_time: "2026-03-18T02:33:14.895Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/web/search"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["The API implements rate limiting to ensure fair usage and system stability. Rate limits are enforced using a 1-second sliding window to count requests per subscription. This means your request count is evaluated in real-time over the most recent second.","When you exceed your rate limit, the API will return a 429 status code and\nyour request will fail. Monitor the rate limit headers to avoid hitting these\nlimits."],"codeBlocks":[]}
    - {"level":"H2","title":"Rate Limit Response Headers","content":["Every API response includes headers that help you track and manage your rate limits. Use these headers to implement proper rate limiting logic in your application.","HeaderDescriptionExampleX-RateLimit-LimitRate limits associated with your plan1, 15000 (1 request/second, 15000 requests/month)X-RateLimit-PolicyRate limit policies with window sizes in seconds1;w=1, 15000;w=2592000 (1 req per 1s window, 15000 req per month window)X-RateLimit-RemainingRemaining quota for each limit window1, 1000 (1 request left this second, 1000 left this month)X-RateLimit-ResetSeconds until each quota resets1, 1419704 (resets in 1 second and 1419704 seconds)"],"codeBlocks":[]}
    - {"level":"H2","title":"Understanding the Headers","content":["Shows the maximum number of requests allowed for each time window in your plan.","Example: X-RateLimit-Limit: 1, 15000","• 1 request per second - Burst rate limit\n• 15,000 requests per month - Monthly quota (0 for unlimited)","Provides the complete policy specification including window sizes. Windows are always expressed in seconds.","Example: X-RateLimit-Policy: 1;w=1, 15000;w=2592000","• 1;w=1 - Limit of 1 request over a 1-second window\n• 15000;w=2592000 - Limit of 15,000 requests over a 2,592,000-second window (30 days)","Indicates how many requests you can still make within each time window before hitting the limit.","Example: X-RateLimit-Remaining: 1, 1000","• 1 request available in the current second\n• 1,000 requests remaining in the current month","Important: Only successful requests (non-error responses) are counted\nagainst your quota and billed.","Shows when each quota window will reset, expressed in seconds from now.","Example: X-RateLimit-Reset: 1, 1419704","• 1 second until you can make another request (per-second limit resets)\n• 1,419,704 seconds until your monthly quota fully resets (≈16.4 days)"],"codeBlocks":[]}
    - {"level":"H3","title":"X-RateLimit-Limit","content":["Shows the maximum number of requests allowed for each time window in your plan.","Example: X-RateLimit-Limit: 1, 15000","• 1 request per second - Burst rate limit\n• 15,000 requests per month - Monthly quota (0 for unlimited)"],"codeBlocks":[]}
    - {"level":"H3","title":"X-RateLimit-Policy","content":["Provides the complete policy specification including window sizes. Windows are always expressed in seconds.","Example: X-RateLimit-Policy: 1;w=1, 15000;w=2592000","• 1;w=1 - Limit of 1 request over a 1-second window\n• 15000;w=2592000 - Limit of 15,000 requests over a 2,592,000-second window (30 days)"],"codeBlocks":[]}
    - {"level":"H3","title":"X-RateLimit-Remaining","content":["Indicates how many requests you can still make within each time window before hitting the limit.","Example: X-RateLimit-Remaining: 1, 1000","• 1 request available in the current second\n• 1,000 requests remaining in the current month","Important: Only successful requests (non-error responses) are counted\nagainst your quota and billed."],"codeBlocks":[]}
    - {"level":"H3","title":"X-RateLimit-Reset","content":["Shows when each quota window will reset, expressed in seconds from now.","Example: X-RateLimit-Reset: 1, 1419704","• 1 second until you can make another request (per-second limit resets)\n• 1,419,704 seconds until your monthly quota fully resets (≈16.4 days)"],"codeBlocks":[]}
    - {"level":"H2","title":"Key Insights","content":["• Real-time tracking: The 1-second window slides continuously, so your request count is always calculated for the most recent second.\n• Counted on arrival: The request count is increased when request is received. The processing time does not affect the rate-limit.\n• Multiple limits: Most plans have both burst limits (per-second) and quota limits (per-month) that must be respected simultaneously\n• Successful requests only: Failed requests don’t count against your quota, so you’re only charged for successful API calls\n• Predictable resets: Use the X-RateLimit-Reset header to calculate exactly when you can safely retry"],"codeBlocks":[]}
    - {"level":"H2","title":"Example Response Headers","content":["Here’s what you might see in a typical API response:","Interpretation:","• You’ve used your 1 request for this second (Remaining: 0)\n• You have 14,523 requests left this month (Remaining: 14523)\n• You can make another request in 1 second\n• Your monthly quota resets in 1,234,567 seconds (≈14.3 days)"],"codeBlocks":[]}
  tables:
    - {"index":0,"headers":["Header","Description","Example"],"rows":[["X-RateLimit-Limit","Rate limits associated with your plan","1, 15000 (1 request/second, 15000 requests/month)"],["X-RateLimit-Policy","Rate limit policies with window sizes in seconds","1;w=1, 15000;w=2592000 (1 req per 1s window, 15000 req per month window)"],["X-RateLimit-Remaining","Remaining quota for each limit window","1, 1000 (1 request left this second, 1000 left this month)"],["X-RateLimit-Reset","Seconds until each quota resets","1, 1419704 (resets in 1 second and 1419704 seconds)"]]}
  examples: []
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nBasics\n\nUnderstand how rate limiting works and best practices for staying within your quota\n\nOverview\n\nThe API implements rate limiting to ensure fair usage and system stability. Rate limits are enforced using a 1-second sliding window to count requests per subscription. This means your request count is evaluated in real-time over the most recent second.\n\nWhen you exceed your rate limit, the API will return a 429 status code and\nyour request will fail. Monitor the rate limit headers to avoid hitting these\nlimits.\n\nRate Limit Response Headers\n\nEvery API response includes headers that help you track and manage your rate limits. Use these headers to implement proper rate limiting logic in your application.\n\nUnderstanding the Headers\n\nX-RateLimit-Limit\n\nShows the maximum number of requests allowed for each time window in your plan.\n\nExample: X-RateLimit-Limit: 1, 15000\n\n1 request per second - Burst rate limit\n\n15,000 requests per month - Monthly quota (0 for unlimited)\n\nX-RateLimit-Policy\n\nProvides the complete policy specification including window sizes. Windows are always expressed in seconds.\n\nExample: X-RateLimit-Policy: 1;w=1, 15000;w=2592000\n\n1;w=1 - Limit of 1 request over a 1-second window\n\n15000;w=2592000 - Limit of 15,000 requests over a 2,592,000-second window (30 days)\n\nX-RateLimit-Remaining\n\nIndicates how many requests you can still make within each time window before hitting the limit.\n\nExample: X-RateLimit-Remaining: 1, 1000\n\n1 request available in the current second\n\n1,000 requests remaining in the current month\n\nImportant: Only successful requests (non-error responses) are counted\nagainst your quota and billed.\n\nX-RateLimit-Reset\n\nShows when each quota window will reset, expressed in seconds from now.\n\nExample: X-RateLimit-Reset: 1, 1419704\n\n1 second until you can make another request (per-second limit resets)\n\n1,419,704 seconds until your monthly quota fully resets (≈16.4 days)\n\nBest Practices\n\nWhen you receive a 429 status code, check the X-RateLimit-Reset header to determine how long to wait before retrying. Implement exponential backoff for additional resilience.\n\nPython\n\nCheck X-RateLimit-Remaining before making subsequent requests. This helps you avoid hitting limits unexpectedly.\n\nJavaScript\n\nInstead of bursting all requests at once, distribute them evenly throughout\nyour time window to maximize throughput and avoid hitting the per-second\nlimit.\n\nYour plan may have multiple limit windows (per-second, quota). Track all to ensure you don’t exceed either limit.\n\nKey Insights\n\nReal-time tracking: The 1-second window slides continuously, so your request count is always calculated for the most recent second.\n\nCounted on arrival: The request count is increased when request is received. The processing time does not affect the rate-limit.\n\nMultiple limits: Most plans have both burst limits (per-second) and quota limits (per-month) that must be respected simultaneously\n\nSuccessful requests only: Failed requests don’t count against your quota, so you’re only charged for successful API calls\n\nPredictable resets: Use the X-RateLimit-Reset header to calculate exactly when you can safely retry\n\nExample Response Headers\n\nHere’s what you might see in a typical API response:\n\nInterpretation:\n\nYou’ve used your 1 request for this second (Remaining: 0)\n\nYou have 14,523 requests left this month (Remaining: 14523)\n\nYou can make another request in 1 second\n\nYour monthly quota resets in 1,234,567 seconds (≈14.3 days)\n\nOn this page"
  suggestedFilename: "guides-rate-limiting"
---

# Rate limiting

## 源URL

https://api-dashboard.search.brave.com/documentation/guides/rate-limiting

## 描述

The API implements rate limiting to ensure fair usage and system stability. Rate limits are enforced using a 1-second sliding window to count requests per subscription. This means your request count is evaluated in real-time over the most recent second.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/web/search`

## 文档正文

The API implements rate limiting to ensure fair usage and system stability. Rate limits are enforced using a 1-second sliding window to count requests per subscription. This means your request count is evaluated in real-time over the most recent second.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/web/search`

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

Understand how rate limiting works and best practices for staying within your quota

Overview

The API implements rate limiting to ensure fair usage and system stability. Rate limits are enforced using a 1-second sliding window to count requests per subscription. This means your request count is evaluated in real-time over the most recent second.

When you exceed your rate limit, the API will return a 429 status code and
your request will fail. Monitor the rate limit headers to avoid hitting these
limits.

Rate Limit Response Headers

Every API response includes headers that help you track and manage your rate limits. Use these headers to implement proper rate limiting logic in your application.

Understanding the Headers

X-RateLimit-Limit

Shows the maximum number of requests allowed for each time window in your plan.

Example: X-RateLimit-Limit: 1, 15000

1 request per second - Burst rate limit

15,000 requests per month - Monthly quota (0 for unlimited)

X-RateLimit-Policy

Provides the complete policy specification including window sizes. Windows are always expressed in seconds.

Example: X-RateLimit-Policy: 1;w=1, 15000;w=2592000

1;w=1 - Limit of 1 request over a 1-second window

15000;w=2592000 - Limit of 15,000 requests over a 2,592,000-second window (30 days)

X-RateLimit-Remaining

Indicates how many requests you can still make within each time window before hitting the limit.

Example: X-RateLimit-Remaining: 1, 1000

1 request available in the current second

1,000 requests remaining in the current month

Important: Only successful requests (non-error responses) are counted
against your quota and billed.

X-RateLimit-Reset

Shows when each quota window will reset, expressed in seconds from now.

Example: X-RateLimit-Reset: 1, 1419704

1 second until you can make another request (per-second limit resets)

1,419,704 seconds until your monthly quota fully resets (≈16.4 days)

Best Practices

When you receive a 429 status code, check the X-RateLimit-Reset header to determine how long to wait before retrying. Implement exponential backoff for additional resilience.

Python

Check X-RateLimit-Remaining before making subsequent requests. This helps you avoid hitting limits unexpectedly.

JavaScript

Instead of bursting all requests at once, distribute them evenly throughout
your time window to maximize throughput and avoid hitting the per-second
limit.

Your plan may have multiple limit windows (per-second, quota). Track all to ensure you don’t exceed either limit.

Key Insights

Real-time tracking: The 1-second window slides continuously, so your request count is always calculated for the most recent second.

Counted on arrival: The request count is increased when request is received. The processing time does not affect the rate-limit.

Multiple limits: Most plans have both burst limits (per-second) and quota limits (per-month) that must be respected simultaneously

Successful requests only: Failed requests don’t count against your quota, so you’re only charged for successful API calls

Predictable resets: Use the X-RateLimit-Reset header to calculate exactly when you can safely retry

Example Response Headers

Here’s what you might see in a typical API response:

Interpretation:

You’ve used your 1 request for this second (Remaining: 0)

You have 14,523 requests left this month (Remaining: 14523)

You can make another request in 1 second

Your monthly quota resets in 1,234,567 seconds (≈14.3 days)

On this page
