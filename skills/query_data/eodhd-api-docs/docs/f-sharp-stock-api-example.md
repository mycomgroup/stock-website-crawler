---
id: "url-5935f319"
type: "api"
title: "F Sharp (F#) Stock API Example"
url: "https://eodhd.com/financial-apis/f-sharp-stock-api-example"
description: "It’s very easy to use our API with F# (F Sharp) language as well. We provide simple examples of using our API with F# (F Sharp) and we believe that it will help to start working with our API very quick."
source: ""
tags: []
crawl_time: "2026-03-18T03:07:38.964Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# F Sharp (F#) Stock API Example\n\nIt’s very easy to use our API with F# (F Sharp) language as well. We provide simple examples of using our API with F# (F Sharp) and we believe that it will help to start working with our API very quick.\n\n\n## Installation\n\nFirst, you should download f_sharp_bundle.zip. In this archive, you will find three files:\n\nThe two text files contain the F# (F-Sharp) code that downloads data from the EODHD API. The file Download.fs must be above Program.fs in the Visual Studio solution, as the order of files matters in F#, differently from other languages like C#.\n\nThe CSV file contains a list of tickers to be downloaded. It is an example of the kind of file that is read by the F# program.\n\nFor testing purposes, you can use this API Key:\n\nWorks with AAPL.US only.\n\n## Prerequisites\n\nThe user will have to install the packages Deedle and FSharp.Data from Nuget.\n\n## Code\n\nThe full code of Program.fs\n\nThe full code of Download.fs\n\n1. Use “DEMO” API key to test our data from a limited set of the tickers without registering:AAPL.US | TSLA.US | VTI.US | AMZN.US | BTC-USD | EUR-USDReal-Time Data and All of the APIs (except Bulk) are included without limitations on API calls.2. Register to get your free API key (limitated by 20 API calls per day) with access to:End-Of-Day Historical Data with only past year for any ticker and List of tickers per Exchange 3. To unlock your API key we recommend to choose subscription which covers your needs\n\nThanks for this code to Fernando Saldanha. Fernando Saldanha has a Ph.D. in Economics from Massachusetts Institute of Technology (1982). He worked many years in the U.S. and Brazilian financial markets and is now happily retired. His hobby is writing financial software with F#.\n\n## Code Examples\n\n```text\napi_token=demo\n```\n\n```text\nopen Deedle\n\n[<EntryPoint>]\nlet main argv =\n\nlet dropboxRoot = \"C:\\\\\" // or whenever your Dropbox folder is\n\n// File with list of tickers of stocks to be downloaded\nlet eODAssetsPath = dropboxRoot + @\"\\Dropbox\\EODData\\EOD.csv\"\n\n// Alternatively delete the 'let dropBoxRoot = ...' line and set the value of eODAssetsPath to the location where you saved EOD.csv.\n\n// Data stored in this folder\nlet storageDataPath = dropboxRoot + @\"\\Dropbox\\EODDAta\\\"\n\n// Tickers to be downloaded from EOD Historical Data\n// The CSV file in eODAssetsPath contains a column labeled Ticker with\n// the tickers of the stocks to be downloaded from EOD Historical Data\nlet eODTickers : string seq =\nFrame.ReadCsv(eODAssetsPath, hasHeaders=true, inferTypes=false)\n|> Frame.getCol \"Ticker\"\n|> Series.dropMissing\n|> Series.filterValues (fun x -> x <> \"\")\n|> Series.values\n\nSeq.iter (Download.downloadFromEOD storageDataPath) eODTickers\n\nprintfn \"%A\" argv\n0 // return an integer exit code\n```\n\n```json\n[<RequireQualifiedAccess>]\nmodule Download\n\nopen FSharp.Data\n\nopen Deedle\n\n/// Downloads data from EOD Historical Data for one stock.\nlet downloadFromEOD (storageDataPath: string) (symbol: string) : unit =\n\n// Token for the EOD Historical Data service\nlet apiToken = \"99999999999999\" // insert your EOD token here\n\nlet endStr = \"?api_token=\" + apiToken + \"&period=d&order=d\"\n\nprintfn \"Downloading symbol %s\" symbol\n\nlet url = @\"http://eodhd.com/api/eod/\" + symbol + endStr\n\nlet df =\nHttp.RequestString(url)\n|> DeedleFuncs.Frame.stringToTSDF\n\nlet path = storageDataPath + symbol + \".csv\"\n\nFrameExtensions.SaveCsv(df, path, includeRowKeys=true, keyNames=[\"Date\"])\n```\n\n\n## Related APIs\n\n- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)\n- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)\n- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)\n- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)\n- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)\n- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)\n- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)\n- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)\n- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)\n- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)"
  rawContent: ""
  suggestedFilename: "f-sharp-stock-api-example"
---

# F Sharp (F#) Stock API Example

## 源URL

https://eodhd.com/financial-apis/f-sharp-stock-api-example

## 描述

