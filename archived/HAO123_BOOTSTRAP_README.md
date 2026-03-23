# Hao123 网站批量抓取工具

## 功能说明

这个工具可以自动从 hao123.com 获取所有网站链接，为每个网站生成独立的爬虫配置文件。每个配置文件会设置为只抓取该网站自己的内容（3层深度）。

## 工作流程

1. 访问 hao123.com 获取所有外部网站列表
2. 为每个网站生成一个独立的配置文件
3. 每个配置文件设置为只抓取该网站自己域名下的内容
4. 生成 master-config.json 汇总所有网站信息

## 使用步骤

### 1. 生成所有网站的配置文件

```bash
cd stock-crawler
npm run bootstrap:hao123
```

这个命令会：
- 访问 hao123.com 获取所有外部网站链接
- 为每个网站生成独立的配置文件（不实际抓取）
- 生成一个 master-config.json 汇总文件

生成的配置文件位置：`stock-crawler/config/hao123-sites/`

### 2. 测试单个网站

使用生成的配置文件抓取单个网站：

```bash
npm run crawl config/hao123-sites/hao123-example-com.json
```

这会抓取该网站的内容（3层深度），只抓取该网站自己的页面。

### 3. 批量抓取所有网站

运行所有生成的配置文件：

```bash
npm run test:all-hao123
```

这会依次抓取所有网站，并生成测试报告。

## 配置说明

### 生成的配置文件结构

每个网站的配置文件包含：

```json
{
  "name": "hao123-example-com",
  "seedUrls": ["https://example.com/"],
  "urlRules": {
    "include": ["^https?://([a-z0-9-]+\\.)*example\\.com(/.*)?$"],
    "exclude": [".*\\.(jpg|jpeg|png|...)$", "..."]
  },
  "crawler": {
    "headless": true,
    "timeout": 30000,
    "maxDepth": 3,
    "waitBetweenRequests": 300,
    "maxRetries": 2,
    "batchSize": 10
  },
  "output": {
    "directory": "./output",
    "format": "markdown"
  },
  "metadata": {
    "source": "hao123.com",
    "title": "Example Site"
  }
}
```

关键配置说明：
- `seedUrls`: 起始URL（该网站的首页）
- `urlRules.include`: 只匹配该网站自己的域名
- `crawler.maxDepth`: 抓取深度为3层
- 爬虫会自动发现并抓取该网站内的链接，最多3层

### Master Config 文件

`master-config.json` 包含所有网站的汇总信息：

```json
{
  "version": "1.0.0",
  "generated": "2026-03-06T...",
  "source": "hao123.com",
  "totalSites": 50,
  "maxDepth": 3,
  "sites": [
    {
      "name": "hao123-example-com",
      "host": "example.com",
      "title": "Example Site",
      "configFile": "hao123-example-com.json"
    }
  ]
}
```

## 自定义配置

### 修改爬取深度

编辑 `scripts/bootstrap-hao123-sites.js`：

```javascript
const MAX_DEPTH = 3; // 改为你想要的深度（1-5层）
```

### 修改生成的配置

生成配置后，你可以手动编辑 `config/hao123-sites/` 下的任何配置文件来调整：
- 爬取深度
- URL 匹配规则
- 超时时间
- 请求间隔等

## 输出结果

每个网站抓取后的结果会保存在：
- `stock-crawler/output/hao123-{site-name}/` - 每个网站的输出目录
- `pages/` - Markdown 格式的页面内容
- `links.txt` - 发现的所有链接
- `url-patterns.json` - URL 模式分析

## 示例

假设 hao123 上有网站 `sina.com.cn`：

1. 生成配置：
```bash
npm run bootstrap:hao123
# 生成 config/hao123-sites/hao123-sina-com-cn.json
```

2. 抓取该网站：
```bash
npm run crawl config/hao123-sites/hao123-sina-com-cn.json
# 只会抓取 sina.com.cn 域名下的页面，3层深度
# 不会抓取其他域名的链接
```

## 注意事项

1. 配置生成很快，只访问 hao123.com 一次
2. 实际抓取时才会访问各个网站
3. 每个网站只抓取自己域名下的内容
4. 某些网站可能有反爬虫机制，需要调整配置
5. 建议先测试几个网站，确认配置正确后再批量运行

## 故障排除

### 问题：某些网站抓取失败

解决方案：
- 检查网站是否需要登录
- 增加 timeout 时间
- 检查网络连接
- 查看该网站的 robots.txt

### 问题：生成的配置太多

解决方案：
- 手动删除不需要的配置文件
- 或者只运行你需要的配置

### 问题：抓取深度不够

解决方案：
- 修改配置文件中的 `crawler.maxDepth`
- 或者重新生成配置（修改 MAX_DEPTH）
