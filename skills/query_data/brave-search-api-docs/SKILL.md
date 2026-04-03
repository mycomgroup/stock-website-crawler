# Brave Search API Skill

## 概述

Brave Search API 是一个隐私优先的搜索API，提供独立的搜索索引，不依赖Google或Bing。支持网页搜索、新闻、图片、视频等多种搜索类型，以及AI摘要和Grounding等高级功能。

- **基础URL**: `https://api.search.brave.com`
- **文档地址**: https://api-dashboard.search.brave.com/documentation
- **认证方式**: API Key (X-Subscription-Token Header)

## 定价与免费额度

**⚠️ 付费服务** - Brave Search API 为付费服务，无完全免费的接口。

**每月免费额度**:
- 每月赠送 **$5 积分**，自动抵扣费用
- Web 搜索: 约 1000 次免费请求/月
- Spellcheck/Autosuggest: 约 10000 次免费请求/月

**价格明细**:

| 服务 | 价格 | 说明 |
|------|------|------|
| **Web 搜索** | $5.00/1000 请求 | 包含网页、新闻、图片、视频搜索 |
| **AI Answers** | $4.00/1000 查询 + $5.00/1M tokens | LLM 生成答案服务 |
| **Spellcheck** | $5.00/10000 请求 | 拼写检查 |
| **Autosuggest** | $5.00/10000 请求 | 自动建议/搜索补全 |

**容量限制**:
- Web 搜索: 50 请求/秒
- Answers: 2 请求/秒
- Spellcheck/Autosuggest: 100 请求/秒

## 认证

所有请求必须在Header中包含订阅令牌：

```
X-Subscription-Token: YOUR_API_KEY
```

**获取API Key**：
1. 访问 https://api-dashboard.search.brave.com 注册账号
2. 订阅适合的套餐计划
3. 在Dashboard的API Keys部分创建密钥

## 核心API端点

### 1. 网页搜索

```
GET /res/v1/web/search
```

**主要参数**：
- `q` (必需): 搜索查询词，最大400字符/50词
- `country`: 2字符国家代码，默认`US`
- `search_lang`: 搜索语言，默认`en`
- `ui_lang`: UI语言，默认`en-US`
- `count`: 结果数量，默认20，最大20
- `offset`: 分页偏移(0-9)，默认0
- `safesearch`: 安全搜索过滤 (`off`/`moderate`/`strict`)，默认`moderate`
- `spellcheck`: 拼写检查，默认`true`
- `freshness`: 时间过滤 (`pd`/`pw`/`pm`/`py`或自定义日期范围如`2022-04-01to2022-07-30`)

**示例请求**：
```bash
curl "https://api.search.brave.com/res/v1/web/search?q=artificial+intelligence&count=10" \
  -H "Accept: application/json" \
  -H "Accept-Encoding: gzip" \
  -H "X-Subscription-Token: YOUR_API_KEY"
```

**响应包含**：
- `web.results`: 网页结果
- `news.results`: 新闻结果
- `videos.results`: 视频结果
- `images.results`: 图片结果
- `discussions`: 讨论内容
- `faq`: 常见问题
- `infobox`: 知识图谱
- `locations`: 本地位置
- `summarizer`: AI摘要

### 2. 新闻搜索

```
GET /res/v1/news/search
```

**主要参数**（同网页搜索，但`count`最大50）：
- `q` (必需): 查询词
- `country`: 国家代码，默认`US`
- `count`: 结果数量，默认20，最大50
- `offset`: 分页偏移(0-9)
- `freshness`: 时间过滤（特别适合新闻）

**示例请求**：
```bash
curl "https://api.search.brave.com/res/v1/news/search?q=machine+learning&freshness=pd" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: YOUR_API_KEY"
```

### 3. 图片搜索

```
GET /res/v1/images/search
```

**主要参数**：
- `q` (必需): 查询词
- `count`: 结果数量，默认50，最大200
- `country`: 国家代码
- `safesearch`: 安全搜索 (`off`/`strict`)，默认`strict`

**响应字段**：
- `results[].thumbnail`: 缩略图信息(src, width, height)
- `results[].properties`: 原图信息
- `results[].meta_url`: 来源网站信息
- `results[].confidence`: 置信度

