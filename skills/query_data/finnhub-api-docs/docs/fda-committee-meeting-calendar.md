---
id: "url-7c92854b"
type: "api"
title: "FDA Committee Meeting Calendar"
url: "https://finnhub.io/docs/api/fda-committee-meeting-calendar"
description: "FDA's advisory committees are established to provide functions which support the agency's mission of protecting and promoting the public health, while meeting the requirements set forth in the Federal Advisory Committee Act. Committees are either mandated by statute or established at the discretion of the Department of Health and Human Services. Each committee is subject to renewal at two-year intervals unless the committee charter states otherwise. Method: GET"
source: ""
tags: []
crawl_time: "2026-03-18T11:21:09.384Z"
metadata:
  requestMethod: "GET"
  endpoint: "/fda-advisory-committee-calendar"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "FDA Committee Meeting Calendar\n\nFDA's advisory committees are established to provide functions which support the agency's mission of protecting and promoting the public health, while meeting the requirements set forth in the Federal Advisory Committee Act. Committees are either mandated by statute or established at the discretion of the Department of Health and Human Services. Each committee is subject to renewal at two-year intervals unless the committee charter states otherwise.\n\nMethod: GET\n\nExamples:\n\n/fda-advisory-committee-calendar\n\nArguments:\n\nResponse Attributes:\n\neventDescription\n\nEvent's description.\n\nfromDate\n\nStart time of the event in EST.\n\ntoDate\n\nEnd time of the event in EST.\n\nurl\n\nURL.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.fda_calendar())\n\nSample response\n\n[\n  {\n    \"fromDate\": \"2016-01-11 19:00:00\",\n    \"toDate\": \"2016-01-11 19:00:00\",\n    \"eventDescription\": \"January 12, 2016: Meeting of the Psychopharmacologic Drugs Advisory Committee Meeting Announcement - 01/11/2016 - 01/11/2016\",\n    \"url\": \"https://www.fda.gov/advisory-committees/advisory-committee-calendar/january-12-2016-meeting-psychopharmacologic-drugs-advisory-committee-meeting-announcement-01112016\"\n  },\n  {\n    \"fromDate\": \"2016-01-14 13:00:00\",\n    \"toDate\": \"2016-01-14 17:00:00\",\n    \"eventDescription\": \"January 14, 2016: Vaccines and Related Biological Products Advisory Committee Meeting Announcement - 01/14/2016 - 01/14/2016\",\n    \"url\": \"https://www.fda.gov/advisory-committees/advisory-committee-calendar/january-14-2016-vaccines-and-related-biological-products-advisory-committee-meeting-announcement\"\n  }\n]"
  suggestedFilename: "fda-committee-meeting-calendar"
---

# FDA Committee Meeting Calendar

## 源URL

https://finnhub.io/docs/api/fda-committee-meeting-calendar

## 描述

FDA's advisory committees are established to provide functions which support the agency's mission of protecting and promoting the public health, while meeting the requirements set forth in the Federal Advisory Committee Act. Committees are either mandated by statute or established at the discretion of the Department of Health and Human Services. Each committee is subject to renewal at two-year intervals unless the committee charter states otherwise. Method: GET

## API 端点

**Method**: `GET`
**Endpoint**: `/fda-advisory-committee-calendar`

## 文档正文

FDA's advisory committees are established to provide functions which support the agency's mission of protecting and promoting the public health, while meeting the requirements set forth in the Federal Advisory Committee Act. Committees are either mandated by statute or established at the discretion of the Department of Health and Human Services. Each committee is subject to renewal at two-year intervals unless the committee charter states otherwise. Method: GET

## API 端点

**Method:** `GET`
**Endpoint:** `/fda-advisory-committee-calendar`

FDA Committee Meeting Calendar

FDA's advisory committees are established to provide functions which support the agency's mission of protecting and promoting the public health, while meeting the requirements set forth in the Federal Advisory Committee Act. Committees are either mandated by statute or established at the discretion of the Department of Health and Human Services. Each committee is subject to renewal at two-year intervals unless the committee charter states otherwise.

Method: GET

Examples:

/fda-advisory-committee-calendar

Arguments:

Response Attributes:

eventDescription

Event's description.

fromDate

Start time of the event in EST.

toDate

End time of the event in EST.

url

URL.

Sample code
cURL
Python
Javascript
Go
Ruby
Kotlin
PHP

import finnhub
finnhub_client = finnhub.Client(api_key="")

print(finnhub_client.fda_calendar())

Sample response

[
  {
    "fromDate": "2016-01-11 19:00:00",
    "toDate": "2016-01-11 19:00:00",
    "eventDescription": "January 12, 2016: Meeting of the Psychopharmacologic Drugs Advisory Committee Meeting Announcement - 01/11/2016 - 01/11/2016",
    "url": "https://www.fda.gov/advisory-committees/advisory-committee-calendar/january-12-2016-meeting-psychopharmacologic-drugs-advisory-committee-meeting-announcement-01112016"
  },
  {
    "fromDate": "2016-01-14 13:00:00",
    "toDate": "2016-01-14 17:00:00",
    "eventDescription": "January 14, 2016: Vaccines and Related Biological Products Advisory Committee Meeting Announcement - 01/14/2016 - 01/14/2016",
    "url": "https://www.fda.gov/advisory-committees/advisory-committee-calendar/january-14-2016-vaccines-and-related-biological-products-advisory-committee-meeting-announcement"
  }
]
