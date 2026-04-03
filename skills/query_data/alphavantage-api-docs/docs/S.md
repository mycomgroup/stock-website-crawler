# Search Endpoint Utility [Utility]

## 源URL

https://www.alphavantage.co/documentation/#symbolsearch

## 函数名

`S`

## 描述

Looking for some specific symbols or companies? Trying to build an auto-complete search box similar to the one below?

We've got you covered! The Search Endpoint returns the best-matching symbols and market information based on keywords of your choice. The search results also contain match scores that provide you with the full flexibility to develop your own search and filtering logic.


## 请求端点

```text
GET https://www.alphavantage.co/query
```

## 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The API function of your choice. In this case, function=SYMBOL_SEARCH |
| `keywords` | A text string of your choice. For example: keywords=microsoft. |
| `apikey` | Your API key. Claim your free API key here. |

## 可选参数

| 参数名 | 描述 |
|--------|------|
| `datatype` | By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the search results in JSON format; csv returns the search results as a CSV (comma separated value) file. |

## 示例 URL

**https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo**
```text
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo
``

**https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tencent&apikey=demo**
```text
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tencent&apikey=demo
``

**https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=demo**
```text
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=demo
``

**https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=SAIC&apikey=demo**
```text
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=SAIC&apikey=demo
``

**https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=demo&datatype=csv**
```text
https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=demo&datatype=csv
``

## 代码示例

### Python

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)
```

### Javascript

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

### Php

```php
<?php
// replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
$json = file_get_contents('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=tesco&apikey=demo');

$data = json_decode($json,true);

print_r($data);

exit;
```

### Csharp

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
