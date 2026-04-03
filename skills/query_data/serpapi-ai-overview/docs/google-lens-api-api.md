---
id: "url-6410d6c2"
type: "api"
title: "Google Lens API"
url: "https://serpapi.com/google-lens-api"
description: "Our Google Lens API allows you to scrape results from the Google Lens page when performing an image search. The results related to the image could contain visual matches and other data.\n\nThe API endpoint is https://serpapi.com/search?engine=google_lens Head to the playground for a live and interactive demo.\n\nWe have introduced new search capability to Google Lens API. You can now include the q parameter along with the usual image search parameters to refine the search results.\n\nIn addition, we have discontinued the page_token parameter and replaced it with the new type parameter. This change makes the API more intuitive and easier to use when performing searches for Product, Exact Matches, and Visual Matches.\n\nSearches made with country parameter return results with more localized data. For example, country=jp will mostly return results with ¥ (Japanese Yen)."
source: ""
tags: []
crawl_time: "2026-03-18T09:08:46.459Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Example with url: https://i.imgur.com/HBrB8p0.png","description":"","requestParams":{"engine":"google_lens","url":"https://i.imgur.com/HBrB8p0.png","highlight":"visual_matches"},"responseJson":"https://serpapi.com/search.json?engine=google_lens&url=https://i.imgur.com/HBrB8p0.png"}
    - {"title":"Example with country: jp (Japan)","description":"Searches made with country parameter return results with more localized data. For example, country=jp will mostly return results with ¥ (Japanese Yen).","requestParams":{"engine":"google_lens","hl":"en","country":"jp","url":"https://s3.zoommer.ge/zoommer-images/thumbs/0170510_apple-macbook-pro-13-inch-2022-mneh3lla-m2-chip-8gb256gb-ssd-space-grey-apple-m25nm-apple-8-core-gpu_550.jpeg","highlight":"visual_matches"},"responseJson":"https://serpapi.com/search.json?engine=google_lens&hl=en&country=jp&url=https://s3.zoommer.ge/zoommer-images/thumbs/0170510_apple-macbook-pro-13-inch-2022-mneh3lla-m2-chip-8gb256gb-ssd-space-grey-apple-m25nm-apple-8-core-gpu_550.jpeg"}
    - {"title":"Example with q: Red","description":"The q parameter can be used along with the image search to refine the search results.","requestParams":{"engine":"google_lens","url":"https://www.decorilla.com/online-decorating/wp-content/uploads/2022/01/Biophilic-interior-design-by-Wanda-P.jpg","q":"Red","highlight":"visual_matches"},"responseJson":"https://serpapi.com/search.json?engine=google_lens&url=https://www.decorilla.com/online-decorating/wp-content/uploads/2022/01/Biophilic-interior-design-by-Wanda-P.jpg&q=Red"}
    - {"title":"Example with ai_overview","description":"Some searches may include AI Overview content accessible through a separate request. In these cases we return page_token for the associated request and serpapi_link for the corresponding SerpApi search using our Google AI Overview API. The rendered HTML will show \"Searching...\" — this is expected behaviour and can be ignored. page_token and serpapi_link will expire within 4 minutes of the search and should be used immediately..","requestParams":{"engine":"google_lens","url":"https://i.imgur.com/HBrB8p0.png","q":"who is him?","highlight":"ai_overview"},"responseJson":"https://serpapi.com/search.json?engine=google_lens&url=https://i.imgur.com/HBrB8p0.png&q=who+is+him?"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"ai_overview\": {\n    \"page_token\": \"String - Token for the AI Overview block\",\n    \"serpapi_link\": \"String - URL to the corresponding SerpApi search\",\n  },\n  \"visual_matches\": [\n    {\n      \"position\": \"Integer - Position of the image\",\n      \"title\": \"String - Title of the image\",\n      \"link\": \"String - Source URL of the website containing the image\",\n      \"source\": \"String - Displayed URL of the website containing the image\",\n      \"source_icon\": \"String - Icon URL of the source website containing the image\",\n      \"rating\": \"Float - Rating of the item in the image\",\n      \"reviews\": \"Integer - Number of reviews of the item in the image\",\n      \"price\": {\n        \"value\": \"String - Price of the item in the image\",\n        \"extracted_value\": \"Float - Extracted price of the item in the image\",\n        \"currency\": \"String - Price currency of the item in the image\"\n      },\n      \"in_stock\": \"Boolean - Availability of the item in the image\",\n      \"condition\": \"String - Condition of the item in the image\",\n      \"thumbnail\": \"String - URL to the image thumbnail\",\n      \"thumbnail_width\": \"Integer - width of the image thumbnail\",\n      \"thumbnail_height\": \"Integer - height of the image thumbnail\",\n      \"image\": \"String - URL to the full image\",\n      \"image_width\": \"Integer - width of the full image\",\n      \"image_height\": \"Integer - height of the full image\",\n      \"exact_matches\": \"Boolean - Indicates if there are exact matches\",\n      \"serpapi_exact_matches_link\": \"String - URL to the SerpApi search for exact matches\"\n    },\n    ...\n  ],\n  \"related_content\": [\n    {\n      \"query\": \"String - Related image query\",\n      \"link\": \"String - URL to the Google search\",\n      \"thumbnail\": \"String - URL to the image thumbnail\",\n      \"serpapi_link\": \"String - URL to the SerpApi search\"\n    },\n    ...\n  ]\n}"}
  importantNotes:
    - "Some searches may include AI Overview content accessible through a separate request. In these cases we return page_token for the associated request and serpapi_link for the corresponding SerpApi search using our Google AI Overview API.The rendered HTML will show \"Searching...\" — this is expected behaviour and can be ignored.page_token and serpapi_link will expire within 4 minutes of the search and should be used immediately.."
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nBilling Information\n\nChange Plan\n\nEdit Profile\n\nExtra Credits\n\nYour API Metrics\n\nAPI Absolute Numbers\n\nAPI Engines\n\nAPI Response Times\n\nAPI Success Rates\n\nYour Searches\n\nYour Playground\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API"
  suggestedFilename: "google-lens-api-api"
