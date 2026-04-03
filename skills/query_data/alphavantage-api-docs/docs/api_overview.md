# Alpha Vantage API Documentation

## 源URL

https://www.alphavantage.co/documentation/

## 概述

Our stock APIs © are grouped into eight categories: (1) Core Time Series Stock Data APIs, (2) US Options Data APIs, (3) Alpha Intelligence™, (4) Fundamental Data, (5) Physical and Crypto Currencies (e.g., Bitcoin), (6) Commodities, (7) Economic Indicators, and (8) Technical Indicators - also outlined here. Examples in this documentation are for demo purposes. Claim your free API key today to explore our full API offerings!

---

# API 详细文档

## TIME_SERIES_INTRADAY Trending Premium [Premium, Trending]

**函数名**: `TIME_SERIES_INTRADAY`

### 描述

This API returns current and 20+ years of historical intraday OHLCV time series of the equity specified, covering pre-market and post-market hours where applicable (e.g., 4:00am to 8:00pm Eastern Time for the US market). You can query both raw (as-traded) and split/dividend-adjusted intraday data from this endpoint. The OHLCV data is sometimes called "candles" in finance literature.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=TIME_SERIES_INTRADAY |
| `symbol` | The name of the equity of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `adjusted` | By default, adjusted=true and the output time series is adjusted by historical split and dividend events. Set adjusted=false to query raw (as-traded) intraday values. |
| `extended_hours` | By default, extended_hours=true and the output time series will include both the regular trading hours and the extended (pre-market and post-market) trading hours (4:00am to 8:00pm Eastern Time for the US market). Set extended_hours=false to query regular trading hours (9:30am to 4:00pm US Eastern Time) only. |
| `month` | By default, this parameter is not set and the API will return intraday data for the most recent days of trading. You can use the month parameter (in YYYY-MM format) to query a specific month in history. For example, month=2009-01. Any month in the last 20+ years since 2000-01 (January 2000) is supported. |
| `outputsize` | By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns trailing 30 days of the most recent intraday data if the month parameter (see above) is not specified, or the full intraday data for a specific month in history if the month parameter is specified. The "compact" option is recommended if you would like to reduce the data size of each API call. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the intraday time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime intraday time series. Setting the parameter to entitlement=delayed will return 15-minute delayed intraday time series. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&month=2009-01&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## TIME_SERIES_DAILY

**函数名**: `TIME_SERIES_DAILY`

### 描述

This API returns raw (as-traded) daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the global equity specified, covering 20+ years of historical data. The OHLCV data is sometimes called "candles" in finance literature. If you are also interested in split/dividend-adjusted data, please use the Daily Adjusted API, which covers adjusted close values and historical split and dividend events.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=TIME_SERIES_DAILY |
| `symbol` | The name of the equity of your choice. For example: symbol=IBM |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `outputsize` | By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points; full returns the full-length time series of 20+ years of historical data. The "compact" option is recommended if you would like to reduce the data size of each API call. The "compact" outputsize is available to both free and premium API keys. The "full" outputsize is available to premium keys. Please subscribe to any premium membership plan to unlock the outputsize=full capability. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo
```

**https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=demo**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSCO.LON&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SHOP.TRT&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GPV.TRV&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MBG.DEX&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=RELIANCE.BSE&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=600104.SHH&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=000002.SHZ&outputsize=full&apikey=demo
```

**https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo&datatype=csv**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## TIME_SERIES_DAILY_ADJUSTED Trending Premium [Premium, Trending]

**函数名**: `TIME_SERIES_DAILY_ADJUSTED`

### 描述

This API returns raw (as-traded) daily open/high/low/close/volume values, adjusted close values, and historical split/dividend events of the global equity specified, covering 20+ years of historical data. The OHLCV data is sometimes called "candles" in finance literature.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=TIME_SERIES_DAILY_ADJUSTED |
| `symbol` | The name of the equity of your choice. For example: symbol=IBM |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `outputsize` | By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points; full returns the full-length time series of 20+ years of historical data. The "compact" option is recommended if you would like to reduce the data size of each API call. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=TSCO.LON&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=SHOP.TRT&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=GPV.TRV&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MBG.DEX&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=RELIANCE.BSE&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=600104.SHH&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=000002.SHZ&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## TIME_SERIES_WEEKLY

**函数名**: `TIME_SERIES_WEEKLY`

### 描述

This API returns weekly time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly volume) of the global equity specified, covering 20+ years of historical data.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=TIME_SERIES_WEEKLY |
| `symbol` | The name of the equity of your choice. For example: symbol=IBM |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the weekly time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=demo
```

**https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=TSCO.LON&apikey=demo**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=TSCO.LON&apikey=demo
```

**https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=demo&datatype=csv**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=IBM&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## TIME_SERIES_WEEKLY_ADJUSTED

**函数名**: `TIME_SERIES_WEEKLY_ADJUSTED`

### 描述

This API returns weekly adjusted time series (last trading day of each week, weekly open, weekly high, weekly low, weekly close, weekly adjusted close, weekly volume, weekly dividend) of the global equity specified, covering 20+ years of historical data.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=TIME_SERIES_WEEKLY_ADJUSTED |
| `symbol` | The name of the equity of your choice. For example: symbol=IBM |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the weekly time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey=demo
```

**https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=TSCO.LON&apikey=demo**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=TSCO.LON&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## TIME_SERIES_MONTHLY

**函数名**: `TIME_SERIES_MONTHLY`

### 描述

This API returns monthly time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly volume) of the global equity specified, covering 20+ years of historical data.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=TIME_SERIES_MONTHLY |
| `symbol` | The name of the equity of your choice. For example: symbol=IBM |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the monthly time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo
```

**https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=TSCO.LON&apikey=demo**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=TSCO.LON&apikey=demo
```

**https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo&datatype=csv**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## TIME_SERIES_MONTHLY_ADJUSTED

**函数名**: `TIME_SERIES_MONTHLY_ADJUSTED`

### 描述

This API returns monthly adjusted time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly adjusted close, monthly volume, monthly dividend) of the equity specified, covering 20+ years of historical data.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=TIME_SERIES_MONTHLY_ADJUSTED |
| `symbol` | The name of the equity of your choice. For example: symbol=IBM |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the monthly time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=demo
```

**https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=TSCO.LON&apikey=demo**
```text
https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=TSCO.LON&apikey=demo
```

```text
https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Quote Endpoint Trending [Trending]

**函数名**: `Q`

### 描述

This endpoint returns the latest price and volume information for a ticker of your choice. You can specify one ticker per API request.

If you would like to query a large universe of tickers in bulk, you may want to try out our Realtime Bulk Quotes API, which accepts up to 100 tickers per API request.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The API function of your choice. |
| `symbol` | The symbol of the global ticker of your choice. For example: symbol=IBM. |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the quote data in JSON format; csv returns the quote data as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime US market data. Setting the parameter to entitlement=delayed will return 15-minute delayed US market data. |

### 示例 URL

**https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo
```

**https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=300135.SHZ&apikey=demo**
```text
https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=300135.SHZ&apikey=demo
```

**https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo&datatype=csv**
```text
https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Realtime Bulk Quotes Premium [Premium]

**函数名**: `R`

### 描述

This API returns realtime quotes for US-traded symbols in bulk, accepting up to 100 symbols per API request and covering both regular and extended (pre-market and post-market) trading hours. You can use this endpoint as a high-throughput alternative to the Global Quote API, which accepts one symbol per API request.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=REALTIME_BULK_QUOTES |
| `symbol` | Up to 100 symbols separated by comma. For example: symbol=MSFT,AAPL,IBM. If more than 100 symbols are provided, only the first 100 symbols will be honored as part of the API input. |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the search results in JSON format; csv returns the search results as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=REALTIME_BULK_QUOTES&symbol=MSFT,AAPL,IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=REALTIME_BULK_QUOTES&symbol=MSFT,AAPL,IBM&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=REALTIME_BULK_QUOTES&symbol=MSFT,AAPL,IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=REALTIME_BULK_QUOTES&symbol=MSFT,AAPL,IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=REALTIME_BULK_QUOTES&symbol=MSFT,AAPL,IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=REALTIME_BULK_QUOTES&symbol=MSFT,AAPL,IBM&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Search Endpoint Utility [Utility]

**函数名**: `S`

### 描述

Looking for some specific symbols or companies? Trying to build an auto-complete search box similar to the one below?

We've got you covered! The Search Endpoint returns the best-matching symbols and market information based on keywords of your choice. The search results also contain match scores that provide you with the full flexibility to develop your own search and filtering logic.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The API function of your choice. In this case, function=SYMBOL_SEARCH |
| `keywords` | A text string of your choice. For example: keywords=microsoft. |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the search results in JSON format; csv returns the search results as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo**
```text
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo
```

**https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tencent&apikey=demo**
```text
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tencent&apikey=demo
```

**https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=demo**
```text
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=demo
```

**https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=SAIC&apikey=demo**
```text
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=SAIC&apikey=demo
```

**https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=demo&datatype=csv**
```text
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Global Market Open & Close Status Utility [Utility]

**函数名**: `G`

### 描述

This endpoint returns the current market status (open vs. closed) of major trading venues for equities, forex, and cryptocurrencies around the world.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The API function of your choice. In this case, function=MARKET_STATUS |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=MARKET_STATUS&apikey=demo**
```text
https://www.alphavantage.co/query?function=MARKET_STATUS&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=MARKET_STATUS&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=MARKET_STATUS&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Realtime Options Trending Premium [Premium, Trending]

**函数名**: `R`

### 描述

This API returns realtime US options data with full market coverage. Option chains are sorted by expiration dates in chronological order. Within the same expiration date, contracts are sorted by strike prices from low to high.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=REALTIME_OPTIONS |
| `symbol` | The name of the equity of your choice. For example: symbol=IBM |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `require_greeks` | Enable greeks & implied volatility (IV) fields. By default, require_greeks=false. Set require_greeks=true to enable greeks & IVs in the API response. |
| `contract` | The US options contract ID you would like to specify. By default, the contract parameter is not set and the entire option chain for a given symbol will be returned. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the options data in JSON format; csv returns the data as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol=IBM&apikey=demo
```

```text
https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol=IBM&require_greeks=true&apikey=demo
```

```text
https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol=IBM&require_greeks=true&contract=IBM270115C00390000&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=REALTIME_OPTIONS&symbol=IBM&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Historical Options Trending Premium [Premium, Trending]

**函数名**: `H`

### 描述

This API returns the full historical options chain for a specific symbol on a specific date, covering 15+ years of history. Implied volatility (IV) and common Greeks (e.g., delta, gamma, theta, vega, rho) are also returned. Option chains are sorted by expiration dates in chronological order. Within the same expiration date, contracts are sorted by strike prices from low to high.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=HISTORICAL_OPTIONS |
| `symbol` | The name of the equity of your choice. For example: symbol=IBM |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `date` | By default, the date parameter is not set and the API will return data for the previous trading session. Any date later than 2008-01-01 is accepted. For example, date=2017-11-15. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the options data in JSON format; csv returns the data as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey=demo
```

