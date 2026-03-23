# 日志优化总结

## 优化内容

### 1. 日志级别调整

将详细的操作日志从INFO级别降级到DEBUG级别，减少控制台输出噪音。

#### 修改的日志

**crawler-main.js**：
- `Appended table X, page Y` → DEBUG
- `Appended X rows to table Y, page Z` → DEBUG
- `Appended tab content: X` → DEBUG
- `Appended dropdown option: X - Y` → DEBUG
- `Appended date filter data: X` → DEBUG

**generic-parser.js**：
- `找到 X 个可能的Tab` → DEBUG
- `尝试Tab: "X"` → DEBUG
- `点击了"X"按钮 (Y)` → DEBUG
- `共点击了 X 个展开按钮` → DEBUG
- `滚动了 X 次` → DEBUG

### 2. 页面处理时间统计

为每个页面添加处理总时间显示。

#### 成功情况
```
[2026-02-27 08:18:31] [SUCCESS] Saved: page.md (11.23s)
```

#### 失败情况
```
[2026-02-27 08:18:30] [ERROR] Error processing https://example.com/page (5.23s): Timeout
```

时间包括：
- 页面加载
- 内容提取（Tab、下拉框、分页等）
- Markdown生成和保存

### 3. 配置文件支持

在配置文件中添加 `logLevel` 参数：

```json
{
  "crawler": {
    "logLevel": "INFO"
  }
}
```

可选值：
- `DEBUG` - 显示所有日志（包括详细操作）
- `INFO` - 显示关键信息（默认）
- `WARN` - 只显示警告和错误
- `ERROR` - 只显示错误

## 效果对比

### 优化前（INFO级别）

```
[2026-02-27 08:18:20] [INFO] Found 47 new links
查找并点击展开按钮...
✓ 点击了"全部"按钮 (1)
✓ 点击了"全部"按钮 (2)
✓ 点击了"全部"按钮 (3)
✓ 点击了"全部"按钮 (4)
✓ 共点击了 4 个展开按钮
处理无限滚动...
滚动超时
✓ 滚动了 2 次
提取运行时图表数据...
找到 2 个可能的Tab (策略: clickable)
尝试Tab: "导出CSV..."
[2026-02-27 08:57:04] [INFO] Appended tab content: 导出CSV
尝试Tab: "导出图片..."
[2026-02-27 08:57:05] [INFO] Appended table 1, page 1
[2026-02-27 08:57:05] [INFO] Appended table 2, page 1
[2026-02-27 08:57:05] [INFO] Appended table 3, page 1
[2026-02-27 08:57:05] [INFO] Appended table 4, page 1
[2026-02-27 08:57:05] [INFO] Appended table 5, page 1
[2026-02-27 08:57:05] [INFO] Appended table 6, page 1
[2026-02-27 08:57:05] [INFO] Appended table 7, page 1
[2026-02-27 08:57:05] [INFO] Appended table 8, page 1
[2026-02-27 08:57:05] [INFO] Appended table 9, page 1
[2026-02-27 08:57:05] [INFO] Appended table 10, page 1
[2026-02-27 08:57:05] [INFO] Appended table 11, page 1
[2026-02-27 08:57:05] [INFO] Appended table 12, page 1
[2026-02-27 08:57:05] [INFO] Appended table 13, page 1
[2026-02-27 08:57:05] [INFO] Appended table 14, page 1
[2026-02-27 08:57:05] [INFO] Appended table 15, page 1
```

### 优化后（INFO级别）

```
[2026-02-27 08:18:20] [INFO] Processing: https://example.com/page
[2026-02-27 08:18:21] [INFO] Loaded: https://example.com/page
[2026-02-27 08:18:22] [INFO] Found 47 new links
[2026-02-27 08:57:05] [SUCCESS] Saved: page.md (38.85s)
```

### 优化后（DEBUG级别）

如果需要查看详细操作，设置 `logLevel: "DEBUG"`：

