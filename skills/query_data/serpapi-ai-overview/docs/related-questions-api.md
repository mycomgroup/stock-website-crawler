---
id: "url-5d089dca"
type: "api"
title: "Google Related Questions API"
url: "https://serpapi.com/related-questions"
description: "For some searches, Google search includes a related questions \"People also ask\" block. SerpApi is able to scrape, extract, and make sense of this information. We also have the Google Related Questions API which allows you to retrieve more results. It mimics the behavior that you get on the live Google results page when you click a question and more questions get loaded.\n\nThe API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.\n\nFor some searches, some related questions are ansered by an AI Overview. SerpApi is able to make sense of the AI Overview and extract the relevant information."
source: ""
tags: []
crawl_time: "2026-03-18T15:17:24.798Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Results for: Pu Erh Tea","description":"","requestParams":{"q":"Pu Erh Tea","location":"United States","highlight":"related_questions"},"responseJson":"https://serpapi.com/search.json?q=Pu+Erh+Tea&location=United+States"}
    - {"title":"Results for: Richard Feynman's Family","description":"","requestParams":{"q":"Richard Feynman's Family","highlight":"related_questions"},"responseJson":"https://serpapi.com/search.json?q=Richard+Feynman's+Family"}
    - {"title":"Results for: Who is Michael Faraday?","description":"","requestParams":{"q":"Who is Michael Faraday?","highlight":"related_questions"},"responseJson":"https://serpapi.com/search.json?q=Who+is+Michael+Faraday?"}
    - {"title":"Example table results for: Athlete height","description":"","requestParams":{"q":"Athlete height","highlight":"related_questions"},"responseJson":"https://serpapi.com/search.json?q=Athlete+height"}
    - {"title":"Example AI Overview results for: China","description":"For some searches, some related questions are ansered by an AI Overview. SerpApi is able to make sense of the AI Overview and extract the relevant information.","requestParams":{"q":"China","highlight":"related_questions"},"responseJson":"https://serpapi.com/search.json?q=China"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"related_questions\": [\n    {\n      \"question\": \"String - Displayed question\",\n      \"type\": \"String - Type of the answer. Can be 'featured_snippet', 'ai_overview'\",\n      \"next_page_token\": \"String - Token used for retrieving more related questions\",\n      \"serpapi_link\": \"String - API to get more related questions\"\n      // Only for 'featured_snippet' type\n      \"snippet\": \"String - Snippet of the answer\",\n      \"table\": \"Array - Answer to the question in table format\",\n      \"title\":  \"String - Title of the answer\",\n      \"date\":  \"String - Date of the answer\",\n      \"info\": \"String - Information about the answer\",\n      \"link\": \"String - Link of the answer\",\n      \"source_logo\": \"String - Link of the website logo (favicon)\",\n      // Only for 'ai_overview' type\n      \"text_blocks\": [\n        {\n          \"type\": \"String - Type of the text block. Can be 'paragraph', 'list', 'expandable', 'table'\",\n          \"snippet\": \"String - Snippet of the text block\",\n          \"snippet_highlighted_words\": \"Array of strings - Highlighted words in the snippet\",\n          \"reference_indexes\": \"Array of integers - Indexes of the references in the root 'references' field\",\n          \"thumbnail\": \"String - URL to the thumbnail image\",\n          \"video\": {\n            \"link\": \"String - URL to the video\",\n            \"thumbnail\": \"String - URL to the thumbnail image\",\n            \"source\": \"String - Source of the video\",\n            \"date\": \"String - Date of the video\"\n          },\n          // Only for 'list' type\n          \"list\": [\n            {\n              \"title\": \"String - Title of the list item\",\n              \"snippet\": \"String - Snippet of the list item\",\n              \"reference_indexes\": \"Array of integers - Indexes of the references in the root 'references' field\",\n              \"thumbnail\": \"String - URL to the thumbnail image\",\n              // Nested lists\n              \"list\": [\n                {\n                  \"snippet\": \"String - Snippet of the nested list item\",\n                  \"reference_indexes\": \"Array of integers - Indexes of the references in the root 'references' field\",\n                },\n                ...\n              ]\n            },\n            ...\n          ],\n          // Only for `table` type\n          \"table\": [\n            [\n              \"String - Table cell\",\n              ...\n            ],\n            ...\n          ],\n          \"formatted\": \"Array or Object, depending on the structure of the table - Formatted table data\",\n          // Only for 'expandable' type\n          \"text_blocks\": [\n            // The same structure as the parent 'text_blocks' field\n          ]\n        },\n        ...\n      ],\n      \"thumbnail\": \"String - Link of the thumbnail\",\n      \"references\": [\n        {\n          \"title\": \"String - Title of the reference\",\n          \"link\": \"String - URL to the reference\",\n          \"snippet\": \"String - Snippet of the reference\",\n          \"source\": \"String - Source of the reference\",\n          \"index\": \"Integer - Index of the reference\"\n        },\n        ...\n      ],\n    },\n  ],\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "related-questions-api"
---

# Google Related Questions API

## 源URL

https://serpapi.com/related-questions

## 描述

For some searches, Google search includes a related questions "People also ask" block. SerpApi is able to scrape, extract, and make sense of this information. We also have the Google Related Questions API which allows you to retrieve more results. It mimics the behavior that you get on the live Google results page when you click a question and more questions get loaded.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

For some searches, some related questions are ansered by an AI Overview. SerpApi is able to make sense of the AI Overview and extract the relevant information.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

For some searches, Google search includes a related questions "People also ask" block. SerpApi is able to scrape, extract, and make sense of this information. We also have the Google Related Questions API which allows you to retrieve more results. It mimics the behavior that you get on the live Google results page when you click a question and more questions get loaded.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

For some searches, some related questions are ansered by an AI Overview. SerpApi is able to make sense of the AI Overview and extract the relevant information.

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
