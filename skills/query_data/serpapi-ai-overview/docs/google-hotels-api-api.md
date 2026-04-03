---
id: "url-4d60a43f"
type: "api"
title: "Google Hotels API"
url: "https://serpapi.com/google-hotels-api"
description: "Our Google Hotels API allows you to scrape hotel and vacation rental results from Google Hotels.\n\nThe API endpoint is https://serpapi.com/search?engine=google_hotels Head to the playground for a live and interactive demo.\n\nFor certain searches with q, especially when q is the exact name of a hotel, Google Hotels may return the details of the single matching property instead of properties search results.In such cases, search_information.hotels_results_state will have the value Showing results for property details.Also serpapi_property_details_link will be present as a canonical way to retrieve the property details using property_token."
source: ""
tags: []
crawl_time: "2026-03-18T17:20:24.044Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Example with q: Bali Resorts","description":"","requestParams":{"engine":"google_hotels","q":"Bali Resorts","check_in_date":"2026-03-19","check_out_date":"2026-03-20","adults":"2","currency":"USD","gl":"us","hl":"en"},"responseJson":"https://serpapi.com/search.json?engine=google_hotels&q=Bali+Resorts&check_in_date=2026-03-19&check_out_date=2026-03-20&adults=2&currency=USD&gl=us&hl=en"}
    - {"title":"Example Vacation Rentals with q: Bali","description":"","requestParams":{"engine":"google_hotels","q":"Bali","vacation_rentals":"true","check_in_date":"2026-03-19","check_out_date":"2026-03-20","adults":"2","currency":"USD","gl":"us","hl":"en"},"responseJson":"https://serpapi.com/search.json?engine=google_hotels&q=Bali&vacation_rentals=true&check_in_date=2026-03-19&check_out_date=2026-03-20&adults=2&currency=USD&gl=us&hl=en"}
    - {"title":"Example of showing property details with q search","description":"For certain searches with q, especially when q is the exact name of a hotel, Google Hotels may return the details of the single matching property instead of properties search results. In such cases, search_information.hotels_results_state will have the value Showing results for property details. Also serpapi_property_details_link will be present as a canonical way to retrieve the property details using property_token.","requestParams":{"engine":"google_hotels","q":"H10 Port Vell","check_in_date":"2026-03-19","check_out_date":"2026-03-20","adults":"2","currency":"USD","gl":"us","hl":"en"},"responseJson":"https://serpapi.com/search.json?engine=google_hotels&q=H10+Port+Vell&check_in_date=2026-03-19&check_out_date=2026-03-20&adults=2&currency=USD&gl=us&hl=en"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  \"brands\": [\n    {\n      \"id\": \"Integer - ID of the brand\",\n      \"name\": \"String - Name of the brand\",\n      // children can be null\n      \"children\": [\n        {\n          \"id\": \"Integer - ID of the child's brand\",\n          \"name\": \"String - Name of the child's brand\"\n        }\n      ]\n    }\n  ],\n  \"ads\": [\n    {\n      \"name\": \"String - Name of the ad property\",\n      \"source\": \"String - Source of the ad property\",\n      \"source_icon\": \"String - URL of the source's icon\",\n      \"link\": \"String - URL of the source property's website\",\n      \"property_token\": \"String - Property token to retrieve the details of the property\",\n      \"serpapi_property_details_link\": \"String - SerpApi's endpoint for retrieving details of the property\",\n      \"gps_coordinates\": {\n        \"latitude\": \"Float - Latitude of the GPS Coordinates\",\n        \"longitude\": \"Float - Longitude of the GPS Coordinates\"\n      },\n      \"hotel_class\": \"Integer - Hotel class of the property\",\n      \"thumbnail\": \"String - URL of the thumbnail image\",\n      \"overall_rating\": \"Float - Overall rating for the property\",\n      \"reviews\": \"Integer - Total reviews for the property\",\n      \"price\": \"String - Price per night formatted with currency\",\n      \"extracted_price\": \"Float - Extracted price per night\",\n      \"amenities\": \"Array - Amenities provided by the property (e.g. Free Wi-Fi, Free parking, Hot tub, Pools, Airport shuttle and many more)\",\n      \"free_cancellation\": \"Boolean - Indicate if the property offers free cancellation\"\n    },\n    ...\n  ],\n  \"properties\": [\n    {\n      \"type\": \"String - Type of property (e.g. hotel or vacation rental)\",\n      \"name\": \"String - Name of the property\",\n      \"description\": \"String - Description of the property\",\n      \"link\": \"String - URL of the property's website\",\n      \"logo\": \"String - URL of the property's logo\",\n      \"sponsored\": \"Boolean - Indicate if the property result is sponsored\",\n      \"eco_certified\": \"Boolean - Indicate if the property is Eco-certified\",\n      \"gps_coordinates\": {\n        \"latitude\": \"Float - Latitude of the GPS Coordinates\",\n        \"longitude\": \"Float - Langitude of the GPS Coordinates\"\n      },\n      \"check_in_time\": \"String - Check-in time of the property (e.g. 3:00 PM)\",\n      \"check_out_time\": \"String - Check-out time of the property (e.g. 12:00 PM)\",\n      \"rate_per_night\": {\n        \"lowest\": \"String - Lowest rate per night formatted with currency\",\n        \"extracted_lowest\": \"Float - Extracted lowest rate per night\",\n        \"before_taxes_fees\": \"String - Rate per night before taxes and fees formatted with currency\",\n        \"extracted_before_taxes_fees\": \"Float - Extracted rate per night before taxes and fees\"\n      },\n      \"total_rate\": {\n        \"lowest\": \"String - Lowest total rate for the entire trip formatted with currency\",\n        \"extracted_lowest\": \"Float - Extracted lowest total rate for the entire trip\",\n        \"before_taxes_fees\": \"String - Total rate before taxes and fees for the entire trip formatted with currency\",\n        \"extracted_before_taxes_fees\": \"Float - Extracted total rate before taxes and fees for the entire trip\"\n      },\n      \"prices\": [\n        {\n          \"source\": \"String - Source of the site that list the price\",\n          \"logo\": \"String - URL of the source's logo\",\n          \"rate_per_night\": {\n            \"lowest\": \"String - Lowest rate per night formatted with currency\",\n            \"extracted_lowest\": \"Float - Extracted lowest rate per night\",\n            \"before_taxes_fees\": \"String - Rate per night before taxes and fees formatted with currency\",\n            \"extracted_before_taxes_fees\": \"Float - Extracted rate per night before taxes and fees\"\n          }\n        }\n      ],\n      \"nearby_places\": [\n        {\n          \"name\": \"String - Name of the place\",\n          \"transportations\": [\n            {\n              \"type\": \"String - Type of transportation (e.g. Taxi, Walking, Public transport)\",\n              \"duration\": \"String - Travel duration (e.g. 30 min)\"\n            }\n          ]\n        }\n      ],\n      \"hotel_class\": \"String - Hotel class of the property (e.g. 5-star hotel)\",\n      \"extracted_hotel_class\": \"Integer - Extracted hotel class of the property (e.g. 5)\",\n      \"images\": [\n        {\n          \"thumbnail\": \"String - URL of the thumbnail\",\n          \"original_image\": \"String - URL of the original image\"\n        }\n      ],\n      \"overall_rating\": \"Float - Overall rating for the property\",\n      \"reviews\": \"Integer - Total reviews for the property\",\n      \"ratings\": [\n        {\n          \"stars\": \"Integer - Number of stars from 1 to 5\",\n          \"count\": \"Integer - Total number of reviews for given star\"\n        }\n      ],\n      \"location_rating\": \"Float - Location rating of the property (e.g. 1.8 is Bad location, 4.8 is excellent location)\",\n      \"reviews_breakdown\": [\n        {\n          \"name\": \"String - Name of the review breakdown category\",\n          \"description\": \"String - Description of the category\",\n          \"total_mentioned\": \"Integer - Total mentioned about the category\",\n          \"positive\": \"Integer - Total amount of positivity\",\n          \"negative\": \"Integer - Total amount of negativity\",\n          \"neutral\": \"Integer - Total amount of neutrality\",\n          \"category_token\": \"String - Category token to retrieve reviews for the category\",\n          \"serpapi_link\": \"String - SerpApi's Google Hotels Reviews endpoint for the property and category\"\n        }\n      ],\n      \"amenities\": \"Array - Amenities provided by the property (e.g. Free Wi-Fi, Free parking, Hot tub, Pools, Airport shuttle and many more)\",\n      \"excluded_amenities\": \"Array - Excluded amenities (e.g. No air conditioning, No airport shuttle, No beach access, Not pet-friendly and many more)\",\n      \"health_and_safety\": {\n        \"groups\": [\n          {\n            \"title\": \"String - Name of the amenity group\",\n            \"list\": [\n              {\n                \"title\": \"String - Name of the amenity\",\n                \"available\": \"Boolean - Indicates whether the amenity is available\"\n              },\n              ...\n            ]\n          },\n          ...\n        ],\n        \"details_link\": \"String - URL to get additional information about health and safety\"\n      },\n      \"essential_info\": \"Array - Essential info of the vacation rental property (e.g. Entire villa, Sleeps 4, 9 bedrooms, 7 bathrooms)\",\n      \"property_token\": \"String - Property token to retrieve the details of the property\",\n      \"serpapi_property_details_link\": \"String - SerpApi's endpoint for retrieving details of the property\",\n      \"serpapi_google_hotels_reviews_link\": \"String - SerpApi's Google Hotels Reviews endpoint for the property\"\n    },\n    ...\n  ],\n  \"serpapi_pagination\": {\n    \"current_from\": \"Integer - Current page start index\",\n    \"current_to\": \"Integer - Current page end index\",\n    \"next_page_token\": \"String - Next page token\",\n    \"next\": \"String - SerpApi's Google Hotels API endpoint for the next page\"\n  }\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "google-hotels-api-api"
---

# Google Hotels API

## 源URL

https://serpapi.com/google-hotels-api

## 描述

Our Google Hotels API allows you to scrape hotel and vacation rental results from Google Hotels.

The API endpoint is https://serpapi.com/search?engine=google_hotels Head to the playground for a live and interactive demo.

For certain searches with q, especially when q is the exact name of a hotel, Google Hotels may return the details of the single matching property instead of properties search results.In such cases, search_information.hotels_results_state will have the value Showing results for property details.Also serpapi_property_details_link will be present as a canonical way to retrieve the property details using property_token.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Our Google Hotels API allows you to scrape hotel and vacation rental results from Google Hotels.

The API endpoint is https://serpapi.com/search?engine=google_hotels Head to the playground for a live and interactive demo.

For certain searches with q, especially when q is the exact name of a hotel, Google Hotels may return the details of the single matching property instead of properties search results.In such cases, search_information.hotels_results_state will have the value Showing results for property details.Also serpapi_property_details_link will be present as a canonical way to retrieve the property details using property_token.

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
