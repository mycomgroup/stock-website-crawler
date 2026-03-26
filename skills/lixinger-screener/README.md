# lixinger-screener

理杏仁筛选工具现在统一放在这个目录下，分成两套可独立运行的实现：

- `browser/`: 浏览器自动化版本，适合自然语言 + Playwright 操作页面
- `request/`: 纯请求版本，适合直接读取筛选器配置、拼请求体并返回结果
- 两套实现现在共用同一份输入 schema：既支持 `--query` 自然语言，也支持 `--input-file` 参数文件

常用命令：

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/lixinger-screener

# 浏览器版：自然语言
node run-skill.js --query "PE-TTM(扣非)统计值10年分位点小于30%，股息率大于2%"

# 浏览器版：统一参数文件
node run-skill.js --input-file unified-input.example.json --headless false

# 浏览器版：指定 screener 页面和 profile
node run-skill.js \
  --url "https://www.lixinger.com/analytics/screener/company-fundamental/cn?screener-id=587c4d21d6e94ed9d447b29d" \
  --profile-dir /path/to/chrome-profile

# request 版：自然语言
node request/fetch-lixinger-screener.js --query "PE-TTM(扣非)统计值10年分位点小于30%，股息率大于2%" --output markdown

# request 版：统一参数文件
node request/fetch-lixinger-screener.js --input-file unified-input.example.json --output csv

# request 版：按筛选器入口直接调用
npm run request:fund-cn -- --output markdown
npm run request:index-cn -- --output markdown
npm run request:company-hk -- --output markdown
npm run request:company-us -- --output markdown
npm run request:index-hk -- --output markdown
```

新增的独立 request 入口对应以下页面：

- `request/fetch-fund-fundamental-cn.js`
  对应 `https://www.lixinger.com/analytics/screener/fund-fundamental/cn`
- `request/fetch-index-fundamental-cn.js`
  对应 `https://www.lixinger.com/analytics/screener/index-fundamental/cn`
- `request/fetch-company-fundamental-hk.js`
  对应 `https://www.lixinger.com/analytics/screener/company-fundamental/hk`
- `request/fetch-company-fundamental-us.js`
  对应 `https://www.lixinger.com/analytics/screener/company-fundamental/us`
- `request/fetch-index-fundamental-hk.js`
  对应 `https://www.lixinger.com/analytics/screener/index-fundamental/hk`

它们都复用 `request/screener-runner.js`，由 runner 根据入口预设切换正确的 API 端点、`ranges`、`industrySource` 和分页逻辑；每个筛选器仍然保持独立入口文件，避免大改现有结构。

所有理杏仁相关入口现在都只保留在这个目录下，不再保留 `stock-crawler/scripts` 里的兼容包装。

浏览器版登录优先级：

- 已保存的 `storageState`
- `--profile-dir` 或 `LIXINGER_BROWSER_PROFILE_DIR`
- 登录接口写 cookie
- 浏览器表单自动登录

统一参数文件示例见：

- `unified-input.example.json`

参数文件里可以手写 `conditions`，也可以带一个 `query` 字段；当前两套入口都会把它们合并处理。推荐的 condition 结构是：

```json
{
  "metric": "PE-TTM统计值",
  "selectors": ["10年", "分位点%"],
  "min": 0,
  "max": 30
}
```

---

## 如何筛选有价值的股票

### condition 参数结构

```json
{
  "metric": "指标名称",
  "selectors": ["时间维度", "计算方式"],
  "min": 数字,
  "max": 数字
}
```

自然语言模式下也支持 `operator` + `value` 写法：

```json
{
  "metric": "股息率",
  "operator": "大于",
  "value": 2
}
```

### 经典筛选策略

**低估值 + 高股息（价值投资基础组合）**

```json
{
  "name": "低估值高股息",
  "conditions": [
    { "metric": "PE-TTM(扣非)统计值", "selectors": ["10年", "分位点%"], "max": 30 },
    { "metric": "PB(不含商誉)统计值", "selectors": ["10年", "分位点%"], "max": 30 },
    { "metric": "股息率", "min": 2 },
    { "metric": "上市日期", "max": "2015-01-01" }
  ],
  "sort": { "metric": "股息率", "order": "desc" }
}
```

逻辑：PE/PB 历史分位点低于 30% 说明当前估值处于历史低位；股息率 > 2% 保证有现金回报；上市超 10 年过滤新股炒作期。

**高质量合理价**

```json
{
  "name": "高质量合理价",
  "conditions": [
    { "metric": "市盈率(TTM)", "operator": "介于", "value": [10, 30] },
    { "metric": "净资产收益率(TTM)", "operator": "大于", "value": 15 },
    { "metric": "毛利率(TTM)", "operator": "大于", "value": 25 },
    { "metric": "营业收入增长率(3年复合)", "operator": "大于", "value": 10 },
    { "metric": "净利润增长率(3年复合)", "operator": "大于", "value": 10 },
    { "metric": "资产负债率", "operator": "小于", "value": 45 }
  ],
  "sort": { "metric": "净资产收益率(TTM)", "order": "desc" }
}
```

建议：这套优先用浏览器版自然语言试，因为它更贴近页面字段和交互。

**现金流防雷**

```bash
node run-skill.js --query "市值/自由现金流小于20，股息率(TTM)大于3%，净利润率(TTM)大于10%，资产负债率小于50%" --headless false
```

建议：这套也优先用浏览器版先试，确认结果数量和字段映射都正常。

**自然语言方式（最简单）**

```bash
node request/fetch-lixinger-screener.js \
  --query "PE-TTM(扣非)统计值10年分位点小于30%，股息率大于2%，上市日期早于2015年" \
  --output markdown
```

### 关键参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `selectors[0]` 时间维度 | `3年` / `5年` / `10年` | `10年`（最严格） |
| `selectors[1]` 计算方式 | `分位点%` / `均值` / `标准差` | `分位点%`（最直观） |
| `ranges.excludeSpecialTreatment` | 排除 ST 股 | `true` |
| `ranges.excludeDelisted` | 排除退市股 | `true` |
| `industrySource` | 行业分类标准 | `sw_2021`（申万2021） |
| `sort.order` | 排序方向 | `asc` / `desc` |

### 识别"有价值"的核心逻辑

- 估值历史分位点 < 30% — 当前便宜，相对自身历史
- 股息率 > 2% — 有真实现金回报，不是纯炒作
- ROE > 12% — 公司有持续盈利能力
- 上市 > 5 年 — 过滤掉新股炒作期
- 排除 ST — `ranges.excludeSpecialTreatment: true`

### 三套样例

`unified-input.example.json` 现在保留第一套“低估值高股息”的可直接运行样例。其余两套建议直接用下面的浏览器命令试：

```bash
node run-skill.js --query "市盈率(TTM)介于10到30，净资产收益率(TTM)大于15%，毛利率(TTM)大于25%，营业收入增长率(3年复合)大于10%，净利润增长率(3年复合)大于10%，资产负债率小于45%" --headless false
```

```bash
node run-skill.js --query "市值/自由现金流小于20，股息率(TTM)大于3%，净利润率(TTM)大于10%，资产负债率小于50%" --headless false
```
