# Tavily API Skill

## 概述

Tavily 是一个强大的 AI 驱动的搜索引擎和 Web 数据提取平台，提供多种 API 端点用于搜索、提取、爬取和研究任务。

**基础 URL**: `https://api.tavily.com`  
**文档地址**: https://docs.tavily.com  
**Python SDK**: `pip install tavily-python`

## 数据访问与套餐

### 免费套餐 (Researcher)

Tavily 提供**完全免费的 Researcher 套餐**，包含：

- **每月 1,000 API credits** - 无需信用卡即可注册使用
- **所有 API 端点均可访问** - Search、Extract、Crawl、Map、Research、Usage 等全部可用
- **邮件支持**
- **按使用量计费** - 使用 credits 系统，不同操作消耗不同数量的 credits

### 付费套餐

| 套餐 | 月额度 | 月费 | 单价/信用 |
|------|--------|------|-----------|
| Researcher | 1,000 | **免费** | - |
| Project | 4,000 | $30 | $0.0075 |
| Bootstrap | 15,000 | $100 | $0.0067 |
| Startup | 38,000 | $220 | $0.0058 |
| Growth | 100,000 | $500 | $0.005 |
| Pay as you go | 按需 | - | $0.008 |

### API 接口可用性汇总

**所有接口在免费套餐下均可访问**，区别仅在于 credits 消耗量：

| 接口 | 免费额度可用 | Credits 消耗 | 免费月调用量* |
|------|-------------|-------------|--------------|
| Search API | ✅ | 1-2 credits/请求 | ~500-1000 次 |
| Extract API | ✅ | 1-2 credits/5 URLs | ~500-1000 次 (5 URLs) |
| Crawl API | ✅ | 1-2 credits/10 页面 | ~500-1000 次 (10 页面) |
| Map API | ✅ | 1-2 credits/10 页面 | ~500-1000 次 (10 页面) |
| Research API | ✅ | 4-250 credits/请求 | ~4-250 次 |
| Usage API | ✅ | 0 credits (免费) | 无限次 |

*基于每月 1,000 credits 的免费额度估算

### 关键限制

免费套餐的限制主要来自于 credits 配额，而非功能限制：
- Research API 的高消耗模式（pro 模型，复杂查询）可能快速耗尽免费额度
- 所有其他 API 在合理调用频率下，免费额度足够支撑日常开发测试

## 认证

所有 API 请求都需要在 Header 中包含 API Key：

```
Authorization: Bearer tvly-YOUR_API_KEY
```

可选的 Project ID Header：
```
X-Project-ID: your-project-id
```

## 核心 API 端点

### 1. Search API - 网络搜索

**端点**: `POST /search`

**功能**: 执行 Tavily 搜索，返回相关搜索结果和 AI 生成的答案。

**核心参数**:
| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `query` | string | 是 | - | 搜索查询 |
| `search_depth` | enum | 否 | basic | `basic`(1 credit), `fast`(1 credit), `advanced`(2 credits), `ultra-fast`(1 credit) |
| `max_results` | integer | 否 | 5 | 返回结果数量 (0-20) |
| `topic` | enum | 否 | general | `general`, `news`, `finance` |
| `time_range` | enum | 否 | - | `day`, `week`, `month`, `year` |
| `include_answer` | boolean/enum | 否 | false | `true`/`basic` 或 `advanced` 获取 AI 答案 |
| `include_raw_content` | boolean/enum | 否 | false | 包含原始 HTML 内容 |
| `include_images` | boolean | 否 | false | 包含图片搜索结果 |
| `chunks_per_source` | integer | 否 | 3 | 每个源的片段数 (1-3) |
| `country` | enum | 否 | - | 国家代码筛选 |
| `include_domains` | string[] | 否 | - | 包含的域名列表 (最多300) |
| `exclude_domains` | string[] | 否 | - | 排除的域名列表 (最多150) |

**返回示例**:
```json
{
  "query": "Who is Leo Messi?",
  "answer": "Lionel Messi, born in 1987, is an Argentine footballer...",
  "images": [],
  "results": [
    {
      "title": "Lionel Messi Facts | Britannica",
      "url": "https://www.britannica.com/facts/Lionel-Messi",
      "content": "Lionel Messi, an Argentine footballer...",
      "score": 0.81025416,
      "raw_content": null,
      "favicon": "https://britannica.com/favicon.png"
    }
  ],
  "response_time": "1.67",
  "usage": { "credits": 1 },
  "request_id": "123e4567-e89b-12d3-a456-426614174111"
}
```

