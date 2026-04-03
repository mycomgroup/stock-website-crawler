# IPO Calendar

## 源URL

https://www.alphavantage.co/documentation/#ipo-calendar

## 函数名

`IPO`

## 描述

This API returns a list of IPOs expected in the next 3 months.


## 请求端点

```text
GET https://www.alphavantage.co/query
```

## 必需参数

| 参数名 | 描述 |
|--------|------|
| `function` | The API function of your choice. In this case, function=IPO_CALENDAR |
| `apikey` | Your API key. Claim your free API key here. |

## 示例 URL

**https://www.alphavantage.co/query?function=IPO_CALENDAR&apikey=demo**
```text
https://www.alphavantage.co/query?function=IPO_CALENDAR&apikey=demo
``

## 代码示例

### Python

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

### Text

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

### Php

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
