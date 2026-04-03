---
id: "url-737be33d"
type: "api"
title: "YouTube Video API"
url: "https://serpapi.com/youtube-video-api"
description: "Youtube Video API allows you to scrape video details from Youtube. Video details such as description, view count, related videos, comments, replies, and many others.\n\nThe API endpoint is https://serpapi.com/search?engine=youtube_video Head to the playground for a live and interactive demo.\n\nTo further get comments, use the comments_next_page_token or comments_sorting_token.token from this result.To paginate related videos, use the related_videos_next_page_token from this result.\n\nUse the comments_next_page_token from the video result to get the initial comments. And use the same key from this result for pagination.To further get replies of a comment, use the replies_next_page_token from the comment.\n\nUse the replies_next_page_token from the comment item to get the initial replies. And use the same key from this result for pagination."
source: ""
tags: []
crawl_time: "2026-03-18T19:13:59.856Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "youtube_video"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Typical results","description":"To further get comments, use the comments_next_page_token or comments_sorting_token.token from this result. To paginate related videos, use the related_videos_next_page_token from this result.","requestParams":{"engine":"youtube_video","v":"vFcS080VYQ0"},"responseJson":"https://serpapi.com/search.json?engine=youtube_video&v=vFcS080VYQ0"}
    - {"title":"Live video results","description":"","requestParams":{"engine":"youtube_video","v":"tduwK1tNxEg"},"responseJson":"https://serpapi.com/search.json?engine=youtube_video&v=tduwK1tNxEg"}
    - {"title":"Video with additional info block (parental warning)","description":"","requestParams":{"engine":"youtube_video","v":"erMYt-Ztmdw"},"responseJson":"https://serpapi.com/search.json?engine=youtube_video&v=erMYt-Ztmdw"}
    - {"title":"Video with additional info block (age restriction notice)","description":"","requestParams":{"engine":"youtube_video","v":"q2UpP10V-6U"},"responseJson":"https://serpapi.com/search.json?engine=youtube_video&v=q2UpP10V-6U"}
    - {"title":"Example for shopping results","description":"","requestParams":{"engine":"youtube_video","v":"ENhfIeZF_AY"},"responseJson":"https://serpapi.com/search.json?engine=youtube_video&v=ENhfIeZF_AY"}
    - {"title":"Example for comments","description":"Use the comments_next_page_token from the video result to get the initial comments. And use the same key from this result for pagination. To further get replies of a comment, use the replies_next_page_token from the comment.","requestParams":{"engine":"youtube_video","next_page_token":"Eg0SC0VOaGZJZVpGX0FZGAYyJSIRIgtFTmhmSWVaRl9BWTAAeAJCEGNvbW1lbnRzLXNlY3Rpb24%3D"},"responseJson":"https://serpapi.com/search.json?engine=youtube_video&next_page_token=Eg0SC0VOaGZJZVpGX0FZGAYyJSIRIgtFTmhmSWVaRl9BWTAAeAJCEGNvbW1lbnRzLXNlY3Rpb24%3D"}
    - {"title":"Example replies for comment id UgwgDTmQSDph3n7Lyr54AaABAg","description":"Use the replies_next_page_token from the comment item to get the initial replies. And use the same key from this result for pagination.","requestParams":{"engine":"youtube_video","next_page_token":"Eg0SC0VOaGZJZVpGX0FZGAYygwEaUBIaVWd3Z0RUbVFTRHBoM243THlyNTRBYUFCQWciAggAKhhVQ1hHUjcwQ2tXX3BYYjhuNTJMekNDUncyC0VOaGZJZVpGX0FZQAFICoIBAggBQi9jb21tZW50LXJlcGxpZXMtaXRlbS1VZ3dnRFRtUVNEcGgzbjdMeXI1NEFhQUJBZw%3D%3D"},"responseJson":"https://serpapi.com/search.json?engine=youtube_video&next_page_token=Eg0SC0VOaGZJZVpGX0FZGAYygwEaUBIaVWd3Z0RUbVFTRHBoM243THlyNTRBYUFCQWciAggAKhhVQ1hHUjcwQ2tXX3BYYjhuNTJMekNDUncyC0VOaGZJZVpGX0FZQAFICoIBAggBQi9jb21tZW50LXJlcGxpZXMtaXRlbS1VZ3dnRFRtUVNEcGgzbjdMeXI1NEFhQUJBZw%3D%3D"}
    - {"title":"Related videos with single video results and a playlist result (second page)","description":"","requestParams":{"engine":"youtube_video","next_page_token":"CBQSKRILdkZjUzA4MFZZUTDAAQDIAQDgAQGiAg0o____________AUAA-AIAGAAqjgYyczZMNnd6REJBckFCQW9EOGo0QUNnN0NQZ3NJeHVfRjdNbm41NHZJQVFvRDhqNEFDZzNDUGdvSWhidkx2ZTMxbWJVT0NnUHlQZ0FLRGNJLUNnal95WTJMck96bXoya0tBX0ktQUFvTndqNEtDT0xLc0t1andlZmtOd29EOGo0QUNnN0NQZ3NJeDhiQnVPem0xSUs5QVFvRDhqNEFDZzNDUGdvSTMtV0hzY0dZeC01TUNnUHlQZ0FLRHNJLUN3akk0ZHljd3VYNDA5WUJDZ1B5UGdBS0RzSS1Dd2pHMTlMbDBLR2wyNndCQ2dQeVBnQUtEY0ktQ2dpQTFOZkF1N2ZNdlJFS0FfSS1BQW9Od2o0S0NJMnoyNjdvNXBfbkZBb0Q4ajRBQ2czQ1Bnb0lfUHkyODh5cWt0QTNDZ1B5UGdBS0RzSS1Dd2o4a1A2NXVkbUk4Y0lCQ2dQeVBnQUtEc0ktQ3dpV2twM18wUC1FazdrQkNnUHlQZ0FLRHNJLUN3alcwY21Mcm83c2tKWUJDZ1B5UGdBS0RjSS1DZ2lyaHFHVnF1N0F5WG9LQV9JLUFBb093ajRMQ0phVGhxRGNzSUdseFFFS0FfSS1BQW9Pd2o0TENQVDk4Nnp0XzhhMGl3RUtBX0ktQUFvT3dqNExDTzJidXR6OWxhUEdwZ0VLQV9JLUFBb093ajRMQ09hSDdaM3RrS0g3MVFFS0FfSS1BQW9Pd2o0TENPV2l2TlA3bHBTdTZ3RVNGQUFDQkFZSUNnd09FQklVRmhnYUhCNGdJaVFtR2dRSUFCQUJHZ1FJQWhBREdnUUlCQkFGR2dRSUJoQUhHZ1FJQ0JBSkdnUUlDaEFMR2dRSURCQU5HZ1FJRGhBUEdnUUlFQkFSR2dRSUVoQVRHZ1FJRkJBVkdnUUlGaEFYR2dRSUdCQVpHZ1FJR2hBYkdnUUlIQkFkR2dRSUhoQWZHZ1FJSUJBaEdnUUlJaEFqR2dRSUpCQWxHZ1FJSmhBbktoUUFBZ1FHQ0FvTURoQVNGQllZR2h3ZUlDSWtKZ2oPd2F0Y2gtbmV4dC1mZWVk"},"responseJson":"https://serpapi.com/search.json?engine=youtube_video&next_page_token=CBQSKRILdkZjUzA4MFZZUTDAAQDIAQDgAQGiAg0o____________AUAA-AIAGAAqjgYyczZMNnd6REJBckFCQW9EOGo0QUNnN0NQZ3NJeHVfRjdNbm41NHZJQVFvRDhqNEFDZzNDUGdvSWhidkx2ZTMxbWJVT0NnUHlQZ0FLRGNJLUNnal95WTJMck96bXoya0tBX0ktQUFvTndqNEtDT0xLc0t1andlZmtOd29EOGo0QUNnN0NQZ3NJeDhiQnVPem0xSUs5QVFvRDhqNEFDZzNDUGdvSTMtV0hzY0dZeC01TUNnUHlQZ0FLRHNJLUN3akk0ZHljd3VYNDA5WUJDZ1B5UGdBS0RzSS1Dd2pHMTlMbDBLR2wyNndCQ2dQeVBnQUtEY0ktQ2dpQTFOZkF1N2ZNdlJFS0FfSS1BQW9Od2o0S0NJMnoyNjdvNXBfbkZBb0Q4ajRBQ2czQ1Bnb0lfUHkyODh5cWt0QTNDZ1B5UGdBS0RzSS1Dd2o4a1A2NXVkbUk4Y0lCQ2dQeVBnQUtEc0ktQ3dpV2twM18wUC1FazdrQkNnUHlQZ0FLRHNJLUN3alcwY21Mcm83c2tKWUJDZ1B5UGdBS0RjSS1DZ2lyaHFHVnF1N0F5WG9LQV9JLUFBb093ajRMQ0phVGhxRGNzSUdseFFFS0FfSS1BQW9Pd2o0TENQVDk4Nnp0XzhhMGl3RUtBX0ktQUFvT3dqNExDTzJidXR6OWxhUEdwZ0VLQV9JLUFBb093ajRMQ09hSDdaM3RrS0g3MVFFS0FfSS1BQW9Pd2o0TENPV2l2TlA3bHBTdTZ3RVNGQUFDQkFZSUNnd09FQklVRmhnYUhCNGdJaVFtR2dRSUFCQUJHZ1FJQWhBREdnUUlCQkFGR2dRSUJoQUhHZ1FJQ0JBSkdnUUlDaEFMR2dRSURCQU5HZ1FJRGhBUEdnUUlFQkFSR2dRSUVoQVRHZ1FJRkJBVkdnUUlGaEFYR2dRSUdCQVpHZ1FJR2hBYkdnUUlIQkFkR2dRSUhoQWZHZ1FJSUJBaEdnUUlJaEFqR2dRSUpCQWxHZ1FJSmhBbktoUUFBZ1FHQ0FvTURoQVNGQllZR2h3ZUlDSWtKZ2oPd2F0Y2gtbmV4dC1mZWVk"}
    - {"title":"Related videos with official_artist channels","description":"","requestParams":{"engine":"youtube_video","v":"yKNxeF4KMsY"},"responseJson":"https://serpapi.com/search.json?engine=youtube_video&v=yKNxeF4KMsY"}
    - {"title":"JSON structure overview","description":"","requestParams":{},"responseJson":"{\n  ...\n  \"title\": \"String - Title of the video\",\n  \"thumbnail\": \"String - URL of the video thumbnail\",\n  \"channel\": {\n    \"name\": \"String - Name of the channel\",\n    \"thumbnail\": \"String - URL of the channel thumbnail\",\n    \"link\": \"String - URL of the channel\",\n    \"subscribers\": \"String - Number of subscribers\",\n    \"verified\": \"Boolean - True if the channel is verified\",\n  },\n  \"views\": \"String - Number of views\",\n  \"extracted_views\": \"Integer - Extracted number of views\",\n  \"likes\": \"String - Number of likes\",\n  \"extracted_likes\": \"Integer - Extracted number of likes\",\n  \"live\": \"Boolean - True if the video is live\",\n  \"published_date\": \"String - Date of publication\",\n  \"description\": {\n    \"content\": \"String - Description of the video in pure text\",\n    \"links\": [\n      {\n        \"start_index\": \"Integer - Start index of the link text in the content\",\n        \"length\": \"Integer - Length of the link text\",\n        \"text\": \"String - The link text\",\n        \"url\": \"String - URL of the link\",\n        \"type\": \"String - Type of the link\",\n      }\n    ]\n  },\n  \"additional_info\": [\n    {\n      \"title\": \"String - Title of the info row\",\n      \"text\": \"String - Text of the info row\",\n      \"link\": \"String - URL associated with the text\",\n    },\n    ...\n  ],\n  \"shopping_results\": [\n    {\n      \"title\": \"String - Title of the product\",\n      \"description\": \"String - Description of the product\",\n      \"thumbnail\": \"String - URL of the product thumbnail\",\n      \"price\": \"String - Price of the product\",\n      \"extracted_price\": \"Float - Extracted price of the product\",\n      \"vendor\": \"String - Vendor of the product\",\n      \"link\": \"String - URL of the product\",\n    }\n  ],\n  \"chapters\": [\n    {\n      \"title\": \"String - Title of the chapter\",\n      \"thumbnail\": \"String - URL of the chapter thumbnail\",\n      \"time_start\": \"Integer - Time start of the chapter in seconds\",\n    }\n  ],\n  \"related_videos\": [\n    {\n      \"video_id\": \"String - ID of the video\",\n      \"playlist_id\": \"String - ID of the playlist if the result is a playlist\",\n      \"link\": \"String - URL of the video\",\n      \"serpapi_link\": \"String - URL to the SerpApi search\",\n      \"thumbnail\": {\n        \"static\": \"String - URL of the static video thumbnail\",\n        \"rich\": \"String - URL of the rich video thumbnail, usually in the form of a video containing the multiple screenshots\",\n      },\n      \"title\": \"String - Title of the video\",\n      \"published_date\": \"String - Date of publication\",\n      \"views\": \"String - Number of views\",\n      \"extracted_views\": \"Integer - Extracted number of views\",\n      \"live\": \"Boolean - True if the video is live\",\n      \"length\": \"String - Length of the video\",\n      \"channel\": {\n        \"name\": \"String - Name of the channel\",\n        \"link\": \"String - URL of the channel\",\n        \"thumbnail\": \"String - URL of the channel thumbnail\",\n        \"verified\": \"Boolean - True if the channel is verified\",\n        \"official_artist\": \"Boolean - True if the channel is an official artist channel\",\n      },\n      \"extensions\": \"Array - List of video badges\"\n    }\n  ],\n  \"related_videos_next_page_token\": \"String - Token to get the next page of related videos\",\n  \"end_screen_videos\": [\n    {\n      \"video_id\": \"String - ID of the video\",\n      \"link\": \"String - URL of the video\",\n      \"serpapi_link\": \"String - URL to the SerpApi search\",\n      \"thumbnail\": \"String - URL of the video thumbnail\",\n      \"title\": \"String - Title of the video\",\n      \"published_date\": \"String - Date of publication\",\n      \"views\": \"String - Number of views\",\n      \"extracted_views\": \"Integer - Extracted number of views\",\n      \"live\": \"Boolean - True if the video is live\",\n      \"length\": \"String - Length of the video\",\n      \"channel\": {\n        \"name\": \"String - Name of the channel\",\n        \"link\": \"String - URL of the channel\",\n      }\n    }\n  ],\n  // comments do not exist in the initial response, they must be retrieved with the `comments_next_page_token` or `comments_sorting_token`\n  \"comments\": [\n    {\n      \"comment_id\": \"String - ID of the comment\",\n      \"link\": \"String - URL of the comment\",\n      \"channel\": {\n        \"name\": \"String - Name of the channel\",\n        \"link\": \"String - URL of the channel\",\n        \"thumbnail\": \"String - URL of the channel thumbnail\",\n        \"verified\": \"Boolean - True if the channel is verified\",\n      },\n      \"published_date\": \"String - Date of publication\",\n      \"content\": \"String - Content of the comment\",\n      \"vote_count\": \"String - Number of votes\",\n      \"extracted_vote_count\": \"Integer - Extracted number of votes\",\n      \"reply_count\": \"Integer - Number of replies\",\n      \"replies_next_page_token\": \"String - Token to get the next page of replies\",\n    }\n  ],\n  \"comment_count\": \"String - Number of comments\",\n  \"extracted_comment_count\": \"Integer - Extracted number of comments\",\n  \"comments_next_page_token\": \"String - Token to get the next page of comments\",\n  \"comments_sorting_token\": [\n    {\n      \"title\": \"String - Title of the sorting option\",\n      \"token\": \"String - Token to sort the comments\",\n    }\n  ],\n  \"comment_parent_id\": \"String - The parent comment ID of the replies\",\n  // replies do not exist in the initial response, they must be retrieved with the `replies_next_page_token`\n  \"replies\": [\n    // the same structure as comments\n  ],\n  \"replies_next_page_token\": \"String - Token to get the next page of replies\",\n  \"transcript\": {\n    \"serpapi_link\": \"String - URL to the SerpApi Youtube Video Transcript API\",\n  },\n  ...\n}"}
  importantNotes: []
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "youtube-video-api-api"
---

