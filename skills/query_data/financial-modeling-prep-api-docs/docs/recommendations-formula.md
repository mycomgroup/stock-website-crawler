---
id: "url-738f7617"
type: "api"
title: "Recommend Formula - Financial Modeling Prep API"
url: "https://site.financialmodelingprep.com/developer/docs/recommendations-formula"
description: "DCF: [ 0.3, 0.05, -0.1, -0.3 ]\nROE: [ 0.3, 0.05, -0.1, -0.3 ]\nROA: [ 0.3, 0.05, -0.1, -0.3 ]\nDebt to equity ratio: [ 2, 0.5, -0.5, -3 ]\nPrice to earnings ratio: [ 8, 0.5, -0.5, -3 ]\nPrice to book ratio: [ 1, 0.5, -0.5, -2 ]\nTotal Score: [ 25, 20, 15, 10 ]"
source: ""
tags: []
crawl_time: "2026-03-18T08:46:15.296Z"
metadata:
  markdownContent: "# Recommend Formula - Financial Modeling Prep API\n\nDCF: [ 0.3, 0.05, -0.1, -0.3 ]\nROE: [ 0.3, 0.05, -0.1, -0.3 ]\nROA: [ 0.3, 0.05, -0.1, -0.3 ]\nDebt to equity ratio: [ 2, 0.5, -0.5, -3 ]\nPrice to earnings ratio: [ 8, 0.5, -0.5, -3 ]\nPrice to book ratio: [ 1, 0.5, -0.5, -2 ]\nTotal Score: [ 25, 20, 15, 10 ]\n\n\n#### 1. ASSUMPTIONS\n\nDCF: [ 0.3, 0.05, -0.1, -0.3 ]\nROE: [ 0.3, 0.05, -0.1, -0.3 ]\nROA: [ 0.3, 0.05, -0.1, -0.3 ]\nDebt to equity ratio: [ 2, 0.5, -0.5, -3 ]\nPrice to earnings ratio: [ 8, 0.5, -0.5, -3 ]\nPrice to book ratio: [ 1, 0.5, -0.5, -2 ]\nTotal Score: [ 25, 20, 15, 10 ]\n\n\n#### 2. Individual Calculations\n\nEvery number in brackets represent part of range that is used to determine score and recommendation. First number is the best and last number is the worst.\n\nDetailed breakdown of ranges:\n\nIf value is higher than first number in brackets, the score will be 5 and recommendation would be \"Strong Buy\".\n\nIf value is higher than second number and lower than first number, the score will be 4 and recommendation would be \"Buy\".\n\nIf value is higher than third number and lower than second number, the score will be 3 and recommendation would be \"Neutral\".\n\nIf value is higher than fourth number and lower than third number, the score will be 2 and recommendation would be \"Sell\".\n\nIf value is lower than fourth number, the score will be 1 and recommendation would be \"Strong Sell\".\n\n\n#### 3. Main Rating Calculations\n\nTo calculate main rating for stock we add scores of other individual values. Fields named \"ratingScore\" and \"ratingRecommendation\" are based on conditions above. Only difference is \"rating\" field.\n\nConditions for \"rating\" are:\n\nIf score is higher than 30, rating would be \"S+\"\n\nIf score is higher than 28 and lower than 30, rating would be \"S\"\n\nIf score is higher than 26 and lower than 28, rating would be \"S-\"\n\nIf score is higher than 24 and lower than 26, rating would be \"A+\"\n\nIf score is higher than 22 and lower than 24, rating would be \"A\"\n\nIf score is higher than 20 and lower than 22, rating would be \"A-\"\n\nIf score is higher than 18 and lower than 20, rating would be \"B+\"\n\nIf score is higher than 16 and lower than 18, rating would be \"B\"\n\nIf score is higher than 14 and lower than 16, rating would be \"B-\"\n\nIf score is higher than 12 and lower than 14, rating would be \"C+\"\n\nIf score is higher than 10 and lower than 12, rating would be \"C\"\n\nIf score is higher than 8 and lower than 10, rating would be \"C-\"\n\nIf score is higher than 6 and lower than 8, rating would be \"D+\"\n\nIf score is higher than 4 and lower than 6, rating would be \"D\"\n\nIf score is higher than 2 and lower than 4, rating would be \"D-\"\n\n\n#### Stay Ahead with Fresh Data!\n\nYour session has been inactive. For the latest financial insights, please refresh.\n\nRefresh Now\n"
  rawContent: ""
  suggestedFilename: "recommendations-formula"