**使用场景**:
- 一般网络搜索
- 新闻检索
- 需要 AI 生成答案的查询
- 实时信息获取

---

### 2. Extract API - 网页内容提取

**端点**: `POST /extract`

**功能**: 从指定 URL 提取网页内容。

**核心参数**:
| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `urls` | string/string[] | 是 | - | 要提取的 URL |
| `query` | string | 否 | - | 用于重新排序的用户意图查询 |
| `extract_depth` | enum | 否 | basic | `basic` (1 credit/5 URLs), `advanced` (2 credits/5 URLs) |
| `include_images` | boolean | 否 | false | 包含图片列表 |
| `include_favicon` | boolean | 否 | false | 包含 favicon |
| `format` | enum | 否 | markdown | `markdown` 或 `text` |
| `chunks_per_source` | integer | 否 | 3 | 每个源的片段数 (1-5) |
| `timeout` | float | 否 | 10/30s | 超时时间 (1-60秒) |

**返回示例**:
```json
{
  "results": [
    {
      "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
      "raw_content": "Artificial intelligence (AI), in its broadest sense...",
      "images": [],
      "favicon": "https://en.wikipedia.org/static/favicon/wikipedia.ico"
    }
  ],
  "failed_results": [],
  "response_time": 0.02,
  "usage": { "credits": 1 },
  "request_id": "123e4567-e89b-12d3-a456-426614174111"
}
```

**使用场景**:
- 提取单个网页内容
- 批量 URL 提取
- 将网页转换为 Markdown
- 获取原始文本内容

---

### 3. Crawl API - 网站爬取

**端点**: `POST /crawl`

**功能**: 基于图的网站遍历工具，可并行探索数百条路径。

**核心参数**:
| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `url` | string | 是 | - | 爬取的起始 URL |
| `instructions` | string | 否 | - | 自然语言指令 (带指令时成本翻倍) |
| `max_depth` | integer | 否 | 1 | 最大爬取深度 (1-5) |
| `max_breadth` | integer | 否 | 20 | 每层最大链接数 (1-500) |
| `limit` | integer | 否 | 50 | 处理的最大链接数 |
| `select_paths` | string[] | 否 | - | 选择路径的正则模式 |
| `exclude_paths` | string[] | 否 | - | 排除路径的正则模式 |
| `select_domains` | string[] | 否 | - | 选择域名的正则模式 |
| `exclude_domains` | string[] | 否 | - | 排除域名的正则模式 |
| `allow_external` | boolean | 否 | true | 是否包含外部域名 |
| `extract_depth` | enum | 否 | basic | `basic` 或 `advanced` |
| `include_images` | boolean | 否 | false | 包含图片 |
| `include_favicon` | boolean | 否 | false | 包含 favicon |
| `format` | enum | 否 | markdown | `markdown` 或 `text` |
| `timeout` | float | 否 | 150 | 超时时间 (10-150秒) |

**计费**:
- 基础: 1 credit / 10 成功页面
- 带指令: 2 credits / 10 成功页面
- 高级提取: 额外计费 (2 credits / 5 URLs)

**使用场景**:
- 网站内容抓取
- 文档站点提取
- 企业知识库构建
- RAG 数据准备

---

### 4. Map API - 网站地图生成

**端点**: `POST /map`

**功能**: 像图一样遍历网站，生成全面的站点地图。

**核心参数**:
| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `url` | string | 是 | - | 起始 URL |
| `instructions` | string | 否 | - | 自然语言指令 |
| `max_depth` | integer | 否 | 1 | 最大深度 (1-5) |
| `max_breadth` | integer | 否 | 20 | 每层最大链接数 (1-500) |
| `limit` | integer | 否 | 50 | 最大链接数 |
| `select_paths` | string[] | 否 | - | 选择路径模式 |
| `exclude_paths` | string[] | 否 | - | 排除路径模式 |
| `allow_external` | boolean | 否 | true | 允许外部链接 |
| `timeout` | float | 否 | 150 | 超时时间 (10-150秒) |