# YouTube Video API

## 源URL

https://serpapi.com/youtube-video-api

## 描述

Youtube Video API allows you to scrape video details from Youtube. Video details such as description, view count, related videos, comments, replies, and many others.

The API endpoint is https://serpapi.com/search?engine=youtube_video Head to the playground for a live and interactive demo.

To further get comments, use the comments_next_page_token or comments_sorting_token.token from this result.To paginate related videos, use the related_videos_next_page_token from this result.

Use the comments_next_page_token from the video result to get the initial comments. And use the same key from this result for pagination.To further get replies of a comment, use the replies_next_page_token from the comment.

Use the replies_next_page_token from the comment item to get the initial replies. And use the same key from this result for pagination.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Youtube Video API allows you to scrape video details from Youtube. Video details such as description, view count, related videos, comments, replies, and many others.

The API endpoint is https://serpapi.com/search?engine=youtube_video Head to the playground for a live and interactive demo.

To further get comments, use the comments_next_page_token or comments_sorting_token.token from this result.To paginate related videos, use the related_videos_next_page_token from this result.

Use the comments_next_page_token from the video result to get the initial comments. And use the same key from this result for pagination.To further get replies of a comment, use the replies_next_page_token from the comment.

Use the replies_next_page_token from the comment item to get the initial replies. And use the same key from this result for pagination.

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
