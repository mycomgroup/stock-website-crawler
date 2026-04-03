---
id: "url-7329f7cb"
type: "api"
title: "Yelp Place Scraper API"
url: "https://serpapi.com/yelp-place"
description: "Our Yelp Place API allows you to scrape results from the Yelp place page.\n\nThe API endpoint is https://serpapi.com/search?engine=yelp_place Head to the playground for a live and interactive demo.\n\nBusiness alert shows the most recent operation status of a business. It is usually present when the business has moved or closed. Set business_alert to true to include business alert information.Example of business alert:- Business is temporarily closed.- Yelpers report this location has closed."
source: ""
tags: []
crawl_time: "2026-03-18T04:10:45.654Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Place results overview","description":"","requestParams":{"engine":"yelp_place","place_id":"maman-new-york-22","highlight":"place_results"},"responseJson":"https://serpapi.com/search.json?engine=yelp_place&place_id=maman-new-york-22"}
    - {"title":"Business Alert Example","description":"Business alert shows the most recent operation status of a business. It is usually present when the business has moved or closed. Set business_alert to true to include business alert information. Example of business alert: - Business is temporarily closed. - Yelpers report this location has closed.","requestParams":{"engine":"yelp_place","place_id":"thats-yogurt-milpitas","business_alert":"true","highlight":"place_results"},"responseJson":"https://serpapi.com/search.json?engine=yelp_place&place_id=thats-yogurt-milpitas&business_alert=true"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"search_information\": {\n    \"query_displayed\": \"String - Place Id searched for\",\n    \"place_results_state\": \"String - State of the place results\",\n  },\n  \"place_results\": {\n    \"name\": \"String - Name of the place (Ex: '% Arabica')\",\n    \"place_ids\": [\n      \"String - Encoded business ID (Ex: 'DE0ROwygh-86i4s-WLp8wQ')\",\n      \"String - Alias business ID (Ex: 'maman-new-york-22')\"\n    ],\n    \"business_alert\": \"String - Alert message about the place (Ex: 'Yelpers report this location has closed.', 'Place is temporarily closed.')\",\n    \"about\": \"String - Extra Information about the place ('Maman, a café and bakery in SoHo, serves family-inspired recipes from the South of France.')\",\n    \"reviews\": \"Integer - Number of reviews of the place (Ex: 229)\",\n    \"rating\": \"Float - Rating of the place (Ex: 4.4)\",\n    \"is_claimable\": \"Boolean - Whether the page of the place is claimable or not. In some cases, a place is still claimable although it is claimed. (Ex: false)\",\n    \"is_claimed\": \"Boolean - Whether the page of the place is claimed or not. (Ex: true)\",\n    \"price\": \"String - Expensiveness expressed in currency (Ex: '$$')\",\n    \"categories\": [\n      {\n        \"title\": \"String - Category title (Ex: 'Coffee & Tea')\",\n        \"link\": \"String - Yelp link to category\"\n      },\n      ...\n    ],\n    \"images\": [\n      \"String - Link to an image of the place\",\n      ...\n    ],\n    \"see_all_images_link\": \"String - Yelp link to all images of the place\",\n    \"website\": \"String - Website of the place\",\n    \"phone\": \"String - Phone number of the place\",\n    \"address\": \"String - Address of the place\",\n    \"directions\": \"String - Yelp Map directions link to the place\",\n    \"history\": {\n      \"description\": \"String - Description about the history of the place (Ex: 'In 2021, Maman founders released the highly anticipated cookbook')\",\n      \"established\": \"String - Establishment date of the place (Ex: '2014')\"\n    },\n    \"popular_items\": [\n      {\n        \"title\": \"String - Name of a popular dish or drink of the place (Ex: 'Spanish Lattes')\",\n        \"photos\": \"Integer - Number of photos of the popular item (Ex: 71)\",\n        \"reviews\": \"Integer - Number of reviews made to a popular item (Ex: 88)\",\n        \"thumbnail\": \"String - Link to the thumbnail of a popular item\"\n      },\n      ...\n    ],\n    \"ambiance\": {\n      \"images\": [\n        {\n          \"title\": \"String - Title of the images\",\n          \"photos\": \"Integer - Total number of photos\",\n          \"images\": \"Array - Link to the images\"\n        },\n        ...\n      ],\n      \"highlights\": \"Array - List of highlights of the ambiance\"\n    },\n    \"review_highlights\": [\n      {\n        \"highlight\": \"String - Highlighted word in a review (Ex 'Kyoto Latte')\",\n        \"review\": \"String - Entire review text (Ex: 'Kyoto Latte was refreshing.')\",\n        \"review_count\": \"Integer - Number of reviews with the same highlighted word (Ex: 27)\",\n        \"author\": \"String - Author of the Review\",\n        \"thumbnail\": \"String - Link to thumbnail of a review\",\n        \"link\": \"String - Yelp Link to all reviews with the highlighted word\"\n      },\n      ...\n    ],\n    \"website_menu\": \"String - Yelp redirection link to the menu on the website of the place\",\n    \"full_menu\": \"String - Yelp link to the menu of the place\",\n    \"serpapi_full_menu_link\": \"String - SerpApi link to fetch the full menu for this place\",\n    \"business_map\": \"String - Link to the image of Google Maps marking the place\",\n    \"cross_streets\": \"String - Cross streets where the place is located (Ex: 'Grand St & Cleveland Pl')\",\n    \"neighborhoods\": [\n      \"String - Neighborhoods nearby the place (Ex: 'Brooklyn Heights')\",\n    ],\n    \"country\": \"String - Two letter country code of the place's location (Ex: 'US')\",\n    \"operation_hours\": {\n      \"last_update\": \"String - Information about when the operational hours were updated (Ex: 'Hours updated 1 month ago')\",\n      \"hours\": [\n        {\n          \"day\": \"String - Day at the operational hours table (Ex: 'Mon')\",\n          \"hours\": \"String - Operational hours of the day (Ex: '8:00 AM - 6:00 PM')\",\n          \"currently_open\": \"Boolean - If the place is open on the day or not (Ex: true)\"\n        },\n        ...\n      ]\n    },\n    \"health_provider\": {\n      \"name\": \"String - Name of the health provider company of the place (Ex: 'Hazel Analytics')\",\n      \"link\": \"String - Link to the website of the health provider company\",\n      \"score\": \"String - Score given by the health provider company (Ex: 'A')\"\n    },\n    \"features\": [\n      {\n        \"title\": \"String - Title of the feature of the place (Ex: 'Offers Takeout')\",\n        \"is_active\": \"Boolean - Whether or not the feature is active (Ex: true)\"\n      },\n      ...\n    ],\n    \"community_questions\": [\n      {\n        \"question\": \"String - Question from the community about the place (Ex: 'Do they sell whole bean coffee to go?')\",\n        \"answer\": \"String - Answer to the question from the community (Ex: 'Yes')\",\n        \"author\": \"String - Author of the question\",\n        \"date\": \"String - Date of the question (Ex: '2 years ago')\",\n        \"helpful_vote_count\": \"Integer - How many people vote this question to be helpful (Ex: 2)\",\n        \"extra_link\": {\n          \"text\": \"String - Text of the extra button about question or answer (Ex: 'See question details')\",\n          \"link\": \"String - Yelp link of the extra button about question or answer\"\n        },\n      },\n      ...\n    ],\n    \"see_more_questions_link\": \"String - Yelp link to more community questions about the place\"\n  }\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "yelp-place-api"
---

# Yelp Place Scraper API

## 源URL

https://serpapi.com/yelp-place

## 描述

Our Yelp Place API allows you to scrape results from the Yelp place page.

The API endpoint is https://serpapi.com/search?engine=yelp_place Head to the playground for a live and interactive demo.

Business alert shows the most recent operation status of a business. It is usually present when the business has moved or closed. Set business_alert to true to include business alert information.Example of business alert:- Business is temporarily closed.- Yelpers report this location has closed.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Yelp Place API allows you to scrape results from the Yelp place page.

The API endpoint is https://serpapi.com/search?engine=yelp_place Head to the playground for a live and interactive demo.

Business alert shows the most recent operation status of a business. It is usually present when the business has moved or closed. Set business_alert to true to include business alert information.Example of business alert:- Business is temporarily closed.- Yelpers report this location has closed.

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
