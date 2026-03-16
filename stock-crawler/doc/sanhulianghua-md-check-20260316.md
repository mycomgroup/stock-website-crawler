# sanhulianghua.json 抓取结果核查（2026-03-16）

## 运行轮次

- 已执行 10 轮：`rounds-10.log` 中包含 `ROUND 1` 到 `ROUND 10`。
- 初始 10 轮因 Playwright 缺少系统依赖失败（`libatk-1.0.so.0`）。
- 安装浏览器与系统依赖后再次运行，成功产出 markdown 文件（见 `rounds-10-after-deps.log`）。

## 输出 Markdown 结构检查

### 1) `base_hsa_gupiao.md`

- Markdown 内容包含：标题、源 URL、描述、API 端点。
- 原网页包含更多内容：
  - 安全接口地址（HTTPS）
  - 请求参数（表格）
  - 返回数据（表格）
- 结论：该 md 结构清晰，但有明显字段缺失。

### 2) `jszb_ma.md`

- Markdown 仅有标题 + 源 URL。
- 原网页仅有“接口说明：即将上线”，暂无参数/返回表。
- 结论：该 md 不算“乱”，但信息非常少，基本与页面信息量一致。

### 3) 其他已生成文件（`jszb_wr.md`、`jszb_kdj.md`、`jszb_cci.md`、`jszb_rsi.md`）

- 目前也多为“标题 + 源 URL”；其中 `jszb_rsi.md` 标题为 `Untitled`。
- 结论：段落结构没有错乱，但抽取完整性偏弱（尤其标题识别与正文抽取）。

## 综合判断

- **Markdown 是否会乱掉**：本次样本中未见明显格式错乱（标题层级、段落分隔正常）。
- **是否有缺失**：有，尤其是 `base_hsa_gupiao.md` 缺少网页中的“安全接口 / 请求参数 / 返回数据”区块。
- **结构段落是否清晰**：清晰，但内容覆盖率不足。
