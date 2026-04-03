---
id: "url-5de4d874"
type: "api"
title: "Earnings Call Transcripts Premium"
url: "https://finnhub.io/docs/api/earnings-call-transcripts-api"
description: "Get earnings call transcripts, audio and participants' list. Data is available for US, UK, European, Australian and Canadian companies. 15+ years of data is available with 220,000+ audio which add up to 7TB in size. Method: GET Premium: Premium required."
source: ""
tags: []
crawl_time: "2026-03-18T11:20:57.609Z"
metadata:
  requestMethod: "GET"
  endpoint: "/stock/transcripts?id=AAPL_162777"
  parameters: []
  responses: []
  codeExamples: []
  sampleResponse: ""
  curlExample: ""
  jsonExample: ""
  rawContent: "Earnings Call Transcripts Premium\n\nGet earnings call transcripts, audio and participants' list. Data is available for US, UK, European, Australian and Canadian companies.\n\n15+ years of data is available with 220,000+ audio which add up to 7TB in size.\n\nMethod: GET\n\nPremium: Premium required.\n\nExamples:\n\n/stock/transcripts?id=AAPL_162777\n\nArguments:\n\nidREQUIRED\n\nTranscript's id obtained with Transcripts List endpoint.\n\nResponse Attributes:\n\naudio\n\nAudio link.\n\nid\n\nTranscript's ID.\n\nparticipant\n\nParticipant list\n\ndescription\n\nParticipant's description\n\nname\n\nParticipant's name\n\nrole\n\nWhether the speak is a company's executive or an analyst\n\nquarter\n\nQuarter of earnings result in the case of earnings call transcript.\n\nsymbol\n\nCompany symbol.\n\ntime\n\nTime of the event.\n\ntitle\n\nTitle.\n\ntranscript\n\nTranscript content.\n\nname\n\nSpeaker's name\n\nsession\n\nEarnings calls section (management discussion or Q&A)\n\nspeech\n\nSpeaker's speech\n\nyear\n\nYear of earnings result in the case of earnings call transcript.\n\nSample code\ncURL\nPython\nJavascript\nGo\nRuby\nKotlin\nPHP\n\nimport finnhub\nfinnhub_client = finnhub.Client(api_key=\"\")\n\nprint(finnhub_client.transcripts('AAPL_162777'))\n\nSample response\n\n{\n  \"audio\": \"https://static.finnhub.io/transcripts_audio/4319666.mp3\",\n  \"id\": \"AAPL_326091\",\n  \"participant\": [\n    {\n      \"name\": \"Tejas Gala\",\n      \"description\": \"Senior Analyst at Corporate Finance and IR\"\n    },\n    {\n      \"name\": \"Tim Cook\",\n      \"description\": \"CEO\"\n    }\n  ],\n  \"quarter\": 1,\n  \"symbol\": \"AAPL\",\n  \"time\": \"2020-01-28 21:35:45\",\n  \"title\": \"AAPL - Earnings call transcripts Q1 2020\",\n  \"transcript\": [\n    {\n      \"name\": \"Operator\",\n      \"speech\": [\n        \"Good day, everyone. Welcome to the Apple Incorporated First Quarter Fiscal Year 2020 Earnings Conference Call. Today's conference is being recorded. At this time for opening remarks and introductions, I would like to turn the call over to Tejas Gala, Senior Analyst, Corporate Finance and Investor Relations. Please go ahead.\"\n      ]\n    },\n    {\n      \"name\": \"Tejas Gala\",\n      \"speech\": [\n        \"Thank you. Good afternoon, and thank you for joining us. Speaking first today is Apple's CEO, Tim Cook, and he'll be followed by CFO, Luca Maestri. After that, we'll open the call to questions from analysts. Please note that some of the information you'll hear during our discussion today will consist of forward-looking statements, including without limitation, those regarding revenue, gross margin, operating expenses, other income and expenses, taxes, capital allocation and future business outlook. Actual results or trends could differ materially from our forecast. For more information, please refer to the risk factors discussed in Apple's most recently filed periodic reports on Form 10-K and Form 10-Q and the Form 8-K filed with the SEC today, along with the associated press release. Apple assumes no obligation to update any forward-looking statements or information, which speaks as of their respective dates. I'd now like to turn the call over to Tim for introductory remarks.\"\n      ]\n    }\n  ],\n  \"year\": 2020\n}"
  suggestedFilename: "earnings-call-transcripts-api"
