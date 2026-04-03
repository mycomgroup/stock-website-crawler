---
id: "url-400d2039"
type: "api"
title: "Apple App Store Reviews Scraper API"
url: "https://serpapi.com/apple-reviews"
description: "Our Apple App Store Reviews API allows you to scrape results from the Apple App Store Reviews page.\n\nThe API endpoint is https://serpapi.com/search?engine=apple_reviews Head to the playground for a live and interactive demo.\n\nIf product_id being searched belongs to a reviews from the macOS App Store, it may cause certain variations in the search. The sort parameter will be ineffective for reviews from the macOS App Store. Also, the resulting reviews results will not contain the id or author_id keys."
source: ""
tags: []
crawl_time: "2026-03-18T06:38:00.068Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Example results for product_id:534220544","description":"","requestParams":{"engine":"apple_reviews","product_id":"534220544","highlight":"reviews"},"responseJson":"https://serpapi.com/search.json?engine=apple_reviews&product_id=534220544"}
    - {"title":"Example results for product_id: 534220544, and sort: mosthelpful","description":"","requestParams":{"engine":"apple_reviews","product_id":"534220544","sort":"mosthelpful","highlight":"reviews"},"responseJson":"https://serpapi.com/search.json?engine=apple_reviews&product_id=534220544&sort=mosthelpful"}
    - {"title":"Example results for product_id: 747648890 (Reviews from the macOS App Store)","description":"If product_id being searched belongs to a reviews from the macOS App Store, it may cause certain variations in the search. The sort parameter will be ineffective for reviews from the macOS App Store. Also, the resulting reviews results will not contain the id or author_id keys.","requestParams":{"engine":"apple_reviews","product_id":"747648890","highlight":"reviews"},"responseJson":"https://serpapi.com/search.json?engine=apple_reviews&product_id=747648890"}
    - {"title":"More complex examples with multiple optional parameters","description":"The URL below fetches: • Third page of result, • Product with the ID: 1499149941, • sorted by mosthelpful, • in country gb","requestParams":{"engine":"apple_reviews","product_id":"1499149941","page":"3","country":"gb","sort":"mosthelpful","highlight":"reviews"},"responseJson":"https://serpapi.com/search.json?engine=apple_reviews&product_id=1499149941&page=3&country=gb&sort=mosthelpful"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"search_information\": {\n    \"reviews_for_current_version\": \"Integer, Number of reviews (with or without a text) for current version of the app\",\n    \"total_page_count\": \"Integer, Total number of pages of reviews\",\n    \"reviews_results_state\": \"String, State of the reviews results (Ex: Results for exact ID number.)\",\n    \"results_count\": \"Integer, Number of reviews results returned\"\n  },\n  \"reviews\": [\n    {\n      \"position\": \"Integer, Position of the review (Ex: 1)\",\n      \"id\": \"String, Unique identifying number of the review (Ex: 7417861364)\",\n      \"title\": \"String, Title of the review, (Ex: Lacks ratios)\",\n      \"text\": \"String, Body text of the review, (Ex: Beautiful app with images and videos but doesn’t tell you how much of what goes in making the drink. Needs ratios!)\",\n      \"rating\": \"Integer, Rating of the review, (Ex: 3)\",\n      \"review_date\": \"String, Date of the review (Ex: Jun 02, 2021)\",\n      \"author\": {\n        \"name\": \"String, Username of the reviewer\",\n        \"author_id\": \"String, Unique user id of the author (Ex: 000000000)\",\n      }\n    }\n    ...\n  ],\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "apple-reviews-api"
---

# Apple App Store Reviews Scraper API

## 源URL

https://serpapi.com/apple-reviews

## 描述

Our Apple App Store Reviews API allows you to scrape results from the Apple App Store Reviews page.

The API endpoint is https://serpapi.com/search?engine=apple_reviews Head to the playground for a live and interactive demo.

If product_id being searched belongs to a reviews from the macOS App Store, it may cause certain variations in the search. The sort parameter will be ineffective for reviews from the macOS App Store. Also, the resulting reviews results will not contain the id or author_id keys.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Apple App Store Reviews API allows you to scrape results from the Apple App Store Reviews page.

The API endpoint is https://serpapi.com/search?engine=apple_reviews Head to the playground for a live and interactive demo.

If product_id being searched belongs to a reviews from the macOS App Store, it may cause certain variations in the search. The sort parameter will be ineffective for reviews from the macOS App Store. Also, the resulting reviews results will not contain the id or author_id keys.

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
