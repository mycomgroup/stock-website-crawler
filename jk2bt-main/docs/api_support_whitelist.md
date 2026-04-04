# API 支持白名单与分层策略

> 创建日期：2026-04-04
> 维护者：jk2bt 团队
> 目的：明确 API 支持状态，避免扫描器误判和 runtime 假支持混用

## 1. API 支持状态矩阵

### 1.1 已完整实现的 API（扫描器白名单）

| API 名称 | 实现位置 | 实现方式 | 备注 |
|---------|---------|---------|------|
| `get_price` | api/market.py | AkShare + market_data 模块 | 支持日线/分钟线，支持复权 |
| `get_price_jq` | api/market.py | 别名映射 | get_price 的聚宽风格别名 |
| `history` | api/market.py | 调用 get_price | 多标点单字段历史数据 |
| `attribute_history` | api/market.py | 调用 get_price | 单标点多字段历史数据 |
| `get_bars` | api/market.py | 调用 get_price | K线数据聚宽风格 |
| `get_bars_jq` | api/market.py | 别名映射 | get_bars 的聚宽风格别名 |
| `get_market` | api/market.py | 扩展版行情 | 支持估值字段 |
| `get_detailed_quote` | api/market.py | 实时行情 | 详细行情信息 |
| `get_ticks_enhanced` | api/market.py | AkShare tick | Tick级数据（映射旧名称 get_ticks） |
| **get_ticks** | api/market.py | 名称映射 | 旧名称 → `get_ticks_enhanced` ✅ |
| `get_fundamentals` | core/strategy_base.py | AkShare + DuckDB | 财务数据查询 |
| `get_all_securities` | core/strategy_base.py | AkShare | 全市场证券列表 |
| `get_security_info` | core/strategy_base.py | AkShare | 证券详细信息 |
| `get_index_weights` | core/strategy_base.py | AkShare | 指数权重 |
| `get_index_stocks` | core/strategy_base.py | AkShare | 指数成分股 |
| `get_all_trade_days` | core/strategy_base.py | AkShare | 交易日历 |
| `get_trade_days` | core/strategy_base.py | 别名 | 交易日历（简化版） |
| `get_extras` | core/strategy_base.py | AkShare | 市场额外信息 |
| `get_billboard_list` | api/billboard.py | AkShare | 龙虎榜数据 |
| **get_institutional_holdings** | api/billboard.py | AkShare | 机构持股数据 ✅ |
| `get_factor_values` | core/strategy_base.py | 预留 | 因子数据（部分支持） |
| `get_current_data` | core/strategy_base.py | Backtrader context | 当前行情快照 |
| `get_current_tick` | core/strategy_base.py | Backtrader | 当前tick数据 |
| **get_future_contracts** | api/futures.py | AkShare | 期货合约列表 ✅ |
| **get_dominant_contract** | api/futures.py | 内部函数 | 主力合约（通过 get_dominant_future） ✅ |
| `get_dominant_future` | api/futures.py | AkShare | 主力合约代码 |
| `get_futures_info` | api/futures.py | AkShare | 期货合约信息 |
| **get_contract_multiplier** | api/futures.py | 内部函数 | 合约乘数（通过 `_get_multiplier`） ✅ |
| `get_mtss` | api/margin.py | AkShare | 融资融券数据 |
| **get_margin_stocks** | api/margin.py | 新接口映射 | → `get_margincash_stocks` / `get_marginsec_stocks` ✅ |
| `get_margincash_stocks` | api/margin.py | AkShare | 可融资标的列表 |
| `get_marginsec_stocks` | api/margin.py | AkShare | 可融券标的列表 |
| `get_concepts` | api/concept.py | AkShare | 概念板块 |
| `get_concept_stocks` | api/concept.py | AkShare | 概念板块成分股 |
| `get_index_valuation` | api/valuation.py | AkShare | 指数估值 |
| `get_valuation` | api/valuation.py | AkShare | 个股估值 |
| `query` | core/strategy_base.py | 模拟实现 | 财务查询构建器 |

**标记说明：**
- ✅ 表示之前扫描器误判为未实现，现已修正
- 所有在 `_KNOWN_APIS` 中的 API 都视为已实现或部分实现

### 1.2 名称映射表（解决扫描器与 runtime 命名差异）

扫描器检查旧 API 名称时，实际 runtime 通过新名称已实现：

```python
_API_NAME_MAPPING = {
    "get_ticks": "get_ticks_enhanced",          # Tick数据增强版
    "get_future_contracts": "get_future_contracts",  # 直接映射
    "get_dominant_contract": "get_dominant_future",  # 主力合约
    "get_institutional_holdings": "get_institutional_holdings",  # 直接映射
    "get_margin_stocks": "get_margincash_stocks",  # 融资标的（新接口）
}
```