```text
https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&date=2017-11-15&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Market News & Sentiment Trending [Trending]

**函数名**: `M`

### 描述

Looking for market news data to train your LLM models or to augment your trading strategy? You have just found it. This API returns live and historical market news & sentiment data from a large & growing selection of premier news outlets around the world, covering stocks, cryptocurrencies, forex, and a wide range of topics such as fiscal policy, mergers & acquisitions, IPOs, etc. This API, combined with our core stock API, fundamental data, and technical indicator APIs, can provide you with a 360-degree view of the financial market and the broader economy.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=NEWS_SENTIMENT |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `tickers` | The stock/crypto/forex symbols of your choice. For example: tickers=IBM will filter for articles that mention the IBM ticker; tickers=COIN,CRYPTO:BTC,FOREX:USD will filter for articles that simultaneously mention Coinbase (COIN), Bitcoin (CRYPTO:BTC), and US Dollar (FOREX:USD) in their content. |
| `topics` | The news topics of your choice. For example: topics=technology will filter for articles that write about the technology sector; topics=technology,ipo will filter for articles that simultaneously cover technology and IPO in their content. Below is the full list of supported topics: |
| `time_from` | The time range of the news articles you are targeting, in YYYYMMDDTHHMM format. For example: time_from=20220410T0130. If time_from is specified but time_to is missing, the API will return articles published between the time_from value and the current time. |
| `sort` | By default, sort=LATEST and the API will return the latest articles first. You can also set sort=EARLIEST or sort=RELEVANCE based on your use case. |
| `limit` | By default, limit=50 and the API will return up to 50 matching results. You can also set limit=1000 to output up to 1000 results. |

### 示例 URL

**https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo**
```text
https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo
```

```text
https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=COIN,CRYPTO:BTC,FOREX:USD&time_from=20220410T0130&limit=1000&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Earnings Call Transcript Trending [Trending]

**函数名**: `E`

### 描述

This API returns the earnings call transcript for a given company in a specific quarter, covering over 15 years of history and enriched with LLM-based sentiment signals.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=EARNINGS_CALL_TRANSCRIPT |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=IBM. |
| `quarter` | Fiscal quarter in YYYYQM format. For example: quarter=2024Q1. Any quarter since 2010Q1 is supported. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol=IBM&quarter=2024Q1&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol=IBM&quarter=2024Q1&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol=IBM&quarter=2024Q1&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol=IBM&quarter=2024Q1&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=EARNINGS_CALL_TRANSCRIPT&symbol=IBM&quarter=2024Q1&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Top Gainers, Losers, and Most Actively Traded Tickers (US Market)

**函数名**: `T`

### 描述

This endpoint returns the top 20 gainers, losers, and the most active traded tickers in the US market.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The API function of your choice. In this case, function=TOP_GAINERS_LOSERS |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=demo**
```text
https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Insider Transactions Trending [Trending]

**函数名**: `I`

### 描述

This API returns the latest and historical insider transactions made by key stakeholders (e.g., founders, executives, board members, etc.) of a specific company.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=INSIDER_TRANSACTIONS |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=IBM. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=INSIDER_TRANSACTIONS&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=INSIDER_TRANSACTIONS&symbol=IBM&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=INSIDER_TRANSACTIONS&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=INSIDER_TRANSACTIONS&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=INSIDER_TRANSACTIONS&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=INSIDER_TRANSACTIONS&symbol=IBM&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Institutional Holdings

**函数名**: `I`

### 描述

This API returns the institutional ownership and holdings information for an equity of interest.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=INSTITUTIONAL_HOLDINGS |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=IBM. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=INSTITUTIONAL_HOLDINGS&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=INSTITUTIONAL_HOLDINGS&symbol=IBM&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=INSTITUTIONAL_HOLDINGS&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=INSTITUTIONAL_HOLDINGS&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=INSTITUTIONAL_HOLDINGS&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=INSTITUTIONAL_HOLDINGS&symbol=IBM&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Advanced Analytics (Fixed Window)

**函数名**: `A`

### 描述

This endpoint returns a rich set of advanced analytics metrics (e.g., total return, variance, auto-correlation, etc.) for a given time series over a fixed temporal window.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=ANALYTICS_FIXED_WINDOW |
| `SYMBOLS` | A list of symbols for the calculation. It can be a comma separated list of symbols as a string. Free API keys can specify up to 5 symbols per API request. Premium API keys can specify up to 50 symbols per API request. |
| `RANGE` | This is the date range for the series being requested. By default, the date range is the full set of data for the equity history. This can be further modified by the LIMIT variable. |
| `INTERVAL` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, DAILY, WEEKLY, MONTHLY. |
| `CALCULATIONS` | A comma separated list of the analytics metrics you would like to calculate: |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `OHLC` | This allows you to choose which open, high, low, or close field the calculation will be performed on. By default, OHLC=close. Valid values for these fields are open, high, low, close. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=ANALYTICS_FIXED_WINDOW&SYMBOLS=AAPL,MSFT,IBM&RANGE=2023-07-01&RANGE=2023-08-31&INTERVAL=DAILY&OHLC=close&CALCULATIONS=MEAN,STDDEV,CORRELATION&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://alphavantageapi.co/timeseries/analytics?SYMBOLS=AAPL,MSFT,IBM&RANGE=2023-07-01&RANGE=2023-08-31&INTERVAL=DAILY&OHLC=close&CALCULATIONS=MEAN,STDDEV,CORRELATION&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://alphavantageapi.co/timeseries/analytics?SYMBOLS=AAPL,MSFT,IBM&RANGE=2023-07-01&RANGE=2023-08-31&INTERVAL=DAILY&OHLC=close&CALCULATIONS=MEAN,STDDEV,CORRELATION&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://alphavantageapi.co/timeseries/analytics?SYMBOLS=AAPL,MSFT,IBM&RANGE=2023-07-01&RANGE=2023-08-31&INTERVAL=DAILY&OHLC=close&CALCULATIONS=MEAN,STDDEV,CORRELATION&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://alphavantageapi.co/timeseries/analytics?SYMBOLS=AAPL,MSFT,IBM&RANGE=2023-07-01&RANGE=2023-08-31&INTERVAL=DAILY&OHLC=close&CALCULATIONS=MEAN,STDDEV,CORRELATION&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Advanced Analytics (Sliding Window) Trending [Trending]

**函数名**: `A`

### 描述

This endpoint returns a rich set of advanced analytics metrics (e.g., total return, variance, auto-correlation, etc.) for a given time series over sliding time windows. For example, we can calculate a moving variance over 5 years with a window of 100 points to see how the variance changes over time.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=ANALYTICS_SLIDING_WINDOW |
| `SYMBOLS` | A list of symbols for the calculation. It can be a comma separated list of symbols as a string. Free API keys can specify up to 5 symbols per API request. Premium API keys can specify up to 50 symbols per API request. |
| `RANGE` | This is the date range for the series being requested. By default, the date range is the full set of data for the equity history. This can be further modified by the LIMIT variable. |
| `INTERVAL` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, DAILY, WEEKLY, MONTHLY. |
| `WINDOW_SIZE` | An integer representing the size of the moving window. A hard lower boundary of 10 has been set though it is recommended to make this window larger to make sure the running calculations are statistically significant. |
| `CALCULATIONS` | A comma separated list of the analytics metrics you would like to calculate. Free API keys can specify 1 metric to be calculated per API request. Premium API keys can specify multiple metrics to be calculated simultaneously per API request. |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `OHLC` | This allows you to choose which open, high, low, or close field the calculation will be performed on. By default, OHLC=close. Valid values for these fields are open, high, low, close. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=ANALYTICS_SLIDING_WINDOW&SYMBOLS=AAPL,IBM&RANGE=2month&INTERVAL=DAILY&OHLC=close&WINDOW_SIZE=20&CALCULATIONS=MEAN,STDDEV(annualized=True)&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://alphavantageapi.co/timeseries/running_analytics?SYMBOLS=AAPL,IBM&RANGE=2month&INTERVAL=DAILY&OHLC=close&WINDOW_SIZE=20&CALCULATIONS=MEAN,STDDEV(annualized=True)&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://alphavantageapi.co/timeseries/running_analytics?SYMBOLS=AAPL,IBM&RANGE=2month&INTERVAL=DAILY&OHLC=close&WINDOW_SIZE=20&CALCULATIONS=MEAN,STDDEV(annualized=True)&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://alphavantageapi.co/timeseries/running_analytics?SYMBOLS=AAPL,IBM&RANGE=2month&INTERVAL=DAILY&OHLC=close&WINDOW_SIZE=20&CALCULATIONS=MEAN,STDDEV(annualized=True)&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://alphavantageapi.co/timeseries/running_analytics?SYMBOLS=AAPL,IBM&RANGE=2month&INTERVAL=DAILY&OHLC=close&WINDOW_SIZE=20&CALCULATIONS=MEAN,STDDEV(annualized=True)&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Company Overview Trending [Trending]

**函数名**: `C`

### 描述

This API returns the company information, financial ratios, and other key metrics for the equity specified. Data is generally refreshed on the same day a company reports its latest earnings and financials.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=OVERVIEW |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=IBM. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## ETF Profile & Holdings

**函数名**: `ETF`

### 描述

This API returns key ETF metrics (e.g., net assets, expense ratio, and turnover), along with the corresponding ETF holdings / constituents with allocation by asset types and sectors.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=ETF_PROFILE |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=QQQ. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=ETF_PROFILE&symbol=QQQ&apikey=demo**
```text
https://www.alphavantage.co/query?function=ETF_PROFILE&symbol=QQQ&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=ETF_PROFILE&symbol=QQQ&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=ETF_PROFILE&symbol=QQQ&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=ETF_PROFILE&symbol=QQQ&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=ETF_PROFILE&symbol=QQQ&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Corporate Action - Dividends

**函数名**: `C`

### 描述

This API returns historical and future (declared) dividend distributions.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=DIVIDENDS |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=IBM. |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the options data in JSON format; csv returns the data as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=DIVIDENDS&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=DIVIDENDS&symbol=IBM&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=DIVIDENDS&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=DIVIDENDS&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=DIVIDENDS&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=DIVIDENDS&symbol=IBM&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Corporate Action - Splits

**函数名**: `C`

### 描述

This API returns historical split events.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=SPLITS |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=IBM. |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the options data in JSON format; csv returns the data as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=SPLITS&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=SPLITS&symbol=IBM&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=SPLITS&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=SPLITS&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=SPLITS&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=SPLITS&symbol=IBM&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## INCOME_STATEMENT

**函数名**: `INCOME_STATEMENT`

### 描述

This API returns the annual and quarterly income statements for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on the same day a company reports its latest earnings and financials.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=INCOME_STATEMENT |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=IBM. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## BALANCE_SHEET

**函数名**: `BALANCE_SHEET`

### 描述

