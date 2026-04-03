---
id: "url-12b04af3"
type: "api"
title: "Bing Copilot API"
url: "https://serpapi.com/bing-copilot-api"
description: "Our Bing Copilot API allows you to scrape results from the Bing Copilot page.\n\nThe API endpoint is https://serpapi.com/search?engine=bing_copilot Head to the playground for a live and interactive demo.\n\nBing Copilot API does not support explicit language parameter. However, the return language could be specified inside the query. Example query: Coffee, return results in Korean.\n\nIn most cases, Copilot complies with the requested language. However, given that it is an AI model, the final language is not guaranteed."
source: ""
tags: []
crawl_time: "2026-03-18T11:58:17.982Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Example for table in text_blocks","description":"","requestParams":{"engine":"bing_copilot","q":"GDP by country, table","highlight":"text_blocks"},"responseJson":"https://serpapi.com/search.json?engine=bing_copilot&q=GDP+by+country,+table"}
    - {"title":"Example for code_block in text_blocks","description":"","requestParams":{"engine":"bing_copilot","q":"python bubble sort example","highlight":"text_blocks"},"responseJson":"https://serpapi.com/search.json?engine=bing_copilot&q=python+bubble+sort+example"}
    - {"title":"Example for nested lists in text_blocks","description":"","requestParams":{"engine":"bing_copilot","q":"how do I calculate the velocity of a train ... nested list","highlight":"text_blocks"},"responseJson":"https://serpapi.com/search.json?engine=bing_copilot&q=how+do+I+calculate+the+velocity+of+a+train+...+nested+list"}
    - {"title":"Example for header_video","description":"","requestParams":{"engine":"bing_copilot","q":"how to tie a tie","highlight":"header_video"},"responseJson":"https://serpapi.com/search.json?engine=bing_copilot&q=how+to+tie+a+tie"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"header\": \"String - main answer heading\",\n  \"header_video\": {\n    \"title\": \"String - Title of the video\",\n    \"link\": \"String - URL to the video\",\n    \"duration\": \"String - Duration of the video\",\n    \"thumbnail\": \"String - URL to the video thumbnail\",\n    \"source\": \"String - Source of the video (e.g., YouTube)\",\n    \"channel\": \"String - Channel name\",\n    \"views\": \"String - Number of views\",\n    \"published\": \"String - Published date\"\n  },\n  \"images_link\": \"String (URL) - link to Bing Images for the query\",\n  \"videos_link\": \"String (URL) - link to Bing Videos for the query\",\n  \"text_blocks\": [\n    {\n      \"type\": \"paragraph\",\n      \"snippet\": \"String\",\n      \"snippet_links\": [\n        {\n          \"text\": \"String\",\n          \"link\": \"String\"\n        }\n      ],\n      \"snippet_highlighted_words\": \"Array - Array of highlighted words\",\n      \"reference_indexes\": \"Array - Array of reference indexes\"\n    },\n    {\n      \"type\": \"heading\", \n      \"level\": \"Integer (1..6)\",\n      \"snippet\": \"String\",\n      \"snippet_links\": \"Array\",\n      \"snippet_highlighted_words\": \"Array - Array of highlighted words\",\n      \"reference_indexes\": \"Array - Array of reference indexes\"\n    },\n    {\n      \"type\": \"list\",\n      \"list\": [\n        {\n          \"snippet\": \"String\", \n          \"snippet_links\": \"Array\",\n          \"snippet_highlighted_words\": \"Array - Array of highlighted words\",\n          \"reference_indexes\": \"Array - Array of reference indexes\",\n        }\n      ]\n    },\n    {\n      \"type\": \"code_block\",\n      \"code\": \"String\",\n      \"language\": \"String - Optional language\"\n    },\n    {\n      \"type\": \"table\",\n      \"headers\": \"Array - Array of header strings\",\n      \"table\": \"Array - Array of table rows (each row is an array of strings)\"\n      \"formatted\": \"Array\"\n    }\n  ],\n  \"references\": [\n    {\n      \"index\": \"Integer (zero-based)\",\n      \"title\": \"String - Optional title\",\n      \"link\": \"String - URL to the reference\",\n      \"snippet\": \"String - Optional snippet text\",\n      \"source\": \"String - Optional source\"\n    }\n  ],\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "bing-copilot-api-api"
---

# Bing Copilot API

## 源URL

https://serpapi.com/bing-copilot-api

## 描述

Our Bing Copilot API allows you to scrape results from the Bing Copilot page.

The API endpoint is https://serpapi.com/search?engine=bing_copilot Head to the playground for a live and interactive demo.

Bing Copilot API does not support explicit language parameter. However, the return language could be specified inside the query. Example query: Coffee, return results in Korean.

In most cases, Copilot complies with the requested language. However, given that it is an AI model, the final language is not guaranteed.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Bing Copilot API allows you to scrape results from the Bing Copilot page.

The API endpoint is https://serpapi.com/search?engine=bing_copilot Head to the playground for a live and interactive demo.

Bing Copilot API does not support explicit language parameter. However, the return language could be specified inside the query. Example query: Coffee, return results in Korean.

In most cases, Copilot complies with the requested language. However, given that it is an AI model, the final language is not guaranteed.

## API 端点

**Method:** `GET`
**Endpoint:** `https://serpapi.com/search`

Api Dashboard

Api Dashboard

Your Account

Edit Profile

Extra Credits

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

Related Searches

Shopping Results

Suggested Searches

Google Images Light API

Google Immersive Product API

Google Jobs API

Listing API

Google Lens API

About This Image
