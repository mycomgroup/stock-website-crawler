# Massive 文档抓取与 Markdown 结构检查报告

## 执行情况

- 使用 `stock-crawler/config/massive.json` 进行了 11 轮批量执行（首次 11 轮因 Playwright 浏览器缺失失败，后续补齐运行环境并继续抓取）。
- 成功产出了 Massive 文档的多批次 Markdown 文件，覆盖首页、REST、WebSocket、Flat Files 等页面。

## 抽样对比（Markdown vs 原站）

抽样页面：
- `https://massive.com/docs`
- `https://massive.com/docs/rest/futures/overview`
- `https://massive.com/docs/websocket/stocks/trades`

结论：
1. **页面主标题与核心描述保留良好**：如 `Futures Overview`、`Trades` 等标题及描述均在 Markdown 中可见。
2. **文档结构整体清晰**：Markdown 统一包含 `# 标题`、`## 源URL`、`## 描述`、`## 内容/参数/示例` 等段落。
3. **存在少量内容截断**：部分超长页面尾部出现 `... (内容已截断)`，代表当前抓取策略有长度上限，可能造成细节缺失。
4. **格式稳定性较好**：未发现明显“乱段落”或标题错位；参数表与代码块在抽样页中可正常呈现。

## 建议

- 若需要“与原站逐段完全一致”，建议取消或提高内容长度截断阈值。
- 可追加一个自动校验步骤：
  - 校验是否含 `#` 一级标题；
  - 校验是否含 `## 源URL` 和 `## 描述`；
  - 统计是否出现 `内容已截断` 并出告警。