This API returns the annual and quarterly balance sheets for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on the same day a company reports its latest earnings and financials.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=BALANCE_SHEET |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=IBM. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## CASH_FLOW

**函数名**: `CASH_FLOW`

### 描述

This API returns the annual and quarterly cash flow for the company of interest, with normalized fields mapped to GAAP and IFRS taxonomies of the SEC. Data is generally refreshed on the same day a company reports its latest earnings and financials.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=CASH_FLOW |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=IBM. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## SHARES_OUTSTANDING

**函数名**: `SHARES_OUTSTANDING`

### 描述

This API returns the quarterly numbers of shares outstanding for the company of interest, with both diluted and basic shares outstanding values returned. Data is generally refreshed on the same day a company reports its latest earnings and financials.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=SHARES_OUTSTANDING |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=MSFT. |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the options data in JSON format; csv returns the data as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=SHARES_OUTSTANDING&symbol=MSFT&apikey=demo**
```text
https://www.alphavantage.co/query?function=SHARES_OUTSTANDING&symbol=MSFT&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=SHARES_OUTSTANDING&symbol=MSFT&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=SHARES_OUTSTANDING&symbol=MSFT&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=SHARES_OUTSTANDING&symbol=MSFT&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=SHARES_OUTSTANDING&symbol=MSFT&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Earnings History

**函数名**: `E`

### 描述

This API returns the annual and quarterly earnings (EPS) for the company of interest. Quarterly data also includes analyst estimates and surprise metrics.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=EARNINGS |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=IBM. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Earnings Estimates Trending [Trending]

**函数名**: `E`

### 描述

This API returns the annual and quarterly EPS and revenue estimates for the company of interest, along with analyst count and revision history.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=EARNINGS_ESTIMATES |
| `symbol` | The symbol of the ticker of your choice. For example: symbol=IBM. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=EARNINGS_ESTIMATES&symbol=IBM&apikey=demo**
```text
https://www.alphavantage.co/query?function=EARNINGS_ESTIMATES&symbol=IBM&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=EARNINGS_ESTIMATES&symbol=IBM&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=EARNINGS_ESTIMATES&symbol=IBM&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=EARNINGS_ESTIMATES&symbol=IBM&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=EARNINGS_ESTIMATES&symbol=IBM&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Listing & Delisting Status

**函数名**: `L`

### 描述

This API returns a list of active or delisted US stocks and ETFs, either as of the latest trading day or at a specific time in history. The endpoint is positioned to facilitate equity research on asset lifecycle and survivorship.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The API function of your choice. In this case, function=LISTING_STATUS |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `date` | If no date is set, the API endpoint will return a list of active or delisted symbols as of the latest trading day. If a date is set, the API endpoint will "travel back" in time and return a list of active or delisted symbols on that particular date in history. Any YYYY-MM-DD date later than 2010-01-01 is supported. For example, date=2013-08-03 |
| `state` | By default, state=active and the API will return a list of actively traded stocks and ETFs. Set state=delisted to query a list of delisted assets. |

### 示例 URL

**https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo**
```text
https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo
```

```text
https://www.alphavantage.co/query?function=LISTING_STATUS&date=2014-07-10&state=delisted&apikey=demo
```

### 代码示例

#### Python

```python
import csv
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
CSV_URL = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo'

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        print(row)
```

#### Text

```text
const {StringStream} = require("scramjet");
const request = require("request");

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
request.get("https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo")
    .pipe(new StringStream())
    .CSVParse()                                   // parse CSV output into row objects
    .consume(object => console.log("Row:", object))
    .then(() => console.log("success"));
```

#### Php

```php
<?php

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$data = file_get_contents("https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo");
$rows = explode("\n",$data);
$s = array();
foreach($rows as $row) {
    $s[] = str_getcsv($row);
    print_r($s);
}
```

#### Csharp

```csharp
using CsvHelper;
using System;
using System.Globalization;
using System.IO;
using System.Net;

// Compatible with any recent version of .NET Framework or .Net Core

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo";

            Uri queryUri = new Uri(QUERY_URL);

            // print the output
            // This example uses the fine nuget package CsvHelper (https://www.nuget.org/packages/CsvHelper/)

            CultureInfo culture = CultureInfo.CreateSpecificCulture("en-US"); ;
            using (WebClient client = new WebClient())
            {
                using (MemoryStream stream = new MemoryStream(client.DownloadDataTaskAsync(queryUri).Result))
                {
                    stream.Position = 0;

                    using (StreamReader reader = new StreamReader(stream))
                    {
                        using (CsvReader csv = new CsvReader(reader, CultureInfo.InvariantCulture))
                        {
                            csv.Read();
                            csv.ReadHeader();
                            Console.WriteLine(string.Join("\t", csv.HeaderRecord));
                            while (csv.Read())
                            {
                                Console.WriteLine(string.Join("\t", csv.Parser.Record));
                            }
                        }
                    }
                }
            }
        }
    }
}
```

---

## Earnings Calendar

**函数名**: `E`

### 描述

This API returns a list of company earnings expected in the next 3, 6, or 12 months.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The API function of your choice. In this case, function=EARNINGS_CALENDAR |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `symbol` | By default, no symbol will be set for this API. When no symbol is set, the API endpoint will return the full list of company earnings scheduled. If a symbol is set, the API endpoint will return the expected earnings for that specific symbol. For example, symbol=IBM |
| `horizon` | By default, horizon=3month and the API will return a list of expected company earnings in the next 3 months. You may set horizon=6month or horizon=12month to query the earnings scheduled for the next 6 months or 12 months, respectively. |

### 示例 URL

**https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey=demo**
```text
https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey=demo
```

**https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol=IBM&horizon=12month&apikey=demo**
```text
https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol=IBM&horizon=12month&apikey=demo
```

### 代码示例

#### Python

```python
import csv
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
CSV_URL = 'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey=demo'

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        print(row)
```

#### Text

```text
const {StringStream} = require("scramjet");
const request = require("request");

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
request.get("https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey=demo")
    .pipe(new StringStream())
    .CSVParse()                                   // parse CSV output into row objects
    .consume(object => console.log("Row:", object))
    .then(() => console.log("success"));
```

#### Php

```php
<?php

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$data = file_get_contents("https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey=demo");
$rows = explode("\n",$data);
$s = array();
foreach($rows as $row) {
    $s[] = str_getcsv($row);
    print_r($s);
}
```

#### Csharp

```csharp
using CsvHelper;
using System;
using System.Globalization;
using System.IO;
using System.Net;

// Compatible with any recent version of .NET Framework or .Net Core

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey=demo";

            Uri queryUri = new Uri(QUERY_URL);

            // print the output
            // This example uses the fine nuget package CsvHelper (https://www.nuget.org/packages/CsvHelper/)

            CultureInfo culture = CultureInfo.CreateSpecificCulture("en-US"); ;
            using (WebClient client = new WebClient())
            {
                using (MemoryStream stream = new MemoryStream(client.DownloadDataTaskAsync(queryUri).Result))
                {
                    stream.Position = 0;

                    using (StreamReader reader = new StreamReader(stream))
                    {
                        using (CsvReader csv = new CsvReader(reader, CultureInfo.InvariantCulture))
                        {
                            csv.Read();
                            csv.ReadHeader();
                            Console.WriteLine(string.Join("\t", csv.HeaderRecord));
                            while (csv.Read())
                            {
                                Console.WriteLine(string.Join("\t", csv.Parser.Record));
                            }
                        }
                    }
                }
            }
        }
    }
}
```

---

## IPO Calendar

**函数名**: `IPO`

### 描述

This API returns a list of IPOs expected in the next 3 months.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The API function of your choice. In this case, function=IPO_CALENDAR |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=IPO_CALENDAR&apikey=demo**
```text
https://www.alphavantage.co/query?function=IPO_CALENDAR&apikey=demo
```

### 代码示例

#### Python

```python
import csv
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
CSV_URL = 'https://www.alphavantage.co/query?function=IPO_CALENDAR&apikey=demo'

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    for row in my_list:
        print(row)
```

#### Text

```text
const {StringStream} = require("scramjet");
const request = require("request");

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
request.get("https://www.alphavantage.co/query?function=IPO_CALENDAR&apikey=demo")
    .pipe(new StringStream())
    .CSVParse()                                   // parse CSV output into row objects
    .consume(object => console.log("Row:", object))
    .then(() => console.log("success"));
```

#### Php

```php
<?php

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$data = file_get_contents("https://www.alphavantage.co/query?function=IPO_CALENDAR&apikey=demo");
$rows = explode("\n",$data);
$s = array();
foreach($rows as $row) {
    $s[] = str_getcsv($row);
    print_r($s);
}
```

#### Csharp

```csharp
using CsvHelper;
using System;
using System.Globalization;
using System.IO;
using System.Net;

// Compatible with any recent version of .NET Framework or .Net Core

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=IPO_CALENDAR&apikey=demo";

            Uri queryUri = new Uri(QUERY_URL);

            // print the output
            // This example uses the fine nuget package CsvHelper (https://www.nuget.org/packages/CsvHelper/)

            CultureInfo culture = CultureInfo.CreateSpecificCulture("en-US"); ;
            using (WebClient client = new WebClient())
            {
                using (MemoryStream stream = new MemoryStream(client.DownloadDataTaskAsync(queryUri).Result))
                {
                    stream.Position = 0;

                    using (StreamReader reader = new StreamReader(stream))
                    {
                        using (CsvReader csv = new CsvReader(reader, CultureInfo.InvariantCulture))
                        {
                            csv.Read();
                            csv.ReadHeader();
                            Console.WriteLine(string.Join("\t", csv.HeaderRecord));
                            while (csv.Read())
                            {
                                Console.WriteLine(string.Join("\t", csv.Parser.Record));
                            }
                        }
                    }
                }
            }
        }
    }
}
```

---

## CURRENCY_EXCHANGE_RATE Trending [Trending]

**函数名**: `CURRENCY_EXCHANGE_RATE`

### 描述

This API returns the realtime exchange rate for a pair of fiat currencies (e.g., USD, EUR, CNY, etc.).

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=CURRENCY_EXCHANGE_RATE |
| `from_currency` | The currency you would like to get the exchange rate for. It can either be a  physical currency or cryptocurrency. For example: from_currency=USD or from_currency=BTC. |
| `to_currency` | The destination currency for the exchange rate. It can either be a  physical currency or cryptocurrency. For example: to_currency=USD or to_currency=BTC. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=demo
```

```text
https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=EUR&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## FX_INTRADAY Premium Trending [Premium, Trending]

**函数名**: `FX_INTRADAY`

### 描述

This API returns intraday time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=FX_INTRADAY |
| `from_symbol` | A three-letter symbol from the  forex currency list. For example: from_symbol=EUR |
| `to_symbol` | A three-letter symbol from the  forex currency list. For example: to_symbol=USD |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `outputsize` | By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns the full-length intraday time series. The "compact" option is recommended if you would like to reduce the data size of each API call. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the intraday time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey=demo
```

```text
https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD&interval=5min&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## FX_DAILY

