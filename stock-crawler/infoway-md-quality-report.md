# Infoway 任务执行与 Markdown 质量检查报告

## 执行结论

- 已按 `stock-crawler/config/infoway.json` 连续执行 **10 轮**爬取。
- 10 轮均成功结束，但每轮日志都出现 `Link discovery failed`，导致没有发现新的文档链接。
- 当前输出仅有一个页面文件 `overview.md`，且内容极短。

## 10 轮运行情况

- 轮次：1~10
- 每轮统计均为：
  - Total URLs: 1
  - Crawled: 1
  - Failed: 0
  - New Links Found: 0
  - Files Generated: 1
- 这说明爬虫每次都只抓取首页，未扩展到侧边栏文档树。

## Markdown 输出检查

### 实际输出（overview.md）

当前 `overview.md` 只有：

```md
# 欢迎 | Infoway API Docs

## 源URL

https://docs.infoway.io/
```

### 与原页面内容对比

通过浏览器渲染检查原页面，正文包含大量结构化内容（例如“欢迎来到Infoway API文档 / 什么是Infoway API / 主要特点 / 适用对象 / 使用场景”等），并且侧边栏包含多个文档入口（如 A 股/港股/美股实时行情接口、REST API、WEBSOCKET API 等）。

因此，当前 Markdown 相比原页面存在**明显缺失**：

- 缺失绝大多数正文段落内容。
- 缺失侧边栏文档链接及后续页面抓取结果。
- 缺失章节层级（H2/H3）与完整段落文本。

## 格式是否“乱掉”评估

- **结论：Markdown 格式本身没有乱。**
- 目前文件结构非常规整，但属于“内容几乎未抽取”的情况：
  - 标题层级正常（`#` + `##`）。
  - 没有出现乱码、标签残留或段落错乱。
- 真正的问题是**内容严重不完整**，不是排版错乱。

## 根因判断

日志反复出现：

- `Using parser-based link discovery`
- `[InfowayParser] Link discovery failed: page.waitForSelector: Timeout 10000ms exceeded.`
- `waiting for locator('[class*="Sidebar"]') to be visible`

说明 Infoway 站点页面结构（或加载时机）与当前选择器不匹配，导致侧栏未被识别，进而无法发现子页面链接，最终只抓到首页基础信息。

## 建议修复方向

1. **调整侧栏选择器**：不要仅依赖 `[class*="Sidebar"]`，增加 GitBook 常见导航选择器兜底。
2. **增加等待策略**：在 link discovery 前等待主文档容器与导航容器稳定渲染（例如 `networkidle` + 定向 selector）。
3. **加入失败兜底**：当 parser link discovery 失败时，回退到通用 `a[href]` 规则并按 include/exclude 过滤。
4. **加质量门禁**：若正文字符数低于阈值（如 <500）且站点明显有侧栏，标记为“抽取不完整”并告警。

