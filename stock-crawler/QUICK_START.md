# 快速开始指南

## 安装

```bash
cd stock-crawler
npm install
```

## 运行爬虫

### 推荐方式

```bash
npm run crawl config/lixinger.json
```

### 其他方式

```bash
# 直接使用 node
node src/index.js config/lixinger.json

# 使用 npm start（需要 --）
npm start -- config/lixinger.json
```

## 命令对比

| 命令 | 说明 | 参数传递 |
|------|------|----------|
| `npm run crawl <config>` | 推荐方式 | 直接传递 ✅ |
| `node src/index.js <config>` | 直接运行 | 直接传递 ✅ |
| `npm start -- <config>` | 需要 `--` | 需要 `--` ⚠️ |

## 配置文件

最小配置示例：

```json
{
  "name": "my-crawler",
  "seedUrls": ["https://example.com"],
  "urlRules": {
    "include": [".*example\\.com.*"],
    "exclude": []
  },
  "login": {
    "required": false
  },
  "crawler": {
    "headless": true,
    "timeout": 30000,
    "waitBetweenRequests": 1000,
    "maxRetries": 3,
    "batchSize": 20
  },
  "output": {
    "directory": "./output",
    "format": "markdown"
  }
}
```


## 模板化抓取流水线（新模块）

当你只输入一个站点 URL，需要先自动抓 3-5 层链接、生成 URL Pattern、再分类并生成模板时，可以使用：

```bash
npm run template:pipeline -- https://example.com ./output/example-site
```

该命令会在 `output/<site>/template-pipeline/` 下生成：
- `links.txt`：3-5 层发现到的链接（JSONL）
- `url-patterns.json`：基于 skill 的 URL Pattern 分析结果
- `classified-patterns.json`：带页面分类标签的 Pattern
- `templates/`：按 Pattern 自动生成的抓取模板

后续你可以直接复用 `templates/` 做模板化抓取，减少页面差异带来的抽取误差。

## 常用选项

### 批量处理

设置 `batchSize` 控制每次运行处理的链接数量：

```json
{
  "crawler": {
    "batchSize": 20
  }
}
```

### 登录配置

```json
{
  "login": {
    "required": true,
    "username": "your-username",
    "password": "your-password",
    "loginUrl": "https://example.com/"
  }
}
```

### 调试模式

```bash
DEBUG=1 node src/index.js config/lixinger.json
```

## 输出结构

```
output/
└── <project-name>/
    ├── pages/          # Markdown 文件
    ├── logs/           # 日志文件
    └── links.txt       # 链接列表（含状态）
```

## 链接状态

- `unfetched` - 未抓取
- `fetching` - 正在抓取
- `fetched` - 已完成
- `failed` - 失败（达到最大重试次数）

## 继续抓取

爬虫会自动保存进度。如果中断，再次运行相同命令即可继续：

```bash
npm run crawl config/lixinger.json
```

只会处理状态为 `unfetched` 的链接。

## 查看帮助

```bash
node src/index.js --help
```

## 运行测试

```bash
# 运行所有测试
npm test

# 运行特定测试
npm test -- link-manager.test.js

# 监视模式
npm run test:watch

# 测试登录功能（不运行完整爬虫）
npm run test:login config/lixinger.json
```

## 常见问题

### 浏览器启动失败

```bash
npx playwright install
```

### 登录失败

1. 检查配置文件中的用户名和密码
2. 设置 `headless: false` 查看浏览器行为
3. 查看日志文件了解详细错误

### 没有找到链接

1. 检查 URL 规则（include/exclude 模式）
2. 验证种子 URL 是否可访问
3. 设置 `headless: false` 检查页面内容

## 更多信息

详细文档请参考：
- [README.md](README.md) - 完整文档
- [doc/LOGIN_FLOW.md](doc/LOGIN_FLOW.md) - 登录流程说明
- [doc/IMPLEMENTATION_SUMMARY.md](doc/IMPLEMENTATION_SUMMARY.md) - 实现总结
