---
id: "url-7d867c7c"
type: "api"
title: "Google Local Pack API"
url: "https://serpapi.com/local-pack"
description: "For some requests, Google search includes local results, called local pack, and a local map. SerpApi is able to scrape, extract, and make sense of this information.When SerpApi encounters a local map and/or local results, we add them to our JSON output. From the local_map, we are able to extract link, gps_coordinates, image and streetview information. From the local_results, we are able to extract position title, reviews, price, type, address, description, hours, extensions, thumbnail, gps_coordinates, place_id, lsig and more.\n\nThe API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.\n\nNote the additional within_radius place field that tells whether the returned place is within the requested radius. It's included only when radius parameter is specified and place has gps_coordinates.\n\nNote the additional gl search parameter, in this case for France. With some countries, coordinates should be accompanied with the matching country parameter. Otherwise, incorrect search results are returned.\n\nWhen the device is set to mobile, we sometimes see ads in local_results.places, which are identified by the ad field being set to true."
source: ""
tags: []
crawl_time: "2026-03-18T04:10:23.598Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Results for: stores and places","description":"","requestParams":{"q":"McDonald's","highlight":"local_results"},"responseJson":"https://serpapi.com/search.json?q=McDonald's"}
    - {"title":"Results for: products","description":"","requestParams":{"q":"Coffee","location":"New York, New York, United States","highlight":"local_results"},"responseJson":"https://serpapi.com/search.json?q=Coffee&location=New+York,+New+York,+United+States"}
    - {"title":"Results for: specific addresses","description":"","requestParams":{"q":"500 Comal St, Austin, TX 78702 United States","highlight":"local_results"},"responseJson":"https://serpapi.com/search.json?q=500+Comal+St,+Austin,+TX+78702+United+States"}
    - {"title":"Results for cafes nearby with New York coordinates and the radius","description":"Note the additional within_radius place field that tells whether the returned place is within the requested radius. It's included only when radius parameter is specified and place has gps_coordinates.","requestParams":{"q":"cafes nearby","lat":"40.58788097425217","lon":"-73.95527792835198","radius":"150.75","highlight":"local_results"},"responseJson":"https://serpapi.com/search.json?q=cafes+nearby&lat=40.58788097425217&lon=-73.95527792835198&radius=150.75"}
    - {"title":"Results for cafes nearby with Paris coordinates and the radius","description":"Note the additional gl search parameter, in this case for France. With some countries, coordinates should be accompanied with the matching country parameter. Otherwise, incorrect search results are returned.","requestParams":{"q":"cafes nearby","lat":"48.87069489094314","lon":"2.3322903791831706","radius":"150.75","gl":"fr","highlight":"local_results"},"responseJson":"https://serpapi.com/search.json?q=cafes+nearby&lat=48.87069489094314&lon=2.3322903791831706&radius=150.75&gl=fr"}
    - {"title":"Results for q: plumber, and device: mobile","description":"When the device is set to mobile, we sometimes see ads in local_results.places, which are identified by the ad field being set to true.","requestParams":{"q":"plumber","device":"mobile","highlight":"local_results"},"responseJson":"https://serpapi.com/search.json?q=plumber&device=mobile"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "local-pack-api"
---

# Google Local Pack API

## 源URL

https://serpapi.com/local-pack

## 描述

For some requests, Google search includes local results, called local pack, and a local map. SerpApi is able to scrape, extract, and make sense of this information.When SerpApi encounters a local map and/or local results, we add them to our JSON output. From the local_map, we are able to extract link, gps_coordinates, image and streetview information. From the local_results, we are able to extract position title, reviews, price, type, address, description, hours, extensions, thumbnail, gps_coordinates, place_id, lsig and more.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

Note the additional within_radius place field that tells whether the returned place is within the requested radius. It's included only when radius parameter is specified and place has gps_coordinates.

Note the additional gl search parameter, in this case for France. With some countries, coordinates should be accompanied with the matching country parameter. Otherwise, incorrect search results are returned.

When the device is set to mobile, we sometimes see ads in local_results.places, which are identified by the ad field being set to true.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

For some requests, Google search includes local results, called local pack, and a local map. SerpApi is able to scrape, extract, and make sense of this information.When SerpApi encounters a local map and/or local results, we add them to our JSON output. From the local_map, we are able to extract link, gps_coordinates, image and streetview information. From the local_results, we are able to extract position title, reviews, price, type, address, description, hours, extensions, thumbnail, gps_coordinates, place_id, lsig and more.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

Note the additional within_radius place field that tells whether the returned place is within the requested radius. It's included only when radius parameter is specified and place has gps_coordinates.

Note the additional gl search parameter, in this case for France. With some countries, coordinates should be accompanied with the matching country parameter. Otherwise, incorrect search results are returned.

When the device is set to mobile, we sometimes see ads in local_results.places, which are identified by the ad field being set to true.

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
