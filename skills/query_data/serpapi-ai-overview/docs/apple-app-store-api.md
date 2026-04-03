---
id: "url-7628a51f"
type: "api"
title: "Apple App Store Search Scraper API"
url: "https://serpapi.com/apple-app-store"
description: "Our Apple App Store Search API allows you to scrape results from the Apple App Store search page.\n\nThe API endpoint is https://serpapi.com/search?engine=apple_app_store Head to the playground for a live and interactive demo."
source: ""
tags: []
crawl_time: "2026-03-18T09:09:16.599Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"organic_results\": [\n    {\n      \"position\": \"Integer - Position of the App. (Ex. 1)\",\n      \"id\": \"Integer - Unique app id that helps you lookup more of the app details in other engines. (Ex. 1339438881)\",\n      \"title\": \"String - Title of the app. (Ex. Easy CSV Editor)\",\n      \"bundle_id\": \"String - Unique bundle id. Usually reversed version of the app's website. (Ex. com.amazon.aiv.AIVApp)\",\n      \"version\": \"String - Version Number of the app. (Ex. 6.4.6)\",\n      \"vpp_license\": \"Boolean - Apple VPP (Volume Purchase Program) License. It allows bussinesses to buy the app in sums. (Ex. true)\",\n      \"age_rating\": \"String - Age Rating. (Ex. 7+)\",\n      \"release_note\": \"String - Latest software update release notes. (Ex. Supercharge your worksheets with fourteen new text and array functions in Excel.)\",\n      \"minimum_os_version\": \"String - Minimum OS version needed to install apps. (Ex. 12.0)\",\n      \"description\": \"String - Description of the app. (Ex. Learn Python Data Scraping, Automation Algorithms, BeautifulSoup, Pandas Dataframes, Numpy, Machine Learning, Sentiment Analysis and many other topics in details with easy to understand tutorial videos.)\",\n      \"game_center_enabled\": \"Boolean - Apple Game Center availability. It lets users play with other friends on the platform with their identity. (Ex. false)\",\n      \"link\": \"String - Product page of the app, former iTunes Store link. (Ex. https://apps.apple.com/us/app/id61889819e7d08a1d5c5ea6d4)\",\n      \"serpapi_product_link\": \"String - Link to SerpApi’s App Store Product Page Scraper API that allows you to scrape data from product web pages containing deeper information about the app. (Ex. https://serpapi.com/search.json?engine=apple_product&product_id=534220544&country=us)\",\n      \"serpapi_reviews_link\": \"String - Link to SerpApi's App Store Reviews Scraper API that lets you to scrape App Store Reviews. (Ex: https://serpapi.com/search.json?engine=apple_reviews&country=us&product_id=409882593)\",\n      \"release_date\": \"String - Release Date of the app (Ex. 2018-02-06 04:02:02 UTC)\",\n      \"latest_version_release_date\": \"String - Release Date of the latest version of the app (Ex. 2023-02-06 04:02:02 UTC)\",\n      \"price\": {\n        \"type\": \"String - Price Type of the Product. Could be 'Free', 'Paid', or 'Free Trial'\",\n        \"amount\": \"Integer or Float - Price amount of the app. Not returned if it is a free app. (Ex. 4.99)\",\n        \"currency\": \"String - Three letter abbreviation of the currency. (Ex. USD)\",\n        \"symbol\": \"String - Symbol of the currency (Ex. $)\"\n      },\n      \"rating\": [\n        {\n          \"type\": \"String - Type of the rating. It could be for all times, or from the latest update etc. (Ex. All Times)\",\n          \"rating\": \"Float - Average rating of the app. (Ex. 4.6)\",\n          \"count\": \"Integer - Total number of reviews. (Ex. 5016)\"\n        }\n      ],\n      \"genres\": [\n        {\n          \"name\": \"String - Genre of the app. (Ex. Productivity)\",\n          \"id\": \"Integer - Unique identifying number of the genre. (Ex. 6023)\",\n          \"primary\": \"Boolean - If the genre is primary genre of the app or not. (Ex. true)\"\n        },\n        ...\n      ],\n      \"developer\": {\n        \"name\": \"String - Developer Name. (Ex. Apple Inc.)\",\n        \"id\": \"Integer - Unique developer id. (Ex. 1291620790)\",\n        \"link\": \"String - Developer page. (Ex. https://apps.apple.com/us/developer/id1291620790)\"\n      },\n      \"size_in_bytes\": \"Integer - Size of the app in bytes. (Ex. 80698368)\",\n      \"supported_languages\": [\n        \"String - Two letter abbreviation of the supported language. (Ex. EN)\",\n        ...\n      ],\n      \"screenshots\": {\n        \"iphone_screenshots\": [\n          {\n            \"link\": \"String - Link of the screenshot. (Ex. https://is5-ssl.mzstatic.com/image/thumb/PurpleSource125/v4/be/90/c5/be90c518-44d1-bb50-38a2-6ff68d61f7f1/fe82090c-7953-483b-9d69-89a7e13c14a2_5.5-Inch_1st.jpg/392x696bb.jpg)\",\n            \"size\": \"String - Size of the image. (Ex. 392x696)\"\n          },\n          ...\n        ],\n        ...\n      },\n      \"logos\": [\n        {\n          \"size\": \"String - Size of the logo. (Ex. 60x60)\",\n          \"link\": \"String - Link of the logo. (Ex. https://is5-ssl.mzstatic.com/image/thumb/Purple116/v4/39/4a/a4/394aa4f8-fd68-2bfb-6619-2a38abfebf4b/source/60x60bb.jpg)\"\n        },\n        ...\n      ],\n      \"features\": [\n        \"String - Supported functionality features. (Ex. iosUniversal)\"\n      ],\n      \"advisories\": [\n        \"String - Advisory text. (Ex. Infrequent/Mild Cartoon or Fantasy Violence)\"\n      ],\n      \"supported_devices\": [\n        \"String - Supported device. (Ex. iPhone5s)\",\n        ...\n      ]\n    },\n  ],\n  ...\n}"}
    - {"title":"Apple App Store search results for term: TestFlight","description":"","requestParams":{"engine":"apple_app_store","term":"TestFlight","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=apple_app_store&term=TestFlight"}
    - {"title":"Apple App Store search results for term: Netflix, and device: tablet","description":"","requestParams":{"engine":"apple_app_store","term":"Netflix","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=apple_app_store&term=Netflix"}
    - {"title":"Apple App Store search results for term: CheatSheet, and device: desktop","description":"","requestParams":{"engine":"apple_app_store","device":"desktop","term":"CheatSheet","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=apple_app_store&device=desktop&term=CheatSheet"}
    - {"title":"Apple App Store search results for term: Ubisoftand property: developer (Apps by Developer)","description":"","requestParams":{"engine":"apple_app_store","term":"Ubisoft","property":"developer","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=apple_app_store&term=Ubisoft&property=developer"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "apple-app-store-api"
---

# Apple App Store Search Scraper API

## 源URL

https://serpapi.com/apple-app-store

## 描述

Our Apple App Store Search API allows you to scrape results from the Apple App Store search page.

The API endpoint is https://serpapi.com/search?engine=apple_app_store Head to the playground for a live and interactive demo.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Apple App Store Search API allows you to scrape results from the Apple App Store search page.

The API endpoint is https://serpapi.com/search?engine=apple_app_store Head to the playground for a live and interactive demo.

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
