# PolyRouter 配置运行与 Markdown 质量检查报告（2026-03-16）

## 运行结论（先看）

- 已按要求执行 `config/polyrouter.json`，共运行 **11 轮**。
- 抓取到 `links.txt` 中 **25 条 URL**，状态均为 `fetched`。
- Markdown 结构整体没有“乱码”或语法破坏，标题、段落、代码块基本可读。
- 但存在**内容缺失**现象：部分 API 页只保留了标题+简短描述+一个很短代码片段，未完整保留参数、响应结构等详情。
- 发现一个无效路由产物：`get-league-info` 被抓成了 `Page Not Found`。

## 我执行的命令

```bash
cd stock-crawler
npm install
npx playwright install chromium
npx playwright install --with-deps chromium
for i in $(seq 1 11); do echo "===== ROUND $i ====="; npm run crawl config/polyrouter.json || break; done
```

## 运行轮次概览

- Round 1：初始化抓取首页，发现新链接。
- Round 2~4：逐步完成 API 页面抓取（批量 10 + 10 + 7）。
- Round 5~11：由于队列耗尽，主要重复抓取根页面 `https://docs.polyrouter.io/`。

## 数据完整性检查

### 链接状态

`links.txt` 中共 25 条 URL，全部为 `"status":"fetched"`（包含 sports / markets / events / series / profile 等路径）。

### 文件数量

- 所有轮次累计生成 `.md` 文件 35 个（含重复轮次输出目录）。
- 去重后唯一 Markdown 文件名 25 个，对应 25 条 URL。

## Markdown 结构质量

整体结构是统一模板：

1. 一级标题（页面标题）
2. `## 源URL`
3. `## 描述`
4. 可选 `## 章节` / `## 代码示例` / `## 详细内容`

从渲染角度看：

- 标题层级正常；
- 段落分段正常；
- 代码块闭合正常；
- 未发现明显 Markdown 语法损坏或段落错乱。

## 缺失与偏差（对比原页面）

### 1) 明显缺失：API 细节被大幅压缩

示例：`api-reference_sports_list-games.md`

- 当前仅有简述 + 一个很短 JSON 数组示例；
- 原站页面通常包含更完整的请求参数、响应示例、状态码与字段说明（抓取 HTML 可见大量结构化内容）；
- 结论：该页面的 Markdown 不是“乱”，而是“被过度摘要”。

### 2) 无效页面被保存为有效文档

示例：`api-reference_sports_get-league-info.md`

- 文件内容仅为 `# Page Not Found` + 源 URL；
- 同时 `links.txt` 中存在正确路由 `get-league-information`；
- 说明链接发现阶段收到了旧/错误路径，且未在落盘前做 404 过滤。

## 建议

1. 在解析器中区分“摘要模式”和“保真模式”，针对 API 文档默认保真（保留参数/响应 schema）。
2. 对 HTTP 404 或页面标题为 `Page Not Found` 的页面，不输出最终 Markdown，改写为失败状态或重定向。
3. 对 Mintlify/Next.js 文档页，优先抓取主内容容器的结构化 DOM，而不是只取首段与零散 code snippet。
4. 轮次执行建议改为“直到 unfetched 为 0 自动停止”，避免 Round 5+ 的重复抓取。

