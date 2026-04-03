---
id: "url-4efd0370"
type: "api"
title: "Yandex Search Engine Results API"
url: "https://serpapi.com/yandex-search-api"
description: "Our Yandex Search API allows you to scrape results from the Yandex search page.\n\nThe API endpoint is https://serpapi.com/search?engine=yandex Head to the playground for a live and interactive demo.\n\nNote that lang have to be set to null to make the search work\n\nYandex Search API supports multiple languages. You can specify the language of the search results using the lang parameter. The lang parameter accepts a comma-separated two-letter list of languages."
source: ""
tags: []
crawl_time: "2026-03-18T17:31:01.919Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Example results for text: coffee","description":"","requestParams":{"engine":"yandex","text":"coffee","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=yandex&text=coffee"}
    - {"title":"More complex examples with multiple optional parameters","description":"The URL below fetches: • The forth page (p=3) of the results, • for the search \"apple\" (q=apple), • with the French language and domain (lang=fr, yandex_domain=yandex.com.fr)","requestParams":{"engine":"yandex","text":"apple","p":"3","lang":"fr","yandex_domain":"yandex.com.fr"},"responseJson":"https://serpapi.com/search.json?engine=yandex&text=apple&p=3&lang=fr&yandex_domain=yandex.com.fr"}
    - {"title":"Example using | (OR) operator","description":"Note that lang have to be set to null to make the search work","requestParams":{"engine":"yandex","text":"Late Breakfast | Early Lunch","lr":"84","lang":"null","yandex_domain":"yandex.com"},"responseJson":"https://serpapi.com/search.json?engine=yandex&text=Late+Breakfast+|+Early+Lunch&lr=84&lang=null&yandex_domain=yandex.com"}
    - {"title":"Example results for text: Coffee, lang: ru,en","description":"Yandex Search API supports multiple languages. You can specify the language of the search results using the lang parameter. The lang parameter accepts a comma-separated two-letter list of languages.","requestParams":{"engine":"yandex","text":"Coffee","lang":"ru,en","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=yandex&text=Coffee&lang=ru,en"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  \"organic_results\": [\n    {\n      \"position\": \"Integer - Organic result position\",\n      \"title\": \"String - Organic result title\",\n      \"link\": \"String - Organic result link\",\n      \"displayed_link\": \"String - Organic result displayed link\",\n      \"snippet\": \"String - Organic result snippet\",\n    },\n    ...\n  ],\n  \"knowledge_graph\": {\n    \"title\": \"String - Knowledge graph title\",\n    ...\n  }\n}"}
  importantNotes:
    - "Yandex Search API supports multiple languages. You can specify the language of the search results using the lang parameter. The lang parameter accepts a comma-separated two-letter list of languages."
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "yandex-search-api-api"
---

# Yandex Search Engine Results API

## 源URL

https://serpapi.com/yandex-search-api

## 描述

Our Yandex Search API allows you to scrape results from the Yandex search page.

The API endpoint is https://serpapi.com/search?engine=yandex Head to the playground for a live and interactive demo.

Note that lang have to be set to null to make the search work

Yandex Search API supports multiple languages. You can specify the language of the search results using the lang parameter. The lang parameter accepts a comma-separated two-letter list of languages.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 注意事项

- Yandex Search API supports multiple languages. You can specify the language of the search results using the lang parameter. The lang parameter accepts a comma-separated two-letter list of languages.

## 文档正文

Our Yandex Search API allows you to scrape results from the Yandex search page.

The API endpoint is https://serpapi.com/search?engine=yandex Head to the playground for a live and interactive demo.

Note that lang have to be set to null to make the search work

Yandex Search API supports multiple languages. You can specify the language of the search results using the lang parameter. The lang parameter accepts a comma-separated two-letter list of languages.

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