**示例请求**：
```bash
curl "https://api.search.brave.com/res/v1/images/search?q=mountain+landscape&count=20" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: YOUR_API_KEY"
```

### 4. 视频搜索

```
GET /res/v1/videos/search
```

**主要参数**（同新闻搜索，`count`最大50）：
- `q` (必需): 查询词
- `count`: 结果数量，默认20，最大50
- `offset`: 分页偏移(0-9)
- `freshness`: 时间过滤

**响应字段**：
- `results[].video`: 视频详情(duration, views, creator, publisher)
- `results[].meta_url`: 来源信息

**示例请求**：
```bash
curl "https://api.search.brave.com/res/v1/videos/search?q=python+tutorial" \
  -H "Accept: application/json" \
  -H "X-Subscription-Token: YOUR_API_KEY"
```

## 高级功能

### 5. AI摘要 (Summarizer)

通过网页搜索时添加`summary=true`参数启用AI摘要：

```bash
curl "https://api.search.brave.com/res/v1/web/search?q=quantum+computing&summary=true" \
  -H "X-Subscription-Token: YOUR_API_KEY"
```

响应中的`summarizer.key`可用于获取详细摘要。

### 6. LLM上下文 (LLM Context)

为LLM应用提供搜索结果上下文：

```
GET /res/v1/summarizer/llm_context
```

### 7. 地点搜索 (Place Search)

```
GET /res/v1/local/pois
GET /res/v1/local/descriptions
```

### 8. 自动建议 (Autosuggest)

```
GET /res/v1/suggest/search
```

### 9. 拼写检查 (Spellcheck)

```
GET /res/v1/spellcheck
```

## 限流与配额

**限流策略**：
- 1秒滑动窗口限流
- 同时存在突发限流(每秒)和月度配额限制

**响应头信息**：
- `X-RateLimit-Limit`: 配额上限 (如 `1, 15000`)
- `X-RateLimit-Policy`: 限流策略 (如 `1;w=1, 15000;w=2592000`)
- `X-RateLimit-Remaining`: 剩余配额
- `X-RateLimit-Reset`: 重置时间(秒)

**超过限制**：返回429状态码

**最佳实践**：
- 检查`X-RateLimit-Remaining`避免意外超限
- 实现指数退避重试机制
- 均匀分布请求避免突发

## 通用请求头

```
Accept: application/json
Accept-Encoding: gzip
X-Subscription-Token: YOUR_API_KEY
User-Agent: Mozilla/5.0 ...
```

可选：
- `Cache-Control: no-cache` (禁用缓存，最佳努力)
- `x-loc-*`: 地理位置相关头部(纬度、经度、时区、城市等)
- `api-version`: API版本 (格式: YYYY-MM-DD)

## 通用参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `q` | string | 必需 | 查询词，1-400字符，最多50词 |
| `country` | string | US | 2字符国家代码或ALL |
| `search_lang` | string | en | 搜索语言代码 |
| `ui_lang` | string | en-US | UI语言 (如 en-US, zh-CN) |
| `count` | integer | 20 | 结果数量 (Web最大20, News/Video最大50, Image最大200) |
| `offset` | integer | 0 | 分页偏移 (0-9) |
| `safesearch` | enum | moderate | off/moderate/strict |
| `spellcheck` | boolean | true | 是否启用拼写检查 |
| `freshness` | string | - | pd/pw/pm/py 或日期范围 |
| `extra_snippets` | boolean | - | 包含额外摘要 |
| `goggles` | string | - | Goggles过滤ID |
| `include_fetch_metadata` | boolean | false | 包含获取元数据 |

## 安全搜索选项

- `off`: 不过滤（图片搜索时仍过滤非法内容）
- `moderate`: 过滤明确内容（图片/视频），但允许成人域名
- `strict`: 完全过滤所有成人内容

## 时间过滤选项 (freshness)

- `pd`: 过去24小时
- `pw`: 过去7天
- `pm`: 过去31天
- `py`: 过去365天
- `YYYY-MM-DDtoYYYY-MM-DD`: 自定义日期范围

