---
id: "url-65ee53bf"
type: "api"
title: "Bing Shopping API"
url: "https://serpapi.com/bing-shopping-api"
description: "Our Bing Shopping API allows you to scrape SERP results from Bing Shopping page.\n\nThe API endpoint is https://serpapi.com/search?engine=bing_shopping Head to the playground for a live and interactive demo."
source: ""
tags: []
crawl_time: "2026-03-18T17:29:42.223Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Example results for q: jacket","description":"","requestParams":{"engine":"bing_shopping","q":"jacket","highlight":"shopping_results"},"responseJson":"https://serpapi.com/search.json?engine=bing_shopping&q=jacket"}
    - {"title":"Example results for q: jacket with filter","description":"","requestParams":{"engine":"bing_shopping","q":"jacket","highlight":"shopping_results","filters":"gsfilter%253A%2522Mjk2MTA2MTUxNSxCYXNpYywwPTIzMzAyOTQxNDEsRnwxNDY5Njg5ODQzLFR8MjIzODY4NjA2NixGfDQwNTQwMDc1MDIsRnwyMjI5OTY3NTczLEZ8Ow%253D%253D%2522%2Bscenario%253A%252215%2522"},"responseJson":"https://serpapi.com/search.json?engine=bing_shopping&q=jacket&filters=gsfilter%253A%2522Mjk2MTA2MTUxNSxCYXNpYywwPTIzMzAyOTQxNDEsRnwxNDY5Njg5ODQzLFR8MjIzODY4NjA2NixGfDQwNTQwMDc1MDIsRnwyMjI5OTY3NTczLEZ8Ow%253D%253D%2522%2Bscenario%253A%252215%2522"}
    - {"title":"Example results for q: iphone","description":"","requestParams":{"engine":"bing_shopping","q":"iphone","highlight":"shopping_results"},"responseJson":"https://serpapi.com/search.json?engine=bing_shopping&q=iphone"}
    - {"title":"Example results for q: coffee","description":"","requestParams":{"engine":"bing_shopping","q":"coffee","highlight":"shopping_results"},"responseJson":"https://serpapi.com/search.json?engine=bing_shopping&q=coffee"}
    - {"title":"Example results for q: switch","description":"","requestParams":{"engine":"bing_shopping","q":"switch","highlight":"inline_ads_results"},"responseJson":"https://serpapi.com/search.json?engine=bing_shopping&q=switch"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"shopping_results\": [\n    {\n      \"title\": \"String - Title of the item result\",\n      \"link\": \"String - URL to the item\",\n      \"thumbnails\": \"Array - List of URLs to the item thumbnails\",\n      \"seller\": \"String - Seller's name of the item\",\n      \"price\": \"String - Item price (Ex : '$14.99')\",\n      \"extracted_price\": \"Numeric - Item price as a float or integer (Ex: '14.99')\".,\n      \"old_price\": \"String - Item's price before discount (Ex: '$15.99')\",\n      \"extracted_old_price\": \"Numeric - Item's old price as float or integer (Ex: '15.99')\",\n      \"sale\": \"Boolean - Is the item on sale\",\n      \"price_drop\": \"String - The percentage of the price drop\",\n      \"installments\": {\n        \"price\": \"String - Displayed price, e.g. $0\",\n        \"text\": \"String - Instalment text, e.g. now\",\n        \"installments\": \"String - Instalment price to the item, e.g. $41.67/mo\",\n        \"duration\": \"String - Instalment duration in months, e.g. 24\",\n      }\n      \"rating\": \"Float - Rating of the item\",\n      \"reviews\": \"String - Number of reviews of the item\",\n      \"price_history_link\": \"String - Link to the price history\",\n      \"compare_sellers_link\": \"String - Link to comparing sellers\",\n      \"free_shipping\": \"Boolean - Is the item shipping for free\",\n      \"top_pick\": \"Boolean - Is the item on top pick\",\n      \"popular\": \"Boolean - Is the item popular\",\n      \"great_deal\": \"Boolean - Is the item on great deal\",\n      \"special_offer\": \"String - The content of item's special offer\",\n      \"ethical_choice\": \"String - The 'Good On You' rating for the item's brand\",\n      \"external_link\": \"String - External product link\",\n      \"product_token\": \"String - Product token of the item\",\n      \"serpapi_bing_product_api\": \"String - Link to the Bing Product API results of the product\"\n    }\n  ],\n  \"filters\": [\n    {\n      \"type\": \"String - Type of the filter\",\n      \"options\": [\n        {\n          \"text\": \"String - Name of the filter\",\n          \"link\": \"String - Link to the filter results in Bing Shopping\",\n          \"serpapi_link\": \"String - Link to the Bing Shopping results of the filter in JSON format by SerpApi\",\n        }\n      ]\n    }\n  ],\n  \"inline_ads_results\": [\n    {\n      \"title\": \"String - Title of the item result\",\n      \"link\": \"String - URL to the item\",\n      \"external_link\": \"String - External product link\",\n      \"thumbnail\": \"String - URL to the item's thumbnail\",\n      \"seller\": \"String - Seller's name of the item\",\n      \"price\": \"String - Item price (Ex : '$14.99')\",\n      \"extracted_price\": \"Numeric - Item price as a float or integer (Ex: '14.99')\".,\n      \"old_price\": \"String - Item's price before discount (Ex: '$15.99')\",\n      \"extracted_old_price\": \"Numeric - Item's old price as float or integer (Ex: '15.99')\",\n      \"block_position\": \"String - Position of the item on the page, one of 'top', 'middle' and 'bottom'\",\n      \"unit_price\": \"String - The unit price to the item\",\n      \"installments\": {\n        \"price\": \"String - Displayed price, e.g. $0\",\n        \"text\": \"String - Instalment text, e.g. now\",\n        \"installments\": \"String - Instalment price to the item, e.g. $41.67/mo\",\n        \"duration\": \"String - Instalment duration in months, e.g. 24\",\n      }\n      \"rating\": \"Float - Rating of the item\",\n      \"reviews\": \"String - Number of reviews of the item\",\n      \"free_shipping\": \"Boolean - Is the item shipping for free\",\n      \"tag\": {\n        \"top\": \"String - The tag to the item on the top\",\n        \"bottom\": \"String - The tag to the item on the bottom\",\n      }\n    }\n  ],\n  \"ads_results\": [\n    {\n      \"title\": \"String - Title of the item result\",\n      \"link\": \"String - URL to the item\",\n      \"displayed_link\": \"String - Displayed link to the item\",\n      \"price\": \"String - Price to the item\",\n      \"snippet\": \"String - Snippet to the item\",\n      \"extensions\": \"Array - List of extensions to the item result\",\n      \"sitelinks\": [\n        {\n          \"title\": \"Title to the sitelink\",\n          \"link\": \"URL to the sitelink\",\n        }\n      ]\n    }\n  ],\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "bing-shopping-api-api"
---

# Bing Shopping API

## 源URL

https://serpapi.com/bing-shopping-api

## 描述

Our Bing Shopping API allows you to scrape SERP results from Bing Shopping page.

The API endpoint is https://serpapi.com/search?engine=bing_shopping Head to the playground for a live and interactive demo.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Bing Shopping API allows you to scrape SERP results from Bing Shopping page.

The API endpoint is https://serpapi.com/search?engine=bing_shopping Head to the playground for a live and interactive demo.

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
