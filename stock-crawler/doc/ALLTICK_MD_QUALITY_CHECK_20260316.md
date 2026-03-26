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

---

## 2026-03-18 追加执行记录（本次修复后）

### 代码修复点
- `src/parsers/alltick-api-parser.js`
  - 扩展 GitBook 导航/侧边栏 selector（`nav`、`role=navigation`、`data-testid*=sidebar`）以提升链接发现率。
  - 主内容提取改为“候选节点打分”策略，避免误取到菜单容器导致正文缺失。
  - 增加关键字段兜底：`title`/`description` 在结构化抽取失败时仍可从页面文本回填。
  - Markdown 表格输出增加 `|` 和换行转义，降低格式破损概率。
  - 增加 `networkidle` 等待与更长 SPA 渲染等待时间。

### 本次多轮执行
执行时间：**2026-03-18（UTC）**  
命令：`for i in $(seq 1 3); do npm run crawl config/alltick.json; done`

结果：
- 3 轮均成功进入爬虫流程，但在浏览器启动阶段失败。
- 失败原因为运行环境缺少系统动态库：`libatk-1.0.so.0`，导致 Playwright Chromium 无法启动。
- 因页面未实际打开，本轮未生成新的 Markdown 文件，无法对新产物做线上内容一致性比对。

### 新增站点级 Markdown 质量校验脚本
- 新增：`scripts/validate-alltick-markdown.js`
- 功能：
  - 校验最新 `pages-*` 目录是否存在 Markdown 文件；
  - 校验 H1 标题、最小正文长度（>=300）、连续空行、表格分隔符等格式约束；
  - 以非零状态码返回失败，适合接入 CI / smoke test。
