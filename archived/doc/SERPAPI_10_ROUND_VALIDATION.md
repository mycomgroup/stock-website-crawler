# SerpApi 任务 10 轮运行与 Markdown 质量检查

## 执行结论
- 已完成 `config/serpapi.json` 连续 10 轮抓取（另有 1 轮预热运行）。
- 10 轮中前 9 轮无失败，最后 1 轮出现 1 个失败 URL（`/locations.json`，页面触发下载导致 Playwright `page.goto` 报错）。
- Markdown 整体结构稳定，标题层级、代码块围栏、段落结构基本清晰，无批量“格式乱掉”现象。
- 与原页面（`https://serpapi.com/ai-overview`）对比，核心内容未见明显缺失；仅发现一个轻微一致性问题：网页标题 `API Examples` 在 Markdown 中被本地化为 `API 示例`（语义一致，非内容丢失）。

## 运行命令
```bash
npm install
npx playwright install chromium
npx playwright install-deps chromium
npm run crawl config/serpapi.json
for i in $(seq 1 10); do npm run crawl config/serpapi.json > /tmp/serpapi-rounds-success/round-$i.log 2>&1; done
```

## 10 轮结果摘要
- Round 1: Crawled 10 / Failed 0 / Files 10 / Duration 139s
- Round 2: Crawled 10 / Failed 0 / Files 10 / Duration 95s
- Round 3: Crawled 10 / Failed 0 / Files 10 / Duration 106s
- Round 4: Crawled 10 / Failed 0 / Files 10 / Duration 143s
- Round 5: Crawled 10 / Failed 0 / Files 10 / Duration 81s
- Round 6: Crawled 10 / Failed 0 / Files 10 / Duration 111s
- Round 7: Crawled 10 / Failed 0 / Files 10 / Duration 134s
- Round 8: Crawled 10 / Failed 0 / Files 10 / Duration 111s
- Round 9: Crawled 10 / Failed 0 / Files 10 / Duration 96s
- Round 10: Crawled 9 / Failed 1 / Files 9 / Duration 113s

## Markdown 结构检查
检查范围：10 轮输出目录中的 99 个 `.md` 文件。

检查项：
- 每个文件是否有 H1 标题
- 代码块围栏（```）是否成对
- 是否出现明显结构损坏

结果：
- 99/99 文件通过上述结构检查
- 未发现空文件
- 未发现代码块围栏失配

## 页面对比样本（ai-overview）
对比对象：
- 原网页：`https://serpapi.com/ai-overview`
- 抓取文件：`output/serpapi-ai-overview/pages-20260316-195945/ai-overview-api.md`

对比结果：
- 页面主要章节（Typical result、nested lists、table、LaTeX、video、expandable sections、snippet links、products comparison、extra request、error message、JSON structure）在 Markdown 中均可找到。
- 检测到 1 处标题文本差异：`API Examples` -> `API 示例`。
- 检测到 1 处可读性问题：`...above examples.The rendered HTML...` 这类英文句子连接处缺少空格，属于轻微排版问题，不影响主结构。

## 建议
- 若要避免 `/locations.json` 一类下载链接导致失败，可在配置中增加排除规则（如 `\.json$`）或在抓取器中对 `Content-Disposition: attachment` 做跳过处理。
- 若需进一步提升可读性，可在 Markdown 生成阶段增加英文标点后的空格修正（例如 `.` 后接大写字母时补空格的安全规则）。