**函数名**: `FX_DAILY`

### 描述

This API returns the daily time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=FX_DAILY |
| `from_symbol` | A three-letter symbol from the  forex currency list. For example: from_symbol=EUR |
| `to_symbol` | A three-letter symbol from the  forex currency list. For example: to_symbol=USD |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `outputsize` | By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the daily time series; full returns the full-length daily time series. The "compact" option is recommended if you would like to reduce the data size of each API call. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey=demo**
```text
https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey=demo
```

```text
https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=EUR&to_symbol=USD&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## FX_WEEKLY

**函数名**: `FX_WEEKLY`

### 描述

This API returns the weekly time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.

The latest data point is the price information for the week (or partial week) containing the current trading day, updated realtime.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=FX_WEEKLY |
| `from_symbol` | A three-letter symbol from the  forex currency list. For example: from_symbol=EUR |
| `to_symbol` | A three-letter symbol from the  forex currency list. For example: to_symbol=USD |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the weekly time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol=EUR&to_symbol=USD&apikey=demo**
```text
https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol=EUR&to_symbol=USD&apikey=demo
```

```text
https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol=EUR&to_symbol=USD&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol=EUR&to_symbol=USD&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol=EUR&to_symbol=USD&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol=EUR&to_symbol=USD&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=FX_WEEKLY&from_symbol=EUR&to_symbol=USD&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## FX_MONTHLY

**函数名**: `FX_MONTHLY`

### 描述

This API returns the monthly time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.

The latest data point is the prices information for the month (or partial month) containing the current trading day, updated realtime.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=FX_MONTHLY |
| `from_symbol` | A three-letter symbol from the  forex currency list. For example: from_symbol=EUR |
| `to_symbol` | A three-letter symbol from the  forex currency list. For example: to_symbol=USD |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the monthly time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=EUR&to_symbol=USD&apikey=demo**
```text
https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=EUR&to_symbol=USD&apikey=demo
```

```text
https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=EUR&to_symbol=USD&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=EUR&to_symbol=USD&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=EUR&to_symbol=USD&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=EUR&to_symbol=USD&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=FX_MONTHLY&from_symbol=EUR&to_symbol=USD&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## CURRENCY_EXCHANGE_RATE Trending [Trending]

**函数名**: `CURRENCY_EXCHANGE_RATE`

### 描述

This API returns the realtime exchange rate for any pair of cryptocurrency (e.g., Bitcoin) or physical currency (e.g., USD).

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=CURRENCY_EXCHANGE_RATE |
| `from_currency` | The currency you would like to get the exchange rate for. It can either be a  physical currency or cryptocurrency. For example: from_currency=USD or from_currency=BTC. |
| `to_currency` | The destination currency for the exchange rate. It can either be a  physical currency or cryptocurrency. For example: to_currency=USD or to_currency=BTC. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=EUR&apikey=demo
```

```text
https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=EUR&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=EUR&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=EUR&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=EUR&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## CRYPTO_INTRADAY Trending Premium [Premium, Trending]

**函数名**: `CRYPTO_INTRADAY`

### 描述

This API returns intraday time series (timestamp, open, high, low, close, volume) of the cryptocurrency specified, updated realtime.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=CRYPTO_INTRADAY |
| `symbol` | The cryptocurrency of your choice. It can be any of the "from" currencies in the cryptocurrency list. For example: symbol=ETH. |
| `market` | The exchange market of your choice. It can be any of the "to" currencies in the cryptocurrency list. For example: market=USD. |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `outputsize` | By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns the full-length intraday time series. The "compact" option is recommended if you would like to reduce the data size of each API call. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the intraday time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=ETH&market=USD&interval=5min&apikey=demo
```

```text
https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=ETH&market=USD&interval=5min&outputsize=full&apikey=demo
```

```text
https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=ETH&market=USD&interval=5min&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=ETH&market=USD&interval=5min&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=ETH&market=USD&interval=5min&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=ETH&market=USD&interval=5min&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=CRYPTO_INTRADAY&symbol=ETH&market=USD&interval=5min&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## DIGITAL_CURRENCY_DAILY

**函数名**: `DIGITAL_CURRENCY_DAILY`

### 描述

This API returns the daily historical time series for a cryptocurrency (e.g., BTC) traded on a specific market (e.g., EUR/Euro), refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific currency and USD.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=DIGITAL_CURRENCY_DAILY |
| `symbol` | The cryptocurrency of your choice. It can be any of the "from" currencies in the cryptocurrency list. For example: symbol=BTC. |
| `market` | The exchange market of your choice. It can be any of the "to" currencies in the cryptocurrency list. For example: market=EUR. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=EUR&apikey=demo**
```text
https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=EUR&apikey=demo
```

```text
https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=EUR&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=EUR&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=EUR&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=EUR&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=EUR&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## DIGITAL_CURRENCY_WEEKLY Trending [Trending]

**函数名**: `DIGITAL_CURRENCY_WEEKLY`

### 描述

This API returns the weekly historical time series for a cryptocurrency (e.g., BTC) traded on a specific market (e.g., EUR/Euro), refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific currency and USD.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=DIGITAL_CURRENCY_WEEKLY |
| `symbol` | The cryptocurrency of your choice. It can be any of the "from" currencies in the cryptocurrency list. For example: symbol=BTC. |
| `market` | The exchange market of your choice. It can be any of the "to" currencies in the cryptocurrency list. For example: market=EUR. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol=BTC&market=EUR&apikey=demo
```

```text
https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol=BTC&market=EUR&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol=BTC&market=EUR&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol=BTC&market=EUR&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol=BTC&market=EUR&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_WEEKLY&symbol=BTC&market=EUR&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## DIGITAL_CURRENCY_MONTHLY Trending [Trending]

**函数名**: `DIGITAL_CURRENCY_MONTHLY`

### 描述

This API returns the monthly historical time series for a cryptocurrency (e.g., BTC) traded on a specific market (e.g., EUR/Euro), refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific currency and USD.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The time series of your choice. In this case, function=DIGITAL_CURRENCY_MONTHLY |
| `symbol` | The cryptocurrency of your choice. It can be any of the "from" currencies in the cryptocurrency list. For example: symbol=BTC. |
| `market` | The exchange market of your choice. It can be any of the "to" currencies in the cryptocurrency list. For example: market=EUR. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=EUR&apikey=demo
```

```text
https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=EUR&apikey=demo&datatype=csv
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=EUR&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=EUR&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=EUR&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=BTC&market=EUR&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Gold & Silver Spot Prices Trending [Trending]

**函数名**: `G`

### 描述

This API returns the live spot prices of gold and silver metals.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=GOLD_SILVER_SPOT |
| `symbol` | For gold, strings GOLD and XAU are accepted. For silver, strings SILVER and XAG are accepted. |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

**https://www.alphavantage.co/query?function=GOLD_SILVER_SPOT&symbol=SILVER&apikey=demo**
```text
https://www.alphavantage.co/query?function=GOLD_SILVER_SPOT&symbol=SILVER&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=GOLD_SILVER_SPOT&symbol=SILVER&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=GOLD_SILVER_SPOT&symbol=SILVER&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=GOLD_SILVER_SPOT&symbol=SILVER&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=GOLD_SILVER_SPOT&symbol=SILVER&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Gold & Silver Historical Prices Trending [Trending]

**函数名**: `G`

### 描述

This API returns the historical gold and silver prices in daily, weekly, and monthly horizons.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=GOLD_SILVER_HISTORY |
| `symbol` | For gold, strings GOLD and XAU are accepted. For silver, strings SILVER and XAG are accepted. |
| `interval` | Strings daily, weekly and monthly are accepted |
| `apikey` | Your API key. Claim your free API key here. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=GOLD_SILVER_HISTORY&symbol=SILVER&interval=daily&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=GOLD_SILVER_HISTORY&symbol=SILVER&interval=daily&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=GOLD_SILVER_HISTORY&symbol=SILVER&interval=daily&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=GOLD_SILVER_HISTORY&symbol=SILVER&interval=daily&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=GOLD_SILVER_HISTORY&symbol=SILVER&interval=daily&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Crude Oil Prices: West Texas Intermediate (WTI) Trending [Trending]

**函数名**: `C`

### 描述

This API returns the West Texas Intermediate (WTI) crude oil prices in daily, weekly, and monthly horizons.

Source: U.S. Energy Information Administration, Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=WTI |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings daily, weekly, and monthly are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=WTI&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=WTI&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=WTI&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=WTI&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=WTI&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=WTI&interval=monthly&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Crude Oil Prices (Brent) Trending [Trending]

**函数名**: `C`

### 描述

This API returns the Brent (Europe) crude oil prices in daily, weekly, and monthly horizons.

Source: U.S. Energy Information Administration, Crude Oil Prices: Brent - Europe, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=BRENT |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings daily, weekly, and monthly are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=BRENT&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=BRENT&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=BRENT&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=BRENT&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=BRENT&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=BRENT&interval=monthly&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Natural Gas

**函数名**: `N`

### 描述

This API returns the Henry Hub natural gas spot prices in daily, weekly, and monthly horizons.

Source: U.S. Energy Information Administration, Henry Hub Natural Gas Spot Price, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=NATURAL_GAS |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings daily, weekly, and monthly are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=NATURAL_GAS&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=NATURAL_GAS&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=NATURAL_GAS&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=NATURAL_GAS&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=NATURAL_GAS&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=NATURAL_GAS&interval=monthly&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Global Price of Copper

**函数名**: `G`

### 描述

This API returns the global price of copper in monthly, quarterly, and annual horizons.

Source: International Monetary Fund (IMF Terms of Use), Global price of Copper, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=COPPER |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings monthly, quarterly, and annual are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=COPPER&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=COPPER&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=COPPER&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=COPPER&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=COPPER&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=COPPER&interval=monthly&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Global Price of Aluminum

**函数名**: `G`

### 描述

This API returns the global price of aluminum in monthly, quarterly, and annual horizons.

Source: International Monetary Fund (IMF Terms of Use), Global price of Aluminum, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=ALUMINUM |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings monthly, quarterly, and annual are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=ALUMINUM&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=ALUMINUM&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=ALUMINUM&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=ALUMINUM&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=ALUMINUM&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=ALUMINUM&interval=monthly&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Global Price of Wheat

**函数名**: `G`

### 描述

This API returns the global price of wheat in monthly, quarterly, and annual horizons.

Source: International Monetary Fund (IMF Terms of Use), Global price of Wheat, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=WHEAT |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings monthly, quarterly, and annual are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=WHEAT&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=WHEAT&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=WHEAT&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=WHEAT&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=WHEAT&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=WHEAT&interval=monthly&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Global Price of Corn

**函数名**: `G`

### 描述

This API returns the global price of corn in monthly, quarterly, and annual horizons.

Source: International Monetary Fund (IMF Terms of Use), Global price of Corn, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=CORN |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings monthly, quarterly, and annual are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=CORN&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=CORN&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=CORN&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=CORN&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=CORN&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=CORN&interval=monthly&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Global Price of Cotton

**函数名**: `G`

### 描述

This API returns the global price of cotton in monthly, quarterly, and annual horizons.

Source: International Monetary Fund (IMF Terms of Use), Global price of Cotton, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=COTTON |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings monthly, quarterly, and annual are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=COTTON&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=COTTON&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=COTTON&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=COTTON&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=COTTON&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=COTTON&interval=monthly&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Global Price of Sugar

**函数名**: `G`

### 描述

This API returns the global price of sugar in monthly, quarterly, and annual horizons.

Source: International Monetary Fund (IMF Terms of Use), Global price of Sugar, No. 11, World, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=SUGAR |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings monthly, quarterly, and annual are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=SUGAR&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=SUGAR&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=SUGAR&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=SUGAR&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=SUGAR&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=SUGAR&interval=monthly&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Global Price of Coffee

**函数名**: `G`

### 描述

This API returns the global price of coffee in monthly, quarterly, and annual horizons.

Source: International Monetary Fund (IMF Terms of Use), Global price of Coffee, Other Mild Arabica, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=COFFEE |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings monthly, quarterly, and annual are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=COFFEE&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=COFFEE&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=COFFEE&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=COFFEE&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=COFFEE&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=COFFEE&interval=monthly&apikey=demo";
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## Global Price Index of All Commodities

**函数名**: `G`

### 描述

This API returns the global price index of all commodities in monthly, quarterly, and annual temporal dimensions.

Source: International Monetary Fund (IMF Terms of Use), Global Price Index of All Commodities, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=ALL_COMMODITIES |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings monthly, quarterly, and annual are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval=monthly&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## REAL_GDP Trending [Trending]

**函数名**: `REAL_GDP`

### 描述

This API returns the annual and quarterly Real GDP of the United States.

Source: U.S. Bureau of Economic Analysis, Real Gross Domestic Product, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=REAL_GDP |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=annual. Strings quarterly and annual are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo**
```text
https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## REAL_GDP_PER_CAPITA

