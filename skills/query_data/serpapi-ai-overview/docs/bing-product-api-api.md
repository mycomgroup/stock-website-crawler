---
id: "url-7a434550"
type: "api"
title: "Bing Product API"
url: "https://serpapi.com/bing-product-api"
description: "Our Bing Product API allows you to scrape SERP results from Bing Product.\n\nThe API endpoint is https://serpapi.com/search?engine=bing_product Head to the playground for a live and interactive demo."
source: ""
tags: []
crawl_time: "2026-03-18T11:57:35.283Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Example with product_token","description":"","requestParams":{"engine":"bing_product","product_token":"pc13NHicdY3BbsIwEETVjyES8oUaEXrJAWgJqBQiwg-YeEOsWF53vRblV_s1jRIOPcBlR_tmRvP7Mv7O9qYFsbSqasWnsTY0yEKKHShugETpQLVAIamN5U6zUIFTZHA0VSMpX-fdEZfTzcMdyB5s9fDKVM5nMp1M32bp3dio0AzmpCe5xbOyh7oG2urwuLaI1Qodww_n0eh_7Zww-g_Hhm_PJvfoSo8uIIHuV4bYiSJ0knhCHSv26gIZdyxZH45fWbkpivciORNew8D_AJZIW7o","highlight":"product_results"},"responseJson":"https://serpapi.com/search.json?engine=bing_product&product_token=pc13NHicdY3BbsIwEETVjyES8oUaEXrJAWgJqBQiwg-YeEOsWF53vRblV_s1jRIOPcBlR_tmRvP7Mv7O9qYFsbSqasWnsTY0yEKKHShugETpQLVAIamN5U6zUIFTZHA0VSMpX-fdEZfTzcMdyB5s9fDKVM5nMp1M32bp3dio0AzmpCe5xbOyh7oG2urwuLaI1Qodww_n0eh_7Zww-g_Hhm_PJvfoSo8uIIHuV4bYiSJ0knhCHSv26gIZdyxZH45fWbkpivciORNew8D_AJZIW7o"}
    - {"title":"Variants Example","description":"","requestParams":{"engine":"bing_product","product_token":"LL6gs3icdY9NDoIwEIXjRdzJpjGRQkAXLPxFFwpRL1DpIE1Ip_YnylU9jQRYuNDNTOZ78_Ly3qPxI1kqVQOZEpFXKIH4IfHpPF0RDdwrRW1Bm8QUIJkWOAnYhFI_bge5XxsFA6AdOPDhjIKQhmFEZ_FiEPbMVL0460ha443VWVmCPnDz27Z0xRqlhZdNneBf7lSjU1tphW3-RZ5QXhRKg22LLqV_u2oH7fKURu4Kq9gdEtsyb5edj8lln-eb3LtpfJqefwBAaFYI","highlight":"variants"},"responseJson":"https://serpapi.com/search.json?engine=bing_product&product_token=LL6gs3icdY9NDoIwEIXjRdzJpjGRQkAXLPxFFwpRL1DpIE1Ip_YnylU9jQRYuNDNTOZ78_Ly3qPxI1kqVQOZEpFXKIH4IfHpPF0RDdwrRW1Bm8QUIJkWOAnYhFI_bge5XxsFA6AdOPDhjIKQhmFEZ_FiEPbMVL0460ha443VWVmCPnDz27Z0xRqlhZdNneBf7lSjU1tphW3-RZ5QXhRKg22LLqV_u2oH7fKURu4Kq9gdEtsyb5edj8lln-eb3LtpfJqefwBAaFYI"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"product_results\": [\n    {\n      \"title\": \"String - Title of the item\",\n      \"description\": \"String - Description of the item\",\n      \"rating\": \"Float - Rating of the item\",\n      \"reviews\": \"String - Number of reviews of the item\",\n      \"thumbnails\": [\n        \"String - URL to the item thumbnail\",\n        ...\n      ],\n      \"images\": [\n        \"String - URL to the item image\",\n        ...\n      ],\n      \"specifications\": {\n        \"snake_case name of specifications (e.g. capacity)\": \"String - Value of the specifications\",\n        ...\n      }\n    }\n  ],\n  \"reviews_results\": {\n    \"ratings\": [\n      {\n        \"stars\": \"Integer - Number of stars\",\n        \"percentage\": \"Integer - Percentage of reviews with the number of stars\"\n      }\n    ]\n  },\n  \"buying_options\": [\n    {\n      \"seller_name\": \"String - Seller's name\",\n      \"seller_logo\": \"String - URL to the seller's logo\",\n      \"price\": \"String - Item price (Ex : '$14.99')\",\n      \"extracted_price\": \"Numeric - Item price as a float or integer (Ex: '14.99')\",\n      \"old_price\": \"String - Item's price before discount (Ex: '$15.99')\",\n      \"extracted_old_price\": \"Numeric - Item's old price as float or integer (Ex: '15.99')\",\n      \"installments\": {\n        \"price\": \"String - Displayed price, e.g. $0\",\n        \"text\": \"String - Instalment text, e.g. now\",\n        \"installments\": \"String - Instalment price to the item, e.g. $41.67/mo\",\n        \"duration\": \"String - Instalment duration in months, e.g. 24\",\n      },\n      \"link\": \"String - URL to the item\",\n      \"free_shipping\": \"Boolean - Returns `true` if the item has free shipping\",\n      \"ad\": \"Boolean - Returns `true` if the item is an ad\"\n    }\n  ],\n  \"variants\": [\n    {\n      \"title\": \"String - Title of the variant\",\n      \"items\": [\n        {\n          \"name\": \"String - Name of the variant\",\n          \"link\": \"String - URL to the variant\",\n          \"image\": \"String - URL to the variant image\"\n        }\n      ]\n    }\n  ]\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "bing-product-api-api"
---

# Bing Product API

## 源URL

https://serpapi.com/bing-product-api

## 描述

Our Bing Product API allows you to scrape SERP results from Bing Product.

The API endpoint is https://serpapi.com/search?engine=bing_product Head to the playground for a live and interactive demo.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Bing Product API allows you to scrape SERP results from Bing Product.

The API endpoint is https://serpapi.com/search?engine=bing_product Head to the playground for a live and interactive demo.

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
