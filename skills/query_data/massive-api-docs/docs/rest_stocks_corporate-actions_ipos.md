# Initial Public Offerings (IPOs)

## 源URL

https://massive.com/docs/rest/stocks/corporate-actions/ipos

## 描述

Retrieve comprehensive information on Initial Public Offerings (IPOs), including upcoming and historical events, starting from the year 2008. This endpoint provides key details such as issuer name, ticker symbol, security type, IPO date, number of shares offered, expected price ranges, final issue prices, and offering sizes. Users can filter results by IPO status (e.g., pending, new, rumors, historical) to target their research and inform investment decisions.

## 参数

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| ticker | string | 否 | Specify a case-sensitive ticker symbol. For example, TSLA represents Tesla Inc. |
| us_code | string | 否 | Specify a us_code. This is a unique nine-character alphanumeric code that identifies a North American financial security for the purposes of facilitating clearing and settlement of trades. |
| isin | string | 否 | Specify an International Securities Identification Number (ISIN). This is a unique twelve-digit code that is assigned to every security issuance in the world. |
| listing_date | string | 否 | Specify a listing date. This is the first trading date for the newly listed entity. |
| ipo_status | enum (string) | 否 | Specify an IPO status. |
| order | enum (string) | 否 | Order results based on the `sort` field. |
| limit | integer | 否 | Limit the number of results returned, default is 10 and max is 1000. |
| sort | enum (string) | 否 | Sort field used for ordering. |

## Response Attributes

| 参数名称 | 类型 | 必选 | 说明 |
| -------- | ---- | ---- | ---- |
| next_url | string | 否 | If present, this value can be used to fetch the next page of data. |
| request_id | string | 否 | A request id assigned by the server. |
| results | array (object) | 否 | An array of results containing the requested data. |
| announced_date | string | 否 | The date when the IPO event was announced. |
| currency_code | string | 否 | Underlying currency of the security. |
| final_issue_price | number | 否 | The price set by the company and its underwriters before the IPO goes live. |
| highest_offer_price | number | 否 | The highest price within the IPO price range that the company might use to price the shares. |
| ipo_status | enum | 否 | The status of the IPO event. IPO events start out as status "rumor" or "pending". On listing day, the status changes to "new". After the listing day, the status changes to "history".The status "direct_listing_process" corresponds to a type of offering where, instead of going through all the IPO processes, the company decides to list its shares directly on an exchange, without using an investment bank or other intermediaries. This is called a direct listing, direct placement, or direct public offering (DPO). |
| isin | string | 否 | International Securities Identification Number. This is a unique twelve-digit code that is assigned to every security issuance in the world. |
| issuer_name | string | 否 | Name of issuer. |
| last_updated | string | 否 | The date when the IPO event was last modified. |
| listing_date | string | 否 | First trading date for the newly listed entity. |
| lot_size | number | 否 | The minimum number of shares that can be bought or sold in a single transaction. |
| lowest_offer_price | number | 否 | The lowest price within the IPO price range that the company is willing to offer its shares to investors. |
| max_shares_offered | number | 否 | The upper limit of the shares that the company is offering to investors. |
| min_shares_offered | number | 否 | The lower limit of shares that the company is willing to sell in the IPO. |
| primary_exchange | string | 否 | Market Identifier Code (MIC) of the primary exchange where the security is listed. The Market Identifier Code (MIC) (ISO 10383) is a unique identification code used to identify securities trading exchanges, regulated and non-regulated trading markets. |
| security_description | string | 否 | Description of the security. |
| security_type | string | 否 | The classification of the stock. For example, "CS" stands for Common Stock. |
| shares_outstanding | number | 否 | The total number of shares that the company has issued and are held by investors. |
| ticker | string | 否 | The ticker symbol of the IPO event. |
| total_offer_size | number | 否 | The total amount raised by the company for IPO. |
| us_code | string | 否 | This is a unique nine-character alphanumeric code that identifies a North American financial security for the purposes of facilitating clearing and settlement of trades. |
| status | string | 否 | The status of this request's response. |

## 代码示例

```text
/vX/reference/ipos
```

### Request

```bash
curl -X GET "https://api.massive.com/vX/reference/ipos?order=desc&limit=10&sort=listing_date&apiKey=YOUR_API_KEY"
```

### Response

```json
{
  "next_url": "https://api.massive.com/vX/reference/ipos?cursor=YWN0aXZlPXRydWUmZGF0ZT0yMDIxLTA0LTI1JmxpbWl0PTEmb3JkZXI9YXNjJnBhZ2VfbWFya2VyPUElN0M5YWRjMjY0ZTgyM2E1ZjBiOGUyNDc5YmZiOGE1YmYwNDVkYzU0YjgwMDcyMWE2YmI1ZjBjMjQwMjU4MjFmNGZiJnNvcnQ9dGlja2Vy",
  "request_id": "6a7e466379af0a71039d60cc78e72282",
  "results": [
    {
      "announced_date": "2024-06-01",
      "currency_code": "USD",
      "final_issue_price": 17,
      "highest_offer_price": 17,
      "ipo_status": "history",
      "isin": "US75383L1026",
      "issue_end_date": "2024-06-06",
      "issue_start_date": "2024-06-01",
      "issuer_name": "Rapport Therapeutics Inc.",
      "last_updated": "2024-06-27",
      "listing_date": "2024-06-07",
      "lot_size": 100,
      "lowest_offer_price": 17,
      "max_shares_offered": 8000000,
      "min_shares_offered": 1000000,
      "primary_exchange": "XNAS",
      "security_description": "Ordinary Shares",
      "security_type": "CS",
      "shares_outstanding": 35376457,
      "ticker": "RAPP",
      "total_offer_size": 136000000,
      "us_code": "75383L102"
    }
  ],
  "status": "OK"
}
```
