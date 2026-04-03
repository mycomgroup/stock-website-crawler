---
name: akshare-data-query
description: 通过 AkShare 库查询中国金融市场的全面数据，包括股票、债券、基金、期货、指数和宏观经济数据。适用于需要获取东方财富、新浪、集思录等多源数据的场景。
---

# AkShare 数据查询 Skill

通过 [AkShare](https://www.akshare.xyz/) 库获取中国金融市场的全面数据，涵盖股票、债券、基金、期货、指数和宏观经济等多个领域。

## 核心定位

该 skill 是 **AkShare 数据查询的执行入口**，负责：
- 执行 AkShare 数据查询
- 提供 800+ 接口的文档索引
- 支持股票、债券、基金、期货、宏观等多类数据

数据来源包括：东方财富、新浪、集思录、同花顺等主流金融数据平台。

## 核心功能

- **股票数据**：A股/港股/美股实时和历史行情、财务数据、龙虎榜、融资融券等
- **债券数据**：可转债、国债、企业债、债券指数等
- **基金数据**：ETF、开放式基金、基金经理、基金持仓等
- **期货数据**：国内期货、外盘期货、期货持仓、库存等
- **指数数据**：A股指数、港股指数、美股指数、概念板块等
- **宏观数据**：中国、美国、欧洲等全球宏观经济指标

## 最佳实践

### 查询入口选择

1. **先搜索接口**：使用关键词搜索找到合适的接口
   ```bash
   grep -r "可转债" .
   grep -r "龙虎榜" .
   grep -r "ETF" .
   ```

2. **查看接口文档**：打开对应的 `.md` 文件了解参数和返回值

3. **执行查询**：使用 Python 直接调用 AkShare

### 参数优化建议

- **使用筛选参数**：大多数接口支持日期范围、股票代码等筛选条件
- **注意复权**：股票历史数据支持前复权(`qfq`)和后复权(`hfq`)
- **处理 Cookie**：部分接口（如集思录）需要设置 Cookie 获取完整数据

## 使用方法

### 查找接口

在 `docs` 目录下搜索关键词：

```bash
# 搜索可转债相关接口
grep -r "可转债" .

# 搜索龙虎榜相关接口
grep -r "龙虎榜" .

# 搜索基金相关接口
grep -r "基金" .
```

### 查看接口文档

每个接口都有对应的 `.md` 文档，包含：
- 接口名称和描述
- 输入参数说明
- 输出字段说明
- 调用示例代码

**示例文档结构**：
```markdown
接口: stock_zh_a_hist

目标地址: https://quote.eastmoney.com/...

描述: 东方财富-沪深京 A 股日频率数据

输入参数

| 名称     | 类型  | 描述                   |
|--------|-----|----------------------|
| symbol | str | symbol='603777'; 股票代码 |
| ...    | ... | ...                  |

输出参数

| 名称  | 类型      | 描述   |
|-----|---------|------|
| 日期  | object  | 交易日  |
| ... | ...     | ...  |

接口示例

```python
import akshare as ak
stock_zh_a_hist_df = ak.stock_zh_a_hist(...)
```
```

### 执行查询

所有接口均通过 Python 直接调用：

```python
import akshare as ak

# 示例 1：查询 A股历史数据
df = ak.stock_zh_a_hist(
    symbol="000001", 
    period="daily", 
    start_date="20240101", 
    end_date="20241231", 
    adjust="qfq"
)

# 示例 2：查询可转债数据
df = ak.bond_cb_jsl(cookie="your_cookie")

# 示例 3：查询 ETF 实时行情
df = ak.fund_etf_spot_em()

# 示例 4：查询宏观经济数据
df = ak.macro_china_gdp()
```

## 接口分类

### 股票数据（300+ 接口）

| 功能分类 | 示例接口 | 说明 |
|---------|---------|------|
| 实时行情 | `stock_zh_a_spot_em` | A股实时行情（东方财富） |
| 历史行情 | `stock_zh_a_hist` | A股历史日线数据 |
| 港股行情 | `stock_hk_spot_em` | 港股实时行情 |
| 美股行情 | `stock_us_spot_em` | 美股实时行情 |
| 财务数据 | `stock_financial_analysis_indicator_em` | 财务分析指标 |
| 龙虎榜 | `stock_lhb_detail_em` | 龙虎榜详情 |
| 大宗交易 | `stock_changes_em` | 大宗交易数据 |
| 融资融券 | `stock_margin_sse` | 融资融券数据 |
| 股东数据 | `stock_gdfx_holding_detail_em` | 股东持股详情 |
| 分红送转 | `stock_fhps_em` | 分红配送数据 |
| 概念板块 | `stock_board_concept_name_em` | 概念板块列表 |
| 行业板块 | `stock_board_industry_name_em` | 行业板块列表 |

### 债券数据（50+ 接口）

| 功能分类 | 示例接口 | 说明 |
|---------|---------|------|
| 可转债 | `bond_cb_jsl` | 集思录可转债数据 |
| 可转债行情 | `bond_zh_hs_cov_spot` | 可转债实时行情 |
| 国债 | `bond_china_yield` | 国债收益率曲线 |
| 企业债 | `bond_corporate_issue_cninfo` | 企业债发行信息 |

### 基金数据（100+ 接口）

| 功能分类 | 示例接口 | 说明 |
|---------|---------|------|
| ETF行情 | `fund_etf_spot_em` | ETF实时行情 |
| ETF历史 | `fund_etf_hist_em` | ETF历史数据 |
| 开放式基金 | `fund_open_fund_daily_em` | 开放式基金行情 |
| 基金经理 | `fund_manager_em` | 基金经理信息 |
| 基金持仓 | `fund_portfolio_hold_em` | 基金持仓详情 |

### 期货数据（100+ 接口）

| 功能分类 | 示例接口 | 说明 |
|---------|---------|------|
| 期货行情 | `futures_zh_spot` | 期货实时行情 |
| 期货历史 | `futures_zh_daily_sina` | 期货日线数据 |
| 期货持仓 | `futures_hold_pos_sina` | 期货持仓排名 |
| 期货库存 | `futures_inventory_em` | 期货库存数据 |

### 指数数据（100+ 接口）

| 功能分类 | 示例接口 | 说明 |
|---------|---------|------|
| A股指数 | `index_zh_a_hist` | A股指数历史数据 |
| 指数成分股 | `index_stock_cons` | 指数成分股列表 |
| 概念指数 | `stock_board_concept_spot_em` | 概念板块行情 |
| 行业指数 | `stock_board_industry_spot_em` | 行业板块行情 |

### 宏观数据（200+ 接口）

| 功能分类 | 示例接口 | 说明 |
|---------|---------|------|
| 中国GDP | `macro_china_gdp` | 国内生产总值 |
| 中国CPI | `macro_china_cpi` | 居民消费价格指数 |
| 中国PPI | `macro_china_ppi` | 工业生产者出厂价格 |
| 中国PMI | `macro_china_pmi` | 采购经理指数 |
| 利率数据 | `macro_china_lpr` | 贷款市场报价利率 |
| 货币供应 | `macro_china_money_supply` | 货币供应量 |
| 美国宏观 | `macro_usa_cpi_monthly` | 美国CPI |
| 欧洲宏观 | `macro_euro_cpi_yoy` | 欧元区CPI |

## 注意事项

### 安装依赖

使用前需安装 AkShare：

```bash
pip install akshare
```

### Cookie 设置

部分接口需要设置 Cookie 才能获取完整数据：

- **集思录接口**（如 `bond_cb_jsl`）：需要设置集思录 Cookie
- 获取方法：登录集思录网站，从浏览器开发者工具中复制 Cookie

### 数据复权

股票历史数据支持三种复权方式：

- **不复权**（默认）：原始价格
- **前复权**（`qfq`）：保持当前价格不变，调整历史价格
- **后复权**（`hfq`）：保持历史价格不变，调整当前价格

**建议**：量化研究通常使用后复权数据。

### 数据源说明

- 东方财富：A股、基金、债券等主要数据
- 集思录：可转债数据
- 新浪：港股、美股、期货等
- 同花顺：概念板块、行业板块

### 数据更新频率

- 实时行情：交易时间实时更新
- 日线数据：收盘后更新
- 财务数据：财报发布日更新
- 宏观数据：按发布周期更新（月度/季度/年度）

## 接口文档索引

当前目录包含 800+ 个接口文档，按功能分类：

- `stock_*.md` - 股票相关接口
- `bond_*.md` - 债券相关接口
- `fund_*.md` - 基金相关接口
- `futures_*.md` - 期货相关接口
- `index_*.md` - 指数相关接口
- `macro_*.md` - 宏观相关接口
- `amac_*.md` - 基金业协会相关接口

使用 `grep` 命令搜索关键词可快速定位所需接口。
