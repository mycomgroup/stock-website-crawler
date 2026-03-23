# modelscope-mcp.json 12轮任务执行与Markdown质量检查

## 执行目标

按要求对 `config/modelscope-mcp.json` 连续执行超过 10 轮抓取，并核对输出 Markdown：

1. 与原页面相比是否存在内容缺失。
2. Markdown 结构是否清晰。
3. Markdown 格式是否会乱掉（不稳定）。

## 执行命令

```bash
cd stock-crawler
npx playwright install chromium
npx playwright install-deps chromium
for i in $(seq 1 12); do
  echo "===== ROUND $i ====="
  npm run crawl -- config/modelscope-mcp.json
 done
```

日志已记录到：`stock-crawler/tmp/modelscope-12rounds.log`。

## 运行结果（12轮）

- 成功执行 12 轮（满足“10轮以上”要求）。
- 最终链接池仅包含 2 个 URL：
  - `https://modelscope.cn/mcp`
  - `https://modelscope.cn/mcp/playground`
- 每轮大多数情况下只会重复抓取 seed 页面（`/mcp`）。

`links.txt` 最终状态：2 条链接均为 `fetched`。

## Markdown 稳定性检查

对 12 份 `mcp_overview.md` 做了长度与结构统计：

- 存在 3 类明显不同输出：
  - 长版：约 `12423` / `12585` 字符，`##` 标题数为 6。
  - 短版A：约 `2778` 字符，`##` 标题数为 4，含代码块。
  - 短版B：约 `2362` 字符，`##` 标题数为 4，含代码块。

结论：**同一页面在不同轮次输出波动很大，Markdown 会“乱跳”**，格式与内容稳定性不足。

## 与原网页对比（是否缺失）

基于浏览器读取到的页面文本快照，页面主体包含：

- 顶部导航（Home / Models / Datasets / Studios / Docs / Community / MCP 等）
- MCP 广场主视觉文案
- Playground / Tutorial / Cherry Studio / DingTalk / Intel / Kimi 等入口

Markdown 对比结果：

- 优点：
  - 主要入口链接大体可保留（尤其在短版中较清晰）。
- 问题：
  1. **内容缺失明显**：大量页面文本在某些轮次未进入结构化段落，仅残留在 `完整内容` 或被丢失。
  2. **结构不一致**：有时输出“服务器信息 + 标签 + 配置”，有时只剩“可用工具 + 相关链接 + 完整内容”。
  3. **段落可读性波动**：长版出现多条“拼接式”超长条目（字段串联、重复片段），可读性差。

综合判断：

- **有缺失**：是。
- **md 格式会乱掉**：会。
- **结构段落是否始终清晰**：否（仅部分轮次较清晰，整体不稳定）。

## 建议

1. 对动态页面增加“稳定等待条件”（例如特定卡片容器出现后再解析），减少轮次间抖动。
2. 对“卡片列表”使用更强约束的结构化提取，避免把碎片文本串接为超长段落。
3. 为同一 URL 增加质量门槛（标题数量、最小长度、关键区块存在性），不达标则重试。
4. 若目标是抓取 MCP server 详情，建议补充列表页到详情页 URL 提取策略，避免长期只停留在 `/mcp` 与 `/playground` 两页。