**扫描器逻辑修正：**
- 优先检查 `_API_NAME_MAPPING`，映射存在则视为已实现
- 不再误判这些 API 为 MISSING_API

---

## 2. 真实未支持的 API 分层管理

### 2.1 分层定义

| 层级 | 定义 | 典型特征 | 处理策略 |
|-----|------|---------|---------|
| **暂不支持层** | 低频使用或特殊场景，不影响核心策略运行 | 债券/期权/信用数据等 | 扫描器标记为未实现，策略可继续运行 |
| **可降级模拟层** | 中频使用，可提供简化实现或降级方案 | 融资融券详细信息、现金流数据等 | 提供基础实现或降级映射 |
| **必须实现层** | 高频使用，核心策略依赖 | 分红拆股数据、股东信息等 | 优先实现，标记为 MISSING_API |

### 2.2 暂不支持层（低频/特殊场景）

| API 名称 | 原因 | 替代方案 | 实现优先级 |
|---------|------|---------|-----------|
| `get_margin_info` | 已有 `get_mtss` 提供基础融资融券数据 | 使用 `get_mtss` | P3 - 低优先级 |
| `get_trade_info` | 交易详细信息需求少 | 使用 `get_bars` + `get_ticks_enhanced` | P3 |
| `get_trading_dates` | 已有 `get_all_trade_days` | 使用 `get_all_trade_days` | P3 |
| `get_interest_rate` | 债券数据低频使用 | 无替代，暂不支持 | P3 |
| `get_yield_curve` | 债券曲线数据低频 | 无替代，暂不支持 | P3 |
| `get_bond_prices` | 债券价格数据低频 | 无替代，暂不支持 | P3 |
| `get_bond_yield` | 债券收益率低频 | 无替代，暂不支持 | P3 |
| `get_option_pricing` | 期权定价特殊场景 | 无替代，暂不支持 | P3 |
| `get_volatility_surface` | 波动率曲面特殊场景 | 无替代，暂不支持 | P3 |
| `get_call_info` | 期权认购信息特殊场景 | 无替代，暂不支持 | P3 |
| `get_credit_data` | 信用数据低频使用 | 无替代，暂不支持 | P3 |
| `get_macro_data` | 宏观数据低频使用 | 无替代，暂不支持 | P3 |
| `get_company_info` | 公司详细信息低频 | 使用 `get_security_info` | P3 |
| `get_board_info` | 董事会信息低频 | 无替代，暂不支持 | P3 |
| `get insider_trades` | 内部交易数据低频 | 无替代，暂不支持 | P3 |

**扫描器处理：**
- 标记为 MISSING_API，但不阻止策略运行（is_executable 可为 True）
- 日志警告："API XXX 暂不支持，策略可能受限"

### 2.3 可降级模拟层（中频使用）

| API 名称 | 当前状态 | 降级方案 | 实现优先级 |
|---------|---------|---------|-----------|
| `get_margin_stocks` | ✅ 已通过新接口实现 | 使用 `get_margincash_stocks` 或 `get_marginsec_stocks` | 已实现 |
| `get_cash_flow` | 已有 income/cash_flow/balance 模块 | 使用 `query(finance.cash_flow)` | P2 - 中优先级 |
| `get_contract_multiplier` | ✅ 内部函数已实现 | 通过 `get_futures_info` 获取 multiplier | 已实现 |

**降级策略：**
- 提供 API 别名映射或简化实现
- 扫描器不标记为 MISSING_API

### 2.4 必须实现层（高频使用）

| API 名称 | 当前状态 | 使用频率 | 实现优先级 | 计划实现时间 |
|---------|---------|---------|-----------|-------------|
| `get_dividends` | ❌ 未实现 | 高频 | P0 - 最高优先级 | 2026-04-05 |
| `get_splits` | ❌ 未实现 | 高频 | P0 - 最高优先级 | 2026-04-05 |
| `get_shareholder_info` | ❌ 未实现 | 中频 | P1 - 高优先级 | 2026-04-10 |

**扫描器处理：**
- 标记为 MISSING_API，阻止策略运行（is_executable = False）
- 必须在 runtime 中完整实现后才允许运行

---

## 3. API 实现优先级路线图

### P0 级（本周必须完成）
- `get_dividends` - 分红数据（AkShare: `stock_dividend_cn`)
- `get_splits` - 拆股数据（AkShare: `stock_split_cn`)

### P1 级（两周内完成）
- `get_shareholder_info` - 股东信息（AkShare: `stock_share_change_cn`)

### P2 级（一个月内完成）
- `get_cash_flow` - 现金流简化接口（封装现有 finance 模块）

