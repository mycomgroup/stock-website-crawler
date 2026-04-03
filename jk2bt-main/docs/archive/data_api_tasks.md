# 聚宽数据 API 实现子任务提示词

基于 GitHub 文档：https://github.com/mycomgroup/stock-website-crawler/tree/main/skills/joinquant_nookbook/joinquant_doc/doc

本文档给出 10 个数据 API 实现子任务提示词，每个任务聚焦一个重要的数据类别。用户将一个一个在当前代码库中实现。

通用要求：
- 你负责实现具体的数据 API，要确保数据能正确获取、格式统一、缓存有效
- 参考对应聚宽文档实现，保持 API 签名和返回格式兼容
- 实现后需编写测试验证功能可用
- 注意与现有代码风格保持一致，优先复用现有基础设施（如 DuckDB 缓存、数据标准化层）
- 每个任务结束时输出：修改文件列表、实现功能、测试验证方法、已知限制

---

## 任务 1: 上市公司基本信息与状态变动 API

目标：
实现上市公司基本信息查询 API，包括公司概况、状态变动、上市信息等。

需实现的 API：
- `get_company_info(code)` - 获取公司基本信息
- `finance.STK_COMPANY_BASIC_INFO` - 公司基本信息表查询
- `finance.STK_STATUS_CHANGE` - 公司状态变动查询（停牌、复牌、退市等）
- `get_security_status(code, date)` - 获取指定日期的证券状态

参考文档：
- `doc_JQDatadoc_10016_overview_上市公司基本信息.md`
- `doc_JQDatadoc_10023_overview_上市公司状态变动.md`
- `doc_JQDatadoc_10025_overview_上市信息.md`

数据字段（至少包含）：
- 公司代码、公司名称、成立日期、上市日期
- 主营业务、所属行业、注册地址
- 公司状态（正常、停牌、退市等）
- 状态变动日期、变动类型

实现要求：
- 数据源优先使用 AkShare，必要时补充其他数据源
- 建立本地 DuckDB 缓存，避免重复下载
- 实现 finance.run_query 兼容的查询接口
- 公司状态查询需支持历史日期回溯

测试建议：
- 查询 3-5 家上市公司基本信息，验证字段完整性
- 查询某公司停牌/复牌历史记录
- 验证 finance.run_query 查询格式兼容性

交付范围：
- 在 `jqdata_akshare_backtrader_utility/finance_data/` 下新增模块
- 在 `backtrader_base_strategy.py` 中集成 API
- 编写对应测试文件

---

## 任务 2: 上市公司股东信息 API

目标：
实现上市公司股东信息查询 API，包括十大股东、十大流通股东、股东户数等。

需实现的 API：
- `finance.STK_SHAREHOLDER_TOP10` - 前10大股东查询
- `finance.STK_SHAREHOLDER_FLOAT_TOP10` - 前10大流通股东查询
- `finance.STK_SHAREHOLDER_NUM` - 股东户数查询
- `get_top10_shareholders(code, date)` - 获取十大股东快照
- `get_shareholder_count(code)` - 获取股东户数

参考文档：
- `doc_JQDatadoc_10011_overview_上市公司前10大股东.md`
- `doc_JQDatadoc_10012_overview_十大流通股东.md`
- `doc_JQDatadoc_10015_overview_股东户数.md`

数据字段（至少包含）：
- 股东名称、股东代码
- 持股数量、持股比例
- 股东类型（个人、机构、国有等）
- 变动情况（增持、减持、不变）
- 报告期、公告日期

实现要求：
- 支持按日期查询历史股东结构
- 股东户数支持时间序列查询
- 十大股东返回 DataFrame 格式，便于分析
- 建立缓存机制，按报告期缓存

测试建议：
- 查询某公司最近 4 个季度十大股东变化
- 查询股东户数历史序列
- 验证十大流通股东字段完整性

交付范围：
- 在 `finance_data/shareholder.py` 中实现
- 集成到 finance.run_query 接口
- 编写测试验证

---

## 任务 3: 公司行为与分红送股 API

目标：
实现公司行为查询 API，包括分红送股、配股、拆股、除权除息等。

需实现的 API：
- `finance.STK_XR_XD` - 除权除息数据查询
- `finance.STK_DIVIDEND_RIGHT` - 分红送股数据
- `get_dividend_info(code)` - 获取分红送股信息
- `get_rights_issue(code)` - 获取配股信息
- `get_adjust_factor(code, start_date, end_date)` - 获取复权因子

参考文档：
- `doc_JQDatadoc_10010_overview_公司行为.md`
- `doc_JQDatadoc_10022_overview_上市公司分红送股（除权除息）数据.md`