---

# Google Lens API

## 源URL

https://serpapi.com/google-lens-api

## 描述

Our Google Lens API allows you to scrape results from the Google Lens page when performing an image search. The results related to the image could contain visual matches and other data.

The API endpoint is https://serpapi.com/search?engine=google_lens Head to the playground for a live and interactive demo.

We have introduced new search capability to Google Lens API. You can now include the q parameter along with the usual image search parameters to refine the search results.

In addition, we have discontinued the page_token parameter and replaced it with the new type parameter. This change makes the API more intuitive and easier to use when performing searches for Product, Exact Matches, and Visual Matches.

Searches made with country parameter return results with more localized data. For example, country=jp will mostly return results with ¥ (Japanese Yen).

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 注意事项

- Some searches may include AI Overview content accessible through a separate request. In these cases we return page_token for the associated request and serpapi_link for the corresponding SerpApi search using our Google AI Overview API.The rendered HTML will show "Searching..." — this is expected behaviour and can be ignored.page_token and serpapi_link will expire within 4 minutes of the search and should be used immediately..

## 文档正文

Our Google Lens API allows you to scrape results from the Google Lens page when performing an image search. The results related to the image could contain visual matches and other data.

The API endpoint is https://serpapi.com/search?engine=google_lens Head to the playground for a live and interactive demo.

We have introduced new search capability to Google Lens API. You can now include the q parameter along with the usual image search parameters to refine the search results.

In addition, we have discontinued the page_token parameter and replaced it with the new type parameter. This change makes the API more intuitive and easier to use when performing searches for Product, Exact Matches, and Visual Matches.

Searches made with country parameter return results with more localized data. For example, country=jp will mostly return results with ¥ (Japanese Yen).

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