**函数名**: `REAL_GDP_PER_CAPITA`

### 描述

This API returns the quarterly Real GDP per Capita data of the United States.

Source: U.S. Bureau of Economic Analysis, Real gross domestic product per capita, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=REAL_GDP_PER_CAPITA |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&apikey=demo**
```text
https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=REAL_GDP_PER_CAPITA&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## TREASURY_YIELD Trending [Trending]

**函数名**: `TREASURY_YIELD`

### 描述

This API returns the daily, weekly, and monthly US treasury yield of a given maturity timeline (e.g., 5 year, 30 year, etc).

Source: Board of Governors of the Federal Reserve System (US), Market Yield on U.S. Treasury Securities at 3-month, 2-year, 5-year, 7-year, 10-year, and 30-year Constant Maturities, Quoted on an Investment Basis, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=TREASURY_YIELD |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings daily, weekly, and monthly are accepted. |
| `maturity` | By default, maturity=10year. Strings 3month, 2year, 5year, 7year, 10year, and 30year are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## FEDERAL_FUNDS_RATE

**函数名**: `FEDERAL_FUNDS_RATE`

### 描述

This API returns the daily, weekly, and monthly federal funds rate (interest rate) of the United States.

Source: Board of Governors of the Federal Reserve System (US), Federal Funds Effective Rate, retrieved from FRED, Federal Reserve Bank of St. Louis (https://fred.stlouisfed.org/series/FEDFUNDS). This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=FEDERAL_FUNDS_RATE |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings daily, weekly, and monthly are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=FEDERAL_FUNDS_RATE&interval=monthly&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## CPI

**函数名**: `CPI`

### 描述

This API returns the monthly and semiannual consumer price index (CPI) of the United States. CPI is widely regarded as the barometer of inflation levels in the broader economy.

Source: U.S. Bureau of Labor Statistics, Consumer Price Index for All Urban Consumers: All Items in U.S. City Average, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=CPI |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `interval` | By default, interval=monthly. Strings monthly and semiannual are accepted. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey=demo**
```text
https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## INFLATION

**函数名**: `INFLATION`

### 描述

This API returns the annual inflation rates (consumer prices) of the United States.

Source: World Bank, Inflation, consumer prices for the United States, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=INFLATION |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=INFLATION&apikey=demo**
```text
https://www.alphavantage.co/query?function=INFLATION&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=INFLATION&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=INFLATION&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=INFLATION&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=INFLATION&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## RETAIL_SALES

**函数名**: `RETAIL_SALES`

### 描述

This API returns the monthly Advance Retail Sales: Retail Trade data of the United States.

Source: U.S. Census Bureau, Advance Retail Sales: Retail Trade, retrieved from FRED, Federal Reserve Bank of St. Louis (https://fred.stlouisfed.org/series/RSXFSN). This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=RETAIL_SALES |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=RETAIL_SALES&apikey=demo**
```text
https://www.alphavantage.co/query?function=RETAIL_SALES&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=RETAIL_SALES&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=RETAIL_SALES&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=RETAIL_SALES&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=RETAIL_SALES&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## DURABLES

**函数名**: `DURABLES`

### 描述

This API returns the monthly manufacturers' new orders of durable goods in the United States.

Source: U.S. Census Bureau, Manufacturers' New Orders: Durable Goods, retrieved from FRED, Federal Reserve Bank of St. Louis (https://fred.stlouisfed.org/series/UMDMNO). This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=DURABLES |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=DURABLES&apikey=demo**
```text
https://www.alphavantage.co/query?function=DURABLES&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=DURABLES&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=DURABLES&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=DURABLES&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=DURABLES&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## UNEMPLOYMENT

**函数名**: `UNEMPLOYMENT`

### 描述

This API returns the monthly unemployment data of the United States. The unemployment rate represents the number of unemployed as a percentage of the labor force. Labor force data are restricted to people 16 years of age and older, who currently reside in 1 of the 50 states or the District of Columbia, who do not reside in institutions (e.g., penal and mental facilities, homes for the aged), and who are not on active duty in the Armed Forces (source).

Source: U.S. Bureau of Labor Statistics, Unemployment Rate, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=UNEMPLOYMENT |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey=demo**
```text
https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## NONFARM_PAYROLL

**函数名**: `NONFARM_PAYROLL`

### 描述

This API returns the monthly US All Employees: Total Nonfarm (commonly known as Total Nonfarm Payroll), a measure of the number of U.S. workers in the economy that excludes proprietors, private household employees, unpaid volunteers, farm employees, and the unincorporated self-employed.

Source: U.S. Bureau of Labor Statistics, All Employees, Total Nonfarm, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The function of your choice. In this case, function=NONFARM_PAYROLL |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |

### 示例 URL

**https://www.alphavantage.co/query?function=NONFARM_PAYROLL&apikey=demo**
```text
https://www.alphavantage.co/query?function=NONFARM_PAYROLL&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=NONFARM_PAYROLL&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=NONFARM_PAYROLL&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=NONFARM_PAYROLL&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=NONFARM_PAYROLL&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## SMA Trending [Trending]

**函数名**: `SMA`

### 描述

This API returns the simple moving average (SMA) values. See also: SMA explainer and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=SMA |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo
```

```text
https://www.alphavantage.co/query?function=SMA&symbol=USDEUR&interval=weekly&time_period=10&series_type=open&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## EMA Trending [Trending]

**函数名**: `EMA`

### 描述

This API returns the exponential moving average (EMA) values. See also: EMA explainer and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=EMA |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=EMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo
```

```text
https://www.alphavantage.co/query?function=EMA&symbol=USDEUR&interval=weekly&time_period=10&series_type=open&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=EMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=EMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=EMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=EMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## WMA

**函数名**: `WMA`

### 描述

This API returns the weighted moving average (WMA) values. See also: mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=WMA |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=WMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=WMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=WMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=WMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=WMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## DEMA

**函数名**: `DEMA`

### 描述

This API returns the double exponential moving average (DEMA) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=DEMA |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=DEMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=DEMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=DEMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=DEMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=DEMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## TEMA

**函数名**: `TEMA`

### 描述

This API returns the triple exponential moving average (TEMA) values. See also: mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=TEMA |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=TEMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TEMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TEMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TEMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TEMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## TRIMA

**函数名**: `TRIMA`

### 描述

This API returns the triangular moving average (TRIMA) values. See also: mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=TRIMA |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=TRIMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TRIMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TRIMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TRIMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TRIMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## KAMA

**函数名**: `KAMA`

### 描述

This API returns the Kaufman adaptive moving average (KAMA) values.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=KAMA |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=KAMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=KAMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=KAMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=KAMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=KAMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## MAMA

**函数名**: `MAMA`

### 描述

This API returns the MESA adaptive moving average (MAMA) values.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=MAMA |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `fastlimit` | Positive floats are accepted. By default, fastlimit=0.01. |
| `slowlimit` | Positive floats are accepted. By default, slowlimit=0.01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=MAMA&symbol=IBM&interval=daily&series_type=close&fastlimit=0.02&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=MAMA&symbol=IBM&interval=daily&series_type=close&fastlimit=0.02&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=MAMA&symbol=IBM&interval=daily&series_type=close&fastlimit=0.02&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=MAMA&symbol=IBM&interval=daily&series_type=close&fastlimit=0.02&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=MAMA&symbol=IBM&interval=daily&series_type=close&fastlimit=0.02&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## VWAP Trending Premium [Premium, Trending]

**函数名**: `VWAP`

### 描述

This API returns the volume weighted average price (VWAP) for intraday time series. See also: Investopedia article.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=VWAP |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. In keeping with mainstream investment literatures on VWAP, the following intraday intervals are supported: 1min, 5min, 15min, 30min, 60min |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=VWAP&symbol=IBM&interval=15min&apikey=demo**
```text
https://www.alphavantage.co/query?function=VWAP&symbol=IBM&interval=15min&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=VWAP&symbol=IBM&interval=15min&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=VWAP&symbol=IBM&interval=15min&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=VWAP&symbol=IBM&interval=15min&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=VWAP&symbol=IBM&interval=15min&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## T3

**函数名**: `T`

### 描述

This API returns the Tilson moving average (T3) values. See also: mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=T3 |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=T3&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=T3&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=T3&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=T3&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=T3&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## MACD Trending Premium [Premium, Trending]

**函数名**: `MACD`

### 描述

This API returns the moving average convergence / divergence (MACD) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=MACD |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `fastperiod` | Positive integers are accepted. By default, fastperiod=12. |
| `slowperiod` | Positive integers are accepted. By default, slowperiod=26. |
| `signalperiod` | Positive integers are accepted. By default, signalperiod=9. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=MACD&symbol=IBM&interval=daily&series_type=open&apikey=demo
```

```text
https://www.alphavantage.co/query?function=MACD&symbol=USDEUR&interval=weekly&series_type=open&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=MACD&symbol=IBM&interval=daily&series_type=open&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=MACD&symbol=IBM&interval=daily&series_type=open&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=MACD&symbol=IBM&interval=daily&series_type=open&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=MACD&symbol=IBM&interval=daily&series_type=open&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## MACDEXT

