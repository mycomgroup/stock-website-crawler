---
id: "url-50d17648"
type: "api"
title: "Bing Answer Box API"
url: "https://serpapi.com/bing-answer-box"
description: "For some requests, Bing search includes a \"Answer\" block, typically on top of the page and before organic results. SerpApi is able to extract and make sense of this information.\n\nThe API endpoint is https://serpapi.com/search?engine=bing Head to the playground for a live and interactive demo.\n\nFor some searches, Bing display answer box that contains the answer to the search query. In this example, result contains the answer and snippet contains the extra information. We are also able to extract snippet_attributions, highlighted_snippets, thumbnail, sources and many more.\n\nFor some qna answer box, result is not present. In this example, we can consider the snippet as the result.\n\nFor some qna answer box, Bing display a series of images, we extract it as images. We are also able to extract result, title, link, displayed_link, logo and many more."
source: ""
tags: []
crawl_time: "2026-03-18T09:33:48.660Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Wellness","description":"","requestParams":{"engine":"bing","q":"banana","highlight":"answer_box"},"responseJson":"https://serpapi.com/search.json?engine=bing&q=banana"}
    - {"title":"Questions and Answers - qna","description":"For some searches, Bing display answer box that contains the answer to the search query. In this example, result contains the answer and snippet contains the extra information. We are also able to extract snippet_attributions, highlighted_snippets, thumbnail, sources and many more.","requestParams":{"engine":"bing","q":"Spiderman real name","highlight":"answer_box"},"responseJson":"https://serpapi.com/search.json?engine=bing&q=Spiderman+real+name"}
    - {"title":"Questions and Answers - qna","description":"For some qna answer box, result is not present. In this example, we can consider the snippet as the result.","requestParams":{"engine":"bing","q":"What is the purpose of Rails","highlight":"answer_box"},"responseJson":"https://serpapi.com/search.json?engine=bing&q=What+is+the+purpose+of+Rails"}
    - {"title":"Questions and Answers - qna","description":"For some qna answer box, Bing display a series of images, we extract it as images. We are also able to extract result, title, link, displayed_link, logo and many more.","requestParams":{"engine":"bing","q":"population in paris france","highlight":"answer_box"},"responseJson":"https://serpapi.com/search.json?engine=bing&q=population+in+paris+france"}
    - {"title":"Questions and Answers - qna","description":"For some qna answer box, Bing display a list of results, we extract it as list. We are also able to extract snippet, snippet, sources and many more.","requestParams":{"engine":"bing","q":"top 10 nba players of all time","highlight":"answer_box"},"responseJson":"https://serpapi.com/search.json?engine=bing&q=top+10+nba+players+of+all+time"}
    - {"title":"Questions and Answers - qna","description":"For some qna answer box, Bing display a comparison, is_comparison is the indicator for these results.","requestParams":{"engine":"bing","q":"is matcha good or bad?","highlight":"answer_box"},"responseJson":"https://serpapi.com/search.json?engine=bing&q=is+matcha+good+or+bad?"}
    - {"title":"Questions and Answers - qna","description":"For some qna answer box, Bing display multiple sources for the result. We are also able to extract remark, thumbnail and many more.","requestParams":{"engine":"bing","q":"why color of the sky is blue?","highlight":"answer_box"},"responseJson":"https://serpapi.com/search.json?engine=bing&q=why+color+of+the+sky+is+blue?"}
    - {"title":"Fact","description":"For some searches, Bing display fact answer box, we are able to extract result, breadcrumb, thumbnail and many more.","requestParams":{"engine":"bing","q":"Capital of Australia","highlight":"answer_box"},"responseJson":"https://serpapi.com/search.json?engine=bing&q=Capital+of+Australia"}
    - {"title":"Answer Box List","description":"For some searches, Bing might display fact block and question and answer block at the same time. We include both answer box in answer_box_list.","requestParams":{"engine":"bing","q":"Capital of China","highlight":"answer_box_list"},"responseJson":"https://serpapi.com/search.json?engine=bing&q=Capital+of+China"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"answer_box\": [\n    {\n      \"type\": \"String - Type of answer box (wellness, qna, fact)\",\n      // Answer box result has different JSON structure depends on which type is parsed\n      // Refer to examples below to get to know more about the detail JSON structure\n    },\n  ],\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "bing-answer-box-api"
---

# Bing Answer Box API

## 源URL

https://serpapi.com/bing-answer-box

## 描述

For some requests, Bing search includes a "Answer" block, typically on top of the page and before organic results. SerpApi is able to extract and make sense of this information.

The API endpoint is https://serpapi.com/search?engine=bing Head to the playground for a live and interactive demo.

For some searches, Bing display answer box that contains the answer to the search query. In this example, result contains the answer and snippet contains the extra information. We are also able to extract snippet_attributions, highlighted_snippets, thumbnail, sources and many more.

For some qna answer box, result is not present. In this example, we can consider the snippet as the result.

For some qna answer box, Bing display a series of images, we extract it as images. We are also able to extract result, title, link, displayed_link, logo and many more.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

For some requests, Bing search includes a "Answer" block, typically on top of the page and before organic results. SerpApi is able to extract and make sense of this information.

The API endpoint is https://serpapi.com/search?engine=bing Head to the playground for a live and interactive demo.

For some searches, Bing display answer box that contains the answer to the search query. In this example, result contains the answer and snippet contains the extra information. We are also able to extract snippet_attributions, highlighted_snippets, thumbnail, sources and many more.

For some qna answer box, result is not present. In this example, we can consider the snippet as the result.

For some qna answer box, Bing display a series of images, we extract it as images. We are also able to extract result, title, link, displayed_link, logo and many more.

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
