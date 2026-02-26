# Timestamp Pages Directory Feature

## 概述

从现在开始，每次运行爬虫任务时，`pages` 目录会自动添加时间戳后缀，格式为 `pages-YYYYMMDD-HHmmss`。这个时间戳与日志文件名保持一致，方便排查问题和追踪任务执行历史。

## 功能说明

### 目录结构示例

```
output/lixinger-crawler/
├── pages-20260226-153523/     # 2026年2月26日 15:35:23 执行的任务
│   ├── page1.md
│   ├── page2.md
│   └── ...
├── pages-20260226-160145/     # 2026年2月26日 16:01:45 执行的任务
│   ├── page1.md
│   ├── page2.md
│   └── ...
├── logs/
│   ├── crawler-20260226-153523.log  # 对应第一次任务
│   ├── crawler-20260226-160145.log  # 对应第二次任务
│   └── ...
└── links.txt
```

### 时间戳格式

- **格式**: `YYYYMMDD-HHmmss`
- **时区**: 北京时间 (UTC+8)
- **示例**: `20260226-153523` 表示 2026年2月26日 15:35:23

### 对应关系

每次任务执行时：
- 日志文件: `logs/crawler-{timestamp}.log`
- Pages目录: `pages-{timestamp}/`

两者使用相同的时间戳，确保一一对应。

## 使用场景

### 1. 问题排查

当某次抓取出现问题时，可以通过时间戳快速定位：

```bash
# 查看特定时间的日志
cat output/lixinger-crawler/logs/crawler-20260226-153523.log

# 查看对应的抓取结果
ls output/lixinger-crawler/pages-20260226-153523/
```

### 2. 历史追踪

保留多次执行的结果，方便对比和分析：

```bash
# 对比两次抓取的差异
diff -r pages-20260226-153523/ pages-20260226-160145/
```

### 3. 数据备份

每次执行都会创建新的目录，不会覆盖之前的数据：

```bash
# 旧数据自动保留
output/lixinger-crawler/
├── pages-20260226-153523/  # 第一次执行
├── pages-20260226-160145/  # 第二次执行
└── pages-20260226-173012/  # 第三次执行
```

## 实现细节

### 代码修改

1. **Logger类** (`src/logger.js`)
   - 添加 `timestamp` 实例变量存储时间戳
   - 添加 `getTimestamp()` 方法供外部获取

2. **CrawlerMain类** (`src/crawler-main.js`)
   - 在初始化Logger后获取时间戳
   - 使用时间戳创建带后缀的pages目录

### 关键代码

```javascript
// Logger初始化时生成时间戳
this.timestamp = this.getBeijingTimeForFilename();
this.logFile = path.join(this.logDir, `crawler-${this.timestamp}.log`);

// CrawlerMain使用相同的时间戳
const timestamp = this.logger.getTimestamp();
this.pagesDir = `${this.projectDir}/pages-${timestamp}`;
```

## 向后兼容性

- 旧的 `pages/` 目录（如果存在）不会被删除
- 新的执行会创建带时间戳的目录
- 不影响 `links.txt` 的使用和恢复功能

## 测试

运行测试脚本验证功能：

```bash
node scripts/test-timestamp-pages.js
```

预期输出：
```
✓ Logger timestamp: 20260226-153523
✓ Log file: test-logs/crawler-20260226-153523.log
✓ Pages directory would be: ./test-output/pages-20260226-153523
✓ Timestamp format is correct (YYYYMMDD-HHmmss)
✓ Log file name matches expected format
✓ All tests passed!
```

## 注意事项

1. **磁盘空间**: 每次执行都会创建新目录，注意定期清理旧数据
2. **时间戳唯一性**: 同一秒内多次执行会使用相同的时间戳（极少发生）
3. **时区**: 所有时间戳使用北京时间，与日志内容保持一致

## 清理旧数据

可以使用以下命令清理旧的pages目录：

```bash
# 删除7天前的pages目录
find output/lixinger-crawler -name "pages-*" -type d -mtime +7 -exec rm -rf {} +

# 删除7天前的日志文件
find output/lixinger-crawler/logs -name "crawler-*.log" -mtime +7 -delete
```
