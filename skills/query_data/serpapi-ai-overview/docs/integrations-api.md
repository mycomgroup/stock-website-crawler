---
id: "url-35efe620"
type: "api"
title: "Integrations"
url: "https://serpapi.com/integrations"
description: "Easy integration. SerpApi provides APIs and integrations for multiple programming languages and AI tools, including Model Context Protocol (MCP)."
source: ""
tags: []
crawl_time: "2026-03-18T05:58:42.115Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples:
    - {"title":"Example 9","description":"","requestParams":{},"responseJson":"{\n  \"name\": \"search\",\n  \"arguments\": {\n    \"params\": {\n      \"q\": \"Coffee\",\n      \"location\": \"Austin, Texas, United States\",\n      \"engine\": \"google\"\n    }\n  }\n}"}
  importantNotes: []
  rawContent: "Documentation\n\nIntegrations\n\nDocumentation\n\nIntegrations\n\nIntegrations\n\nStart integration with your preferred language or tool.\n\nRuby\n                \n                \n              \n              \n                  require \"serpapi\" \n\nclient = SerpApi::Client.new(\n  q: \"Coffee\",\n  location: \"Austin, Texas, United States\",\n  engine: \"google\",\n  api_key: \"secret_api_key\"\n)\n\nresults = client.search\n\nrequire \"serpapi\" \n\nclient = SerpApi::Client.new(\n  q: \"Coffee\",\n  location: \"Austin, Texas, United States\",\n  engine: \"google\",\n  api_key: \"secret_api_key\"\n)\n\nresults = client.search\n\nrequire \"serpapi\" \n\nclient = SerpApi::Client.new(\n  q: \"Coffee\",\n  location: \"Austin, Texas, United States\",\n  engine: \"google\",\n  api_key: \"secret_api_key\"\n)\n\nresults = client.search\n\nPython\n                \n                \n              \n              \n                  from serpapi import GoogleSearch\n\nparams = {\n  \"q\": \"Coffee\",\n  \"location\": \"Austin, Texas, United States\",\n  \"engine\": \"google\",\n  \"api_key\": \"secret_api_key\"\n}\n\nsearch = GoogleSearch(params)\nresults = search.get_dict()\n\nfrom serpapi import GoogleSearch\n\nparams = {\n  \"q\": \"Coffee\",\n  \"location\": \"Austin, Texas, United States\",\n  \"engine\": \"google\",\n  \"api_key\": \"secret_api_key\"\n}\n\nsearch = GoogleSearch(params)\nresults = search.get_dict()\n\nfrom serpapi import GoogleSearch\n\nparams = {\n  \"q\": \"Coffee\",\n  \"location\": \"Austin, Texas, United States\",\n  \"engine\": \"google\",\n  \"api_key\": \"secret_api_key\"\n}\n\nsearch = GoogleSearch(params)\nresults = search.get_dict()\n\nJavaScript\n                \n                \n              \n              \n                  const { getJson } = require(\"serpapi\");\n\ngetJson({\n  q: \"Coffee\",\n  location: \"Austin, Texas, United States\",\n  engine: \"google\",\n  api_key: \"secret_api_key\"\n}, (json) => {\n  console.log(json);\n});\n\nconst { getJson } = require(\"serpapi\");\n\ngetJson({\n  q: \"Coffee\",\n  location: \"Austin, Texas, United States\",\n  engine: \"google\",\n  api_key: \"secret_api_key\"\n}, (json) => {\n  console.log(json);\n});\n\nconst { getJson } = require(\"serpapi\");\n\ngetJson({\n  q: \"Coffee\",\n  location: \"Austin, Texas, United States\",\n  engine: \"google\",\n  api_key: \"secret_api_key\"\n}, (json) => {\n  console.log(json);\n});\n\nGolang\n                \n                \n              \n              \n                  package main\n\nimport (\n  \"github.com/serpapi/serpapi-golang\"\n  \"os\"\n  \"fmt\"\n  \"log\"\n)\n\nfunc main(){\n  setting := serpapi.NewSerpApiClientSetting(os.Getenv(\"SERPAPI_KEY\"))\n  setting.Engine = \"google\"\n  client := serpapi.NewClient(setting)\n  parameter := map[string]string{\n    \"q\": \"Coffee\",\n    \"location\": \"Austin, Texas, United States\",\n  }\n  results, err := client.Search(parameter)\n  if err != nil {\n    log.Fatal(err)\n  }\n  fmt.Println(results)\n}\n\npackage main\n\nimport (\n  \"github.com/serpapi/serpapi-golang\"\n  \"os\"\n  \"fmt\"\n  \"log\"\n)\n\nfunc main(){\n  setting := serpapi.NewSerpApiClientSetting(os.Getenv(\"SERPAPI_KEY\"))\n  setting.Engine = \"google\"\n  client := serpapi.NewClient(setting)\n  parameter := map[string]string{\n    \"q\": \"Coffee\",\n    \"location\": \"Austin, Texas, United States\",\n  }\n  results, err := client.Search(parameter)\n  if err != nil {\n    log.Fatal(err)\n  }\n  fmt.Println(results)\n}\n\npackage main\n\nimport (\n  \"github.com/serpapi/serpapi-golang\"\n  \"os\"\n  \"fmt\"\n  \"log\"\n)\n\nfunc main(){\n  setting := serpapi.NewSerpApiClientSetting(os.Getenv(\"SERPAPI_KEY\"))\n  setting.Engine = \"google\"\n  client := serpapi.NewClient(setting)\n  parameter := map[string]string{\n    \"q\": \"Coffee\",\n    \"location\": \"Austin, Texas, United States\",\n  }\n  results, err := client.Search(parameter)\n  if err != nil {\n    log.Fatal(err)\n  }\n  fmt.Println(results)\n}\n\nPHP\n                \n                \n              \n              \n                  require 'path/to/google-search-results.php';\nrequire 'path/to/restclient.php';\n\n$query = [\n \"q\" => \"Coffee\",\n \"location\" => \"Austin, Texas, United States\",\n \"engine\" => \"google\",\n];\n\n$search = new GoogleSearch('secret_api_key');\n$result = $search->get_json($query);\n\nrequire 'path/to/google-search-results.php';\nrequire 'path/to/restclient.php';\n\n$query = [\n \"q\" => \"Coffee\",\n \"location\" => \"Austin, Texas, United States\",\n \"engine\" => \"google\",\n];\n\n$search = new GoogleSearch('secret_api_key');\n$result = $search->get_json($query);\n\nrequire 'path/to/google-search-results.php';\nrequire 'path/to/restclient.php';\n\n$query = [\n \"q\" => \"Coffee\",\n \"location\" => \"Austin, Texas, United States\",\n \"engine\" => \"google\",\n];\n\n$search = new GoogleSearch('secret_api_key');\n$result = $search->get_json($query);\n\nJava\n                \n                \n              \n              \n                  Map<String, String> parameter = new HashMap<>();\n\nparameter.put(\"q\", \"Coffee\");\nparameter.put(\"location\", \"Austin, Texas, United States\");\nparameter.put(\"engine\", \"google\");\nparameter.put(\"api_key\", \"secret_api_key\");\n\nGoogleSearch search = new GoogleSearch(parameter);\n\ntry {\n  JsonObject results = search.getJson();\n} catch (SerpApiSearchException ex) {\n  System.out.println(\"Exception:\");\n  System.out.println(ex.toString());\n}\n\nMap<String, String> parameter = new HashMap<>();\n\nparameter.put(\"q\", \"Coffee\");\nparameter.put(\"location\", \"Austin, Texas, United States\");\nparameter.put(\"engine\", \"google\");\nparameter.put(\"api_key\", \"secret_api_key\");\n\nGoogleSearch search = new GoogleSearch(parameter);\n\ntry {\n  JsonObject results = search.getJson();\n} catch (SerpApiSearchException ex) {\n  System.out.println(\"Exception:\");\n  System.out.println(ex.toString());\n}\n\nMap<String, String> parameter = new HashMap<>();\n\nparameter.put(\"q\", \"Coffee\");\nparameter.put(\"location\", \"Austin, Texas, United States\");\nparameter.put(\"engine\", \"google\");\nparameter.put(\"api_key\", \"secret_api_key\");\n\nGoogleSearch search = new GoogleSearch(parameter);\n\ntry {\n  JsonObject results = search.getJson();\n} catch (SerpApiSearchException ex) {\n  System.out.println(\"Exception:\");\n  System.out.println(ex.toString());\n}\n\nRust\n                \n                \n              \n              \n                  use serpapi_search_rust::serp_api_search::SerpApiSearch;\nuse std::collections::HashMap;\n\n#[tokio::main]\nasync fn main() -> Result<(), Box<dyn std::error::Error>> {\n  let mut params = HashMap::<String, String>::new();\n  params.insert(\"q\".to_string(), \"Coffee\".to_string());\n  params.insert(\"location\".to_string(), \"Austin, Texas, United States\".to_string());\n  params.insert(\"engine\".to_string(), \"google\".to_string());\n\n  let search = SerpApiSearch::google(params, \"secret_api_key\".to_string());\n\n  let results = search.json().await?;\n  println!(\"results received\");\n  println!(\"--- JSON ---\");\n  println!(\" - results: {}\", results);\n\n  print!(\"ok\");\n  Ok(())\n}\n\nuse serpapi_search_rust::serp_api_search::SerpApiSearch;\nuse std::collections::HashMap;\n\n#[tokio::main]\nasync fn main() -> Result<(), Box<dyn std::error::Error>> {\n  let mut params = HashMap::<String, String>::new();\n  params.insert(\"q\".to_string(), \"Coffee\".to_string());\n  params.insert(\"location\".to_string(), \"Austin, Texas, United States\".to_string());\n  params.insert(\"engine\".to_string(), \"google\".to_string());\n\n  let search = SerpApiSearch::google(params, \"secret_api_key\".to_string());\n\n  let results = search.json().await?;\n  println!(\"results received\");\n  println!(\"--- JSON ---\");\n  println!(\" - results: {}\", results);\n\n  print!(\"ok\");\n  Ok(())\n}\n\nuse serpapi_search_rust::serp_api_search::SerpApiSearch;\nuse std::collections::HashMap;\n\n#[tokio::main]\nasync fn main() -> Result<(), Box<dyn std::error::Error>> {\n  let mut params = HashMap::<String, String>::new();\n  params.insert(\"q\".to_string(), \"Coffee\".to_string());\n  params.insert(\"location\".to_string(), \"Austin, Texas, United States\".to_string());\n  params.insert(\"engine\".to_string(), \"google\".to_string());\n\n  let search = SerpApiSearch::google(params, \"secret_api_key\".to_string());\n\n  let results = search.json().await?;\n  println!(\"results received\");\n  println!(\"--- JSON ---\");\n  println!(\" - results: {}\", results);\n\n  print!(\"ok\");\n  Ok(())\n}\n\n.Net\n                \n                \n              \n              \n                  using System;\nusing System.Collections;\nusing SerpApi;\nusing Newtonsoft.Json.Linq;\n\nString apiKey = \"secret_api_key\";\nHashtable ht = new Hashtable();\nht.Add(\"q\", \"Coffee\");\nht.Add(\"location\", \"Austin, Texas, United States\");\nht.Add(\"engine\", \"google\");\n\ntry\n{\n  GoogleSearch search = new GoogleSearch(ht, apiKey);\n  JObject data = search.GetJson();\n  JArray results = (JArray)data[\"organic_results\"];\n  foreach (JObject result in results)\n  {\n    Console.WriteLine(\"Found: \" + result[\"title\"]);\n  }\n}\ncatch (SerpApiSearchException ex)\n{\n  Console.WriteLine(\"Exception:\");\n  Console.WriteLine(ex.ToString());\n}\n\nusing System;\nusing System.Collections;\nusing SerpApi;\nusing Newtonsoft.Json.Linq;\n\nString apiKey = \"secret_api_key\";\nHashtable ht = new Hashtable();\nht.Add(\"q\", \"Coffee\");\nht.Add(\"location\", \"Austin, Texas, United States\");\nht.Add(\"engine\", \"google\");\n\ntry\n{\n  GoogleSearch search = new GoogleSearch(ht, apiKey);\n  JObject data = search.GetJson();\n  JArray results = (JArray)data[\"organic_results\"];\n  foreach (JObject result in results)\n  {\n    Console.WriteLine(\"Found: \" + result[\"title\"]);\n  }\n}\ncatch (SerpApiSearchException ex)\n{\n  Console.WriteLine(\"Exception:\");\n  Console.WriteLine(ex.ToString());\n}\n\nusing System;\nusing System.Collections;\nusing SerpApi;\nusing Newtonsoft.Json.Linq;\n\nString apiKey = \"secret_api_key\";\nHashtable ht = new Hashtable();\nht.Add(\"q\", \"Coffee\");\nht.Add(\"location\", \"Austin, Texas, United States\");\nht.Add(\"engine\", \"google\");\n\ntry\n{\n  GoogleSearch search = new GoogleSearch(ht, apiKey);\n  JObject data = search.GetJson();\n  JArray results = (JArray)data[\"organic_results\"];\n  foreach (JObject result in results)\n  {\n    Console.WriteLine(\"Found: \" + result[\"title\"]);\n  }\n}\ncatch (SerpApiSearchException ex)\n{\n  Console.WriteLine(\"Exception:\");\n  Console.WriteLine(ex.ToString());\n}\n\nMCP\n                \n                \n              \n              \n      {\n  \"name\": \"search\",\n  \"arguments\": {\n    \"params\": {\n      \"q\": \"Coffee\",\n      \"location\": \"Austin, Texas, United States\",\n      \"engine\": \"google\"\n    }\n  }\n}\n\n{\n  \"name\": \"search\",\n  \"arguments\": {\n    \"params\": {\n      \"q\": \"Coffee\",\n      \"location\": \"Austin, Texas, United States\",\n      \"engine\": \"google\"\n    }\n  }\n}\n\nSwift\n                \n                \n              \n              \n                  In developmentComing soon!\n\nIn developmentComing soon!\n\nC++\n                \n                \n              \n              \n                  In developmentComing soon!\n\nIn developmentComing soon!\n\nFree Plan · 250 searches / month\n\nThey trust us\n\nYou are in good company. Join them.\n\nDocumentation\n\nGoogle Search API\n\nGoogle Light Search API\n\nGoogle AI Mode API\n\nGoogle AI Overview API\n\nGoogle Ads Transparency API\n\nGoogle Autocomplete API\n\nGoogle Events API\n\nGoogle Finance API\n\nGoogle Flights API\n\nGoogle Forums API\n\nGoogle Hotels API\n\nGoogle Images API\n\nGoogle Images Light API\n\nGoogle Immersive Product API\n\nGoogle Jobs API\n\nGoogle Lens API\n\nGoogle Light Fast API\n\nGoogle Local API\n\nGoogle Local Services API\n\nGoogle Maps API\n\nGoogle Maps Reviews API\n\nGoogle News API\n\nGoogle News Light API\n\nGoogle Patents API\n\nGoogle Play Store API\n\nGoogle Related Questions API\n\nGoogle Reverse Image API\n\nGoogle Scholar API\n\nGoogle Shopping API\n\nGoogle Shopping Light API\n\nGoogle Short Videos API\n\nGoogle Travel Explore API\n\nGoogle Trends API\n\nGoogle Videos API\n\nGoogle Videos Light API\n\nAmazon Search API\n\nAmazon Product API\n\nApple App Store API\n\nBaidu Search API\n\nBing Search API\n\nBing Copilot API\n\nBing Images API\n\nDuckDuckGo Search API\n\nDuckDuckGo Light API\n\neBay Search API\n\nFacebook Profile API\n\nNaver Search API\n\nOpenTable Reviews API\n\nThe Home Depot Search API\n\nTripadvisor Search API\n\nWalmart Search API\n\nYahoo! Search API\n\nYandex Search API\n\nYelp Search API\n\nYouTube Search API\n\nStatus and Error Codes\n\nDocumentation\n\nIntegrations\n\nSerpApi, LLC\n\n5540 N Lamar Blvd #12"
  suggestedFilename: "integrations-api"
