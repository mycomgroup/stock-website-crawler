# P1离线样本数据包与验收策略集方案

## 1. 设计目标

### 1.1 最小离线样本数据包
**完成标准**：新用户不依赖网络也能跑出结果

**覆盖范围**：
- README示例策略（03 一个简单而持续稳定的懒人超额收益策略）
- 3-5个真实样本策略（覆盖核心API）

### 1.2 产品级验收策略集
**完成标准**：有一份小而稳定的金标策略集，用于安装验收和回归

**特点**：
- 小而精（5-10个策略）
- 稳定可预期（避免复杂策略）
- API覆盖全面
- 数据需求明确

---

## 2. 验收策略集（Validation Strategy Set）

### 2.1 策略选择标准
1. **简单性**：代码逻辑清晰，易于理解和维护
2. **稳定性**：避免使用复杂因子、机器学习等不稳定组件
3. **API覆盖**：覆盖核心聚宽API（定时器、下单、数据查询、基本面）
4. **数据范围**：股票池小、时间范围适中、数据类型明确
5. **可回归**：结果可预期，用于回归测试

### 2.2 金标策略集（共7个）

#### 策略1：README示例 - 指数权重轮动
**文件**：`strategies/03 一个简单而持续稳定的懒人超额收益策略.txt`
**特点**：最简单，README示例
**API覆盖**：
- `get_index_weights` - 指数权重查询
- `get_current_data` - 实时数据
- `run_monthly` - 月度定时器
- `order_target` / `order_value` - 下单函数

**数据需求**：
- 股票池：沪深300前10大权重股（固定股票池）
- 指数：000300.XSHG（沪深300）
- 时间：2020-01-01 到 2023-12-31（3年）
- 类型：股票日线 + 指数成分权重

#### 策略2：红利搬砖 - 基本面选股
**文件**：`strategies/04 红利搬砖，年化29%.txt`
**特点**：基本面策略，财务数据查询
**API覆盖**：
- `get_index_stocks` - 指数成分股
- `get_fundamentals` - 基本面查询（valuation表）
- `finance.run_query` - 分红数据查询（STK_XR_XD表）
- `get_security_info` - 证券信息
- `run_monthly` - 月度定时器

**数据需求**：
- 股票池：沪深300成分股（约300只）
- 指数：000300.XSHG
- 时间：2020-01-01 到 2022-12-31（3年）
- 类型：股票日线 + 基本面数据（valuation） + 分红数据

#### 策略3：ETF轮动 - 多资产类别
**文件**：`strategies/16 ETF轮动策略升级-多类别-低回撤.txt`
**特点**：多资产类别（股票ETF、期货ETF、全球ETF、REITs）
**API覆盖**：
- `get_price` - 历史价格数据
- `get_security_info` - 证券信息
- `get_all_securities` - 全市场证券列表
- `get_current_data` - 实时数据
- `run_daily` - 日度定时器

**数据需求**：
- ETF池：约15只代表性ETF（A股指数、国际期货、全球股指、REITs）
- 时间：2020-01-01 到 2022-12-31（3年）
- 类型：ETF日线数据 + 证券基础信息

#### 策略4：简单双均线策略（自定义）
**特点**：最简单的技术指标策略，不依赖基本面数据
**API覆盖**：
- `get_price` - 历史价格数据
- `history` - 历史数据查询
- `run_daily` - 日度定时器
- `order_target_percent` - 百分比下单

**数据需求**：
- 股票池：5只蓝筹股（贵州茅台、五粮液、美的集团、招商银行、中国平安）
- 时间：2021-01-01 到 2023-12-31（3年）
- 类型：股票日线数据

#### 策略5：小市值选股（简化版）
**文件**：从现有策略中选一个简单的小市值策略
**特点**：经典量化策略，基本面+市值过滤
**API覆盖**：
- `get_fundamentals` - 基本面查询
- `get_index_stocks` - 股票池过滤
- `run_monthly` - 月度调仓
- `filter_st` / `filter_paused` - 过滤函数

**数据需求**：
- 股票池：沪深300成分股
- 时间：2020-01-01 到 2022-12-31（3年）
- 类型：股票日线 + 基本面数据

