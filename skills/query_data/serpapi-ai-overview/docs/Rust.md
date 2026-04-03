# Rust

## 源URL

https://serpapi.com/integrations

## 描述

Easy integration with Rust. SerpApi provides APIs and integrations for multiple programming languages and AI tools, including Model Context Protocol (MCP).

## 内容

Code to integrate

- [](https://github.com/serpapi/serpapi-search-rust)`// [dependencies]
// serpapi-search-rust="0.1.0"
// tokio = { version = "1", features = ["full"] }

use serpapi_search_rust::serp_api_search::SerpApiSearch;
use std::collections::HashMap;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
  let mut params = HashMap::<String, String>::new();
  params.insert("q".to_string(), "Coffee".to_string());
  params.insert("location".to_string(), "Austin, Texas, United States".to_string());
  params.insert("hl".to_string(), "en".to_string());
  params.insert("gl".to_string(), "us".to_string());
  params.insert("google_domain".to_string(), "google.com".to_string());

  let search = SerpApiSearch::google(params, "secret_api_key".to_string());

  let results = search.json().await?;
  println!("results received");
  println!("--- JSON ---");
  println!(" - results: {}", results);

  print!("ok");
  Ok(())
}`

## SerpApi Search in Rust

[](https://github.com/serpapi/serpapi-search-rust/actions/workflows/ci.yml) [](https://crates.io/crates/serpapi-search-rust)

This Rust package enables to scrape and parse search results from Google, Bing, Baidu, Yandex, Yahoo, Ebay, Apple, Youtube, Naver, Home depot and more. It's powered by [SerpApi](https://serpapi.com/) which delivered a consistent JSON format accross search engines.
SerpApi.com enables to do localized search, leverage advanced search engine features and a lot more...
A completed documentation is available at [SerpApi](https://serpapi.com/).

To install in your rust application, update Cargo.toml

```text
serpapi-search-rust="0.1.0"
```

Basic application.

```text
use serpapi_search_rust::serp_api_search::SerpApiSearch;
use std::collections::HashMap;
use std::env;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // read secret api key from environment variable
    // To get the key simply copy/paste from https://serpapi.com/dashboard.
    let api_key = match env::var_os("API_KEY") {
        Some(v) => v.into_string().unwrap(),
        None => panic!("$API_KEY is not set"),
    };

    println!("let's search about coffee on google");
    let mut params = HashMap::<String, String>::new();
    params.insert("q".to_string(), "coffee".to_string());
    params.insert("location".to_string(), "Austin, TX, Texas, United States".to_string());

    // initialize the search engine
    let search = SerpApiSearch::google(params, api_key);

    // search returns a JSON as serde_json::Value which can be accessed like a HashMap.
    println!("waiting...");
    let results = search.json().await?;
    let organic_results = results["organic_results"].as_array().unwrap();
    println!("results received");
    println!("--- JSON ---");
    println!(" - number of organic results: {}", organic_results.len());
    println!(" - organic_results first result description: {}", results["organic_results"][0]["about_this_result"]["source"]["description"]);
    let places = results["local_results"]["places"].as_array().unwrap();
    println!("number of local_results: {}", places.len());
    println!(" - local_results first address: {}", places[0]["address"]);

    // search returns text
    println!("--- HTML search ---");
    let raw = search.html().await?;
    print!(" - raw HTML size {} bytes\n", raw.len());
    print!(" - async search completed with {}\n", results["search_parameters"]["engine"]);

    // // edit the location in the search
    // println!("--- JSON search with a different location ---");
    // params = HashMap::<String, String>::new();
    // params.insert("location".to_string(), "Destin, Florida, United States".to_string());
    // search = SerpApiSearch::google(params, api_key);
    // let results = search.json().await?;
    // println!(">> search_parameters: {}", results["search_parameters"]);
    // let places = results["local_results"]["places"].as_array().unwrap();
    // println!("number of local_results: {}\n", places.len());
    // println!("local_results first address: {}\n", places[0]["address"]);

    print!("ok");
    Ok(())
}
```

To run an example:

```text
cargo build --example google_search_example
```

file: (examples/google_search_example.rs)

The keyword google can be replaced by any supported search engine:

- google
- baidu
- bing
- duckduckgo
- yahoo
- yandex
- ebay
- youtube
- walmart
- home_depot
- apple_app_store
- naver

To run test.

```text
cargo test
```

For more information how to build a paramaters HashMap see [serpapi.com documentation](https://serpapi.com/search-api)

#### Technical features

- Dynamic JSON decoding using Serde JSON
- Asyncronous HTTP request handle method using tokio and reqwest
- Async tests using Tokio

#### TODO

- [ ] more test to close code coverage (each search engine)
- [ ] add more examples
- [ ] better documentation

#### Free Plan · 250 searches / month

### They trust us

You are in good company. Join them.

![Nvidia](SerpApi_Rust_Integration/image_1.svg)

![Shopify](SerpApi_Rust_Integration/image_2.svg)

![Perplexity](SerpApi_Rust_Integration/image_3.svg)

![Adobe](SerpApi_Rust_Integration/image_4.svg)

![Samsung](SerpApi_Rust_Integration/image_5.svg)

![KPMG](SerpApi_Rust_Integration/image_6.svg)

![Ahrefs](SerpApi_Rust_Integration/image_7.svg)

![Grubhub](SerpApi_Rust_Integration/image_8.svg)

![AI21 Labs](SerpApi_Rust_Integration/image_9.svg)

![United Nations](SerpApi_Rust_Integration/image_10.svg)

![Thomson Reuters](SerpApi_Rust_Integration/image_11.svg)

![Morgan Stanley](SerpApi_Rust_Integration/image_12.svg)

![BrightLocal](SerpApi_Rust_Integration/image_13.svg)

![Experian](SerpApi_Rust_Integration/image_14.svg)

![Uber](SerpApi_Rust_Integration/image_15.svg)

## 图片

![SerpApi home](SerpApi_Rust_Integration/image_1.png)

![SerpApi home](SerpApi_Rust_Integration/image_2.png)

![图片](SerpApi_Rust_Integration/image_3.svg)

![图片](SerpApi_Rust_Integration/image_4.svg)

![图片](SerpApi_Rust_Integration/image_5.svg)

![图片](SerpApi_Rust_Integration/image_6.svg)

![图片](SerpApi_Rust_Integration/image_7.svg)

![CI](SerpApi_Rust_Integration/image_8.svg)

![serpapi-search-rust](SerpApi_Rust_Integration/image_9.svg)

![Nvidia](SerpApi_Rust_Integration/image_10.svg)

![Shopify](SerpApi_Rust_Integration/image_11.svg)

![Perplexity](SerpApi_Rust_Integration/image_12.svg)

![Adobe](SerpApi_Rust_Integration/image_13.svg)

![Samsung](SerpApi_Rust_Integration/image_14.svg)

![KPMG](SerpApi_Rust_Integration/image_15.svg)

![Ahrefs](SerpApi_Rust_Integration/image_16.svg)

![Grubhub](SerpApi_Rust_Integration/image_17.svg)

![AI21 Labs](SerpApi_Rust_Integration/image_18.svg)

![United Nations](SerpApi_Rust_Integration/image_19.svg)

![Thomson Reuters](SerpApi_Rust_Integration/image_20.svg)

![Morgan Stanley](SerpApi_Rust_Integration/image_21.svg)

![BrightLocal](SerpApi_Rust_Integration/image_22.svg)

![Experian](SerpApi_Rust_Integration/image_23.svg)

![Uber](SerpApi_Rust_Integration/image_24.svg)

![图片](SerpApi_Rust_Integration/image_25.svg)

![图片](SerpApi_Rust_Integration/image_26.svg)

![图片](SerpApi_Rust_Integration/image_27.svg)

![图片](SerpApi_Rust_Integration/image_28.svg)

![图片](SerpApi_Rust_Integration/image_29.svg)

![图片](SerpApi_Rust_Integration/image_30.svg)

![图片](SerpApi_Rust_Integration/image_31.svg)

![图片](SerpApi_Rust_Integration/image_32.svg)

![图片](SerpApi_Rust_Integration/image_33.svg)

![图片](SerpApi_Rust_Integration/image_34.svg)

![图片](SerpApi_Rust_Integration/image_35.svg)

![图片](SerpApi_Rust_Integration/image_36.svg)

![SerpApi](SerpApi_Rust_Integration/image_37.svg)

## 图表

![SVG图表 1](SerpApi_Rust_Integration/svg_1.png)
*尺寸: 24x24px*
