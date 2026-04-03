---
id: "url-47b25cc9"
type: "api"
title: "Golang"
url: "https://serpapi.com/integrations/go"
description: "Integrate search data into your Go application. This library is the official wrapper for SerpApi.\n\nSerpApi supports Google, Google Maps, Google Shopping, Baidu, Yandex, Yahoo, eBay, App Stores, and more.\n\nThis example runs a search for \"coffee\" on Google. It then returns the results a Go map. See the playground to generate your own code.\n\nGoogle search documentation. More hands on examples are available below.\n\nIt prints the first 5 locations matching Austin (Texas, Texas, Rochester)"
source: ""
tags: []
crawl_time: "2026-03-18T10:18:13.943Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples: []
  importantNotes: []
  rawContent: "Documentation\n\nIntegrations\n\nDocumentation\n\nIntegrations\n\nStart integration with your preferred language.\n\nCode to integrate\n\npackage main\n\nimport (\n  \"github.com/serpapi/serpapi-golang\"\n  \"os\"\n  \"fmt\"\n  \"log\"\n)\n\nfunc main(){\n  // replace with your SerpApi key\n  setting := serpapi.NewSerpApiClientSetting(os.Getenv(\"SERPAPI_KEY\"))\n  setting.Engine = \"google\"\n  // initialize the client\n  client := serpapi.NewClient(setting)\n  parameter := map[string]string{\n    \"q\": \"Coffee\",\n    \"location\": \"Austin, Texas, United States\",\n    \"hl\": \"en\",\n    \"gl\": \"us\",\n    \"google_domain\": \"google.com\",\n  }\n  results, err := client.Search(parameter)\n  if err != nil {\n    log.Fatal(err)\n  }\n  fmt.Println(results)\n}\n\npackage main\n\nimport (\n  \"github.com/serpapi/serpapi-golang\"\n  \"os\"\n  \"fmt\"\n  \"log\"\n)\n\nfunc main(){\n  // replace with your SerpApi key\n  setting := serpapi.NewSerpApiClientSetting(os.Getenv(\"SERPAPI_KEY\"))\n  setting.Engine = \"google\"\n  // initialize the client\n  client := serpapi.NewClient(setting)\n  parameter := map[string]string{\n    \"q\": \"Coffee\",\n    \"location\": \"Austin, Texas, United States\",\n    \"hl\": \"en\",\n    \"gl\": \"us\",\n    \"google_domain\": \"google.com\",\n  }\n  results, err := client.Search(parameter)\n  if err != nil {\n    log.Fatal(err)\n  }\n  fmt.Println(results)\n}\n\nSerpApi Go Library\n\nIntegrate search data into your Go application. This library is the official wrapper for SerpApi.\n\nSerpApi supports Google, Google Maps, Google Shopping, Baidu, Yandex, Yahoo, eBay, App Stores, and more.\n\nInstallation\n\nGo 1.10+ is required.\n\ngo get -u github.com/serpapi/serpapi-golang\n\nSimple Usage\n\nimport \"github.com/serpapi/serpapi-golang\"\nsetting := serpapi.NewSerpApiClientSetting(\"<SERPAPI_KEY>\") // Replace with your SerpApi key\nsetting.Engine = \"google\" // Set the search engine to Google\nclient := serpapi.NewClient(setting)\nparameter := map[string]string{\n  \"q\":             \"Coffee\",\n  \"location\":      \"Austin, Texas, United States\",\n}\nresults, err := client.Search(parameter)\nfmt.Println(results)\n\nThis example runs a search for \"coffee\" on Google. It then returns the results a Go map.\nSee the playground to generate your own code.\n\nAdvanced Usage\n\nfunc main() {\n  // Initialize the client with custom setting\n\tsetting := serpapi.NewSerpApiClientSetting(\"<SERPAPI_KEY>\") // Replace with your SerpApi key\n\tsetting.Persistent = false                     // Enable persistent search\n\tsetting.Asynchronous = true                    // Enable asynchronous search\n\tsetting.Timeout = 60 * time.Second             // Set timeout for HTTP requests\n\tsetting.MaxIdleConnection = 10                 // Set maximum idle connections\n\tsetting.KeepAlive = 60 * time.Second           // Set keep-alive duration\n\tsetting.TLSHandshakeTimeout = 10 * time.Second // Set TLS handshake timeout\n\n\tclient := serpapi.NewClient(setting)\n\n  // search query overview (more fields available depending on search engine)\n  parameter := map[string]string{\n    \"q\":             \"Coffee\",\n    \"location\":      \"Austin, Texas, United States\",\n    \"hl\":            \"en\",\n    \"gl\":            \"us\",\n    \"google_domain\": \"google.com\",\n    \"safe\":          \"active\",\n    \"start\":         \"10\",\n    \"device\":        \"desktop\",\n  }\n\n  // formated search results as a map\n  // serpapi.com converts HTML -> JSON\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    panic(err)\n  }\n  fmt.Println(rsp)\n\n  // raw search engine html as a String\n  // serpapi.com acts a proxy to provive high throughputs, no search limit and more.\n  raw_html, err := client.Html(parameter)\n  if err != nil { \n    panic(err)\n  }\n  fmt.Println(raw_html)\n}\n\nGoogle search documentation.\nMore hands on examples are available below.\n\nFull documentation on SerpApi.com\n\nLibrary Github page\n\nAPI health status\n\nLocation API\n\nimport (\n\t\"fmt\"\n\t\"github.com/serpapi/serpapi-golang\"\n)\n\nsetting := serpapi.NewSerpApiClientSetting(\"<SERPAPI_KEY>\") // Replace with your SerpApi secret key\nclient := serpapi.NewClient(setting)\nlocationList, err := client.Location(\"Austin\", 5)\n\nif err != nil {\n  panic(err)\n}\nfmt.Println(locationList)\n\nIt prints the first 5 locations matching Austin (Texas, Texas, Rochester)\n\n[map[canonical_name:Austin,TX,Texas,United States country_code:US google_id:200635 google_parent_id:21176 gps:[-97.7430608 30.267153]...\n\nsee: (test/location_test.go)\n\nSearch Archive API\n\nThis API allows retrieving previous search results.\nTo fetch earlier results from the search_id.\n\nFirst, you need to run a search and save the search id.\n\n// First, you need to run a search and save the search id.\nauth := map[string]string{\n  \"engine\":  \"google\",\n  \"api_key\": \"secret_api_key\",\n}\nclient := serpapi.NewClient(auth)\nparameter := map[string]string{\n  \"q\":        \"Coffee\",\n  \"location\": \"Portland\"}\n\nrsp, err := client.Search(parameter)\n\nif err != nil {\n  t.Error(\"unexpected error\", err)\n  return\n}\n\n// Now let's retrieve the previous search results from the archive.\nsearchID := rsp[\"search_metadata\"].(map[string]interface{})[\"id\"].(string)\nif len(searchID) == 0 {\n  t.Error(\"search_metadata.id must be defined\")\n  return\n}\n\nsearchArchive, err := client.SearchArchive(searchID)\nif err != nil {\n  t.Error(err)\n  return\n}\n\nsearchIDArchive := searchArchive[\"search_metadata\"].(map[string]interface{})[\"id\"].(string)\nif searchIDArchive != searchID {\n  t.Error(\"search_metadata.id do not match\", searchIDArchive, searchID)\n}\n\nThis code prints the search results from the archive. :)\n\nAccount API\n\nauth := map[string]string{\n \"api_key\": \"<secret_api_key>\"\n}\nclient := serpapi.NewClient(auth)\nrsp, err = client.Account()\nfmt.Println(rsp)\n\nIt prints your account information.\n\nBasic examples in Go\n\nSearch google\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google\", \n    \"q\": \"coffee\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"organic_results\"] == nil {\n    fmt.Println(\"key is not found: organic_results\")\n    return \n  }\n\n  if len(rsp[\"organic_results\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 organic_results\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_test.go\n\nsee: serpapi.com/search-api\n\nSearch google light\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_light\", \n    \"q\": \"coffee\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"organic_results\"] == nil {\n    fmt.Println(\"key is not found: organic_results\")\n    return \n  }\n\n  if len(rsp[\"organic_results\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 organic_results\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_light_test.go\n\nsee: serpapi.com/google-light-api\n\nSearch google scholar\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_scholar\", \n    \"q\": \"biology\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"organic_results\"] == nil {\n    fmt.Println(\"key is not found: organic_results\")\n    return \n  }\n\n  if len(rsp[\"organic_results\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 organic_results\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_scholar_test.go\n\nsee: serpapi.com/google-scholar-api\n\nSearch google autocomplete\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_autocomplete\", \n    \"q\": \"coffee\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"suggestions\"] == nil {\n    fmt.Println(\"key is not found: suggestions\")\n    return \n  }\n\n  if len(rsp[\"suggestions\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 suggestions\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_autocomplete_test.go\n\nsee: serpapi.com/google-autocomplete-api\n\nSearch google product\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_product\", \n    \"q\": \"coffee\", \n    \"product_id\": \"4887235756540435899\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"product_results\"] == nil {\n    fmt.Println(\"key is not found: product_results\")\n    return \n  }\n\n  if len(rsp[\"product_results\"].(map[string]interface{})) < 5 {\n    fmt.Println(\"expect more than  5 product_results\")\n    return\n  }\n}\n\nsource code: test/example/example_search_google_product_test.go\n\nsee: serpapi.com/google-product-api\n\nSearch google reverse image\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_reverse_image\", \n    \"image_url\": \"https://i.imgur.com/5bGzZi7.jpg\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"image_sizes\"] == nil {\n    fmt.Println(\"key is not found: image_sizes\")\n    return \n  }\n\n  if len(rsp[\"image_sizes\"].([]interface{})) < 1 {\n    fmt.Println(\"expect more than 1 image_sizes\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_reverse_image_test.go\n\nsee: serpapi.com/google-reverse-image\n\nSearch google events\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_events\", \n    \"q\": \"coffee\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"events_results\"] == nil {\n    fmt.Println(\"key is not found: events_results\")\n    return \n  }\n\n  if len(rsp[\"events_results\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 events_results\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_events_test.go\n\nsee: serpapi.com/google-events-api\n\nSearch google local services\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_local_services\", \n    \"q\": \"electrician\", \n    \"data_cid\": \"6745062158417646970\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"local_ads\"] == nil {\n    fmt.Println(\"key is not found: local_ads\")\n    return \n  }\n\n  if len(rsp[\"local_ads\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 local_ads\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_local_services_test.go\n\nsee: serpapi.com/google-local-services-api\n\nSearch google maps\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_maps\", \n    \"q\": \"Coffee\", \n    \"ll\": \"@40.7455096,-74.0083012,14z\", \n    \"type\": \"search\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"local_results\"] == nil {\n    fmt.Println(\"key is not found: local_results\")\n    return \n  }\n\n  if len(rsp[\"local_results\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 local_results\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_maps_test.go\n\nsee: serpapi.com/google-maps-api\n\nSearch google jobs\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_jobs\", \n    \"q\": \"coffee\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"jobs_results\"] == nil {\n    fmt.Println(\"key is not found: jobs_results\")\n    return \n  }\n\n  if len(rsp[\"jobs_results\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 jobs_results\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_jobs_test.go\n\nsee: serpapi.com/google-jobs-api\n\nSearch google play\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_play\", \n    \"q\": \"kite\", \n    \"store\": \"apps\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"organic_results\"] == nil {\n    fmt.Println(\"key is not found: organic_results\")\n    return \n  }\n\n  if len(rsp[\"organic_results\"].([]interface{})) < 1 {\n    fmt.Println(\"expect more than 1 organic_results\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_play_test.go\n\nsee: serpapi.com/google-play-api\n\nSearch google images\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_images\", \n    \"tbm\": \"isch\", \n    \"q\": \"coffee\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"images_results\"] == nil {\n    fmt.Println(\"key is not found: images_results\")\n    return \n  }\n\n  if len(rsp[\"images_results\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 images_results\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_images_test.go\n\nsee: serpapi.com/images-results\n\nSearch google lens\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_lens\", \n    \"url\": \"https://i.imgur.com/HBrB8p0.png\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"visual_matches\"] == nil {\n    fmt.Println(\"key is not found: visual_matches\")\n    return \n  }\n\n  if len(rsp[\"visual_matches\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 visual_matches\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_lens_test.go\n\nsee: serpapi.com/google-lens-api\n\nSearch google images light\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_images_light\", \n    \"q\": \"Coffee\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"images_results\"] == nil {\n    fmt.Println(\"key is not found: images_results\")\n    return \n  }\n\n  if len(rsp[\"images_results\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 images_results\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_images_light_test.go\n\nsee: serpapi.com/google-images-light-api\n\nSearch google hotels\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_hotels\", \n    \"q\": \"Bali Resorts\", \n    \"check_in_date\": \"2025-05-26\", \n    \"check_out_date\": \"2025-05-27\", \n    \"adults\": \"2\", \n    \"currency\": \"USD\", \n    \"gl\": \"us\", \n    \"hl\": \"en\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"properties\"] == nil {\n    fmt.Println(\"key is not found: properties\")\n    return \n  }\n\n  if len(rsp[\"properties\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 properties\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_hotels_test.go\n\nsee: serpapi.com/google-hotels-api\n\nSearch google flights\n\nimport (\t\n  \"github.com/serpapi/serpapi-golang\" \n  \"fmt\"\n)\n\n func main() {\n\n  auth := map[string]string{\n    \"api_key\": \"secret_api_key\",\n  }\n  client := serpapi.NewClient(auth)\n\n  parameter := map[string]string{\n    \"engine\": \"google_flights\", \n    \"departure_id\": \"PEK\", \n    \"arrival_id\": \"AUS\", \n    \"outbound_date\": \"2025-05-26\", \n    \"return_date\": \"2025-06-01\", \n    \"currency\": \"USD\", \n    \"hl\": \"en\",  }\n  rsp, err := client.Search(parameter)\n\n  if err != nil {\n    fmt.Println(\"unexpected error\", err)\n    return\n  }\n\n  if rsp[\"search_metadata\"].(map[string]interface{})[\"status\"] != \"Success\" {\n    fmt.Println(\"bad status\")\n    return\n  }\n\n  if rsp[\"best_flights\"] == nil {\n    fmt.Println(\"key is not found: best_flights\")\n    return \n  }\n\n  if len(rsp[\"best_flights\"].([]interface{})) < 5 {\n    fmt.Println(\"expect more than 5 best_flights\") \n    return\n  }\n}\n\nsource code: test/example/example_search_google_flights_test.go"
  suggestedFilename: "integrations_go-api"
