---
id: "url-438fcdc"
type: "api"
title: "Place search"
url: "https://api-dashboard.search.brave.com/documentation/services/place-search"
description: "Place Search is built for finding geographic places. Where Web Search finds web pages, Place Search finds locations in the physical world — coffee shops, museums, hotels, parks, and any other point of interest. You can anchor your search to a specific area using coordinates or a location name, or cast a broader net and let the index surface the most relevant matches globally."
source: ""
tags: []
crawl_time: "2026-03-18T03:28:18.196Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/local/place_search?latitude=37.7749&longitude=-122.4194&q=coffee+shops&radius=1000"
  method: "GET"
  sections:
    - {"level":"H2","title":"Overview","content":["Place Search is built for finding geographic places. Where Web Search finds web pages, Place Search finds locations in the physical world — coffee shops, museums, hotels, parks, and any other point of interest. You can anchor your search to a specific area using coordinates or a location name, or cast a broader net and let the index surface the most relevant matches globally.","With over 200 million indexed places worldwide, the API works well for everything from “find a specific restaurant nearby” to “what are the major landmarks associated with this city”."],"codeBlocks":[]}
    - {"level":"H2","title":"Key Features","content":["200M+ Places Access our comprehensive global index of over 200 million points of interest   Flexible Geography Search near coordinates or a location name — with or without a radius constraint   Rich POI Data Get detailed information including ratings, hours, contact info, and photos   Explore Mode Discover general points of interest in an area without a specific query","Place Search is part of Search plan. Subscribe to use this feature."],"codeBlocks":[]}
    - {"level":"H2","title":"200M+ Places","content":["Access our comprehensive global index of over 200 million points of interest"],"codeBlocks":[]}
    - {"level":"H2","title":"Flexible Geography","content":["Search near coordinates or a location name — with or without a radius constraint"],"codeBlocks":[]}
    - {"level":"H2","title":"Rich POI Data","content":["Get detailed information including ratings, hours, contact info, and photos"],"codeBlocks":[]}
    - {"level":"H2","title":"Explore Mode","content":["Discover general points of interest in an area without a specific query"],"codeBlocks":[]}
    - {"level":"H2","title":"Place Search API Documentation","content":["View the complete API reference, including endpoints, parameters, and example requests"],"codeBlocks":[]}
    - {"level":"H2","title":"Use Cases","content":["Place Search is a good fit when your goal is geographic discovery:","• Location-Based Apps: Build apps that help users discover nearby places\n• Travel & Tourism: Find attractions, restaurants, and hotels in any destination\n• Business Directories: Create local business listings and discovery features\n• Mapping Applications: Populate maps with relevant points of interest\n• Geofenced Recommendations: Suggest places based on user location"],"codeBlocks":[]}
    - {"level":"H2","title":"Basic Usage","content":["Search for places near a set of coordinates:","Or use a location name if you don’t have coordinates at hand:","The response includes a list of matching places with detailed information:"],"codeBlocks":["{\n  \"type\": \"locations\",\n  \"query\": {\n    \"original\": \"coffee shops\",\n    \"altered\": null,\n    \"spellcheck_off\": false,\n    \"show_strict_warning\": false\n  },\n  \"results\": [\n    {\n      \"type\": \"location_result\",\n      \"id\": \"loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY=\",\n      \"title\": \"Blue Bottle Coffee\",\n      \"url\": \"https://bluebottlecoffee.com\",\n      \"provider_url\": \"https://yelp.com/biz/blue-bottle-coffee-sf\",\n      \"coordinates\": [37.7825, -122.4095],\n      \"postal_address\": {\n        \"type\": \"PostalAddress\",\n        \"displayAddress\": \"66 Mint St, San Francisco, CA 94103\",\n        \"streetAddress\": \"66 Mint St\",\n        \"addressLocality\": \"San Francisco\",\n        \"addressRegion\": \"CA\",\n        \"postalCode\": \"94103\",\n        \"country\": \"US\"\n      },\n      \"rating\": {\n        \"ratingValue\": 4.5,\n        \"bestRating\": 5.0,\n        \"reviewCount\": 1250\n      },\n      \"opening_hours\": {\n        \"current_day\": [\n          {\n            \"abbr_name\": \"Tue\",\n            \"full_name\": \"Tuesday\",\n            \"opens\": \"07:00\",\n            \"closes\": \"18:00\"\n          }\n        ]\n      },\n      \"distance\": {\n        \"value\": 0.3,\n        \"units\": \"km\"\n      },\n      \"categories\": [\"Coffee & Tea\", \"Cafe\"],\n      \"price_range\": \"$$\",\n      \"thumbnail\": {\n        \"src\": \"https://example.com/thumb.jpg\",\n        \"original\": \"https://example.com/original.jpg\"\n      },\n      \"timezone\": \"America/Los_Angeles\"\n    }\n  ],\n  \"location\": {\n    \"coordinates\": [37.7749, -122.4194],\n    \"name\": \"San Francisco\",\n    \"country\": \"US\"\n  }\n}"]}
    - {"level":"H2","title":"Request Parameters","content":["Providing a geographic anchor is optional but strongly recommended for most queries. You can use either coordinates (latitude + longitude) or a location string. If neither is given, results are sourced more broadly and may be less precise.","ParameterTypeDescriptionlatitudefloatLatitude of the search center (-90.0 to +90.0). Required together with longitude.longitudefloatLongitude of the search center (-180.0 to +180.0). Required together with latitude.locationstringLocation name, alternative to coordinates. For US locations use the form city state country (e.g., san francisco ca united states). For non-US locations use city country (e.g., tokyo japan). Case-insensitive, no commas needed. Multilingual supported.","ParameterTypeDefaultDescriptionqstring—What to look for (e.g., coffee shops, pizza, museums). Omit for general area exploration.radiusfloat—Search radius in meters, centered on the provided coordinates. See Radius and result quality.countint20Number of results to return (1 to 50)","ParameterTypeDefaultDescriptioncountrystringUSTwo-letter country code (ISO 3166-1 alpha-2)search_langstringenSearch language (2+ character language code)ui_langstringen-USUI language for the response (locale code)unitsstringmetricMeasurement units: metric or imperialsafesearchstringstrictSafe search level: off, moderate, or strictspellcheckbooltrueWhether to apply spellcheck to the query"],"codeBlocks":[]}
    - {"level":"H3","title":"Location","content":["Providing a geographic anchor is optional but strongly recommended for most queries. You can use either coordinates (latitude + longitude) or a location string. If neither is given, results are sourced more broadly and may be less precise.","ParameterTypeDescriptionlatitudefloatLatitude of the search center (-90.0 to +90.0). Required together with longitude.longitudefloatLongitude of the search center (-180.0 to +180.0). Required together with latitude.locationstringLocation name, alternative to coordinates. For US locations use the form city state country (e.g., san francisco ca united states). For non-US locations use city country (e.g., tokyo japan). Case-insensitive, no commas needed. Multilingual supported."],"codeBlocks":[]}
    - {"level":"H3","title":"Search","content":["ParameterTypeDefaultDescriptionqstring—What to look for (e.g., coffee shops, pizza, museums). Omit for general area exploration.radiusfloat—Search radius in meters, centered on the provided coordinates. See Radius and result quality.countint20Number of results to return (1 to 50)"],"codeBlocks":[]}
    - {"level":"H3","title":"Locale and Preferences","content":["ParameterTypeDefaultDescriptioncountrystringUSTwo-letter country code (ISO 3166-1 alpha-2)search_langstringenSearch language (2+ character language code)ui_langstringen-USUI language for the response (locale code)unitsstringmetricMeasurement units: metric or imperialsafesearchstringstrictSafe search level: off, moderate, or strictspellcheckbooltrueWhether to apply spellcheck to the query"],"codeBlocks":[]}
    - {"level":"H2","title":"Radius and Result Quality","content":["The radius parameter controls how tightly the search is anchored to your coordinates. No upper limit is enforced, so you can search a neighborhood or an entire region.","In practice, a tighter radius tends to produce more focused results. When you search within a compact area, the index can confidently surface places that are unambiguously nearby. As the radius grows — or when no radius is given — results are drawn from a wider pool, which works well for well-known or distinctive places but may be less precise for common query types where many candidates exist across a large area.","A few rough guidelines:","• Under ~20 km: Results are typically well-matched to the search area. Good for “what’s near me” use cases.\n• Larger areas or no radius: Works best for specific or distinctive queries (a particular museum, a named landmark, a regional specialty). Generic category searches (e.g., restaurants, hotels) may return a broader set of candidates.","If your use case is finding a specific known place by name or type across a wide region, omitting the radius or using a large one is fine. For density-based searches — “show me all the pharmacies in this district” — a tighter radius will give cleaner results."],"codeBlocks":[]}
    - {"level":"H2","title":"Location String Format","content":["When using the location parameter instead of coordinates, follow these conventions:","RegionFormatExampleUnited Statescity state countrysan francisco ca united statesOther countriescity countrytokyo japanMultilingualnative or English namenueva york or new york","No commas or special characters are needed, and capitalization does not matter. English or the most popular language for the target city generally works best."],"codeBlocks":[]}
    - {"level":"H2","title":"Explore Mode","content":["Omit q to get a general snapshot of points of interest in an area — useful for map views, destination previews, or any feature where you want to show what’s around a location rather than answer a specific query:"],"codeBlocks":[]}
    - {"level":"H2","title":"Fetching Additional POI Details","content":["Each result includes an id that works with the same detail endpoints used for Web Search location results — so the same integration serves both.","Use /local/pois to fetch photos, web result mentions, profiles, and more:","Use /local/descriptions to get AI-generated descriptions for locations:","You can request details for up to 20 POIs in a single request by providing multiple ids parameters.","POI IDs are interchangeable: The same IDs work whether they came from Place Search or Web Search location results, making it straightforward to build unified experiences across both.","POI IDs are ephemeral and expire after approximately 8 hours. Do not store them for later use."],"codeBlocks":[]}
    - {"level":"H3","title":"Detailed POI Information","content":["Use /local/pois to fetch photos, web result mentions, profiles, and more:"],"codeBlocks":[]}
    - {"level":"H3","title":"AI-Generated Descriptions","content":["Use /local/descriptions to get AI-generated descriptions for locations:","You can request details for up to 20 POIs in a single request by providing multiple ids parameters.","POI IDs are interchangeable: The same IDs work whether they came from Place Search or Web Search location results, making it straightforward to build unified experiences across both.","POI IDs are ephemeral and expire after approximately 8 hours. Do not store them for later use."],"codeBlocks":[]}
    - {"level":"H2","title":"Response Fields","content":["FieldTypeDescriptiontypestringAlways \"location_result\"idstringTemporary identifier for fetching additional details (valid ~8 hours)titlestringName of the locationurlstringCanonical URLprovider_urlstringProvider page URLdescriptionstringShort descriptioncoordinates[float, float]Latitude and longitudepostal_addressobjectAddress with displayAddress, streetAddress, addressLocality, addressRegion, postalCode, countryopening_hoursobjectBusiness hours with current_day and days arrayscontactobjectContact info with telephone and emailratingobjectRatings with ratingValue, bestRating, reviewCountprice_rangestringPrice classification (e.g., \"$$\")distanceobjectDistance from search center with value and unitscategoriesarrayCategory classificationsserves_cuisinearrayCuisine types (for restaurants)thumbnailobjectPrimary image with src and originalpicturesobjectAdditional photosprofilesarrayExternal profiles (name, url, long_name, img)timezonestringIANA timezone identifier (e.g., \"America/Los_Angeles\")"],"codeBlocks":[]}
    - {"level":"H3","title":"LocationResult Fields","content":["FieldTypeDescriptiontypestringAlways \"location_result\"idstringTemporary identifier for fetching additional details (valid ~8 hours)titlestringName of the locationurlstringCanonical URLprovider_urlstringProvider page URLdescriptionstringShort descriptioncoordinates[float, float]Latitude and longitudepostal_addressobjectAddress with displayAddress, streetAddress, addressLocality, addressRegion, postalCode, countryopening_hoursobjectBusiness hours with current_day and days arrayscontactobjectContact info with telephone and emailratingobjectRatings with ratingValue, bestRating, reviewCountprice_rangestringPrice classification (e.g., \"$$\")distanceobjectDistance from search center with value and unitscategoriesarrayCategory classificationsserves_cuisinearrayCuisine types (for restaurants)thumbnailobjectPrimary image with src and originalpicturesobjectAdditional photosprofilesarrayExternal profiles (name, url, long_name, img)timezonestringIANA timezone identifier (e.g., \"America/Los_Angeles\")"],"codeBlocks":[]}
    - {"level":"H2","title":"Rate Limits and Billing","content":["Place Search requests are billed separately from Web Search. Check your subscription dashboard for current limits and usage."],"codeBlocks":[]}
    - {"level":"H2","title":"Changelog","content":["• 2026-03-04 Lifted radius restrictions. Radius now defaults to none.\n• 2026-01-15 Add Place Search endpoint for geographic POI discovery."],"codeBlocks":[]}
  tables:
    - {"index":0,"headers":["Parameter","Type","Description"],"rows":[["latitude","float","Latitude of the search center (-90.0 to +90.0). Required together with longitude."],["longitude","float","Longitude of the search center (-180.0 to +180.0). Required together with latitude."],["location","string","Location name, alternative to coordinates. For US locations use the form city state country (e.g., san francisco ca united states). For non-US locations use city country (e.g., tokyo japan). Case-insensitive, no commas needed. Multilingual supported."]]}
    - {"index":1,"headers":["Parameter","Type","Default","Description"],"rows":[["q","string","—","What to look for (e.g., coffee shops, pizza, museums). Omit for general area exploration."],["radius","float","—","Search radius in meters, centered on the provided coordinates. See Radius and result quality."],["count","int","20","Number of results to return (1 to 50)"]]}
    - {"index":2,"headers":["Parameter","Type","Default","Description"],"rows":[["country","string","US","Two-letter country code (ISO 3166-1 alpha-2)"],["search_lang","string","en","Search language (2+ character language code)"],["ui_lang","string","en-US","UI language for the response (locale code)"],["units","string","metric","Measurement units: metric or imperial"],["safesearch","string","strict","Safe search level: off, moderate, or strict"],["spellcheck","bool","true","Whether to apply spellcheck to the query"]]}
    - {"index":3,"headers":["Region","Format","Example"],"rows":[["United States","city state country","san francisco ca united states"],["Other countries","city country","tokyo japan"],["Multilingual","native or English name","nueva york or new york"]]}
    - {"index":4,"headers":["Field","Type","Description"],"rows":[["type","string","Always \"locations\""],["query","object","Query information including original and spell-corrected forms"],["query.original","string","The original query that was requested"],["query.altered","string?","The spell-corrected query, if spellcheck was applied. null if no correction was made"],["query.spellcheck_off","bool?","Whether spellcheck was disabled for this query"],["query.show_strict_warning","bool?","Whether strict safesearch filtered results"],["results","array","List of LocationResult objects"],["location","object","Resolved location information (present when coordinates were provided or resolved)"],["location.coordinates","[float, float]","Latitude and longitude of the resolved search center"],["location.name","string","Resolved location name (e.g., \"San Francisco\")"],["location.country","string","Two-letter country code (e.g., \"US\")"]]}
    - {"index":5,"headers":["Field","Type","Description"],"rows":[["type","string","Always \"location_result\""],["id","string","Temporary identifier for fetching additional details (valid ~8 hours)"],["title","string","Name of the location"],["url","string","Canonical URL"],["provider_url","string","Provider page URL"],["description","string","Short description"],["coordinates","[float, float]","Latitude and longitude"],["postal_address","object","Address with displayAddress, streetAddress, addressLocality, addressRegion, postalCode, country"],["opening_hours","object","Business hours with current_day and days arrays"],["contact","object","Contact info with telephone and email"],["rating","object","Ratings with ratingValue, bestRating, reviewCount"],["price_range","string","Price classification (e.g., \"$$\")"],["distance","object","Distance from search center with value and units"],["categories","array","Category classifications"],["serves_cuisine","array","Cuisine types (for restaurants)"],["thumbnail","object","Primary image with src and original"],["pictures","object","Additional photos"],["profiles","array","External profiles (name, url, long_name, img)"],["timezone","string","IANA timezone identifier (e.g., \"America/Los_Angeles\")"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/place_search?latitude=37.7749&longitude=-122.4194&q=coffee+shops&radius=1000\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/place_search?latitude=37.7749&longitude=-122.4194&q=coffee+shops&radius=1000\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/place_search?location=san+francisco+ca+united+states&q=coffee+shops\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/place_search?location=san+francisco+ca+united+states&q=coffee+shops\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"locations\",\n  \"query\": {\n    \"original\": \"coffee shops\",\n    \"altered\": null,\n    \"spellcheck_off\": false,\n    \"show_strict_warning\": false\n  },\n  \"results\": [\n    {\n      \"type\": \"location_result\",\n      \"id\": \"loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY=\",\n      \"title\": \"Blue Bottle Coffee\",\n      \"url\": \"https://bluebottlecoffee.com\",\n      \"provider_url\": \"https://yelp.com/biz/blue-bottle-coffee-sf\",\n      \"coordinates\": [37.7825, -122.4095],\n      \"postal_address\": {\n        \"type\": \"PostalAddress\",\n        \"displayAddress\": \"66 Mint St, San Francisco, CA 94103\",\n        \"streetAddress\": \"66 Mint St\",\n        \"addressLocality\": \"San Francisco\",\n        \"addressRegion\": \"CA\",\n        \"postalCode\": \"94103\",\n        \"country\": \"US\"\n      },\n      \"rating\": {\n        \"ratingValue\": 4.5,\n        \"bestRating\": 5.0,\n        \"reviewCount\": 1250\n      },\n      \"opening_hours\": {\n        \"current_day\": [\n          {\n            \"abbr_name\": \"Tue\",\n            \"full_name\": \"Tuesday\",\n            \"opens\": \"07:00\",\n            \"closes\": \"18:00\"\n          }\n        ]\n      },\n      \"distance\": {\n        \"value\": 0.3,\n        \"units\": \"km\"\n      },\n      \"categories\": [\"Coffee & Tea\", \"Cafe\"],\n      \"price_range\": \"$$\",\n      \"thumbnail\": {\n        \"src\": \"https://example.com/thumb.jpg\",\n        \"original\": \"https://example.com/original.jpg\"\n      },\n      \"timezone\": \"America/Los_Angeles\"\n    }\n  ],\n  \"location\": {\n    \"coordinates\": [37.7749, -122.4194],\n    \"name\": \"San Francisco\",\n    \"country\": \"US\"\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"locations\",\n  \"query\": {\n    \"original\": \"coffee shops\",\n    \"altered\": null,\n    \"spellcheck_off\": false,\n    \"show_strict_warning\": false\n  },\n  \"results\": [\n    {\n      \"type\": \"location_result\",\n      \"id\": \"loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY=\",\n      \"title\": \"Blue Bottle Coffee\",\n      \"url\": \"https://bluebottlecoffee.com\",\n      \"provider_url\": \"https://yelp.com/biz/blue-bottle-coffee-sf\",\n      \"coordinates\": [37.7825, -122.4095],\n      \"postal_address\": {\n        \"type\": \"PostalAddress\",\n        \"displayAddress\": \"66 Mint St, San Francisco, CA 94103\",\n        \"streetAddress\": \"66 Mint St\",\n        \"addressLocality\": \"San Francisco\",\n        \"addressRegion\": \"CA\",\n        \"postalCode\": \"94103\",\n        \"country\": \"US\"\n      },\n      \"rating\": {\n        \"ratingValue\": 4.5,\n        \"bestRating\": 5.0,\n        \"reviewCount\": 1250\n      },\n      \"opening_hours\": {\n        \"current_day\": [\n          {\n            \"abbr_name\": \"Tue\",\n            \"full_name\": \"Tuesday\",\n            \"opens\": \"07:00\",\n            \"closes\": \"18:00\"\n          }\n        ]\n      },\n      \"distance\": {\n        \"value\": 0.3,\n        \"units\": \"km\"\n      },\n      \"categories\": [\"Coffee & Tea\", \"Cafe\"],\n      \"price_range\": \"$$\",\n      \"thumbnail\": {\n        \"src\": \"https://example.com/thumb.jpg\",\n        \"original\": \"https://example.com/original.jpg\"\n      },\n      \"timezone\": \"America/Los_Angeles\"\n    }\n  ],\n  \"location\": {\n    \"coordinates\": [37.7749, -122.4194],\n    \"name\": \"San Francisco\",\n    \"country\": \"US\"\n  }\n}"}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/place_search?latitude=40.7128&longitude=-74.0060&radius=2000&count=10\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/place_search?latitude=40.7128&longitude=-74.0060&radius=2000&count=10\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/pois?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY=\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/pois?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY=\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/descriptions?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY=\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/local/descriptions?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY=\" \\\n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nService APIs\n\nFind geographic places — businesses, landmarks, and points of interest — from our index of over 200 million locations worldwide\n\nOverview\n\nPlace Search is built for finding geographic places. Where Web Search finds web pages, Place Search finds locations in the physical world — coffee shops, museums, hotels, parks, and any other point of interest. You can anchor your search to a specific area using coordinates or a location name, or cast a broader net and let the index surface the most relevant matches globally.\n\nWith over 200 million indexed places worldwide, the API works well for everything from “find a specific restaurant nearby” to “what are the major landmarks associated with this city”.\n\nKey Features\n\n200M+ Places\n\nAccess our comprehensive global index of over 200 million points of interest\n\nFlexible Geography\n\nSearch near coordinates or a location name — with or without a radius constraint\n\nRich POI Data\n\nGet detailed information including ratings, hours, contact info, and photos\n\nExplore Mode\n\nDiscover general points of interest in an area without a specific query\n\nPlace Search is part of Search plan. Subscribe to use this feature.\n\nAPI Reference\n\nPlace Search API Documentation\n\nView the complete API reference, including endpoints, parameters, and example requests\n\nUse Cases\n\nPlace Search is a good fit when your goal is geographic discovery:\n\nLocation-Based Apps: Build apps that help users discover nearby places\n\nTravel & Tourism: Find attractions, restaurants, and hotels in any destination\n\nBusiness Directories: Create local business listings and discovery features\n\nMapping Applications: Populate maps with relevant points of interest\n\nGeofenced Recommendations: Suggest places based on user location\n\nBasic Usage\n\nSearch for places near a set of coordinates:\n\nOr use a location name if you don’t have coordinates at hand:\n\nThe response includes a list of matching places with detailed information:\n\nRequest Parameters\n\nLocation\n\nProviding a geographic anchor is optional but strongly recommended for most queries. You can use either coordinates (latitude + longitude) or a location string. If neither is given, results are sourced more broadly and may be less precise.\n\nSearch\n\nLocale and Preferences\n\nRadius and Result Quality\n\nThe radius parameter controls how tightly the search is anchored to your coordinates. No upper limit is enforced, so you can search a neighborhood or an entire region.\n\nIn practice, a tighter radius tends to produce more focused results. When you search within a compact area, the index can confidently surface places that are unambiguously nearby. As the radius grows — or when no radius is given — results are drawn from a wider pool, which works well for well-known or distinctive places but may be less precise for common query types where many candidates exist across a large area.\n\nA few rough guidelines:\n\nUnder ~20 km: Results are typically well-matched to the search area. Good for “what’s near me” use cases.\n\nLarger areas or no radius: Works best for specific or distinctive queries (a particular museum, a named landmark, a regional specialty). Generic category searches (e.g., restaurants, hotels) may return a broader set of candidates.\n\nIf your use case is finding a specific known place by name or type across a wide region, omitting the radius or using a large one is fine. For density-based searches — “show me all the pharmacies in this district” — a tighter radius will give cleaner results.\n\nLocation String Format\n\nWhen using the location parameter instead of coordinates, follow these conventions:\n\nNo commas or special characters are needed, and capitalization does not matter. English or the most popular language for the target city generally works best.\n\nOmit q to get a general snapshot of points of interest in an area — useful for map views, destination previews, or any feature where you want to show what’s around a location rather than answer a specific query:\n\nFetching Additional POI Details\n\nEach result includes an id that works with the same detail endpoints used for Web Search location results — so the same integration serves both.\n\nDetailed POI Information\n\nUse /local/pois to fetch photos, web result mentions, profiles, and more:\n\nAI-Generated Descriptions\n\nUse /local/descriptions to get AI-generated descriptions for locations:\n\nYou can request details for up to 20 POIs in a single request by providing multiple ids parameters.\n\nPOI IDs are interchangeable: The same IDs work whether they came from Place Search or Web Search location results, making it straightforward to build unified experiences across both.\n\nPOI IDs are ephemeral and expire after approximately 8 hours. Do not store them for later use.\n\nResponse Fields\n\nTop-Level Fields\n\nLocationResult Fields\n\nExample: Building a Nearby Places Feature\n\nPython\n\nRate Limits and Billing\n\nPlace Search requests are billed separately from Web Search. Check your subscription dashboard for current limits and usage.\n\nChangelog\n\n2026-03-04 Lifted radius restrictions. Radius now defaults to none.\n\n2026-01-15 Add Place Search endpoint for geographic POI discovery.\n\nOn this page\n\n200M+ Places Access our comprehensive global index of over 200 million points of interest\n\nFlexible Geography Search near coordinates or a location name — with or without a radius constraint\n\nRich POI Data Get detailed information including ratings, hours, contact info, and photos\n\nExplore Mode Discover general points of interest in an area without a specific query\n\nPlace Search API Documentation View the complete API reference, including endpoints, parameters, and example requests"
  suggestedFilename: "services-place-search"
---

# Place search

## 源URL

https://api-dashboard.search.brave.com/documentation/services/place-search

## 描述

Place Search is built for finding geographic places. Where Web Search finds web pages, Place Search finds locations in the physical world — coffee shops, museums, hotels, parks, and any other point of interest. You can anchor your search to a specific area using coordinates or a location name, or cast a broader net and let the index surface the most relevant matches globally.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/local/place_search?latitude=37.7749&longitude=-122.4194&q=coffee+shops&radius=1000`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/local/place_search?latitude=37.7749&longitude=-122.4194&q=coffee+shops&radius=1000" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "type": "locations",
  "query": {
    "original": "coffee shops",
    "altered": null,
    "spellcheck_off": false,
    "show_strict_warning": false
  },
  "results": [
    {
      "type": "location_result",
      "id": "loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY=",
      "title": "Blue Bottle Coffee",
      "url": "https://bluebottlecoffee.com",
      "provider_url": "https://yelp.com/biz/blue-bottle-coffee-sf",
      "coordinates": [37.7825, -122.4095],
      "postal_address": {
        "type": "PostalAddress",
        "displayAddress": "66 Mint St, San Francisco, CA 94103",
        "streetAddress": "66 Mint St",
        "addressLocality": "San Francisco",
        "addressRegion": "CA",
        "postalCode": "94103",
        "country": "US"
      },
      "rating": {
        "ratingValue": 4.5,
        "bestRating": 5.0,
        "reviewCount": 1250
      },
      "opening_hours": {
        "current_day": [
          {
            "abbr_name": "Tue",
            "full_name": "Tuesday",
            "opens": "07:00",
            "closes": "18:00"
          }
        ]
      },
      "distance": {
        "value": 0.3,
        "units": "km"
      },
      "categories": ["Coffee & Tea", "Cafe"],
      "price_range": "$$",
      "thumbnail": {
        "src": "https://example.com/thumb.jpg",
        "original": "https://example.com/original.jpg"
      },
      "timezone": "America/Los_Angeles"
    }
  ],
  "location": {
    "coordinates": [37.7749, -122.4194],
    "name": "San Francisco",
    "country": "US"
  }
}
```

### 示例 3 (bash)

```bash
curl "https://api.search.brave.com/res/v1/local/pois?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY=" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 4 (bash)

```bash
curl "https://api.search.brave.com/res/v1/local/descriptions?ids=loc4FNMQJNOOCVHEB7UBOLN354ZYIDIYJ3RPRETERRY=" \
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

## 文档正文

Place Search is built for finding geographic places. Where Web Search finds web pages, Place Search finds locations in the physical world — coffee shops, museums, hotels, parks, and any other point of interest. You can anchor your search to a specific area using coordinates or a location name, or cast a broader net and let the index surface the most relevant matches globally.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/local/place_search?latitude=37.7749&longitude=-122.4194&q=coffee+shops&radius=1000`

Quickstart

Pricing

Authentication

Versioning

Rate limiting

Web search

LLM Context New

News search

Video search

Image search

Summarizer search

Place search New

Answers

Autosuggest

Spellcheck

Skills

Help & Feedback

Goggles

Search operators

Status updates

Security

Privacy notice

Terms of service

Service APIs

Find geographic places — businesses, landmarks, and points of interest — from our index of over 200 million locations worldwide

Overview

Place Search is built for finding geographic places. Where Web Search finds web pages, Place Search finds locations in the physical world — coffee shops, museums, hotels, parks, and any other point of interest. You can anchor your search to a specific area using coordinates or a location name, or cast a broader net and let the index surface the most relevant matches globally.

With over 200 million indexed places worldwide, the API works well for everything from “find a specific restaurant nearby” to “what are the major landmarks associated with this city”.

Key Features

200M+ Places

Access our comprehensive global index of over 200 million points of interest

Flexible Geography

Search near coordinates or a location name — with or without a radius constraint

Rich POI Data

Get detailed information including ratings, hours, contact info, and photos

Explore Mode

Discover general points of interest in an area without a specific query

Place Search is part of Search plan. Subscribe to use this feature.

API Reference

Place Search API Documentation

View the complete API reference, including endpoints, parameters, and example requests

Use Cases

Place Search is a good fit when your goal is geographic discovery:

Location-Based Apps: Build apps that help users discover nearby places

Travel & Tourism: Find attractions, restaurants, and hotels in any destination

Business Directories: Create local business listings and discovery features

Mapping Applications: Populate maps with relevant points of interest

Geofenced Recommendations: Suggest places based on user location

Basic Usage

Search for places near a set of coordinates:

Or use a location name if you don’t have coordinates at hand:

The response includes a list of matching places with detailed information:

Request Parameters

Location

Providing a geographic anchor is optional but strongly recommended for most queries. You can use either coordinates (latitude + longitude) or a location string. If neither is given, results are sourced more broadly and may be less precise.

Search

Locale and Preferences

Radius and Result Quality

The radius parameter controls how tightly the search is anchored to your coordinates. No upper limit is enforced, so you can search a neighborhood or an entire region.

In practice, a tighter radius tends to produce more focused results. When you search within a compact area, the index can confidently surface places that are unambiguously nearby. As the radius grows — or when no radius is given — results are drawn from a wider pool, which works well for well-known or distinctive places but may be less precise for common query types where many candidates exist across a large area.

A few rough guidelines:

Under ~20 km: Results are typically well-matched to the search area. Good for “what’s near me” use cases.

Larger areas or no radius: Works best for specific or distinctive queries (a particular museum, a named landmark, a regional specialty). Generic category searches (e.g., restaurants, hotels) may return a broader set of candidates.

If your use case is finding a specific known place by name or type across a wide region, omitting the radius or using a large one is fine. For density-based searches — “show me all the pharmacies in this district” — a tighter radius will give cleaner results.

Location String Format

When using the location parameter instead of coordinates, follow these conventions:

No commas or special characters are needed, and capitalization does not matter. English or the most popular language for the target city generally works best.

Omit q to get a general snapshot of points of interest in an area — useful for map views, destination previews, or any feature where you want to show what’s around a location rather than answer a specific query:

Fetching Additional POI Details

Each result includes an id that works with the same detail endpoints used for Web Search location results — so the same integration serves both.

Detailed POI Information

Use /local/pois to fetch photos, web result mentions, profiles, and more:

AI-Generated Descriptions

Use /local/descriptions to get AI-generated descriptions for locations:

You can request details for up to 20 POIs in a single request by providing multiple ids parameters.

POI IDs are interchangeable: The same IDs work whether they came from Place Search or Web Search location results, making it straightforward to build unified experiences across both.

POI IDs are ephemeral and expire after app