**函数名**: `MACDEXT`

### 描述

This API returns the moving average convergence / divergence values with controllable moving average type. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=MACDEXT |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `fastperiod` | Positive integers are accepted. By default, fastperiod=12. |
| `slowperiod` | Positive integers are accepted. By default, slowperiod=26. |
| `signalperiod` | Positive integers are accepted. By default, signalperiod=9. |
| `fastmatype` | Moving average type for the faster moving average. By default, fastmatype=0. Integers 0 - 8 are accepted with the following mappings. 0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA), 2 = Weighted Moving Average (WMA), 3 = Double Exponential Moving Average (DEMA), 4 = Triple Exponential Moving Average (TEMA), 5 = Triangular Moving Average (TRIMA), 6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA), 8 = MESA Adaptive Moving Average (MAMA). |
| `slowmatype` | Moving average type for the slower moving average. By default, slowmatype=0. Integers 0 - 8 are accepted with the following mappings. 0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA), 2 = Weighted Moving Average (WMA), 3 = Double Exponential Moving Average (DEMA), 4 = Triple Exponential Moving Average (TEMA), 5 = Triangular Moving Average (TRIMA), 6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA), 8 = MESA Adaptive Moving Average (MAMA). |
| `signalmatype` | Moving average type for the signal moving average. By default, signalmatype=0. Integers 0 - 8 are accepted with the following mappings. 0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA), 2 = Weighted Moving Average (WMA), 3 = Double Exponential Moving Average (DEMA), 4 = Triple Exponential Moving Average (TEMA), 5 = Triangular Moving Average (TRIMA), 6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA), 8 = MESA Adaptive Moving Average (MAMA). |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=MACDEXT&symbol=IBM&interval=daily&series_type=open&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=MACDEXT&symbol=IBM&interval=daily&series_type=open&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=MACDEXT&symbol=IBM&interval=daily&series_type=open&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=MACDEXT&symbol=IBM&interval=daily&series_type=open&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=MACDEXT&symbol=IBM&interval=daily&series_type=open&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## STOCH Trending [Trending]

**函数名**: `STOCH`

### 描述

This API returns the stochastic oscillator (STOCH) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=STOCH |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `fastkperiod` | The time period of the fastk moving average. Positive integers are accepted. By default, fastkperiod=5. |
| `slowkperiod` | The time period of the slowk moving average. Positive integers are accepted. By default, slowkperiod=3. |
| `slowdperiod` | The time period of the slowd moving average. Positive integers are accepted. By default, slowdperiod=3. |
| `slowkmatype` | Moving average type for the slowk moving average. By default, slowkmatype=0. Integers 0 - 8 are accepted with the following mappings. 0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA), 2 = Weighted Moving Average (WMA), 3 = Double Exponential Moving Average (DEMA), 4 = Triple Exponential Moving Average (TEMA), 5 = Triangular Moving Average (TRIMA), 6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA), 8 = MESA Adaptive Moving Average (MAMA). |
| `slowdmatype` | Moving average type for the slowd moving average. By default, slowdmatype=0. Integers 0 - 8 are accepted with the following mappings. 0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA), 2 = Weighted Moving Average (WMA), 3 = Double Exponential Moving Average (DEMA), 4 = Triple Exponential Moving Average (TEMA), 5 = Triangular Moving Average (TRIMA), 6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA), 8 = MESA Adaptive Moving Average (MAMA). |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=STOCH&symbol=IBM&interval=daily&apikey=demo**
```text
https://www.alphavantage.co/query?function=STOCH&symbol=IBM&interval=daily&apikey=demo
```

**https://www.alphavantage.co/query?function=STOCH&symbol=USDEUR&interval=weekly&apikey=demo**
```text
https://www.alphavantage.co/query?function=STOCH&symbol=USDEUR&interval=weekly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=STOCH&symbol=IBM&interval=daily&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=STOCH&symbol=IBM&interval=daily&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=STOCH&symbol=IBM&interval=daily&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=STOCH&symbol=IBM&interval=daily&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## STOCHF

**函数名**: `STOCHF`

### 描述

This API returns the stochastic fast (STOCHF) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=STOCHF |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `fastkperiod` | The time period of the fastk moving average. Positive integers are accepted. By default, fastkperiod=5. |
| `fastdperiod` | The time period of the fastd moving average. Positive integers are accepted. By default, fastdperiod=3. |
| `fastdmatype` | Moving average type for the fastd moving average. By default, fastdmatype=0. Integers 0 - 8 are accepted with the following mappings. 0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA), 2 = Weighted Moving Average (WMA), 3 = Double Exponential Moving Average (DEMA), 4 = Triple Exponential Moving Average (TEMA), 5 = Triangular Moving Average (TRIMA), 6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA), 8 = MESA Adaptive Moving Average (MAMA). |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=STOCHF&symbol=IBM&interval=daily&apikey=demo**
```text
https://www.alphavantage.co/query?function=STOCHF&symbol=IBM&interval=daily&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=STOCHF&symbol=IBM&interval=daily&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=STOCHF&symbol=IBM&interval=daily&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=STOCHF&symbol=IBM&interval=daily&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=STOCHF&symbol=IBM&interval=daily&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## RSI Trending [Trending]

**函数名**: `RSI`

### 描述

This API returns the relative strength index (RSI) values. See also: RSI explainer and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=RSI |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=RSI&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo
```

```text
https://www.alphavantage.co/query?function=RSI&symbol=USDEUR&interval=weekly&time_period=10&series_type=open&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=RSI&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=RSI&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=RSI&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=RSI&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## STOCHRSI

**函数名**: `STOCHRSI`

### 描述

This API returns the stochastic relative strength index (STOCHRSI) values. See also: mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=STOCHRSI |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `fastkperiod` | The time period of the fastk moving average. Positive integers are accepted. By default, fastkperiod=5. |
| `fastdperiod` | The time period of the fastd moving average. Positive integers are accepted. By default, fastdperiod=3. |
| `fastdmatype` | Moving average type for the fastd moving average. By default, fastdmatype=0. Integers 0 - 8 are accepted with the following mappings.  0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA), 2 = Weighted Moving Average (WMA), 3 = Double Exponential Moving Average (DEMA), 4 = Triple Exponential Moving Average (TEMA), 5 = Triangular Moving Average (TRIMA), 6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA), 8 = MESA Adaptive Moving Average (MAMA). |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=STOCHRSI&symbol=IBM&interval=daily&time_period=10&series_type=close&fastkperiod=6&fastdmatype=1&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=STOCHRSI&symbol=IBM&interval=daily&time_period=10&series_type=close&fastkperiod=6&fastdmatype=1&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=STOCHRSI&symbol=IBM&interval=daily&time_period=10&series_type=close&fastkperiod=6&fastdmatype=1&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=STOCHRSI&symbol=IBM&interval=daily&time_period=10&series_type=close&fastkperiod=6&fastdmatype=1&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=STOCHRSI&symbol=IBM&interval=daily&time_period=10&series_type=close&fastkperiod=6&fastdmatype=1&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## WILLR

**函数名**: `WILLR`

### 描述

This API returns the Williams' %R (WILLR) values. See also: mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=WILLR |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=WILLR&symbol=IBM&interval=daily&time_period=10&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=WILLR&symbol=IBM&interval=daily&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=WILLR&symbol=IBM&interval=daily&time_period=10&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=WILLR&symbol=IBM&interval=daily&time_period=10&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=WILLR&symbol=IBM&interval=daily&time_period=10&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## ADX Trending [Trending]

**函数名**: `ADX`

### 描述

This API returns the average directional movement index (ADX) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=ADX |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=ADX&symbol=IBM&interval=daily&time_period=10&apikey=demo**
```text
https://www.alphavantage.co/query?function=ADX&symbol=IBM&interval=daily&time_period=10&apikey=demo
```

```text
https://www.alphavantage.co/query?function=ADX&symbol=USDEUR&interval=weekly&time_period=10&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=ADX&symbol=IBM&interval=daily&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=ADX&symbol=IBM&interval=daily&time_period=10&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=ADX&symbol=IBM&interval=daily&time_period=10&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=ADX&symbol=IBM&interval=daily&time_period=10&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## ADXR

**函数名**: `ADXR`

### 描述

This API returns the average directional movement index rating (ADXR) values. See also: mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=ADXR |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=ADXR&symbol=IBM&interval=daily&time_period=10&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=ADXR&symbol=IBM&interval=daily&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=ADXR&symbol=IBM&interval=daily&time_period=10&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=ADXR&symbol=IBM&interval=daily&time_period=10&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=ADXR&symbol=IBM&interval=daily&time_period=10&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## APO

**函数名**: `APO`

### 描述

This API returns the absolute price oscillator (APO) values. See also: mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=APO |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `fastperiod` | Positive integers are accepted. By default, fastperiod=12. |
| `slowperiod` | Positive integers are accepted. By default, slowperiod=26. |
| `matype` | Moving average type. By default, matype=0. Integers 0 - 8 are accepted with the following mappings. 0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA), 2 = Weighted Moving Average (WMA), 3 = Double Exponential Moving Average (DEMA), 4 = Triple Exponential Moving Average (TEMA), 5 = Triangular Moving Average (TRIMA), 6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA), 8 = MESA Adaptive Moving Average (MAMA). |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=APO&symbol=IBM&interval=daily&series_type=close&fastperiod=10&matype=1&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=APO&symbol=IBM&interval=daily&series_type=close&fastperiod=10&matype=1&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=APO&symbol=IBM&interval=daily&series_type=close&fastperiod=10&matype=1&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=APO&symbol=IBM&interval=daily&series_type=close&fastperiod=10&matype=1&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=APO&symbol=IBM&interval=daily&series_type=close&fastperiod=10&matype=1&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## PPO

**函数名**: `PPO`

### 描述

This API returns the percentage price oscillator (PPO) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=PPO |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `fastperiod` | Positive integers are accepted. By default, fastperiod=12. |
| `slowperiod` | Positive integers are accepted. By default, slowperiod=26. |
| `matype` | Moving average type. By default, matype=0. Integers 0 - 8 are accepted with the following mappings. 0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA), 2 = Weighted Moving Average (WMA), 3 = Double Exponential Moving Average (DEMA), 4 = Triple Exponential Moving Average (TEMA), 5 = Triangular Moving Average (TRIMA), 6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA), 8 = MESA Adaptive Moving Average (MAMA). |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=PPO&symbol=IBM&interval=daily&series_type=close&fastperiod=10&matype=1&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=PPO&symbol=IBM&interval=daily&series_type=close&fastperiod=10&matype=1&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=PPO&symbol=IBM&interval=daily&series_type=close&fastperiod=10&matype=1&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=PPO&symbol=IBM&interval=daily&series_type=close&fastperiod=10&matype=1&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=PPO&symbol=IBM&interval=daily&series_type=close&fastperiod=10&matype=1&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## MOM

**函数名**: `MOM`

### 描述

This API returns the momentum (MOM) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=MOM |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=MOM&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=MOM&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=MOM&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=MOM&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=MOM&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## BOP

**函数名**: `BOP`

### 描述

This API returns the balance of power (BOP) values.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=BOP |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=BOP&symbol=IBM&interval=daily&apikey=demo**
```text
https://www.alphavantage.co/query?function=BOP&symbol=IBM&interval=daily&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=BOP&symbol=IBM&interval=daily&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=BOP&symbol=IBM&interval=daily&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=BOP&symbol=IBM&interval=daily&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=BOP&symbol=IBM&interval=daily&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## CCI Trending [Trending]

