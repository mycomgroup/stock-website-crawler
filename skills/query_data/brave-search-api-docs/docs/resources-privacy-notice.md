---
id: "url-1a15be2"
type: "api"
title: "Privacy notice"
url: "https://api-dashboard.search.brave.com/documentation/resources/privacy-notice"
description: "You must create an account and subscribe to a plan to gain access to the Brave\nSearch API. Data types marked with * indicate mandatory fields. You will need\nto provide payment details, and your postal address and billing details.\nPayment information is processed and held by Stripe and is subject to Stripe’s privacy policy. Brave\ndoes not have access to the personal data processed by Stripe. All subscription\nplans require payment information (this is to help us safeguard against misuse\nof the service)."
source: ""
tags: []
crawl_time: "2026-03-18T03:28:44.718Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/web/search"
  method: "GET"
  sections:
    - {"level":"H3","title":"FOR API CUSTOMERS","content":["You must create an account and subscribe to a plan to gain access to the Brave\nSearch API. Data types marked with * indicate mandatory fields. You will need\nto provide payment details, and your postal address and billing details.\nPayment information is processed and held by Stripe and is subject to Stripe’s privacy policy. Brave\ndoes not have access to the personal data processed by Stripe. All subscription\nplans require payment information (this is to help us safeguard against misuse\nof the service).","A record of search queries submitted to the Brave Search API via a customer’s\nSearch API account is retained for a maximum of 90 days for the purpose of billing\nSearch API account holders and for troubleshooting subject to Brave’s legal\nobligations.","As per Section 3b of the Terms Of Service the Brave Search\nAPI customer (Licensee) is solely responsible for complying with applicable data\nprotection law including the posting of any privacy notice with regard to queries\nsubmitted by end users via the customer’s API access. Brave does not collect any\nidentifiers that can link a search query to an individual or their devices.","You can contact our data protection officer at privacy@brave.com should you have any privacy enquiries\nabout the use of account related data, and to the extent that a search query\ninvolves the processing of personal data."],"codeBlocks":[]}
    - {"level":"H3","title":"Brave Search API and Personal Data","content":["Brave takes the position that query data sent to Brave Search API is not personal\ndata under laws like the General Data Protection Regulation (GDPR). Brave Search\nAPI acts as a conduit – we act on data requests made by our customer’s systems and\nservices, and return search results from our index. It’s no different than\nconducting a search on https://search.brave.com, except\nthat instead of a person doing the search, a computer is doing it via a programmatic\ncall (the Brave Search API).","For our customers, search queries may be personal data, because they may have other\ninformation or means that allow them to link back or identify a particular user or\nquery. But Brave has no way to identify which “end user” made any specific query, only\nthat a customer’s account is making an API call. We have no idea who actually made the\nquery, or whether a given query was even about an identifiable individual.","This is why we specifically exclude Search Query Data in our Data Processing Addendum.","Purpose of processingCategories of personal data processedLegal basis of processingDuration of storageTo create and manage account accessEmail address, full name and account UID (assigned by Brave), API KeyNecessary for the performance of a contractFor data retained after account closure: Legitimate interestsCompliance with legal obligations12 months from when an account is deleted.To provide customer supportUser ID, user email, IP address, other information provided by account holderNecessary for the performance of a contractMaximum 6 years.To process paymentsHashed Stripe identifier, Last 4 credit, expiration dateNecessary for the performance of a contractFor data retained after account closure: Legitimate interests12 months from when an account is deleted.InvoicingAccount information, client contact information, billing details.Necessary for the performance of a contractReturned after contract termination.To resolve billing queries and troubleshootingIP address, authentication tokenNecessary for the performance of a contractFor data retained after account closure: Legitimate interestsSearch Query Logs: 90 days.Option for Zero Data Retention (Enterprise clients), subject to Brave’s legal obligations.Other Data: 12 months from when an account is deleted.To prevent abuse of the Search APIIP address, authentication tokenLegitimate interests.Search Query Logs: 90 days.Option for Zero Data Retention (Enterprise clients), subject to Brave’s legal obligations.Other Data: 12 months from when an account is deleted.Compliance with Brave’s legal obligationsIP address, authentication token, account informationCompliance with legal obligationsTo the extent required by law.","List of sub-processors can be found in Annex IV of the data processing addendum."],"codeBlocks":[]}
  tables:
    - {"index":0,"headers":["Purpose of processing","Categories of personal data processed","Legal basis of processing","Duration of storage"],"rows":[["To create and manage account access","Email address, full name and account UID (assigned by Brave), API Key","Necessary for the performance of a contractFor data retained after account closure: Legitimate interestsCompliance with legal obligations","12 months from when an account is deleted."],["To provide customer support","User ID, user email, IP address, other information provided by account holder","Necessary for the performance of a contract","Maximum 6 years."],["To process payments","Hashed Stripe identifier, Last 4 credit, expiration date","Necessary for the performance of a contractFor data retained after account closure: Legitimate interests","12 months from when an account is deleted."],["Invoicing","Account information, client contact information, billing details.","Necessary for the performance of a contract","Returned after contract termination."],["To resolve billing queries and troubleshooting","IP address, authentication token","Necessary for the performance of a contractFor data retained after account closure: Legitimate interests","Search Query Logs: 90 days.Option for Zero Data Retention (Enterprise clients), subject to Brave’s legal obligations.Other Data: 12 months from when an account is deleted."],["To prevent abuse of the Search API","IP address, authentication token","Legitimate interests.","Search Query Logs: 90 days.Option for Zero Data Retention (Enterprise clients), subject to Brave’s legal obligations.Other Data: 12 months from when an account is deleted."],["Compliance with Brave’s legal obligations","IP address, authentication token, account information","Compliance with legal obligations","To the extent required by law."]]}
  examples: []
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nResources\n\nPrivacy notice for Brave Search API customers\n\nUpdated 4 December 2025\n\nThe Brave Search API is provided by Brave Software Inc located in the U.S.\n\nFOR API CUSTOMERS\n\nYou must create an account and subscribe to a plan to gain access to the Brave\nSearch API. Data types marked with * indicate mandatory fields. You will need\nto provide payment details, and your postal address and billing details.\nPayment information is processed and held by Stripe and is subject to Stripe’s privacy policy. Brave\ndoes not have access to the personal data processed by Stripe. All subscription\nplans require payment information (this is to help us safeguard against misuse\nof the service).\n\nA record of search queries submitted to the Brave Search API via a customer’s\nSearch API account is retained for a maximum of 90 days for the purpose of billing\nSearch API account holders and for troubleshooting subject to Brave’s legal\nobligations.\n\nAs per Section 3b of the Terms Of Service the Brave Search\nAPI customer (Licensee) is solely responsible for complying with applicable data\nprotection law including the posting of any privacy notice with regard to queries\nsubmitted by end users via the customer’s API access. Brave does not collect any\nidentifiers that can link a search query to an individual or their devices.\n\nYou can contact our data protection officer at privacy@brave.com should you have any privacy enquiries\nabout the use of account related data, and to the extent that a search query\ninvolves the processing of personal data.\n\nBrave Search API and Personal Data\n\nBrave takes the position that query data sent to Brave Search API is not personal\ndata under laws like the General Data Protection Regulation (GDPR). Brave Search\nAPI acts as a conduit – we act on data requests made by our customer’s systems and\nservices, and return search results from our index. It’s no different than\nconducting a search on https://search.brave.com, except\nthat instead of a person doing the search, a computer is doing it via a programmatic\ncall (the Brave Search API).\n\nFor our customers, search queries may be personal data, because they may have other\ninformation or means that allow them to link back or identify a particular user or\nquery. But Brave has no way to identify which “end user” made any specific query, only\nthat a customer’s account is making an API call. We have no idea who actually made the\nquery, or whether a given query was even about an identifiable individual.\n\nThis is why we specifically exclude Search Query Data in our Data Processing Addendum.\n\nList of sub-processors can be found in Annex IV of the data processing addendum.\n\nSee our data processing addendum here.\n\nOn this page"
  suggestedFilename: "resources-privacy-notice"
