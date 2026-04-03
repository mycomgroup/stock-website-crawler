---
id: "url-55244243"
type: "api"
title: "Report By Dates API"
url: "https://site.financialmodelingprep.com/developer/docs/cot-reports-api"
description: ""
source: ""
tags: []
crawl_time: "2026-03-18T05:30:45.293Z"
metadata:
  markdownContent: "# Report By Dates API\n\n**Response Example:**\n\n```json\n[\n\t{\n\t\t\"symbol\": \"ZO\",\n\t\t\"date\": \"2022-08-30 00:00:00\",\n\t\t\"short_name\": \"Oats (ZO)\",\n\t\t\"sector\": \"GRAINS\",\n\t\t\"market_and_exchange_names\": \"OATS - CHICAGO BOARD OF TRADE\",\n\t\t\"cftc_contract_market_code\": \"004603\",\n\t\t\"cftc_market_code\": \"CBT\",\n\t\t\"cftc_region_code\": \"0\",\n\t\t\"cftc_commodity_code\": \"4\",\n\t\t\"open_interest_all\": 3238,\n\t\t\"noncomm_positions_long_all\": 685,\n\t\t\"noncomm_positions_short_all\": 541,\n\t\t\"noncomm_postions_spread_all\": 213,\n\t\t\"comm_positions_long_all\": 963,\n\t\t\"comm_positions_short_all\": 1348,\n\t\t\"tot_rept_positions_long_all\": 1861,\n\t\t\"tot_rept_positions_short_all\": 2102,\n\t\t\"nonrept_positions_long_all\": 1377,\n\t\t\"nonrept_positions_short_all\": 1136,\n\t\t\"open_interest_old\": 3200,\n\t\t\"noncomm_positions_long_old\": 708,\n\t\t\"noncomm_positions_short_old\": 541,\n\t\t\"noncomm_positions_spread_old\": 190,\n\t\t\"comm_positions_long_old\": 963,\n\t\t\"comm_positions_short_old\": 1348,\n\t\t\"tot_rept_positions_long_old\": 1861,\n\t\t\"tot_rept_positions_short_old\": 2079,\n\t\t\"nonrept_positions_long_old\": 1339,\n\t\t\"nonrept_positions_short_old\": 1121,\n\t\t\"open_interest_other\": 38,\n\t\t\"noncomm_positions_long_other\": 0,\n\t\t\"noncomm_positions_short_other\": 23,\n\t\t\"noncomm_positions_spread_other\": 0,\n\t\t\"comm_positions_long_other\": 0,\n\t\t\"comm_positions_short_other\": 0,\n\t\t\"tot_rept_positions_long_other\": 0,\n\t\t\"tot_rept_positions_short_other\": 23,\n\t\t\"nonrept_positions_long_other\": 38,\n\t\t\"nonrept_positions_short_other\": 15,\n\t\t\"change_in_open_interest_all\": 0,\n\t\t\"change_in_noncomm_long_all\": 0,\n\t\t\"change_in_noncomm_short_all\": 0,\n\t\t\"change_in_comm_long_all\": 0,\n\t\t\"change_in_comm_short_all\": 0,\n\t\t\"change_in_tot_rept_long_all\": 0,\n\t\t\"change_in_tot_rept_short_all\": 0,\n\t\t\"change_in_nonrept_long_all\": 0,\n\t\t\"change_in_nonrept_short_all\": 0,\n\t\t\"pct_of_open_interest_all\": 100,\n\t\t\"pct_of_oi_noncomm_long_all\": 21.2,\n\t\t\"pct_of_oi_noncomm_short_all\": 16.7,\n\t\t\"pct_of_oi_noncomm_spread_all\": 6.6,\n\t\t\"pct_of_oi_comm_long_all\": 29.7,\n\t\t\"pct_of_oi_comm_short_all\": 41.6,\n\t\t\"pct_of_oi_tot_rept_long_all\": 57.5,\n\t\t\"pct_of_oi_tot_rept_short_all\": 64.9,\n\t\t\"pct_of_oi_nonrept_long_all\": 42.5,\n\t\t\"pct_of_oi_nonrept_short_all\": 35.1,\n\t\t\"pct_of_open_interest_ol\": 100,\n\t\t\"pct_of_oi_noncomm_long_ol\": 22.1,\n\t\t\"pct_of_oi_noncomm_short_ol\": 16.9,\n\t\t\"pct_of_oi_noncomm_spread_ol\": 5.9,\n\t\t\"pct_of_oi_comm_long_ol\": 30.1,\n\t\t\"pct_of_oi_comm_short_ol\": 42.1,\n\t\t\"pct_of_oi_tot_rept_long_ol\": 58.2,\n\t\t\"pct_of_oi_tot_rept_short_ol\": 65,\n\t\t\"pct_of_oi_nonrept_long_ol\": 41.8,\n\t\t\"pct_of_oi_nonrept_short_ol\": 35,\n\t\t\"pct_of_open_interest_other\": 100,\n\t\t\"pct_of_oi_noncomm_long_other\": 0,\n\t\t\"pct_of_oi_noncomm_short_other\": 60.5,\n\t\t\"pct_of_oi_noncomm_spread_other\": 0,\n\t\t\"pct_of_oi_comm_long_other\": 0,\n\t\t\"pct_of_oi_comm_short_other\": 0,\n\t\t\"pct_of_oi_tot_rept_long_other\": 0,\n\t\t\"pct_of_oi_tot_rept_short_other\": 60.5,\n\t\t\"pct_of_oi_nonrept_long_other\": 100,\n\t\t\"pct_of_oi_nonrept_short_other\": 39.5,\n\t\t\"traders_tot_all\": 21,\n\t\t\"traders_noncomm_long_all\": 7,\n\t\t\"traders_noncomm_short_all\": 2,\n\t\t\"traders_noncomm_spread_all\": 2,\n\t\t\"traders_comm_long_all\": 8,\n\t\t\"traders_comm_short_all\": 5,\n\t\t\"traders_tot_rept_long_all\": 16,\n\t\t\"traders_tot_rept_short_all\": 9,\n\t\t\"traders_tot_ol\": 21,\n\t\t\"traders_noncomm_long_ol\": 8,\n\t\t\"traders_noncomm_short_ol\": 2,\n\t\t\"traders_noncomm_spead_ol\": 2,\n\t\t\"traders_comm_long_ol\": 8,\n\t\t\"traders_comm_short_ol\": 5,\n\t\t\"traders_tot_rept_long_ol\": 16,\n\t\t\"traders_tot_rept_short_ol\": 9,\n\t\t\"traders_tot_other\": 2,\n\t\t\"traders_noncomm_long_other\": 0,\n\t\t\"traders_noncomm_short_other\": 2,\n\t\t\"traders_noncomm_spread_other\": 0,\n\t\t\"traders_comm_long_other\": 0,\n\t\t\"traders_comm_short_other\": 0,\n\t\t\"traders_tot_rept_long_other\": 0,\n\t\t\"traders_tot_rept_short_other\": 2,\n\t\t\"conc_gross_le_4_tdr_long_all\": 24,\n\t\t\"conc_gross_le_4_tdr_short_all\": 47.7,\n\t\t\"conc_gross_le_8_tdr_long_all\": 41.3,\n\t\t\"conc_gross_le_8_tdr_short_all\": 64.5,\n\t\t\"conc_net_le_4_tdr_long_all\": 22.7,\n\t\t\"conc_net_le_4_tdr_short_all\": 45.9,\n\t\t\"conc_net_le_8_tdr_long_all\": 38.6,\n\t\t\"conc_net_le_8_tdr_short_all\": 57,\n\t\t\"conc_gross_le_4_tdr_long_ol\": 24.3,\n\t\t\"conc_gross_le_4_tdr_short_ol\": 48,\n\t\t\"conc_gross_le_8_tdr_long_ol\": 41.8,\n\t\t\"conc_gross_le_8_tdr_short_ol\": 64.9,\n\t\t\"conc_net_le_4_tdr_long_ol\": 23,\n\t\t\"conc_net_le_4_tdr_short_ol\": 46.4,\n\t\t\"conc_net_le_8_tdr_long_ol\": 39,\n\t\t\"conc_net_le_8_tdr_short_ol\": 57.7,\n\t\t\"conc_gross_le_4_tdr_long_other\": 0,\n\t\t\"conc_gross_le_4_tdr_short_other\": 60.5,\n\t\t\"conc_gross_le_8_tdr_long_other\": 0,\n\t\t\"conc_gross_le_8_tdr_short_other\": 60.5,\n\t\t\"conc_net_le_4_tdr_long_other\": 0,\n\t\t\"conc_net_le_4_tdr_short_other\": 60.5,\n\t\t\"conc_net_le_8_tdr_long_other\": 0,\n\t\t\"conc_net_le_8_tdr_short_other\": 60.5,\n\t\t\"contract_units\": \"(CONTRACTS OF 5,000 BUSHELS)\",\n\t\t\"updatedAt\": \"2022-09-02T19:30:25.920Z\",\n\t\t\"createdAt\": \"2022-09-02T19:30:25.920Z\",\n\t\t\"as_of_date_in_form_yymmdd\": \"220830\",\n\t\t\"change_in_noncomm_spead_all\": 0\n\t}\n]\n```\n\n\n## About Report By Dates API\n\nReport By Dates endpoint provides a full COT report for a given date range. This report includes information such as the net long and net short positions of different types of market participants, the change in these positions over time, the open interest for all symbols, and the speculative positioning index.\nInvestors can use the Commitment of Traders: Report By Dates endpoint to:\nGet a detailed overview of the COT report for a given date range.\nCompare the positions of all types of market participants over time.\nIdentify trends in market sentiment over a period of time.\nMake informed trading decisions based on the full COT report for a given date range.\n\n**Endpoint:**\n\n```text\nhttps://financialmodelingprep.com/api/v4/commitment_of_traders_report?from=2023-08-10&to=2023-10-10\n```\n\n\n## Related Report By Dates APIs\n\n\n## Report By Dates API FAQs\n\n\n## Unlock Premium Financial Insights Today!\n"
  rawContent: ""
  suggestedFilename: "cot-reports-api"
