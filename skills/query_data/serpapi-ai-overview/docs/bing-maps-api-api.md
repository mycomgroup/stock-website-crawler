---
id: "url-5e158810"
type: "api"
title: "Bing Maps API"
url: "https://serpapi.com/bing-maps-api"
description: "Our Bing Maps API allows you to scrape results from Bing Maps.\n\nThe API endpoint is https://serpapi.com/search?engine=bing_maps Head to the playground for a live and interactive demo.\n\nFor some searches, Bing Maps response multiple sets of local results. In this case, local results are grouped by Coffee shop, Espresso, and etc."
source: ""
tags: []
crawl_time: "2026-03-18T06:38:15.061Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Multiple Local Results example for coffee","description":"For some searches, Bing Maps response multiple sets of local results. In this case, local results are grouped by Coffee shop, Espresso, and etc.","requestParams":{"engine":"bing_maps","q":"coffee","cp":"30.307989~-97.749943","highlight":"local_results"},"responseJson":"https://serpapi.com/search.json?engine=bing_maps&q=coffee&cp=30.307989~-97.749943"}
    - {"title":"Single Local Results example for coffee shop","description":"","requestParams":{"engine":"bing_maps","q":"coffee shop","cp":"30.307989~-97.749943","highlight":"local_results"},"responseJson":"https://serpapi.com/search.json?engine=bing_maps&q=coffee+shop&cp=30.307989~-97.749943"}
    - {"title":"Place Results example for place_id: YN873x14475615034754698960 (Law Firm)","description":"","requestParams":{"engine":"bing_maps","place_id":"YN873x14475615034754698960","highlight":"place_results"},"responseJson":"https://serpapi.com/search.json?engine=bing_maps&place_id=YN873x14475615034754698960"}
    - {"title":"Place Results example for place_id: YN860x189741933 (Restaurant)","description":"","requestParams":{"engine":"bing_maps","place_id":"YN860x189741933","highlight":"place_results"},"responseJson":"https://serpapi.com/search.json?engine=bing_maps&place_id=YN860x189741933"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n\n  \"filters\": [\n    {\n      \"title\": \"String - title of the filter\",\n      \"link\": \"String - URL to the Bing Maps page with the filter applied\",\n      \"serpapi_link\": \"String - SerpApi's API URL of the link\"\n    }\n  ]\n  \"local_results\": [  \n    {\n      \"title\": \"String - title of the local result\",\n      \"link\": \"String - URL to the Bing Maps page\",\n      \"items\": [\n        {\n          \"place_id\": \"String - ID of the entity\",\n          \"address\": \"String - address of the entity\",\n          \"gps_coordinates\": {\n            \"latitude\": \"Float\",\n            \"longitude\": \"Float\"\n          },\n          \"phone\": \"String - phone number of the entity\",\n          \"website\": \"String - website of the entity\",\n          \"price\": \"String - price level of the entity\",\n          \"price_description\": \"String - description of the price (e.g. cheap, very cheap)\",\n          \"type\": \"String - type of the entity (e.g. Restaurant)\",\n          \"secondary_type\": \"String - secondary type of the entity (e.g. Coffee House)\",\n          \"thumbnail\": \"String - Thumbnail's URL of the entity\",\n          \"title\": \"String - title of the entity\",\n          \"rating\": \"Float - rating of the entity\",\n          \"reviews\": \"Integer - number of reviews of the entity\",\n          \"source\": \"String - source of the review\",\n          \"open_state\": \"String - open hours of the entity\",\n          \"description\": \"String - description of the entity\",\n        },\n        ...\n      ]\n    }\n  ],\n  \"place_results\": {\n    \"title\": \"String - title of the entity\",\n    \"place_id\": \"String - ID of the entity\",\n    \"address\": \"String - address of the entity\",\n    \"gps_coordinates\": {\n      \"latitude\": \"Float\",\n      \"longitude\": \"Float\"\n    },\n    \"phone\": \"String - phone number of the entity\",\n    \"website\": \"String - website of the entity\",\n    \"rating\": \"Float - rating of the entity\",\n    \"reviews\": \"Integer - number of reviews of the entity\",\n    \"rating_provider\": \"String - Platform that provides the rating (e.g. Yelp)\",\n    \"type\": \"String - type of the entity\",\n    \"claimed\": \"Boolean - whether the entity is claimed by the owner\",\n    \"images\": [\n      {\n        \"thumbnail\": \"String - URL of the thumbnail\",\n        \"link\": \"String - URL to the Bing Images search\"\n      }\n    ],\n    \"directions\": \"String - URL of the Bing Maps' direction to the entity\",\n    \"open_state\": \"String - open hours of the entity\"\n    \"hours\": \"Hash - open hours of each day of the entity\",\n    \"service_ares\": \"String - entity's service area\",\n    \"reviews\": [\n      {\n        \"source\": \"String - source of the review\",\n        \"source_logo\": \"String - URL of the source's logo\",\n        \"rating\": \"Float - rating of the review\",\n        \"total_reviews\": \"String - total number of reviews\",\n        \"reviews\": [\n          {\n            \"rating\": \"Float - rating of the review\",\n            \"date\": \"String - date of the review\",\n            \"text\": \"String - text of the review\",\n            \"user_name\": \"String - name of the user who wrote the review\",\n            \"link\": \"String - URL to the review in the source platform\"\n          }\n        ],\n        \"see_all_link\": \"String - URL to view all the review in source platform\"\n      }\n    ],\n    \"customer_say\": [\n      {\n        \"title\": \"String - title of the customer say\",\n        \"text\": \"String - text of the customer say\"\n      }\n    ],\n    \"social\": [\n      {\n        \"name\": \"String - Social platform name\",\n        \"link\": \"String - URL to the social profile\",\n        \"thumbnail\": \"String - Thumbnail URL of the social platform's logo\"\n      }\n    ],\n    \"amenities\": \"Array - amenities of the entity (e.g. Wi-Fi, Outdoor seating)\",\n    \"people_also_search_for\": [\n      {\n        \"title\": \"String\",\n        \"items\": [\n          {\n            \"title\": \"String - title of the entity\",\n            \"place_id\": \"String - ID of the entity\",\n            \"link\": \"String - URL to the entity in Bing Maps\",\n            \"rating\": \"Float - rating of the entity\",\n            \"reviews\": \"Integer - number of reviews of the entity\",\n            \"source\": \"String - source of the review\"\n          }\n        ]\n      }\n    ]\n  }\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "bing-maps-api-api"
---

# Bing Maps API

## 源URL

https://serpapi.com/bing-maps-api

## 描述

Our Bing Maps API allows you to scrape results from Bing Maps.

The API endpoint is https://serpapi.com/search?engine=bing_maps Head to the playground for a live and interactive demo.

For some searches, Bing Maps response multiple sets of local results. In this case, local results are grouped by Coffee shop, Espresso, and etc.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Bing Maps API allows you to scrape results from Bing Maps.

The API endpoint is https://serpapi.com/search?engine=bing_maps Head to the playground for a live and interactive demo.

For some searches, Bing Maps response multiple sets of local results. In this case, local results are grouped by Coffee shop, Espresso, and etc.

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
