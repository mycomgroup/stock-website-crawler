---
id: "url-61c8a899"
type: "api"
title: "Brave Search - API"
url: "https://api-dashboard.search.brave.com/api-reference/web/search/get"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T02:30:59.134Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/web/search?q=brave+search"
  method: "GET"
  sections: []
  tables:
    - {"index":0,"headers":["Cookie Enabled","Cookie Key","Cookie Value"],"rows":[["","Key","Value"]]}
    - {"index":1,"headers":["Header Enabled","Header Key","Header Value"],"rows":[["","x-loc-lat","37.787"],["","x-loc-long","-122.4"],["","x-loc-timezone","America/San_Francisco"],["","x-loc-city","San Francisco"],["","x-loc-state","CA"],["","x-loc-state-name","California"],["","x-loc-country","US"],["","x-loc-postal-code","94105"],["","x-subscription-token Required","Value"],["","api-version","Value"],["","accept","application/json"],["","cache-control","Value"],["","user-agent","Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36"],["","Key","Value"]]}
    - {"index":2,"headers":["Parameter Enabled","Parameter Key","Parameter Value"],"rows":[["","q Required","Value"],["","country","US"],["","search_lang","en"],["","ui_lang","en-US"],["","count","20"],["","offset","0"],["","safesearch","Select a value"],["","spellcheck","true"],["","freshness","Select a value"],["","text_decorations","true"],["","result_filter","Select a value"],["","units","Select a value"],["","goggles_id","Select a value"],["","goggles","Select a value"],["","extra_snippets","Select a value"],["","summary","Select a value"],["","enable_rich_callback","false"],["","include_fetch_metadata","false"],["","operators","true"],["","Key","Value"]]}
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=brave+search\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=brave+search\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\""}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"search\",\n  \"query\": {\n    \"original\": \"string\",\n    \"show_strict_warning\": true,\n    \"altered\": \"string\",\n    \"cleaned\": \"string\",\n    \"safesearch\": true,\n    \"is_navigational\": true,\n    \"is_geolocal\": true,\n    \"local_decision\": \"string\",\n    \"local_locations_idx\": 1,\n    \"is_trending\": true,\n    \"is_news_breaking\": true,\n    \"ask_for_location\": true,\n    \"language\": {\n      \"main\": \"string\"\n    },\n    \"spellcheck_off\": true,\n    \"country\": \"string\",\n    \"bad_results\": true,\n    \"should_fallback\": true,\n    \"lat\": \"string\",\n    \"long\": \"string\",\n    \"postal_code\": \"string\",\n    \"city\": \"string\",\n    \"header_country\": \"string\",\n    \"more_results_available\": true,\n    \"state\": \"string\",\n    \"custom_location_label\": \"string\",\n    \"reddit_cluster\": \"string\",\n    \"summary_key\": \"string\",\n    \"search_operators\": {\n      \"applied\": false,\n      \"cleaned_query\": \"string\",\n      \"sites\": [\n        \"string\"\n      ]\n    }\n  },\n  \"discussions\": {\n    \"type\": \"search\",\n    \"results\": [\n      {\n        \"title\": \"string\",\n        \"url\": \"string\",\n        \"is_source_local\": false,\n        \"is_source_both\": false,\n        \"description\": \"\",\n        \"page_age\": \"string\",\n        \"page_fetched\": \"string\",\n        \"fetched_content_timestamp\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"language\": \"en\",\n        \"...\": \"[Additional Properties Truncated]\"\n      }\n    ],\n    \"mutated_by_goggles\": false\n  },\n  \"faq\": {\n    \"type\": \"faq\",\n    \"results\": [\n      {\n        \"question\": \"string\",\n        \"answer\": \"string\",\n        \"title\": \"string\",\n        \"url\": \"string\",\n        \"meta_url\": {\n          \"scheme\": \"string\",\n          \"netloc\": \"string\",\n          \"hostname\": \"string\",\n          \"favicon\": \"string\",\n          \"path\": \"string\"\n        }\n      }\n    ]\n  },\n  \"infobox\": {\n    \"type\": \"graph\",\n    \"results\": [\n      {\n        \"title\": \"string\",\n        \"url\": \"string\",\n        \"is_source_local\": false,\n        \"is_source_both\": false,\n        \"description\": \"\",\n        \"page_age\": \"string\",\n        \"page_fetched\": \"string\",\n        \"fetched_content_timestamp\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"language\": \"string\",\n        \"...\": \"[Additional Properties Truncated]\"\n      }\n    ]\n  },\n  \"locations\": {\n    \"type\": \"locations\",\n    \"results\": [\n      {\n        \"title\": \"string\",\n        \"url\": \"string\",\n        \"is_source_local\": false,\n        \"is_source_both\": false,\n        \"description\": \"\",\n        \"page_age\": \"string\",\n        \"page_fetched\": \"string\",\n        \"fetched_content_timestamp\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"language\": \"string\",\n        \"...\": \"[Additional Properties Truncated]\"\n      }\n    ],\n    \"provider\": {}\n  },\n  \"mixed\": {\n    \"type\": \"mixed\",\n    \"main\": [\n      {\n        \"type\": \"string\",\n        \"index\": 1,\n        \"all\": false\n      }\n    ],\n    \"top\": [\n      {\n        \"type\": \"string\",\n        \"index\": 1,\n        \"all\": false\n      }\n    ],\n    \"side\": [\n      {\n        \"type\": \"string\",\n        \"index\": 1,\n        \"all\": false\n      }\n    ]\n  },\n  \"news\": {\n    \"type\": \"news\",\n    \"results\": [\n      {\n        \"title\": \"string\",\n        \"url\": \"string\",\n        \"is_source_local\": false,\n        \"is_source_both\": false,\n        \"description\": \"\",\n        \"page_age\": \"string\",\n        \"page_fetched\": \"string\",\n        \"fetched_content_timestamp\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"language\": \"string\",\n        \"...\": \"[Additional Properties Truncated]\"\n      }\n    ],\n    \"mutated_by_goggles\": false\n  },\n  \"videos\": {\n    \"type\": \"videos\",\n    \"results\": [\n      {\n        \"type\": \"video_result\",\n        \"url\": \"string\",\n        \"title\": \"string\",\n        \"description\": \"string\",\n        \"age\": \"string\",\n        \"page_age\": \"string\",\n        \"page_fetched\": \"string\",\n        \"fetched_content_timestamp\": 1,\n        \"video\": {\n          \"duration\": \"string\",\n          \"views\": 1,\n          \"creator\": \"string\",\n          \"publisher\": \"string\",\n          \"requires_subscription\": true,\n          \"tags\": [\n            \"string\"\n          ],\n          \"author\": {\n            \"name\": \"string\",\n            \"url\": \"string\",\n            \"long_name\": \"string\",\n            \"img\": \"string\"\n          }\n        },\n        \"meta_url\": {\n          \"scheme\": \"string\",\n          \"netloc\": \"string\",\n          \"hostname\": \"string\",\n          \"favicon\": \"string\",\n          \"path\": \"string\"\n        },\n        \"...\": \"[Additional Properties Truncated]\"\n      }\n    ],\n    \"mutated_by_goggles\": false\n  },\n  \"web\": {\n    \"type\": \"search\",\n    \"results\": [\n      {\n        \"title\": \"string\",\n        \"url\": \"string\",\n        \"is_source_local\": false,\n        \"is_source_both\": false,\n        \"description\": \"\",\n        \"page_age\": \"string\",\n        \"page_fetched\": \"string\",\n        \"fetched_content_timestamp\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"language\": \"en\",\n        \"...\": \"[Additional Properties Truncated]\"\n      }\n    ],\n    \"family_friendly\": true\n  },\n  \"summarizer\": {\n    \"type\": \"summarizer\",\n    \"key\": \"string\"\n  },\n  \"rich\": {\n    \"type\": \"rich\",\n    \"hint\": {\n      \"vertical\": \"calculator\",\n      \"callback_key\": \"string\"\n    }\n  }\n}"}
    - {"type":"response","language":"json","code":"{\n  \"type\": \"search\",\n  \"query\": {\n    \"original\": \"string\",\n    \"show_strict_warning\": true,\n    \"altered\": \"string\",\n    \"cleaned\": \"string\",\n    \"safesearch\": true,\n    \"is_navigational\": true,\n    \"is_geolocal\": true,\n    \"local_decision\": \"string\",\n    \"local_locations_idx\": 1,\n    \"is_trending\": true,\n    \"is_news_breaking\": true,\n    \"ask_for_location\": true,\n    \"language\": {\n      \"main\": \"string\"\n    },\n    \"spellcheck_off\": true,\n    \"country\": \"string\",\n    \"bad_results\": true,\n    \"should_fallback\": true,\n    \"lat\": \"string\",\n    \"long\": \"string\",\n    \"postal_code\": \"string\",\n    \"city\": \"string\",\n    \"header_country\": \"string\",\n    \"more_results_available\": true,\n    \"state\": \"string\",\n    \"custom_location_label\": \"string\",\n    \"reddit_cluster\": \"string\",\n    \"summary_key\": \"string\",\n    \"search_operators\": {\n      \"applied\": false,\n      \"cleaned_query\": \"string\",\n      \"sites\": [\n        \"string\"\n      ]\n    }\n  },\n  \"discussions\": {\n    \"type\": \"search\",\n    \"results\": [\n      {\n        \"title\": \"string\",\n        \"url\": \"string\",\n        \"is_source_local\": false,\n        \"is_source_both\": false,\n        \"description\": \"\",\n        \"page_age\": \"string\",\n        \"page_fetched\": \"string\",\n        \"fetched_content_timestamp\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"language\": \"en\",\n        \"...\": \"[Additional Properties Truncated]\"\n      }\n    ],\n    \"mutated_by_goggles\": false\n  },\n  \"faq\": {\n    \"type\": \"faq\",\n    \"results\": [\n      {\n        \"question\": \"string\",\n        \"answer\": \"string\",\n        \"title\": \"string\",\n        \"url\": \"string\",\n        \"meta_url\": {\n          \"scheme\": \"string\",\n          \"netloc\": \"string\",\n          \"hostname\": \"string\",\n          \"favicon\": \"string\",\n          \"path\": \"string\"\n        }\n      }\n    ]\n  },\n  \"infobox\": {\n    \"type\": \"graph\",\n    \"results\": [\n      {\n        \"title\": \"string\",\n        \"url\": \"string\",\n        \"is_source_local\": false,\n        \"is_source_both\": false,\n        \"description\": \"\",\n        \"page_age\": \"string\",\n        \"page_fetched\": \"string\",\n        \"fetched_content_timestamp\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"language\": \"string\",\n        \"...\": \"[Additional Properties Truncated]\"\n      }\n    ]\n  },\n  \"locations\": {\n    \"type\": \"locations\",\n    \"results\": [\n      {\n        \"title\": \"string\",\n        \"url\": \"string\",\n        \"is_source_local\": false,\n        \"is_source_both\": false,\n        \"description\": \"\",\n        \"page_age\": \"string\",\n        \"page_fetched\": \"string\",\n        \"fetched_content_timestamp\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"language\": \"string\",\n        \"...\": \"[Additional Properties Truncated]\"\n      }\n    ],\n    \"provider\": {}\n  },\n  \"mixed\": {\n    \"type\": \"mixed\",\n    \"main\": [\n      {\n        \"type\": \"string\",\n        \"index\": 1,\n        \"all\": false\n      }\n    ],\n    \"top\": [\n      {\n        \"type\": \"string\",\n        \"index\": 1,\n        \"all\": false\n      }\n    ],\n    \"side\": [\n      {\n        \"type\": \"string\",\n        \"index\": 1,\n        \"all\": false\n      }\n    ]\n  },\n  \"news\": {\n    \"type\": \"news\",\n    \"results\": [\n      {\n        \"title\": \"string\",\n        \"url\": \"string\",\n        \"is_source_local\": false,\n        \"is_source_both\": false,\n        \"description\": \"\",\n        \"page_age\": \"string\",\n        \"page_fetched\": \"string\",\n        \"fetched_content_timestamp\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"language\": \"string\",\n        \"...\": \"[Additional Properties Truncated]\"\n      }\n    ],\n    \"mutated_by_goggles\": false\n  },\n  \"videos\": {\n    \"type\": \"videos\",\n    \"results\": [\n      {\n        \"type\": \"video_result\",\n        \"url\": \"string\",\n        \"title\": \"string\",\n        \"description\": \"string\",\n        \"age\": \"string\",\n        \"page_age\": \"string\",\n        \"page_fetched\": \"string\",\n        \"fetched_content_timestamp\": 1,\n        \"video\": {\n          \"duration\": \"string\",\n          \"views\": 1,\n          \"creator\": \"string\",\n          \"publisher\": \"string\",\n          \"requires_subscription\": true,\n          \"tags\": [\n            \"string\"\n          ],\n          \"author\": {\n            \"name\": \"string\",\n            \"url\": \"string\",\n            \"long_name\": \"string\",\n            \"img\": \"string\"\n          }\n        },\n        \"meta_url\": {\n          \"scheme\": \"string\",\n          \"netloc\": \"string\",\n          \"hostname\": \"string\",\n          \"favicon\": \"string\",\n          \"path\": \"string\"\n        },\n        \"...\": \"[Additional Properties Truncated]\"\n      }\n    ],\n    \"mutated_by_goggles\": false\n  },\n  \"web\": {\n    \"type\": \"search\",\n    \"results\": [\n      {\n        \"title\": \"string\",\n        \"url\": \"string\",\n        \"is_source_local\": false,\n        \"is_source_both\": false,\n        \"description\": \"\",\n        \"page_age\": \"string\",\n        \"page_fetched\": \"string\",\n        \"fetched_content_timestamp\": 1,\n        \"profile\": {\n          \"name\": \"string\",\n          \"url\": \"string\",\n          \"long_name\": \"string\",\n          \"img\": \"string\"\n        },\n        \"language\": \"en\",\n        \"...\": \"[Additional Properties Truncated]\"\n      }\n    ],\n    \"family_friendly\": true\n  },\n  \"summarizer\": {\n    \"type\": \"summarizer\",\n    \"key\": \"string\"\n  },\n  \"rich\": {\n    \"type\": \"rich\",\n    \"hint\": {\n      \"vertical\": \"calculator\",\n      \"callback_key\": \"string\"\n    }\n  }\n}"}
  rawContent: "Search GET\n\nSearch POST\n\nLocal POIs GET\n\nPOI Descriptions GET\n\nRich search GET\n\nLLM Context GET\n\nLLM Context POST\n\nPlace Search GET\n\nNews GET\n\nNews POST\n\nVideos GET\n\nVideos POST\n\nImages GET\n\nAnswers POST\n\nSuggest GET\n\nSpell check GET\n\nSearch\n\nSearch the web from a large independent index of web pages.\n\nget/v1/web/search\n\nqCopy link to qType: Querymin length:    1max length:    400 required \nThe user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.\n\nThe user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.\n\ncountryCopy link to countryType: SearchCountryenum\nThe 2 character country code where the search results come from. The default value is US.\nARAUATBEBR Show all values\n\nThe 2 character country code where the search results come from. The default value is US.\n\nShow all values\n\nsearch_langCopy link to search_langType: Languageenum\nThe 2 or more character language code for which the search results are provided.\nareubnbgca Show all values\n\nThe 2 or more character language code for which the search results are provided.\n\nui_langCopy link to ui_langType: MarketCodesenum\nUser interface language preferred in response. Usually of the format <language_code>-<country_code>. For more, see RFC 9110.\nes-ARen-AUde-ATnl-BEfr-BE Show all values\n\nUser interface language preferred in response. Usually of the format <language_code>-<country_code>. For more, see RFC 9110.\n\ncountCopy link to countType: Countmin:    1max:    20default:  20\n\n  The number of search results returned in response.\n  The maximum is 20. The actual number delivered may be less than requested.\n  Combine this parameter with offset to paginate search results.\n\n\nNOTE: Count only applies to web results.\n\nThe number of search results returned in response.\n  The maximum is 20. The actual number delivered may be less than requested.\n  Combine this parameter with offset to paginate search results.\n\nNOTE: Count only applies to web results.\n\noffsetCopy link to offsetType: Offsetmin:    0max:    9default:  0\n\n  The zero based offset that indicates number of search\n  result pages (count) to skip before returning the result.\n  The default is 0 and the maximum is 9.\n  The actual number delivered may be less than requested.\n\n\n\n  Use this parameter along with the count parameter to page results.\n  For example, if your user interface displays 10 search results per page,\n  set count to 10 and offset to 0 to get the first page of results.\n  For each subsequent page, increment offset by 1 (for example, 0, 1, 2).\n  It is possible for multiple pages to include some overlap in results.\n\nThe zero based offset that indicates number of search\n  result pages (count) to skip before returning the result.\n  The default is 0 and the maximum is 9.\n  The actual number delivered may be less than requested.\n\nUse this parameter along with the count parameter to page results.\n  For example, if your user interface displays 10 search results per page,\n  set count to 10 and offset to 0 to get the first page of results.\n  For each subsequent page, increment offset by 1 (for example, 0, 1, 2).\n  It is possible for multiple pages to include some overlap in results.\n\nsafesearchCopy link to safesearchType: SafeSearchenum\nFilters search results for adult content. The following values are supported:\n\n\n  off - No filtering is done.\n  moderate - Filters explicit content, like images and videos, but allows adult domains in the search results.\n  strict - Drops all adult content from search results.\n\nDefaults to moderate.\noffmoderatestrict\n\nFilters search results for adult content. The following values are supported:\n\noff - No filtering is done.\n\nmoderate - Filters explicit content, like images and videos, but allows adult domains in the search results.\n\nstrict - Drops all adult content from search results.\n\nDefaults to moderate.\n\nmoderate\n\nstrict\n\nspellcheckCopy link to spellcheckType: Spellcheckdefault:  trueExamplestruefalse\nWhether to spell check provided query. If the spell checker is enabled, the modified query is always used for search. The modified query can be found in altered key from the query response model.\n\nWhether to spell check provided query. If the spell checker is enabled, the modified query is always used for search. The modified query can be found in altered key from the query response model.\n\nfreshnessCopy link to freshnessType: Freshnessdefault:  \"\"Examplespm2022-04-01to2022-07-30\nFilters search results by page age. The age of a page is determined by the most relevant date reported by the content, such as its published or last modified date. The following values are supported:\n\n  pd - Pages aged 24 hours or less.\n  pw - Pages aged 7 days or less.\n  pm - Pages aged 31 days or less.\n  py - Pages aged 365 days or less.\n  YYYY-MM-DDtoYYYY-MM-DD - A custom date range is also supported by specifying start and end dates e.g. 2022-04-01to2022-07-30.\n\nFilters search results by page age. The age of a page is determined by the most relevant date reported by the content, such as its published or last modified date. The following values are supported:\n\npd - Pages aged 24 hours or less.\n\npw - Pages aged 7 days or less.\n\npm - Pages aged 31 days or less.\n\npy - Pages aged 365 days or less.\n\nYYYY-MM-DDtoYYYY-MM-DD - A custom date range is also supported by specifying start and end dates e.g. 2022-04-01to2022-07-30.\n\ntext_decorationsCopy link to text_decorationsType: Text decorationsdefault:  trueExamplestruefalse\nWhether display strings (e.g. result snippets) should include decoration markers (e.g. highlighting characters).\n\nWhether display strings (e.g. result snippets) should include decoration markers (e.g. highlighting characters).\n\nresult_filterCopy link to result_filterType: array Result filter[] unique! nullable Exampleswebvideosweb,videos\n\n  A comma delimited string of result types to include in the search response.\n  Not specifying this parameter will return back all result types in search response where data is available\n  and a plan with the corresponding option is subscribed. The response always includes query and type to\n  identify any query modifications and response type respectively.\n  Available result filter values are: discussions, faq, infobox, news, query, summarizer, videos, web, locations.\n\n\nNOTE: count param only applies to web results.\n\nA comma delimited string of result types to include in the search response.\n  Not specifying this parameter will return back all result types in search response where data is available\n  and a plan with the corresponding option is subscribed. The response always includes query and type to\n  identify any query modifications and response type respectively.\n  Available result filter values are: discussions, faq, infobox, news, query, summarizer, videos, web, locations.\n\nNOTE: count param only applies to web results.\n\nunitsCopy link to unitsType: MeasurementUnitenum nullable Examplesmetricimperial\nThe measurement units. The following values are supported:\n\n  metric - The standardized measurement system (km, celcius…)\n  imperial - The British Imperial system of units (mile, fahrenheit…)\n\nimperialmetric\n\nThe measurement units. The following values are supported:\n\nmetric - The standardized measurement system (km, celcius…)\n\nimperial - The British Imperial system of units (mile, fahrenheit…)\n\nimperial\n\nmetric\n\ngoggles_idCopy link to goggles_idType: Goggles iddeprecated nullable Exampleshttps://raw.githubusercontent.com/brave/goggles-quickstart/main/goggles/hacker_news.goggle\nGoggles act as a custom re-ranking on top of Brave’s search index. For more details, refer to the Goggles repository. This parameter is deprecated. Please use the goggles parameter.\n\nGoggles act as a custom re-ranking on top of Brave’s search index. For more details, refer to the Goggles repository. This parameter is deprecated. Please use the goggles parameter.\n\ngogglesCopy link to goggles nullable \nGoggles act as a custom re-ranking on top of Brave’s search index. The parameter supports both a url where the Goggle is hosted or the definition of the goggle. For more details, see the Goggles documentation. The parameter can be repeated to query with multiple goggles.\nAny ofstringType: string\n\nGoggles act as a custom re-ranking on top of Brave’s search index. The parameter supports both a url where the Goggle is hosted or the definition of the goggle. For more details, see the Goggles documentation. The parameter can be repeated to query with multiple goggles.\n\nType: string\n\nextra_snippetsCopy link to extra_snippetsType: Extra snippets nullable Examplestruefalse\nA snippet is an excerpt from a page you get as a result of the query, and extra_snippets allow you to get up to 5 additional, alternative excerpts.\n\nA snippet is an excerpt from a page you get as a result of the query, and extra_snippets allow you to get up to 5 additional, alternative excerpts.\n\nsummaryCopy link to summaryType: Summary nullable Examplestruefalse\nThis parameter enables summary key generation in web search results. This is required for summarizer to be enabled.\n\nThis parameter enables summary key generation in web search results. This is required for summarizer to be enabled.\n\nenable_rich_callbackCopy link to enable_rich_callbackType: Enable Rich Callbackdefault:  falseExamplesfalsetrue\n\n  Enable rich callback.\n  Allows you to get real time rich results via a callback URL when they are relevant to your query.\n\n\nNOTE: Requires Search subscription.\n\nEnable rich callback.\n  Allows you to get real time rich results via a callback URL when they are relevant to your query.\n\nNOTE: Requires Search subscription.\n\ninclude_fetch_metadataCopy link to include_fetch_metadataType: Include Fetch Metadatadefault:  falseExamplesfalsetrue\nInclude fetch metadata. Defaults to false.\n\nInclude fetch metadata. Defaults to false.\n\noperatorsCopy link to operatorsType: Operatorsdefault:  trueExamplestruefalse\nWhether to apply search operators\n\nWhether to apply search operators\n\nx-loc-latCopy link to x-loc-latType: Latitudemin:    -90max:    90 nullable Example37.787\nThe latitude of the client’s geographical location in degrees, to provide relevant local results. The latitude must be greater than or equal to -90.0 degrees and less than or equal to +90.0 degrees.\n\nThe latitude of the client’s geographical location in degrees, to provide relevant local results. The latitude must be greater than or equal to -90.0 degrees and less than or equal to +90.0 degrees.\n\nx-loc-longCopy link to x-loc-longType: Longitudemin:    -180max:    180 nullable Example-122.4\nThe longitude of the client’s geographical location in degrees, to provide relevant local results. The longitude must be greater than or equal to -180.0 and less than or equal to +180.0 degrees.\n\nThe longitude of the client’s geographical location in degrees, to provide relevant local results. The longitude must be greater than or equal to -180.0 and less than or equal to +180.0 degrees.\n\nx-loc-timezoneCopy link to x-loc-timezoneType: IANA timezone nullable ExampleAmerica/San_Francisco\nThe IANA timezone for the client’s device. For complete list of IANA timezones and location mappings see IANA Database and Geonames Database.\n\nThe IANA timezone for the client’s device. For complete list of IANA timezones and location mappings see IANA Database and Geonames Database.\n\nx-loc-cityCopy link to x-loc-cityType: City nullable ExampleSan Francisco\nThe generic name of the client city.\n\nThe generic name of the client city.\n\nx-loc-stateCopy link to x-loc-stateType: State/Region code nullable ExampleCA\nA code which could be up to three characters, that represent the client’s state/region. The region is the first-level subdivision (the broadest or least specific) of the ISO 3166-2 code.\n\nA code which could be up to three characters, that represent the client’s state/region. The region is the first-level subdivision (the broadest or least specific) of the ISO 3166-2 code.\n\nx-loc-state-nameCopy link to x-loc-state-nameType: State/Region name nullable ExampleCalifornia\nThe name of the client’s state/region. The region is the first-level subdivision (the broadest or least specific) of the ISO 3166-2 code.\n\nThe name of the client’s state/region. The region is the first-level subdivision (the broadest or least specific) of the ISO 3166-2 code.\n\nx-loc-countryCopy link to x-loc-countryType: Countryenum nullable ExampleUS\n\n  The two letter country code for the client’s country.\n  For a list of country codes, see ISO 3166-1 alpha-2.\n\nADAEAFAGAI Show all values\n\nThe two letter country code for the client’s country.\n  For a list of country codes, see ISO 3166-1 alpha-2.\n\nx-loc-postal-codeCopy link to x-loc-postal-codeType: Postal code nullable Example94105\nThe client’s postal code.\n\nThe client’s postal code.\n\nx-subscription-tokenCopy link to x-subscription-tokenType: Subscription token required \nThe subscription token that was generated for the product.\n\nThe subscription token that was generated for the product.\n\napi-versionCopy link to api-versionType: API version nullable \nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nThe API version to use. This is denoted by the format YYYY-MM-DD. Default is the latest that is available. Read more about API versioning.\n\nacceptCopy link to acceptType: Acceptenum\nThe default supported media type is application/json.\napplication/json*/*\n\nThe default supported media type is application/json.\n\napplication/json\n\ncache-controlCopy link to cache-controlenumconst:   no-cache\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\nno-cache\n\nBrave Search will return cached content by default. To prevent caching set the Cache-Control header to no-cache. This is currently done as best effort.\n\nno-cache\n\nuser-agentCopy link to user-agentType: User agent nullable ExamplesMozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/103.0.5060.63 Mobile/15E148 Safari/604.1Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\nThe user agent originating the request. Brave search can utilize the user agent to provide a different experience depending on the device as described by the string. The user agent should follow the commonly used browser agent strings on each platform. For more information on curating user agents, see RFC 9110.\n\n200Copy link to 200Type: WebSearchApiResponsediscussionsType: Discussions nullable \nA model representing a discussion cluster relevant to the query.\n Show Discussionsfor discussionsfaqType: FAQ nullable \nFrequently asked questions relevant to the search query term.\n Show FAQfor faqinfoboxType: GraphInfobox nullable \nAggregated information on an entity shown as an infobox.\n Show GraphInfoboxfor infoboxlocationsType: Locations nullable \nA model representing location results.\n Show Locationsfor locationsmixedType: MixedResponse nullable \nThe ranking order of results on a search result page.\n Show MixedResponsefor mixednewsType: News nullable \nNews results relevant to the query.\n Show Newsfor newsqueryType: Query nullable \nSearch query string and its modifications that are used for search.\n Show Queryfor queryrichType: RichHeaderCallback nullable \nCallback information to retrieve rich results.\n Show RichHeaderCallbackfor richsummarizerType: Summarizer nullable \nSummary key to get summary results for the query.\n Show Summarizerfor summarizertypeenumdefault:  \"search\"const:   searchsearchvideosType: Videos nullable \nVideos results relevant to the query.\n Show Videosfor videoswebType: Search nullable \nA model representing a collection of web search results.\n Show Searchfor web\n\ndiscussionsType: Discussions nullable \nA model representing a discussion cluster relevant to the query.\n Show Discussionsfor discussions\n\nA model representing a discussion cluster relevant to the query.\n\nfaqType: FAQ nullable \nFrequently asked questions relevant to the search query term.\n Show FAQfor faq\n\nFrequently asked questions relevant to the search query term.\n\ninfoboxType: GraphInfobox nullable \nAggregated information on an entity shown as an infobox.\n Show GraphInfoboxfor infobox\n\nAggregated information on an entity shown as an infobox.\n\nlocationsType: Locations nullable \nA model representing location results.\n Show Locationsfor locations\n\nA model representing location results.\n\nmixedType: MixedResponse nullable \nThe ranking order of results on a search result page.\n Show MixedResponsefor mixed\n\nThe ranking order of results on a search result page.\n\nnewsType: News nullable \nNews results relevant to the query.\n Show Newsfor news\n\nNews results relevant to the query.\n\nqueryType: Query nullable \nSearch query string and its modifications that are used for search.\n Show Queryfor query\n\nSearch query string and its modifications that are used for search.\n\nrichType: RichHeaderCallback nullable \nCallback information to retrieve rich results.\n Show RichHeaderCallbackfor rich\n\nCallback information to retrieve rich results.\n\nsummarizerType: Summarizer nullable \nSummary key to get summary results for the query.\n Show Summarizerfor summarizer\n\nSummary key to get summary results for the query.\n\ntypeenumdefault:  \"search\"const:   searchsearch\n\nsearch\n\nvideosType: Videos nullable \nVideos results relevant to the query.\n Show Videosfor videos\n\nVideos results relevant to the query.\n\nwebType: Search nullable \nA model representing a collection of web search results.\n Show Searchfor web\n\nA model representing a collection of web search results.\n\n404Copy link to 404Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_NOT_FOUND\",\n      \"detail\": \"No subscription found.\",\n      \"status\": 404,\n      \"meta\": {\n        \"component\": \"subscriptions\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nerrorType: APIErrorModel required  Show APIErrorModelfor error\n\ntimeType: Timedefault:  0\nInteger numbers.\n\nInteger numbers.\n\ntypeType: Typedefault:  \"ErrorResponse\"\n\n422Copy link to 422Type: APIErrorResponseExample{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"SUBSCRIPTION_TOKEN_INVALID\",\n      \"detail\": \"The provided subscription token is invalid.\",\n      \"status\": 422,\n      \"meta\": {\n        \"component\": \"authentication\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\n429Copy link to 429Type: APIErrorResponseExamples{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"RATE_LIMITED\",\n      \"detail\": \"Request rate limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}{\n  \"type\": \"ErrorResponse\",\n  \"errors\": [\n    {\n      \"id\": \"5d832250-9396-4f6e-b84a-2a1fe524cd7d\",\n      \"code\": \"QUOTA_LIMITED\",\n      \"detail\": \"Request quota limit exceeded for plan.\",\n      \"status\": 429,\n      \"meta\": {\n        \"component\": \"rate_limiter\"\n      }\n    }\n  ],\n  \"time\": 1663072993\n}errorType: APIErrorModel required  Show APIErrorModelfor errortimeType: Timedefault:  0\nInteger numbers.\ntypeType: Typedefault:  \"ErrorResponse\"\n\nSuccessful Response\n\nPath Parameters\n\nCookies\n\nHeaders\n\nQuery Parameters\n\nCode Snippet (Collapsed)\n\nServer Server:https://api.search.brave.com/res\n\nSearch Operations get/v1/web/search\n\nRequest Example for get/v1/web/searchcURL curl \"https://api.search.brave.com/res/v1/web/search?q=brave+search\" \\\n  -H \"Accept: application/json\" \\ \n  -H \"Accept-Encoding: gzip\" \\ \n  -H \"X-Subscription-Token: <YOUR_API_KEY>\"\nTest Request(get /v1/web/search)\n\nStatus: 200Status: 404Status: 422Status: 429 Show Schema"
  suggestedFilename: "search-get"
