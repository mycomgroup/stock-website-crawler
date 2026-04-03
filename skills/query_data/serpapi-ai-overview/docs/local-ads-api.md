---
id: "url-56a105ed"
type: "api"
title: "Google Local Ads Results API"
url: "https://serpapi.com/local-ads"
description: "When a Google search contains local advertisements near the specified area, they are parsed and exist within the local_ads object in the JSON output. Advertisements can contain title, link, see_more_text, badge, and ads. Individual ad blocks can contain title, rating, badge, service_area, hours, phone and more.To access the full list of local ads you can use our Google Local Services API, by following local_ads.serpapi_link.\n\nThe API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo."
source: ""
tags: []
crawl_time: "2026-03-18T02:58:23.630Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Results for: q: Plumbing","description":"","requestParams":{"q":"Plumbing","location":"Dracut, Massachusetts, United States","hl":"en","gl":"us","highlight":"local_ads"},"responseJson":"https://serpapi.com/search.json?q=Plumbing&location=Dracut,+Massachusetts,+United+States&hl=en&gl=us"}
    - {"title":"Mobile results for: q: Plumbing, location: London, England, United Kingdom","description":"","requestParams":{"q":"Plumbing","location":"London, England, United Kingdom","hl":"en","gl":"uk","device":"mobile","highlight":"local_ads"},"responseJson":"https://serpapi.com/search.json?q=Plumbing&location=London,+England,+United+Kingdom&hl=en&gl=uk&device=mobile"}
    - {"title":"Mobile results for: q: plumber in queens, hl: en, gl: us, device: mobile","description":"","requestParams":{"q":"plumber in queens","hl":"en","gl":"us","device":"mobile","highlight":"local_ads"},"responseJson":"https://serpapi.com/search.json?q=plumber+in+queens&hl=en&gl=us&device=mobile"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"local_ads\": {\n    \"title\": \"String - Title of Local Ads section\",\n    \"badge\": \"String - Google badge\",\n    \"see_more_text\": \"String - Text on link to see more results\",\n    \"link\": \"String - URL to see more results\",\n    // Tags are only available for mobile results\n    \"tags\": [\n      {\n        \"position\": \"Integer - Position of the tag\",\n        \"text\": \"String - Text on the tag\",\n        \"link\": \"String - URL to see results related to the tag\",\n      },\n      ...\n    ],\n    \"ads\": [\n      {\n        \"position\": \"Integer - Position of the ad\",\n        \"title\": \"String - Title on the ad\",\n        \"link\": \"String - URL to see more details about the ad\",\n        \"rating\": \"Integer - Rating of the service being advertised on the ad\",\n        \"rating_count\": \"Integer - Number of ratings given to the service being advertised on the ad\",\n        \"type\": \"String - Type of service advertised on the ad\",\n        \"service_area\": \"String - Area where service advertised cover\",\n        \"hours\": \"String - Text describing when service advertised on the ad is available\",\n        \"years_in_business\": \"String - Information about how many years service provider has been operational\",\n        \"phone\": \"String - Phone number of service provider on the ad\",\n        \"thumbnail\": \"String - URL to the thumbnail image\",\n        \"highlighted_details\": [\n          \"String - Detail about the service provider highlighted on the ad\"\n          ...\n        ],\n      }\n    ],\n  }\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "local-ads-api"
---

# Google Local Ads Results API

## 源URL

https://serpapi.com/local-ads

## 描述

When a Google search contains local advertisements near the specified area, they are parsed and exist within the local_ads object in the JSON output. Advertisements can contain title, link, see_more_text, badge, and ads. Individual ad blocks can contain title, rating, badge, service_area, hours, phone and more.To access the full list of local ads you can use our Google Local Services API, by following local_ads.serpapi_link.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

When a Google search contains local advertisements near the specified area, they are parsed and exist within the local_ads object in the JSON output. Advertisements can contain title, link, see_more_text, badge, and ads. Individual ad blocks can contain title, rating, badge, service_area, hours, phone and more.To access the full list of local ads you can use our Google Local Services API, by following local_ads.serpapi_link.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

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
