# AllTick 抓取结果校验（11轮）

## 执行目标
- 使用 `config/alltick.json` 连续运行爬虫 **11 轮**。
- 检查输出 Markdown 是否与原网页内容一致，是否存在缺失。
- 检查 Markdown 结构/段落是否清晰、是否错乱。

## 实际执行命令
1. `cd stock-crawler && npx playwright install chromium`
2. `cd stock-crawler && npx playwright install-deps chromium`
3. `cd stock-crawler && for i in $(seq 1 11); do echo "===== ROUND $i ====="; npm run crawl config/alltick.json; done | tee ../alltick-11-rounds-after-deps.log`

## 运行结果摘要
- 11 轮均执行完成。
- 每轮均只处理 1 个 URL（`https://apis.alltick.co/`）。
- 每轮均提示：`[AlltickParser] Link discovery failed: ... waiting for locator('[class*="Sidebar"]')`，因此未发现新链接。
- 每轮均输出同一个文件名：`overview.md`。

## Markdown 输出检查
最新一轮目录：`output/alltick-api-docs/pages-20260316-195824/`。

`overview.md` 内容非常短，仅包含：
- 标题：`欢迎 | AllTick API Docs`
- 源 URL：`https://apis.alltick.co/`

这说明当前 markdown 抽取几乎没有抓到正文信息。

## 与原网站页面对比
通过 Playwright 直接读取在线页面 `https://apis.alltick.co/`：
- `TITLE`: `欢迎 | AllTick API Docs`
- `MAIN_TEXT_LEN`: `1386`
- 页面正文实际包含多个完整段落，例如：
  - “欢迎光临 AllTick API文档部分...”
  - “什么是AllTick”
  - “主要特点”
  - 多条说明性段落

结论：**当前生成的 Markdown 相比原页面存在明显、大量内容缺失**。

## 结构与段落清晰度结论
- 当前输出的 Markdown 本身并未出现“格式错乱”现象（标题 + 源 URL 结构是规整的）。
- 但内容抽取严重不足，导致“结构清晰但信息不完整”。
- 从可用性角度看，当前结果不满足“页面内容完整还原”的要求。

## 可能原因（从日志推断）
- 站点是 GitBook 动态结构。
- 解析器在侧边栏发现阶段超时（等待 `[class*="Sidebar"]` 失败），导致链接扩展和正文抽取链路受限。

## 建议
1. 优先修复 `AlltickParser` 的侧边栏选择器策略（增加 GitBook 新版 selector 兜底）。
2. 在正文抽取前增加主内容区兜底提取（如 `main` 内文本分块提取），避免仅输出标题。
3. 对该站点加一条站点级 smoke test：要求 markdown 最小字符数（如 >500）并校验关键小标题（如“什么是AllTick”）。