**函数名**: `CCI`

### 描述

This API returns the commodity channel index (CCI) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=CCI |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=CCI&symbol=IBM&interval=daily&time_period=10&apikey=demo**
```text
https://www.alphavantage.co/query?function=CCI&symbol=IBM&interval=daily&time_period=10&apikey=demo
```

```text
https://www.alphavantage.co/query?function=CCI&symbol=USDEUR&interval=weekly&time_period=10&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=CCI&symbol=IBM&interval=daily&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=CCI&symbol=IBM&interval=daily&time_period=10&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=CCI&symbol=IBM&interval=daily&time_period=10&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=CCI&symbol=IBM&interval=daily&time_period=10&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## CMO

**函数名**: `CMO`

### 描述

This API returns the Chande momentum oscillator (CMO) values. See also: mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=CMO |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=CMO&symbol=IBM&interval=weekly&time_period=10&series_type=close&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=CMO&symbol=IBM&interval=weekly&time_period=10&series_type=close&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=CMO&symbol=IBM&interval=weekly&time_period=10&series_type=close&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=CMO&symbol=IBM&interval=weekly&time_period=10&series_type=close&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=CMO&symbol=IBM&interval=weekly&time_period=10&series_type=close&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## ROC

**函数名**: `ROC`

### 描述

This API returns the rate of change (ROC) values. See also: Investopedia article.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=ROC |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=ROC&symbol=IBM&interval=weekly&time_period=10&series_type=close&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=ROC&symbol=IBM&interval=weekly&time_period=10&series_type=close&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=ROC&symbol=IBM&interval=weekly&time_period=10&series_type=close&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=ROC&symbol=IBM&interval=weekly&time_period=10&series_type=close&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=ROC&symbol=IBM&interval=weekly&time_period=10&series_type=close&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## ROCR

**函数名**: `ROCR`

### 描述

This API returns the rate of change ratio (ROCR) values. See also: Investopedia article.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=ROCR |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=ROCR&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=ROCR&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=ROCR&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=ROCR&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=ROCR&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## AROON Trending [Trending]

**函数名**: `AROON`

### 描述

This API returns the Aroon (AROON) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=AROON |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=AROON&symbol=IBM&interval=daily&time_period=14&apikey=demo
```

```text
https://www.alphavantage.co/query?function=AROON&symbol=USDEUR&interval=weekly&time_period=14&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=AROON&symbol=IBM&interval=daily&time_period=14&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=AROON&symbol=IBM&interval=daily&time_period=14&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=AROON&symbol=IBM&interval=daily&time_period=14&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=AROON&symbol=IBM&interval=daily&time_period=14&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## AROONOSC

**函数名**: `AROONOSC`

### 描述

This API returns the Aroon oscillator (AROONOSC) values. See also: mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=AROONOSC |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=AROONOSC&symbol=IBM&interval=daily&time_period=10&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=AROONOSC&symbol=IBM&interval=daily&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=AROONOSC&symbol=IBM&interval=daily&time_period=10&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=AROONOSC&symbol=IBM&interval=daily&time_period=10&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=AROONOSC&symbol=IBM&interval=daily&time_period=10&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## MFI

**函数名**: `MFI`

### 描述

This API returns the money flow index (MFI) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=MFI |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=MFI&symbol=IBM&interval=weekly&time_period=10&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=MFI&symbol=IBM&interval=weekly&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=MFI&symbol=IBM&interval=weekly&time_period=10&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=MFI&symbol=IBM&interval=weekly&time_period=10&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=MFI&symbol=IBM&interval=weekly&time_period=10&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## TRIX

**函数名**: `TRIX`

### 描述

This API returns the 1-day rate of change of a triple smooth exponential moving average (TRIX) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=TRIX |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=TRIX&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TRIX&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TRIX&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TRIX&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TRIX&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## ULTOSC

**函数名**: `ULTOSC`

### 描述

This API returns the ultimate oscillator (ULTOSC) values. See also: mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=ULTOSC |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `timeperiod1` | The first time period for the indicator. Positive integers are accepted. By default, timeperiod1=7. |
| `timeperiod2` | The second time period for the indicator. Positive integers are accepted. By default, timeperiod2=14. |
| `timeperiod3` | The third time period for the indicator. Positive integers are accepted. By default, timeperiod3=28. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=ULTOSC&symbol=IBM&interval=daily&timeperiod1=8&apikey=demo
```

**https://www.alphavantage.co/query?function=ULTOSC&symbol=IBM&interval=daily&apikey=demo**
```text
https://www.alphavantage.co/query?function=ULTOSC&symbol=IBM&interval=weekly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=ULTOSC&symbol=IBM&interval=daily&timeperiod1=8&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=ULTOSC&symbol=IBM&interval=daily&timeperiod1=8&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=ULTOSC&symbol=IBM&interval=daily&timeperiod1=8&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=ULTOSC&symbol=IBM&interval=daily&timeperiod1=8&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## DX

**函数名**: `DX`

### 描述

This API returns the directional movement index (DX) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=DX |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=DX&symbol=IBM&interval=daily&time_period=10&apikey=demo**
```text
https://www.alphavantage.co/query?function=DX&symbol=IBM&interval=daily&time_period=10&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=DX&symbol=IBM&interval=daily&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=DX&symbol=IBM&interval=daily&time_period=10&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=DX&symbol=IBM&interval=daily&time_period=10&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=DX&symbol=IBM&interval=daily&time_period=10&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## MINUS_DI

**函数名**: `MINUS_DI`

### 描述

This API returns the minus directional indicator (MINUS_DI) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=MINUS_DI |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=MINUS_DI&symbol=IBM&interval=weekly&time_period=10&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=MINUS_DI&symbol=IBM&interval=weekly&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=MINUS_DI&symbol=IBM&interval=weekly&time_period=10&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=MINUS_DI&symbol=IBM&interval=weekly&time_period=10&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=MINUS_DI&symbol=IBM&interval=weekly&time_period=10&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## PLUS_DI

**函数名**: `PLUS_DI`

### 描述

This API returns the plus directional indicator (PLUS_DI) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=PLUS_DI |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=PLUS_DI&symbol=IBM&interval=daily&time_period=10&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=PLUS_DI&symbol=IBM&interval=daily&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=PLUS_DI&symbol=IBM&interval=daily&time_period=10&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=PLUS_DI&symbol=IBM&interval=daily&time_period=10&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=PLUS_DI&symbol=IBM&interval=daily&time_period=10&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## MINUS_DM

**函数名**: `MINUS_DM`

### 描述

This API returns the minus directional movement (MINUS_DM) values. See also: Investopedia article

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=MINUS_DM |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=MINUS_DM&symbol=IBM&interval=daily&time_period=10&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=MINUS_DM&symbol=IBM&interval=daily&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=MINUS_DM&symbol=IBM&interval=daily&time_period=10&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=MINUS_DM&symbol=IBM&interval=daily&time_period=10&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=MINUS_DM&symbol=IBM&interval=daily&time_period=10&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## PLUS_DM

**函数名**: `PLUS_DM`

### 描述

This API returns the plus directional movement (PLUS_DM) values. See also: Investopedia article

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=PLUS_DM |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=PLUS_DM&symbol=IBM&interval=daily&time_period=10&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=PLUS_DM&symbol=IBM&interval=daily&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=PLUS_DM&symbol=IBM&interval=daily&time_period=10&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=PLUS_DM&symbol=IBM&interval=daily&time_period=10&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=PLUS_DM&symbol=IBM&interval=daily&time_period=10&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## BBANDS Trending [Trending]

**函数名**: `BBANDS`

### 描述

This API returns the Bollinger bands (BBANDS) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=BBANDS |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `nbdevup` | The standard deviation multiplier of the upper band. Positive integers are accepted. By default, nbdevup=2. |
| `nbdevdn` | The standard deviation multiplier of the lower band. Positive integers are accepted. By default, nbdevdn=2. |
| `matype` | Moving average type of the time series. By default, matype=0. Integers 0 - 8 are accepted with the following mappings. 0 = Simple Moving Average (SMA), 1 = Exponential Moving Average (EMA), 2 = Weighted Moving Average (WMA), 3 = Double Exponential Moving Average (DEMA), 4 = Triple Exponential Moving Average (TEMA), 5 = Triangular Moving Average (TRIMA), 6 = T3 Moving Average, 7 = Kaufman Adaptive Moving Average (KAMA), 8 = MESA Adaptive Moving Average (MAMA). |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=BBANDS&symbol=IBM&interval=weekly&time_period=5&series_type=close&nbdevup=3&nbdevdn=3&apikey=demo
```

```text
https://www.alphavantage.co/query?function=BBANDS&symbol=USDEUR&interval=weekly&time_period=5&series_type=close&nbdevup=3&nbdevdn=3&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=BBANDS&symbol=IBM&interval=weekly&time_period=5&series_type=close&nbdevup=3&nbdevdn=3&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=BBANDS&symbol=IBM&interval=weekly&time_period=5&series_type=close&nbdevup=3&nbdevdn=3&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=BBANDS&symbol=IBM&interval=weekly&time_period=5&series_type=close&nbdevup=3&nbdevdn=3&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=BBANDS&symbol=IBM&interval=weekly&time_period=5&series_type=close&nbdevup=3&nbdevdn=3&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## MIDPOINT

**函数名**: `MIDPOINT`

### 描述

This API returns the midpoint (MIDPOINT) values. MIDPOINT = (highest value + lowest value)/2.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=MIDPOINT |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=MIDPOINT&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=MIDPOINT&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=MIDPOINT&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=MIDPOINT&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=MIDPOINT&symbol=IBM&interval=daily&time_period=10&series_type=close&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## MIDPRICE

**函数名**: `MIDPRICE`

### 描述

This API returns the midpoint price (MIDPRICE) values. MIDPRICE = (highest high + lowest low)/2.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=MIDPRICE |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=MIDPRICE&symbol=IBM&interval=daily&time_period=10&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=MIDPRICE&symbol=IBM&interval=daily&time_period=10&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=MIDPRICE&symbol=IBM&interval=daily&time_period=10&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=MIDPRICE&symbol=IBM&interval=daily&time_period=10&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=MIDPRICE&symbol=IBM&interval=daily&time_period=10&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## SAR

