# 日志级别说明

## 概述

爬虫支持4个日志级别，可以通过配置文件控制输出的详细程度。

## 日志级别

### DEBUG（调试级别）

最详细的日志输出，包含所有操作细节。

**包含内容**：
- 所有INFO级别的日志
- 每个表格的追加操作
- 每个Tab的点击尝试
- 每个展开按钮的点击
- 每次滚动操作
- 每个下拉框选项的处理
- 每个日期筛选的处理

**适用场景**：
- 开发和调试
- 排查具体问题
- 了解详细执行流程

**示例输出**：
```
[2026-02-27 08:18:20] [INFO] Processing: https://example.com/page
[2026-02-27 08:18:21] [INFO] Loaded: https://example.com/page
[2026-02-27 08:18:22] [DEBUG] 找到 4 个可能的Tab (策略: clickable)
[2026-02-27 08:18:23] [DEBUG] 尝试Tab: "导出CSV..."
[2026-02-27 08:18:24] [DEBUG] Appended tab content: 导出CSV
[2026-02-27 08:18:25] [DEBUG] Appended table 1, page 1
[2026-02-27 08:18:26] [DEBUG] Appended table 2, page 1
[2026-02-27 08:18:27] [DEBUG] 点击了"全部"按钮 (1)
[2026-02-27 08:18:28] [DEBUG] 点击了"全部"按钮 (2)
[2026-02-27 08:18:29] [DEBUG] 共点击了 2 个展开按钮
[2026-02-27 08:18:30] [DEBUG] 滚动了 3 次
[2026-02-27 08:18:31] [SUCCESS] Saved: page.md (11.23s)
```

### INFO（信息级别）- 默认

标准日志输出，包含关键操作和结果。

**包含内容**：
- 页面处理开始/结束
- 发现的新链接数量
- 文件保存成功
- 页面处理总时间
- 进度信息
- 重要状态变化

**不包含**：
- 详细的操作步骤
- 每个元素的处理细节

**适用场景**：
- 生产环境运行
- 日常爬取任务
- 监控爬取进度

**示例输出**：
```
[2026-02-27 08:18:20] [INFO] Processing: https://example.com/page
[2026-02-27 08:18:21] [INFO] Loaded: https://example.com/page
[2026-02-27 08:18:22] [INFO] Found 47 new links
[2026-02-27 08:18:31] [SUCCESS] Saved: page.md (11.23s)
```

### WARN（警告级别）

只显示警告和错误信息。

**包含内容**：
- 警告信息（重试、跳过等）
- 错误信息
- 成功信息

**不包含**：
- 常规操作日志
- 调试信息

**适用场景**：
- 只关注问题
- 减少日志输出
- 快速定位错误

**示例输出**：
```
[2026-02-27 08:18:25] [WARN] Retry 1/3, setting back to unfetched
[2026-02-27 08:18:30] [ERROR] Error processing https://example.com/page (5.23s): Timeout
[2026-02-27 08:18:35] [SUCCESS] Saved: page.md (11.23s)
```

### ERROR（错误级别）

只显示错误和成功信息。

**包含内容**：
- 错误信息
- 成功信息

**适用场景**：
- 只关注失败
- 最小化日志输出

**示例输出**：
```
[2026-02-27 08:18:30] [ERROR] Error processing https://example.com/page (5.23s): Timeout
[2026-02-27 08:18:35] [SUCCESS] Saved: page.md (11.23s)
```

## 配置方法

### 在配置文件中设置

编辑 `config/lixinger.json`：

```json
{
  "crawler": {
    "headless": true,
    "timeout": 30000,
    "logLevel": "INFO"
  }
}
```

可选值：
- `"DEBUG"` - 调试级别
- `"INFO"` - 信息级别（默认）
- `"WARN"` - 警告级别
- `"ERROR"` - 错误级别

### 运行时示例

**开发调试（DEBUG级别）**：
```json
{
  "crawler": {
    "logLevel": "DEBUG"
  }
}
```

**生产环境（INFO级别）**：
```json
{
  "crawler": {
    "logLevel": "INFO"
  }
}
```

**只看问题（WARN级别）**：
```json
{
  "crawler": {
    "logLevel": "WARN"
  }
}
```

## 日志输出位置

所有级别的日志都会：
1. **输出到控制台**：根据日志级别过滤
2. **写入日志文件**：完整记录所有级别（包括被过滤的）

日志文件位置：`output/<project-name>/logs/crawler-<timestamp>.log`

## 性能影响

| 级别 | 控制台输出量 | 性能影响 |
|------|------------|---------|
| DEBUG | 非常多 | 轻微影响（I/O操作） |
| INFO | 适中 | 几乎无影响 |
| WARN | 很少 | 无影响 |
| ERROR | 极少 | 无影响 |

**注意**：即使设置为ERROR级别，所有日志仍会写入文件，只是不在控制台显示。

## 页面处理时间

从版本1.x开始，每个页面处理完成后会显示总耗时：

```
[2026-02-27 08:18:31] [SUCCESS] Saved: page.md (11.23s)
```

时间包括：
- 页面加载
- 内容提取
- Tab/下拉框/日期筛选处理
- 分页处理
- Markdown生成和保存

## 推荐设置

### 开发阶段
```json
{
  "crawler": {
    "logLevel": "DEBUG",
    "headless": false
  }
}
```

### 测试阶段
```json
{
  "crawler": {
    "logLevel": "INFO",
    "headless": true
  }
}
```

### 生产环境
```json
{
  "crawler": {
    "logLevel": "INFO",
    "headless": true
  }
}
```

### 问题排查
```json
{
  "crawler": {
    "logLevel": "DEBUG",
    "headless": false
  }
}
```

## 日志分析

### 查看特定级别的日志

```bash
# 只看错误
grep "\[ERROR\]" logs/crawler-*.log

# 只看警告和错误
grep -E "\[(WARN|ERROR)\]" logs/crawler-*.log

# 只看成功的页面
grep "\[SUCCESS\]" logs/crawler-*.log

# 统计处理时间
grep "Saved:" logs/crawler-*.log | grep -oP '\(\K[0-9.]+(?=s\))' | awk '{sum+=$1; count++} END {print "平均:", sum/count, "秒"}'
```

### 查看最慢的页面

```bash
# 提取所有处理时间并排序
grep "Saved:" logs/crawler-*.log | \
  grep -oP '.*(?=\s+\([0-9.]+s\))' | \
  sed 's/.*Saved: //' | \
  paste - <(grep "Saved:" logs/crawler-*.log | grep -oP '\(\K[0-9.]+(?=s\))') | \
  sort -k2 -rn | \
  head -10
```

## 常见问题

### Q: 为什么设置了ERROR级别还能看到SUCCESS日志？

A: SUCCESS级别等同于INFO级别，会在WARN和ERROR级别显示。这是为了确保你能看到成功的结果。

### Q: 日志文件太大怎么办？

A: 日志文件按时间戳命名，每次运行创建新文件。可以定期清理旧日志：

```bash
# 删除7天前的日志
find output/*/logs -name "crawler-*.log" -mtime +7 -delete
```

### Q: 如何临时查看DEBUG日志而不修改配置？

A: 修改配置文件后重启爬虫，或者查看日志文件（包含所有级别）：

```bash
tail -f logs/crawler-*.log
```

### Q: 页面处理时间包括什么？

A: 包括从开始处理URL到保存Markdown文件的全部时间：
- 页面加载和等待
- 登录检查
- 链接提取
- 内容解析（Tab、下拉框、分页等）
- Markdown生成
- 文件写入

不包括：
- 等待下一个URL的延迟时间
- 浏览器启动时间
