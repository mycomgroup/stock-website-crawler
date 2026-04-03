---
id: "url-2eff537d"
type: "api"
title: "Amazon Search API"
url: "https://serpapi.com/amazon-search-api"
description: "Our Amazon Search API allows you to scrape results from the Amazon search page.\n\nThe API endpoint is https://serpapi.com/search?engine=amazon Head to the playground for a live and interactive demo."
source: ""
tags: []
crawl_time: "2026-03-18T17:27:35.864Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Example results for k: Coffee","description":"","requestParams":{"engine":"amazon","k":"Coffee"},"responseJson":"https://serpapi.com/search.json?engine=amazon&k=Coffee"}
    - {"title":"Example results for search by k: Coffee in i: fashion","description":"","requestParams":{"engine":"amazon","k":"Coffee","i":"fashion"},"responseJson":"https://serpapi.com/search.json?engine=amazon&k=Coffee&i=fashion"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  \"search_information\": {\n    \"total_results\": \"Integer - Total number of search results\",\n    \"query_displayed\": \"String - The search query displayed\",\n    \"store\": \"String - Amazon store identifier\",\n    \"page\": \"Integer - Current page number\"\n  },\n  \"product_ads\": {\n    \"image\": \"String - Brand image URL\",\n    \"logo\": \"String - Brand logo URL\",\n    \"headline\": \"String - Advertisement headline\",\n    \"link\": \"String - Store page link\",\n    \"video_thumbnail\": \"String - Video thumbnail URL\",\n    \"video_src\": \"String - Video source URL\",\n    \"video_link\": \"String - Link to the video page\",\n    \"store_page\": \"String - Store page name\",\n    \"store_page_link\": \"String - Store page link URL\",\n    \"products\": [\n      {\n        \"position\": \"Integer - Product position in ads\",\n        \"asin\": \"String - Amazon Standard Identification Number\",\n        \"sponsored\": \"Boolean - Whether the product is sponsored\",\n        \"title\": \"String - Product title\",\n        \"link\": \"String - Product link\",\n        \"link_clean\": \"String - Clean product link without tracking parameters\",\n        \"thumbnail\": \"String - Product thumbnail URL\",\n        \"prime\": \"Boolean - Whether Prime delivery is available\",\n        \"rating\": \"Float - Product rating (e.g., 4.6)\",\n        \"reviews\": \"Integer - Number of reviews\",\n        \"badges\": [\n          \"String - Product badges\"\n        ],\n        \"price\": \"String - Product price\",\n        \"extracted_price\": \"Float - Extracted numeric price\",\n        \"old_price\": \"String - Original price before discount\",\n        \"extracted_old_price\": \"Float - Extracted numeric original price\",\n        \"offers\": [\n          \"String - Special offer descriptions\"\n        ]\n      },\n      ...\n    ]\n  },\n  \"featured_products\": [\n    {\n      \"title\": \"String - Section title\",\n      \"description\": \"String - Section description\",\n      \"products\": [\n        {\n          \"position\": \"Integer - Product position\",\n          \"asin\": \"String - Amazon Standard Identification Number\",\n          \"sponsored\": \"Boolean - Whether the product is sponsored\",\n          \"title\": \"String - Product title\",\n          \"link\": \"String - Product link\",\n          \"link_clean\": \"String - Clean product link\",\n          \"thumbnail\": \"String - Product thumbnail URL\",\n          \"badges\": [\n            \"String - Product badges\"\n          ],\n          \"bought_last_month\": \"String - Number of purchases in past month\",\n          \"rating\": \"Float - Product rating\",\n          \"reviews\": \"Integer - Number of reviews\",\n          \"price\": \"String - Product price\",\n          \"extracted_price\": \"Float - Extracted numeric price\",\n          \"prime\": \"Boolean - Whether Prime delivery is available\",\n          \"old_price\": \"String - Original price\",\n          \"extracted_old_price\": \"Float - Extracted numeric original price\",\n          \"save_with_coupon\": \"String - Coupon savings description\",\n          \"offers\": [\n            \"String - Special offer descriptions\"\n          ],\n          \"sustainability_features\": [\n            {\n              \"position\": \"Integer - Feature position\",\n              \"name\": \"String - Feature name\",\n              \"snippet\": \"String - Brief description\",\n              \"thumbnail\": \"String - Feature icon URL\",\n              \"certified_by\": \"String - Certification authority\",\n              \"certified_info\": \"String - Certification details\"\n            },\n            ...\n          ]\n        },\n        ...\n      ]\n    },\n    ...\n  ],\n  \"organic_results\": [\n    {\n      \"position\": \"Integer - Result position\",\n      \"asin\": \"String - Amazon Standard Identification Number\",\n      \"title\": \"String - Product title\",\n      \"link\": \"String - Product link\",\n      \"link_clean\": \"String - Clean product link without tracking parameters\",\n      \"thumbnail\": \"String - Product thumbnail URL\",\n      \"brand\": \"String - Product brand name\",\n      \"badges\": [\n        \"String - Badge text (e.g., 'Limited time deal', 'Amazon's Choice')\"\n      ],\n      \"tags\": [\n        \"String - Product tags\"\n      ],\n      \"variants\": {\n        \"options\": [\n          {\n            \"position\": \"Integer - Variant position\",\n            \"asin\": \"String - ASIN of the variant\",\n            \"title\": \"String - Variant title\",\n            \"link\": \"String - Variant link\"\n          },\n          ...\n        ],\n        \"more_variants\": \"String - Text indicating more variants available\",\n        \"more_variants_link\": \"String - Link to see more variants\"\n      },\n      \"sponsored\": \"Boolean - Whether the result is sponsored\",\n      \"amazon_brand\": \"Boolean - Whether it's an Amazon brand product\",\n      \"top_rated\": \"Boolean - Whether the product is top rated\",\n      \"options\": \"String - Available options text\",\n      \"options_link\": \"String - Link to see options\",\n      \"rating\": \"Float - Product rating (e.g., 4.4)\",\n      \"reviews\": \"Integer - Number of reviews\",\n      \"price\": \"String - Product price (e.g., '$13.60')\",\n      \"extracted_price\": \"Float - Extracted numeric price value\",\n      \"no_featured_offers_available\": \"Boolean - Whether no featured offers are available\",\n      \"bought_last_month\": \"String - Number of purchases in past month (e.g., '20K+ bought in past month')\",\n      \"save_with_coupon\": \"String - Coupon savings description\",\n      \"snap_ebt_eligible\": \"Boolean - Whether SNAP EBT is accepted\",\n      \"prime\": \"Boolean - Whether Prime delivery is available\",\n      \"offers\": [\n        \"String - Special offer descriptions\"\n      ],\n      \"stock\": \"String - Stock availability status\",\n      \"price_unit\": \"String - Price per unit (e.g., '$1.13/Ounce')\",\n      \"extracted_price_unit\": \"Float - Extracted numeric price per unit\",\n      \"whole_foods_market\": \"Boolean - Whether available at Whole Foods Market\",\n      \"amazon_fresh\": \"Boolean - Whether Amazon Fresh is available\",\n      \"climate_pledge_friendly\": \"Boolean - Whether product is climate pledge friendly\",\n      \"small_business\": \"Boolean - Whether it's from a small business\",\n      \"works_with_alexa\": \"Boolean - Whether the product works with Alexa\",\n      \"sustainability_features\": [\n        {\n          \"position\": \"Integer - Feature position\",\n          \"name\": \"String - Feature name (e.g., 'Organic content')\",\n          \"snippet\": \"String - Brief description of the feature\",\n          \"thumbnail\": \"String - Feature icon URL\",\n          \"certified_by\": \"String - Certification authority\",\n          \"certified_info\": \"String - Detailed certification information\"\n        },\n        ...\n      ],\n      \"delivery\": [\n        \"String - Delivery options and dates\"\n      ],\n      \"age_rating\": \"String - Age rating for the product\",\n      \"origin_country\": {\n        \"name\": \"String - Country name\",\n        \"link\": \"String - Country link\",\n        \"thumbnail\": \"String - Country flag thumbnail\"\n      },\n      \"specs\": {\n        \"...\": \"String - Other product specifications (dynamic keys)\"\n      },\n      \"more_buying_choices\": \"String - More buying choices text\",\n      \"more_buying_choices_link\": \"String - Link to more buying choices\"\n    },\n    ...\n  ],\n  \"video_results\": [\n    {\n      \"block_position\": \"String - Position of video block\",\n      \"video_thumbnail\": \"String - Video thumbnail URL\",\n      \"video_src\": \"String - Video source URL\",\n      \"video_link\": \"String - Link to video\",\n      \"products\": [\n        {\n          \"position\": \"Integer - Product position\",\n          \"asin\": \"String - Amazon Standard Identification Number\",\n          \"sponsored\": \"Boolean - Whether the product is sponsored\",\n          \"title\": \"String - Product title\",\n          \"link\": \"String - Product link\",\n          \"link_clean\": \"String - Clean product link\",\n          \"thumbnail\": \"String - Product thumbnail URL\",\n          \"rating\": \"Float - Product rating\",\n          \"reviews\": \"Integer - Number of reviews\",\n          \"price\": \"String - Product price\",\n          \"extracted_price\": \"Float - Extracted numeric price\",\n          \"old_price\": \"String - Original price\",\n          \"extracted_old_price\": \"Float - Extracted numeric original price\",\n          \"offers\": [\n            \"String - Special offer descriptions\"\n          ],\n          \"prime\": \"Boolean - Whether Prime delivery is available\",\n          \"delivery\": [\n            \"String - Delivery options\"\n          ]\n        },\n        ...\n      ]\n    },\n    ...\n  ],\n  \"sponsored_brands\": {\n    \"title\": \"String - Section title\",\n    \"brands\": [\n      {\n        \"position\": \"Integer - Brand position\",\n        \"name\": \"String - Brand name\",\n        \"image\": \"String - Brand image URL\",\n        \"logo\": \"String - Brand logo URL\",\n        \"headline\": \"String - Brand headline\",\n        \"link\": \"String - Brand page link\"\n      },\n      ...\n    ]\n  },\n  \"filters\": {\n    \"category_name\": [\n      {\n        \"position\": \"Integer - Filter position\",\n        \"rh\": \"String - Filter refinement hash parameter\",\n        \"name\": \"String - Filter name\",\n        \"description\": \"String - Filter description\",\n        \"image\": \"String - Filter image URL\",\n        \"link\": \"String - Filter link\",\n        \"serpapi_link\": \"String - SerpApi filter link\",\n        \"used\": \"Boolean - Whether filter is currently applied\"\n      },\n      ...\n    ]\n  },\n  \"related_searches\": [\n    {\n      \"position\": \"Integer - Position in related searches\",\n      \"query\": \"String - Related search query\",\n      \"link\": \"String - Search link\"\n    },\n    ...\n  ],\n  \"serpapi_pagination\": {\n    \"current\": \"Integer - Current page number\",\n    \"previous\": \"String - SerpApi URL to previous page\",\n    \"next\": \"String - SerpApi URL to next page\"\n  }\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "amazon-search-api-api"
---

# Amazon Search API

## 源URL

https://serpapi.com/amazon-search-api

## 描述

Our Amazon Search API allows you to scrape results from the Amazon search page.

The API endpoint is https://serpapi.com/search?engine=amazon Head to the playground for a live and interactive demo.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Amazon Search API allows you to scrape results from the Amazon search page.

The API endpoint is https://serpapi.com/search?engine=amazon Head to the playground for a live and interactive demo.

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