```
[2026-02-27 08:18:20] [INFO] Processing: https://example.com/page
[2026-02-27 08:18:21] [INFO] Loaded: https://example.com/page
[2026-02-27 08:18:22] [INFO] Found 47 new links
[2026-02-27 08:18:23] [DEBUG] 找到 2 个可能的Tab (策略: clickable)
[2026-02-27 08:18:24] [DEBUG] 尝试Tab: "导出CSV..."
[2026-02-27 08:18:25] [DEBUG] Appended tab content: 导出CSV
[2026-02-27 08:18:26] [DEBUG] 点击了"全部"按钮 (1)
[2026-02-27 08:18:27] [DEBUG] 点击了"全部"按钮 (2)
[2026-02-27 08:18:28] [DEBUG] 共点击了 2 个展开按钮
[2026-02-27 08:18:29] [DEBUG] 滚动了 2 次
[2026-02-27 08:18:30] [DEBUG] Appended table 1, page 1
[2026-02-27 08:18:31] [DEBUG] Appended table 2, page 1
...
[2026-02-27 08:57:05] [SUCCESS] Saved: page.md (38.85s)
```

## 使用建议

### 日常爬取（生产环境）
```json
{
  "crawler": {
    "logLevel": "INFO"
  }
}
```

优点：
- 清晰简洁的输出
- 只显示关键信息
- 易于监控进度
- 每个页面显示总处理时间

### 开发调试
```json
{
  "crawler": {
    "logLevel": "DEBUG"
  }
}
```

优点：
- 查看所有操作细节
- 排查具体问题
- 了解执行流程

### 只看问题
```json
{
  "crawler": {
    "logLevel": "WARN"
  }
}
```

优点：
- 只显示警告和错误
- 最小化输出
- 快速定位问题

## 日志文件

无论设置什么级别，所有日志都会完整写入日志文件：

```
output/<project-name>/logs/crawler-<timestamp>.log
```

这意味着：
- 控制台可以设置为INFO减少噪音
- 日志文件包含完整的DEBUG信息
- 需要时可以查看日志文件获取详细信息

## 性能统计

### 页面处理时间分析

可以使用以下命令分析处理时间：

```bash
# 查看所有成功页面的处理时间
grep "Saved:" logs/crawler-*.log

# 计算平均处理时间
grep "Saved:" logs/crawler-*.log | \
  grep -oP '\(\K[0-9.]+(?=s\))' | \
  awk '{sum+=$1; count++} END {print "平均:", sum/count, "秒"}'

# 找出最慢的10个页面
grep "Saved:" logs/crawler-*.log | \
  sed 's/.*Saved: //' | \
  sed 's/\.md.*//' | \
  paste - <(grep "Saved:" logs/crawler-*.log | grep -oP '\(\K[0-9.]+(?=s\))') | \
  sort -k2 -rn | \
  head -10
```

## 修改的文件

1. `stock-crawler/src/crawler-main.js`
   - 添加页面处理时间统计
   - 将详细日志改为DEBUG级别
   - 从配置读取日志级别

2. `stock-crawler/src/parsers/generic-parser.js`
   - 将Tab、展开按钮、滚动等操作日志改为DEBUG级别

3. `stock-crawler/config/lixinger.json`
   - 添加 `logLevel` 配置项

4. `stock-crawler/doc/LOG_LEVELS.md`
   - 新增：日志级别详细说明文档

5. `stock-crawler/doc/LOG_OPTIMIZATION_SUMMARY.md`
   - 新增：本优化总结文档

## 向后兼容

- 如果配置文件中没有 `logLevel`，默认使用 `INFO` 级别
- 现有配置文件无需修改即可正常工作
- 日志文件格式保持不变

## 测试建议

1. 使用INFO级别运行一次，确认输出简洁
2. 使用DEBUG级别运行一次，确认详细信息可用
3. 检查日志文件包含完整信息
4. 验证页面处理时间显示正确

## 后续优化建议

1. 添加更多统计信息（如平均处理时间、最慢页面等）
2. 支持按URL pattern设置不同的日志级别
3. 添加日志轮转功能（自动清理旧日志）
4. 支持JSON格式的结构化日志输出
