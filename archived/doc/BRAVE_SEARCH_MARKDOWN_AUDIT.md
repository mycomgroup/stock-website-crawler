# Brave Search 文档抓取与 Markdown 质量检查

## 执行摘要

- 已执行 `brave-search.json` 任务并累计运行 **10 轮以上**（本次环境中累计生成了 38 份轮次日志/页面目录）。
- 当前 `links.txt` 状态：`fetched=33`、`unfetched=8`、`fetching=2`，说明任务尚未完全收敛，但已经产出可评估的 Markdown。
- Markdown 总体结构可读，标题层级和代码块基本正常；但存在少量段落拼接问题（多卡片内容被合并在同一行，影响阅读）。

## 运行观察

- 首次运行时因浏览器依赖缺失导致失败，补齐 Playwright 依赖后可正常抓取并输出 Markdown。
- 典型成功轮次：
  - `crawler-20260316-195913.log`：抓取 2 页，发现 49 条新链接。
  - `crawler-20260316-195956.log`：抓取 25 页，发现 824 条新链接。

## Markdown 质量检查

### 1) 结构是否清晰

- 正常项：
  - 页面以 H1 标题起始（如 `# Documentation`、`# Brave Search - API`）。
  - `##` 分节明显。
  - API 示例使用 fenced code block（```bash / ```json），可读性较好。
- 异常项：
  - 在 `documentation.md` 中，部分“卡片列表”被拼接在同一行（例如 `Web Search ... News Search ... Image Search ...`），段落分隔不够清晰。
  - 在 `documentation-pricing.md` 也有类似长句拼接现象。

### 2) 与原页面信息是否有明显缺失

- `documentation` 页面核心区块（Get started / Search APIs / AI-Powered Features / API Reference）在抓取结果中均可见。
- API Reference 细节页（如 `search-get.md`）含 endpoint、header/parameter 表格、请求与响应示例，主体信息较完整。
- 但因目标站点为前端渲染页面，个别细节可能受运行轮次与页面动态加载影响，仍建议继续跑到 `unfetched=0` 后再做终版对齐。

## 结论

- **是否缺失：** 暂未发现核心板块的大面积缺失，但仍有未抓取链接，不能断言 100% 完整。
- **MD 是否会乱：** 大多数页面结构正常；少数页面存在段落拼接导致的“看起来有点乱”，主要体现在卡片/多列信息被压平为单段。
- **结构段落是否清晰：** 整体“可读”，但并非“完全清晰”，建议后续增强列表/卡片分段策略。
