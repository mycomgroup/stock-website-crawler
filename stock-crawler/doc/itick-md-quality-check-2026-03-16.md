# iTick 抓取结果质量检查（2026-03-16）

## 执行概况

- 任务配置：`config/itick.json`
- 累计执行轮次：
  - 第一批：11 轮（早期因 Playwright/系统依赖问题失败）
  - 第二批：11 轮尝试（修复依赖后，至少前 2 轮成功并产生页面；第 3 轮执行中断）
- 关键进展（成功轮次）：
  - Round 1 结束后仍有 `50 unfetched URLs remaining`
  - Round 2 结束后仍有 `46 unfetched URLs remaining`

## 产出目录

- 主要抽样目录：`output/itick-api-docs/pages-20260316-195800/`
- 该目录共 13 个 Markdown 文件，包括：
  - `en_error-code.md`
  - `en_getting-started.md`
  - `en_websocket_stocks.md`
  - 等。

## 与原站页面对比（抽样）

### 1) `/en/websocket/stocks`

- 原站页面结构特征（浏览器抓取）：
  - `h1`: 1 个
  - `h2`: 1 个（`Stock WebSocket`）
  - 代码块：14 个
  - 表格：0 个
- 对应 Markdown：`en_websocket_stocks.md`
  - 保留了大量示例代码块（示例 1~14），主体内容基本齐全。
  - 但 `h1` 行将标题、副标题、简介挤在同一行，不够清晰。

### 2) `/en/error-code`

- 原站页面结构特征（浏览器抓取）：
  - `h1`: 1 个
  - `h2`: 1 个（`Error Codes`）
  - 表格：1 个
- 对应 Markdown：`en_error-code.md`
  - 内容出现明显噪音：导航栏、页脚、法律声明、站点栏目等混入正文。
  - 错误码表没有转换为标准 Markdown 表格，而是退化成纯文本行。
  - 结构段落可读性较差。

### 3) `/en/getting-started`

- 对应 Markdown：`en_getting-started.md`
  - 主体流程（账号准备、API Key 获取、服务介绍）保留。
  - 同样存在导航栏与页脚混入正文的问题。
  - 文档章节边界不明显，段落层次不够清楚。

## 结论

- **是否有缺失**：
  - 抽样看，核心正文大体有抓到（特别是示例代码）；
  - 但在部分页面（如 error-code）存在结构化信息退化（表格丢失为纯文本）与模板噪音混入，属于“信息质量缺失”。

- **Markdown 会不会乱掉**：
  - 会，且较明显；
  - 主要问题是：标题拼接、导航/页脚污染、表格未结构化、段落边界不清。

- **结构段落是否清晰**：
  - 当前结果 **不够清晰**，需要进一步清洗与结构化提取优化。

## 建议优化方向

1. 在解析阶段过滤 `header/nav/footer` 及全局菜单容器。
2. 针对 docs 页面优先提取 `main article` 区域，降低模板噪音。
3. 增强表格提取策略，确保输出 Markdown 表格语法。
4. 标题与描述分离，避免多个字段拼接到单一 `#` 标题行。
5. 对段落/列表增加二次格式化，提升可读性。
