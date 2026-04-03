---
id: "url-41fdebd0"
type: "api"
title: "EODHD Official  Financial Assistant for ChatGPT"
url: "https://eodhd.com/financial-apis/eodhd-chatgpt-assistant"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T03:05:53.777Z"
metadata:
  endpoint: ""
  parameters: []
  markdownContent: "# EODHD Official  Financial Assistant for ChatGPT\n\n\n## Demo mode\n\nStart exploring right away! You can test me with demo data for\n                            Apple, Microsoft, and Tesla.\n                            No sign-up required - just ask me about these companies.\n\n## Sign up on eodhd.com\n\nNot a user yet? Signing up is free and gives you\n                            access to more data. Subscribing to one of our\n                            advanced plans unlocks even greater possibilities, allowing me\n                            to access an extensive range of data for your queries.\n\n## Provide your API key to the assistant\n\nOnce you sign up on eodhd.com, you’ll receive your own API key.\n                            I need this key to retrieve data for you - give it to me in the chat.\n                            Don’t worry - your key is completely secure.\n                            I only use it within your session, and I don’t store or share your information\n                            with anyone.These are the essential principles of ChatGPT.\n\n## Ask the assistant anything\n\nStart asking your questions! The first time you make a request,\n                            I’ll connect to our server to fetch the data. Once the connection\n                            is established, I’ll handle every request seamlessly. Need to save responses\n                            as files or images? Just let me know!\n\n## Questions & Answers\n\nFeel free to ask us anything related to our service & subscription plans in live chat.  You'll only find real assistants on the other end.\n\n## Code Examples\n\n```text\nimport requests\n\napi_token = \"demo\"\nticker = \"AAPL.US\"\n\n# Fetch latest EOD close price\neod_url = f\"https://eodhd.com/api/eod/{ticker}?api_token={api_token}&fmt=json&filter=close\"\neod_close = requests.get(eod_url).json()\n\n# Fetch P/E ratio\npe_url = f\"https://eodhd.com/api/fundamentals/{ticker}?api_token={api_token}&fmt=json&filter=TrailingPE\"\npe_ratio = requests.get(pe_url).json().get('TrailingPE')\n\n# Output data\nprint(f\"Apple Latest Close: ${eod_close}\")\nprint(f\"Apple P/E Ratio: {pe_ratio}\")\n```\n"
  rawContent: ""
  suggestedFilename: "eodhd-chatgpt-assistant"
---

# EODHD Official  Financial Assistant for ChatGPT

## 源URL

https://eodhd.com/financial-apis/eodhd-chatgpt-assistant

## 文档正文

## Demo mode

Start exploring right away! You can test me with demo data for
                            Apple, Microsoft, and Tesla.
                            No sign-up required - just ask me about these companies.

## Sign up on eodhd.com

Not a user yet? Signing up is free and gives you
                            access to more data. Subscribing to one of our
                            advanced plans unlocks even greater possibilities, allowing me
                            to access an extensive range of data for your queries.

## Provide your API key to the assistant

Once you sign up on eodhd.com, you’ll receive your own API key.
                            I need this key to retrieve data for you - give it to me in the chat.
                            Don’t worry - your key is completely secure.
                            I only use it within your session, and I don’t store or share your information
                            with anyone.These are the essential principles of ChatGPT.

## Ask the assistant anything

Start asking your questions! The first time you make a request,
                            I’ll connect to our server to fetch the data. Once the connection
                            is established, I’ll handle every request seamlessly. Need to save responses
                            as files or images? Just let me know!

## Questions & Answers

Feel free to ask us anything related to our service & subscription plans in live chat.  You'll only find real assistants on the other end.

## Code Examples

```text
import requests

api_token = "demo"
ticker = "AAPL.US"

# Fetch latest EOD close price
eod_url = f"https://eodhd.com/api/eod/{ticker}?api_token={api_token}&fmt=json&filter=close"
eod_close = requests.get(eod_url).json()

# Fetch P/E ratio
pe_url = f"https://eodhd.com/api/fundamentals/{ticker}?api_token={api_token}&fmt=json&filter=TrailingPE"
pe_ratio = requests.get(pe_url).json().get('TrailingPE')

# Output data
print(f"Apple Latest Close: ${eod_close}")
print(f"Apple P/E Ratio: {pe_ratio}")
```