---

# Golang

## 源URL

https://serpapi.com/integrations/go

## 描述

Integrate search data into your Go application. This library is the official wrapper for SerpApi.

SerpApi supports Google, Google Maps, Google Shopping, Baidu, Yandex, Yahoo, eBay, App Stores, and more.

This example runs a search for "coffee" on Google. It then returns the results a Go map. See the playground to generate your own code.

Google search documentation. More hands on examples are available below.

It prints the first 5 locations matching Austin (Texas, Texas, Rochester)

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Integrate search data into your Go application. This library is the official wrapper for SerpApi.

SerpApi supports Google, Google Maps, Google Shopping, Baidu, Yandex, Yahoo, eBay, App Stores, and more.

This example runs a search for "coffee" on Google. It then returns the results a Go map. See the playground to generate your own code.

Google search documentation. More hands on examples are available below.

It prints the first 5 locations matching Austin (Texas, Texas, Rochester)

## API 端点

**Method:** `GET`
**Endpoint:** `https://serpapi.com/search`

Documentation

Integrations

Documentation

Integrations

Start integration with your preferred language.

Code to integrate

package main

import (
  "github.com/serpapi/serpapi-golang"
  "os"
  "fmt"
  "log"
)

func main(){
  // replace with your SerpApi key
  setting := serpapi.NewSerpApiClientSetting(os.Getenv("SERPAPI_KEY"))
  setting.Engine = "google"
  // initialize the client
  client := serpapi.NewClient(setting)
  parameter := map[string]string{
    "q": "Coffee",
    "location": "Austin, Texas, United States",
    "hl": "en",
    "gl": "us",
    "google_domain": "google.com",
  }
  results, err := client.Search(parameter)
  if err != nil {
    log.Fatal(err)
  }
  fmt.Println(results)
}