数据字段（至少包含）：
- 公告日期、除权除息日期
- 分红金额、送股比例、配股比例
- 配股价、配股比例
- 除权价、除息价
- 复权因子（前复权、后复权）

实现要求：
- 必须支持历史时间序列查询
- 复权因子计算需考虑累积影响
- 除权除息日查询需精确匹配
- 提供快速查询接口：`get_next_dividend(code)`

测试建议：
- 查询某股票 5 年内的所有分红送股记录
- 计算某股票的复权因子序列
- 验证除权除息日查询准确性

交付范围：
- 在 `finance_data/dividend.py` 中实现
- 提供复权因子计算辅助函数
- 编写测试验证

---

## 任务 4: 股东股份变动与增减持 API

目标：
实现股东股份质押、冻结、增减持等变动数据查询 API。

需实现的 API：
- `finance.STK_SHARE_PLEDGE` - 股东股份质押查询
- `finance.STK_SHARE_FREEZE` - 股东股份冻结查询
- `finance.STK_TOPHOLDER_CHANGE` - 大股东增减持查询
- `finance.STK_CAPITAL_CHANGE` - 股本变动查询
- `get_pledge_info(code)` - 获取质押信息
- `get_major_holder_trade(code, start_date, end_date)` - 获取大股东交易

参考文档：
- `doc_JQDatadoc_10013_overview_股东股份质押.md`
- `doc_JQDatadoc_10014_overview_股东股份冻结.md`
- `doc_JQDatadoc_10017_overview_大股东增减持.md`
- `doc_JQDatadoc_10018_overview_上市公司股本变动.md`

数据字段（至少包含）：
- 股东名称、股东代码
- 质押股数、质押比例、质押开始/结束日期
- 冻结股数、冻结原因、冻结日期
- 增减持股数、增减持金额、变动日期
- 股本变动类型、变动数量、变动日期

实现要求：
- 质押数据需支持按股东查询
- 大股东增减持需支持时间范围过滤
- 股本变动需区分总股本、流通股本
- 建立缓存，按季度更新

测试建议：
- 查询某公司质押比例变化趋势
- 查询某公司大股东近 1 年增减持记录
- 查询某公司股本扩张历史

交付范围：
- 在 `finance_data/share_change.py` 中实现
- 集成到 finance 查询接口
- 编写测试验证

---

## 任务 5: 限售解禁数据 API

目标：
实现限售股解禁数据查询 API，为策略提供解禁压力判断依据。

需实现的 API：
- `finance.STK_LOCK_UNLOCK` - 限售解禁数据查询
- `finance.STK_LOCK_SHARE` - 上市公告日期和预计解禁日期
- `finance.STK_UNLOCK_DATE` - 受限股份实际解禁日期
- `get_unlock_schedule(code, start_date, end_date)` - 获取解禁时间表
- `get_unlock_pressure(code)` - 计算解禁压力指标

参考文档：
- `doc_JQDatadoc_10019_overview_上市公司上市公告日期和预计解禁日期.md`
- `doc_JQDatadoc_10020_overview_上市公司受限股份实际解禁的日期.md`
- `doc_JQDatadoc_10021_overview_限售解禁数据.md`

数据字段（至少包含）：
- 解禁日期、解禁股数
- 解禁股占总股本比例、解禁股占流通股比例
- 解禁股东类型、股东名称
- 原始公告日期、预计解禁日期
- 实际解禁日期、解禁状态

实现要求：
- 支持按日期范围查询解禁计划
- 提供解禁压力量化指标（如：未来 30 天解禁量占比）
- 支持按股票代码查询解禁历史
- 数据需及时更新，建议每日缓存

测试建议：
- 查询某股票未来 3 个月解禁时间表
- 查询某股票历史解禁记录与股价表现对照
- 验证解禁压力指标计算合理性

交付范围：
- 在 `finance_data/unlock.py` 中实现
- 提供解禁压力计算辅助函数
- 编写测试验证

---

## 任务 6: 可转债数据 API

目标：
实现可转债行情、基本信息、转股数据查询 API。

需实现的 API：
- `get_conversion_bond_list()` - 获取可转债列表
- `get_conversion_bond_quote(code)` - 获取可转债行情
- `finance.STK_CONVERSION_BOND_BASIC` - 可转债基本信息
- `finance.STK_CONVERSION_BOND_PRICE` - 可转债价格数据
- `get_conversion_info(code)` - 获取转股信息
- `get_conversion_value(code)` - 计算转股价值

参考文档：
- `doc_JQDatadoc_10293_overview_可转债.md`

