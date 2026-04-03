---
id: "url-5166e509"
type: "api"
title: "PHP"
url: "https://serpapi.com/integrations/php"
description: "This PHP API is meant to scrape and parse Google, Bing or Baidu results using SerpApi.\n\nThe full documentation is available here.\n\nThe following services are provided:\n\nSerpApi provides a script builder to get you started quickly.\n\nPhp 7+ must be already installed and composer dependency management tool."
source: ""
tags: []
crawl_time: "2026-03-18T14:31:03.630Z"
metadata:
  endpoint: "https://serpapi.com/search"
  engine: "google"
  method: "GET"
  parameters: []
  responseStructure: []
  examples: []
  importantNotes: []
  rawContent: "Documentation\n\nIntegrations\n\nDocumentation\n\nIntegrations\n\nStart integration with your preferred language.\n\nCode to integrate\n\nrequire 'path/to/google-search-results.php';\nrequire 'path/to/restclient.php';\n\n$query = [\n \"q\" => \"Coffee\",\n \"location\" => \"Austin, Texas, United States\",\n \"hl\" => \"en\",\n \"gl\" => \"us\",\n \"google_domain\" => \"google.com\",\n];\n\n$search = new GoogleSearch('secret_api_key');\n$result = $search->get_json($query);\n\nrequire 'path/to/google-search-results.php';\nrequire 'path/to/restclient.php';\n\n$query = [\n \"q\" => \"Coffee\",\n \"location\" => \"Austin, Texas, United States\",\n \"hl\" => \"en\",\n \"gl\" => \"us\",\n \"google_domain\" => \"google.com\",\n];\n\n$search = new GoogleSearch('secret_api_key');\n$result = $search->get_json($query);\n\nGoogle Search Results in PHP\n\nThis PHP API is meant to scrape and parse Google, Bing or Baidu results using SerpApi.\n\nThe full documentation is available here.\n\nThe following services are provided:\n\nLocation API\n\nSearch Archive API\n\nAccount API\n\nSerpApi provides a script builder to get you started quickly.\n\nInstallation\n\nPhp 7+ must be already installed and composer dependency management tool.\n\nPackage available from packagist.\n\nQuick start\n\nif you're using composer, you can add this package (link to packagist).\n\n$ composer require serpapi/google-search-results-php\n\nThen you need to load the dependency in your script.\n\n<?php\nrequire __DIR__ . '/vendor/autoload.php';\n ?>\n\nif not, you must clone this repository and link the class.\n\nrequire 'path/to/google-search-results';\nrequire 'path/to/restclient';\n\nGet \"your secret key\" from https://serpapi.com/dashboard\n\nThen you can start coding something like:\n\n$client = new GoogleSearch(\"your secret key\");\n$query = [\"q\" => \"coffee\",\"location\"=>\"Austin,Texas\"];\n$response = $client->get_json($query);\nprint_r($response);\n\nThis example runs a search about \"coffee\" using your secret api key.\n\nThe SerpApi service (backend)\n\nsearches on Google using the query: q = \"coffee\"\n\nparses the messy HTML responses\n\nreturn a standardizes JSON response\nThe Php class GoogleSearch\n\nFormat the request to SerpApi server\n\nExecute GET http request\n\nParse JSON into Ruby Hash using JSON standard library provided by Ruby\nEt voila..\n\nAlternatively, you can search:\n\nBing using BingSearch class\n\nBaidu using BaiduSearch class\n\nEbay using EbaySearch class\n\nYahoo using YahooSearch class\n\nYandex using YandexSearch class\n\nWalmart using WalmartSearch class\n\nYoutube using YoutubeSearch class\n\nHomeDepot using HomeDepotSearch class\n\nApple App Store using AppleAppStoreSearch class\n\nNaver using NaverSearch class\n\nSee the playground to generate your code.\nhttps://serpapi.com/playground\n\nHow to set SERP API key\n\nSearch API capability\n\nLocation API\n\nSearch Archive API\n\nAccount API\n\nSearch Google Images\n\nGeneric SerpApiClient\n\nExample by specification\n\nComposer example\n\nHow to set SERP API key\n\nThe SerpApi api_key can be set globally using a singleton pattern.\n\n$client = new GoogleSearch();\n$client->set_serp_api_key(\"Your Private Key\");\n\n$client = new GoogleSearch(\"Your Private Key\");\n\nSearch API capability\n\n$query = [\n  \"q\" =>  \"query\",\n  \"google_domain\" =>  \"Google Domain\", \n  \"location\" =>  \"Location Requested\", \n  \"device\" =>  \"device\",\n  \"hl\" =>  \"Google UI Language\",\n  \"gl\" =>  \"Google Country\",\n  \"safe\" =>  \"Safe Search Flag\",\n  \"start\" =>  \"Pagination Offset\",\n  \"serp_api_key\" =>  \"Your SERP API Key\",\n  \"tbm\" => \"nws|isch|shop\"\n  \"tbs\" => \"custom to be search criteria\"\n  \"async\" => true|false # allow async \n];\n\n$client = new GoogleSearch(\"private key\");\n\n$html_results = $client->get_html($query);\n$json_results = $client->get_json($query);\n\nLocation API\n\n$client = new GoogleSearch(getenv(\"API_KEY\"));\n$location_list = $client->get_location('Austin', 3);\nprint_r($location_list);\n\nit prints the first 3 location matching Austin (Texas, Texas, Rochester)\n\n[{:id=>\"585069bdee19ad271e9bc072\",\n  :google_id=>200635,\n  :google_parent_id=>21176,\n  :name=>\"Austin, TX\",\n  :canonical_name=>\"Austin,TX,Texas,United States\",\n  :country_code=>\"US\",\n  :target_type=>\"DMA Region\",\n  :reach=>5560000,\n  :gps=>[-97.7430608, 30.267153],\n  :keys=>[\"austin\", \"tx\", \"texas\", \"united\", \"states\"]},\n  ...]\n\nSearch Archive API\n\nLet's run a search to get a search_id.\n\n$client = new GoogleSearch(getenv(\"API_KEY\"));\n$result = $client->get_json($this->QUERY);\n$search_id = $result->search_metadata->id\n\nNow let's retrieve the previous search from the archive.\n\n$archived_result = $client->get_search_archive($search_id);\nprint_r($archived_result);\n\nit prints the search from the archive.\n\nAccount API\n\n$client = new GoogleSearch($this->API_KEY);\n$info = $client->get_account();\nprint_r($info);\n\nit prints your account information.\n\nSearch Google Images\n\n$client = new GoogleSearch(getenv(\"API_KEY\"));\n$data = $client->get_json([\n  'q' => \"Coffee\", \n  'tbm' => 'isch'\n]);\n\nforeach($data->images_results as $image_result) {\n  print_r($image_result->original);\n  //to download the image:\n  // `wget #{image_result[:original]}`\n}\n\nthis code prints all the images links,\nand download image if you un-comment the line with wget (linux/osx tool to download image).\n\nExample by specification\n\nThe code described above is tested in the file test.php and example.php.\nTo run the test locally.\n\nexport API_KEY='your secret key'\nmake test example\n\nComposer example\n\nsee: https://github.com/serpapi/google-search-results-php/example_composer/\n\nTo run the code.\n\ngit clone https://github.com/serpapi/google-search-results-php\n\ncd google-search-results-php/example_composer/\n\nmake API_KEY= all\n\n2.0\n\nCode refractoring SearchResult -> Search\nAdd walmart and youtube search engine\n\nCode refractoring SearchResult -> Search\n\nAdd walmart and youtube search engine\n\n1.2.0\n\nAdd more search engine\n\nAdd more search engine\n\n1.0\n\nFirst stable version\n\nFirst stable version\n\nSerpApi supports all the major search engines. Google has the more advance support with all the major services available: Images, News, Shopping and more.. To enable a type of search, the field tbm (to be matched) must be set to:\n\nisch: Google Images API.\n\nnws: Google News API.\n\nshop: Google Shopping API."
  suggestedFilename: "integrations_php-api"