---

# Report By Dates API

## 源URL

https://site.financialmodelingprep.com/developer/docs/cot-reports-api

## 文档正文

**Response Example:**

```json
[
	{
		"symbol": "ZO",
		"date": "2022-08-30 00:00:00",
		"short_name": "Oats (ZO)",
		"sector": "GRAINS",
		"market_and_exchange_names": "OATS - CHICAGO BOARD OF TRADE",
		"cftc_contract_market_code": "004603",
		"cftc_market_code": "CBT",
		"cftc_region_code": "0",
		"cftc_commodity_code": "4",
		"open_interest_all": 3238,
		"noncomm_positions_long_all": 685,
		"noncomm_positions_short_all": 541,
		"noncomm_postions_spread_all": 213,
		"comm_positions_long_all": 963,
		"comm_positions_short_all": 1348,
		"tot_rept_positions_long_all": 1861,
		"tot_rept_positions_short_all": 2102,
		"nonrept_positions_long_all": 1377,
		"nonrept_positions_short_all": 1136,
		"open_interest_old": 3200,
		"noncomm_positions_long_old": 708,
		"noncomm_positions_short_old": 541,
		"noncomm_positions_spread_old": 190,
		"comm_positions_long_old": 963,
		"comm_positions_short_old": 1348,
		"tot_rept_positions_long_old": 1861,
		"tot_rept_positions_short_old": 2079,
		"nonrept_positions_long_old": 1339,
		"nonrept_positions_short_old": 1121,
		"open_interest_other": 38,
		"noncomm_positions_long_other": 0,
		"noncomm_positions_short_other": 23,
		"noncomm_positions_spread_other": 0,
		"comm_positions_long_other": 0,
		"comm_positions_short_other": 0,
		"tot_rept_positions_long_other": 0,
		"tot_rept_positions_short_other": 23,
		"nonrept_positions_long_other": 38,
		"nonrept_positions_short_other": 15,
		"change_in_open_interest_all": 0,
		"change_in_noncomm_long_all": 0,
		"change_in_noncomm_short_all": 0,
		"change_in_comm_long_all": 0,
		"change_in_comm_short_all": 0,
		"change_in_tot_rept_long_all": 0,
		"change_in_tot_rept_short_all": 0,
		"change_in_nonrept_long_all": 0,
		"change_in_nonrept_short_all": 0,
		"pct_of_open_interest_all": 100,
		"pct_of_oi_noncomm_long_all": 21.2,
		"pct_of_oi_noncomm_short_all": 16.7,
		"pct_of_oi_noncomm_spread_all": 6.6,
		"pct_of_oi_comm_long_all": 29.7,
		"pct_of_oi_comm_short_all": 41.6,
		"pct_of_oi_tot_rept_long_all": 57.5,
		"pct_of_oi_tot_rept_short_all": 64.9,
		"pct_of_oi_nonrept_long_all": 42.5,
		"pct_of_oi_nonrept_short_all": 35.1,
		"pct_of_open_interest_ol": 100,
		"pct_of_oi_noncomm_long_ol": 22.1,
		"pct_of_oi_noncomm_short_ol": 16.9,
		"pct_of_oi_noncomm_spread_ol": 5.9,
		"pct_of_oi_comm_long_ol": 30.1,
		"pct_of_oi_comm_short_ol": 42.1,
		"pct_of_oi_tot_rept_long_ol": 58.2,
		"pct_of_oi_tot_rept_short_ol": 65,
		"pct_of_oi_nonrept_long_ol": 41.8,
		"pct_of_oi_nonrept_short_ol": 35,
		"pct_of_open_interest_other": 100,
		"pct_of_oi_noncomm_long_other": 0,
		"pct_of_oi_noncomm_short_other": 60.5,
		"pct_of_oi_noncomm_spread_other": 0,
		"pct_of_oi_comm_long_other": 0,
		"pct_of_oi_comm_short_other": 0,
		"pct_of_oi_tot_rept_long_other": 0,
		"pct_of_oi_tot_rept_short_other": 60.5,
		"pct_of_oi_nonrept_long_other": 100,
		"pct_of_oi_nonrept_short_other": 39.5,
		"traders_tot_all": 21,
		"traders_noncomm_long_all": 7,
		"traders_noncomm_short_all": 2,
		"traders_noncomm_spread_all": 2,
		"traders_comm_long_all": 8,
		"traders_comm_short_all": 5,
		"traders_tot_rept_long_all": 16,
		"traders_tot_rept_short_all": 9,
		"traders_tot_ol": 21,
		"traders_noncomm_long_ol": 8,
		"traders_noncomm_short_ol": 2,
		"traders_noncomm_spead_ol": 2,
		"traders_comm_long_ol": 8,
		"traders_comm_short_ol": 5,
		"traders_tot_rept_long_ol": 16,
		"traders_tot_rept_short_ol": 9,
		"traders_tot_other": 2,
		"traders_noncomm_long_other": 0,
		"traders_noncomm_short_other": 2,
		"traders_noncomm_spread_other": 0,
		"traders_comm_long_other": 0,
		"traders_comm_short_other": 0,
		"traders_tot_rept_long_other": 0,
		"traders_tot_rept_short_other": 2,
		"conc_gross_le_4_tdr_long_all": 24,
		"conc_gross_le_4_tdr_short_all": 47.7,
		"conc_gross_le_8_tdr_long_all": 41.3,
		"conc_gross_le_8_tdr_short_all": 64.5,
		"conc_net_le_4_tdr_long_all": 22.7,
		"conc_net_le_4_tdr_short_all": 45.9,
		"conc_net_le_8_tdr_long_all": 38.6,
		"conc_net_le_8_tdr_short_all": 57,
		"conc_gross_le_4_tdr_long_ol": 24.3,
		"conc_gross_le_4_tdr_short_ol": 48,
		"conc_gross_le_8_tdr_long_ol": 41.8,
		"conc_gross_le_8_tdr_short_ol": 64.9,
		"conc_net_le_4_tdr_long_ol": 23,
		"conc_net_le_4_tdr_short_ol": 46.4,
		"conc_net_le_8_tdr_long_ol": 39,
		"conc_net_le_8_tdr_short_ol": 57.7,
		"conc_gross_le_4_tdr_long_other": 0,
		"conc_gross_le_4_tdr_short_other": 60.5,
		"conc_gross_le_8_tdr_long_other": 0,
		"conc_gross_le_8_tdr_short_other": 60.5,
		"conc_net_le_4_tdr_long_other": 0,
		"conc_net_le_4_tdr_short_other": 60.5,
		"conc_net_le_8_tdr_long_other": 0,
		"conc_net_le_8_tdr_short_other": 60.5,
		"contract_units": "(CONTRACTS OF 5,000 BUSHELS)",
		"updatedAt": "2022-09-02T19:30:25.920Z",
		"createdAt": "2022-09-02T19:30:25.920Z",
		"as_of_date_in_form_yymmdd": "220830",
		"change_in_noncomm_spead_all": 0
	}
]
```

## About Report By Dates API

Report By Dates endpoint provides a full COT report for a given date range. This report includes information such as the net long and net short positions of different types of market participants, the change in these positions over time, the open interest for all symbols, and the speculative positioning index.
Investors can use the Commitment of Traders: Report By Dates endpoint to:
Get a detailed overview of the COT report for a given date range.
Compare the positions of all types of market participants over time.
Identify trends in market sentiment over a period of time.
Make informed trading decisions based on the full COT report for a given date range.

**Endpoint:**

```text
https://financialmodelingprep.com/api/v4/commitment_of_traders_report?from=2023-08-10&to=2023-10-10
```

## Related Report By Dates APIs

## Report By Dates API FAQs

## Unlock Premium Financial Insights Today!
