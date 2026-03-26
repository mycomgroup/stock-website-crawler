# 股票筛选方法论

## 核心原则

不要一上来把所有参数压满。正确做法是先定股票池，再按"估值 → 质量 → 风险 → 分红"一层层加条件，每次只改 1 到 2 个阈值，反复试。

---

## 参数分工

**ranges** — 先定股票池，后面的条件都在这个池子里跑

| 字段 | 说明 |
|------|------|
| `market` | `a` 表示 A 股全市场 |
| `stockBourseTypes` | 限定板块，空数组 = 不限 |
| `mutualMarkets` | 沪深港通标的过滤 |
| `multiMarketListedType` | AH 股等多市场上市类型 |
| `excludeBlacklist` | 排除黑名单 |
| `excludeDelisted` | 排除退市股，建议 `true` |
| `excludeSpecialTreatment` | 排除 ST，建议 `true` |

**conditions** — 真正判断"值不值得看"的核心，一层层加，别一次全上

**selectors** — 给"统计值"类指标选窗口，比如 `10年`、`分位点%`

**sort** — 决定优先看谁。低估值看 `asc`，高股息看 `desc`，要切换着看

**industrySource + industryLevel** — 固定用 `sw_2021` + `three`，跨行业比 PE/PB 很容易失真

**pageSize** — 先拉 100 就够

**operator/value** — 可以代替 `min`/`max`，自然语言模式常用

**category** — 用来解决重名指标，比如同名指标在不同分类下含义不同

---

## 推荐工作流

先用浏览器版自然语言快速试错，试出手感后再把条件固化成 `input.json`，用 request 版批量导出 CSV。

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/lixinger-screener

# 第一步：快速试错
node run-skill.js --query "市盈率(TTM)小于20，市净率小于2，股息率(TTM)大于3%，净资产收益率(TTM)大于12%，资产负债率小于50%" --headless false

# 第二步：固化后导出
node request/fetch-lixinger-screener.js --input-file ./my-value-screen.json --output csv
```

如果目标不是 A 股公司页，而是基金 / 指数 / 港美股公司页，直接用独立 request 入口：

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/lixinger-screener

node request/fetch-fund-fundamental-cn.js --output markdown
node request/fetch-index-fundamental-cn.js --output markdown
node request/fetch-company-fundamental-hk.js --output markdown
node request/fetch-company-fundamental-us.js --output markdown
node request/fetch-index-fundamental-hk.js --output markdown
```

这些入口分别固定到：

- `fund-fundamental/cn`
- `index-fundamental/cn`
- `company-fundamental/hk`
- `company-fundamental/us`
- `index-fundamental/hk`

---

## 三套筛选模板

### 第一套：低估值高股息

最适合先跑，request 版对"基本指标 + selectors"支持最稳。

```json
{
  "name": "低估值高股息_第一轮",
  "areaCode": "cn",
  "industrySource": "sw_2021",
  "industryLevel": "three",
  "pageSize": 100,
  "ranges": {
    "market": "a",
    "stockBourseTypes": [],
    "mutualMarkets": { "selectedMutualMarkets": [], "selectType": "include" },
    "multiMarketListedType": { "selectedMultiMarketListedTypes": [], "selectType": "include" },
    "excludeBlacklist": true,
    "excludeDelisted": true,
    "excludeSpecialTreatment": true,
    "specialTreatmentOnly": false
  },
  "conditions": [
    { "metric": "PE-TTM(扣非)统计值", "category": "基本指标", "selectors": ["10年", "分位点%"], "max": 30 },
    { "metric": "PB(不含商誉)统计值", "category": "基本指标", "selectors": ["10年", "分位点%"], "max": 30 },
    { "metric": "股息率", "category": "基本指标", "min": 2.5 },
    { "metric": "上市日期", "category": "基本指标", "subCondition": "上市时间", "max": "2015-01-01" }
  ],
  "sort": {
    "metric": "PE-TTM(扣非)统计值",
    "category": "基本指标",
    "selectors": ["10年", "分位点%"],
    "order": "asc"
  }
}
```

### 第二套：高质量合理价

"好公司别太贵"，建议先用浏览器版试。

```bash
node run-skill.js --query "市盈率(TTM)介于10到30，净资产收益率(TTM)大于15%，毛利率(TTM)大于25%，营业收入增长率(3年复合)大于10%，净利润增长率(3年复合)大于10%，资产负债率小于45%" --headless false
```

### 第三套：现金流防雷

排除"利润好看但现金差"的公司。

```bash
node run-skill.js --query "市值/自由现金流小于20，股息率(TTM)大于3%，净利润率(TTM)大于10%，资产负债率小于50%" --headless false
```

---

## 迭代技巧

结果超过 200 只，条件太宽：把估值分位点从 30 收到 20，或把股息率从 2.5 提到 3.5。

结果只有几只，条件太严：一次只放松一个条件。

不同行业不要共用同一套 PE/PB 阈值，最好先限定行业再筛。

第一轮看"便宜"，第二轮一定加"质量"或"现金流"，不然容易掉进价值陷阱。

排序要切换着看：先按低估值排，再按高股息排，再按 ROE 排。
