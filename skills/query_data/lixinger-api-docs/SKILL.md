---
name: lixinger-data-query
description: 从理杏仁开放平台获取金融数据，并作为当前默认的多数据源查询执行中枢。适用于已有 provider 文档、本地鉴权方式和单命令示例的轻量查询场景。
---

# 理杏仁数据查询 Skill

从 [理杏仁开放平台](https://www.lixinger.com/open/api) 获取金融数据，并复用同一目录承载 AkShare 与未来 provider 的查询文档、单命令示例和薄脚本。

## 核心定位

该 skill 当前是默认的 **execution hub**，负责：
- 执行理杏仁查询
- 执行或承载 AkShare 查询示例
- 挂载未来 provider 的文档和最小调用入口

该 skill 不负责：
- 不做跨 provider 标准化
- 不维护完整 provider -> canonical 映射
- 不替代 `cn-data-source` 的发现 / 路由 / 溯源职责

## 核心功能
- 查询基本面数据：PE、PB、市值等财务指标
- 查询指数数据：成分股、行业权重、指数点位
- 市场覆盖：A股、港股、美股
- 数据格式：JSON、CSV、文本
- **新增**：AkShare 数据源（1000+ 接口，覆盖股票、债券、基金、期货、宏观等）
- **扩展**：未来 provider 只需补文档、鉴权说明和一个查询命令或薄脚本

## 最佳实践（重要）

### 查询入口选择

**优先使用已有 provider 文档和单命令示例**：
- 理杏仁场景先看 `API_KEYWORD_INDEX.md` 和 `docs/`
- AkShare 场景再看 `akshare_data/`
- 未来 provider 按 `{provider}_data/` 或等价目录挂载

### 轻量 Provider Pack 约定

每个 provider 最低只要求：
- 本地可读文档
- 本地鉴权方式说明
- 一个最小可运行查询命令或薄脚本

### 查询工作流

1. **先确定当前任务需要的最小字段**
2. **优先查看对应 provider 文档**
3. **执行最小查询命令**
4. **只返回当前任务真正需要的字段**
5. **如需标准化，留给任务层按本次运行临时提取**

### 参数优化建议

为了返回最有用的信息，**强烈建议**使用以下参数：

1. **`--columns`**：只返回需要的字段，减少无用数据
   - 示例：`--columns "stockCode,name,pe_ttm,pb"`
   - 好处：节省 token，数据更清晰

2. **`--row-filter`**：过滤符合条件的数据
   - 示例：`--row-filter '{"pe_ttm": {">": 10, "<": 20}}'`
   - 好处：只返回有价值的数据

3. **`--flatten`**：展开嵌套数组
   - 示例：`--flatten "constituents"`
   - 好处：处理指数成分股等嵌套数据

4. **`--limit`**：控制返回数量
   - 示例：`--limit 50`
   - 好处：避免数据过多

**推荐工作流**：
1. 查看 API 文档（`docs/`）了解可用字段
2. 使用 `--columns` 只返回需要的字段
3. 使用 `--row-filter` 过滤数据
4. 使用 `--limit` 控制数量

## 使用方法

### 独立运行（无需虚拟环境）

`query_tool.py` 已经是完全独立的工具，包含所有依赖：
- ✅ 无需安装虚拟环境
- ✅ 无需 pip install
- ✅ 直接运行即可

只需确保：
1. Python 3.x 已安装
2. 有 `token.cfg` 文件（在项目根目录或 scripts 目录）
3. 如需使用 AkShare，需安装：`pip install akshare`

### 调用指南（给大模型）

#### 理杏仁 API 查询（优先使用）

**步骤 1：选择 API**
- 从下方"理杏仁 API 接口列表"选择合适的 API
- 或使用 `grep -r "关键字" docs/` 搜索（在 lixinger-api-docs 目录下执行）

**步骤 2：查看 API 文档**
- 打开 `docs/` 中对应的 `.md` 文件
- 查看"参数"表格，了解必需参数和可选参数
- 查看"API试用示例"了解参数格式

**步骤 3：构造命令**
- 使用 `--suffix` 指定 API 路径
- 使用 `--params` 传递 API 参数（JSON 格式）
- **重要**：使用 `--columns` 只返回需要的字段
- **重要**：使用 `--row-filter` 过滤数据（如果需要）
- **重要**：使用 `--flatten` 展开嵌套数组（如果需要）

**步骤 4：执行查询**
- 默认输出 CSV 格式（最节省 token）
- 使用 `--limit` 控制返回数量

#### AkShare 接口查询（备选方案）

**当理杏仁 API 无法满足需求时，使用 AkShare**：

**步骤 1：搜索 AkShare 接口**
```bash
# 搜索关键字，找到合适的接口
grep -r "可转债" api_new/akshare_data/
grep -r "龙虎榜" api_new/akshare_data/
```

**步骤 2：查看接口文档**
- 打开 `api_new/akshare_data/` 中对应的 `.md` 文件
- 查看"输入参数"表格，了解参数要求
- 查看"接口示例"了解调用方式

**步骤 3：使用 Python 调用**
```python
import akshare as ak

# 示例：查询可转债数据
bond_cb_jsl_df = ak.bond_cb_jsl(cookie="")
print(bond_cb_jsl_df)

# 示例：查询 A股历史数据
stock_zh_a_hist_df = ak.stock_zh_a_hist(
    symbol="000001", 
    period="daily", 
    start_date="20240101", 
    end_date='20240131', 
    adjust=""
)
print(stock_zh_a_hist_df)
```

**AkShare 接口特点**：
- 1000+ 接口，覆盖股票、债券、基金、期货、宏观等
- 数据来源广泛（东方财富、新浪、集思录等）
- 部分接口需要 cookie 或其他认证
- 返回 pandas DataFrame 格式

**AkShare 常用接口分类**：
- 股票：`stock_zh_a_hist`（历史行情）、`stock_zh_a_spot_em`（实时行情）
- 债券：`bond_cb_jsl`（可转债）、`bond_zh_hs_cov_spot`（可转债实时）
- 基金：`fund_etf_spot_em`（ETF实时）、`fund_open_fund_daily_em`（开放式基金）
- 期货：`futures_zh_spot`（期货实时）、`futures_zh_daily_sina`（期货日线）
- 宏观：`macro_china_gdp`（GDP）、`macro_china_cpi`（CPI）
- 指数：`index_zh_a_hist`（指数历史）、`stock_board_concept_name_em`（概念板块）

### 1. 查找 API

**理杏仁 API（优先）**：
```bash
# 搜索理杏仁 API
grep -r "基本面" docs/
```

**AkShare 接口（备选）**：
```bash
# 搜索 AkShare 接口
grep -r "可转债" api_new/akshare_data/
grep -r "龙虎榜" api_new/akshare_data/
```

### 2. 查看参数

**理杏仁 API**：
阅读 `docs/` 中对应的 `.md` 文件确认参数要求，例如 `cn_company.md`。

**AkShare 接口**：
阅读 `api_new/akshare_data/` 中对应的 `.md` 文件确认参数要求，例如 `bond_cb_jsl.md`。

### 3. 执行查询

#### 理杏仁 API 查询（推荐）

**基础示例**：
```bash
# 查询银行股（推荐：使用 --columns 只返回需要的字段）
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"fsTableType": "bank"}' \
  --columns "stockCode,name"

# 过滤以 600 开头的股票（推荐：使用 --flatten 和 --row-filter）
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date": "2024-12-10", "stockCodes": ["000016"]}' \
  --flatten "constituents" \
  --row-filter '{"stockCode": {"startswith": "600"}}' \
  --columns "stockCode"
```

**查找 API 参数**：
- 参考 `docs/` 目录中的 API 文档
- 每个 API 文档包含完整的参数说明和示例
- 示例：查看 `cn_company.md` 了解 `cn/company` 的参数

#### AkShare 接口查询（备选）

**使用 Python 直接调用**：
```python
import akshare as ak

# 示例 1：查询可转债数据
bond_cb_jsl_df = ak.bond_cb_jsl(cookie="")
print(bond_cb_jsl_df)

# 示例 2：查询 A股历史数据
stock_zh_a_hist_df = ak.stock_zh_a_hist(
    symbol="000001", 
    period="daily", 
    start_date="20240101", 
    end_date='20240131', 
    adjust=""
)
print(stock_zh_a_hist_df)

# 示例 3：查询 ETF 实时行情
fund_etf_spot_em_df = ak.fund_etf_spot_em()
print(fund_etf_spot_em_df)
```

**查找 AkShare 参数**：
- 参考 `api_new/akshare_data/` 目录中的接口文档
- 每个接口文档包含完整的参数说明和示例
- 示例：查看 `bond_cb_jsl.md` 了解可转债接口的参数

更多示例请查看 [EXAMPLES.md](./EXAMPLES.md)

### 参数说明

**必需参数**：
- `--suffix`: API 后缀（从下方 API 列表选择，或查看 `docs/`）
- `--params`: JSON 格式参数（参考对应 API 文档中的参数表格）

**增强参数（强烈推荐使用）**：
- `--columns`: 指定返回字段，逗号分隔（如 `stockCode,name,pe_ttm`）
  - **用途**：只返回需要的字段，减少无用数据
  - **示例**：`--columns "stockCode,name,ipoDate"`
  
- `--row-filter`: JSON 格式行过滤条件
  - **用途**：过滤符合条件的数据，提高数据质量
  - **示例**：`--row-filter '{"pe_ttm": {">": 10, "<": 20}}'`
  
- `--flatten`: 展开嵌套数组字段
  - **用途**：处理指数成分股等嵌套结构
  - **示例**：`--flatten "constituents"`

**可选参数**：
- `--format`: 输出格式 `csv`（默认）、`json`、`text`
- `--limit`: 限制返回行数（默认 100）

**参数构造提示**：
1. 查看 `docs/` 中对应的 API 文档
2. 根据文档中的"参数"表格构造 JSON
3. 注意：外层单引号，内层双引号
4. 示例：`'{"date": "2024-12-10", "stockCodes": ["600519"]}'`

### 高级功能

#### 字段过滤（--columns）
只返回指定的字段，减少数据量：
```bash
--columns "stockCode,name,pe_ttm"
```

#### 行过滤（--row-filter）
支持的操作符：`==`、`!=`、`>`、`>=`、`<`、`<=`、`in`、`not_in`、`startswith`、`endswith`、`contains`

示例：
```bash
# PE 在 10-20 之间
--row-filter '{"pe_ttm": {">": 10, "<": 20}}'

# 字符串开头匹配
--row-filter '{"stockCode": {"startswith": "600"}}'
```

#### 嵌套数组展开（--flatten）
某些 API 返回嵌套数组（如 `cn/index/constituents`），使用 `--flatten` 展开：
```bash
--flatten "constituents"
```

## API 接口列表

### 理杏仁 API（162 个接口，优先使用）

#### A股公司

| API 后缀 | 说明 |
|---------|------|
| `cn/company` |股票详细信息 |
| `cn/company/allotment` |配股信息 |
| `cn/company/announcement` |公告信息 |
| `cn/company/block-deal` |大宗交易数据 |
| `cn/company/candlestick` |K线数据 |
| `cn/company/customers` |客户信息 |
| `cn/company/dividend` |分红信息 |
| `cn/company/equity-change` |股本变动数据 |
| `cn/company/fs/non_financial` |财务数据（营业收入、ROE等） |
| `cn/company/fund-collection-shareholders` |基金公司持股信息 |
| `cn/company/fund-shareholders` |公募基金持股信息 |
| `cn/company/fundamental/non_financial` |基本面数据（PE、PB等） |
| `cn/company/hot/tr_dri` |分红再投入收益率数据 |
| `cn/company/indices` |股票所属指数信息 |
| `cn/company/industries` |股票所属行业信息 |
| `cn/company/inquiry` |问询函信息 |
| `cn/company/major-shareholders-shares-change` |大股东增减持数据 |
| `cn/company/majority-shareholders` |前十大股东持股信息 |
| `cn/company/margin-trading-and-securities-lending` |融资融券数据 |
| `cn/company/measures` |监管措施信息 |
| `cn/company/mutual-market` |互联互通数据 |
| `cn/company/nolimit-shareholders` |前十大流通股东持股信息 |
| `cn/company/operating-data` |经营数据信息 |
| `cn/company/operation-revenue-constitution` |营收构成数据 |
| `cn/company/pledge` |股权质押数据 |
| `cn/company/profile` |公司概况数据 |
| `cn/company/senior-executive-shares-change` |高管增减持数据 |
| `cn/company/shareholders-num` |股东人数数据 |
| `cn/company/suppliers` |供应商信息 |
| `cn/company/trading-abnormal` |龙虎榜信息 |

### A股指数

| API 后缀 | 说明 |
|---------|------|
| `cn/index` |指数详细信息 |
| `cn/index/candlestick` |K线数据 |
| `cn/index/constituent-weightings` |指数样本权重信息 |
| `cn/index/constituents` |样本信息 |
| `cn/index/drawdown` |指数回撤数据 |
| `cn/index/fs/hybrid` |财务数据（营业收入、ROE等） |
| `cn/index/fundamental` |基本面数据（PE、PB等） |
| `cn/index/hot/mm_ha` |互联互通数据 |
| `cn/index/margin-trading-and-securities-lending` |融资融券数据 |
| `cn/index/mutual-market` |互联互通数据 |
| `cn/index/tracking-fund` |指数跟踪基金数据 |

### A股行业

| API 后缀 | 说明 |
|---------|------|
| `cn/industry` |行业详细信息 |
| `cn/industry/constituents/sw_2021` |样本信息 |
| `cn/industry/fs/sw_2021/hybrid` |财务数据（营业收入、ROE等） |
| `cn/industry/fundamental/sw_2021` |基本面数据（PE、PB等） |
| `cn/industry/hot/mm_ha/sw_2021` |互联互通数据 |
| `cn/industry/margin-trading-and-securities-lending/sw_2021` |融资融券数据 |
| `cn/industry/mutual-market/sw_2021` |互联互通数据 |

### A股基金

| API 后缀 | 说明 |
|---------|------|
| `cn/fund` |基金详细信息 |
| `cn/fund-company` |基金公司详细信息 |
| `cn/fund-company/asset-scale` |资产规模详细信息 |
| `cn/fund-company/fund-list` |基金列表详细信息 |
| `cn/fund-company/fund-manager-list` |基金经理列表详情 |
| `cn/fund-company/hot/fc_as` |基金公司资产规模数据 |
| `cn/fund-company/shareholdings` |持仓详细信息 |
| `cn/fund-manager` |基金经理详细信息 |
| `cn/fund-manager/hot/fmp` |基金经理收益率数据 |
| `cn/fund-manager/management-funds` |管理的基金详细信息 |
| `cn/fund-manager/profit-ratio` |利润率信息 |
| `cn/fund-manager/shareholdings` |基金经理持仓信息 |
| `cn/fund/announcement` |公告信息 |
| `cn/fund/asset-combination` |资产组合信息 |
| `cn/fund/asset-industry-combination` |按行业分类的股票投资组合数据 |
| `cn/fund/candlestick` |K线数据 |
| `cn/fund/dividend` |分红信息 |
| `cn/fund/drawdown` |基金回撤数据 |
| `cn/fund/exchange-traded-close-price` | 场内基金收盘价数据 |
| `cn/fund/fees` |费用信息 |
| `cn/fund/hot/f_nlacan` |最新收盘价溢价率信息数据 |
| `cn/fund/manager` |基金历史基金经理任职信息 |
| `cn/fund/net-value` |净值数据 |
| `cn/fund/net-value-of-dividend-reinvestment` |分红再投入净值数据 |
| `cn/fund/profile` |基金概况数据 |
| `cn/fund/shareholders-structure` |基金持有人结构数据 |
| `cn/fund/shareholdings` |基金持仓数据 |
| `cn/fund/shares` |基金份额及规模数据 |
| `cn/fund/split` |拆分数据 |
| `cn/fund/total-net-value` |基金累计净值数据 |
| `cn/fund/turnover-rate` |换手率信息 |

### 港股公司

| API 后缀 | 说明 |
|---------|------|
| `hk/company` |股票详细信息 |
| `hk/company/allotment` |配股信息 |
| `hk/company/announcement` |公告信息 |
| `hk/company/candlestick` |K线数据 |
| `hk/company/dividend` |分红信息 |
| `hk/company/employee` |员工数据 |
| `hk/company/equity-change` |股本变动数据 |
| `hk/company/fs/non_financial` |财务数据（营业收入、ROE等） |
| `hk/company/fund-collection-shareholders` |内资基金公司持股信息 |
| `hk/company/fund-shareholders` |内资基金持股信息 |
| `hk/company/fundamental/non_financial` |基本面数据（PE、PB等） |
| `hk/company/hot/tr_dri` |分红再投入收益率数据 |
| `hk/company/indices` |股票所属指数信息 |
| `hk/company/industries` |股票所属行业信息 |
| `hk/company/latest-shareholders` |最新股东数据 |
| `hk/company/mutual-market` |互联互通数据 |
| `hk/company/operation-revenue-constitution` |营收构成数据 |
| `hk/company/profile` |公司概况数据 |
| `hk/company/repurchase` |回购数据 |
| `hk/company/shareholders-equity-change` |股东权益变动数据 |
| `hk/company/short-selling` |做空数据 |
| `hk/company/split` |拆分数据 |

### 港股指数

| API 后缀 | 说明 |
|---------|------|
| `hk/index` |指数详细信息 |
| `hk/index/candlestick` |K线数据 |
| `hk/index/constituents` |样本信息 |
| `hk/index/drawdown` |指数回撤数据 |
| `hk/index/fs/hybrid` |财务数据（营业收入、ROE等） |
| `hk/index/fundamental` |基本面数据（PE、PB等） |
| `hk/index/hot/mm_ah` |互联互通数据 |
| `hk/index/mutual-market` |互联互通数据 |
| `hk/index/tracking-fund` |指数跟踪基金数据 |

### 港股行业

| API 后缀 | 说明 |
|---------|------|
| `hk/industry` |行业详细信息 |
| `hk/industry/constituents/hsi` |样本信息 |
| `hk/industry/fs/hsi/hybrid` |财务数据（营业收入、ROE等） |
| `hk/industry/fundamental/hsi` |基本面数据（PE、PB等） |
| `hk/industry/hot/mm_ah/hsi` |互联互通数据 |
| `hk/industry/mutual-market/hsi` |互联互通数据 |

### 美股指数

| API 后缀 | 说明 |
|---------|------|
| `us/index` |指数详细信息 |
| `us/index/candlestick` |K线数据 |
| `us/index/constituents` |样本信息 |
| `us/index/drawdown` |指数回撤数据 |
| `us/index/fs/non_financial` |财务数据（营业收入、ROE等） |
| `us/index/fundamental` |基本面数据（PE、PB等） |
| `us/index/hot/cp` |收盘点位数据 |
| `us/index/hot/ifet_sni` |场内基金认购净流入数据 |
| `us/index/tracking-fund` |指数跟踪基金数据 |

### 宏观数据

| API 后缀 | 说明 |
|---------|------|
| `macro/bop` | 国际收支平衡数据 |
| `macro/central-bank-balance-sheet` | 央行资产负债表数据 |
| `macro/credit-securities-account` | 信用证券账户数据 |
| `macro/crude-oil` | 原油数据 |
| `macro/currency-exchange-rate` | 汇率数据 |
| `macro/domestic-debt-securities` | 国内债券数据 |
| `macro/domestic-trade` | 社会消费品零售数据 |
| `macro/energy` | 能源数据 |
| `macro/foreign-assets` | 国外资产数据 |
| `macro/foreign-trade` | 对外贸易数据 |
| `macro/gdp` | GDP数据 |
| `macro/gold-price` | 黄金数据 |
| `macro/industrialization` | 工业数据 |
| `macro/interest-rates` | 利率数据 |
| `macro/investment-in-fixed-assets` | 固定资产投资数据 |
| `macro/investor` | 投资者数据 |
| `macro/leverage-ratio` | 杠杆率数据 |
| `macro/money-supply` | 货币供应数据 |
| `macro/national-debt` | 国债数据 |
| `macro/natural-gas` | 天然气数据 |
| `macro/non-ferrous-metals` | 有色金属数据 |
| `macro/official-reserve-assets` | 官方储备资产数据 |
| `macro/petroleum` | 石油数据 |
| `macro/platinum-price` | 铂金数据 |
| `macro/population` | 人口数据 |
| `macro/price-index` | 价格指数数据 |
| `macro/real-estate` | 房地产数据 |
| `macro/required-reserves` | 存款准备金率 |
| `macro/rmb-deposits` | 人民币存款数据 |
| `macro/rmb-loans` | 人民币贷款数据 |
| `macro/rmbidx` | 人民币指数数据 |
| `macro/silver-price` | 白银数据 |
| `macro/social-financing` | 社会融资数据 |
| `macro/stamp-duty` | 印花税数据 |
| `macro/traffic-transportation` | 交通运输数据 |
| `macro/usdx` | 美元指数数据 |

### AkShare 接口（1000+ 接口，备选方案）

**使用说明**：
- AkShare 提供 1000+ 接口，覆盖更广泛的数据源
- 当理杏仁 API 无法满足需求时使用
- 使用 `grep -r "关键字" akshare_data/` 搜索（在 lixinger-api-docs 目录下执行）
- 查看 `akshare_data/` 中的 `.md` 文件了解参数
- 使用 Python 直接调用：`import akshare as ak`

**接口分类**：

#### 股票数据（约 300+ 接口）
- 实时行情：`stock_zh_a_spot_em`、`stock_hk_spot_em`、`stock_us_spot_em`
- 历史数据：`stock_zh_a_hist`、`stock_hk_hist`、`stock_us_hist`
- 财务数据：`stock_financial_analysis_indicator_em`、`stock_balance_sheet_by_report_em`
- 龙虎榜：`stock_lhb_detail_em`、`stock_lhb_stock_statistic_em`
- 大宗交易：`stock_changes_em`
- 融资融券：`stock_margin_detail_sse`、`stock_margin_detail_szse`
- 股东数据：`stock_gdfx_holding_detail_em`、`stock_hold_management_detail_em`
- 分红送转：`stock_fhps_em`、`stock_dividend_cninfo`
- 公告数据：`stock_notice_report`
- 板块数据：`stock_board_concept_name_em`、`stock_board_industry_name_em`

#### 债券数据（约 50+ 接口）
- 可转债：`bond_cb_jsl`、`bond_zh_hs_cov_spot`、`bond_cb_redeem_jsl`
- 国债：`bond_treasure_issue_cninfo`、`bond_china_yield`
- 企业债：`bond_corporate_issue_cninfo`
- 债券行情：`bond_zh_hs_daily`、`bond_spot_deal`

#### 基金数据（约 100+ 接口）
- ETF：`fund_etf_spot_em`、`fund_etf_hist_em`、`fund_etf_fund_info_em`
- 开放式基金：`fund_open_fund_daily_em`、`fund_open_fund_info_em`
- 基金经理：`fund_manager_em`
- 基金持仓：`fund_portfolio_hold_em`、`fund_portfolio_industry_allocation_em`
- 基金评级：`fund_rating_all`

#### 期货数据（约 100+ 接口）
- 期货行情：`futures_zh_spot`、`futures_zh_daily_sina`
- 期货持仓：`futures_hold_pos_sina`
- 期货库存：`futures_inventory_em`
- 期货合约：`futures_contract_detail_em`
- 外盘期货：`futures_foreign_hist`、`futures_global_spot_em`

#### 指数数据（约 100+ 接口）
- A股指数：`index_zh_a_hist`、`stock_zh_index_spot_em`
- 港股指数：`stock_hk_index_spot_em`、`stock_hk_index_daily_em`
- 美股指数：`index_us_stock_sina`
- 行业指数：`index_analysis_daily_sw`、`stock_board_industry_spot_em`
- 概念指数：`stock_board_concept_spot_em`

#### 宏观数据（约 200+ 接口）
- 中国宏观：`macro_china_gdp`、`macro_china_cpi`、`macro_china_pmi`
- 美国宏观：`macro_usa_gdp_monthly`、`macro_usa_cpi_monthly`
- 欧洲宏观：`macro_euro_gdp_yoy`、`macro_euro_cpi_yoy`
- 利率数据：`macro_china_lpr`、`macro_china_shibor_all`
- 货币供应：`macro_china_money_supply`
- 外汇储备：`macro_china_fx_reserves_yearly`

#### 其他数据（约 150+ 接口）
- REITs：`reits_realtime_em`、`reits_hist_em`
- 新股数据：`stock_ipo_info`、`stock_new_a_spot_em`
- ESG数据：`stock_esg_rate_sina`
- 研报数据：`stock_research_report_em`
- 经济日历：`macro_cons_gold`

**查找 AkShare 接口**：
```bash
# 搜索关键字
grep -r "可转债" api_new/akshare_data/
grep -r "龙虎榜" api_new/akshare_data/
grep -r "ETF" api_new/akshare_data/
grep -r "期货" api_new/akshare_data/
```

**AkShare 接口文档位置**：
- 所有接口文档：`plugins/query_data/lixinger-api-docs/akshare_data/*.md`
- 每个文档包含：接口名称、参数说明、返回字段、调用示例
- 示例：`bond_cb_jsl.md`、`stock_zh_a_hist.md`、`fund_etf_spot_em.md`

## 注意事项

### 理杏仁 API
- Token 从项目根目录 `token.cfg` 文件读取
- 成功请求返回 `code` 为 `1`
- 所有 API 需要有效 token，有每日访问次数限制
- 更多示例和工作流请查看 [EXAMPLES.md](./EXAMPLES.md)

### AkShare 接口
- 需要安装：`pip install akshare`
- 部分接口需要 cookie 或其他认证（如集思录可转债数据）
- 返回 pandas DataFrame 格式
- 数据来源广泛，更新频率各异
- 使用 Python 直接调用，不通过 `query_tool.py`


---

## 新数据源接入规范

本章节定义未来引入新数据源时的标准接入流程。所有数据源统一收口在 `.claude/plugins/query_data/lixinger-api-docs/`。

### 目录约定

```
.claude/plugins/query_data/lixinger-api-docs/
├── api_new/
│   ├── api-docs/              # 理杏仁 API 文档（每个 API 一个 .md 文件）
│   ├── akshare_data/          # AkShare 接口文档（每个接口一个 .md 文件）
│   ├── {datasource}_data/     # 新数据源文档目录（命名规范：{datasource}_data/）
│   └── API_KEYWORD_INDEX.md   # 统一关键词索引（覆盖所有数据源）
```

新数据源目录命名规范：`{datasource}_data/`，例如 `wind_data/`、`tushare_data/`。

### 文档格式要求

每个接口一个 `.md` 文件，格式与 `akshare_data/` 保持一致，包含：

```markdown
接口: {interface_name}

描述: {接口功能描述}

输入参数

| 名称 | 类型 | 描述 |
|------|------|------|
| ...  | ...  | ...  |

输出参数

| 名称 | 类型 | 描述 |
|------|------|------|
| ...  | ...  | ...  |

接口示例

```python
# 调用示例代码
```
```

### 新增数据源的标准步骤

1. **创建文档目录**：在 `api_new/` 下创建 `{datasource}_data/` 目录，每个接口一个 `.md` 文件

2. **更新 API_KEYWORD_INDEX.md**：在索引文件中为新数据源添加独立章节，格式与现有章节一致，支持中文关键词 grep 搜索

3. **更新本文件（SKILL.md）**：在"数据源选择优先级"和"API 接口列表"章节中添加新数据源说明，包括适用场景、查找方式、调用示例

4. **更新 analysis-market/SKILL.md**：在三级优先级规则中说明新数据源的位置

### 优先级插入原则

当前优先级：理杏仁 API > AkShare > 其他

新数据源插入位置由以下原则决定：
- 数据质量高、覆盖面广 → 插入理杏仁 API 之后（成为第二优先级）
- 补充性数据源 → 插入 AkShare 之后
- 优先级顺序在 `analysis-market/SKILL.md` 的"使用优先级"章节中维护