---

# Brave Search - API

## 源URL

https://api-dashboard.search.brave.com/api-reference/web/search/get

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/web/search?q=brave+search`

## 代码示例

### 示例 1 (bash)

```bash
curl "https://api.search.brave.com/res/v1/web/search?q=brave+search" \
  -H "Accept: application/json" \ 
  -H "Accept-Encoding: gzip" \ 
  -H "X-Subscription-Token: <YOUR_API_KEY>"
```

### 示例 2 (json)

```json
{
  "type": "search",
  "query": {
    "original": "string",
    "show_strict_warning": true,
    "altered": "string",
    "cleaned": "string",
    "safesearch": true,
    "is_navigational": true,
    "is_geolocal": true,
    "local_decision": "string",
    "local_locations_idx": 1,
    "is_trending": true,
    "is_news_breaking": true,
    "ask_for_location": true,
    "language": {
      "main": "string"
    },
    "spellcheck_off": true,
    "country": "string",
    "bad_results": true,
    "should_fallback": true,
    "lat": "string",
    "long": "string",
    "postal_code": "string",
    "city": "string",
    "header_country": "string",
    "more_results_available": true,
    "state": "string",
    "custom_location_label": "string",
    "reddit_cluster": "string",
    "summary_key": "string",
    "search_operators": {
      "applied": false,
      "cleaned_query": "string",
      "sites": [
        "string"
      ]
    }
  },
  "discussions": {
    "type": "search",
    "results": [
      {
        "title": "string",
        "url": "string",
        "is_source_local": false,
        "is_source_both": false,
        "description": "",
        "page_age": "string",
        "page_fetched": "string",
        "fetched_content_timestamp": 1,
        "profile": {
          "name": "string",
          "url": "string",
          "long_name": "string",
          "img": "string"
        },
        "language": "en",
        "...": "[Additional Properties Truncated]"
      }
    ],
    "mutated_by_goggles": false
  },
  "faq": {
    "type": "faq",
    "results": [
      {
        "question": "string",
        "answer": "string",
        "title": "string",
        "url": "string",
        "meta_url": {
          "scheme": "string",
          "netloc": "string",
          "hostname": "string",
          "favicon": "string",
          "path": "string"
        }
      }
    ]
  },
  "infobox": {
    "type": "graph",
    "results": [
      {
        "title": "string",
        "url": "string",
        "is_source_local": false,
        "is_source_both": false,
        "description": "",
        "page_age": "string",
        "page_fetched": "string",
        "fetched_content_timestamp": 1,
        "profile": {
          "name": "string",
          "url": "string",
          "long_name": "string",
          "img": "string"
        },
        "language": "string",
        "...": "[Additional Properties Truncated]"
      }
    ]
  },
  "locations": {
    "type": "locations",
    "results": [
      {
        "title": "string",
        "url": "string",
        "is_source_local": false,
        "is_source_both": false,
        "description": "",
        "page_age": "string",
        "page_fetched": "string",
        "fetched_content_timestamp": 1,
        "profile": {
          "name": "string",
          "url": "string",
          "long_name": "string",
          "img": "string"
        },
        "language": "string",
        "...": "[Additional Properties Truncated]"
      }
    ],
    "provider": {}
  },
  "mixed": {
    "type": "mixed",
    "main": [
      {
        "type": "string",
        "index": 1,
        "all": false
      }
    ],
    "top": [
      {
        "type": "string",
        "index": 1,
        "all": false
      }
    ],
    "side": [
      {
        "type": "string",
        "index": 1,
        "all": false
      }
    ]
  },
  "news": {
    "type": "news",
    "results": [
      {
        "title": "string",
        "url": "string",
        "is_source_local": false,
        "is_source_both": false,
        "description": "",
        "page_age": "string",
        "page_fetched": "string",
        "fetched_content_timestamp": 1,
        "profile": {
          "name": "string",
          "url": "string",
          "long_name": "string",
          "img": "string"
        },
        "language": "string",
        "...": "[Additional Properties Truncated]"
      }
    ],
    "mutated_by_goggles": false
  },
  "videos": {
    "type": "videos",
    "results": [
      {
        "type": "video_result",
        "url": "string",
        "title": "string",
        "description": "string",
        "age": "string",
        "page_age": "string",
        "page_fetched": "string",
        "fetched_content_timestamp": 1,
        "video": {
          "duration": "string",
          "views": 1,
          "creator": "string",
          "publisher": "string",
          "requires_subscription": true,
          "tags": [
            "string"
          ],
          "author": {
            "name": "string",
            "url": "string",
            "long_name": "string",
            "img": "string"
          }
        },
        "meta_url": {
          "scheme": "string",
          "netloc": "string",
          "hostname": "string",
          "favicon": "string",
          "path": "string"
        },
        "...": "[Additional Properties Truncated]"
      }
    ],
    "mutated_by_goggles": false
  },
  "web": {
    "type": "search",
    "results": [
      {
        "title": "string",
        "url": "string",
        "is_source_local": false,
        "is_source_both": false,
        "description": "",
        "page_age": "string",
        "page_fetched": "string",
        "fetched_content_timestamp": 1,
        "profile": {
          "name": "string",
          "url": "string",
          "long_name": "string",
          "img": "string"
        },
        "language": "en",
        "...": "[Additional Properties Truncated]"
      }
    ],
    "family_friendly": true
  },
  "summarizer": {
    "type": "summarizer",
    "key": "string"
  },
  "rich": {
    "type": "rich",
    "hint": {
      "vertical": "calculator",
      "callback_key": "string"
    }
  }
}
```

## 文档正文

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/web/search?q=brave+search`

