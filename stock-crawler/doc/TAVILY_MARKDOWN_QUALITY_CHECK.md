# Tavily 抓取结果质量检查（11 轮）

## 执行范围
- 配置文件：`config/tavily.json`
- 轮次：11 轮（满足“10 轮以上”）
- 执行命令：
  - `node src/index.js config/tavily.json`（循环执行 11 次）

## 轮次结果摘要
- 第 1 轮抓取到 `7` 个页面，并提示剩余 `2` 个未抓取 URL。
- 第 2 轮抓取到 `3` 个页面。
- 第 3~11 轮每轮都重复抓取 `introduction`（每轮 `1` 个页面），并持续出现 `New Links Found: 13`。
- 轮次统计中 `links.txt` 的状态统计出现异常：`total=8 pending=0 completed=0 failed=0`，说明状态字段没有正常落盘或统计口径不一致。

## 样本对比页面
- 原始页面：`https://docs.tavily.com/documentation/api-reference/introduction`
- 生成 Markdown：`output/tavily-api-docs/pages-20260316-195921/introduction.md`

## 是否存在内容缺失
结论：**有缺失**。

### 发现的缺失点（Introduction 页）
1. `Endpoints` 小节在原网页有 4 个 endpoint 的说明（`/search`、`/extract`、`/crawl,/map`、`/research`），Markdown 中仅保留了 `### Endpoints` 标题，未保留逐条说明。
2. `Project Tracking` 小节末尾“SDK 可通过 `project_id` 或 `TAVILY_PROJECT` 指定项目”的说明，在 Markdown 中缺失。

## Markdown 结构是否清晰
结论：**Introduction 页结构基本清晰；复杂 API 页结构有明显乱序/粘连**。

### Introduction 页
- 标题层级基本可读：`# Introduction` → `## 概述`/`## API 端点`/`## 详细内容`。
- 代码块与 bullet 列表能正常显示。

### Endpoint 页（以 Search 为例）
文件：`output/tavily-api-docs/pages-20260316-195938/endpoint_search.md`

存在问题：
1. 参数表中多个字段描述被截断（如 `country`、`auto_parameters`）。
2. `## 详细内容` 下的 Body/Response 字段出现大段粘连，多个参数说明串在同一段，阅读成本高。
3. 混入 `Show child attributes` 等 UI 文案，未做结构化清洗。

## 总结
- 任务已跑满 11 轮。
- 输出 Markdown **存在内容缺失**（与原网页相比）。
- Markdown **在简单页面可读，在复杂参数页会乱掉**，段落结构不够清晰，建议后续增强字段分段与 UI 噪音过滤。