---

# Earnings Call Transcripts Premium

## 源URL

https://finnhub.io/docs/api/earnings-call-transcripts-api

## 描述

Get earnings call transcripts, audio and participants' list. Data is available for US, UK, European, Australian and Canadian companies. 15+ years of data is available with 220,000+ audio which add up to 7TB in size. Method: GET Premium: Premium required.

## API 端点

**Method**: `GET`
**Endpoint**: `/stock/transcripts?id=AAPL_162777`

## 文档正文

Get earnings call transcripts, audio and participants' list. Data is available for US, UK, European, Australian and Canadian companies. 15+ years of data is available with 220,000+ audio which add up to 7TB in size. Method: GET Premium: Premium required.

## API 端点

**Method:** `GET`
**Endpoint:** `/stock/transcripts?id=AAPL_162777`

Earnings Call Transcripts Premium

Get earnings call transcripts, audio and participants' list. Data is available for US, UK, European, Australian and Canadian companies.

15+ years of data is available with 220,000+ audio which add up to 7TB in size.

Method: GET

Premium: Premium required.

Examples:

/stock/transcripts?id=AAPL_162777

Arguments:

idREQUIRED

Transcript's id obtained with Transcripts List endpoint.

Response Attributes:

audio

Audio link.

id

Transcript's ID.

participant

Participant list

description

Participant's description

name

Participant's name

role

Whether the speak is a company's executive or an analyst

quarter

Quarter of earnings result in the case of earnings call transcript.

symbol

Company symbol.

time

Time of the event.

title

Title.

transcript

Transcript content.

name

Speaker's name

session

Earnings calls section (management discussion or Q&A)

speech

Speaker's speech

year

Year of earnings result in the case of earnings call transcript.

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

print(finnhub_client.transcripts('AAPL_162777'))

Sample response

{
  "audio": "https://static.finnhub.io/transcripts_audio/4319666.mp3",
  "id": "AAPL_326091",
  "participant": [
    {
      "name": "Tejas Gala",
      "description": "Senior Analyst at Corporate Finance and IR"
    },
    {
      "name": "Tim Cook",
      "description": "CEO"
    }
  ],
  "quarter": 1,
  "symbol": "AAPL",
  "time": "2020-01-28 21:35:45",
  "title": "AAPL - Earnings call transcripts Q1 2020",
  "transcript": [
    {
      "name": "Operator",
      "speech": [
        "Good day, everyone. Welcome to the Apple Incorporated First Quarter Fiscal Year 2020 Earnings Conference Call. Today's conference is being recorded. At this time for opening remarks and introductions, I would like to turn the call over to Tejas Gala, Senior Analyst, Corporate Finance and Investor Relations. Please go ahead."
      ]
    },
    {
      "name": "Tejas Gala",
      "speech": [
        "Thank you. Good afternoon, and thank you for joining us. Speaking first today is Apple's CEO, Tim Cook, and he'll be followed by CFO, Luca Maestri. After that, we'll open the call to questions from analysts. Please note that some of the information you'll hear during our discussion today will consist of forward-looking statements, including without limitation, those regarding revenue, gross margin, operating expenses, other income and expenses, taxes, capital allocation and future business outlook. Actual results or trends could differ materially from our forecast. For more information, please refer to the risk factors discussed in Apple's most recently filed periodic reports on Form 10-K and Form 10-Q and the Form 8-K filed with the SEC today, along with the associated press release. Apple assumes no obligation to update any forward-looking statements or information, which speaks as of their respective dates. I'd now like to turn the call over to Tim for introductory remarks."
      ]
    }
  ],
  "year": 2020
}
