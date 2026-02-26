# Quick Reference Guide

## 运行爬虫

```bash
# 基本用法
node src/index.js config/lixinger.json

# 或使用 npm
npm run crawl config/lixinger.json
```

## 输出目录结构

每次运行会创建带时间戳的目录：

```
output/lixinger-crawler/
├── pages-20260226-153523/     # 抓取的页面（带时间戳）
│   ├── page1.md
│   ├── page2.md
│   └── ...
├── logs/                       # 日志文件
│   └── crawler-20260226-153523.log  # 对应的日志
└── links.txt                   # URL列表
```

## 时间戳说明

- **格式**: `YYYYMMDD-HHmmss`
- **时区**: 北京时间 (UTC+8)
- **对应关系**: pages目录和日志文件使用相同的时间戳

## 常用命令

### 查看特定任务的日志
```bash
cat output/lixinger-crawler/logs/crawler-20260226-153523.log
```

### 查看特定任务的抓取结果
```bash
ls output/lixinger-crawler/pages-20260226-153523/
```

### 对比两次抓取的差异
```bash
diff -r pages-20260226-153523/ pages-20260226-160145/
```

### 清理旧数据（7天前）
```bash
# 删除旧的pages目录
find output/lixinger-crawler -name "pages-*" -type d -mtime +7 -exec rm -rf {} +

# 删除旧的日志文件
find output/lixinger-crawler/logs -name "crawler-*.log" -mtime +7 -delete
```

## 测试

### 运行所有测试
```bash
npm test
```

### 测试时间戳功能
```bash
node scripts/test-timestamp-pages.js
```

## 配置文件

配置文件位于 `config/` 目录：
- `config/lixinger.json` - 理杏仁网站配置
- `config/example.json` - 示例配置

## 环境变量

```bash
# 启用调试模式
DEBUG=1 node src/index.js config/lixinger.json
```

## 常见问题

### Q: 为什么每次运行都创建新的pages目录？
A: 这样可以保留历史数据，方便对比和追踪。如果不需要，可以手动删除旧目录。

### Q: 如何找到某次抓取的日志？
A: pages目录和日志文件使用相同的时间戳，例如 `pages-20260226-153523/` 对应 `logs/crawler-20260226-153523.log`。

### Q: 旧的pages目录会被删除吗？
A: 不会。每次运行都会创建新目录，旧目录保持不变。

### Q: 如何恢复之前的抓取任务？
A: 爬虫使用 `links.txt` 来跟踪URL状态，可以从中断的地方继续。

## 更多文档

- [README.md](../README.md) - 完整文档
- [TIMESTAMP_PAGES_FEATURE.md](TIMESTAMP_PAGES_FEATURE.md) - 时间戳功能详解
- [QUICK_START.md](../QUICK_START.md) - 快速开始指南