---

# Integrations

## 源URL

https://serpapi.com/integrations

## 描述

Easy integration. SerpApi provides APIs and integrations for multiple programming languages and AI tools, including Model Context Protocol (MCP).

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

Easy integration. SerpApi provides APIs and integrations for multiple programming languages and AI tools, including Model Context Protocol (MCP).

## API 端点

**Method:** `GET`
**Endpoint:** `https://serpapi.com/search`

Documentation

Integrations

Documentation

Integrations

Integrations

Start integration with your preferred language or tool.

Ruby
                
                
              
              
                  require "serpapi" 

client = SerpApi::Client.new(
  q: "Coffee",
  location: "Austin, Texas, United States",
  engine: "google",
  api_key: "secret_api_key"
)

results = client.search

require "serpapi" 

client = SerpApi::Client.new(
  q: "Coffee",
  location: "Austin, Texas, United States",
  engine: "google",
  api_key: "secret_api_key"
)

results = client.search

require "serpapi" 

client = SerpApi::Client.new(
  q: "Coffee",
  location: "Austin, Texas, United States",
  engine: "google",
  api_key: "secret_api_key"
)

results = client.search

Python
                
                
              
              
                  from serpapi import GoogleSearch

params = {
  "q": "Coffee",
  "location": "Austin, Texas, United States",
  "engine": "google",
  "api_key": "secret_api_key"
}

