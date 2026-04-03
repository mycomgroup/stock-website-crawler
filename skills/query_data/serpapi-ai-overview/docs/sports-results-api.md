---
id: "url-4415c69"
type: "api"
title: "Google Sports Results API"
url: "https://serpapi.com/sports-results"
description: "The Google Sports Results API allows a user to scrape the results of Google Sports search. SerpApi is able to make sense of this information and extract various sports data.These results can include team sports, such as: Soccer, American Football, Basketball, Hockey, Baseball or Cricket; or individual sports, such as: Tennis, Auto Racing sports and others. The Google Sports Results API can also extract professional athletes stats, team standings, league stats and more.\n\nThe API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.\n\nThese kind of results are seen for team sports such as: Soccer, American Football, Basketball, Hockey, Baseball. From these results SerpApi is able to extract: title, thumbnail, league, score, video_highlights, tournament, stage and more.\n\nThis kind of results are usually seen for live games, recently finished or soon to begin games. From these results SerpApi is able to extract: title, rankings, thumbnail, game_spotlight data which could contain: league, date, stage, video_highlights, team_stats, score and more.\n\nSometimes Google will show game recap in carousel. SerpApi is able extract it as video_highlight_carousel. Also worth noting SerpApi include the seeding of the team if it is available."
source: ""
tags: []
crawl_time: "2026-03-18T07:48:42.275Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Team sports results (Soccer, American Football, Basketball, Hockey, Baseball, Cricket)","description":"These kind of results are seen for team sports such as: Soccer, American Football, Basketball, Hockey, Baseball. From these results SerpApi is able to extract: title, thumbnail, league, score, video_highlights, tournament, stage and more.","requestParams":{"q":"Manchester United F.C.","location":"austin, texas, united states","highlight":"sports_results"},"responseJson":"https://serpapi.com/search.json?q=Manchester+United+F.C.&location=austin,+texas,+united+states"}
    - {"title":"Game spotlight results","description":"This kind of results are usually seen for live games, recently finished or soon to begin games. From these results SerpApi is able to extract: title, rankings, thumbnail, game_spotlight data which could contain: league, date, stage, video_highlights, team_stats, score and more.","requestParams":{"q":"Milwaukee Bucks","location":"austin, texas, united states","highlight":"sports_results"},"responseJson":"https://serpapi.com/search.json?q=Milwaukee+Bucks&location=austin,+texas,+united+states"}
    - {"title":"Game spotlight results (video highlights carousel)","description":"Sometimes Google will show game recap in carousel. SerpApi is able extract it as video_highlight_carousel. Also worth noting SerpApi include the seeding of the team if it is available.","requestParams":{"q":"UCLA basketball last game result","location":"Austin, Texas, United States","highlight":"sports_results"},"responseJson":"https://serpapi.com/search.json?q=UCLA+basketball+last+game+result&location=Austin,+Texas,+United+States"}
    - {"title":"Sports results for athletes (Soccer)","description":"This kind of results are seen when you search for soccer athletes stats. From these results SerpApi is able to extract: title, profession, tournament, games data which could contain: year, matches, goals, assists and more.","requestParams":{"q":"lionel messi stats","location":"austin, texas, united states","highlight":"sports_results"},"responseJson":"https://serpapi.com/search.json?q=lionel+messi+stats&location=austin,+texas,+united+states"}
    - {"title":"Sports results for athletes (American Football, Basketball, Baseball)","description":"This kind of results are usually seen when you search for american football, basketball or baseball athletes stats. From these results SerpApi is able to extract: title and games data which could contain various stats and information.","requestParams":{"q":"tom brady stats","location":"austin, texas, united states","highlight":"sports_results"},"responseJson":"https://serpapi.com/search.json?q=tom+brady+stats&location=austin,+texas,+united+states"}
    - {"title":"Sports results for athletes (Tennis)","description":"This kind of results are seen when you search for tennis athletes stats, tournaments or ligues. From these results SerpApi is able to extract: title, country, date, location, players which could contain: name, ranking, sets data and more.","requestParams":{"q":"novak djokovic","location":"austin, texas, united states","highlight":"sports_results"},"responseJson":"https://serpapi.com/search.json?q=novak+djokovic&location=austin,+texas,+united+states"}
    - {"title":"Results for Auto and Moto Racing sports","description":"This kind of results are seen when you search for auto and moto racing sports. From these results SerpApi is able to extract: title, ranking, date, standings which could contain: rank, name, team, vehicle_number, points and more.","requestParams":{"q":"lewis hamilton","location":"austin, texas, united states","highlight":"sports_results"},"responseJson":"https://serpapi.com/search.json?q=lewis+hamilton&location=austin,+texas,+united+states"}
    - {"title":"Results for standings","description":"This kind of result is seen when you search for sports standings results. SerpApi is able to extract: title, thumbnail, season, rounds, leagues which could contain: standings, team, pos, pts, last_5 and more.","requestParams":{"q":"premier league standings","location":"austin, texas, united states","highlight":"sports_results"},"responseJson":"https://serpapi.com/search.json?q=premier+league+standings&location=austin,+texas,+united+states"}
    - {"title":"Results for new york mets standings on mobile","description":"In the case of multiple leagues the selected one is parsed into league, all the others - into other_leagues.","requestParams":{"q":"new york mets standings","location":"austin, texas, united states","highlight":"sports_results"},"responseJson":"https://serpapi.com/search.json?q=new+york+mets+standings&location=austin,+texas,+united+states"}
    - {"title":"Soccer-specific game spotlight","description":"","requestParams":{"q":"world cup 2022 netherlands vs argentina","location":"austin, texas, united states","highlight":"sports_results"},"responseJson":"https://serpapi.com/search.json?q=world+cup+2022+netherlands+vs+argentina&location=austin,+texas,+united+states"}
    - {"title":"Game spotlight for LIVE soccer game","description":"","requestParams":{"q":"Port FC vs Chiangrai United","location":"Austin, Texas, United States","highlight":"sports_results"},"responseJson":"https://serpapi.com/search.json?q=Port+FC+vs+Chiangrai+United&location=Austin,+Texas,+United+States"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"sports_results\": {\n    \"title\": \"String - Title of the sports results\",\n    \"thumbnail\": \"String - URL to the thumbnail image\",\n    \"score\": \"String - Score of the game\",\n    \"rankings\": \"String - Rankings of the team\",\n    \"ranking\": \"Integer - Ranking of the athlete\",\n    \"country\": \"String - Country of the athlete\",\n    \"tables\": [\n      {\n        \"title\": \"String - Title of the table\",\n        \"games\": \"Array - List of games\",\n        \"results\": {\n          \"date\": \"String - Date of the game\",\n          \"track\": {\n            \"name\": \"String - Name of the track\",\n            \"link\": \"String - URL to the track\",\n          }\n        },\n        \"standings\": \"Array - List of standings\",\n      },\n      ...\n    ],\n    \"league\": {\n      \"name\": \"String - League name\",\n      \"standings\": \"Array - List of standings\",\n      \"divisions\": [\n        {\n          \"name\": \"String - Division name\",\n          \"standings\": \"Array - List of standings\"\n        },\n        ...\n      ]\n    },\n    \"other_leagues\": [\n      {\n        \"name\": \"String - League name\",\n        \"standings\": \"Array - List of standings\",\n        \"divisions\": [\n          {\n            \"name\": \"String - Division name\",\n            \"standings\": \"Array - List of standings\"\n          },\n          ...\n        ]\n      },\n      ...\n    ],\n    \"games\": [\n      {\n        \"tournament\": \"String - Tournament name\",\n        \"status\": \"String - Status of the game\",\n        \"date\": \"String - Date of the game\",\n        \"time\": \"String - Time of the game\",\n        \"stadium\": \"String - Stadium name. This key is dynamic and can be different\",\n        \"video_highlights\": {\n          \"link\": \"String - URL to the video highlights\",\n          \"thumbnail\": \"String - URL to the video thumbnail\",\n          \"duration\": \"String - Duration of the video\"\n        }\n        \"teams\": [\n          {\n            \"name\": \"String - Team name\",\n            \"score\": \"String - Team score\",\n            \"kgmid\": \"String - Team Knowledge Graph ID\",\n            \"thumbnail\": \"String - URL to the team thumbnail\",\n            \"red_card\": \"String - Has red card\",\n          },\n          ...\n        ],\n      },\n      ...\n    ],\n    \"game_spotlight\": {\n      \"league\": \"String - League name\",\n      \"stadium\": \"String - Stadium name\",\n      \"stadium_kgmid\": \"String - Stadium Knowledge Graph ID\",\n      \"date\": \"String - Date of the game\",\n      \"stage\": \"String - Stage of the game\",\n      \"status\": \"String - Status of the game\",\n      \"in_game_time\": \"Hash - Live game timer\",\n      \"watch_on\": \"String - URL to watch the game\",\n      \"video_highlight_carousel\": [\n        {\n          \"title\": \"String - Title of the video\",\n          \"link\": \"String - URL to the video highlights\",\n          \"thumbnail\": \"String - URL to the video thumbnail\",\n          \"duration\": \"String - Duration of the video\"\n        },\n        ...\n      ],\n      \"teams\": [\n        {\n          \"name\": \"String - Team name\",\n          \"thumbnail\": \"String - URL to the team thumbnail\",\n          \"seeding\": \"Integer - Seeding of the team\",\n          \"kgmid\": \"String - Team Knowledge Graph ID\",\n          \"team_stats\": {\n            \"wins\": \"Integer - Number of wins\",\n            \"losses\": \"Integer - Number of losses\"\n          },\n          \"score\": \"Hash - Team score info\",\n          \"penalty_score\": \"Integer - Penalty score\",\n          \"goal_summary\": [\n            {\n              \"player\": {\n                \"name\": \"String - Player name\",\n                \"jersey_number\": \"String - Player jersey number\",\n                \"position\": \"String - Player position\"\n              },\n              \"goals\": \"Array - List of goals\",\n            },\n            ...\n          ],\n          \"red_cards_summary\": [\n            {\n              \"player\": {\n                \"name\": \"String - Player name\",\n                \"jersey_number\": \"String - Player jersey number\",\n                \"position\": \"String - Player position\"\n              },\n              \"cards\": \"Array - List of red cards\"\n            },\n            ...\n          ]\n        },\n        ...\n      ],\n    },\n  },\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "sports-results-api"
---

# Google Sports Results API

## 源URL

https://serpapi.com/sports-results

## 描述

The Google Sports Results API allows a user to scrape the results of Google Sports search. SerpApi is able to make sense of this information and extract various sports data.These results can include team sports, such as: Soccer, American Football, Basketball, Hockey, Baseball or Cricket; or individual sports, such as: Tennis, Auto Racing sports and others. The Google Sports Results API can also extract professional athletes stats, team standings, league stats and more.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

These kind of results are seen for team sports such as: Soccer, American Football, Basketball, Hockey, Baseball. From these results SerpApi is able to extract: title, thumbnail, league, score, video_highlights, tournament, stage and more.

This kind of results are usually seen for live games, recently finished or soon to begin games. From these results SerpApi is able to extract: title, rankings, thumbnail, game_spotlight data which could contain: league, date, stage, video_highlights, team_stats, score and more.

Sometimes Google will show game recap in carousel. SerpApi is able extract it as video_highlight_carousel. Also worth noting SerpApi include the seeding of the team if it is available.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

The Google Sports Results API allows a user to scrape the results of Google Sports search. SerpApi is able to make sense of this information and extract various sports data.These results can include team sports, such as: Soccer, American Football, Basketball, Hockey, Baseball or Cricket; or individual sports, such as: Tennis, Auto Racing sports and others. The Google Sports Results API can also extract professional athletes stats, team standings, league stats and more.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

These kind of results are seen for team sports such as: Soccer, American Football, Basketball, Hockey, Baseball. From these results SerpApi is able to extract: title, thumbnail, league, score, video_highlights, tournament, stage and more.

This kind of results are usually seen for live games, recently finished or soon to begin games. From these results SerpApi is able to extract: title, rankings, thumbnail, game_spotlight data which could contain: league, date, stage, video_highlights, team_stats, score and more.

Sometimes Google will show game recap in carousel. SerpApi is able extract it as video_highlight_carousel. Also worth noting SerpApi include the seeding of the team if it is available.

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
