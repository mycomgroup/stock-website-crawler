---
id: "url-69fd2f7c"
type: "api"
title: "Google Product Result API"
url: "https://serpapi.com/product-result"
description: "For some products (depending on your location), Google search will include the \"Product Result\" block, typically on the right side. SerpApi is able to extract and make sense of this information.\n\nThe API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.\n\nThese results are retrieved from the modal that appears after the \"Details\" or \"More details\" button is clicked."
source: ""
tags: []
crawl_time: "2026-03-18T07:12:03.923Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Results for: dyson v8","description":"","requestParams":{"q":"dyson v8","highlight":"product_result","device":"mobile"},"responseJson":"https://serpapi.com/search.json?q=dyson+v8&device=mobile"}
    - {"title":"Results for: Features (Details modal)","description":"These results are retrieved from the modal that appears after the \"Details\" or \"More details\" button is clicked.","requestParams":{"q":"AW3423DW","highlight":"product_result.features","gl":"us","hl":"en"},"responseJson":"https://serpapi.com/search.json?q=AW3423DW&gl=us&hl=en"}
    - {"title":"Results for: video results on mobile","description":"","requestParams":{"q":"iphone 11 pro","device":"mobile","highlight":"product_result.videos"},"responseJson":"https://serpapi.com/search.json?q=iphone+11+pro&device=mobile"}
    - {"title":"Results with installments and ratings","description":"","requestParams":{"q":"iphone 14","device":"desktop","highlight":"product_result"},"responseJson":"https://serpapi.com/search.json?q=iphone+14&device=desktop"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"product_result\": {\n    \"title\": \"String - Product title\",\n    \"reviews\": \"Integer - Number of reviews\",\n    \"rating\": \"Float - Rating of the product\",\n    \"typical_price\": \"String - Typical price of the product\",\n    \"pricing\": [\n      {\n        \"price\": \"String - Price of the product\",\n        \"extracted_price\": \"Float - Extracted price of the product\",\n        \"original_price\": \"String - Original price of the product\",\n        \"extracted_original_price\": \"Float - Extracted original price of the product\",\n        \"installments\": \"String - Installments information of the product\",\n        \"finance_option\": \"String - Finance option of the product\",\n        \"name\": \"String - Name of the seller\",\n        \"link\": \"String - Link to the product\",\n        \"description\": \"String - Description of the product\",\n        \"details\": \"String - Details of the product\",\n        \"thumbnail\": \"String - Thumbnail of the seller\",\n        \"buying_options\": \"Array - Buying options of the product. E.g. 'Free shipping', 'In stock'\",\n        \"tag\": \"String - Tag of the product. E.g. 'Sale', 'Best Seller'\",\n        \"badge\": \"String - Badge of the product. E.g. 'Trusted Store'\",\n        \"rating\": \"String - Rating of the product (e.g. '4.5/5')\",\n        \"extracted_rating\": \"Float - Extracted rating of the product (e.g. 4.5)\"\n      },\n      ...\n    ],\n    \"manufacturer\": {\n      \"name\": \"String - Name of the manufacturer\",\n      \"link\": \"String - Link to the manufacturer\"\n    },\n    \"description\": \"String - Description of the product\",\n    \"features\": {\n      \"Name of the feature\": \"Value of the feature\",\n    },\n    \"thumbnails\": \"Array - URL to the thumbnail\",\n    \"reviews_results\": {\n      \"user_reviews\": {\n        \"ratings\": [\n          {\n            \"stars\": \"Integer - Number of stars\",\n            \"amount\": \"String - Percentage of reviews\"\n          },\n        ],\n        \"popular_questions\": \"Array - Popular questions\",\n        \"review\": [\n          {\n            \"date\": \"String - Date of the review\",\n            \"rating\": \"Integer - Number of stars\",\n            \"title\": \"String - Title of the review\",\n            \"user\": \"String - Name of the user\",\n            \"source\": \"String - Source of the review\",\n            \"snippet\": \"String - Snippet of the review\"\n          }\n        ]\n      }\n    },\n    \"editorial_reviews\": [\n      {\n        \"title\": \"String - Title of the editorial review\",\n        \"rating\": \"Float - Rating of the editorial review\",\n        \"link\": \"String - Link to the editorial review\",\n        \"snippet\": \"String - Snippet of the editorial review\",\n        \"thumbnail\": \"String - Thumbnail of the editorial review\"\n      },\n      ...\n    ],\n    \"critic_ratings\": {\n      \"link\": \"String - Link to the critic rating\",\n      \"name\": \"String - Name of the critic rating\",\n      \"rating\": \"Float - Rating of the critic rating\"\n    },\n    \"videos\": {\n      \"title\": \"String - Title of the video\",\n      \"link\": \"String - Link to the video\",\n      \"thumbnail\": \"String - Thumbnail of the video\",\n      \"channel\": \"String - Channel of the video\",\n      \"date\": \"String - Date of the video\",\n      \"duration\": \"String - Duration of the video\"\n    },\n  },\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "product-result-api"
---

# Google Product Result API

## 源URL

https://serpapi.com/product-result

## 描述

For some products (depending on your location), Google search will include the "Product Result" block, typically on the right side. SerpApi is able to extract and make sense of this information.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

These results are retrieved from the modal that appears after the "Details" or "More details" button is clicked.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

For some products (depending on your location), Google search will include the "Product Result" block, typically on the right side. SerpApi is able to extract and make sense of this information.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

These results are retrieved from the modal that appears after the "Details" or "More details" button is clicked.

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