#### 策略6：指数成分股跟踪策略（自定义）
**特点**：跟踪指数成分股变化
**API覆盖**：
- `get_index_stocks` - 指数成分股查询
- `get_index_weights` - 指数权重
- `run_monthly` - 月度调仓
- `order_target` - 目标仓位下单

**数据需求**：
- 指数：沪深300、中证500
- 时间：2020-01-01 到 2023-12-31（4年）
- 类型：指数成分权重数据 + 股票日线

#### 策略7：RSI择时策略（自定义）
**特点**：技术指标择时，不依赖基本面
**API覆盖**：
- `get_price` - 历史价格数据
- `attribute_history` - 属性历史数据
- 计算指标函数（内部实现RSI）
- `run_daily` - 日度定时器

**数据需求**：
- 股票池：3只ETF（沪深300ETF、创业板ETF、上证50ETF）
- 时间：2021-01-01 到 2023-12-31（3年）
- 类型：ETF日线数据

### 2.3 验收策略集总结

| ID | 策略名称 | 类型 | 股票池大小 | 时间范围 | 核心API |
|----|---------|------|----------|---------|---------|
| V1 | 指数权重轮动 | 股票 | 10只 | 2020-2023 | get_index_weights, order_value |
| V2 | 红利搬砖 | 股票 | 300只 | 2020-2022 | get_fundamentals, finance.run_query |
| V3 | ETF轮动 | ETF | 15只 | 2020-2022 | get_price, get_all_securities |
| V4 | 双均线择时 | 股票 | 5只 | 2021-2023 | get_price, history |
| V5 | 小市值选股 | 股票 | 300只 | 2020-2022 | get_fundamentals, filter_st |
| V6 | 指数跟踪 | 股票 | 动态 | 2020-2023 | get_index_stocks, get_index_weights |
| V7 | RSI择时 | ETF | 3只 | 2021-2023 | get_price, attribute_history |

**验收集特点**：
- 共7个策略，覆盖股票和ETF两大资产类别
- 股票池范围：5只（最小）到300只（最大）
- 时间范围：统一为3-4年（2020-2023）
- API覆盖：定时器、下单、价格数据、基本面、指数数据

---

## 3. 最小离线数据包设计

### 3.1 数据包组成

#### 3.1.1 元数据（必须）
```
data/cache/meta_cache/
├── trade_days.pkl          # 交易日历（2020-2023）
└── securities_YYYYMMDD.pkl # 全市场证券信息
```

#### 3.1.2 股票日线数据
```
data/jk2bt.duckdb（stock_daily表）
- 覆盖股票池：
  * 沪深300成分股（约300只） - 用于V1, V2, V5, V6
  * 核心蓝筹股（固定10只） - 用于V1, V4
- 时间范围：2020-01-01 到 2023-12-31
- 复权方式：qfq（前复权）
- 字段：datetime, symbol, open, high, low, close, volume, adjust
```

#### 3.1.3 ETF日线数据
```
data/jk2bt.duckdb（etf_daily表）
- 覆盖ETF池：
  * A股指数ETF：510300, 159915, 510050（沪深300、创业板、上证50）
  * 国际期货ETF：518880（黄金）, 501018（原油）, 161226（白银）
  * 全球股指ETF：513100（纳斯达克）, 513030（德国）, 513520（日经）
  * 国内期货ETF：159985（豆粕）, 159981（能源化工）, 159980（有色）
  * REITs：180101, 180301, 180801（简化为3只）
  * 共约15只代表性ETF
- 时间范围：2020-01-01 到 2022-12-31
- 字段：datetime, symbol, open, high, low, close, volume
```

#### 3.1.4 指数日线数据
```
data/jk2bt.duckdb（index_daily表）
- 覆盖指数：
  * 000300（沪深300）
  * 000905（中证500）
  * 000016（上证50）
- 时间范围：2020-01-01 到 2023-12-31
- 字段：datetime, symbol, open, high, low, close, volume
```

#### 3.1.5 指数成分权重数据
```
data/cache/index_cache/
├── 000300_weights.pkl  # 沪深300成分权重（历史快照）
├── 000905_weights.pkl  # 中证500成分权重
└── 000016_weights.pkl  # 上证50成分权重
```

