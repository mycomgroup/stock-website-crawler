---
id: "url-a266a87"
type: "api"
title: "Versioning"
url: "https://api-dashboard.search.brave.com/documentation/guides/versioning"
description: "The first is a major version number (e.g. v1) included in the\nAPI URL. An example URL will look something like this /v1/web/search.\nAs a user, you can expect this version to be rarely changed, but we\nreserve the right to do so. These will only be used when there is a\nmajor API redesign, which should happen only rarely, and naturally\nwould warrant a major upgrade."
source: ""
tags: []
crawl_time: "2026-03-18T02:32:14.739Z"
metadata:
  endpoint: "https://api.search.brave.com/res/v1/web/search?q=brave+search"
  method: "GET"
  sections:
    - {"level":"H2","title":"1. Versioning in Request URL","content":["The first is a major version number (e.g. v1) included in the\nAPI URL. An example URL will look something like this /v1/web/search.\nAs a user, you can expect this version to be rarely changed, but we\nreserve the right to do so. These will only be used when there is a\nmajor API redesign, which should happen only rarely, and naturally\nwould warrant a major upgrade."],"codeBlocks":[]}
    - {"level":"H2","title":"2. Versioning in Request Header","content":["Backwards\nincompatible changes, which require an upgrade path and are dated with\nthe format YYYY-MM-DD. Without a version header, API requests default\nto the latest version. The API behavior can be locked to a\nspecific version by providing a version header named Api-Version as\npart of the request. An example version header will look something\nlike Api-Version: 2023-01-01.","Changes made to the API can be backwards compatible or incompatible.\nTo learn more about which changes are considered backwards compatible\nor incompatible, read below.","API requests default to latest version if no Api-Version header is specified."],"codeBlocks":[]}
    - {"level":"H2","title":"Backwards compatible changes","content":["Brave Search considers the following changes to be backwards compatible,\nand they will not require action from the API user:","• Adding new optional request parameters or headers to APIs that already exist.\n• Adding new properties to an existing API response.\n• Adding new API resources.\n• Changing the order of properties in an existing API response.\n• Changing the length and format of string values. e.g. object IDs, urls,\ndisplay strings."],"codeBlocks":[]}
    - {"level":"H2","title":"Backwards incompatible changes","content":["Brave Search considers the following changes to be backwards\nincompatible, and they will require action from the API user\n(provided the API user has updated to the new API version):","• Removing an existing request parameter or header from the API request.\n• Removing properties from an existing API response.\n• Renaming properties in an existing API response.\n• Changing the value type of properties in an existing API response."],"codeBlocks":[]}
  tables: []
  examples:
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=brave+search\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\" \\\n  -H \"Api-Version: 2023-01-01\""}
    - {"type":"request","language":"bash","code":"curl \"https://api.search.brave.com/res/v1/web/search?q=brave+search\" \\\n  -H \"X-Subscription-Token: YOUR_API_KEY\" \\\n  -H \"Api-Version: 2023-01-01\""}
  rawContent: "Quickstart\n\nPricing\n\nAuthentication\n\nVersioning\n\nRate limiting\n\nWeb search\n\nLLM Context New\n\nNews search\n\nVideo search\n\nImage search\n\nSummarizer search\n\nPlace search New\n\nAnswers\n\nAutosuggest\n\nSpellcheck\n\nSkills\n\nHelp & Feedback\n\nGoggles\n\nSearch operators\n\nStatus updates\n\nSecurity\n\nPrivacy notice\n\nTerms of service\n\nBasics\n\nHow API versioning works and what changes to expect between versions\n\nThe Brave Search API is evolving rapidly, with new iterations released\nall the time. However, we know that changing an existing API can be\ndisruptive, and that API developers can quickly lose flexibility\nto make changes as users start consuming their API. A common way to mitigate this is to\nadd some form of versioning to the published API so users can fully\nrely on the API’s behavior. When you’re ready for an API change, you’ll\nthen have an easy upgrade path forward provided by the API developers.\n\nWith Brave Search, you can expect two types of versioning schemes.\n\n1. Versioning in Request URL\n\nThe first is a major version number (e.g. v1) included in the\nAPI URL. An example URL will look something like this /v1/web/search.\nAs a user, you can expect this version to be rarely changed, but we\nreserve the right to do so. These will only be used when there is a\nmajor API redesign, which should happen only rarely, and naturally\nwould warrant a major upgrade.\n\n2. Versioning in Request Header\n\nBackwards\nincompatible changes, which require an upgrade path and are dated with\nthe format YYYY-MM-DD. Without a version header, API requests default\nto the latest version. The API behavior can be locked to a\nspecific version by providing a version header named Api-Version as\npart of the request. An example version header will look something\nlike Api-Version: 2023-01-01.\n\nChanges made to the API can be backwards compatible or incompatible.\nTo learn more about which changes are considered backwards compatible\nor incompatible, read below.\n\nAPI requests default to latest version if no Api-Version header is specified.\n\nBackwards compatible changes\n\nBrave Search considers the following changes to be backwards compatible,\nand they will not require action from the API user:\n\nAdding new optional request parameters or headers to APIs that already exist.\n\nAdding new properties to an existing API response.\n\nAdding new API resources.\n\nChanging the order of properties in an existing API response.\n\nChanging the length and format of string values. e.g. object IDs, urls,\ndisplay strings.\n\nBackwards incompatible changes\n\nBrave Search considers the following changes to be backwards\nincompatible, and they will require action from the API user\n(provided the API user has updated to the new API version):\n\nRemoving an existing request parameter or header from the API request.\n\nRemoving properties from an existing API response.\n\nRenaming properties in an existing API response.\n\nChanging the value type of properties in an existing API response.\n\nOn this page"
  suggestedFilename: "guides-versioning"
