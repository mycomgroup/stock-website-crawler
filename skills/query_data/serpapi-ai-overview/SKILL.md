# SerpApi SKILL

SerpApi 是一个强大的搜索引擎结果页面（SERP）抓取服务 API，支持多种搜索引擎和平台。当需要获取搜索引擎数据时，使用此技能快速访问 SerpApi 的各种接口。

## 核心功能

### 1. 搜索引擎 API

#### Google Search API
- **端点**: `GET https://serpapi.com/search`
- **必需参数**:
  - `engine=google` - 指定 Google 搜索引擎
  - `q` - 搜索查询词
- **可选参数**:
  - `location` - 地理位置（如 "Seattle-Tacoma, WA, Washington, United States"）
  - `hl` - 界面语言（如 "en"）
  - `gl` - 国家代码（如 "us"）
  - `google_domain` - Google 域名（如 "google.com"）
  - `start` - 分页起始位置（如 10）
  - `safe` - 安全搜索过滤（"active" 或 "off"）
  - `api_key` - API 密钥

**示例请求**:
```bash
# 基础搜索
curl "https://serpapi.com/search.json?engine=google&q=Coffee&api_key=YOUR_API_KEY"

# 带完整参数的复杂搜索
curl "https://serpapi.com/search.json?engine=google&q=Fresh+Bagels&location=Seattle-Tacoma,+WA,+Washington,+United+States&hl=en&gl=us&google_domain=google.com&start=10&safe=active&api_key=YOUR_API_KEY"
```

#### Google AI Overview API
- **端点**: `GET https://serpapi.com/search?engine=google`
- **说明**: 获取 Google AI Overview 块内容（仅支持英文搜索 hl=en）
- **特殊处理**: 有时需要额外请求，返回包含 `page_token` 和 `serpapi_link`，需在 4 分钟内使用

**AI Overview 返回结构**:
```json
{
  "ai_overview": {
    "text_blocks": [
      {
        "type": "heading|paragraph|list|expandable|comparison",
        "snippet": "文本内容",
        "snippet_latex": ["LaTeX方程"],
        "snippet_highlighted_words": ["高亮词"],
        "snippet_links": [{"text": "链接文本", "link": "URL"}],
        "reference_indexes": [0, 1, 2],
        "thumbnail": "缩略图URL",
        "video": {
          "link": "视频链接",
          "thumbnail": "缩略图",
          "source": "来源",
          "date": "日期"
        }
      }
    ],
    "references": ["引用来源"],
    "products": [{
      "thumbnail": "产品图",
      "title": "产品名称",
      "rating": "评分",
      "reviews": "评论数",
      "price": "价格",
      "extracted_price": 提取的价格数值
    }],
    "page_token": "用于额外请求的token",
    "serpapi_link": "额外请求的URL"
  }
}
```

**示例**:
```bash
# 搜索 AI Overview
curl "https://serpapi.com/search.json?engine=google&q=drop+shipping&hl=en&api_key=YOUR_API_KEY"

# 需要额外请求时（使用返回的 serpapi_link）
curl "https://serpapi.com/search.json?engine=google_ai_overview&page_token=TOKEN&api_key=YOUR_API_KEY"
```

### 2. Google 专项 API

| API | 引擎参数 | 主要功能 |
|-----|----------|----------|
| Google Images | `engine=google_images` | 图片搜索 |
| Google News | `engine=google_news` | 新闻搜索 |
| Google Maps | `engine=google_maps` | 地图搜索和地点信息 |
| Google Shopping | `engine=google_shopping` | 购物产品搜索 |
| Google Jobs | `engine=google_jobs` | 职位搜索 |
| Google Hotels | `engine=google_hotels` | 酒店搜索 |
| Google Flights | `engine=google_flights` | 航班搜索 |
| Google Finance | `engine=google_finance` | 金融数据 |
| Google Videos | `engine=google_videos` | 视频搜索 |
| Google Scholar | `engine=google_scholar` | 学术文献 |
| Google Trends | `engine=google_trends` | 趋势数据 |
| Google Autocomplete | `engine=google_autocomplete` | 搜索建议 |