**返回示例**:
```json
{
  "base_url": "docs.tavily.com",
  "results": [
    "https://docs.tavily.com/welcome",
    "https://docs.tavily.com/documentation/api-credits",
    "https://docs.tavily.com/documentation/about"
  ],
  "response_time": 1.23,
  "usage": { "credits": 1 },
  "request_id": "123e4567-e89b-12d3-a456-426614174111"
}
```

**计费**: 同 Crawl API

**使用场景**:
- 生成网站 URL 列表
- 发现网站结构
- 站点地图生成

---

### 5. Research API - 深度研究

#### 5.1 创建研究任务

**端点**: `POST /research`

**功能**: 对给定主题进行全面研究，生成详细研究报告。

**核心参数**:
| 参数 | 类型 | 必需 | 默认值 | 描述 |
|------|------|------|--------|------|
| `input` | string | 是 | - | 研究任务或问题 |
| `model` | enum | 否 | auto | `mini`(高效), `pro`(全面), `auto` |
| `stream` | boolean | 否 | false | 是否流式输出 |
| `citation_format` | enum | 否 | numbered | `numbered`, `mla`, `apa`, `chicago` |
| `output_schema` | object | 否 | - | JSON Schema 结构化输出 |

**返回示例**:
```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174111",
  "created_at": "2025-01-15T10:30:00Z",
  "status": "pending",
  "input": "What are the latest developments in AI?",
  "model": "mini",
  "response_time": 1.23
}
```

#### 5.2 获取研究任务状态

**端点**: `GET /research-get/{request_id}`

**功能**: 使用 request_id 检索研究任务的状态和结果。

**返回示例**:
```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174111",
  "created_at": "2025-01-15T10:30:00Z",
  "status": "completed",
  "content": "Research Report: Latest Developments in AI...",
  "sources": [
    {
      "title": "Latest AI Developments",
      "url": "https://example.com/ai-news",
      "favicon": "https://example.com/favicon.ico"
    }
  ],
  "response_time": 1.23
}
```

#### 5.3 流式研究

**端点**: `/research` (with `stream: true`)

**功能**: 实时流式返回研究进度和结果。

**流式事件类型**:
- `tool_call`: 工具调用事件 (WebSearch, ResearchSubtopic 等)
- `tool_response`: 工具响应事件
- `content`: 研究报告内容块
- `sources`: 使用的所有源
- `done`: 流结束

**使用场景**:
- 复杂主题深度研究
- 多步骤信息收集
- 结构化数据提取
- 实时研究进度展示

---

### 6. Usage API - 用量查询

**端点**: `GET /usage`

**功能**: 获取 API Key 和账户的用量详情。

**返回示例**:
```json
{
  "key": {
    "usage": 150,
    "limit": 1000,
    "search_usage": 100,
    "extract_usage": 25,
    "crawl_usage": 15,
    "map_usage": 7,
    "research_usage": 3
  },
  "account": {
    "current_plan": "Bootstrap",
    "plan_usage": 500,
    "plan_limit": 15000,
    "paygo_usage": 25,
    "paygo_limit": 100,
    "search_usage": 350,
    "extract_usage": 75,
    "crawl_usage": 50,
    "map_usage": 15,
    "research_usage": 10
  }
}
```

**使用场景**:
- 监控 API 用量
- 配额管理
- 成本控制

---

## Python SDK 使用示例

### 安装
```bash
pip install tavily-python
```

### 基础用法

```python
from tavily import TavilyClient

tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")

# 搜索
response = tavily_client.search("Who is Leo Messi?")
print(response)

# 提取
response = tavily_client.extract("https://en.wikipedia.org/wiki/Lionel_Messi")
print(response)

# 爬取
response = tavily_client.crawl(
    "https://docs.tavily.com", 
    instructions="Find all pages on the Python SDK"
)
print(response)

# 地图
response = tavily_client.map("https://docs.tavily.com")
print(response)

# 研究
response = tavily_client.research("What are the latest developments in AI?")
print(response)

# 流式研究
stream = tavily_client.research(
    input="Research the latest developments in AI",
    model="pro",
    stream=True
)
for chunk in stream:
    print(chunk.decode('utf-8'))

# 获取研究状态
response = tavily_client.get_research("123e4567-e89b-12d3-a456-426614174111")
print(response)
```

---

## 计费说明

### Credits 消耗