---

# Versioning

## 源URL

https://api-dashboard.search.brave.com/documentation/guides/versioning

## 描述

The first is a major version number (e.g. v1) included in the
API URL. An example URL will look something like this /v1/web/search.
As a user, you can expect this version to be rarely changed, but we
reserve the right to do so. These will only be used when there is a
major API redesign, which should happen only rarely, and naturally
would warrant a major upgrade.

## API 端点

**Method**: `GET`
**Endpoint**: `https://api.search.brave.com/res/v1/web/search?q=brave+search`

## 代码示例

```bash
curl "https://api.search.brave.com/res/v1/web/search?q=brave+search" \
  -H "X-Subscription-Token: YOUR_API_KEY" \
  -H "Api-Version: 2023-01-01"
```

## 文档正文

The first is a major version number (e.g. v1) included in the
API URL. An example URL will look something like this /v1/web/search.
As a user, you can expect this version to be rarely changed, but we
reserve the right to do so. These will only be used when there is a
major API redesign, which should happen only rarely, and naturally
would warrant a major upgrade.

## API 端点

**Method:** `GET`
**Endpoint:** `https://api.search.brave.com/res/v1/web/search?q=brave+search`

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

Basics

How API versioning works and what changes to expect between versions

The Brave Search API is evolving rapidly, with new iterations released
all the time. However, we know that changing an existing API can be
disruptive, and that API developers can quickly lose flexibility
to make changes as users start consuming their API. A common way to mitigate this is to
add some form of versioning to the published API so users can fully
rely on the API’s behavior. When you’re ready for an API change, you’ll
then have an easy upgrade path forward provided by the API developers.

With Brave Search, you can expect two types of versioning schemes.

1. Versioning in Request URL

The first is a major version number (e.g. v1) included in the
API URL. An example URL will look something like this /v1/web/search.
As a user, you can expect this version to be rarely changed, but we
reserve the right to do so. These will only be used when there is a
major API redesign, which should happen only rarely, and naturally
would warrant a major upgrade.

2. Versioning in Request Header

Backwards
incompatible changes, which require an upgrade path and are dated with
the format YYYY-MM-DD. Without a version header, API requests default
to the latest version. The API behavior can be locked to a
specific version by providing a version header named Api-Version as
part of the request. An example version header will look something
like Api-Version: 2023-01-01.

Changes made to the API can be backwards compatible or incompatible.
To learn more about which changes are considered backwards compatible
or incompatible, read below.

API requests default to latest version if no Api-Version header is specified.

Backwards compatible changes

Brave Search considers the following changes to be backwards compatible,
and they will not require action from the API user:

Adding new optional request parameters or headers to APIs that already exist.

Adding new properties to an existing API response.

Adding new API resources.

Changing the order of properties in an existing API response.

Changing the length and format of string values. e.g. object IDs, urls,
display strings.

Backwards incompatible changes

Brave Search considers the following changes to be backwards
incompatible, and they will require action from the API user
(provided the API user has updated to the new API version):

Removing an existing request parameter or header from the API request.

Removing properties from an existing API response.

Renaming properties in an existing API response.

Changing the value type of properties in an existing API response.

On this page