### 3. 其他搜索引擎 API

#### Bing Search API
- **引擎**: `engine=bing`
- **端点**: `GET https://serpapi.com/search`
- **相关**:
  - Bing Images: `engine=bing_images`
  - Bing News: `engine=bing_news`
  - Bing Videos: `engine=bing_videos`
  - Bing Shopping: `engine=bing_shopping`

#### Yahoo Search API
- **引擎**: `engine=yahoo`
- 支持 Images, News, Videos 等子类型

#### DuckDuckGo Search API
- **引擎**: `engine=duckduckgo`

#### Yandex Search API
- **引擎**: `engine=yandex`
- 支持 Images, Videos 等

#### Baidu Search API
- **引擎**: `engine=baidu`
- 支持 News, Images 等

#### Naver Search API
- **引擎**: `engine=naver`
- 韩国搜索引擎

### 4. 电商平台 API

| 平台 | 引擎参数 | 功能 |
|------|----------|------|
| Amazon | `engine=amazon` | 产品搜索 |
| eBay | `engine=ebay` | 产品搜索和交易 |
| Walmart | `engine=walmart` | 沃尔玛产品搜索 |
| The Home Depot | `engine=home_depot` | 家居建材 |

**Amazon 示例**:
```bash
curl "https://serpapi.com/search.json?engine=amazon&q=laptop&api_key=YOUR_API_KEY"
```

### 5. 本地服务 API

#### Yelp Search API
- **引擎**: `engine=yelp`
- **功能**: 本地商家搜索和评论
- **可选**:
  - Yelp Place: `engine=yelp_place`
  - Yelp Reviews: `engine=yelp_reviews`

**示例**:
```bash
curl "https://serpapi.com/search.json?engine=yelp&q=restaurant&location=Austin,TX&api_key=YOUR_API_KEY"
```

### 6. 社交媒体和内容平台

| 平台 | 引擎参数 | 功能 |
|------|----------|------|
| YouTube | `engine=youtube` | 视频搜索 |
| Facebook | `engine=facebook` | 个人资料搜索 |
| Twitter/X | 支持在 Google 结果中抓取 | 推文结果 |
| Tripadvisor | `engine=tripadvisor` | 旅游点评 |
| OpenTable | `engine=opentable` | 餐厅预订和评论 |

### 7. 应用商店 API

#### Apple App Store API
- **引擎**: `engine=apple_app_store`
- **功能**: 应用搜索和评论

**示例**:
```bash
# 搜索应用
curl "https://serpapi.com/search.json?engine=apple_app_store&q=fitness&api_key=YOUR_API_KEY"

# 应用详情
curl "https://serpapi.com/search.json?engine=apple_product&id=APP_ID&api_key=YOUR_API_KEY"

# 应用评论
curl "https://serpapi.com/search.json?engine=apple_reviews&id=APP_ID&api_key=YOUR_API_KEY"
```

#### Google Play Store API
- **引擎**: `engine=google_play`
- 支持 Books, Games 等分类

### 8. 实用 API

#### Locations API（免费）
- **端点**: `GET https://serpapi.com/locations.json`
- **功能**: 搜索支持的地理位置
- **参数**:
  - `q` - 地点名称关键词
  - `limit` - 返回结果数量

**示例**:
```bash
curl "https://serpapi.com/locations.json?q=Austin&limit=5"
```

**返回结构**:
```json
[{
  "id": "585069bdee19ad271e9bc072",
  "google_id": 200635,
  "name": "Austin, TX",
  "canonical_name": "Austin, TX,Texas,United States",
  "country_code": "US",
  "target_type": "DMA Region",
  "reach": 5560000,
  "gps": [-97.7430608, 30.267153]
}]
```

#### Supported Domains API
- **Google Domains**: `https://serpapi.com/google-domains.json`
- **Bing Domains**: `https://serpapi.com/bing-domains.json`
- **Yahoo Domains**: `https://serpapi.com/yahoo-domains.json`

