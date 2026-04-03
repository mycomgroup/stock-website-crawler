---
id: "url-35deedf6"
type: "api"
title: "Google Trends API"
url: "https://serpapi.com/google-trends-api"
description: "Our Google Trends API allows you to scrape results from the Google Trends search page.\n\nThe API endpoint is https://serpapi.com/search?engine=google_trends Head to the playground for a live and interactive demo.\n\nA Google Trends search without a query is valid with filters (cat). In this example, it is filtered to show only TIMESERIES results from the category 319 (Cartoons).\n\nThe tz parameter in our Google Trends API is calculated as the UTC offset in minutes.For instance, consider Tokyo, which operates on JST (UTC+9). If the local time is 3:00 PM in Tokyo, UTC time is 6:00 AM. The calculation for tz would be (9 hours ahead of UTC) * 60 minutes, resulting in a tz value of -540. (If you subtract 540 minutes, you get back to UTC.) This parameter ensures that time-sensitive data aligns correctly with the selected region’s local time.Additionally, the tz parameter influences search results based on different date parameter values. For example, in queries like \"sakura,\" the effect of tz can be observed up to 7 days of data (using \"now 7-d\" as the date parameter). Any date value below 7 days will still affect the results. This impact might vary for different queries and their respective date parameters.It is important to adjust this value based on daylight saving changes or other time variations to maintain data accuracy. The tz range spans from -1439 to 1439, allowing for granular control over time zone settings in the API response.To make sure the value is correct, please refer to the time zone database and your programming language UTC offset calculation.\n\nParameter include_low_search_volume can be set to true for including low search volume regions in the results."
source: ""
tags: []
crawl_time: "2026-03-18T17:26:08.901Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Interest over time chart with q: coffee,milk,bread,pasta,steak and data_type: TIMESERIES","description":"","requestParams":{"engine":"google_trends","q":"coffee,milk,bread,pasta,steak","data_type":"TIMESERIES","highlight":"interest_over_time"},"responseJson":"https://serpapi.com/search.json?engine=google_trends&q=coffee,milk,bread,pasta,steak&data_type=TIMESERIES"}
    - {"title":"Compared breakdown by region chart with q: coffee,milk,bread,pasta,steak and data_type: GEO_MAP","description":"","requestParams":{"engine":"google_trends","q":"coffee,milk,bread,pasta,steak","data_type":"GEO_MAP","highlight":"compared_breakdown_by_region"},"responseJson":"https://serpapi.com/search.json?engine=google_trends&q=coffee,milk,bread,pasta,steak&data_type=GEO_MAP"}
    - {"title":"Interest by region chart with q: coffee and data_type: GEO_MAP_0","description":"","requestParams":{"engine":"google_trends","q":"coffee","data_type":"GEO_MAP_0","highlight":"interest_by_region"},"responseJson":"https://serpapi.com/search.json?engine=google_trends&q=coffee&data_type=GEO_MAP_0"}
    - {"title":"Related topics chart with q: coffee and data_type: RELATED_TOPICS","description":"","requestParams":{"engine":"google_trends","q":"coffee","data_type":"RELATED_TOPICS","highlight":"related_topics"},"responseJson":"https://serpapi.com/search.json?engine=google_trends&q=coffee&data_type=RELATED_TOPICS"}
    - {"title":"Related queries chart with q: coffee and data_type: RELATED_QUERIES","description":"","requestParams":{"engine":"google_trends","q":"coffee","data_type":"RELATED_QUERIES","highlight":"related_queries"},"responseJson":"https://serpapi.com/search.json?engine=google_trends&q=coffee&data_type=RELATED_QUERIES"}
    - {"title":"Search results for a specified category with no query provided","description":"A Google Trends search without a query is valid with filters (cat). In this example, it is filtered to show only TIMESERIES results from the category 319 (Cartoons).","requestParams":{"engine":"google_trends","cat":"319"},"responseJson":"https://serpapi.com/search.json?engine=google_trends&cat=319"}
    - {"title":"Understanding the tz parameter","description":"The tz parameter in our Google Trends API is calculated as the UTC offset in minutes. For instance, consider Tokyo, which operates on JST (UTC+9). If the local time is 3:00 PM in Tokyo, UTC time is 6:00 AM. The calculation for tz would be (9 hours ahead of UTC) * 60 minutes, resulting in a tz value of -540. (If you subtract 540 minutes, you get back to UTC.) This parameter ensures that time-sensitive data aligns correctly with the selected region’s local time. Additionally, the tz parameter influences search results based on different date parameter values. For example, in queries like \"sakura,\" the effect of tz can be observed up to 7 days of data (using \"now 7-d\" as the date parameter). Any date value below 7 days will still affect the results. This impact might vary for different queries and their respective date parameters. It is important to adjust this value based on daylight saving changes or other time variations to maintain data accuracy. The tz range spans from -1439 to 1439, allowing for granular control over time zone settings in the API response. To make sure the value is correct, please refer to the time zone database and your programming language UTC offset calculation.","requestParams":{"engine":"google_trends","q":"sakura","date":"now 7-d","tz":"-540","data_type":"TIMESERIES","highlight":"interest_over_time"},"responseJson":"https://serpapi.com/search.json?engine=google_trends&q=sakura&date=now+7-d&tz=-540&data_type=TIMESERIES"}
    - {"title":"Compared breakdown by region q: Football, Basketball, Golf, data_type: GEO_MAP and include_low_search_volume: true","description":"Parameter include_low_search_volume can be set to true for including low search volume regions in the results.","requestParams":{"engine":"google_trends","q":"Football, Basketball, Golf","data_type":"GEO_MAP","include_low_search_volume":"true","highlight":"compared_breakdown_by_region"},"responseJson":"https://serpapi.com/search.json?engine=google_trends&q=Football,+Basketball,+Golf&data_type=GEO_MAP&include_low_search_volume=true"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nBilling Information\n\nChange Plan\n\nEdit Profile\n\nExtra Credits\n\nYour API Metrics\n\nAPI Absolute Numbers\n\nAPI Engines\n\nAPI Response Times\n\nAPI Success Rates\n\nYour Searches\n\nYour Playground\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API"
  suggestedFilename: "google-trends-api-api"
---

# Google Trends API

## 源URL

https://serpapi.com/google-trends-api

## 描述

Our Google Trends API allows you to scrape results from the Google Trends search page.

The API endpoint is https://serpapi.com/search?engine=google_trends Head to the playground for a live and interactive demo.

A Google Trends search without a query is valid with filters (cat). In this example, it is filtered to show only TIMESERIES results from the category 319 (Cartoons).

The tz parameter in our Google Trends API is calculated as the UTC offset in minutes.For instance, consider Tokyo, which operates on JST (UTC+9). If the local time is 3:00 PM in Tokyo, UTC time is 6:00 AM. The calculation for tz would be (9 hours ahead of UTC) * 60 minutes, resulting in a tz value of -540. (If you subtract 540 minutes, you get back to UTC.) This parameter ensures that time-sensitive data aligns correctly with the selected region’s local time.Additionally, the tz parameter influences search results based on different date parameter values. For example, in queries like "sakura," the effect of tz can be observed up to 7 days of data (using "now 7-d" as the date parameter). Any date value below 7 days will still affect the results. This impact might vary for different queries and their respective date parameters.It is important to adjust this value based on daylight saving changes or other time variations to maintain data accuracy. The tz range spans from -1439 to 1439, allowing for granular control over time zone settings in the API response.To make sure the value is correct, please refer to the time zone database and your programming language UTC offset calculation.

Parameter include_low_search_volume can be set to true for including low search volume regions in the results.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Google Trends API allows you to scrape results from the Google Trends search page.

The API endpoint is https://serpapi.com/search?engine=google_trends Head to the playground for a live and interactive demo.

A Google Trends search without a query is valid with filters (cat). In this example, it is filtered to show only TIMESERIES results from the category 319 (Cartoons).

The tz parameter in our Google Trends API is calculated as the UTC offset in minutes.For instance, consider Tokyo, which operates on JST (UTC+9). If the local time is 3:00 PM in Tokyo, UTC time is 6:00 AM. The calculation for tz would be (9 hours ahead of UTC) * 60 minutes, resulting in a tz value of -540. (If you subtract 540 minutes, you get back to UTC.) This parameter ensures that time-sensitive data aligns correctly with the selected region’s local time.Additionally, the tz parameter influences search results based on different date parameter values. For example, in queries like "sakura," the effect of tz can be observed up to 7 days of data (using "now 7-d" as the date parameter). Any date value below 7 days will still affect the results. This impact might vary for different queries and their respective date parameters.It is important to adjust this value based on daylight saving changes or other time variations to maintain data accuracy. The tz range spans from -1439 to 1439, allowing for granular control over time zone settings in the API response.To make sure the value is correct, please refer to the time zone database and your programming language UTC offset calculation.

Parameter include_low_search_volume can be set to true for including low search volume regions in the results.

## API 端点

**Method:** `GET`
**Endpoint:** `https://serpapi.com/search`

Api Dashboard

Api Dashboard

Your Account

Billing Information

Change Plan

Edit Profile

Extra Credits

Your API Metrics

API Absolute Numbers

API Engines

API Response Times

API Success Rates

Your Searches

Your Playground

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
