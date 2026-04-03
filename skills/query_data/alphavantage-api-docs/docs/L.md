# Listing & Delisting Status

## 源URL

https://www.alphavantage.co/documentation/#listing-status

## 函数名

`L`

## 描述

This API returns a list of active or delisted US stocks and ETFs, either as of the latest trading day or at a specific time in history. The endpoint is positioned to facilitate equity research on asset lifecycle and survivorship.


## 请求端点

```text
GET https://www.alphavantage.co/query
```

## 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The API function of your choice. In this case, function=LISTING_STATUS |
| `apikey` | Your API key. Claim your free API key here. |

## 可选参数

| 参数名 | 描述 |
|--------|------|
| `date` | If no date is set, the API endpoint will return a list of active or delisted symbols as of the latest trading day. If a date is set, the API endpoint will "travel back" in time and return a list of active or delisted symbols on that particular date in history. Any YYYY-MM-DD date later than 2010-01-01 is supported. For example, date=2013-08-03 |
| `state` | By default, state=active and the API will return a list of actively traded stocks and ETFs. Set state=delisted to query a list of delisted assets. |

## 示例 URL

**https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo**
```text
https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo
``

```text
https://www.alphavantage.co/query?function=LISTING_STATUS&date=2014-07-10&state=delisted&apikey=demo
``

## 代码示例

### Python

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

### Text

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

### Php

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

### Csharp

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