#### Supported Languages API
- **端点**: `https://serpapi.com/languages.json`
- **功能**: 获取所有支持的语言代码

### 9. Google 特殊结果类型

| 结果类型 | 说明 |
|----------|------|
| Organic Results | 自然搜索结果 |
| Knowledge Graph | 知识图谱 |
| Local Pack | 本地商家包 |
| Top Stories | 热门新闻 |
| Images Results | 图片结果 |
| Videos Results | 视频结果 |
| News Results | 新闻结果 |
| Related Questions | 相关问题（People Also Ask） |
| Related Searches | 相关搜索 |
| Shopping Results | 购物结果 |
| Ads | 广告结果 |
| AI Overview | AI 概述块 |
| Featured Snippets | 精选摘要 |

### 10. 响应数据结构

典型的 Google Search API 响应包含以下字段：

```json
{
  "search_metadata": {
    "id": "搜索ID",
    "status": "Success",
    "json_endpoint": "JSON端点URL",
    "created_at": "创建时间",
    "processed_at": "处理时间",
    "google_url": "原始Google URL",
    "raw_html_file": "原始HTML文件URL",
    "total_time_taken": 1.23
  },
  "search_parameters": {
    "engine": "google",
    "q": "查询词",
    "location": "位置",
    "google_domain": "google.com",
    "hl": "en",
    "gl": "us",
    "device": "desktop"
  },
  "search_information": {
    "organic_results_state": "Results for exact spelling",
    "query_displayed": "显示的查询",
    "total_results": 1000000,
    "time_taken_displayed": 0.5
  },
  "ai_overview": { /* AI Overview 内容 */ },
  "knowledge_graph": { /* 知识图谱 */ },
  "organic_results": [
    {
      "position": 1,
      "title": "结果标题",
      "link": "结果链接",
      "redirect_link": "重定向链接",
      "displayed_link": "显示的链接",
      "snippet": "摘要文本",
      "snippet_highlighted_words": ["高亮词"],
      "sitelinks": {
        "inline": [{"title": "链接标题", "link": "URL"}],
        "expanded": [{"title": "扩展链接", "link": "URL", "snippet": "描述"}]
      },
      "rich_snippet": {
        "top": {
          "detected_extensions": [{"text": "扩展文本"}],
          "extensions": ["扩展信息"]
        }
      },
      "date": "日期",
      "thumbnail": "缩略图URL"
    }
  ],
  "related_questions": [
    {
      "question": "问题文本",
      "snippet": "答案摘要",
      "title": "来源标题",
      "link": "来源链接",
      "displayed_link": "显示链接"
    }
  ],
  "related_searches": [
    {
      "block_position": 8,
      "query": "相关搜索词",
      "link": "搜索链接",
      "serpapi_link": "SerpApi链接"
    }
  ],
  "pagination": {
    "current": 1,
    "next": "https://www.google.com/search?q=...&start=10",
    "other_pages": {
      "2": "https://www.google.com/search?q=...&start=10",
      "3": "..."
    }
  },
  "serpapi_pagination": {
    "current": 1,
    "next_link": "https://serpapi.com/search.json?...&start=10",
    "next": "https://serpapi.com/search.json?...&start=10"
  }
}
```

## 快速使用指南

### 1. 基本搜索流程

```bash
# 1. 获取 API Key（从 https://serpapi.com 注册）
# 2. 构造请求 URL
# 3. 发送 GET 请求
# 4. 解析 JSON 响应
```

### 2. 常见使用场景

**场景 1: 基础网页搜索**
```bash
curl "https://serpapi.com/search.json?engine=google&q=artificial+intelligence&api_key=YOUR_API_KEY"
```

**场景 2: 图片搜索**
```bash
curl "https://serpapi.com/search.json?engine=google_images&q=cats&api_key=YOUR_API_KEY"
```

**场景 3: 新闻搜索**
```bash
curl "https://serpapi.com/search.json?engine=google_news&q=technology&api_key=YOUR_API_KEY"
```

