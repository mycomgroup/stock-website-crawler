---
id: "url-736eadf3"
type: "api"
title: "Amazon Filters API"
url: "https://serpapi.com/amazon-filters"
description: "SerpApi Amazon API scrapes the name, description, filter, and url of filters which are needed to narrow down the search results.\n\nThe API endpoint is https://serpapi.com/search?engine=amazon Head to the playground for a live and interactive demo.\n\nTo apply filters for the Amazon search, you need to update the rh parameter with the appropriate value. You can get the rh values for each filter from the filters array in the JSON results for an Amazon API search.The rh parameter is constructed in the following manner:key:valueTo apply multiple filters, use , (comma) to separate key:value pairs. For example: key:value+,+key:value"
source: ""
tags: []
crawl_time: "2026-03-18T07:49:13.597Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "amazon"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Results with rh values","description":"To apply filters for the Amazon search, you need to update the rh parameter with the appropriate value. You can get the rh values for each filter from the filters array in the JSON results for an Amazon API search. The rh parameter is constructed in the following manner:key:value To apply multiple filters, use , (comma) to separate key:value pairs. For example: key:value+,+key:value","requestParams":{"engine":"amazon","k":"coffee","rh":"p_76:1249146011,p_90:8308921011","highlight":"filters"},"responseJson":"https://serpapi.com/search.json?engine=amazon&k=coffee&rh=p_76:1249146011,p_90:8308921011"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"filters\": [\n    \"snake_case name of the filter (Ex: 'eligible_for_free_shipping')\": [\n      {\n        \"name\": \"String - Filter name\",\n        \"description\": \"String - Filter description\",\n        \"rh\": \"String - 'rh' value (Ex: 'p_76:1249146011')\",\n        \"url\": \"String - Link to the Amazon search\",\n        \"serpapi_url\": \"String - Link to the SerpApi search\",\n        \"used\": \"Boolean - Returns 'true' if filter is applied\"\n      }\n    ],\n    ...\n  ],\n  ...\n}"}
  importantNotes:
    - "To apply filters for the Amazon search, you need to update the rh parameter with the appropriate value. You can get the rh values for each filter from the filters array in the JSON results for an Amazon API search.The rh parameter is constructed in the following manner:key:valueTo apply multiple filters, use , (comma) to separate key:value pairs. For example: key:value+,+key:value"
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "amazon-filters-api"
---

# Amazon Filters API

## 源URL

https://serpapi.com/amazon-filters

## 描述

SerpApi Amazon API scrapes the name, description, filter, and url of filters which are needed to narrow down the search results.

The API endpoint is https://serpapi.com/search?engine=amazon Head to the playground for a live and interactive demo.

To apply filters for the Amazon search, you need to update the rh parameter with the appropriate value. You can get the rh values for each filter from the filters array in the JSON results for an Amazon API search.The rh parameter is constructed in the following manner:key:valueTo apply multiple filters, use , (comma) to separate key:value pairs. For example: key:value+,+key:value

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 注意事项

- To apply filters for the Amazon search, you need to update the rh parameter with the appropriate value. You can get the rh values for each filter from the filters array in the JSON results for an Amazon API search.The rh parameter is constructed in the following manner:key:valueTo apply multiple filters, use , (comma) to separate key:value pairs. For example: key:value+,+key:value

## 文档正文

SerpApi Amazon API scrapes the name, description, filter, and url of filters which are needed to narrow down the search results.

The API endpoint is https://serpapi.com/search?engine=amazon Head to the playground for a live and interactive demo.

To apply filters for the Amazon search, you need to update the rh parameter with the appropriate value. You can get the rh values for each filter from the filters array in the JSON results for an Amazon API search.The rh parameter is constructed in the following manner:key:valueTo apply multiple filters, use , (comma) to separate key:value pairs. For example: key:value+,+key:value

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
