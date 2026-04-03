---
id: "url-3837b7c7"
type: "api"
title: "Google Related Searches API"
url: "https://serpapi.com/related-searches"
description: "Google searches that may be related to other search terms are presented with related search boxes or a related searches section, typically at the bottom of the search page.\n\nThe API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.\n\nUsually in mobile search, Google will display People also search for section along with Related searches. They are exactly the same content, thus we have parsed these sections into related_searches. To differentiate the section, we have added block_position to the result. In this case, it will be 1 for People also search for and 2 for Related searches.\n\nFor some searches like restaurants, Google will might show restaurants with rating and reviews.\n\nFor some searches, Google will might show multiple related searches with items queries."
source: ""
tags: []
crawl_time: "2026-03-18T11:05:02.656Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Related Searches for Coffee","description":"","requestParams":{"q":"Coffee","hl":"en","gl":"us","highlight":"related_searches"},"responseJson":"https://serpapi.com/search.json?q=Coffee&hl=en&gl=us"}
    - {"title":"Related Searches with items results for Doctor Strange","description":"","requestParams":{"q":"Doctor Strange","hl":"en","gl":"us","highlight":"related_searches"},"responseJson":"https://serpapi.com/search.json?q=Doctor+Strange&hl=en&gl=us"}
    - {"title":"Related Searches with items results for Apple","description":"","requestParams":{"q":"Apple","hl":"en","gl":"us","highlight":"related_searches"},"responseJson":"https://serpapi.com/search.json?q=Apple&hl=en&gl=us"}
    - {"title":"Related Searches for ChatGPT on mobile","description":"Usually in mobile search, Google will display People also search for section along with Related searches. They are exactly the same content, thus we have parsed these sections into related_searches. To differentiate the section, we have added block_position to the result. In this case, it will be 1 for People also search for and 2 for Related searches.","requestParams":{"q":"ChatGPT","hl":"en","gl":"us","device":"mobile","highlight":"related_searches"},"responseJson":"https://serpapi.com/search.json?q=ChatGPT&hl=en&gl=us&device=mobile"}
    - {"title":"Related Searches for Royal Pizza Tulcea on mobile","description":"For some searches like restaurants, Google will might show restaurants with rating and reviews.","requestParams":{"q":"Royal Pizza Tulcea","device":"mobile","highlight":"related_searches"},"responseJson":"https://serpapi.com/search.json?q=Royal+Pizza+Tulcea&device=mobile"}
    - {"title":"Related Searches for Oriocenter on mobile","description":"For some searches, Google will might show multiple related searches with items queries.","requestParams":{"q":"Oriocenter","device":"mobile","highlight":"related_searches"},"responseJson":"https://serpapi.com/search.json?q=Oriocenter&device=mobile"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"related_searches\": [\n    {\n      \"block_position\": \"Integer - Index of related search container\",\n      \"query\": \"String - Query of the related search\",\n      \"image\": \"String - Image of the related search\",\n      \"link\":  \"String - Link to the Google search\",\n      \"serpapi_link\":  \"String - SerpApi Link of the Google search\",\n      \"items\": [\n        {\n          \"name\": \"String - Name of the item\",\n          \"image\": \"String - Image of the item\",\n          \"reviews\": \"Integer - Number of reviews. Available for some searches, e.g. restaurants\",\n          \"rating\": \"Float - Rating of the item. Available for some searches, e.g. restaurants\",\n          \"duration\": \"String - Duration of a video\",\n          \"extensions\": \"Array - Extensions of the item\",\n          \"link\":  \"String - Link to the Google search\",\n          \"serpapi_link\":  \"String - SerpApi Link of the Google search\",\n        }\n      ],\n    },\n    ...\n  ],\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "related-searches-api"
---

# Google Related Searches API

## 源URL

https://serpapi.com/related-searches

## 描述

Google searches that may be related to other search terms are presented with related search boxes or a related searches section, typically at the bottom of the search page.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

Usually in mobile search, Google will display People also search for section along with Related searches. They are exactly the same content, thus we have parsed these sections into related_searches. To differentiate the section, we have added block_position to the result. In this case, it will be 1 for People also search for and 2 for Related searches.

For some searches like restaurants, Google will might show restaurants with rating and reviews.

For some searches, Google will might show multiple related searches with items queries.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Google searches that may be related to other search terms are presented with related search boxes or a related searches section, typically at the bottom of the search page.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

Usually in mobile search, Google will display People also search for section along with Related searches. They are exactly the same content, thus we have parsed these sections into related_searches. To differentiate the section, we have added block_position to the result. In this case, it will be 1 for People also search for and 2 for Related searches.

For some searches like restaurants, Google will might show restaurants with rating and reviews.

For some searches, Google will might show multiple related searches with items queries.

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