## 使用建议

1. **安全存储**: 使用环境变量存储API Key，不要硬编码
2. **密钥轮换**: 定期轮换API Key
3. **错误处理**: 处理429限流错误，实现重试逻辑
4. **分页**: 使用count和offset组合分页，注意不同端点的最大限制
5. **结果过滤**: 使用freshness获取最新内容，使用safesearch控制内容安全级别
6. **性能**: 启用gzip压缩减少数据传输

## 错误码

- `429`: 超过速率限制
- 其他标准HTTP错误码

## 完整示例代码

### Python

```python
import requests
import os

API_KEY = os.environ.get('BRAVE_API_KEY')
BASE_URL = 'https://api.search.brave.com/res/v1'

def search_web(query, count=10):
    """执行网页搜索"""
    url = f'{BASE_URL}/web/search'
    headers = {
        'Accept': 'application/json',
        'X-Subscription-Token': API_KEY
    }
    params = {
        'q': query,
        'count': count
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    # 检查限流
    remaining = response.headers.get('X-RateLimit-Remaining')
    if remaining:
        print(f'剩余配额: {remaining}')
    
    if response.status_code == 429:
        reset_time = response.headers.get('X-RateLimit-Reset')
        print(f'限流中，{reset_time}秒后重试')
        return None
    
    response.raise_for_status()
    return response.json()

def search_news(query, freshness='pw'):
    """搜索新闻"""
    url = f'{BASE_URL}/news/search'
    headers = {
        'Accept': 'application/json',
        'X-Subscription-Token': API_KEY
    }
    params = {
        'q': query,
        'freshness': freshness,  # pw = 过去一周
        'count': 20
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# 使用示例
if __name__ == '__main__':
    # 网页搜索
    results = search_web('artificial intelligence trends 2024')
    if results and 'web' in results:
        for item in results['web']['results'][:5]:
            print(f"标题: {item['title']}")
            print(f"链接: {item['url']}")
            print(f"描述: {item.get('description', 'N/A')}")
            print('---')
    
    # 新闻搜索
    news = search_news('technology', freshness='pd')  # 今日新闻
    if news and 'results' in news:
        for item in news['results'][:3]:
            print(f"新闻: {item['title']}")
            print(f"来源: {item.get('meta_url', {}).get('hostname', 'N/A')}")
            print('---')
```

### Node.js

```javascript
const axios = require('axios');

const API_KEY = process.env.BRAVE_API_KEY;
const BASE_URL = 'https://api.search.brave.com/res/v1';

async function searchWeb(query, count = 10) {
    try {
        const response = await axios.get(`${BASE_URL}/web/search`, {
            headers: {
                'Accept': 'application/json',
                'X-Subscription-Token': API_KEY
            },
            params: {
                q: query,
                count: count
            }
        });
        
        // 检查限流
        const remaining = response.headers['x-ratelimit-remaining'];
        if (remaining) {
            console.log(`剩余配额: ${remaining}`);
        }
        
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 429) {
            const resetTime = error.response.headers['x-ratelimit-reset'];
            console.error(`限流中，${resetTime}秒后重试`);
        }
        throw error;
    }
}

// 使用示例
searchWeb('machine learning tutorial', 5)
    .then(data => {
        if (data.web && data.web.results) {
            data.web.results.forEach(item => {
                console.log(`标题: ${item.title}`);
                console.log(`链接: ${item.url}`);
                console.log('---');
            });
        }
    })
    .catch(console.error);
```

## 相关链接

- [官方文档](https://api-dashboard.search.brave.com/documentation)
- [API控制台](https://api-dashboard.search.brave.com)
- [定价页面](https://api-dashboard.search.brave.com/documentation/pricing)
- [搜索运算符](https://api-dashboard.search.brave.com/documentation/resources/search-operators)

## 注意事项

1. 仅成功请求计入配额和计费
2. 失败的请求(非2xx响应)不计入配额
3. API Key需保密，不要在客户端代码中暴露
4. 定期监控API使用情况，避免超出套餐限制
5. 不同套餐有不同的速率限制和月度配额
