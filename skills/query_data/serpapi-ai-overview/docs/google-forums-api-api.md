---
id: "url-1adc0b0e"
type: "api"
title: "Google Forums API"
url: "https://serpapi.com/google-forums-api"
description: "Our Google Forums API allows you to scrape forum results from Google Search \"Forums\" tab.\n\nThe API endpoint is https://serpapi.com/search?engine=google_forums Head to the playground for a live and interactive demo."
source: ""
tags: []
crawl_time: "2026-03-18T15:19:52.202Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Google Forums organic results for q: what is the best programming language","description":"","requestParams":{"engine":"google_forums","q":"what is the best programming language","hl":"en","gl":"us","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=google_forums&q=what+is+the+best+programming+language&hl=en&gl=us"}
    - {"title":"Google Forums organic results for q: what is the best programming language on device: mobile","description":"","requestParams":{"engine":"google_forums","q":"what is the best programming language","device":"mobile","hl":"en","gl":"us","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=google_forums&q=what+is+the+best+programming+language&device=mobile&hl=en&gl=us"}
    - {"title":"Google Forums 'Related Searches' results","description":"","requestParams":{"engine":"google_forums","q":"how to brew the best coffee","hl":"en","gl":"us","highlight":"related_searches"},"responseJson":"https://serpapi.com/search.json?engine=google_forums&q=how+to+brew+the+best+coffee&hl=en&gl=us"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"organic_results\": [\n    {\n      \"position\": \"Integer - Position of the organic result on the search page\",\n      \"title\": \"String - Title of the organic result\",\n      \"link\": \"String - Link of the organic result\",\n      \"redirect_link\": \"String - Redirect link of the organic result\",\n      \"displayed_link\": \"String - Displayed link of the organic result\",\n      \"displayed_meta\": \"String - Displayed meta content of the organic result\",\n      \"thumbnail\": \"String - Thumbnail of the organic result\",\n      \"date\": \"String - Date of the organic result\",\n      \"favicon\": \"String - Favicon of the organic result\",\n      \"snippet\": \"String - Snippet of the organic result\",\n      \"snippet_highlighted_words\": [\n        \"String - Snippet highlighted word of the organic result\",\n      ],\n      \"sitelinks\": {\n        \"expanded\": [\n          {\n            \"title\": \"String - Title of the expanded sitelink\",\n            \"link\": \"String - Link of the expanded sitelink\",\n            \"snippet\": \"String - Snippet of the expanded sitelink\"\n          },\n        ],\n        \"list\": [\n          {\n            \"title\": \"String - Title of the list sitelink\",\n            \"link\": \"String - Link of the list sitelink\",\n            \"snippet\": \"String - Snippet of the list sitelink\"\n          },\n        ]\n      },\n      \"about_this_result\": {\n        \"source\": {\n          \"icon\": \"String - Icon of the about_this_result of the organic result\"\n        },\n      },\n      \"source\": \"String - Source of the organic result\",\n      \"answers\": [\n        {\n          \"link\": \"String - Link of the answer\",\n          \"answer\": \"String - Answer of the answer\",\n          \"top_answer\": \"Boolean - Is the top answer\",\n          \"votes\": \"Integer - Votes of the answer\"\n        }\n      ],\n    }\n  ],\n  \"related_searches\": [\n    {\n      \"block_position\": \"Integer - Index of related search container\",\n      \"query\": \"String - Query of the related search\",\n      \"link\":  \"String - Link to the Google Forums search\",\n      \"serpapi_link\":  \"String - SerpApi Link of the Google Forums search\",\n    },\n  ],,\n  \"serpapi_pagination\": {\n    \"current\": \"Integer - Current page number\",\n    \"next\": \"String - Link to the query for the next SerpApi Google Forums results page\",\n    \"previous\": \"String - Link to the query for the previous SerpApi Google Forums results page\",\n  }\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "google-forums-api-api"
---

# Google Forums API

## 源URL

https://serpapi.com/google-forums-api

## 描述

Our Google Forums API allows you to scrape forum results from Google Search "Forums" tab.

The API endpoint is https://serpapi.com/search?engine=google_forums Head to the playground for a live and interactive demo.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Google Forums API allows you to scrape forum results from Google Search "Forums" tab.

The API endpoint is https://serpapi.com/search?engine=google_forums Head to the playground for a live and interactive demo.

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
