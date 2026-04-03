# Treasury Yields

## 源URL

https://massive.com/docs/rest/economy/treasury-yields

## 描述

Retrieve historical U.S. Treasury yield data for standard timeframes ranging from 1-month to 30-years, with daily historical records back to 1962. This endpoint lets you query by date or date range to see how interest rates have changed over time. Each data point reflects the market yield for Treasury securities of a specific maturity, helping users understand short- and long-term rate movements.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| date | string | 否 | Calendar date of the yield observation (YYYY-MM-DD). |
| limit | integer | 否 | Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'. |
| sort | string | 否 | A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'date' if not specified. The sort order defaults to 'asc' if not specified. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | The results for this request. |
| date | string | 否 | Calendar date of the yield observation (YYYY-MM-DD). |
| yield_10_year | number | 否 | Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity, Quoted on an Investment Basis |
| yield_1_month | number | 否 | Market Yield on U.S. Treasury Securities at 1-Month Constant Maturity, Quoted on an Investment Basis |
| yield_1_year | number | 否 | Market Yield on U.S. Treasury Securities at 1-Year Constant Maturity, Quoted on an Investment Basis |
| yield_20_year | number | 否 | Market Yield on U.S. Treasury Securities at 20-Year Constant Maturity, Quoted on an Investment Basis |
| yield_2_year | number | 否 | Market Yield on U.S. Treasury Securities at 2-Year Constant Maturity, Quoted on an Investment Basis |
| yield_30_year | number | 否 | Market Yield on U.S. Treasury Securities at 30-Year Constant Maturity, Quoted on an Investment Basis |
| yield_3_month | number | 否 | Market Yield on U.S. Treasury Securities at 3-Month Constant Maturity, Quoted on an Investment Basis |
| yield_3_year | number | 否 | Market Yield on U.S. Treasury Securities at 3-Year Constant Maturity, Quoted on an Investment Basis |
| yield_5_year | number | 否 | Market Yield on U.S. Treasury Securities at 5-Year Constant Maturity, Quoted on an Investment Basis |
| yield_6_month | number | 否 | Market Yield on U.S. Treasury Securities at 6-Month Constant Maturity, Quoted on an Investment Basis |
| yield_7_year | number | 否 | Market Yield on U.S. Treasury Securities at 7-Year Constant Maturity, Quoted on an Investment Basis |
| status | enum (OK) | 否 | The status of this request's response. |

## 代码示例

```text
/fed/v1/treasury-yields
```

### Request

```bash
curl -X GET "https://api.massive.com/fed/v1/treasury-yields?limit=100&sort=date.asc&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "count": 1,
  "request_id": 1,
  "results": [
    {
      "date": "1962-01-02",
      "yield_10_year": 4.06,
      "yield_1_year": 3.22,
      "yield_5_year": 3.88
    }
  ],
  "status": "OK"
}
```
