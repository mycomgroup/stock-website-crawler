# yfinance.json 任务（11轮）Markdown 质量检查

## 执行范围

- 配置文件：`config/yfinance.json`
- 连续运行：11 轮（>10 轮）
- 运行时间区间：`2026-03-16 19:58:51` 到 `2026-03-16 20:06:50`

## 结论（先说结果）

1. **有明显内容缺失**：抓取产出的 Markdown 与原页面相比，缺失了大量 API 条目与结构化导航内容。
2. **Markdown 结构不稳定**：同一个 URL 在不同轮次输出了 3 种不同结果（`API参考` / `yfinance 文档` / `Untitled`），说明解析结果有波动。
3. **结构段落基本可读但信息严重不完整**：Markdown 本身没有明显“乱码”或标签破碎，但章节经常过于稀疏（仅标题+源URL）。

## 11 轮运行证据

- 运行日志统计：`runs=11`，`parsed=11`
- 页面标题出现 3 种解析结果：`API参考`、`yfinance 文档`、`Untitled`

## 对比样例

### 原站页面（节选）

原页面包含大量 API 入口与方法名称，例如：

- `yfinance.Ticker.get_isin`
- `yfinance.Ticker.history`
- `yfinance.Ticker.get_dividends`
- `yfinance.Ticker.actions`

这类条目在页面中是密集出现的导航/参考信息。

### 抓取输出样例 1（过度缺失）

文件：`output/yfinance/yfinance-api-docs/pages-20260316-200650/API.md`

```md
# API参考

## 源URL

https://www.aidoczh.com/yfinance/reference/index.html
```

只有标题和 URL，几乎没有正文内容。

### 抓取输出样例 2（部分内容）

文件：`output/yfinance/yfinance-api-docs/pages-20260316-200137/yfinance.md`

该版本有描述与代码示例，但仍缺失原页面中的大量 API 方法清单与层级导航。

### 抓取输出样例 3（异常退化）

文件：`output/yfinance/yfinance-api-docs/pages-20260316-200256/index.md`

```md
# Untitled

## 源URL

https://www.aidoczh.com/yfinance/reference/index.html
```

该轮次标题退化为 `Untitled`，说明解析稳定性存在问题。

## 对“md格式会不会乱掉，结构段落要清晰”的判断

- **格式层面**：未出现严重 markdown 语法破坏（如代码块未闭合、随机标签混入等）。
- **结构层面**：标题/段落还算清晰。
- **质量层面**：信息密度不稳定，且经常严重缺失，导致文档可用性不足。

## 建议

1. 固定页面主内容容器后再抽取（避免抽到导航壳层或空壳）。
2. 对同 URL 多轮结果做一致性校验（标题、段落数、关键词覆盖率）。
3. 增加“关键术语最低覆盖率”检查（例如 `yfinance.Ticker.*` 至少命中若干项）。
4. 将 `Untitled` 视为低质量结果并自动重试。

