---
id: "url-3989eee"
type: "api"
title: "Google Shopping Results API"
url: "https://serpapi.com/shopping-results"
description: "The Google Shopping Results API scrapes the position, title, product_id, product_link, serpapi_product_api, immersive_product_page_token, serpapi_immersive_product_api, source, source_icon, price, extracted_price, installment, alternative_price, old_price, extracted_old_price, delivery, second_hand_condition, rating, reviews, snippet, extensions, thumbnail, thumbnails, serpapi_thumbnail, serpapi_thumbnails, multiple_sources, tag and badge fields of a shopping result.\n\nThe API endpoint is https://serpapi.com/search?engine=google_shopping Head to the playground for a live and interactive demo.\n\nSome shopping results have a price in another currency.\n\nShopping results can sometimes contain monthly prices. SerpApi is able to make sense of this data and serve monthly price as installment."
source: ""
tags: []
crawl_time: "2026-03-18T11:06:49.853Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Results for: q: Coffee","description":"","requestParams":{"engine":"google_shopping","q":"Coffee","location":"Austin, Texas, United States","hl":"en","gl":"us","highlight":"shopping_results"},"responseJson":"https://serpapi.com/search.json?engine=google_shopping&q=Coffee&location=Austin,+Texas,+United+States&hl=en&gl=us"}
    - {"title":"Tablet Results for: device: tablet, and q: Coffee","description":"","requestParams":{"engine":"google_shopping","q":"Coffee","device":"tablet","location":"Austin, Texas, United States","hl":"en","gl":"us","highlight":"shopping_results"},"responseJson":"https://serpapi.com/search.json?engine=google_shopping&q=Coffee&device=tablet&location=Austin,+Texas,+United+States&hl=en&gl=us"}
    - {"title":"Mobile Results for: device: mobile, and q: Auto Parts","description":"","requestParams":{"engine":"google_shopping","q":"Auto Parts","device":"mobile","location":"Austin, Texas, United States","hl":"en","gl":"us","highlight":"shopping_results"},"responseJson":"https://serpapi.com/search.json?engine=google_shopping&q=Auto+Parts&device=mobile&location=Austin,+Texas,+United+States&hl=en&gl=us"}
    - {"title":"Results for: q: Apple - iPhone 14 128GB - Starlight","description":"Some shopping results have a price in another currency.","requestParams":{"engine":"google_shopping","q":"Apple - iPhone 14 128GB - Starlight","location":"Province of Barcelona, Catalonia, Spain","hl":"en","gl":"tr","google_domain":"google.ad","highlight":"shopping_results"},"responseJson":"https://serpapi.com/search.json?engine=google_shopping&q=Apple+-+iPhone+14+128GB+-+Starlight&location=Province+of+Barcelona,+Catalonia,+Spain&hl=en&gl=tr&google_domain=google.ad"}
    - {"title":"Results for: q: iphone","description":"Shopping results can sometimes contain monthly prices. SerpApi is able to make sense of this data and serve monthly price as installment.","requestParams":{"engine":"google_shopping","q":"iPhone","gl":"us","highlight":"shopping_results"},"responseJson":"https://serpapi.com/search.json?engine=google_shopping&q=iPhone&gl=us"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"shopping_results\": [\n    {\n      \"position\": \"Integer - Item position\",\n      \"title\": \"String - Item title\",\n      \"tagline\": \"String - Item tagline\",\n      \"product_link\": \"String - Link to the Google item page\",\n      \"product_id\": \"String - Unique Google product identifier\",\n      \"immersive_product_page_token\": \"String - Product Token for in Search API Google Immersive Product API\",\n      \"serpapi_immersive_product_api\": \"String - SerpApi URL to fetch more information about this specific product via Google Immersive Product API\",\n      \"source\": \"String - Product source name\",\n      \"source_icon\": \"String - Link to the source icon\",\n      \"price\": \"String - Item price\",\n      \"extracted_price\": \"Numeric - Item's price as float or integer\",\n      \"installment\": {\n        \"price\": \"String - Monthly installment price of the item\",\n        \"extracted_price\": \"Numeric - Item's installment price as float or integer\",\n        \"period\": \"Integer - Number of months\",\n      },\n      \"alternative_price\": {\n        \"price\": \"String - Price of an item in alternative currency\",\n        \"currency\": \"String - Currency of an item\",\n        \"extracted_price\": \"Numeric - Item's price as float or integer\" \n      },\n      \"old_price\": \"String - Item's price before discount (Ex: '$15.99')\",\n      \"extracted_old_price\": \"Numeric - Item's old price as float or integer (Ex: '15.99')\",\n      \"delivery\": \"String - Delivery price information of the item\",\n      \"second_hand_condition\": \"String - Description of condition when the product is second hand (Ex: 'used', or 'refurbished')\",\n      \"rating\": \"Float - Item rating\",\n      \"reviews\": \"Integer - Item review count\",\n      \"snippet\": \"String - Item description\",\n      \"snippet_highlighted_words\": \"Array - List of the highlighted words in the item description\",\n      \"extensions\": \"Array - Item tags/extensions\",\n      \"thumbnail\": \"String - URL of the item's main image\",\n      \"thumbnails\": \"Array - URLs of item images when there are multiple ones\",\n      \"serpapi_thumbnail\": \"String - SerpApi link to the item's main image\",\n      \"serpapi_thumbnails\": \"Array - SerpApi links to the item images when there are multiple ones\",\n      \"multiple_sources\": \"True - If more than one seller available\",\n      \"tag\": \"String - Item tag ex: CURBSIDE, IN-STORE PICKUP, SALE, or FREE 2-DAY\",\n      \"badge\": \"String - Seller's Extra Information eg: Small business\",\n    },\n    ...\n  ],\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "shopping-results-api"
---

# Google Shopping Results API

## 源URL

https://serpapi.com/shopping-results

## 描述

The Google Shopping Results API scrapes the position, title, product_id, product_link, serpapi_product_api, immersive_product_page_token, serpapi_immersive_product_api, source, source_icon, price, extracted_price, installment, alternative_price, old_price, extracted_old_price, delivery, second_hand_condition, rating, reviews, snippet, extensions, thumbnail, thumbnails, serpapi_thumbnail, serpapi_thumbnails, multiple_sources, tag and badge fields of a shopping result.

The API endpoint is https://serpapi.com/search?engine=google_shopping Head to the playground for a live and interactive demo.

Some shopping results have a price in another currency.

Shopping results can sometimes contain monthly prices. SerpApi is able to make sense of this data and serve monthly price as installment.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

The Google Shopping Results API scrapes the position, title, product_id, product_link, serpapi_product_api, immersive_product_page_token, serpapi_immersive_product_api, source, source_icon, price, extracted_price, installment, alternative_price, old_price, extracted_old_price, delivery, second_hand_condition, rating, reviews, snippet, extensions, thumbnail, thumbnails, serpapi_thumbnail, serpapi_thumbnails, multiple_sources, tag and badge fields of a shopping result.

The API endpoint is https://serpapi.com/search?engine=google_shopping Head to the playground for a live and interactive demo.

Some shopping results have a price in another currency.

Shopping results can sometimes contain monthly prices. SerpApi is able to make sense of this data and serve monthly price as installment.

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