#### 3.1.6 基本面数据（可选，按需）
```
data/valuation.db, data/dividend.db等
- valuation表：code, pe_ratio, pb_ratio, market_cap, pcf_ratio等
- dividend表：code, bonus_amount_rmb, board_plan_pub_date等
- 覆盖股票池：沪深300成分股
- 时间范围：2020-2022（按季度更新）
```

### 3.2 数据包大小预估

| 数据类型 | 覆盖范围 | 时间范围 | 预估大小 |
|---------|---------|---------|---------|
| 元数据 | 全市场 | 2020-2023 | ~1 MB |
| 股票日线 | 300只 | 4年×250天 | ~15 MB |
| ETF日线 | 15只 | 3年×250天 | ~0.8 MB |
| 指数日线 | 3只 | 4年×250天 | ~0.15 MB |
| 指数权重 | 3只 | 历史快照 | ~0.5 MB |
| 基本面数据 | 300只 | 季度数据 | ~5 MB |
| **总计** | | | **~22 MB** |

**结论**：最小离线数据包约20-25MB，完全可以打包分发。

---

## 4. 实施方案

### 4.1 创建验收策略集脚本

**文件**：`tools/validation/create_validation_set.py`
**功能**：
- 定义7个验收策略的元数据（股票池、时间范围、API列表）
- 生成验收策略清单文件：`validation_strategies.json`
- 自动识别策略的数据需求

### 4.2 生成离线数据包脚本

**文件**：`tools/data/create_offline_package.py`
**功能**：
- 基于验收策略集，计算数据需求
- 调用`prewarm_data.py`预热所有数据
- 打包数据为单个压缩文件：`jk2bt_offline_data_v1.0.tar.gz`
- 包含：
  * DuckDB数据库文件
  * 缓存目录（meta_cache, index_cache）
  * 验收策略清单文件
  * 使用说明文档

### 4.3 验收测试脚本

**文件**：`tests/validation/test_validation_strategies.py`
**功能**：
- 测试所有7个验收策略能否在离线模式下运行
- 验证数据完整性（使用`cache_status.py`）
- 生成验收报告：`validation_report.md`

### 4.4 安装验收流程

**文件**：`docs/installation_validation.md`
**流程**：
```bash
# 1. 包导入测试
python3 -c "import jk2bt; print(jk2bt.__version__)"

# 2. 核心链路测试
pytest -q tests/test_package_import.py tests/integration/test_jq_runner.py

# 3. 验收策略集运行（可选，支持离线模式）
python tools/validation/run_validation_strategies.py --offline
```

---

## 5. 后续优化建议

### 5.1 数据包版本管理
- 定期更新数据包（每季度）
- 版本命名：`jk2bt_offline_data_vYYYY.Q.tar.gz`
- 维护历史版本用于回归测试

### 5.2 验收策略集维护
- 定期review策略稳定性
- 遇到API变更时及时更新
- 新增策略时考虑是否加入验收集

### 5.3 数据预热优化
- 支持增量预热（只预热缺失数据）
- 支持并行预热（多线程下载）
- 支持断点续传（中断后继续）

### 5.4 离线模式增强
- 支持完全离线运行（无网络依赖）
- 离线模式下明确提示数据缺失
- 提供数据需求分析工具

---

## 6. 交付清单

### 6.1 文档
- [x] 本方案文档：`docs/offline_data_package_plan.md`
- [ ] 安装验收指南：`docs/installation_validation.md`
- [ ] 验收策略清单：`tools/validation/validation_strategies.json`

### 6.2 代码
- [ ] 验收策略集脚本：`tools/validation/create_validation_set.py`
- [ ] 离线数据包生成脚本：`tools/data/create_offline_package.py`
- [ ] 验收测试脚本：`tests/validation/test_validation_strategies.py`
- [ ] 验收运行脚本：`tools/validation/run_validation_strategies.py`

### 6.3 数据
- [ ] 离线数据包：`jk2bt_offline_data_v1.0.tar.gz`（约22MB）
- [ ] 验收报告：`validation_report.md`

---

## 附录：验收策略详细清单

见下文`validation_strategies.json`配置文件。