---

# Recommend Formula - Financial Modeling Prep API

## 源URL

https://site.financialmodelingprep.com/developer/docs/recommendations-formula

## 描述

DCF: [ 0.3, 0.05, -0.1, -0.3 ]
ROE: [ 0.3, 0.05, -0.1, -0.3 ]
ROA: [ 0.3, 0.05, -0.1, -0.3 ]
Debt to equity ratio: [ 2, 0.5, -0.5, -3 ]
Price to earnings ratio: [ 8, 0.5, -0.5, -3 ]
Price to book ratio: [ 1, 0.5, -0.5, -2 ]
Total Score: [ 25, 20, 15, 10 ]

## 文档正文

DCF: [ 0.3, 0.05, -0.1, -0.3 ]
ROE: [ 0.3, 0.05, -0.1, -0.3 ]
ROA: [ 0.3, 0.05, -0.1, -0.3 ]
Debt to equity ratio: [ 2, 0.5, -0.5, -3 ]
Price to earnings ratio: [ 8, 0.5, -0.5, -3 ]
Price to book ratio: [ 1, 0.5, -0.5, -2 ]
Total Score: [ 25, 20, 15, 10 ]

#### 1. ASSUMPTIONS

DCF: [ 0.3, 0.05, -0.1, -0.3 ]
ROE: [ 0.3, 0.05, -0.1, -0.3 ]
ROA: [ 0.3, 0.05, -0.1, -0.3 ]
Debt to equity ratio: [ 2, 0.5, -0.5, -3 ]
Price to earnings ratio: [ 8, 0.5, -0.5, -3 ]
Price to book ratio: [ 1, 0.5, -0.5, -2 ]
Total Score: [ 25, 20, 15, 10 ]

#### 2. Individual Calculations

Every number in brackets represent part of range that is used to determine score and recommendation. First number is the best and last number is the worst.

Detailed breakdown of ranges:

If value is higher than first number in brackets, the score will be 5 and recommendation would be "Strong Buy".

If value is higher than second number and lower than first number, the score will be 4 and recommendation would be "Buy".

If value is higher than third number and lower than second number, the score will be 3 and recommendation would be "Neutral".

If value is higher than fourth number and lower than third number, the score will be 2 and recommendation would be "Sell".

If value is lower than fourth number, the score will be 1 and recommendation would be "Strong Sell".

#### 3. Main Rating Calculations

To calculate main rating for stock we add scores of other individual values. Fields named "ratingScore" and "ratingRecommendation" are based on conditions above. Only difference is "rating" field.

Conditions for "rating" are:

If score is higher than 30, rating would be "S+"

If score is higher than 28 and lower than 30, rating would be "S"

If score is higher than 26 and lower than 28, rating would be "S-"

If score is higher than 24 and lower than 26, rating would be "A+"

If score is higher than 22 and lower than 24, rating would be "A"

If score is higher than 20 and lower than 22, rating would be "A-"

If score is higher than 18 and lower than 20, rating would be "B+"

If score is higher than 16 and lower than 18, rating would be "B"

If score is higher than 14 and lower than 16, rating would be "B-"

If score is higher than 12 and lower than 14, rating would be "C+"

If score is higher than 10 and lower than 12, rating would be "C"

If score is higher than 8 and lower than 10, rating would be "C-"

If score is higher than 6 and lower than 8, rating would be "D+"

If score is higher than 4 and lower than 6, rating would be "D"

If score is higher than 2 and lower than 4, rating would be "D-"

#### Stay Ahead with Fresh Data!

Your session has been inactive. For the latest financial insights, please refresh.

Refresh Now