package main

import (
  "github.com/serpapi/serpapi-golang"
  "os"
  "fmt"
  "log"
)

func main(){
  // replace with your SerpApi key
  setting := serpapi.NewSerpApiClientSetting(os.Getenv("SERPAPI_KEY"))
  setting.Engine = "google"
  // initialize the client
  client := serpapi.NewClient(setting)
  parameter := map[string]string{
    "q": "Coffee",
    "location": "Austin, Texas, United States",
    "hl": "en",
    "gl": "us",
    "google_domain": "google.com",
  }
  results, err := client.Search(parameter)
  if err != nil {
    log.Fatal(err)
  }
  fmt.Println(results)
}

SerpApi Go Library

Integrate search data into your Go application. This library is the official wrapper for SerpApi.

SerpApi supports Google, Google Maps, Google Shopping, Baidu, Yandex, Yahoo, eBay, App Stores, and more.

Installation

Go 1.10+ is required.

go get -u github.com/serpapi/serpapi-golang

Simple Usage

import "github.com/serpapi/serpapi-golang"
setting := serpapi.NewSerpApiClientSetting("<SERPAPI_KEY>") // Replace with your SerpApi key
setting.Engine = "google" // Set the search engine to Google
client := serpapi.NewClient(setting)
parameter := map[string]string{
  "q":             "Coffee",
  "location":      "Austin, Texas, United States",
}
results, err := client.Search(parameter)
fmt.Println(results)

