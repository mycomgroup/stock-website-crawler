# 通用数据输出模板 (Unified Output Template)

为了统一 `API`、`RSS`、`MCP` 和 `Hao123网站` 四类数据源的输出结果，我们设计了以下通用模板。该模板采用 **“公共核心字段 + 差异化扩展字段 (metadata)”** 的结构。

由于 API 文档最多且结构最复杂，公共字段的设计很大程度上兼容了 API 的核心需求，同时泛化以适应其他三类数据。

## 1. JSON 数据结构模板

```json
{
  "id": "唯一标识符 (URL的哈希或数据源提供的ID)",
  "type": "数据源类型", // 枚举值: "api" | "rss" | "mcp" | "website"
  "title": "通用名称", // API名称 / RSS Feed标题 / MCP工具名 / Hao123网站名称
  "url": "主链接", // API Endpoint / RSS XML链接 / MCP Server URL / 网站主页URL
  "description": "内容摘要/描述", // API功能描述 / RSS副标题 / MCP能力描述 / 网站简介
  "source": "数据提供方", // 例如: "eodhd", "aliyun-bailian", "hao123"
  "tags": ["标签1", "标签2"], // 分类标签，如 ["finance", "stock"]
  "crawl_time": "2026-03-17T12:00:00Z", // 爬虫抓取时间
  
  "content": "正文详情", // (Markdown格式文本) API详细文档、MCP协议说明、RSS主要内容或网站的详细介绍
  
  "metadata": {
    "//_comment": "这里保留各类数据源特有的、无法统一的原始字段",
    
    "api_details": {
      "method": "GET | POST | PUT",
      "headers": {"Authorization": "Bearer <token>"},
      "parameters": [
        {"name": "symbol", "type": "string", "required": true, "description": "股票代码"}
      ],
      "response_example": "{...}",
      "rate_limit": "调用频率限制说明",
      "authentication": "认证方式说明"
    },
    
    "rss_details": {
      "site_url": "RSS对应的网站主页链接",
      "language": "zh-cn",
      "last_build_date": "最后更新时间",
      "items_count": 50 // 当前抓取到的条目数量
    },
    
    "mcp_details": {
      "capabilities": ["tools", "resources", "prompts"], // MCP支持的能力类型
      "input_schema": {}, // 工具的入参 JSON Schema
      "output_schema": {}, // 工具的出参 JSON Schema
      "server_version": "1.0.0"
    },
    
    "website_details": {
      "icon_url": "网站Favicon或Logo链接",
      "navigation_path": ["首页", "新闻", "科技"], // hao123上的导航层级
      "rank": "热度/推荐指数"
    }
  }
}
```

## 2. Markdown 文件输出模板 (结合 YAML Frontmatter)

由于爬虫目前配置的 `format: "markdown"`，实际输出的 Markdown 文件应采用 `YAML Frontmatter` 来存储结构化字段，正文部分存储 `content`。

```markdown
---
id: "a1b2c3d4"
type: "api"
title: "AlphaVantage Global Quote API"
url: "https://www.alphavantage.co/query?function=GLOBAL_QUOTE"
description: "获取指定证券的最新价格和交易量信息。"
source: "alphavantage"
tags: ["stock", "quote", "api"]
crawl_time: "2026-03-17T10:00:00Z"

# 以下为特有字段 (统一归拢在 metadata 下，或直接平铺但保持命名空间)
metadata:
  method: "GET"
  parameters:
    - name: "symbol"
      type: "string"
      required: true
      description: "股票代码"
  rate_limit: "5 API requests per minute"
---

# AlphaVantage Global Quote API

## 简介
获取指定证券的最新价格和交易量信息。

## 详细说明
(这里放置 API 的详细介绍、MCP 的详细协议、RSS 的正文聚合，或 Hao123 网站的图文介绍等...)

## 请求参数 (仅 API/MCP 适用)
- **symbol** (string, 必填): 股票代码

## 响应示例
```json
{
  "Global Quote": {
    "01. symbol": "IBM",
    "02. open": "117.0000",
    "03. high": "119.8300"
  }
}
```
