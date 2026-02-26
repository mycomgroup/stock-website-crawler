# 配置示例

本文档提供各种场景下的模板配置示例，帮助您快速上手。

## 目录

1. [基础示例](#基础示例)
2. [API文档页面](#api文档页面)
3. [数据仪表板](#数据仪表板)
4. [新闻文章](#新闻文章)
5. [产品列表](#产品列表)
6. [用户资料](#用户资料)
7. [搜索结果](#搜索结果)
8. [高级示例](#高级示例)

## 基础示例

### 最简配置

最基本的配置，只提取标题：

```json
{
  "name": "simple-page",
  "description": "Simple page parser",
  "priority": 50,
  "urlPattern": {
    "pattern": "^https://example\\.com/page",
    "pathTemplate": "/page",
    "queryParams": []
  },
  "extractors": [
    {
      "field": "title",
      "type": "text",
      "selector": "h1",
      "required": true
    }
  ],
  "filters": [],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 10,
    "version": "1.0.0"
  }
}
```

### 标题 + 内容

提取标题和主要内容：

```json
{
  "name": "article-page",
  "description": "Article page parser",
  "priority": 60,
  "urlPattern": {
    "pattern": "^https://example\\.com/articles/[^/]+$",
    "pathTemplate": "/articles/*",
    "queryParams": []
  },
  "extractors": [
    {
      "field": "title",
      "type": "text",
      "selector": "h1.article-title",
      "required": true
    },
    {
      "field": "content",
      "type": "text",
      "selector": "div.article-content"
    },
    {
      "field": "author",
      "type": "text",
      "selector": "span.author-name"
    },
    {
      "field": "publishDate",
      "type": "text",
      "selector": "time.publish-date"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "^相关阅读|^推荐文章",
      "reason": "Related content links"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 50,
    "version": "1.0.0"
  }
}
```

## API文档页面

### 完整API文档配置

理杏仁API文档的实际配置：

```json
{
  "name": "api-doc",
  "description": "Parser configuration for /open/api/doc",
  "priority": 100,
  "urlPattern": {
    "pattern": "^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$",
    "pathTemplate": "/open/api/doc",
    "queryParams": ["api-key"]
  },
  "extractors": [
    {
      "field": "title",
      "type": "text",
      "selector": "h1, h2, title",
      "required": true
    },
    {
      "field": "briefDesc",
      "type": "text",
      "selector": "p",
      "pattern": "^获取"
    },
    {
      "field": "requestUrl",
      "type": "text",
      "selector": "code, pre",
      "pattern": "open\\.lixinger\\.com|api\\.lixinger"
    },
    {
      "field": "parameters",
      "type": "table",
      "selector": "table",
      "columns": ["参数名称", "必选", "类型", "说明"]
    },
    {
      "field": "responseData",
      "type": "table",
      "selector": "table",
      "columns": ["字段", "类型", "说明"]
    },
    {
      "field": "apiExamples",
      "type": "code",
      "selector": "textarea, pre code"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "heading",
      "pattern": "API文档",
      "reason": "Template noise (100% frequency)"
    },
    {
      "type": "remove",
      "target": "heading",
      "pattern": "导航",
      "reason": "Navigation header (100% frequency)"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 163,
    "version": "1.0.0"
  }
}
```

### RESTful API文档

通用的RESTful API文档配置：

```json
{
  "name": "rest-api-doc",
  "description": "RESTful API documentation parser",
  "priority": 90,
  "urlPattern": {
    "pattern": "^https://api\\.example\\.com/docs/[^/]+$",
    "pathTemplate": "/docs/*",
    "queryParams": []
  },
  "extractors": [
    {
      "field": "apiName",
      "type": "text",
      "selector": "h1.api-name",
      "required": true
    },
    {
      "field": "method",
      "type": "text",
      "selector": "span.http-method"
    },
    {
      "field": "endpoint",
      "type": "text",
      "selector": "code.endpoint"
    },
    {
      "field": "description",
      "type": "text",
      "selector": "div.api-description"
    },
    {
      "field": "requestParams",
      "type": "table",
      "selector": "table.request-params",
      "columns": ["Name", "Type", "Required", "Description"]
    },
    {
      "field": "responseFields",
      "type": "table",
      "selector": "table.response-fields",
      "columns": ["Field", "Type", "Description"]
    },
    {
      "field": "requestExample",
      "type": "code",
      "selector": "pre.request-example code"
    },
    {
      "field": "responseExample",
      "type": "code",
      "selector": "pre.response-example code"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "heading",
      "pattern": "API Documentation|Documentation",
      "reason": "Page title"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 50,
    "version": "1.0.0"
  }
}
```

## 数据仪表板

### 分析仪表板

```json
{
  "name": "dashboard",
  "description": "Parser configuration for /analytics/*/dashboard",
  "priority": 90,
  "urlPattern": {
    "pattern": "^https://www\\.lixinger\\.com/analytics/[^/]+/dashboard$",
    "pathTemplate": "/analytics/*/dashboard",
    "queryParams": []
  },
  "extractors": [
    {
      "field": "title",
      "type": "text",
      "selector": "h1",
      "required": true
    },
    {
      "field": "summary",
      "type": "text",
      "selector": "div.summary"
    },
    {
      "field": "mainTable",
      "type": "table",
      "selector": "table.main-data"
    },
    {
      "field": "charts",
      "type": "list",
      "selector": "ul.charts"
    },
    {
      "field": "metrics",
      "type": "list",
      "selector": "ul.metrics"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "heading",
      "pattern": "仪表板|Dashboard",
      "reason": "Page title"
    },
    {
      "type": "remove",
      "target": "list",
      "pattern": "首页|设置|帮助",
      "reason": "Navigation menu"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 50,
    "version": "1.0.0"
  }
}
```

### 财务报表

```json
{
  "name": "financial-report",
  "description": "Financial report parser",
  "priority": 95,
  "urlPattern": {
    "pattern": "^https://finance\\.example\\.com/reports/[^/]+$",
    "pathTemplate": "/reports/*",
    "queryParams": []
  },
  "extractors": [
    {
      "field": "companyName",
      "type": "text",
      "selector": "h1.company-name",
      "required": true
    },
    {
      "field": "reportPeriod",
      "type": "text",
      "selector": "span.period"
    },
    {
      "field": "incomeStatement",
      "type": "table",
      "selector": "table#income-statement",
      "columns": ["项目", "本期金额", "上期金额"]
    },
    {
      "field": "balanceSheet",
      "type": "table",
      "selector": "table#balance-sheet",
      "columns": ["项目", "期末余额", "期初余额"]
    },
    {
      "field": "cashFlow",
      "type": "table",
      "selector": "table#cash-flow",
      "columns": ["项目", "本期金额", "上期金额"]
    },
    {
      "field": "notes",
      "type": "list",
      "selector": "ul.report-notes"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "^免责声明|^Disclaimer",
      "reason": "Legal disclaimer"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 30,
    "version": "1.0.0"
  }
}
```

## 新闻文章

### 新闻详情页

```json
{
  "name": "news-article",
  "description": "News article parser",
  "priority": 80,
  "urlPattern": {
    "pattern": "^https://news\\.example\\.com/\\d{4}/\\d{2}/[^/]+$",
    "pathTemplate": "/YYYY/MM/*",
    "queryParams": []
  },
  "extractors": [
    {
      "field": "headline",
      "type": "text",
      "selector": "h1.headline",
      "required": true
    },
    {
      "field": "subheadline",
      "type": "text",
      "selector": "h2.subheadline"
    },
    {
      "field": "author",
      "type": "text",
      "selector": "span.author"
    },
    {
      "field": "publishDate",
      "type": "text",
      "selector": "time.publish-date"
    },
    {
      "field": "category",
      "type": "text",
      "selector": "span.category"
    },
    {
      "field": "content",
      "type": "text",
      "selector": "div.article-body"
    },
    {
      "field": "tags",
      "type": "list",
      "selector": "ul.tags"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "相关阅读|推荐文章|热门新闻",
      "reason": "Related content links"
    },
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "^广告$|^Advertisement$",
      "reason": "Advertisement blocks"
    },
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "^Copyright|^版权所有",
      "reason": "Copyright notice"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 100,
    "version": "1.0.0"
  }
}
```

### 博客文章

```json
{
  "name": "blog-post",
  "description": "Blog post parser",
  "priority": 75,
  "urlPattern": {
    "pattern": "^https://blog\\.example\\.com/posts/[^/]+$",
    "pathTemplate": "/posts/*",
    "queryParams": []
  },
  "extractors": [
    {
      "field": "title",
      "type": "text",
      "selector": "h1.post-title",
      "required": true
    },
    {
      "field": "author",
      "type": "text",
      "selector": "a.author-link"
    },
    {
      "field": "publishDate",
      "type": "text",
      "selector": "time.publish-date"
    },
    {
      "field": "content",
      "type": "text",
      "selector": "article.post-content"
    },
    {
      "field": "codeSnippets",
      "type": "code",
      "selector": "pre code"
    },
    {
      "field": "tags",
      "type": "list",
      "selector": "ul.post-tags"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "heading",
      "pattern": "评论|Comments|分享|Share",
      "reason": "Social interaction sections"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 80,
    "version": "1.0.0"
  }
}
```

## 产品列表

### 电商产品页

```json
{
  "name": "product-detail",
  "description": "Product detail page parser",
  "priority": 85,
  "urlPattern": {
    "pattern": "^https://shop\\.example\\.com/products/[^/]+$",
    "pathTemplate": "/products/*",
    "queryParams": []
  },
  "extractors": [
    {
      "field": "productName",
      "type": "text",
      "selector": "h1.product-name",
      "required": true
    },
    {
      "field": "price",
      "type": "text",
      "selector": "span.price"
    },
    {
      "field": "description",
      "type": "text",
      "selector": "div.product-description"
    },
    {
      "field": "specifications",
      "type": "table",
      "selector": "table.specs",
      "columns": ["属性", "值"]
    },
    {
      "field": "features",
      "type": "list",
      "selector": "ul.features"
    },
    {
      "field": "reviews",
      "type": "list",
      "selector": "ul.reviews"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "加入购物车|立即购买|Buy Now",
      "reason": "Call-to-action buttons"
    },
    {
      "type": "remove",
      "target": "list",
      "pattern": "推荐商品|相关产品",
      "reason": "Related products"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 200,
    "version": "1.0.0"
  }
}
```

## 用户资料

### 用户个人主页

```json
{
  "name": "user-profile",
  "description": "User profile page parser",
  "priority": 70,
  "urlPattern": {
    "pattern": "^https://social\\.example\\.com/users/[^/]+$",
    "pathTemplate": "/users/*",
    "queryParams": []
  },
  "extractors": [
    {
      "field": "username",
      "type": "text",
      "selector": "h1.username",
      "required": true
    },
    {
      "field": "bio",
      "type": "text",
      "selector": "p.bio"
    },
    {
      "field": "stats",
      "type": "table",
      "selector": "table.user-stats",
      "columns": ["指标", "数值"]
    },
    {
      "field": "recentPosts",
      "type": "list",
      "selector": "ul.recent-posts"
    },
    {
      "field": "skills",
      "type": "list",
      "selector": "ul.skills"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "heading",
      "pattern": "关注|粉丝|Following|Followers",
      "reason": "Social stats headers"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 50,
    "version": "1.0.0"
  }
}
```

## 搜索结果

### 搜索结果页

```json
{
  "name": "search-results",
  "description": "Search results page parser",
  "priority": 65,
  "urlPattern": {
    "pattern": "^https://example\\.com/search\\?q=.+$",
    "pathTemplate": "/search",
    "queryParams": ["q", "page"]
  },
  "extractors": [
    {
      "field": "query",
      "type": "text",
      "selector": "input[name='q']"
    },
    {
      "field": "resultCount",
      "type": "text",
      "selector": "span.result-count"
    },
    {
      "field": "results",
      "type": "list",
      "selector": "ul.search-results"
    },
    {
      "field": "suggestions",
      "type": "list",
      "selector": "ul.suggestions"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "^广告|^赞助",
      "reason": "Sponsored results"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 30,
    "version": "1.0.0"
  }
}
```

## 高级示例

### 多表格提取

提取多个不同类型的表格：

```json
{
  "name": "multi-table-page",
  "description": "Page with multiple tables",
  "priority": 85,
  "urlPattern": {
    "pattern": "^https://data\\.example\\.com/reports/[^/]+$",
    "pathTemplate": "/reports/*",
    "queryParams": []
  },
  "extractors": [
    {
      "field": "title",
      "type": "text",
      "selector": "h1",
      "required": true
    },
    {
      "field": "summaryTable",
      "type": "table",
      "selector": "table:first-of-type",
      "columns": ["指标", "值"]
    },
    {
      "field": "detailTable",
      "type": "table",
      "selector": "table:nth-of-type(2)",
      "columns": ["日期", "数值", "变化"]
    },
    {
      "field": "comparisonTable",
      "type": "table",
      "selector": "table.comparison",
      "columns": ["项目", "本期", "上期", "变化率"]
    }
  ],
  "filters": [],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 40,
    "version": "1.0.0"
  }
}
```

### 复杂过滤规则

使用多个过滤器清理数据：

```json
{
  "name": "complex-filtering",
  "description": "Page with complex filtering needs",
  "priority": 90,
  "urlPattern": {
    "pattern": "^https://content\\.example\\.com/pages/[^/]+$",
    "pathTemplate": "/pages/*",
    "queryParams": []
  },
  "extractors": [
    {
      "field": "title",
      "type": "text",
      "selector": "h1",
      "required": true
    },
    {
      "field": "content",
      "type": "text",
      "selector": "div.main-content"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "heading",
      "pattern": "导航|菜单|Navigation|Menu",
      "reason": "Navigation elements"
    },
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "^Copyright|^©|^版权",
      "reason": "Copyright notices"
    },
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "^广告|^Advertisement|^赞助",
      "reason": "Advertisement content"
    },
    {
      "type": "remove",
      "target": "paragraph",
      "pattern": "相关阅读|推荐文章|热门内容",
      "reason": "Related content links"
    },
    {
      "type": "remove",
      "target": "list",
      "pattern": "首页|关于|联系我们|Home|About|Contact",
      "reason": "Footer navigation"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 60,
    "version": "1.0.0"
  }
}
```

### 带查询参数的URL

处理带有多个查询参数的URL：

```json
{
  "name": "filtered-list",
  "description": "Filtered list page with query params",
  "priority": 75,
  "urlPattern": {
    "pattern": "^https://example\\.com/list\\?category=.+&sort=.+$",
    "pathTemplate": "/list",
    "queryParams": ["category", "sort", "page"]
  },
  "extractors": [
    {
      "field": "title",
      "type": "text",
      "selector": "h1",
      "required": true
    },
    {
      "field": "items",
      "type": "list",
      "selector": "ul.item-list"
    },
    {
      "field": "pagination",
      "type": "list",
      "selector": "ul.pagination"
    }
  ],
  "filters": [
    {
      "type": "remove",
      "target": "list",
      "pattern": "筛选|过滤|Filter",
      "reason": "Filter controls"
    }
  ],
  "metadata": {
    "generatedAt": "2024-02-25T10:00:00.000Z",
    "pageCount": 25,
    "version": "1.0.0"
  }
}
```

## 使用这些示例

### 1. 复制示例

选择最接近您需求的示例，复制到您的配置文件中。

### 2. 修改字段

根据实际页面结构修改：
- `name`: 使用描述性的名称
- `urlPattern`: 匹配您的URL
- `selector`: 使用实际的CSS选择器
- `columns`: 使用实际的表格列名

### 3. 测试验证

使用测试脚本验证配置：

```bash
node scripts/test-template-parser.js
```

### 4. 调整优化

根据测试结果调整：
- 添加或删除提取器
- 调整选择器
- 添加过滤规则
- 修改优先级

## JSONL 格式示例

将多个配置保存为JSONL文件（每行一个JSON对象）：

```jsonl
{"name":"api-doc","description":"API documentation parser","priority":100,"urlPattern":{"pattern":"^https://api\\.example\\.com/docs/[^/]+$","pathTemplate":"/docs/*","queryParams":[]},"extractors":[{"field":"title","type":"text","selector":"h1","required":true}],"filters":[],"metadata":{"generatedAt":"2024-02-25T10:00:00.000Z","pageCount":50,"version":"1.0.0"}}
{"name":"dashboard","description":"Dashboard parser","priority":90,"urlPattern":{"pattern":"^https://app\\.example\\.com/dashboard$","pathTemplate":"/dashboard","queryParams":[]},"extractors":[{"field":"title","type":"text","selector":"h1","required":true}],"filters":[],"metadata":{"generatedAt":"2024-02-25T10:00:00.000Z","pageCount":30,"version":"1.0.0"}}
```

## 相关文档

- [配置格式说明](./CONFIG_FORMAT.md) - 完整的配置格式
- [提取器配置指南](./EXTRACTOR_GUIDE.md) - 提取器详细说明
- [过滤器配置指南](./FILTER_GUIDE.md) - 过滤器详细说明
- [实际配置文件](../examples/template-config.jsonl) - 可运行的示例

## 下一步

1. 选择最接近的示例
2. 根据实际页面修改配置
3. 使用测试脚本验证
4. 根据结果调整优化
5. 保存为JSONL格式
