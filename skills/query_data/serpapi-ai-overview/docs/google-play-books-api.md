---
id: "url-32d28284"
type: "api"
title: "Google Play Books Store API"
url: "https://serpapi.com/google-play-books"
description: "Our Google Play Books Store API allows you to scrape SERP results from Google Play Books & Audiobooks Store.\n\nThree types of searches you can do are: - Query Search: by using q parameter - Category Search: by using books_category parameter - Plain Search: without using q or books_category parameters\n\nThe API endpoint is https://serpapi.com/search?engine=google_play_books Head to the playground for a live and interactive demo."
source: ""
tags: []
crawl_time: "2026-03-18T17:22:50.909Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Rows Type Organic results overview for Google Play Books (Plain Search)","description":"","requestParams":{"engine":"google_play_books","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=google_play_books"}
    - {"title":"List Type Organic results overview for Google Play Books with section_page_token(Plain Search)","description":"","requestParams":{"engine":"google_play_books","q":"Coffee","section_page_token":"Cgj6noGdAwIIFBAUGjKyAi8KJwohcHJvbW90aW9uXzEwMDI0ZDhfYmlnX2Jvb2tzX21vbnRoEEQYASIECAUILA","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=google_play_books&q=Coffee&section_page_token=Cgj6noGdAwIIFBAUGjKyAi8KJwohcHJvbW90aW9uXzEwMDI0ZDhfYmlnX2Jvb2tzX21vbnRoEEQYASIECAUILA"}
    - {"title":"Rows Type Organic results overview for Google Play Books with next_page_token(Plain Search)","description":"","requestParams":{"engine":"google_play_books","next_page_token":"Cgiq5rbCAwIIBRAE","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=google_play_books&next_page_token=Cgiq5rbCAwIIBRAE"}
    - {"title":"List Type Organic results overview for Google Play Books with see_more_token(Plain Search)","description":"","requestParams":{"engine":"google_play_books","see_more_token":"CjeyAjQKLAomcHJvbW90aW9uX2Vib29rc19fZGVidXRfYXV0aG9yX2NsdXN0ZXIQRBgBIgQIBQgs:S:ANO1ljJzTCM","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=google_play_books&see_more_token=CjeyAjQKLAomcHJvbW90aW9uX2Vib29rc19fZGVidXRfYXV0aG9yX2NsdXN0ZXIQRBgBIgQIBQgs:S:ANO1ljJzTCM"}
    - {"title":"Top Charts results overview for Google Play Books with chart(Plain Search)","description":"","requestParams":{"engine":"google_play_books","chart":"top_deals","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=google_play_books&chart=top_deals"}
    - {"title":"Rows Type Organic results overview for Google Play Books with books_category(Category Search)","description":"","requestParams":{"engine":"google_play_books","books_category":"coll_1665","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=google_play_books&books_category=coll_1665"}
    - {"title":"Top Charts results overview for Google Play Books with books_category(Category Search)","description":"","requestParams":{"engine":"google_play_books","books_category":"coll_1690","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=google_play_books&books_category=coll_1690"}
    - {"title":"Rows Type Organic results overview for Google Play Books with books_category, and age(Category Search)","description":"","requestParams":{"engine":"google_play_books","books_category":"coll_1689","age":"AGE_RANGE1","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=google_play_books&books_category=coll_1689&age=AGE_RANGE1"}
    - {"title":"Rows Type Organic results overview for Google Play Books with q(Query Search)","description":"","requestParams":{"engine":"google_play_books","q":"Coffee","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=google_play_books&q=Coffee"}
    - {"title":"Rows Type Organic results overview for Google Play Books with q, and price(Query Search)","description":"","requestParams":{"engine":"google_play_books","q":"Coffee","price":"1","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?engine=google_play_books&q=Coffee&price=1"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "google-play-books-api"
---

# Google Play Books Store API

## 源URL

https://serpapi.com/google-play-books

## 描述

Our Google Play Books Store API allows you to scrape SERP results from Google Play Books & Audiobooks Store.

Three types of searches you can do are: - Query Search: by using q parameter - Category Search: by using books_category parameter - Plain Search: without using q or books_category parameters

The API endpoint is https://serpapi.com/search?engine=google_play_books Head to the playground for a live and interactive demo.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Google Play Books Store API allows you to scrape SERP results from Google Play Books & Audiobooks Store.

Three types of searches you can do are: - Query Search: by using q parameter - Category Search: by using books_category parameter - Plain Search: without using q or books_category parameters

The API endpoint is https://serpapi.com/search?engine=google_play_books Head to the playground for a live and interactive demo.

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