This example runs a search for "coffee" on Google. It then returns the results a Go map.
See the playground to generate your own code.

Advanced Usage

func main() {
  // Initialize the client with custom setting
	setting := serpapi.NewSerpApiClientSetting("<SERPAPI_KEY>") // Replace with your SerpApi key
	setting.Persistent = false                     // Enable persistent search
	setting.Asynchronous = true                    // Enable asynchronous search
	setting.Timeout = 60 * time.Second             // Set timeout for HTTP requests
	setting.MaxIdleConnection = 10                 // Set maximum idle connections
	setting.KeepAlive = 60 * time.Second           // Set keep-alive duration
	setting.TLSHandshakeTimeout = 10 * time.Second // Set TLS handshake timeout

	client := serpapi.NewClient(setting)

  // search query overview (more fields available depending on search engine)
  parameter := map[string]string{
    "q":             "Coffee",
    "location":      "Austin, Texas, United States",
    "hl":            "en",
    "gl":            "us",
    "google_domain": "google.com",
    "safe":          "active",
    "start":         "10",
    "device":        "desktop",
  }

  // formated search results as a map
  // serpapi.com converts HTML -> JSON
  rsp, err := client.Search(parameter)

  if err != nil {
    panic(err)
  }
  fmt.Println(rsp)

  // raw search engine html as a String
  // serpapi.com acts a proxy to provive high throughputs, no search limit and more.
  raw_html, err := client.Html(parameter)
  if err != nil { 
    panic(err)
  }
  fmt.Println(raw_html)
}

