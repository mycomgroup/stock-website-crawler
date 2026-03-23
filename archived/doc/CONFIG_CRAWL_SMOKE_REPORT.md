# 全量 config 抓取任务 Smoke 测试报告

- 配置总数: **32**
- 进程退出码 0: **18**
- 超时 (timeout): **14**
- 产出 Markdown 文件的配置数: **26**
- Markdown 样例格式检查通过: **26**

> 说明：本次为 smoke 运行（每个配置最多 25 秒），用于验证“能否启动并产出 md”。

## 结果明细

| config | exitCode | timeout | md文件数 | md格式检查 | 备注 |
|---|---:|:---:|---:|:---:|---|
| 60s-api-docs.json | 0 | N | 1 | PASS | output/smoke-all-configs/60s-api-docs/60s-api-docs-smoke/pages-20260316-184745/随机一言.md |
| alltick.json | 0 | N | 1 | PASS | output/smoke-all-configs/alltick/alltick-api-docs-smoke/pages-20260316-184810/overview.md |
| alphavantage.json | 0 | N | 1 | PASS | output/smoke-all-configs/alphavantage/alphavantage-api-docs-smoke/pages-20260316-184834/api_overview.md |
| apify-google-finance-scraper.json | 124 | Y | 0 | N/A | - |
| apify.json | 124 | Y | 2 | PASS | output/smoke-all-configs/apify/apify-api-v2-docs-smoke/pages-20260316-184923/Apify_API_247410a8.md |
| apitracker-fintech.json | 0 | N | 1 | PASS | output/smoke-all-configs/apitracker-fintech/apitracker-fintech-smoke/pages-20260316-184949/Fintech_APIs.md |
| brave-search.json | 0 | N | 2 | PASS | output/smoke-all-configs/brave-search/brave-search-api-docs-smoke/pages-20260316-185013/documentation.md |
| eodhd.json | 124 | Y | 1 | PASS | output/smoke-all-configs/eodhd/eodhd-api-docs-smoke/pages-20260316-185038/api_overview.md |
| eulerpool.json | 124 | Y | 0 | N/A | - |
| example.json | 0 | N | 1 | PASS | output/smoke-all-configs/example/example-crawler-smoke/pages-20260316-185131/Example_Domain.md |
| financial-datasets.json | 124 | Y | 1 | PASS | output/smoke-all-configs/financial-datasets/financial-datasets-api-docs-smoke/pages-20260316-185138/api_overview.md |
| financial-modeling-prep.json | 0 | N | 1 | PASS | output/smoke-all-configs/financial-modeling-prep/financial-modeling-prep-api-docs-smoke/pages-20260316-185203/api_overview.md |
| finnhub.json | 0 | N | 1 | PASS | output/smoke-all-configs/finnhub/finnhub-api-docs-smoke/pages-20260316-185216/api_overview.md |
| google-financialservices-discovery.json | 0 | N | 1 | PASS | output/smoke-all-configs/google-financialservices-discovery/google-financialservices-discovery-smoke/pages-20260316-185241/Financial_Services_API_Discovery_(v1).md |
| infoway.json | 0 | N | 1 | PASS | output/smoke-all-configs/infoway/infoway-api-docs-smoke/pages-20260316-185247/overview.md |
| itick.json | 124 | Y | 1 | PASS | output/smoke-all-configs/itick/itick-api-docs-smoke/pages-20260316-185309/api_overview.md |
| kuaishou-apifox.json | 0 | N | 1 | PASS | output/smoke-all-configs/kuaishou-apifox/kuaishou-apifox-docs-smoke/pages-20260316-185335/code2AccessToken.md |
| lixinger.json | 124 | Y | 1 | PASS | output/smoke-all-configs/lixinger/lixinger-crawler-smoke/pages-20260316-185356/最新消息_我的关注_概况.md |
| massive.json | 0 | N | 1 | PASS | output/smoke-all-configs/massive/massive-api-docs-smoke/pages-20260316-185422/overview.md |
| modelscope-mcp.json | 124 | Y | 1 | PASS | output/smoke-all-configs/modelscope-mcp/modelscope-mcp-docs-smoke/pages-20260316-185439/mcp_overview.md |
| polyrouter.json | 0 | N | 1 | PASS | output/smoke-all-configs/polyrouter/polyrouter-docs-smoke/pages-20260316-185504/index.md |
| qveris.json | 0 | N | 1 | PASS | output/smoke-all-configs/qveris/qveris-api-docs-smoke/pages-20260316-185520/qveris-api-docs.md |
| rsshub.json | 124 | Y | 0 | N/A | - |
| sanhulianghua.json | 0 | N | 1 | PASS | output/smoke-all-configs/sanhulianghua/sanhulianghua-api-docs-smoke/pages-20260316-185607/base_hsa_gupiao.md |
| serpapi.json | 124 | Y | 1 | PASS | output/smoke-all-configs/serpapi/serpapi-ai-overview-smoke/pages-20260316-185628/ai-overview-api.md |
| tavily.json | 0 | N | 1 | PASS | output/smoke-all-configs/tavily/tavily-api-docs-smoke/pages-20260316-185654/introduction.md |
| tickdb.json | 0 | N | 1 | PASS | output/smoke-all-configs/tickdb/tickdb-api-docs-smoke/pages-20260316-185714/api_overview.md |
| tiingo.json | 124 | Y | 0 | N/A | - |
| tsanghi.json | 124 | Y | 0 | N/A | - |
| tushare-pro.json | 0 | N | 1 | PASS | output/smoke-all-configs/tushare-pro/tushare-pro-crawler-smoke/pages-20260316-185822/stock_basic_25.md |
| xiaohongshu-apifox.json | 124 | Y | 1 | PASS | output/smoke-all-configs/xiaohongshu-apifox/xiaohongshu-apifox-docs-smoke/pages-20260316-185838/新手指南.md |
| yfinance.json | 124 | Y | 0 | N/A | - |