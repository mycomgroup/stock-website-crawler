---
id: "url-6249e64a"
type: "api"
title: "Supported Locations API"
url: "https://serpapi.com/locations-api"
description: "Locations API allows you to search SerpApi supported locations. It should return an array of locations ordered by reach. Locations that reach the most people will be first. This API is free to use. Download the full JSON list of supported locations:"
source: ""
tags: []
crawl_time: "2026-03-18T06:38:31.848Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Example 2","description":"","requestParams":{},"responseJson":"{\n  {\n    \"id\": \"585069bdee19ad271e9bc072\",\n    \"google_id\": 200635,\n    \"google_parent_id\": 21176,\n    \"name\": \"Austin, TX\",\n    \"canonical_name\": \"Austin, TX,Texas,United States\",\n    \"country_code\": \"US\",\n    \"target_type\": \"DMA Region\",\n    \"reach\": 5560000,\n    \"gps\": [\n      -97.7430608,\n      30.267153\n    ]\n  },\n  {\n    \"id\": \"585069b8ee19ad271e9ba949\",\n    \"google_id\": 1026201,\n    \"google_parent_id\": 21176,\n    \"name\": \"Austin\",\n    \"canonical_name\": \"Austin,Texas,United States\",\n    \"country_code\": \"US\",\n    \"target_type\": \"City\",\n    \"reach\": 4870000,\n    \"gps\": [\n      -97.7430608,\n      30.267153\n    ]\n  },\n  {\n    \"id\": \"585069bdee19ad271e9bc05e\",\n    \"google_id\": 200611,\n    \"google_parent_id\": 2840,\n    \"name\": \"Rochester, MN-Mason City, IA-Austin, MN\",\n    \"canonical_name\": \"Rochester, MN-Mason City, IA-Austin, MN,United States\",\n    \"country_code\": \"US\",\n    \"target_type\": \"DMA Region\",\n    \"reach\": 555000\n  },\n  {\n    \"id\": \"585069eeee19ad271e9c9632\",\n    \"google_id\": 9060008,\n    \"google_parent_id\": 21176,\n    \"name\": \"The University of Texas at Austin\",\n    \"canonical_name\": \"The University of Texas at Austin,Texas,United States\",\n    \"country_code\": \"US\",\n    \"target_type\": \"University\",\n    \"reach\": 250000,\n    \"gps\": [\n      -97.7340567,\n      30.2849185\n    ]\n  },\n  {\n    \"id\": \"585069edee19ad271e9c93df\",\n    \"google_id\": 9059413,\n    \"google_parent_id\": 21176,\n    \"name\": \"Austin County\",\n    \"canonical_name\": \"Austin County,Texas,United States\",\n    \"country_code\": \"US\",\n    \"target_type\": \"County\",\n    \"reach\": 157000,\n    \"gps\": [\n      -96.2800864,\n      29.8711291\n    ]\n  }\n}"}
  importantNotes:
    - "The URL below fetches the 5 biggest locations that contains \"Austin\" in their name in our database. You can then use the location canonical name (e.g., \"Austin,Texas,United States\") or the location id (e.g., \"585069efee19ad271e9c9b36\") as the value of the param location for the /search API to get more precise results."
    - "GET https://serpapi.com/locations.json?q=Austin&limit=5"
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "locations-api-api"
---

# Supported Locations API

## 源URL

https://serpapi.com/locations-api

## 描述

Locations API allows you to search SerpApi supported locations. It should return an array of locations ordered by reach. Locations that reach the most people will be first. This API is free to use. Download the full JSON list of supported locations:

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 注意事项

- The URL below fetches the 5 biggest locations that contains "Austin" in their name in our database. You can then use the location canonical name (e.g., "Austin,Texas,United States") or the location id (e.g., "585069efee19ad271e9c9b36") as the value of the param location for the /search API to get more precise results.
- GET https://serpapi.com/locations.json?q=Austin&limit=5

## 文档正文

Locations API allows you to search SerpApi supported locations. It should return an array of locations ordered by reach. Locations that reach the most people will be first. This API is free to use. Download the full JSON list of supported locations:

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
