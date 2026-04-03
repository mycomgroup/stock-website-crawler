---
id: "url-729a9e"
type: "api"
title: "Google Knowledge Graph API"
url: "https://serpapi.com/knowledge-graph"
description: "For some requests, Google search includes a \"Knowledge Graph\" block, typically on the right side. SerpApi is able to extract and make sense of this information.\n\nThe API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.\n\nFor some searches, SerpApi is able to make sense of Google's Knowledge Graph entities and serve them under entity_type.\n\nFor some searches related to places, Google Knowledge Graph might include events results like title, link, date, price, extracted_price, thumbnail, source, source_thumbnail, and badge. SerpApi is able to make sense of these and serve them under events.\n\nFor some searches related to places, Google Knowledge Graph might include events results like name, extensions, date, time, link and serpapi_link. SerpApi is able to make sense of these and serve them under events."
source: ""
tags: []
crawl_time: "2026-03-18T08:23:37.518Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Results for: Apple","description":"","requestParams":{"q":"Apple","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=Apple"}
    - {"title":"Results for: Coffee","description":"","requestParams":{"q":"Coffee","location":"United Kingdom","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=Coffee&location=United+Kingdom"}
    - {"title":"Results for: Terry Gilliam","description":"For some searches, SerpApi is able to make sense of Google's Knowledge Graph entities and serve them under entity_type.","requestParams":{"q":"Terry Gilliams","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=Terry+Gilliams"}
    - {"title":"Results for: Apple jobs","description":"","requestParams":{"q":"Apple jobs","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=Apple+jobs"}
    - {"title":"Top Carousel results for: People also search for","description":"","requestParams":{"q":"McDonald's","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=McDonald's"}
    - {"title":"Results for: webster hall","description":"For some searches related to places, Google Knowledge Graph might include events results like title, link, date, price, extracted_price, thumbnail, source, source_thumbnail, and badge. SerpApi is able to make sense of these and serve them under events.","requestParams":{"q":"webster hall","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.events"},"responseJson":"https://serpapi.com/search.json?q=webster+hall&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: paris","description":"For some searches related to places, Google Knowledge Graph might include events results like name, extensions, date, time, link and serpapi_link. SerpApi is able to make sense of these and serve them under events.","requestParams":{"q":"paris","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.events"},"responseJson":"https://serpapi.com/search.json?q=paris&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: See photos and See outside","description":"","requestParams":{"q":"Best buy madison heights","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=Best+buy+madison+heights"}
    - {"title":"Results for: Popular Times","description":"For some searches, Google will include the \"Popular Times\" block inside the Knowledge Graph. SerpApi is able to make sense of this information and extract live data and graph_results blocks. This results can contain data such as time, info, wait_time, typical_time_spent and busyness_score (the higher the score, the busier it is).","requestParams":{"q":"Original Wings & Rings","location":"Dubai","hl":"en","gl":"us","highlight":"knowledge_graph.popular_times"},"responseJson":"https://serpapi.com/search.json?q=Original+Wings+&+Rings&location=Dubai&hl=en&gl=us"}
    - {"title":"Results for: Products","description":"For some searches, Google will include the \"Products\" block inside the Knowledge Graph. For each Products result, we are able to extract its name, link, price, description, and image.","requestParams":{"q":"Park 56 Dental New York","hl":"en","gl":"us","highlight":"knowledge_graph.products"},"responseJson":"https://serpapi.com/search.json?q=Park+56+Dental+New+York&hl=en&gl=us"}
    - {"title":"Results for: Local Posts","description":"For some searches, Google will include the \"Local Posts\" block inside the Knowledge Graph. For each Local Posts result, we are able to extract its media (image or video), cta (Call To Action, e.g. \"Call now\", \"View Offer\", \"Book\"), link (for \"Book\" and \"View Offer\" cta), phone (for \"Call now\" cta), post_link, description, duration (e.g. \"Valid Aug 16 - Sep 15\"), and date.","requestParams":{"q":"Park 56 Dental New York","hl":"en","gl":"us","highlight":"knowledge_graph.posts"},"responseJson":"https://serpapi.com/search.json?q=Park+56+Dental+New+York&hl=en&gl=us"}
    - {"title":"Results for: Offers (mobile only)","description":"For some mobile searches, Google will include the \"Offers\" block inside the Knowledge Graph. For each Offer result, we are able to extract its title, image, offer_link, and duration (e.g. \"Valid Aug 16 - Sep 15\").","requestParams":{"q":"Park 56 Dental New York","hl":"en","gl":"us","highlight":"knowledge_graph.offers"},"responseJson":"https://serpapi.com/search.json?q=Park+56+Dental+New+York&hl=en&gl=us"}
    - {"title":"Results for: Shanghai Fresh Cambridge","description":"Notice: After recent changes on the API, the ordering_options key has changed to links. For some searches, Google will include links to some detailed information in Knowledge Graph. SerpApi is able to make sense of this information and extract menu_links or order_links blocks. For some searches, Google will include the \"Order Options\" block inside the Knowledge Graph. SerpApi is also able to make sense of this information and extract links which includes order_pickup and order_delivery parts. These results contain links to Google Food Ordering. Another vital blocks SerpApi is able to extract are service_options and health_and_safety blocks that contain important information about the result.","requestParams":{"q":"Shanghai Fresh Cambridge","location":"Austin","hl":"en","gl":"us","highlight":"knowledge_graph.menu_links"},"responseJson":"https://serpapi.com/search.json?q=Shanghai+Fresh+Cambridge&location=Austin&hl=en&gl=us"}
    - {"title":"Results for: Book Online Link","description":"","requestParams":{"q":"royalty blends barbershop los angeles ca","location":"United States","hl":"en","gl":"us","highlight":"knowledge_graph.menu_links"},"responseJson":"https://serpapi.com/search.json?q=royalty+blends+barbershop+los+angeles+ca&location=United+States&hl=en&gl=us"}
    - {"title":"Results for: Future Open Date","description":"For some searches, Google will include the \"Future Open Date\" block inside the Knowledge Graph. SerpApi is able to make sense of this information and extract business_opens_date.","requestParams":{"q":"Estiatorio Ornas San Francisco","location":"Austin, Texas, United States","hl":"en","gl":"us","highlight":"knowledge_graph.menu_links"},"responseJson":"https://serpapi.com/search.json?q=Estiatorio+Ornas+San+Francisco&location=Austin,+Texas,+United+States&hl=en&gl=us"}
    - {"title":"Results for: Recently Opened Status","description":"For some searches, Google will include the \"Recently Opened\" block inside the Knowledge Graph. SerpApi is able to make sense of this information and extract business_recently_opened.","requestParams":{"q":"Fiorello Inner Sunset San Francisco","location":"Austin, Texas, United States","hl":"en","gl":"us","highlight":"knowledge_graph.menu_links"},"responseJson":"https://serpapi.com/search.json?q=Fiorello+Inner+Sunset+San+Francisco&location=Austin,+Texas,+United+States&hl=en&gl=us"}
    - {"title":"Results for: Merchant Description","description":"For some searches, Google will include the \"Merchant Description\" block inside the Knowledge Graph. SerpApi is able to make sense of this information and extract merchant_description. These results can contain important information on the subject detailed at the Knowledge Graph.","requestParams":{"q":"Century Travel","location":"Austin","hl":"en","gl":"us","highlight":"knowledge_graph.merchant_description"},"responseJson":"https://serpapi.com/search.json?q=Century+Travel&location=Austin&hl=en&gl=us"}
    - {"title":"Results for: Notable Moments","description":"When SerpApi encounters Notable Moments results, we add them to our JSON output as the array notable_moments. For each Short Videos result, we are able to extract its year, summary, source, link_text, and link.","requestParams":{"q":"Tom Hanks","device":"mobile","hl":"en","gl":"us","highlight":"knowledge_graph.notable_moments"},"responseJson":"https://serpapi.com/search.json?q=Tom+Hanks&device=mobile&hl=en&gl=us"}
    - {"title":"Results for: Watch Now","description":"When SerpApi encounters Watch Now results, we add them to our JSON output as the array watch_now. These are direct links to subscription services or markets you can access the media in the query. For each Watch Now result, we are able to extract its name, image, and link.","requestParams":{"q":"Mandalorian","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.watch_now"},"responseJson":"https://serpapi.com/search.json?q=Mandalorian&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: Audience Reviews","description":"When SerpApi encounters Audience Reviews results, we add them to our JSON output as the array audience_reviews. For each Audience Reviews result, we are able to extract its rating, summary, and user.","requestParams":{"q":"Mandalorian","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.audience_reviews"},"responseJson":"https://serpapi.com/search.json?q=Mandalorian&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: Editorial Reviews","description":"When SerpApi encounters Editorial Reviews results, we add them to our JSON output as the array editorial_reviews. For each Editorial Reviews result, we are able to extract its title, rating, and link.","requestParams":{"q":"Mandalorian","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.editorial_reviews"},"responseJson":"https://serpapi.com/search.json?q=Mandalorian&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: User Statistics","description":"When SerpApi encounters User Statistics results, we add them to our JSON output as the array user_statistics. For each User Statistics result, we are able to extract its platform and statistic.","requestParams":{"q":"Mandalorian","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.user_statistics"},"responseJson":"https://serpapi.com/search.json?q=Mandalorian&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: Mandalorian","description":"For some searches, Google's layout could be different, and it could disrupt the knowledge graph results. SerpApi is able to make sense of this situation and deliver the result regardless of the layout.","requestParams":{"q":"Mandalorian","location":"Austin","hl":"en","gl":"us","highlight":"knowledge_graph.cast"},"responseJson":"https://serpapi.com/search.json?q=Mandalorian&location=Austin&hl=en&gl=us"}
    - {"title":"Results for: Episodes","description":"When SerpApi encounters Episodes results, we add them to our JSON output as the array episodes. For each Episodes result, we are able to extract its title, name, watch, extensions, and summary.","requestParams":{"q":"Dark Tv Series","device":"Desktop","hl":"en","gl":"us","highlight":"knowledge_graph.episodes"},"responseJson":"https://serpapi.com/search.json?q=Dark+Tv+Series&device=Desktop&hl=en&gl=us"}
    - {"title":"Results for: Movies","description":"When SerpApi encounters Movies results, we add them to our JSON output as the array movies. For each Movies result, we are able to extract its name, extensions, link and image.","requestParams":{"q":"Tom Cruise","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.movies"},"responseJson":"https://serpapi.com/search.json?q=Tom+Cruise&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: Players","description":"When SerpApi encounters players results (sports rosters or teams), we add them to our JSON output as the array players. For each Players result, we are able to extract its name, extensions, link and image.","requestParams":{"q":"Liverpool Team","device":"mobile","hl":"en","gl":"us","highlight":"knowledge_graph.players"},"responseJson":"https://serpapi.com/search.json?q=Liverpool+Team&device=mobile&hl=en&gl=us"}
    - {"title":"Results for: Density Formula","description":"When SerpApi encounters Formula results, we add them to our JSON output as the dictionary formula. For each Formula result, we are able to extract its parameters, image_formula, tex_formula.","requestParams":{"q":"Density Formula","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.formula"},"responseJson":"https://serpapi.com/search.json?q=Density+Formula&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: Breadcrumbs","description":"When SerpApi encounters breadcrumb elements that consist of links, we add them to our JSON output as the dictionary breadcrumbs. For each Breadcrumb result, we are able to extract its title and link.","requestParams":{"q":"watch bills","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.breadcrumbs"},"responseJson":"https://serpapi.com/search.json?q=watch+bills&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: Pears","description":"For some searches, Google's layout could be different. SerpApi is able to make sense of these cases and deliver header_images and web_results.","requestParams":{"q":"pears","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.web_results"},"responseJson":"https://serpapi.com/search.json?q=pears&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: Jessica Alba","description":"For some searches, Google's mobile layout could be different. SerpApi is able to make sense of these cases and deliver web_results, including title, snippet, images, and more.","requestParams":{"q":"Jessica Alba","device":"mobile","hl":"en","gl":"us","highlight":"knowledge_graph.web_results"},"responseJson":"https://serpapi.com/search.json?q=Jessica+Alba&device=mobile&hl=en&gl=us"}
    - {"title":"Results for: Paris","description":"For some searches, Google's mobile layout contains additional information for locations. SerpApi is able to make sense of these cases and deliver web_results, including carousel, related_searches, and more.","requestParams":{"q":"Paris","device":"mobile","hl":"en","gl":"us","highlight":"knowledge_graph.web_results"},"responseJson":"https://serpapi.com/search.json?q=Paris&device=mobile&hl=en&gl=us"}
    - {"title":"Results for: Cristiano Ronaldo","description":"For some searches, Google's layout contains additional information for individuals. SerpApi is able to make sense of these cases and deliver web_results, including title, snippet, stats, and more.","requestParams":{"q":"Cristiano Ronaldo","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.web_results"},"responseJson":"https://serpapi.com/search.json?q=Cristiano+Ronaldo&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: Saffron","description":"For some searches, Google Knowledge Graph might contain information in unexpanded buttons. SerpApi is able to make sense of these under buttons.","requestParams":{"q":"Saffron","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.buttons"},"responseJson":"https://serpapi.com/search.json?q=Saffron&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: Tesla","description":"For some searches, Google Knowledge Graph might contain a unique Knowledge Graph ID(kgmid). It may also contain tabs that lead to different sections of the same subject within the Knowledge Graph or alongside menu items. SerpApi is able to make sense of these and serve them under kgmid, knowledge_graph_link, serpapi_knowledge_graph_search_link, and tabs keys.","requestParams":{"q":"Tesla","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.tabs"},"responseJson":"https://serpapi.com/search.json?q=Tesla&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: Ford Lake Keowee","description":"For some searches, Google Knowledge Graph might contain listings of vehicles for sale based on a specific location or dealership. SerpApi makes sense of this data by rendering all of this information inside vehicles_for_sale. For new vehicles prices will be listed as msrp (manufacturer's suggested retail price). Meanwhile, used vehicle prices will be listed as used_price and also include the mileage.","requestParams":{"q":"ford lake keowee","device":"mobile","hl":"en","gl":"us","highlight":"knowledge_graph.vehicles_for_sale"},"responseJson":"https://serpapi.com/search.json?q=ford+lake+keowee&device=mobile&hl=en&gl=us"}
    - {"title":"Results for: Boston University","description":"For some searches related to college or university, Google Knowledge Graph might include important information like cost, graduation rate, acceptance rate, College facts, Employer outcomes and Program majors.","requestParams":{"q":"Boston University","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.institution_stats"},"responseJson":"https://serpapi.com/search.json?q=Boston+University&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: Davenport University","description":"For some searches related to college or university, Google Knowledge Graph might include important information like Cost by household income and Graduation rate.","requestParams":{"q":"Davenport University","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.cost_by_household_income"},"responseJson":"https://serpapi.com/search.json?q=Davenport+University&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: apple financials","description":"For some searches, Google will include the \"Financials\" block inside the Knowledge Graph. SerpApi is able to make sense of this information and extract financials.","requestParams":{"q":"apple financials","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.financials"},"responseJson":"https://serpapi.com/search.json?q=apple+financials&device=desktop&hl=en&gl=us"}
    - {"title":"Results for: German Shepherd","description":"For some searches, Google will include the audio files inside the Knowledge Graph. SerpApi is able to make sense of this information and extract audio_results.","requestParams":{"q":"German Shepherd","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.audio_results"},"responseJson":"https://serpapi.com/search.json?q=German+Shepherd&device=desktop&hl=en&gl=us"}
    - {"title":"Admission Results for: Louvre","description":"For some searches, Google will include the Admission Results inside the Knowledge Graph. SerpApi is able to make sense of this information and extract admission.","requestParams":{"q":"Louvre","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.admission"},"responseJson":"https://serpapi.com/search.json?q=Louvre&device=desktop&hl=en&gl=us"}
    - {"title":"Local Business Provider results for: SOFIT GYM","description":"For some local business searches, Google will include the provider links inside the Knowledge Graph. It includes Appointments, Order, Reservations. SerpApi is able to make sense of this information and extract appointment_providers, shop_online_providers, reservation_providers respectively.","requestParams":{"q":"SOFIT GYM","location":"Yokohama, Kanagawa Prefecture, Japan","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph.appointments"},"responseJson":"https://serpapi.com/search.json?q=SOFIT+GYM&location=Yokohama,+Kanagawa+Prefecture,+Japan&device=desktop&hl=en&gl=us"}
    - {"title":"Local Business results for: Footer Locker","description":"For some local business searches, Google will include business-specific links inside the Knowledge Graph. It includes Website, Directions, and Reviews. SerpApi is able to make sense of this information and extract website, directions, and reviews respectively.","requestParams":{"q":"Foot Locker 50 Rideau St","location":"Austin, Texas, United States","device":"desktop","hl":"en","gl":"us","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=Foot+Locker+50+Rideau+St&location=Austin,+Texas,+United+States&device=desktop&hl=en&gl=us"}
    - {"title":"Expanded Knowledge Graph Results with ibp","description":"The ibp parameter can expand knowledge graph data, offering a more detailed view on information. This includes additional fields and insights not typically visible in the standard inline knowledge graph presentation.","requestParams":{"q":"Starbucks","location":"Austin, Texas, United States","device":"mobile","hl":"en","gl":"us","ibp":"gwp;0,7","ludocid":"16634675850833845314","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=Starbucks&location=Austin,+Texas,+United+States&device=mobile&hl=en&gl=us&ibp=gwp;0,7&ludocid=16634675850833845314"}
    - {"title":"Price Details for: Nami Nori","description":"For some searches (usually restaurants), price and price distribution data are available. SerpApi is able to make sense of this information and extract price and price_details.","requestParams":{"q":"Nami Nori","highlight":"knowledge_graph.price_details"},"responseJson":"https://serpapi.com/search.json?q=Nami+Nori"}
    - {"title":"Booking Options for: Big Bus tours new York","description":"For some searches, Google will include the \"Booking Options\" block inside the Knowledge Graph. SerpApi is able to make sense of this information and extract booking_options blocks. This results can contain data such as title, price, duration, confirmation, mobile_ticket, link and thumbnail.","requestParams":{"q":"Big Bus tours new York","highlight":"knowledge_graph.booking_options"},"responseJson":"https://serpapi.com/search.json?q=Big+Bus+tours+new+York"}
    - {"title":"Results for: Coffee","description":"For some searches, Google Knowledge Graph might contain a description with highlighted words and multiple sources. SerpApi is able to make sense of this information and extract the list of description_highlighted_words and sources.","requestParams":{"q":"Coffee","device":"mobile","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=Coffee&device=mobile"}
    - {"title":"Results for: Steve Jobs","description":"For some searches, Google Knowledge Graph might contain some web_results with multiple sources. SerpApi is able to make sense of this information and extract the list of sources.","requestParams":{"q":"Steve Jobs","device":"mobile","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=Steve+Jobs&device=mobile"}
    - {"title":"Results for: The White Lotus","description":"For some searches, Google Knowledge Graph might contain some ratings inside web_results. SerpApi is able to make sense of this information and extract the source, source_icon, rating, and link.","requestParams":{"q":"The White Lotus","device":"desktop","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=The+White+Lotus&device=desktop"}
    - {"title":"Results for: Pedro Pascal","description":"For some searches, Google Knowledge Graph might contain some web_results with a list of expandable content inside. SerpApi is able to make sense of this information and extract the list of items.","requestParams":{"q":"Pedro Pascal","device":"mobile","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=Pedro+Pascal&device=mobile"}
    - {"title":"Results for: Eminem","description":"For some searches related to singers, Google Knowledge Graph might include listings of songs. SerpApi is able to make sense of this information and extract the list of songs.","requestParams":{"q":"Eminem","device":"desktop","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=Eminem&device=desktop"}
    - {"title":"Results for: Taj Mahal","description":"For some searches, Google Knowledge Graph might contain some web_results with relevant informations about the search query, such as: reviews, tickets, weather, and more.","requestParams":{"q":"Taj Mahal","device":"desktop","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=Taj+Mahal&device=desktop"}
    - {"title":"Results for: PSY","description":"For some searches, Google Knowledge Graph might contain some web_results with videos information inside.","requestParams":{"q":"psy","device":"desktop","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=psy&device=desktop"}
    - {"title":"Results for: Club Esperia SP with device: mobile","description":"","requestParams":{"q":"club esperia sp","device":"mobile","location":"Pinheiros, Pinheiros, State of São Paulo, Brazil","google_domain":"google.com.br","hl":"en","gl":"br","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=club+esperia+sp&device=mobile&location=Pinheiros,+Pinheiros,+State+of+São+Paulo,+Brazil&google_domain=google.com.br&hl=en&gl=br"}
    - {"title":"AI Overviews results for: Breaking Bad","description":"For some searches, Google Knowledge Graph might contain AI Overview expandable sections, describing particular aspects of the knowledge graph entity. SerpApi is able to extract this information from the Knowledge Graph.","requestParams":{"q":"breaking bad","device":"mobile","location":"Austin, Texas, United States","google_domain":"google.com","hl":"en","gl":"us","highlight":"knowledge_graph"},"responseJson":"https://serpapi.com/search.json?q=breaking+bad&device=mobile&location=Austin,+Texas,+United+States&google_domain=google.com&hl=en&gl=us"}
  importantNotes:
    - "Notice: After recent changes on the API, the ordering_options key has changed to links. For some searches, Google will include links to some detailed information in Knowledge Graph. SerpApi is able to make sense of this information and extract menu_links or order_links blocks. For some searches, Google will include the \"Order Options\" block inside the Knowledge Graph. SerpApi is also able to make sense of this information and extract links which includes order_pickup and order_delivery parts. These results contain links to Google Food Ordering. Another vital blocks SerpApi is able to extract are service_options and health_and_safety blocks that contain important information about the result."
    - "For some searches related to college or university, Google Knowledge Graph might include important information like cost, graduation rate, acceptance rate, College facts, Employer outcomes and Program majors."
    - "For some searches related to college or university, Google Knowledge Graph might include important information like Cost by household income and Graduation rate."
  rawContent: "Api Dashboard\n\nApi Dashboard\n\nYour Account\n\nEdit Profile\n\nExtra Credits\n\nApi Documentation\n\nApi Documentation\n\nGoogle Search API\n\nAI Overview\n\nAbout Carousel\n\nAsk AI Mode\n\nAvailable On\n\nBroaden Searches\n\nBuying Guide\n\nComplementary Results\n\nDMCA Messages\n\nDiscover More Places\n\nDiscussions and Forums\n\nEpisode Guide\n\nEvents Results\n\nFind Results On\n\nGoogle About This Result API\n\nGrammar Check\n\nImmersive Products\n\nInline Images\n\nInline People Also Search For\n\nInline Products\n\nInline Shopping\n\nInline Videos\n\nInteractive Diagram\n\nJobs Results\n\nKnowledge Graph\n\nLatest From\n\nLatest Posts\n\nMenu Highlights\n\nNews Results\n\nNutrition Information\n\nOrganic Results\n\nPerspectives\n\nPlaces Sites\n\nPopular Destinations\n\nProduct Result\n\nProduct Sites\n\nQuestions And Answers\n\nRecipes Results\n\nRefine Search Filters\n\nRefine This Search\n\nRelated Brands\n\nRelated Categories\n\nRelated Questions\n\nRelated Searches\n\nScholarly Articles\n\nShort Videos\n\nShowtimes Results\n\nSpell Check\n\nSports Results\n\nThings To Know\n\nTop Carousel\n\nTop Insights\n\nTop Stories\n\nTwitter Results\n\nVisual Stories\n\nGoogle Light Search API\n\nKnowledge Graph\n\nOrganic Results\n\nRelated Questions\n\nRelated Searches\n\nSpell Check\n\nTop Stories\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nAd Details API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Finance Markets API\n\nGoogle Flights API\n\nAirports Results\n\nAutocomplete API\n\nBooking Options\n\nFlights Results\n\nPrice Insights\n\nGoogle Forums API\n\nGoogle Hotels API\n\nAutocomplete API\n\nProperty Details\n\nReviews API\n\nGoogle Images API\n\nImages Results\n\nRelated Content API\n\nRelated Searches\n\nShopping Results\n\nSuggested Searches\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nListing API\n\nGoogle Lens API\n\nAbout This Image"
  suggestedFilename: "knowledge-graph-api"
---

# Google Knowledge Graph API

## 源URL

https://serpapi.com/knowledge-graph

## 描述

For some requests, Google search includes a "Knowledge Graph" block, typically on the right side. SerpApi is able to extract and make sense of this information.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

For some searches, SerpApi is able to make sense of Google's Knowledge Graph entities and serve them under entity_type.

For some searches related to places, Google Knowledge Graph might include events results like title, link, date, price, extracted_price, thumbnail, source, source_thumbnail, and badge. SerpApi is able to make sense of these and serve them under events.

For some searches related to places, Google Knowledge Graph might include events results like name, extensions, date, time, link and serpapi_link. SerpApi is able to make sense of these and serve them under events.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 注意事项

- Notice: After recent changes on the API, the ordering_options key has changed to links. For some searches, Google will include links to some detailed information in Knowledge Graph. SerpApi is able to make sense of this information and extract menu_links or order_links blocks. For some searches, Google will include the "Order Options" block inside the Knowledge Graph. SerpApi is also able to make sense of this information and extract links which includes order_pickup and order_delivery parts. These results contain links to Google Food Ordering. Another vital blocks SerpApi is able to extract are service_options and health_and_safety blocks that contain important information about the result.
- For some searches related to college or university, Google Knowledge Graph might include important information like cost, graduation rate, acceptance rate, College facts, Employer outcomes and Program majors.
- For some searches related to college or university, Google Knowledge Graph might include important information like Cost by household income and Graduation rate.

## 文档正文

For some requests, Google search includes a "Knowledge Graph" block, typically on the right side. SerpApi is able to extract and make sense of this information.

The API endpoint is https://serpapi.com/search?engine=google Head to the playground for a live and interactive demo.

For some searches, SerpApi is able to make sense of Google's Knowledge Graph entities and serve them under entity_type.

For some searches related to places, Google Knowledge Graph might include events results like title, link, date, price, extracted_price, thumbnail, source, source_thumbnail, and badge. SerpApi is able to make sense of these and serve them under events.

For some searches related to places, Google Knowledge Graph might include events results like name, extensions, date, time, link and serpapi_link. SerpApi is able to make sense of these and serve them under events.

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
