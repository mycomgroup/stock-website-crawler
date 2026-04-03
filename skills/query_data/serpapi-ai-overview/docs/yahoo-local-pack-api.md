---
id: "url-10313c97"
type: "api"
title: "Yahoo! Local Pack API"
url: "https://serpapi.com/yahoo-local-pack"
description: "For some requests, Yahoo search includes local results, called local pack, and a local map. SerpApi is able to scrape, extract, and make sense of this information.When SerpApi encounters a local map and/or local results, we add them to our JSON output.From the local_map, we are able to extract link and image information. From the local_results, we are able to extract position, title, reviews, price, address, hours, thumbnail, gps_coordinates, place_id and more.\n\nThe API endpoint is https://serpapi.com/search?engine=yahoo Head to the playground for a live and interactive demo."
source: ""
tags: []
crawl_time: "2026-03-18T13:01:54.281Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Local pack results overview","description":"","requestParams":{"engine":"yahoo","p":"Coffee Shop New York","highlight":"local_results"},"responseJson":"{\n  ...\n  \"local_map\": {\n    \"link\": \"https://search.yahoo.com/local/s;_ylt=AwrFOCqY3AlkbCIPp1RXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3Nj?p=Coffee+Shop+New+York&ei=UTF-8&fr=fp-tts\",\n    \"image\": \"https://sgws2.maps.yahoo.com/mapimage?mflags=MKY&appid=search&locale=en_US&imf=jpg&imw=616&imh=200&poi=%3B%2CA-blue-xs-gws.png%2C40.745709%2C-73.988184%3B%2CB-blue-xs-gws.png%2C40.72396%2C-73.99643%3B%2CC-blue-xs-gws.png%2C40.733782%2C-73.99312%3B%2CDot-xs-gws.png%2C40.717247%2C-74.010135%3B%2CDot-xs-gws.png%2C40.757917%2C-73.983198%3B%2CDot-xs-gws.png%2C40.732807%2C-73.997953\"\n  },\n  \"local_results\": {\n    \"more_locations_link\": \"https://search.yahoo.com/local/s;_ylt=AwrFOCqY3AlkbCIP3lRXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3Nj?p=Coffee+Shop+New+York&ei=UTF-8&fr=fp-tts\",\n    \"places\": [\n      {\n        \"position\": 1,\n        \"place_id\": \"117569391\",\n        \"title\": \"Stumptown Coffee Roasters\",\n        \"place_id_search\": \"https://search.yahoo.com/local/s;_ylt=AwrFOCqY3AlkbCIPvFRXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3Nj?p=Coffee+Shop+New+York&ei=UTF-8&selectedId=117569391&fr=fp-tts\",\n        \"type\": \"Coffee House, Coffee & Tea\",\n        \"price\": \"$$\",\n        \"rating\": 4.5,\n        \"reviews\": 1438,\n        \"address\": \"20 W 29th St, New York, NY\",\n        \"phone\": \"(855) 711-3385\",\n        \"thumbnail\": \"https://s.yimg.com/fz/api/res/1.2/BSHMhIK2ii6RPYyutZyxQg--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD0xODA7cT04MDt3PTE4MA--/https://s.yimg.com/bj/859c/859c0d243bcb8acd9a8ff271e6fdbaa4.jpg\",\n        \"links\": {\n          \"website\": \"https://www.stumptowncoffee.com/\"\n        },\n        \"gps_coordinates\": {\n          \"latitude\": \"40.745709\",\n          \"longitude\": \"-73.988184\"\n        }\n      },\n      {\n        \"position\": 2,\n        \"place_id\": \"77525819\",\n        \"title\": \"La Colombe SOHO\",\n        \"place_id_search\": \"https://search.yahoo.com/local/s;_ylt=AwrFOCqY3AlkbCIPwFRXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3Nj?p=Coffee+Shop+New+York&ei=UTF-8&selectedId=77525819&fr=fp-tts\",\n        \"type\": \"Coffee House, Coffee & Tea\",\n        \"price\": \"$$\",\n        \"rating\": 4.5,\n        \"reviews\": 702,\n        \"address\": \"270 Lafayette St, New York, NY\",\n        \"phone\": \"(212) 625-1717\",\n        \"thumbnail\": \"https://s.yimg.com/fz/api/res/1.2/77Lu1ggSpHw6jy6Ky1gogQ--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD0xODA7cT04MDt3PTE4MA--/https://s.yimg.com/bj/64af/64af3e8464367b8b943a3315afdb3ed2.jpg\",\n        \"links\": {\n          \"website\": \"https://www.lacolombe.com/\",\n          \"menu\": \"https://places.singleplatform.com/la-colombe/menu?ref=Yahoo\"\n        }\n      },\n      {\n        \"position\": 3,\n        \"place_id\": \"42501129\",\n        \"title\": \"The Grey Dog - Union Square\",\n        \"place_id_search\": \"https://search.yahoo.com/local/s;_ylt=AwrFOCqY3AlkbCIPxlRXNyoA;_ylu=Y29sbwNiZjEEcG9zAzEEdnRpZAMEc2VjA3Nj?p=Coffee+Shop+New+York&ei=UTF-8&selectedId=42501129&fr=fp-tts\",\n        \"type\": \"Coffee House\",\n        \"price\": \"$$\",\n        \"rating\": 4,\n        \"reviews\": 1173,\n        \"address\": \"90 University Pl, New York, NY\",\n        \"phone\": \"(212) 966-1060\",\n        \"thumbnail\": \"https://s.yimg.com/fz/api/res/1.2/3jj_POYE4nztw602JbactA--~C/YXBwaWQ9c3JjaGRkO2ZpPWZpbGw7aD0xODA7cT04MDt3PTE4MA--/https://s.yimg.com/bj/91bf/91bf63978de6aa47a0f25c56800f17fe.jpg\",\n        \"links\": {\n          \"website\": \"https://order.thegreydog.com/location/university-place\",\n          \"menu\": \"https://places.singleplatform.com/grey-dog-coffee/menu?ref=Yahoo\"\n        }\n      },\n      ...\n    ]\n  },\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "yahoo-local-pack-api"
---

# Yahoo! Local Pack API

## 源URL

https://serpapi.com/yahoo-local-pack

## 描述

For some requests, Yahoo search includes local results, called local pack, and a local map. SerpApi is able to scrape, extract, and make sense of this information.When SerpApi encounters a local map and/or local results, we add them to our JSON output.From the local_map, we are able to extract link and image information. From the local_results, we are able to extract position, title, reviews, price, address, hours, thumbnail, gps_coordinates, place_id and more.

The API endpoint is https://serpapi.com/search?engine=yahoo Head to the playground for a live and interactive demo.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

For some requests, Yahoo search includes local results, called local pack, and a local map. SerpApi is able to scrape, extract, and make sense of this information.When SerpApi encounters a local map and/or local results, we add them to our JSON output.From the local_map, we are able to extract link and image information. From the local_results, we are able to extract position, title, reviews, price, address, hours, thumbnail, gps_coordinates, place_id and more.

The API endpoint is https://serpapi.com/search?engine=yahoo Head to the playground for a live and interactive demo.

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