| 端点 | 基础消耗 | 高级选项 | 免费额度支持 |
|------|---------|---------|-------------|
| Search | 1 credit | advanced: 2 credits | ✅ 1000次/月 |
| Extract | 1 credit / 5 URLs | advanced: 2 credits / 5 URLs | ✅ 1000次/月(5 URLs) |
| Crawl | 1 credit / 10 pages | with instructions: 2 credits / 10 pages | ✅ 1000次/月(10页面) |
| Map | 1 credit / 10 pages | with instructions: 2 credits / 10 pages | ✅ 1000次/月(10页面) |
| Usage | 0 credit | - | ✅ 无限次 |
| Research | **4-250 credits/请求** | model=pro: 15-250 credits; model=mini: 4-110 credits | ✅ 4-250次/月 |

### Research API 详细计费

Research API 的消耗较高，按模型和复杂度计费：

| 模型 | 最低消耗 | 最高消耗 |
|------|---------|---------|
| `model=mini` | 4 credits | 110 credits |
| `model=pro` | 15 credits | 250 credits |

**免费额度使用建议**:
- 使用 `model=mini` 可支持约 250 次研究任务（基于 1,000 credits）
- 使用 `model=pro` 可支持约 4-67 次研究任务（基于 1,000 credits）
- 建议先用 mini 模型测试，确认需求后再使用 pro 模型

### 关键限制

- Search: max_results (0-20), chunks_per_source (1-3)
- Extract: timeout (1-60s), chunks_per_source (1-5)
- Crawl/Map: max_depth (1-5), max_breadth (1-500), timeout (10-150s)

---

## 使用场景推荐

### 快速搜索信息
```python
# 使用 Search API
response = tavily_client.search(
    query="最新的人工智能突破",
    search_depth="basic",
    max_results=5,
    include_answer=True
)
```

### 提取网页内容
```python
# 使用 Extract API
response = tavily_client.extract(
    urls=["https://example.com/article"],
    extract_depth="advanced",
    format="markdown"
)
```

### 构建知识库
```python
# 使用 Crawl API
response = tavily_client.crawl(
    url="https://docs.company.com",
    instructions="Extract all API documentation pages",
    max_depth=3,
    extract_depth="advanced"
)
```

### 深度研究
```python
# 使用 Research API
response = tavily_client.research(
    input="Analyze the competitive landscape of AI companies in 2024",
    model="pro",
    citation_format="apa"
)
```

---

## 集成框架

Tavily 支持与以下框架集成：
- **LangChain**: `langchain-tavily`
- **LlamaIndex**: 原生支持
- **CrewAI**: 原生支持
- **Pydantic AI**: 原生支持
- **Agno**: 原生支持
- **OpenAI**: 函数调用支持

---

## 最佳实践

### 免费额度使用策略

1. **优先使用基础模式**: 
   - Search: 使用 `search_depth=basic` (1 credit) 而非 advanced (2 credits)
   - Extract: 使用 `extract_depth=basic` (1 credit/5 URLs)
   - Research: 使用 `model=mini` (4-110 credits) 测试后再用 pro

2. **优化调用频率**:
   - 批量处理 URL (Extract 支持一次最多 20 个 URL)
   - 合理使用 max_results，避免返回过多结果
   - Crawl/Map API 按页面计费，控制爬取深度和广度

3. **监控用量**: 定期调用 `/usage` 端点监控配额 (免费)

### 通用最佳实践

4. **选择合适的 search_depth**: 
   - `ultra-fast`: 时间敏感场景
   - `fast`: 平衡速度和质量
   - `basic`: 一般用途
   - `advanced`: 高精度需求

5. **使用 include_answer**: 当需要 AI 生成的答案时启用

6. **合理设置 max_results**: 默认 5，根据需求调整 (最大 20)

7. **使用 Project ID**: 多项目时便于跟踪用量

8. **处理失败结果**: Extract API 会返回 `failed_results` 数组

9. **使用流式响应**: 长时间运行的 Research 任务使用 `stream=True`

---

## 错误处理

- 检查 `failed_results` 数组获取失败的 URL
- 使用 `request_id` 联系支持团队排查问题
- 注意 rate limits (查看 `/rate-limits` 文档)

---

## 相关资源

- **官方文档**: https://docs.tavily.com
- **Python SDK**: https://github.com/tavily-ai/tavily-python
- **JavaScript SDK**: https://github.com/tavily-ai/tavily-js
- **API Playground**: https://app.tavily.com/playground
- **获取 API Key**: https://app.tavily.com