数据字段（至少包含）：
- 可转债代码、可转债名称
- 发行规模、票面利率、到期日期
- 转股价、转股比例、转股起始日
- 正股代码、正股价格
- 转股价值、溢价率
- 债券价格、成交量、成交额

实现要求：
- 可转债列表需包含所有在市可转债
- 转股价值需实时计算：`转股价值 = 100 / 转股价 * 正股价`
- 提供溢价率计算：`溢价率 = (债券价格 / 转股价值 - 1) * 100%`
- 支持历史转股价调整记录查询

测试建议：
- 查询所有可转债基本信息
- 计算某可转债转股价值和溢价率
- 查询某可转债转股价调整历史

交付范围：
- 在 `market_data/conversion_bond.py` 中实现
- 提供转股价值计算辅助函数
- 编写测试验证

---

## 任务 7: 期权数据 API

目标：
实现期权合约列表、行情、基础数据查询 API。

需实现的 API：
- `get_option_list(underlying_code)` - 获取期权合约列表
- `get_option_quote(code)` - 获取期权行情
- `finance.STK_OPTION_BASIC` - 期权基本信息
- `finance.STK_OPTION_DAILY` - 期权日行情数据
- `get_option_greeks(code)` - 获取希腊字母
- `get_option_chain(underlying_code, date)` - 获取期权链

参考文档：
- `doc_JQDatadoc_10030_overview_期权列表.md`
- `doc_JQDatadoc_10251_overview_期权交易标的列表.md`
- `doc_JQDatadoc_10252_overview_获取期权交易列表.md`

数据字段（至少包含）：
- 期权代码、期权名称
- 标的代码、行权价、到期日期
- 期权类型（认购/认沽）
- 开盘价、最高价、最低价、收盘价
- 成交量、成交额、持仓量
- Delta、Gamma、Theta、Vega（希腊字母）
- 隐含波动率

实现要求：
- 期权列表需支持按标的筛选
- 期权链需按行权价排列，支持多到期日
- 希腊字母数据需提供计算或获取途径
- 支持历史行情查询

测试建议：
- 查询某标的（如 50ETF）的所有期权合约
- 查询某期权合约的历史行情
- 验证期权链结构完整性

交付范围：
- 在 `market_data/option.py` 中实现
- 提供期权链查询辅助函数
- 编写测试验证

---

## 任务 8: 指数成分股与权重 API

目标：
实现指数成分股及权重查询 API，支持历史成分变化查询。

需实现的 API：
- `finance.STK_INDEX_COMPONENTS` - 指数成分股查询
- `finance.STK_INDEX_WEIGHTS` - 指数成分权重查询
- `get_index_components(index_code, date)` - 获取指数成分股
- `get_index_weights(index_code, date)` - 获取指数成分权重
- `get_index_component_history(index_code, start_date, end_date)` - 获取成分变化历史

参考文档：
- `doc_JQDatadoc_10291_overview_指数成分股及权重.md`

数据字段（至少包含）：
- 指数代码、成分股代码
- 成分股名称、权重比例
- 入选日期、剔除日期
- 调整类型（定期调整、临时调整）

实现要求：
- 支持按日期查询历史成分股（回测必需）
- 权重数据需精确到小数点后 2 位
- 支持主流指数：沪深 300、中证 500、上证 50 等
- 成分变化历史需记录调整原因

测试建议：
- 查询沪深 300 当前成分股及权重
- 查询沪深 300 某历史日期成分股（如 2020-01-01）
- 查询某指数近 3 年成分调整记录

交付范围：
- 在 `market_data/index_components.py` 中实现
- 集成到现有 index 模块
- 编写测试验证

---

## 任务 9: 申万行业分类与成分股 API

目标：
实现申万行业分类查询 API，支持行业成分股查询和历史行业归属。

需实现的 API：
- `finance.STK_SW_INDUSTRY` - 申万行业分类查询
- `finance.STK_SW_INDUSTRY_STOCK` - 行业成分股查询
- `get_industry_category(code)` - 获取股票行业分类
- `get_industry_stocks(industry_code, level)` - 获取行业成分股
- `get_industry_history(code)` - 获取股票行业变更历史

参考文档：
- `doc_JQDatadoc_10282_overview_申万行业.md`
- `doc_JQDatadoc_10283_overview_行业概念及成分股.md`

数据字段（至少包含）：
- 行业代码、行业名称
- 行业层级（一级行业、二级行业、三级行业）
- 股票代码、股票名称
- 行业归属开始日期、结束日期
- 行业版本（如 2014 版、2021 版）