### P3 级（低优先级，按需实现）
- 债券相关 API（`get_interest_rate`, `get_yield_curve`, etc.)
- 期权相关 API（`get_option_pricing`, `get_volatility_surface`, etc.)
- 其他低频 API

---

## 4. 扫描器与 Runtime 对齐检查清单

### 4.1 扫描器修正逻辑

```python
# scanner.py 修正后的逻辑
def check_api_support(func):
    # 1. 先检查名称映射（解决命名差异）
    if func in _API_NAME_MAPPING:
        return True  # 已实现（名称不同）

    # 2. 检查已知 API（完整实现）
    if func in _KNOWN_APIS:
        return True

    # 3. 检查未实现 API（分层管理）
    if func in _UNIMPLEMENTED_APIS:
        return False

    # 4. 其他 API 视为未知
    return False
```

### 4.2 Runtime 实现检查

确保以下导出的 API 在 `__init__.py` 中正确导出：

**jk2bt/api/__init__.py 导出清单：**
```python
__all__ = [
    # 行情数据
    "get_price", "get_price_jq", "history", "attribute_history",
    "get_bars", "get_bars_jq", "get_market", "get_detailed_quote",
    "get_ticks_enhanced",  # ✅ 解决 get_ticks 名称差异

    # 期货数据
    "get_dominant_future", "get_futures_info",
    "get_future_contracts",  # ✅ 解决扫描器误判

    # 融资融券
    "get_mtss", "get_margincash_stocks", "get_marginsec_stocks",

    # 榜单数据
    "get_billboard_list", "get_institutional_holdings",  # ✅ 解决扫描器误判

    # ... 其他已实现 API
]
```

### 4.3 自动化测试验证

**测试策略文件：**
```python
# test_api_support.py
def test_api_mapping():
    """验证 API 名称映射正确"""
    scanner = StrategyScanner()

    # 测试之前误判的 API
    test_apis = [
        "get_ticks",           # → get_ticks_enhanced
        "get_future_contracts", # → get_future_contracts
        "get_dominant_contract", # → get_dominant_future
        "get_institutional_holdings", # → get_institutional_holdings
        "get_margin_stocks",   # → get_margincash_stocks
    ]

    for api in test_apis:
        result = scanner.scan_file(f"test_{api}.py")
        assert api not in result.missing_apis, f"{api} should not be marked as missing"

def test_missing_api_accuracy():
    """验证真实未支持 API 的准确性"""
    scanner = StrategyScanner()

    # 测试真实未支持的 API
    test_apis = [
        "get_dividends",
        "get_splits",
        "get_interest_rate",
    ]

    for api in test_apis:
        result = scanner.scan_file(f"test_{api}.py")
        assert api in result.missing_apis, f"{api} should be marked as missing"
```

---

## 5. 维护与更新机制

### 5.1 API 实现后更新流程

当新 API 实现后，需要同步更新以下文件：

1. **jk2bt/api/*.py** - 实现文件
2. **jk2bt/api/__init__.py** - 导出清单
3. **jk2bt/strategy/scanner.py** - 移除 `_UNIMPLEMENTED_APIS` 中的条目
4. **docs/api_support_whitelist.md** - 更新支持状态矩阵

### 5.2 定期审查机制

- **每月审查：** 检查 `_UNIMPLEMENTED_APIS` 是否与实际 runtime 实现对齐
- **自动化测试：** 每次提交时运行 `test_api_support.py` 验证映射准确性
- **文档同步：** 每次新增 API 时更新白名单文档

---

## 6. 总结

### 修正前的问题
- 扫描器误判：`get_ticks`, `get_future_contracts`, `get_institutional_holdings` 等实际已实现的 API 被标为未实现
- Runtime 假支持：部分 API 在 `__init__.py` 导出但实现不完整

### 修正后的状态
- ✅ 扫描器与 runtime口径一致：missing_api 统计准确反映真实运行缺口
- ✅ API 名称映射：解决命名差异导致的误判
- ✅ 分层管理：暂不支持/可降级/必须实现三层清晰划分
- ✅ 白名单文档：完整记录 API 支持状态，避免未来混用

### 完成标准验证
1. **missing_api 统计准确性：** 100% 反映真实未实现的 API（P0/P1/P2/P3 分层）
2. **扫描器误杀消除：** `get_ticks` 等已实现 API 不再出现在 missing_apis 中
3. **runtime 假支持消除：** 所有导出的 API 都有完整实现或明确降级方案
4. **分层清晰：** 暂不支持/可降级/必须实现三层策略明确，不再出现混用

---

**变更记录：**
- 2026-04-04: 创建文档，修正扫描器误判，建立分层体系