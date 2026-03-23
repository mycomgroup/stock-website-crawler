# sanhulianghua.json 11轮运行与 Markdown 质量检查（2026-03-16）

## 执行结论（先说结果）

- 已按要求执行 **11 轮以上**（实际为两组 11 轮：首次因环境缺少浏览器依赖失败，补齐依赖后再次完整执行 11 轮）。
- 第二组运行中，第 1~2 轮抓取到全部目标页面（18个页面），第 3~11 轮均可稳定运行。
- Markdown 文件格式本身没有“乱码/结构错乱”，但存在**内容缺失**：18 个页面中有 4 个页面输出为 `# Untitled`，且仅保留源 URL，没有抓到页面标题与接口段落。

## 执行命令与轮次

### 依赖安装

- `npm install`
- `npx playwright install chromium`
- `npx playwright install-deps chromium`

### 11 轮执行

执行脚本（循环 11 次）：

```bash
for i in $(seq 1 11); do
  node src/index.js config/sanhulianghua.json
  # 记录 links.txt 统计
done
```

第二组 11 轮统计（补齐依赖后）：

- ROUND 1 STATS total=17 pending=0 completed=0 failed=0
- ROUND 2 STATS total=17 pending=0 completed=0 failed=0
- ROUND 3 STATS total=17 pending=0 completed=0 failed=0
- ROUND 4 STATS total=17 pending=0 completed=0 failed=0
- ROUND 5 STATS total=17 pending=0 completed=0 failed=0
- ROUND 6 STATS total=17 pending=0 completed=0 failed=0
- ROUND 7 STATS total=17 pending=0 completed=0 failed=0
- ROUND 8 STATS total=17 pending=0 completed=0 failed=0
- ROUND 9 STATS total=17 pending=0 completed=0 failed=0
- ROUND 10 STATS total=17 pending=0 completed=0 failed=0
- ROUND 11 STATS total=17 pending=0 completed=0 failed=0

## Markdown 输出质量检查

检查目录：`output/sanhulianghua-api-docs/pages-20260316-195859`

### 1) 结构是否清晰

- 有效抓取到内容的页面，结构统一为：
  - 一级标题（接口名称）
  - `## 源URL`
  - `## 描述`（若能识别）
  - `## API 端点`（若能识别）
- 因此从 Markdown 语法结构看，**没有段落乱掉**。

### 2) 是否缺失内容

统计发现：

- 18 个 md 中，4 个为 `# Untitled` 且仅 5 行，明显缺失页面主体内容：
  - `jszb_boll.md`
  - `jszb_cci.md`
  - `jszb_wr.md`
  - `lshq_zhouxian.md`

此外，多份文件虽非 Untitled，但也只保留标题+源URL（5行），未抽取请求参数/返回数据（例如 `jszb_ma.md`、`jszb_kdj.md`、`real_hsa_zhishu.md` 等）。

## 与原网站页面对比（抽样）

### 对比样本 A：`page_lshq_zhouxian`

- 原站 HTML 中可看到：
  - 页面标题：`沪深个股周线`
  - 接口说明：`获取沪深两市个股的历史周线数据`
  - 接口地址：`/v1/hsa_zhouxian`
  - 以及“请求参数”“返回数据”表格区块
- 对应 md 文件 `lshq_zhouxian.md` 却为：
  - `# Untitled`
  - `## 源URL`
  - 无“描述/API端点/请求参数/返回数据”

=> 结论：该页面存在明显抽取缺失。

### 对比样本 B：`page_jszb_wr`

- 原站 HTML 中可看到：
  - 页面标题：`沪深个股WR`
  - 说明：`接口说明：即将上线`
- 对应 md 文件 `jszb_wr.md` 为：
  - `# Untitled`
  - `## 源URL`

=> 结论：至少标题抽取失败，存在缺失。

## 可能原因（从日志现象推断）

在第二组成功运行日志中，出现多次：

- `Wait for content timeout: page.waitForSelector: Timeout 15000ms exceeded.`
- 紧接 `Parsed page: Untitled`

说明部分页面在等待 `h2, table, p` 可见时超时，导致解析器回退为最小结果（仅 URL）。

## 回答你的问题（简版）

- **“跑10轮以上”**：已完成（11轮）。
- **“md格式会不会乱掉，结构段落要清晰”**：格式本身不乱，结构模板一致。
- **“和原网站页面有没有缺失”**：有缺失，主要表现为 4 个页面变成 `Untitled`，以及若干页面只抓到标题+URL，未抓到参数/返回数据段落。