实现要求：
- 支持多层级行业分类查询（一级到三级）
- 行业成分股需支持按层级筛选
- 股票行业历史需记录行业调整时间点
- 兼容现有 `industry.py` 模块，避免重复实现

测试建议：
- 查询某股票的申万行业分类（所有层级）
- 查询某二级行业的所有成分股
- 查询某股票近 5 年行业归属变化

交付范围：
- 在 `market_data/industry_sw.py` 中实现
- 或扩展现有 `industry.py` 模块
- 编写测试验证

---

## 任务 10: 宏观数据 API

目标：
实现宏观经济数据查询 API，支持主要经济指标查询。

需实现的 API：
- `finance.MAC_ECONOMIC_DATA` - 宏观经济数据查询
- `get_macro_data(indicator_code)` - 获取宏观指标数据
- `get_macro_indicators()` - 获取可用宏观指标列表
- `get_macro_series(indicator_code, start_date, end_date)` - 获取时间序列

参考文档：
- `doc_JQDatadoc_10289_overview_宏观数据.md`

数据指标（至少支持）：
- GDP 及增长率
- CPI、PPI
- M1、M2
- 社会融资规模
- 工业增加值
- 固定资产投资
- 进出口总额
- 利率（LPR、MLF 等）
- 汇率（美元兑人民币）

实现要求：
- 宏观指标列表需提供指标代码、名称、单位、频率
- 数据需支持时间序列查询，返回 DataFrame
- 更新频率需与官方发布同步（月度/季度）
- 建立缓存机制，避免重复下载

测试建议：
- 查询 CPI 近 12 个月数据
- 查询 GDP 近 5 年季度数据
- 验证指标列表完整性

交付范围：
- 在 `finance_data/macro.py` 中实现
- 提供宏观指标字典
- 编写测试验证

---

## 实现建议

### 数据源优先级
1. AkShare（优先，免费）
2. Tushare（需积分，数据质量高）
3. 本地 DuckDB 缓存（已下载的数据）
4. 其他开源数据源

### 缓存策略
- 静态数据（公司信息）：按季度缓存
- 动态数据（股东、解禁）：按周缓存
- 实时数据（行情）：按日缓存
- 宏观数据：按发布周期缓存

### 目录结构建议
```
jqdata_akshare_backtrader_utility/
├── finance_data/
│   ├── company_info.py      # 任务 1
│   ├── shareholder.py       # 任务 2
│   ├── dividend.py          # 任务 3
│   ├── share_change.py      # 任务 4
│   ├── unlock.py            # 任务 5
│   ├── macro.py             # 任务 10
├── market_data/
│   ├── conversion_bond.py   # 任务 6
│   ├── option.py            # 任务 7
│   ├── index_components.py  # 任务 8
│   ├── industry_sw.py       # 任务 9
```

### 测试文件建议
每个任务对应一个测试文件，命名如：
- `tests/test_company_info_api.py`
- `tests/test_shareholder_api.py`
- `tests/test_dividend_api.py`
- 等等

---

## 实施顺序建议

建议按以下顺序实施：

1. **任务 1**：公司基本信息（基础，其他任务可能依赖）
2. **任务 2**：股东信息（高频使用，策略重要）
3. **任务 3**：分红送股（复权计算必需）
4. **任务 8**：指数成分股（回测常用）
5. **任务 9**：申万行业（策略分类必需）
6. **任务 5**：限售解禁（风险管理重要）
7. **任务 4**：股东变动（辅助分析）
8. **任务 6**：可转债（扩展资产类别）
9. **任务 7**：期权（扩展资产类别）
10. **任务 10**：宏观数据（宏观策略必需）

前 5 个任务完成后，股票策略的核心数据支持将基本完善。
后 5 个任务将扩展到更丰富的资产类别和宏观视角。

---

## 注意事项

1. **数据质量验证**：每个数据源获取后需验证字段完整性、数据准确性
2. **错误处理**：数据缺失、数据源不可用时需有明确错误提示，不要静默失败
3. **性能优化**：批量查询需支持，避免单次 API 调用过慢
4. **版本兼容**：保持与聚宽 API 签名兼容，便于策略移植
5. **文档更新**：实现后更新 `docs/api_supplements.md`，记录新增 API

---

## 交付检查清单

每个任务完成后需确认：
- [ ] 核心数据 API 已实现并通过测试
- [ ] finance.run_query 兼容接口已集成
- [ ] DuckDB 缓存机制已建立
- [ ] 单元测试已编写并通过
- [ ] 文档已更新
- [ ] 示例代码已提供
- [ ] 已知限制已说明