Search GET

Search POST

Local POIs GET

POI Descriptions GET

Rich search GET

LLM Context GET

LLM Context POST

Place Search GET

News GET

News POST

Videos GET

Videos POST

Images GET

Answers POST

Suggest GET

Spell check GET

Search

Search the web from a large independent index of web pages.

get/v1/web/search

qCopy link to qType: Querymin length:    1max length:    400 required 
The user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.

The user’s search query term. Query can not be empty. Maximum of 400 characters and 50 words in the query.

countryCopy link to countryType: SearchCountryenum
The 2 character country code where the search results come from. The default value is US.
ARAUATBEBR Show all values

The 2 character country code where the search results come from. The default value is US.

Show all values

search_langCopy link to search_langType: Languageenum
The 2 or more character language code for which the search results are provided.
areubnbgca Show all values

The 2 or more character language code for which the search results are provided.

ui_langCopy link to ui_langType: MarketCodesenum
User interface language preferred in response. Usually of the format <language_code>-<country_code>. For more, see RFC 9110.
es-ARen-AUde-ATnl-BEfr-BE Show all values

User interface language preferred in response. Usually of the format <language_code>-<country_code>. For more, see RFC 9110.

countCopy link to countType: Countmin:    1max:    20default:  20

  The number of search results returned in response.
  The maximum is 20. The actual number delivered may be less than requested.
  Combine this parameter with offset to paginate search results.

