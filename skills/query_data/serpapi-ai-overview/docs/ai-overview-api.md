---
id: "url-13aeb3a3"
type: "api"
title: "Google AI Overview Results API"
url: "https://serpapi.com/ai-overview"
description: "For some searches, Google search results includes an AI Overview block. SerpApi is able to scrape, extract and make sense of this information.\n\nCurrently, the AI Overview block is only seen for English searches (hl=en) with a limited range of countries (gl).\n\nThe API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.\n\nGoogle sometimes requires an additional request to retrieve AI Overview results. See the extra request example and our Google AI Overview API to understand how to handle these cases.\n\nTypical result containing headings, paragraphs, lists (with and without title) and a thumbnail."
source: ""
tags: []
crawl_time: "2026-03-18T01:34:25.902Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Typical result","description":"Typical result containing headings, paragraphs, lists (with and without title) and a thumbnail.","requestParams":{"q":"drop shipping","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=drop+shipping"}
    - {"title":"Example with a list containing thumbnails","description":"","requestParams":{"q":"successful quotes","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=successful+quotes"}
    - {"title":"Example with nested lists","description":"","requestParams":{"q":"drop shipping","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=drop+shipping"}
    - {"title":"Example with table","description":"","requestParams":{"q":"immune related adverse events","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=immune+related+adverse+events"}
    - {"title":"Example with LaTeX equations in the paragraph","description":"","requestParams":{"engine":"google_ai_overview","page_token":"CpFBUnicxZTdcqpIEMev9x329nCTqKjgR6qorWGckDHiYfAj0RuKAA6KSCIK6N2-yz7VPs3OgEmIMamztRfbVTDQ0zPd_OdH__nXerkJ_v7td3-3e45varU0Tas0iujaqzpRWLPjw8apLaJ1vHX8P-ha2cfCfr_2lPQKAkwwxDZ5nB5dbb0f3JprT7s9Dm6ne_vRXM-hOna1W3H-qAv-WvE2wiFRmoITK6LgLZUWMjx7OOirldUgMLDxImv3EgmEPKNiPdmxt2IFZau4ZtXYLfjR7LGXalz1NlUMl_LUyBJDjqoNsd6p_qzZIQsA_93UL_wQIALAPRsJu05GAUCAOb4wgorQUdlJ3554uSjfA3InnpyvR_SUWlUxSO-sdpDq5elyde91Q4lnuQcp2xpq330hOd1pMaDzSHrp3fmU_Nzw7H0BBiChKh-4SXl9fKlK0WTypiNhM6vUTUcIXdSfK09XIVkE8NJ0bgHsx7MXka1HNZcyGMTa05YN9do25mjAcVeMtMNGdyeH9iJ9fuhZjtp-unuQzGXmVsT0OofOid-oi8vU3Xe9kHQffKkPqoOqWn9DDhMwDiYQF2LqrzqNcl6-M_z6wEqGFH6OzoUCkMXdmsSnRagIYiYGYSQW1gFoJsMIgtfjGpXup01UPsMPBUNgEsReIcqFxAQCqPJCAu5AfQAitoDyj1ELUO6AnjN0Ep4wptWEZZ0BDagkLT73kM-dkAOkOEO-b1mDPJbk2D8SHwFMJ0CbuTrLQ1__IazytOSUjjsnTKcOzXfnHh-DXqpS2imKGbFAph0PVQHiPxRFmLMZ8VkeM8uF1Vn2wQfkeNnqOeAlI6eYC79FyfAFxu6w3dBMSYrD7n68mPjomECoueYwHpETY1H49C9am_M_U5g3PobO1ByVKETfUEjQ6GPj4xT6bxT23iksGt85haigcMQbn8ob3yYtU4jeKYSa-k7hh8b3mcLc8UsU-mcU0hKF6GsKWeMrU5jQZ3Yu-Z4SFxZ-pvDXG9-FRn6yD40vh9Erho9dcL-i56Si5Ke66KCm4eFGw37sbbFhBb6RydAH19Yi3N3Y7vraWro3aqO_O7jCi5L9kFHjiu1wJV5fZflDXQjX20gR7XZPxI2-bPRm4nE-7k4rvSRs9-1jFMb6Lqw8jbMsNdzWSKek3W5ri6M-SIaTvnPsjeuV3j4UtcEsuZddQ4Z7KXM2d4axe3aWw6Zlz4mB6d6sb0QvtutiPw3lhZ6BhbW1umYwXeKWVKHOtpNmTTPoyMZwvu0lG2j2o7y4WFnolTnuNieDByCEW0dhJyAFYEgAEWLHtrw4Udy622h5YtNuubbcXLSEkO4Oz0pL-gdEpaR1","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?engine=google_ai_overview&page_token=CpFBUnicxZTdcqpIEMev9x329nCTqKjgR6qorWGckDHiYfAj0RuKAA6KSCIK6N2-yz7VPs3OgEmIMamztRfbVTDQ0zPd_OdH__nXerkJ_v7td3-3e45varU0Tas0iujaqzpRWLPjw8apLaJ1vHX8P-ha2cfCfr_2lPQKAkwwxDZ5nB5dbb0f3JprT7s9Dm6ne_vRXM-hOna1W3H-qAv-WvE2wiFRmoITK6LgLZUWMjx7OOirldUgMLDxImv3EgmEPKNiPdmxt2IFZau4ZtXYLfjR7LGXalz1NlUMl_LUyBJDjqoNsd6p_qzZIQsA_93UL_wQIALAPRsJu05GAUCAOb4wgorQUdlJ3554uSjfA3InnpyvR_SUWlUxSO-sdpDq5elyde91Q4lnuQcp2xpq330hOd1pMaDzSHrp3fmU_Nzw7H0BBiChKh-4SXl9fKlK0WTypiNhM6vUTUcIXdSfK09XIVkE8NJ0bgHsx7MXka1HNZcyGMTa05YN9do25mjAcVeMtMNGdyeH9iJ9fuhZjtp-unuQzGXmVsT0OofOid-oi8vU3Xe9kHQffKkPqoOqWn9DDhMwDiYQF2LqrzqNcl6-M_z6wEqGFH6OzoUCkMXdmsSnRagIYiYGYSQW1gFoJsMIgtfjGpXup01UPsMPBUNgEsReIcqFxAQCqPJCAu5AfQAitoDyj1ELUO6AnjN0Ep4wptWEZZ0BDagkLT73kM-dkAOkOEO-b1mDPJbk2D8SHwFMJ0CbuTrLQ1__IazytOSUjjsnTKcOzXfnHh-DXqpS2imKGbFAph0PVQHiPxRFmLMZ8VkeM8uF1Vn2wQfkeNnqOeAlI6eYC79FyfAFxu6w3dBMSYrD7n68mPjomECoueYwHpETY1H49C9am_M_U5g3PobO1ByVKETfUEjQ6GPj4xT6bxT23iksGt85haigcMQbn8ob3yYtU4jeKYSa-k7hh8b3mcLc8UsU-mcU0hKF6GsKWeMrU5jQZ3Yu-Z4SFxZ-pvDXG9-FRn6yD40vh9Erho9dcL-i56Si5Ke66KCm4eFGw37sbbFhBb6RydAH19Yi3N3Y7vraWro3aqO_O7jCi5L9kFHjiu1wJV5fZflDXQjX20gR7XZPxI2-bPRm4nE-7k4rvSRs9-1jFMb6Lqw8jbMsNdzWSKek3W5ri6M-SIaTvnPsjeuV3j4UtcEsuZddQ4Z7KXM2d4axe3aWw6Zlz4mB6d6sb0QvtutiPw3lhZ6BhbW1umYwXeKWVKHOtpNmTTPoyMZwvu0lG2j2o7y4WFnolTnuNieDByCEW0dhJyAFYEgAEWLHtrw4Udy622h5YtNuubbcXLSEkO4Oz0pL-gdEpaR1"}
    - {"title":"Example with LaTeX equations in the table","description":"","requestParams":{"q":"at what temperature pressure remaining unchanged","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=at+what+temperature+pressure+remaining+unchanged"}
    - {"title":"Example with LaTeX equations in the list","description":"","requestParams":{"q":"why rms velocity of a gas doubles","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=why+rms+velocity+of+a+gas+doubles"}
    - {"title":"Paragraph with video","description":"","requestParams":{"q":"how does android work","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=how+does+android+work"}
    - {"title":"Example with expandable sections","description":"","requestParams":{"q":"drop shipping","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=drop+shipping"}
    - {"title":"Example of paragraph with snippet_links","description":"","requestParams":{"q":"explain ruby language","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=explain+ruby+language"}
    - {"title":"Example of list with snippet_links","description":"","requestParams":{"q":"explain ruby language","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=explain+ruby+language"}
    - {"title":"Example with products comparison","description":"","requestParams":{"q":"iphone 16 vs 15","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=iphone+16+vs+15"}
    - {"title":"Example with an extra request required","description":"Google can return AI Overview content through a separate request instead of directly in a response. In these cases we return page_token for the associated request and serpapi_link for the corresponding SerpApi search using our Google AI Overview API. The resulting JSON structure is the same as the above examples. The rendered HTML will show \"Can't generate an AI overview right now. Try again later.\" — this is expected behaviour and can be ignored. page_token and serpapi_link will expire within 4 minutes of the search and should be used immediately.","requestParams":{"q":"how does art work in android","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=how+does+art+work+in+android"}
    - {"title":"Example with error message","description":"","requestParams":{"q":"drop shipping","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?q=drop+shipping"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"ai_overview\": {\n    // When separate request is required for the AI Overview content\n    \"page_token\": \"String - Token for the AI Overview block\",\n    \"serpapi_link\": \"String - URL to the corresponding SerpApi search\",\n    // When the AI Overview block includes products\n    \"products\": [\n      {\n        \"thumbnail\": \"String - URL to the product thumbnail image\",\n        \"title\": \"String - Title of the product\",\n        \"rating\": \"String - Product rating\",\n        \"reviews\": \"String - Number of reviews for the product\",\n        \"price\": \"String - Price of the product\",\n        \"extracted_price\": \"Number - Extracted price value from the product\",\n        \"installments\": \"String - Installment information for the product\"\n      },\n      ...\n    ],\n    // When the AI Overview block is embedded in the search results\n    \"text_blocks\": [\n      {\n        \"type\": \"String - Type of the text block. Can be 'heading', 'paragraph', 'list', 'expandable', or 'comparison'\",\n        \"snippet\": \"String - Snippet of the text block\",\n        \"snippet_latex\": \"Array of strings - LaTeX equations in the snippet\",\n        \"snippet_highlighted_words\": \"Array of strings - Highlighted words in the snippet\",\n        \"snippet_links\": {\n          \"text\": \"String - Text content of inline link\",\n          \"link\": \"String - URL of inline link\",\n        },\n        \"reference_indexes\": \"Array of integers - Indexes of the references in the root 'references' field\",\n        \"thumbnail\": \"String - URL to the thumbnail image\",\n        \"video\": {\n          \"link\": \"String - URL to the video\",\n          \"thumbnail\": \"String - URL to the thumbnail image\",\n          \"source\": \"String - Source of the video\",\n          \"date\": \"String - Date of the video\"\n        },\n        // Only for 'list' type\n        \"list\": [\n          {\n            \"title\": \"String - Title of the list item\",\n            \"link\": \"String - Link URL of the list item title\",\n            \"snippet\": \"String - Snippet of the list item\",\n            \"snippet_latex\": \"Array of strings - LaTeX equations in the snippet\",\n            \"reference_indexes\": \"Array of integers - Indexes of the references in the root 'references' field\",\n            \"thumbnail\": \"String - URL to the thumbnail image\",\n            // Nested lists\n            \"list\": [\n              {\n                \"snippet\": \"String - Snippet of the nested list item\",\n                \"reference_indexes\": \"Array of integers - Indexes of the references in the root 'references' field\",\n              },\n              ...\n            ]\n          },\n          ...\n        ],\n        // Only for `table` type\n        \"table\": [\n          [\n            \"String - Table cell snippet\",\n            ...\n          ],\n          ...\n        ],\n        \"detailed\": [\n          [\n            {\n              \"snippet\": \"String - Table cell snippet\",\n              \"snippet_latex\": \"Array of strings - LaTeX equations in the snippet\"\n            },\n            ...\n          ],\n          ...\n        ],\n        \"formatted\": \"Array or Object, depending on the structure of the table - Formatted table data\",\n        // Only for 'expandable' type\n        \"text_blocks\": [\n          // The same structure as the parent 'text_blocks' field\n        ],\n        // Only for 'comparison' type\n        \"product_labels\": \"Array of strings - Labels for the products being compared\",\n        \"comparison\": [\n          {\n            \"feature\": \"String - Feature being compared\",\n            \"values\": [\n              \"String - Value for the first product\",\n              \"String - Value for the second product\"\n            ]\n          },\n          ...\n        ]\n      },\n      ...\n    ],\n    \"thumbnail\": \"String - URL to the thumbnail image\",\n    \"references\": [\n      {\n        \"title\": \"String - Title of the reference\",\n        \"link\": \"String - URL to the reference\",\n        \"snippet\": \"String - Snippet of the reference\",\n        \"source\": \"String - Source of the reference\",\n        \"index\": \"Integer - Index of the reference\"\n      },\n      ...\n    ],\n    \"error\": \"String - Error message if the AI Overview results are not available\",\n  },\n  ...\n}"}
  importantNotes:
    - "Google sometimes requires an additional request to retrieve AI Overview results. See the extra request example and our Google AI Overview API to understand how to handle these cases."
    - "Google can return AI Overview content through a separate request instead of directly in a response. In these cases we return page_token for the associated request and serpapi_link for the corresponding SerpApi search using our Google AI Overview API. The resulting JSON structure is the same as the above examples.The rendered HTML will show \"Can't generate an AI overview right now. Try again later.\" — this is expected behaviour and can be ignored.page_token and serpapi_link will expire within 4 minutes of the search and should be used immediately."
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nBilling Information\n\nChange Plan\n\nEdit Profile\n\nExtra Credits\n\nYour API Metrics\n\nAPI Absolute Numbers\n\nAPI Engines\n\nAPI Response Times\n\nAPI Success Rates\n\nYour Searches\n\nYour Playground\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API"
  suggestedFilename: "ai-overview-api"
---

# Google AI Overview Results API

## 源URL

https://serpapi.com/ai-overview

## 描述

For some searches, Google search results includes an AI Overview block. SerpApi is able to scrape, extract and make sense of this information.

Currently, the AI Overview block is only seen for English searches (hl=en) with a limited range of countries (gl).

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

Google sometimes requires an additional request to retrieve AI Overview results. See the extra request example and our Google AI Overview API to understand how to handle these cases.

Typical result containing headings, paragraphs, lists (with and without title) and a thumbnail.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 注意事项

- Google sometimes requires an additional request to retrieve AI Overview results. See the extra request example and our Google AI Overview API to understand how to handle these cases.
- Google can return AI Overview content through a separate request instead of directly in a response. In these cases we return page_token for the associated request and serpapi_link for the corresponding SerpApi search using our Google AI Overview API. The resulting JSON structure is the same as the above examples.The rendered HTML will show "Can't generate an AI overview right now. Try again later." — this is expected behaviour and can be ignored.page_token and serpapi_link will expire within 4 minutes of the search and should be used immediately.

## 文档正文

For some searches, Google search results includes an AI Overview block. SerpApi is able to scrape, extract and make sense of this information.

Currently, the AI Overview block is only seen for English searches (hl=en) with a limited range of countries (gl).

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

Google sometimes requires an additional request to retrieve AI Overview results. See the extra request example and our Google AI Overview API to understand how to handle these cases.

Typical result containing headings, paragraphs, lists (with and without title) and a thumbnail.

## API 端点

**Method:** `GET`
**Endpoint:** `https://serpapi.com/search`

Api Dashboard

Api Dashboard

Your Account

Billing Information

Change Plan

Edit Profile

Extra Credits

Your API Metrics

API Absolute Numbers

API Engines

API Response Times

API Success Rates

Your Searches

Your Playground

Api Documentation

Api Documentation

Google Search API

AI Overview

About Carousel

Ask AI Mode

Available On

Broaden Searches

Buying Guide

Complementary Results

DMCA Messages

Discover More Places

Discussions and Forums

Episode Guide

Events Results

Find Results On

Google About This Result API

Grammar Check

Immersive Products

Inline Images

Inline People Also Search For

Inline Products

Inline Shopping

Inline Videos

Interactive Diagram

Jobs Results

Knowledge Graph

Latest From

Latest Posts

Menu Highlights

News Results

Nutrition Information

Organic Results

Perspectives

Places Sites

Popular Destinations

Product Result

Product Sites

Questions And Answers

Recipes Results

Refine Search Filters

Refine This Search

Related Brands

Related Categories

Related Questions

Related Searches

Scholarly Articles

Short Videos

Showtimes Results

Spell Check

Sports Results

Things To Know

Top Carousel

Top Insights

Top Stories

Twitter Results

Visual Stories

Google Light Search API

Knowledge Graph

Organic Results

Related Questions

Related Searches

Spell Check

Top Stories

Google AI Mode API

Google AI Overview API

Google Ads Transparency API

Ad Details API

Google Autocomplete API

Google Events API

Google Finance API

Google Finance Markets API

Google Flights API

Airports Results

Autocomplete API

Booking Options

Flights Results

Price Insights

Google Forums API

Google Hotels API

Autocomplete API

Property Details

Reviews API

Google Images API

Images Results

Related Content API
