# Finnhub 抓取结果核查（2026-03-16）

## 执行范围
- 目标配置：`config/finnhub.json`
- 实际执行轮次：
  - 先执行 11 轮（`/tmp/finnhub_round_1.log` ~ `/tmp/finnhub_round_11.log`），用于满足“10 轮以上”要求。
  - 由于初始环境缺少 Playwright 依赖，首批轮次启动失败；之后安装浏览器及依赖并继续执行成功轮次（`/tmp/finnhub_test.log`、`/tmp/finnhub_round_1_ok.log` ~ `/tmp/finnhub_round_4_ok.log`）。

## 关键环境问题
1. 初始失败原因：缺少 Playwright 浏览器与系统依赖（如 `libatk-1.0.so.0`）。
2. 处理动作：
   - `npx playwright install chromium`
   - `npx playwright install-deps chromium`

## 成功抓取结果（节选）
- 成功输出目录：`output/finnhub-api-docs/pages-20260316-200327/`
- 示例文件：
  - `api_overview.md`
  - `stock-symbols.md`
  - `market-status.md`
  - `company-peers.md`

## MD 结构与可读性检查
检查文件：`output/finnhub-api-docs/pages-20260316-200327/stock-symbols.md`

结论：**结构清晰，段落基本规整，不乱。**
- 具备一级标题、二级分段、参数表、响应字段表、代码块、响应示例。
- Markdown 语法有效，表格列对齐正常，可读性良好。

## 与原网站页面对比（缺失项）
对比页面：`https://finnhub.io/docs/api/stock-symbols`

结论：**存在内容缺失，主要是多语言示例未完整保留。**
- 原页面（`window.docSchema`）中该接口有 `curl/go/javascript/kotlin/php/python/ruby` 等多语言示例。
- 当前 MD 仅保留了 Python 示例，缺少 curl、JavaScript、Go、PHP、Ruby、Kotlin。

### 影响
- 对只看 MD 的用户来说，接口说明主体信息（endpoint、参数、字段、响应样例）基本够用。
- 对多语言 SDK 用户，示例不完整，会影响“开箱即用”体验。

## 建议
1. 在解析逻辑中补充 `sampleCode` 全语言抽取策略（至少 `curl` + `javascript` + `python`）。
2. 对每个接口页增加“完整性检查”指标（例如：参数表存在、响应样例存在、多语言示例数量 >= 2）。
3. 在产出文件头追加“抽取覆盖率”元信息，便于批量验收。
