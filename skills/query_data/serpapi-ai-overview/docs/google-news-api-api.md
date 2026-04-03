---
id: "url-7b0d2093"
type: "api"
title: "Google News API"
url: "https://serpapi.com/google-news-api"
description: "Our Google News API allows you to scrape results from the Google News search page.\n\nThe API endpoint is https://serpapi.com/search?engine=google_news Head to the playground for a live and interactive demo."
source: ""
tags: []
crawl_time: "2026-03-18T09:09:02.254Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google_news"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Example with search query q: Pizza","description":"","requestParams":{"engine":"google_news","q":"pizza","gl":"us","hl":"en","highlight":"news_results"},"responseJson":"https://serpapi.com/search.json?engine=google_news&q=pizza&gl=us&hl=en"}
    - {"title":"Example with Technology as a topic","description":"","requestParams":{"engine":"google_news","gl":"us","hl":"en","topic_token":"CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB","highlight":"news_results"},"responseJson":"https://serpapi.com/search.json?engine=google_news&gl=us&hl=en&topic_token=CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB"}
    - {"title":"Example for a full coverage page","description":"","requestParams":{"engine":"google_news","gl":"us","hl":"en","story_token":"CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pqdU9UWENSRXNnR1puWWJtdzZ5Z0FQAQ","highlight":"news_results"},"responseJson":"https://serpapi.com/search.json?engine=google_news&gl=us&hl=en&story_token=CAAqNggKIjBDQklTSGpvSmMzUnZjbmt0TXpZd1NoRUtEd2pqdU9UWENSRXNnR1puWWJtdzZ5Z0FQAQ"}
    - {"title":"Example for a publications page","description":"","requestParams":{"engine":"google_news","gl":"us","hl":"en","publication_token":"CAAqBwgKMKHL9QowkqbaAg","highlight":"news_results"},"responseJson":"https://serpapi.com/search.json?engine=google_news&gl=us&hl=en&publication_token=CAAqBwgKMKHL9QowkqbaAg"}
    - {"title":"Example for a publications page with Business subsection","description":"","requestParams":{"engine":"google_news","gl":"us","hl":"en","publication_token":"CAAqBwgKMKHL9QowkqbaAg","section_token":"CAQqEAgAKgcICjChy_UKMJKm2gIwxJScBg","highlight":"news_results"},"responseJson":"https://serpapi.com/search.json?engine=google_news&gl=us&hl=en&publication_token=CAAqBwgKMKHL9QowkqbaAg&section_token=CAQqEAgAKgcICjChy_UKMJKm2gIwxJScBg"}
    - {"title":"Example for a front page","description":"","requestParams":{"engine":"google_news","gl":"us","hl":"en","highlight":"news_results"},"responseJson":"https://serpapi.com/search.json?engine=google_news&gl=us&hl=en"}
    - {"title":"Example with Hip-hop as a topic","description":"","requestParams":{"engine":"google_news","gl":"us","hl":"en","topic_token":"CAAqJAgKIh5DQkFTRUFvS0wyMHZNR2RzZERZM01CSUNaVzRvQUFQAQ","highlight":"news_results"},"responseJson":"https://serpapi.com/search.json?engine=google_news&gl=us&hl=en&topic_token=CAAqJAgKIh5DQkFTRUFvS0wyMHZNR2RzZERZM01CSUNaVzRvQUFQAQ"}
    - {"title":"Example with related topics","description":"","requestParams":{"engine":"google_news","gl":"us","hl":"en","q":"elon musk","highlight":"related_topics"},"responseJson":"https://serpapi.com/search.json?engine=google_news&gl=us&hl=en&q=elon+musk"}
    - {"title":"Example with related topics and publication","description":"","requestParams":{"engine":"google_news","gl":"us","hl":"en","q":"pizza","highlight":"related_topics"},"responseJson":"https://serpapi.com/search.json?engine=google_news&gl=us&hl=en&q=pizza"}
    - {"title":"Example with  kgmid: /m/02_286 (Location: New York City)","description":"","requestParams":{"engine":"google_news","kgmid":"/m/02_286","gl":"us","hl":"en","highlight":"news_results"},"responseJson":"https://serpapi.com/search.json?engine=google_news&kgmid=/m/02_286&gl=us&hl=en"}
    - {"title":"Example with  kgmid: /m/0524b41 (Topic: Game of Thrones)","description":"","requestParams":{"engine":"google_news","kgmid":"/m/0524b41","gl":"us","hl":"en","highlight":"news_results"},"responseJson":"https://serpapi.com/search.json?engine=google_news&kgmid=/m/0524b41&gl=us&hl=en"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  \"top_stories_link\": {\n    \"topic_token\": \"String - Token used for retrieving news results from a specific topic\",\n    \"serpapi_link\": \"String - URL to the SerpApi search\"\n  },\n  \"title\": \"String - Page title\",\n  \"news_results\": [\n    {\n      \"position\": \"Integer - News result position\",\n      \"title\": \"String - News result title\",\n      \"snippet\": \"String - News result snippet\",\n      \"source\": {\n        \"title\": \"String - Title of the source\",\n        \"name\": \"String - Name of the source\",\n        \"icon\": \"String - Link to the source icon\",\n        \"authors\": [\n          \"String - Name of the author\"\n        ]\n      },\n      \"author\": {\n        \"thumbnail\": \"String - Link to the author's thumbnail\",\n        \"name\": \"String - Name of the author\",\n        \"handle\": \"String - X (Twitter) username\"\n      },\n      \"link\": \"String - News result link\",\n      \"thumbnail\": \"String - News result thumbnail link\",\n      \"thumbnail_small\": \"String - News result low-resolution thumbnail link\",\n      \"type\": \"String - News result type (e.g., 'Opinion', 'Local coverage')\",\n      \"video\": \"Boolean - Returns 'true' if the result is a video\",\n      \"topic_token\": \"String - Token used for retrieving news results from a specific topic\",\n      \"story_token\": \"String - Token used for retrieving news results from a specific story\",\n      \"serpapi_link\": \"String - URL to the SerpApi search\",\n      \"date\": \"String - Date when the news result was published (deprecated)\",\n      \"iso_date\": \"String - ISO 8601 Date when the news result was published\",\n      \"related_topics\": [\n        {\n          \"position\": \"Integer - Related topic position\",\n          \"name\": \"String - Name of the related topic\",\n          \"topic_token\": \"String - Token used for retrieving news results from a specific topic\",\n          \"serpapi_link\": \"String - URL to the SerpApi search\"\n        },\n        ...\n      ]\n      \"highlight\": {\n        // Can contain the same data as 'news_results' except 'related_topics', `stories` and 'highlight'\n      },\n      \"stories\": [\n        {\n          // Can contain the same data as 'news_results' except 'related_topics', `highlight` and 'stories'\n        },\n        ...\n      ],\n    },\n    ...\n  ],\n  \"menu_links\": [\n    {\n      \"title\": \"String - Text of the menu item\",\n      \"topic_token\": \"String - Token used for retrieving news results from a specific topic\",\n      \"serpapi_link\": \"String - URL to the SerpApi search\"\n    },\n    ...\n  ],\n  \"sub_menu_links\": [\n    {\n      \"title\": \"String - Text of the sub-menu item\",\n      \"section_token\": \"String - Token used for retrieving news results from a specific section\",\n      \"topic_token\": \"String - Token used for retrieving news results from a specific topic\",\n      \"serpapi_link\": \"String - URL to the SerpApi search\"\n    },\n    ...\n  ],\n  \"related_topics\": [\n    {\n      \"title\": \"String - Name of the related topic\",\n      \"topic_token\": \"String - Token used for retrieving news results from a specific topic\",\n      \"serpapi_link\": \"String - URL to the SerpApi search\",\n      \"thumbnail\": \"String - Link to the thumbnail associated with the related topic\"\n    },\n    ...\n  ],\n  \"related_publications\": [\n    {\n      \"title\": \"String - Name of the related publication\",\n      \"publication_token\": \"String - Token used for retrieving news results from a specific publication\",\n      \"serpapi_link\": \"String - URL to the SerpApi search\",\n      \"thumbnail\": \"String - Link to the thumbnail associated with the related publication\"\n    },\n    ...\n  ]\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nBilling Information\n\nChange Plan\n\nEdit Profile\n\nExtra Credits\n\nYour API Metrics\n\nAPI Absolute Numbers\n\nAPI Engines\n\nAPI Response Times\n\nAPI Success Rates\n\nYour Searches\n\nYour Playground\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API"
  suggestedFilename: "google-news-api-api"
---

# Google News API

## 源URL

https://serpapi.com/google-news-api

## 描述

Our Google News API allows you to scrape results from the Google News search page.

The API endpoint is https://serpapi.com/search?engine=google_news Head to the playground for a live and interactive demo.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Google News API allows you to scrape results from the Google News search page.

The API endpoint is https://serpapi.com/search?engine=google_news Head to the playground for a live and interactive demo.

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