---

# PHP

## 源URL

https://serpapi.com/integrations/php

## 描述

This PHP API is meant to scrape and parse Google, Bing or Baidu results using SerpApi.

The full documentation is available here.

The following services are provided:

SerpApi provides a script builder to get you started quickly.

Php 7+ must be already installed and composer dependency management tool.

## API 端点

**Method**: `GET`
**Endpoint**: `https://serpapi.com/search`

## 文档正文

This PHP API is meant to scrape and parse Google, Bing or Baidu results using SerpApi.

The full documentation is available here.

The following services are provided:

SerpApi provides a script builder to get you started quickly.

Php 7+ must be already installed and composer dependency management tool.

## API 端点

**Method:** `GET`
**Endpoint:** `https://serpapi.com/search`

Documentation

Integrations

Documentation

Integrations

Start integration with your preferred language.

Code to integrate

require 'path/to/google-search-results.php';
require 'path/to/restclient.php';

$query = [
 "q" => "Coffee",
 "location" => "Austin, Texas, United States",
 "hl" => "en",
 "gl" => "us",
 "google_domain" => "google.com",
];

$search = new GoogleSearch('secret_api_key');
$result = $search->get_json($query);

require 'path/to/google-search-results.php';
require 'path/to/restclient.php';

$query = [
 "q" => "Coffee",
 "location" => "Austin, Texas, United States",
 "hl" => "en",
 "gl" => "us",
 "google_domain" => "google.com",
];