**场景 4: 本地商家搜索**
```bash
curl "https://serpapi.com/search.json?engine=google_maps&q=pizza+restaurant&ll=@40.7128,-74.0060,15z&api_key=YOUR_API_KEY"
```

**场景 5: 产品搜索**
```bash
curl "https://serpapi.com/search.json?engine=google_shopping&q=laptop&api_key=YOUR_API_KEY"
```

**场景 6: 带地理位置的搜索**
```bash
# 先获取 location ID
curl "https://serpapi.com/locations.json?q=New+York&limit=1"

# 使用 canonical_name 或 id 进行搜索
curl "https://serpapi.com/search.json?engine=google&q=weather&location=New+York,NY,United+States&api_key=YOUR_API_KEY"
```

### 3. 分页处理

使用 `start` 参数进行分页：

```bash
# 第 1 页（默认）
curl "https://serpapi.com/search.json?engine=google&q=test&api_key=YOUR_API_KEY"

# 第 2 页（每页 10 个结果）
curl "https://serpapi.com/search.json?engine=google&q=test&start=10&api_key=YOUR_API_KEY"

# 第 3 页
curl "https://serpapi.com/search.json?engine=google&q=test&start=20&api_key=YOUR_API_KEY"
```

### 4. 设备类型

使用 `device` 参数指定设备类型：

```bash
# 桌面端（默认）
curl "https://serpapi.com/search.json?engine=google&q=test&device=desktop&api_key=YOUR_API_KEY"

# 移动端
curl "https://serpapi.com/search.json?engine=google&q=test&device=mobile&api_key=YOUR_API_KEY"

# 平板
curl "https://serpapi.com/search.json?engine=google&q=test&device=tablet&api_key=YOUR_API_KEY"
```

## 客户端库

SerpApi 提供多语言客户端库：

- **Python**: `pip install google-search-results`
- **Node.js**: `npm install google-search-results-nodejs`
- **Ruby**: `gem install google_search_results`
- **PHP**: `composer require serpapi/google-search-results-php`
- **Java**: Maven/Gradle 依赖
- **Go**: `go get github.com/serpapi/serpapi-golang`
- **.NET**: NuGet 包
- **Rust**: `cargo add serpapi`

### Python 示例

```python
from serpapi import GoogleSearch

params = {
    "engine": "google",
    "q": "coffee",
    "api_key": "YOUR_API_KEY"
}

search = GoogleSearch(params)
results = search.get_dict()

# 获取自然搜索结果
for result in results.get("organic_results", []):
    print(f"{result['position']}. {result['title']}")
    print(f"   {result['link']}")
    print(f"   {result['snippet']}")
    print()
```

### JavaScript/Node.js 示例

```javascript
const { getJson } = require("serpapi");

(async () => {
  const response = await getJson({
    engine: "google",
    q: "coffee",
    api_key: "YOUR_API_KEY"
  });
  
  console.log(response);
})();
```

## 重要提示

1. **API Key**: 所有请求都需要有效的 API Key，从 https://serpapi.com 注册获取

2. **速率限制**: 根据订阅计划有不同的速率限制，免费计划有每月限额

3. **AI Overview 特殊处理**:
   - 仅支持英文搜索（`hl=en`）
   - 部分查询需要额外请求，使用返回的 `page_token` 和 `serpapi_link`
   - token 有效期仅 4 分钟

4. **Locations API 免费**: 地理位置查询 API 是免费的，无需 API Key

5. **数据保留**: API 返回的结果会保留一段时间，可通过 `search_metadata.json_endpoint` 再次访问

6. **安全搜索**: 使用 `safe=active` 启用安全搜索过滤

7. **语言设置**: 
   - `hl` - 界面语言（如 en, zh-CN）
   - `gl` - 搜索结果国家/地区（如 us, cn）

## 错误处理

常见 HTTP 状态码：
- `200` - 成功
- `400` - 请求参数错误
- `401` - API Key 无效或缺失
- `429` - 超出速率限制
- `500` - 服务器错误