NOTE: Count only applies to web results.

The number of search results returned in response.
  The maximum is 20. The actual number delivered may be less than requested.
  Combine this parameter with offset to paginate search results.

NOTE: Count only applies to web results.

offsetCopy link to offsetType: Offsetmin:    0max:    9default:  0

  The zero based offset that indicates number of search
  result pages (count) to skip before returning the result.
  The default is 0 and the maximum is 9.
  The actual number delivered may be less than requested.

  Use this parameter along with the count parameter to page results.
  For example, if your user interface displays 10 search results per page,
  set count to 10 and offset to 0 to get the first page of results.
  For each subsequent page, increment offset by 1 (for example, 0, 1, 2).
  It is possible for multiple pages to include some overlap in results.

The zero based offset that indicates number of search
  result pages (count) to skip before returning the result.
  The default is 0 and the maximum is 9.
  The actual number delivered may be less than requested.

Use this parameter along with the count parameter to page results.
  For example, if your user interface displays 10 search results per page,
  set count to 10 and offset to 0 to get the first page of results.
  For each subsequent page, increment offset by 1 (for example, 0, 1, 2).
  It is possible for multiple pages to include some overlap in results.

safesearchCopy link to safesearchType: SafeSearchenum
Filters search results for adult content. The following values are supported:

  off - No filtering is done.
  moderate - Filters explicit content, like images and videos, but allows adult domains in the search results.
  strict - Drops all adult content from search results.

Defaults to moderate.
offmoderatestrict

Filters search results for adult content. The following values are supported:

off - No filtering is done.

moderate - Filters explicit content, like images and videos, but allows adult domains in the search results.

strict - Drops all adult content from search results.

Defaults to moderate.

moderate

strict

spellcheckCopy link to spellcheckType: Spellcheckdefault:  trueExamplestruefalse
Whether to spell check provided query. If the spell checker is enabled, the modified query is always used for search. The modified query can be found in altered key from the query response model.

Whether to spell check provided query. If the spell checker is enabled, the modified query is always used for search. The modified query can be found in altered key from the query response model.

freshnessCopy link to freshnessType: Freshnessdefault:  ""Examplespm2022-04-01to2022-07-30
Filters search results by page age. The age of a page is determined by the most relevant date reported by the content, such as its published or last modified date. The following values are supported:

  pd - Pages aged 24 hours or less.
  pw - Pages aged 7 days or less.
  pm - Pages aged 31 days or less.
  py - Pages aged 365 days or less.
  YYYY-MM-DDtoYYYY-MM-DD - A custom date range is also supported by specifying start and end dates e.g. 2022-04-01to2022-07-30.

Filters search results by page age. The age of