Google search documentation.
More hands on examples are available below.

Full documentation on SerpApi.com

Library Github page

API health status

Location API

import (
	"fmt"
	"github.com/serpapi/serpapi-golang"
)

setting := serpapi.NewSerpApiClientSetting("<SERPAPI_KEY>") // Replace with your SerpApi secret key
client := serpapi.NewClient(setting)
locationList, err := client.Location("Austin", 5)

if err != nil {
  panic(err)
}
fmt.Println(locationList)

It prints the first 5 locations matching Austin (Texas, Texas, Rochester)

[map[canonical_name:Austin,TX,Texas,United States country_code:US google_id:200635 google_parent_id:21176 gps:[-97.7430608 30.267153]...

see: (test/location_test.go)

Search Archive API

This API allows retrieving previous search results.
To fetch earlier results from the search_id.

First, you need to run a search and save the search id.

// First, you need to run a search and save the search id.
auth := map[string]string{
  "engine":  "google",
  "api_key": "secret_api_key",
}
client := serpapi.NewClient(auth)
parameter := map[string]string{
  "q":        "Coffee",
  "location": "Portland"}

rsp, err := client.Search(parameter)

if err != nil {
  t.Error("unexpected error", err)
  return
}

// Now let's retrieve the previous search results from the archive.
searchID := rsp["search_metadata"].(map[string]interface{})["id"].(
