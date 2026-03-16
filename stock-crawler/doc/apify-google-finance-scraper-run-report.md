# apify-google-finance-scraper 运行与修复报告

## 背景

之前仅有一次性运行记录，缺少“可重复执行 + 自动校验产出文件是否存在”的机制。
本次补充了可复用脚本，目标是保证关键文档可稳定取得。

## 推荐执行方式（修复后）

```bash
cd stock-crawler
npm run crawl:apify-google-finance
```

该命令会：

1. 调用 `config/apify-google-finance-scraper.json` 执行爬虫。
2. 自动检查关键产出 Markdown 是否存在：
   - `Google_Finance_Scraper.md`
   - `ScrapAPI.md`
   - `Apify_API.md`
3. 若缺失则自动重试（默认最多 3 次，可通过 `APIFY_TASK_MAX_RUNS` 调整）。

## 本次验证结果

- 任务执行成功（`Crawled: 3`, `Failed: 0`, `Files Generated: 3`）。
- 最新产出目录：`stock-crawler/output/apify-google-finance-scraper/pages-20260316-201806/`
- 关键文档已全部成功取得：
  - `Google_Finance_Scraper.md`
  - `ScrapAPI.md`
  - `Apify_API.md`

## 接口可用性检查（基于产出 Markdown）

### 1) Google Finance Scraper 页面

- 已提取明确接口信息：
  - Method: `POST`
  - Endpoint: `https://api.apify.com/v2/acts/scrapapi~google-finance-scraper/run-sync-get-dataset-items`
  - Base URL: `https://api.apify.com/v2`
- 已提取输入/输出 JSON 示例。

结论：**接口信息完整，可直接用于联调**。

### 2) ScrapAPI 主页

- 提取到基础信息与 `Base URL`（`https://api.apify.com/v2`）。
- 页面偏“开发者主页”属性，接口细节少于 actor 详情页。

结论：**可作补充信息源，接口开发优先参考 actor 详情页与官方 API 文档页**。

### 3) Apify API 文档总览

- 提取到平台级入口信息：
  - Method: `MULTI`
  - Endpoint: `/v2/*`
  - Base URL: `https://api.apify.com`
- 包含鉴权、分页、错误结构等平台规则。

结论：**可用于统一的鉴权/分页/异常处理实现**。

## 环境注意事项

如果运行时报 Playwright 或系统依赖缺失，可先执行：

```bash
cd stock-crawler
npx playwright install --with-deps chromium
```

然后再执行：

```bash
npm run crawl:apify-google-finance
```

## 总结

已补齐自动化校验与重试入口，当前流程可以稳定拿到关键文档文件，并可用于后续 API 对接与自动化调用。