**函数名**: `SAR`

### 描述

This API returns the parabolic SAR (SAR) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=SAR |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `acceleration` | The acceleration factor. Positive floats are accepted. By default, acceleration=0.01. |
| `maximum` | The acceleration factor maximum value. Positive floats are accepted. By default, maximum=0.20. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=SAR&symbol=IBM&interval=weekly&acceleration=0.05&maximum=0.25&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=SAR&symbol=IBM&interval=weekly&acceleration=0.05&maximum=0.25&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=SAR&symbol=IBM&interval=weekly&acceleration=0.05&maximum=0.25&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=SAR&symbol=IBM&interval=weekly&acceleration=0.05&maximum=0.25&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=SAR&symbol=IBM&interval=weekly&acceleration=0.05&maximum=0.25&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## TRANGE

**函数名**: `TRANGE`

### 描述

This API returns the true range (TRANGE) values. See also: mathematical reference

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=TRANGE |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=TRANGE&symbol=IBM&interval=daily&apikey=demo**
```text
https://www.alphavantage.co/query?function=TRANGE&symbol=IBM&interval=daily&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TRANGE&symbol=IBM&interval=daily&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=TRANGE&symbol=IBM&interval=daily&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=TRANGE&symbol=IBM&interval=daily&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=TRANGE&symbol=IBM&interval=daily&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## ATR

**函数名**: `ATR`

### 描述

This API returns the average true range (ATR) values. See also: Investopedia article and mathematical reference

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=ATR |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=ATR&symbol=IBM&interval=daily&time_period=14&apikey=demo**
```text
https://www.alphavantage.co/query?function=ATR&symbol=IBM&interval=daily&time_period=14&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=ATR&symbol=IBM&interval=daily&time_period=14&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=ATR&symbol=IBM&interval=daily&time_period=14&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=ATR&symbol=IBM&interval=daily&time_period=14&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=ATR&symbol=IBM&interval=daily&time_period=14&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## NATR

**函数名**: `NATR`

### 描述

This API returns the normalized average true range (NATR) values.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=NATR |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=NATR&symbol=IBM&interval=weekly&time_period=14&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=NATR&symbol=IBM&interval=weekly&time_period=14&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=NATR&symbol=IBM&interval=weekly&time_period=14&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=NATR&symbol=IBM&interval=weekly&time_period=14&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=NATR&symbol=IBM&interval=weekly&time_period=14&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## AD Trending [Trending]

**函数名**: `AD`

### 描述

This API returns the Chaikin A/D line (AD) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=AD |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=AD&symbol=IBM&interval=daily&apikey=demo**
```text
https://www.alphavantage.co/query?function=AD&symbol=IBM&interval=daily&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=AD&symbol=IBM&interval=daily&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=AD&symbol=IBM&interval=daily&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=AD&symbol=IBM&interval=daily&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=AD&symbol=IBM&interval=daily&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## ADOSC

**函数名**: `ADOSC`

### 描述

This API returns the Chaikin A/D oscillator (ADOSC) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=ADOSC |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `fastperiod` | The time period of the fast EMA. Positive integers are accepted. By default, fastperiod=3. |
| `slowperiod` | The time period of the slow EMA. Positive integers are accepted. By default, slowperiod=10. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=ADOSC&symbol=IBM&interval=daily&fastperiod=5&apikey=demo**
```text
https://www.alphavantage.co/query?function=ADOSC&symbol=IBM&interval=daily&fastperiod=5&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=ADOSC&symbol=IBM&interval=daily&fastperiod=5&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=ADOSC&symbol=IBM&interval=daily&fastperiod=5&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=ADOSC&symbol=IBM&interval=daily&fastperiod=5&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=ADOSC&symbol=IBM&interval=daily&fastperiod=5&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## OBV Trending [Trending]

**函数名**: `OBV`

### 描述

This API returns the on balance volume (OBV) values. See also: Investopedia article and mathematical reference.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=OBV |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

**https://www.alphavantage.co/query?function=OBV&symbol=IBM&interval=weekly&apikey=demo**
```text
https://www.alphavantage.co/query?function=OBV&symbol=IBM&interval=weekly&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=OBV&symbol=IBM&interval=weekly&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=OBV&symbol=IBM&interval=weekly&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=OBV&symbol=IBM&interval=weekly&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=OBV&symbol=IBM&interval=weekly&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## HT_TRENDLINE

**函数名**: `HT_TRENDLINE`

### 描述

This API returns the Hilbert transform, instantaneous trendline (HT_TRENDLINE) values.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=HT_TRENDLINE |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=HT_TRENDLINE&symbol=IBM&interval=daily&series_type=close&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=HT_TRENDLINE&symbol=IBM&interval=daily&series_type=close&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=HT_TRENDLINE&symbol=IBM&interval=daily&series_type=close&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=HT_TRENDLINE&symbol=IBM&interval=daily&series_type=close&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=HT_TRENDLINE&symbol=IBM&interval=daily&series_type=close&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## HT_SINE

**函数名**: `HT_SINE`

### 描述

This API returns the Hilbert transform, sine wave (HT_SINE) values.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=HT_SINE |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=HT_SINE&symbol=IBM&interval=daily&series_type=close&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=HT_SINE&symbol=IBM&interval=daily&series_type=close&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=HT_SINE&symbol=IBM&interval=daily&series_type=close&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=HT_SINE&symbol=IBM&interval=daily&series_type=close&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=HT_SINE&symbol=IBM&interval=daily&series_type=close&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## HT_TRENDMODE

**函数名**: `HT_TRENDMODE`

### 描述

This API returns the Hilbert transform, trend vs cycle mode (HT_TRENDMODE) values.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=HT_TRENDMODE |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=HT_TRENDMODE&symbol=IBM&interval=weekly&series_type=close&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=HT_TRENDMODE&symbol=IBM&interval=weekly&series_type=close&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=HT_TRENDMODE&symbol=IBM&interval=weekly&series_type=close&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=HT_TRENDMODE&symbol=IBM&interval=weekly&series_type=close&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=HT_TRENDMODE&symbol=IBM&interval=weekly&series_type=close&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## HT_DCPERIOD

**函数名**: `HT_DCPERIOD`

### 描述

This API returns the Hilbert transform, dominant cycle period (HT_DCPERIOD) values.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=HT_DCPERIOD |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=HT_DCPERIOD&symbol=IBM&interval=daily&series_type=close&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=HT_DCPERIOD&symbol=IBM&interval=daily&series_type=close&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=HT_DCPERIOD&symbol=IBM&interval=daily&series_type=close&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=HT_DCPERIOD&symbol=IBM&interval=daily&series_type=close&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=HT_DCPERIOD&symbol=IBM&interval=daily&series_type=close&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## HT_DCPHASE

**函数名**: `HT_DCPHASE`

### 描述

This API returns the Hilbert transform, dominant cycle phase (HT_DCPHASE) values.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=HT_DCPHASE |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=HT_DCPHASE&symbol=IBM&interval=daily&series_type=close&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=HT_DCPHASE&symbol=IBM&interval=daily&series_type=close&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=HT_DCPHASE&symbol=IBM&interval=daily&series_type=close&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=HT_DCPHASE&symbol=IBM&interval=daily&series_type=close&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=HT_DCPHASE&symbol=IBM&interval=daily&series_type=close&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---

## HT_PHASOR

**函数名**: `HT_PHASOR`

### 描述

This API returns the Hilbert transform, phasor components (HT_PHASOR) values.

### 请求端点

```text
GET https://www.alphavantage.co/query
```

### 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The technical indicator of your choice. In this case, function=HT_PHASOR |
| `symbol` | The name of the ticker of your choice. For example: symbol=IBM |
| `interval` | Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly |
| `series_type` | The desired price type in the time series. Four types are supported: close, open, high, low |
| `apikey` | Your API key. Claim your free API key here. |

### 可选参数

| 参数名 | 描述 |
|--------|------|
| `month` | By default, this parameter is not set and the technical indicator values will be calculated based on the default length of the underlying intraday, daily, weekly, or monthly time series data. You can use the month parameter (in YYYY-MM format) to return technical indicators for a specific month in history. For example, month=2009-01. |
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file. |
| `entitlement` | This parameter controls the freshness of the data returned. By default, entitlement is not set and historical data is returned. Setting the parameter to entitlement=realtime will return realtime data during the US trading day. Setting the parameter to entitlement=delayed will return 15-minute delayed data during the US trading day. |

### 示例 URL

```text
https://www.alphavantage.co/query?function=HT_PHASOR&symbol=IBM&interval=weekly&series_type=close&apikey=demo
```

### 代码示例

#### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=HT_PHASOR&symbol=IBM&interval=weekly&series_type=close&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

#### Javascript

```javascript
'use strict';
var request = require('request');

// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
var url = 'https://www.alphavantage.co/query?function=HT_PHASOR&symbol=IBM&interval=weekly&series_type=close&apikey=demo';

request.get({
    url: url,
    json: true,
    headers: {'User-Agent': 'request'}
  }, (err, res, data) => {
    if (err) {
      console.log('Error:', err);
    } else if (res.statusCode !== 200) {
      console.log('Status:', res.statusCode);
    } else {
      // data is successfully parsed as a JSON object:
      console.log(data);
    }
});
```

#### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=HT_PHASOR&symbol=IBM&interval=weekly&series_type=close&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

#### Csharp

```csharp
using System;
using System.Collections.Generic;
using System.Net;

// -------------------------------------------------------------------------
// if using .NET Framework
// https://docs.microsoft.com/en-us/dotnet/api/system.web.script.serialization.javascriptserializer?view=netframework-4.8
// This requires including the reference to System.Web.Extensions in your project
using System.Web.Script.Serialization;
// -------------------------------------------------------------------------
// if using .Net Core
// https://docs.microsoft.com/en-us/dotnet/api/system.text.json?view=net-5.0
using System.Text.Json;
// -------------------------------------------------------------------------

namespace ConsoleTests
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            // replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
            string QUERY_URL = "https://www.alphavantage.co/query?function=HT_PHASOR&symbol=IBM&interval=weekly&series_type=close&apikey=demo"
            Uri queryUri = new Uri(QUERY_URL);

            using (WebClient client = new WebClient())
            {
                 // -------------------------------------------------------------------------
                 // if using .NET Framework (System.Web.Script.Serialization)

                JavaScriptSerializer js = new JavaScriptSerializer();
                dynamic json_data = js.Deserialize(client.DownloadString(queryUri), typeof(object));

                // -------------------------------------------------------------------------
                // if using .NET Core (System.Text.Json)
                // using .NET Core libraries to parse JSON is more complicated. For an informative blog post
                // https://devblogs.microsoft.com/dotnet/try-the-new-system-text-json-apis/

                dynamic json_data = JsonSerializer.Deserialize<Dictionary<string, dynamic>>(client.DownloadString(queryUri));

                // -------------------------------------------------------------------------

                // do something with the json_data
            }
        }
    }
}
```

---