---

# Privacy notice

## 源URL

https://api-dashboard.search.brave.com/documentation/resources/privacy-notice

## 描述

You must create an account and subscribe to a plan to gain access to the Brave
Search API. Data types marked with * indicate mandatory fields. You will need
to provide payment details, and your postal address and billing details.
Payment information is processed and held by Stripe and is subject to Stripe’s privacy policy. Brave
does not have access to the personal data processed by Stripe. All subscription
plans require payment information (this is to help us safeguard against misuse
of the service).

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/web/search`

## 文档正文

You must create an account and subscribe to a plan to gain access to the Brave
Search API. Data types marked with * indicate mandatory fields. You will need
to provide payment details, and your postal address and billing details.
Payment information is processed and held by Stripe and is subject to Stripe’s privacy policy. Brave
does not have access to the personal data processed by Stripe. All subscription
plans require payment information (this is to help us safeguard against misuse
of the service).

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/web/search`

Quickstart

Pricing

Authentication

Versioning

Rate limiting

Web search

LLM Context New

News search

Video search

Image search

Summarizer search

Place search New

Answers

Autosuggest

Spellcheck

Skills

Help & Feedback

Goggles

Search operators

Status updates

Security

Privacy notice

Terms of service

Resources

Privacy notice for Brave Search API customers

Updated 4 December 2025

The Brave Search API is provided by Brave Software Inc located in the U.S.

FOR API CUSTOMERS

You must create an account and subscribe to a plan to gain access to the Brave
Search API. Data types marked with * indicate mandatory fields. You will need
to provide payment details, and your postal address and billing details.
Payment information is processed and held by Stripe and is subject to Stripe’s privacy policy. Brave
does not have access to the personal data processed by Stripe. All subscription
plans require payment information (this is to help us safeguard against misuse
of the service).

A record of search queries submitted to the Brave Search API via a customer’s
Search API account is retained for a maximum of 90 days for the purpose of billing
Search API account holders and for troubleshooting subject to Brave’s legal
obligations.

As per Section 3b of the Terms Of Service the Brave Search
API customer (Licensee) is solely responsible for complying with applicable data
protection law including the posting of any privacy notice with regard to queries
submitted by end users via the customer’s API access. Brave does not collect any
identifiers that can link a search query to an individual or their devices.

You can contact our data protection officer at privacy@brave.com should you have any privacy enquiries
about the use of account related data, and to the extent that a search query
involves the processing of personal data.

Brave Search API and Personal Data

Brave takes the position that query data sent to Brave Search API is not personal
data under laws like the General Data Protection Regulation (GDPR). Brave Search
API acts as a conduit – we act on data requests made by our customer’s systems and
services, and return search results from our index. It’s no different than
conducting a search on https://search.brave.com, except
that instead of a person doing the search, a computer is doing it via a programmatic
call (the Brave Search API).

For our customers, search queries may be personal data, because they may have other
information or means that allow them to link back or identify a particular user or
query. But Brave has no way to identify which “end user” made any specific query, only
that a customer’s account is making an API call. We have no idea who actually made the
query, or whether a given query was even about an identifiable individual.

This is why we specifically exclude Search Query Data in our Data Processing Addendum.

List of sub-processors can be found in Annex IV of the data processing addendum.

See our data processing addendum here.

On this page