It’s very easy to use our API with F# (F Sharp) language as well. We provide simple examples of using our API with F# (F Sharp) and we believe that it will help to start working with our API very quick.

## 文档正文

It’s very easy to use our API with F# (F Sharp) language as well. We provide simple examples of using our API with F# (F Sharp) and we believe that it will help to start working with our API very quick.

## Installation

First, you should download f_sharp_bundle.zip. In this archive, you will find three files:

The two text files contain the F# (F-Sharp) code that downloads data from the EODHD API. The file Download.fs must be above Program.fs in the Visual Studio solution, as the order of files matters in F#, differently from other languages like C#.

The CSV file contains a list of tickers to be downloaded. It is an example of the kind of file that is read by the F# program.

For testing purposes, you can use this API Key:

Works with AAPL.US only.

## Prerequisites

The user will have to install the packages Deedle and FSharp.Data from Nuget.

## Code

The full code of Program.fs

The full code of Download.fs

1. Use “DEMO” API key to test our data from a limited set of the tickers without registering:AAPL.US | TSLA.US | VTI.US | AMZN.US | BTC-USD | EUR-USDReal-Time Data and All of the APIs (except Bulk) are included without limitations on API calls.2. Register to get your free API key (limitated by 20 API calls per day) with access to:End-Of-Day Historical Data with only past year for any ticker and List of tickers per Exchange 3. To unlock your API key we recommend to choose subscription which covers your needs

Thanks for this code to Fernando Saldanha. Fernando Saldanha has a Ph.D. in Economics from Massachusetts Institute of Technology (1982). He worked many years in the U.S. and Brazilian financial markets and is now happily retired. His hobby is writing financial software with F#.

## Code Examples

```text
api_token=demo
```

```text
open Deedle

[<EntryPoint>]
let main argv =

let dropboxRoot = "C:\\" // or whenever your Dropbox folder is

// File with list of tickers of stocks to be downloaded
let eODAssetsPath = dropboxRoot + @"\Dropbox\EODData\EOD.csv"

// Alternatively delete the 'let dropBoxRoot = ...' line and set the value of eODAssetsPath to the location where you saved EOD.csv.

// Data stored in this folder
let storageDataPath = dropboxRoot + @"\Dropbox\EODDAta\"

// Tickers to be downloaded from EOD Historical Data
// The CSV file in eODAssetsPath contains a column labeled Ticker with
// the tickers of the stocks to be downloaded from EOD Historical Data
let eODTickers : string seq =
Frame.ReadCsv(eODAssetsPath, hasHeaders=true, inferTypes=false)
|> Frame.getCol "Ticker"
|> Series.dropMissing
|> Series.filterValues (fun x -> x <> "")
|> Series.values

Seq.iter (Download.downloadFromEOD storageDataPath) eODTickers

printfn "%A" argv
0 // return an integer exit code
```

```json
[<RequireQualifiedAccess>]
module Download

open FSharp.Data

open Deedle

/// Downloads data from EOD Historical Data for one stock.
let downloadFromEOD (storageDataPath: string) (symbol: string) : unit =

// Token for the EOD Historical Data service
let apiToken = "99999999999999" // insert your EOD token here

let endStr = "?api_token=" + apiToken + "&period=d&order=d"

printfn "Downloading symbol %s" symbol

let url = @"http://eodhd.com/api/eod/" + symbol + endStr

let df =
Http.RequestString(url)
|> DeedleFuncs.Frame.stringToTSDF

let path = storageDataPath + symbol + ".csv"

FrameExtensions.SaveCsv(df, path, includeRowKeys=true, keyNames=["Date"])
```

## Related APIs

- [Bulk for Live OHLCV Stock Prices API (US Exchanges Only)](https://eodhd.com/financial-apis/bulk-for-live-ohlcv-stock-prices-api-us-exchanges-only)
- [Live v2 for US Stocks: Extended Quotes (2025)](https://eodhd.com/financial-apis/live-v2-for-us-stocks-extended-quotes-2025)
- [End-Of-Day Historical Stock Market Data API](https://eodhd.com/financial-apis/api-for-historical-data-and-volumes)
- [Tick Data API: US Stock Market](https://eodhd.com/financial-apis/us-stock-market-tick-data-api)
- [Real-Time Data API via Websockets: US Stocks, Forex pairs, Digital Currencies](https://eodhd.com/financial-apis/new-real-time-data-api-websockets)
- [Intraday Historical Stock Price Data API](https://eodhd.com/financial-apis/intraday-historical-data-api)
- [Live OHLCV Stock Prices API: US & Global Stocks, Currencies](https://eodhd.com/financial-apis/live-ohlcv-stocks-api)
- [Corporate Actions: Splits and Dividends API](https://eodhd.com/financial-apis/api-splits-dividends)
- [Stock Market Screener API](https://eodhd.com/financial-apis/stock-market-screener-api)
- [Delisted Stock Companies Data](https://eodhd.com/financial-apis/delisted-stock-companies-data)
