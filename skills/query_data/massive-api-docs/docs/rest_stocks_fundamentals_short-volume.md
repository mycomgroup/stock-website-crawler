# Short Volume

## 源URL

https://massive.com/docs/rest/stocks/fundamentals/short-volume

## 描述

Retrieve daily aggregated short sale volume data reported to FINRA from off-exchange trading venues and alternative trading systems (ATS) for a specified stock ticker. Unlike short interest, which measures outstanding short positions at specific reporting intervals, short volume captures the daily trading activity of short sales. Monitoring short volume helps users detect immediate market sentiment shifts, analyze trading behavior, and identify trends in short-selling activity that may signal upcoming price movements.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | The primary ticker symbol for the stock. |
| date | string | 否 | The date of trade activity reported in the format YYYY-MM-DD |
| short_volume_ratio | number | 否 | The percentage of total volume that was sold short. Calculated as (short_volume / total_volume) * 100. Value must be a floating point number. |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '10' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'ticker' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| adf_short_volume | integer | 否 | Short volume reported via the Alternative Display Facility (ADF), excluding exempt volume. |
| adf_short_volume_exempt | integer | 否 | Short volume reported via ADF that was marked as exempt. |
| date | string | 否 | The date of trade activity reported in the format YYYY-MM-DD |
| exempt_volume | number | 否 | Portion of short volume that was marked as exempt from regulation SHO. |
| nasdaq_carteret_short_volume | integer | 否 | Short volume reported from Nasdaq's Carteret facility, excluding exempt volume. |
| nasdaq_carteret_short_volume_exempt | integer | 否 | Short volume from Nasdaq Carteret that was marked as exempt. |
| nasdaq_chicago_short_volume | integer | 否 | Short volume reported from Nasdaq's Chicago facility, excluding exempt volume. |
| nasdaq_chicago_short_volume_exempt | integer | 否 | Short volume from Nasdaq Chicago that was marked as exempt. |
| non_exempt_volume | number | 否 | Portion of short volume that was not exempt from regulation SHO (i.e., short_volume - exempt_volume). |
| nyse_short_volume | integer | 否 | Short volume reported from NYSE facilities, excluding exempt volume. |
| nyse_short_volume_exempt | integer | 否 | Short volume from NYSE facilities that was marked as exempt. |
| short_volume | number | 否 | Total number of shares sold short across all venues for the ticker on the given date. |
| short_volume_ratio | number | 否 | The percentage of total volume that was sold short. Calculated as (short_volume / total_volume) * 100. |
| ticker | string | 否 | The primary ticker symbol for the stock. |
| total_volume | number | 否 | Total reported volume across all venues for the ticker on the given date. |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/stocks/v1/short-volume
```

### Request

```bash
curl -X GET "https://api.massive.com/stocks/v1/short-volume?limit=10&sort=ticker.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "adf_short_volume": 0,
      "adf_short_volume_exempt": 0,
      "date": "2025-03-25",
      "exempt_volume": 1,
      "nasdaq_carteret_short_volume": 179943,
      "nasdaq_carteret_short_volume_exempt": 1,
      "nasdaq_chicago_short_volume": 1,
      "nasdaq_chicago_short_volume_exempt": 0,
      "non_exempt_volume": 181218,
      "nyse_short_volume": 1275,
      "nyse_short_volume_exempt": 0,
      "short_volume": 181219,
      "short_volume_ratio": 31.57,
      "ticker": "A",
      "total_volume": 574084
    }
  ],
  "status": "OK"
}
```