错误响应示例：
```json
{
  "error": "Invalid API key"
}
```

## 文档参考

- **官方文档**: https://serpapi.com/search-api
- **Playground**: https://serpapi.com/playground
- **状态页面**: https://serpapi.com/status
- **FAQ**: https://serpapi.com/faq

## 数据源信息

- **来源**: SerpApi (https://serpapi.com)
- **最后更新**: 2026-03-25
- **文档数量**: 232 个 API 文档
- **覆盖范围**: Google, Bing, Yahoo, DuckDuckGo, Yandex, Baidu, Naver, Amazon, eBay, Walmart, Yelp, YouTube, Apple App Store, Google Play 等
- **公司**: SerpApi, LLC (Austin, TX)
- **联系方式**: contact@serpapi.com

### 免费 API（无需 API Key）

以下接口**无需付费**即可访问，不消耗 API 额度：

| API 名称 | 端点 | 功能说明 |
|---------|------|---------|
| **Locations API** | `GET https://serpapi.com/locations.json` | 搜索支持的地理位置，返回按覆盖人数排序的地点列表 |
| **Google Domains API** | `GET https://serpapi.com/google-domains.json` | 获取 Google 支持的所有国家/地区域名（共 184 个） |
| **Bing Domains API** | `GET https://serpapi.com/bing-domains.json` | 获取 Bing 支持的所有国家/地区域名 |
| **Yahoo Domains API** | `GET https://serpapi.com/yahoo-domains.json` | 获取 Yahoo 支持的所有国家/地区域名 |
| **Languages API** | `GET https://serpapi.com/languages.json` | 获取所有支持的语言代码列表 |

**免费 API 使用示例**：
```bash
# Locations API - 搜索地点
curl "https://serpapi.com/locations.json?q=Austin&limit=5"

# Google Domains API - 获取支持的域名
curl "https://serpapi.com/google-domains.json"

# Languages API - 获取支持的语言
curl "https://serpapi.com/languages.json"
```

### 付费 API 概览

其余 **227 个 API** 均需要有效的 API Key 并消耗搜索额度：

#### 主要搜索引擎（7 个）
- **Google** (含 Light/Fast/AI Mode 等变体) - 约 50+ 个细分 API
- **Bing** - 搜索、图片、新闻、视频等
- **Yahoo** - 搜索、图片、新闻等
- **DuckDuckGo** - 搜索、轻量版
- **Yandex** - 搜索、图片、视频等
- **Baidu** - 搜索、图片、新闻等
- **Naver** - 韩国搜索引擎

#### 电商平台（4 个）
- **Amazon** - 产品搜索、筛选器、商品详情
- **eBay** - 产品搜索、商品详情、交易
- **Walmart** - 产品搜索
- **The Home Depot** - 家居建材搜索

#### Google 专项服务（30+ 个）
- AI Overview、Images、News、Maps、Shopping
- Jobs、Hotels、Flights、Finance、Videos
- Scholar、Trends、Autocomplete、Patents 等

#### 社交媒体与内容平台（5 个）
- **YouTube** - 视频搜索
- **Facebook** - 个人资料搜索
- **Yelp** - 本地商家搜索和评论
- **Tripadvisor** - 旅游点评
- **OpenTable** - 餐厅预订

#### 应用商店（2 个）
- **Apple App Store** - 应用搜索、详情、评论
- **Google Play Store** - 应用、图书、游戏

#### 其他实用工具（10+ 个）
- 各种筛选器 API、自动补全、趋势分析等

### 付费计划说明

- **免费试用**: 250 次搜索/月（需注册获取 API Key）
- **付费计划**: 根据搜索量提供不同等级的订阅方案
- **所有付费 API** 均通过 `https://serpapi.com/search` 端点访问
- **必需参数**: `api_key` 和 `engine`

---

**注意**: 此 SKILL 文档总结了 SerpApi 的主要 API 功能。具体参数和响应结构可能随 API 更新而变化，建议参考官方文档获取最新信息。
