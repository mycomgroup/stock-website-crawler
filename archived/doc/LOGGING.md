# 日志系统说明

## 概述

爬虫使用分级日志系统，支持不同级别的日志输出，以便在开发和生产环境中灵活控制日志详细程度。

## 时间格式

所有日志时间均使用**北京时间（UTC+8）**：

- **日志内容时间格式**: `YYYY-MM-DD HH:mm:ss`
  - 示例: `[2026-02-25 18:16:43] [INFO] 开始处理...`
  
- **日志文件名格式**: `crawler-YYYYMMDD-HHmmss.log`
  - 示例: `crawler-20260225-181643.log`

## 日志级别

日志系统支持以下级别（从低到高）：

1. **DEBUG** (0) - 调试信息
   - 详细的执行流程
   - 中间变量值
   - 仅在开发调试时使用

2. **INFO** (1) - 信息日志（默认）
   - 正常的操作流程
   - 进度信息
   - 成功的操作

3. **WARN** (2) - 警告日志
   - 潜在问题
   - 非致命错误
   - 需要注意的情况

4. **ERROR** (3) - 错误日志
   - 致命错误
   - 异常情况
   - 需要立即处理的问题

## 使用方法

### 在代码中使用

```javascript
import Logger from './logger.js';

const logger = new Logger('./logs', 'INFO'); // 第二个参数是日志级别

// 不同级别的日志
logger.debug('这是调试信息');
logger.info('这是普通信息');
logger.warn('这是警告信息');
logger.error('这是错误信息', error);
logger.success('这是成功信息');
```

### 设置日志级别

```javascript
// 创建时设置
const logger = new Logger('./logs', 'WARN'); // 只显示 WARN 和 ERROR

// 运行时修改
logger.setLogLevel('DEBUG'); // 显示所有日志
logger.setLogLevel('ERROR'); // 只显示错误
```

## 日志输出

### 控制台输出
- 带颜色标识不同级别
- 根据日志级别过滤
- 实时显示

### 文件输出
- 所有级别的日志都会写入文件
- 文件名格式：`crawler-YYYY-MM-DDTHH-MM-SS.log`
- 位置：`./logs/` 目录

## 优化说明

### 已移除的冗余日志

为了减少日志噪音，以下信息不再输出到控制台：

1. **API 响应详情** - 不再打印每个 API 响应的详细信息
2. **图片下载** - 不再打印每张图片的下载信息
3. **图表保存** - 不再打印每个图表的保存信息
4. **Tab/Dropdown 处理** - 不再打印每个选项的处理状态
5. **无限滚动** - 不再打印每次滚动的详细信息
6. **分页提取** - 不再打印每页的提取信息
7. **内容已存在** - 不再打印跳过的内容信息

### 保留的重要日志

以下信息仍然会输出：

1. **错误信息** - 所有 `console.error` 调用
2. **进度信息** - 通过 Logger 的 `progress()` 方法
3. **URL 状态** - 通过 Logger 的 `logUrlStatus()` 方法
4. **解析摘要** - 通过 Logger 的 `logParseSummary()` 方法

## 推荐配置

### 开发环境
```javascript
const logger = new Logger('./logs', 'DEBUG');
```
显示所有日志，便于调试。

### 生产环境
```javascript
const logger = new Logger('./logs', 'INFO');
```
只显示重要信息和错误，减少日志噪音。

### 监控环境
```javascript
const logger = new Logger('./logs', 'WARN');
```
只关注警告和错误，便于快速发现问题。

## 示例输出

### INFO 级别（默认）
```
[2026-02-25T03:44:16.859Z] [INFO] Progress: 7/10 (70.0%)
[2026-02-25T03:44:16.859Z] [INFO] Processing: https://www.lixinger.com/analytics/macro/energy
[2026-02-25T03:44:16.859Z] [INFO] Parsed page: 能源|宏观 - 理杏仁
[2026-02-25T03:44:16.859Z] [INFO] Saved: 能源_宏观_-_理杏仁.md
```

### ERROR 级别
```
[2026-02-25T03:44:16.859Z] [ERROR] Failed to parse page: Connection timeout
[2026-02-25T03:44:16.859Z] [ERROR] Error processing tab "数据": Element not found
```

## 注意事项

1. 所有日志都会写入文件，不受日志级别限制
2. 控制台输出会根据日志级别过滤
3. 日志文件会随时间累积，建议定期清理
4. 在生产环境中使用 INFO 或更高级别，避免日志过多