search = GoogleSearch(params)
results = search.get_dict()

from serpapi import GoogleSearch

params = {
  "q": "Coffee",
  "location": "Austin, Texas, United States",
  "engine": "google",
  "api_key": "secret_api_key"
}

search = GoogleSearch(params)
results = search.get_dict()

from serpapi import GoogleSearch

params = {
  "q": "Coffee",
  "location": "Austin, Texas, United States",
  "engine": "google",
  "api_key": "secret_api_key"
}

search = GoogleSearch(params)
results = search.get_dict()

JavaScript
                
                
              
              
                  const { getJson } = require("serpapi");

getJson({
  q: "Coffee",
  location: "Austin, Texas, United States",
  engine: "google",
  api_key: "secret_api_key"
}, (json) => {
  console.log(json);
});

const { getJson } = require("serpapi");

getJson({
  q: "Coffee",
  location: "Austin, Texas, United States",
  engine: "google",
  api_key: "secret_api_key"
}, (json) => {
  console.log(json);
});

const { getJson } = require("serpapi");

getJson({
  q: "Coffee",
  location: "Austin, Texas, United States",
  engine: "google",
  api_key: "secret_api_key"
}, (json) => {
  console.log(json);
});

Golang
                
                
              
              
                  package main

import (
  "github.com/serpapi/serpapi-golang"
  "os"
  "fmt"
  "log"
)

