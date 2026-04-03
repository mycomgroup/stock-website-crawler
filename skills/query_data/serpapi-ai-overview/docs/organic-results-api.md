---
id: "url-4073698d"
type: "api"
title: "Google Organic Results API"
url: "https://serpapi.com/organic-results"
description: "Google search main results are called organic results. Some results are simple and straightforward. Others include rich data like reviews, thumbnails, and other special snippets. SerpApi is able to scrape, extract, and make sense of both simple and more complex organic results.When SerpApi encounters organic results, we add them to our JSON output as the array organic_results.For each organic result, we are able to extract its position, title, link, redirect_link, source, displayed_link, thumbnail, favicon, date, author, cited_by, extracted_cited_by, snippet, cached_page_link, about_page_link, related_pages_link, sitelinks:inline, sitelinks:expanded, rich_snippet:top, rich_snippet:bottom, rich_snippet_table, extensions, reviews, ratings, answers, related_questions, carousel and more.\n\nThe API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.\n\nWeb Result layout is shown when specific ibp value is set, you can check out an example on Google Maps Place Results. Initially, only 3 results will be returned. You can increase the number of results by specifying the start parameter (Yes, it is different from the usual Google search). A Minimum of 3 results will always be returned + the value specified in the start. Here is how it works: • When start is 1, the total results returned is 4 (original 3 + 1) • When start is 5, the total results returned is 8 (original 3 + 5) • When start is 10, the total results returned is 13 (original 3 + 10) • and so on..."
source: ""
tags: []
crawl_time: "2026-03-18T08:23:48.713Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Organic results overview","description":"","requestParams":{"q":"Coffee","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=Coffee&hl=en&gl=us"}
    - {"title":"Results for: OpenAI with Expanded Sitelinks and Latest News","description":"","requestParams":{"q":"OpenAI","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=OpenAI&hl=en&gl=us"}
    - {"title":"Results for: squid game with Video Thumbnail","description":"","requestParams":{"q":"squid game","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=squid+game&hl=en&gl=us"}
    - {"title":"Results for: Book hotels in Austin with Top Rich Snippet","description":"","requestParams":{"q":"Book hotels in Austin","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=Book+hotels+in+Austin&hl=en&gl=us"}
    - {"title":"Results for: macbook m3 with Bottom Rich Snippet","description":"","requestParams":{"q":"macbook m3","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=macbook+m3&hl=en&gl=us"}
    - {"title":"Results for: country codes with Rich Snippet Table","description":"","requestParams":{"q":"country codes","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=country+codes&hl=en&gl=us"}
    - {"title":"Results for: Bacteria Cell, Evolution  Classification with Author","description":"","requestParams":{"q":"Bacteria Cell, Evolution  Classification","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=Bacteria+Cell,+Evolution++Classification&hl=en&gl=us"}
    - {"title":"Results for: Tom Hanks with Carousel","description":"","requestParams":{"q":"Tom Hanks","hl":"en","gl":"us","device":"mobile"},"responseJson":"https://serpapi.com/search.json?q=Tom+Hanks&hl=en&gl=us&device=mobile"}
    - {"title":"Results for: wat eten we vandaag with Carousel","description":"","requestParams":{"q":"wat eten we vandaag","hl":"en","gl":"us","device":"mobile"},"responseJson":"https://serpapi.com/search.json?q=wat+eten+we+vandaag&hl=en&gl=us&device=mobile"}
    - {"title":"Results for: mrbeast videos with Carousel","description":"","requestParams":{"q":"mrbeast videos","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=mrbeast+videos&hl=en&gl=us"}
    - {"title":"Results for: what is the common ratio of 81, 27, 9,3 with Answers","description":"","requestParams":{"q":"what is the common ratio of 81, 27, 9,3","hl":"en","gl":"us","device":"mobile"},"responseJson":"https://serpapi.com/search.json?q=what+is+the+common+ratio+of+81,+27,+9,3&hl=en&gl=us&device=mobile"}
    - {"title":"Results for: cruises with Related Questions","description":"","requestParams":{"q":"cruises","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=cruises&hl=en&gl=us"}
    - {"title":"Results from Web Result layout","description":"Web Result layout is shown when specific ibp value is set, you can check out an example on Google Maps Place Results. Initially, only 3 results will be returned. You can increase the number of results by specifying the start parameter (Yes, it is different from the usual Google search). A Minimum of 3 results will always be returned + the value specified in the start. Here is how it works: • When start is 1, the total results returned is 4 (original 3 + 1) • When start is 5, the total results returned is 8 (original 3 + 5) • When start is 10, the total results returned is 13 (original 3 + 10) • and so on...","requestParams":{"q":"local guide program","ibp":"gwp;0,26,OiIKICIcR3JlZ29yeXMgQ29mZmVlIE5ldyBZb3JrLCBOWSgC","highlight":"organic_results"},"responseJson":"https://serpapi.com/search.json?q=local+guide+program&ibp=gwp;0,26,OiIKICIcR3JlZ29yeXMgQ29mZmVlIE5ldyBZb3JrLCBOWSgC"}
    - {"title":"Organic Results State","description":"","requestParams":{"q":"Cruises","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=Cruises&hl=en&gl=us"}
    - {"title":"Results for exact spelling: Regular Google search results page without query corrections","description":"","requestParams":{"q":"Cruises","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=Cruises&hl=en&gl=us"}
    - {"title":"Empty showing fixed spelling results: No results for exact spelling, but showing some for fixed spelling","description":"","requestParams":{"q":"Coffeedsaasdasdad","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=Coffeedsaasdasdad&hl=en&gl=us"}
    - {"title":"Some results for exact spelling but showing fixed spelling: \"Showing results\" and \"Search instead\" links are shown","description":"","requestParams":{"q":"Cofeeasdasd","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=Cofeeasdasd&hl=en&gl=us"}
    - {"title":"Showing results for exact spelling despite spelling suggestion: \"Did you mean?\" block is shown","description":"","requestParams":{"q":"pewdpie","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=pewdpie&hl=en&gl=us"}
    - {"title":"Fully empty: No organic results","description":"","requestParams":{"q":"fbcvbseflt45","hl":"en","gl":"us"},"responseJson":"https://serpapi.com/search.json?q=fbcvbseflt45&hl=en&gl=us"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"organic_results\": [\n    {\n      \"position\": \"Integer - Position of the organic result on the search page\",\n      \"title\": \"String - Title of the organic result\",\n      \"link\": \"String - Link of the organic result\",\n      \"redirect_link\": \"String - Redirect link of the organic result\",\n      \"displayed_link\": \"String - Displayed link of the organic result\",\n      \"amp_link\": \"String - AMP link of the organic result (available on mobile results only)\",\n      \"thumbnail\": \"String - Thumbnail of the organic result\",\n      \"date\": \"String - Date of the organic result\",\n      \"author\": \"String - Author of the organic result\",\n      \"cited_by\": \"String - Cited by of the organic result\",\n      \"extracted_cited_by\": \"Integer - Extracted cited by number of the organic result\",\n      \"favicon\": \"String - Favicon of the organic result\",\n      \"snippet\": \"String - Snippet of the organic result\",\n      \"snippet_highlighted_words\": [\n        \"String - Snippet highlighted word of the organic result\",\n      ],\n      \"duration\": \"String - Duration of the organic result - video result\",\n      \"key_moments\": [\n        {\n          \"text\": \"String - Text of the key moment\",\n          \"time\": \"String - Time of the key moment\",\n          \"link\": \"String - Link of the key moment\",\n          \"thumbnail\": \"String - Thumbnail of the key moment\"\n        },\n      ],\n      \"video_link\": \"String - Video link of the organic result\",\n      \"sitelinks_search_box\": \"Boolean - Has search box in the organic result\",\n      \"sitelinks\": {\n        \"inline\": [\n          {\n            \"title\": \"String - Title of the inline sitelink\",\n            \"link\": \"String - Link of the inline sitelink\"\n          },\n        ],\n        \"expanded\": [\n          {\n            \"title\": \"String - Title of the expanded sitelink\",\n            \"link\": \"String - Link of the expanded sitelink\",\n            \"snippet\": \"String - Snippet of the expanded sitelink\"\n          },\n        ],\n        \"list\": [\n          {\n            \"title\": \"String - Title of the list sitelink\",\n            \"link\": \"String - Link of the list sitelink\",\n            \"snippet\": \"String - Snippet of the list sitelink\"\n          },\n        ]\n      },\n      \"rich_snippet\": {\n        \"top\": {\n          \"extensions\": [\n            \"String - Extension of the rich snippet top\",\n          ],\n          \"detected_extensions\": {\n            \"price\": \"String - Price of detected extension of the rich snippet top\",\n            \"currency\": \"String - Currency of detected extension of the rich snippet top\",\n            \"month as key\": \"String - Date of the month in detected extension of the rich snippet top\",\n            \"week as key\": \"String - Number of week in detected extension of the rich snippet top\",\n            \"rating\": \"Float - Rating of detected extension of the rich snippet top\",\n            \"reviews\": \"Integer - Reviews of detected extension of the rich snippet top\",\n            \"reviews_link\": \"String - URL of reviews of detected extension of the rich snippet top\",\n            \"price_from\": \"String - Minimum price of detected extension of the rich snippet top\",\n            \"price_to\": \"String - Maximum price of detected extension of the rich snippet top\",\n            \"address\": \"String - Address of detected extension of the rich snippet top\",\n          }\n        },\n        \"bottom\": {\n          \"extensions\": [\n            \"String - Extension of the rich snippet bottom\",\n          ],\n          \"detected_extensions\": {\n            \"price\": \"String - Price of detected extension of the rich snippet bottom\",\n            \"price_from\": \"String - Minimum price of detected extension of the rich snippet top\",\n            \"price_to\": \"String - Maximum price of detected extension of the rich snippet top\",\n            \"currency\": \"String - Currency of detected extension of the rich snippet bottom\",\n            \"rating\": \"Float - Rating of detected extension of the rich snippet top\",\n            \"reviews\": \"Integer - Reviews of detected extension of the rich snippet top\",\n            \"top_answer\": \"String - Top answer of detected extension of the rich snippet bottom\",\n            \"vote_count\": \"String - Vote count of detected extension of the rich snippet bottom\",\n            \"link\": \"String - Link of detected extension of the rich snippet bottom\",\n            \"answer_count\": \"String - Answer count of detected extension of the rich snippet bottom\"\n          }\n        }\n      },\n      \"carousel\": [\n        {\n          \"title\": \"String - Title of the carousel item\",\n          \"link\": \"String - Link of the carousel item\",\n          \"thumbnail\": \"String - Thumbnail of the carousel item\",\n          \"snippet\": \"String - Snippet of the carousel item\",\n          \"source\": \"String - Source of the carousel item\",\n          \"author\": \"String - Author of the source content\",\n          \"duration\": \"String - Duration for video carousel item\",\n          \"date\": \"String - Date posted of the carousel item\",\n          \"extensions\": \"Array - Additional information about the expanded site, for example, movie rating\",\n          \"rating\": \"String - Rating of the carousel item\",\n          \"extracted_rating\": \"Float - Rating of the carousel item\",\n          \"reviews\": \"String - Total number of reviews of the carousel item\",\n          \"extracted_reviews\": \"Integer - Total number of reviews of the carousel item\"\n        },\n      ],\n      \"about_this_result\": {\n        \"source\": {\n          \"description\": \"String - Description of the about_this_result of the organic result\",\n          \"source_info_link\": \"String - Source info link of the about_this_result of the organic result\",\n          \"security\": \"String - Security of the about_this_result of the organic result\",\n          \"icon\": \"String - Icon of the about_this_result of the organic result\"\n        },\n        \"keywords\": [\n          \"String - Keyword of the about_this_result of the organic result\",\n        ],\n        \"languages\": [\n          \"String - Language of the about_this_result of the organic result\",\n        ],\n        \"regions\": [\n          \"String - Region of the about_this_result of the organic result\",\n        ],\n      },\n      \"about_page_link\": \"String - About page link of the organic result\",\n      \"about_page_serpapi_link\": \"String - About page SerpApi link of the organic result\",\n      \"cached_page_link\": \"String - Cached page link of the organic result\",\n      \"related_pages_link\": \"String - Related pages link of the organic result\",\n      \"source\": \"String - Source of the organic result\",\n      \"latest_news\": [\n        {\n          \"title\": \"String - Title of the latest news\",\n          \"link\": \"String - Link of the latest news\",\n          \"thumbnail\": \"String - Thumbnail of the latest news\",\n          \"source\": \"String - Source of the latest news\",\n          \"source_logo\": \"String - URL to the source logo of the latest news\",\n          \"date\": \"String - Date of the latest news\"\n        }\n      ],\n      \"answers\": [\n        {\n          \"link\": \"String - Link of the answer\",\n          \"answer\": \"String - Answer of the answer\",\n          \"top_answer\": \"Boolean - Is the top answer\",\n          \"votes\": \"Integer - Votes of the answer\"\n        }\n      ],\n      \"related_questions\": [\n        {\n          \"question\": \"String - Question of the related question\",\n          \"snippet\": \"String - Snippet of the related question\"\n        }\n      ]\n    }\n  ],\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "organic-results-api"
---

# Google Organic Results API

## 源URL

https://serpapi.com/organic-results

## 描述

Google search main results are called organic results. Some results are simple and straightforward. Others include rich data like reviews, thumbnails, and other special snippets. SerpApi is able to scrape, extract, and make sense of both simple and more complex organic results.When SerpApi encounters organic results, we add them to our JSON output as the array organic_results.For each organic result, we are able to extract its position, title, link, redirect_link, source, displayed_link, thumbnail, favicon, date, author, cited_by, extracted_cited_by, snippet, cached_page_link, about_page_link, related_pages_link, sitelinks:inline, sitelinks:expanded, rich_snippet:top, rich_snippet:bottom, rich_snippet_table, extensions, reviews, ratings, answers, related_questions, carousel and more.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

Web Result layout is shown when specific ibp value is set, you can check out an example on Google Maps Place Results. Initially, only 3 results will be returned. You can increase the number of results by specifying the start parameter (Yes, it is different from the usual Google search). A Minimum of 3 results will always be returned + the value specified in the start. Here is how it works: • When start is 1, the total results returned is 4 (original 3 + 1) • When start is 5, the total results returned is 8 (original 3 + 5) • When start is 10, the total results returned is 13 (original 3 + 10) • and so on...

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Google search main results are called organic results. Some results are simple and straightforward. Others include rich data like reviews, thumbnails, and other special snippets. SerpApi is able to scrape, extract, and make sense of both simple and more complex organic results.When SerpApi encounters organic results, we add them to our JSON output as the array organic_results.For each organic result, we are able to extract its position, title, link, redirect_link, source, displayed_link, thumbnail, favicon, date, author, cited_by, extracted_cited_by, snippet, cached_page_link, about_page_link, related_pages_link, sitelinks:inline, sitelinks:expanded, rich_snippet:top, rich_snippet:bottom, rich_snippet_table, extensions, reviews, ratings, answers, related_questions, carousel and more.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

Web Result layout is shown when specific ibp value is set, you can check out an example on Google Maps Place Results. Initially, only 3 results will be returned. You can increase the number of results by specifying the start parameter (Yes, it is different from the usual Google search). A Minimum of 3 results will always be returned + the value specified in the start. Here is how it works: • When start is 1, the total results returned is 4 (original 3 + 1) • When start is 5, the total results returned is 8 (original 3 + 5) • When start is 10, the total results returned is 13 (original 3 + 10) • and so on...

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