$search = new GoogleSearch('secret_api_key');
$result = $search->get_json($query);

Google Search Results in PHP

This PHP API is meant to scrape and parse Google, Bing or Baidu results using SerpApi.

The full documentation is available here.

The following services are provided:

Location API

Search Archive API

Account API

SerpApi provides a script builder to get you started quickly.

Installation

Php 7+ must be already installed and composer dependency management tool.

Package available from packagist.

Quick start

if you're using composer, you can add this package (link to packagist).

$ composer require serpapi/google-search-results-php

Then you need to load the dependency in your script.

<?php
require __DIR__ . '/vendor/autoload.php';
 ?>

if not, you must clone this repository and link the class.

require 'path/to/google-search-results';
require 'path/to/restclient';

Get "your secret key" from https://serpapi.com/dashboard

Then you can start coding something like:

$client = new GoogleSearch("your secret key");
$query = ["q" => "coffee","location"=>"Austin,Texas"];
$response = $client->get_json($query);
print_r($response);

This example runs a search about "coffee" using your secret api key.

The SerpApi service (backend)

searches on Google using the query: q = "coffee"

parses the messy HTML responses

return a standardizes JSON response
The Php class GoogleSearch

Format the request to SerpApi server

Execute GET http request

Parse JSON into Ruby Hash using JSON standard library provided by Ruby
Et voila..

Alternatively, you can search:

Bing using BingSearch class

Baidu using BaiduSearch class

Ebay using EbaySearch class

Yahoo using YahooSearch class

Yandex using YandexSearch class

Walmart using WalmartSearch class

Youtube using YoutubeSearch class

HomeDepot using HomeDepotSearch class

Apple App Store using AppleAppStoreSearch class

Naver using NaverSearch class

See the playground to generate your code.
https://serpapi.com/playground

How to set SERP API key

Search API capability

Location API

Search Archive API

Account API

Search Google Images

Generic SerpApiClient

Example by specification

Composer example

How to set SERP API key

The SerpApi api_key can be set globally using a singleton pattern.

$client = new GoogleSearch();
$client->set_serp_api_key("Your Private Key");

$client = new GoogleSearch("Your Private Key");

Search API capability

$query = [
  "q" =>  "query",
  "google_domain" =>  "Google Domain", 
  "location" =>  "Location Requested", 
  "device" =>  "device",
  "hl" =>  "Google UI Language",
  "gl" =>  "Google Country",
  "safe" =>  "Safe Search Flag",
  "start" =>  "Pagination Offset",
  "serp_api_key" =>  "Your SERP API Key",
  "tbm" => "nws|isch|shop"
  "tbs" => "custom to be search criteria"
  "async" => true|false # allow async 
];

$client = new GoogleSearch("private key");

$html_results = $client->get_html($query);
$json_results = $client->get_json($query);

Location API

$client = new GoogleSearch(getenv("API_KEY"));
$location_list = $client->get_location('Austin', 3);
print_r($location_list);

it prints the first 3 location matching Austin (Texas, Texas, Rochester)

[{:id=>"585069bdee19ad271e9bc072",
  :google_id=>200635,
  :google_parent_id=>21176,
  :name=>"Austin, TX",
  :canonical_name=>"Austin,TX,Texas,United States",
  :country_code=>"US",
  :target_type=>"DMA Region",
  :reach=>5560000,
  :gps=>[-97.7430608, 30.267153],
  :keys=>["austin", "tx", "texas", "united", "states"]},
  ...]

Search Archive API

Let's run a search to get a search_id.

$client = new GoogleSearch(getenv("API_KEY"));
$result = $client->get_json($this->QUERY);
$search_id = $result->search_metadata->id

Now let's retrieve the previous search from the archive.

$archived_result = $client->get_search_archive($search_id);
print_r($archived_result);

it prints the search from the archive.

Account API

$client = new GoogleSearch($this->API_KEY);
$info = $client->get_account();
print_r($info);

it prints your account information.

Search Google Images

$client = new GoogleSearch(getenv("API_KEY"));
$data = $client->get_json([
  'q' => "Coffee", 
  'tbm' => 'isch'
]);

foreach($data->images_results as $image_result) {
  print_r($image_result->original);
  //to download the image:
  // `wget #{image_result[:original]}`
}

t