func main(){
  setting := serpapi.NewSerpApiClientSetting(os.Getenv("SERPAPI_KEY"))
  setting.Engine = "google"
  client := serpapi.NewClient(setting)
  parameter := map[string]string{
    "q": "Coffee",
    "location": "Austin, Texas, United States",
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
  setting := serpapi.NewSerpApiClientSetting(os.Getenv("SERPAPI_KEY"))
  setting.Engine = "google"
  client := serpapi.NewClient(setting)
  parameter := map[string]string{
    "q": "Coffee",
    "location": "Austin, Texas, United States",
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
  setting := serpapi.NewSerpApiClientSetting(os.Getenv("SERPAPI_KEY"))
  setting.Engine = "google"
  client := serpapi.NewClient(setting)
  parameter := map[string]string{
    "q": "Coffee",
    "location": "Austin, Texas, United States",
  }
  results, err := client.Search(parameter)
  if err != nil {
    log.Fatal(err)
  }
  fmt.Println(results)
}

PHP
                
                
              
              
                  require 'path/to/google-search-results.php';
require 'path/to/restclient.php';

$query = [
 "q" => "Coffee",
 "location" => "Austin, Texas, United States",
 "engine" => "google",
];

$search = new GoogleSearch('secret_api_key');
$result = $search->get_json($query);

require 'path/to/google-search-results.php';
require 'path/to/restclient.php';

$query = [
 "q" => "Coffee",
 "location" => "Austin, Texas, United States",
 "engine" => "google",
];

$search = new GoogleSearch('secret_api_key');
$result = $search->get_json($query);

require 'path/to/google-search-results.php';
require 'path/to/restclient.php';

$query = [
 "q" => "Coffee",
 "location" => "Austin, Texas, United States",
 "engine" => "google",
];

$search = new GoogleSearch('secret_api_key');
$result = $search->get_json($query);

Java
                
                
              
              
                  Map<String, String> parameter = new HashMap<>();

parameter.put("q", "Coffee");
parameter.put("location", "Austin, Texas, United States");
parameter.put("engine", "google");
parameter.put("api_key", "secret_api_key");

GoogleSearch search = new GoogleSearch(parameter);

try {
  JsonObject results = search.getJson();
} catch (SerpApiSearchException ex) {
  Syst
