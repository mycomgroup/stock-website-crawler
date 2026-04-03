# 任务 9: 资产路由与子账户模型 - 完成报告

**执行时间**: 2026-03-30

---

## 1. 修改的文件

| 文件 | 操作 | 说明 |
|------|------|------|
| `jqdata_akshare_backtrader_utility/asset_router.py` | 新增 | 资产类别识别路由器 |
| `jqdata_akshare_backtrader_utility/subportfolios.py` | 新增 | 子账户模型实现 |
| `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py` | 修改 | ContextProxy 整合子账户 |
| `jqdata_akshare_backtrader_utility/__init__.py` | 修改 | 导出新模块 |
| `tests/test_subportfolios.py` | 新增 | 测试文件 |

---

## 2. 完成的功能

### 2.1 资产路由识别 (`asset_router.py`)

**支持识别的资产类型**:

| 资产类型 | 代码格式 | 交易状态 | 说明 |
|----------|----------|----------|------|
| STOCK | `.XSHG`/`.XSHE`/`sh`/`sz`/纯代码 | ✅ 支持 | A股股票 |
| ETF | 51*/52*代码段 | ✅ 支持 | 场内ETF |
| LOF | 16*代码段 | ✅ 支持 | 上市开放式基金 |
| FUND_OF | `.OF` 后缀 | ⚠️ 仅识别 | 场外基金，暂不支持交易 |
| FUTURE_CCFX | `.CCFX` 后缀 | ⚠️ 仅识别 | 股指期货，暂不支持交易 |
| INDEX | 指数代码 | ⚠️ 仅识别 | 指数，暂不支持交易 |

**核心类**:

```python
class AssetType(Enum):
    STOCK = "stock"
    ETF = "etf"
    LOF = "lof"
    FUND_OF = "fund_of"
    FUTURE_CCFX = "future_ccfx"
    INDEX = "index"
    UNKNOWN = "unknown"

class TradingStatus(Enum):
    SUPPORTED = "supported"           # 支持交易
    IDENTIFIED_ONLY = "identified_only"  # 仅识别，不支持交易
    NOT_SUPPORTED = "not_supported"   # 不支持
```

**便捷函数**:

```python
identify_asset(code) -> AssetInfo    # 识别资产类型
is_stock(code) -> bool               # 是否股票
is_etf(code) -> bool                 # 是否ETF/LOF
is_fund_of(code) -> bool             # 是否场外基金
is_future(code) -> bool              # 是否期货
is_index(code) -> bool               # 是否指数
```

### 2.2 子账户模型 (`subportfolios.py`)

**设计原则**:
- 每个子账户有独立的现金视图，非浅包装
- 支持子账户间资金划转
- 为期货、基金等资产类策略预留扩展点

**核心类**:

| 类 | 说明 |
|----|------|
| `SubportfolioConfig` | 子账户配置（名称、类型、初始资金等） |
| `SubportfolioCashAccount` | 独立现金账户，支持存取款和交易记录 |
| `SubportfolioProxy` | 子账户代理，提供 cash/positions/total_value 等属性 |
| `SubportfolioManager` | 管理多子账户，支持资金划转 |

**使用示例**:

```python
class MyStrategy(JQ2BTBaseStrategy):
    def initialize(self):
        # 设置子账户配置
        configs = [
            {"name": "股票账户", "type": "stock", "initial_cash": 40000.0},
            {"name": "ETF账户", "type": "etf", "initial_cash": 30000.0},
        ]
        self.context.set_subportfolios(configs)
    
    def handle_data(self, context):
        # 访问子账户
        stock_sp = context.subportfolios[0]
        etf_sp = context.subportfolios[1]
        
        # 独立现金视图
        print(f"股票账户现金: {stock_sp.cash}")
        print(f"ETF账户现金: {etf_sp.cash}")
        
        # 资金划转
        context.transfer_cash(0, 1, 10000.0)  # 从股票账户划转1万到ETF账户
```

### 2.3 ContextProxy 增强

**新增方法**:

| 方法 | 说明 |
|------|------|
| `set_subportfolios(configs)` | 设置子账户配置 |
| `transfer_cash(from_idx, to_idx, amount, reason)` | 子账户间资金划转 |
| `get_subportfolio(index)` | 获取指定子账户 |
| `get_subportfolio_summary()` | 获取子账户汇总信息 |

**向后兼容**:
- 默认 `context.subportfolios` 返回 `[context.portfolio]`
- 调用 `set_subportfolios()` 后切换到新的子账户模型

---

## 3. 测试验证

### 3.1 测试文件

`tests/test_subportfolios.py` 包含以下测试类:

- `TestAssetRouter`: 资产路由识别测试 (11个测试)
  - 股票识别（沪/深/前缀/纯代码）
  - ETF/LOF识别
  - 场外基金 `.OF` 识别
  - 期货 `.CCFX` 识别
  - 指数识别

- `TestSubportfolioCashAccount`: 现金账户测试 (7个测试)
  - 初始资金
  - 存款/取款
  - 余额不足处理
  - 允许负余额
  - 交易记录

- `TestSubportfolioProxy`: 子账户代理测试 (4个测试)
  - 基本属性
  - 持仓管理
  - 现金存取

- `TestSubportfolioManager`: 子账户管理器测试 (6个测试)
  - 设置子账户
  - 获取子账户
  - 资金划转
  - 主账户划转
  - 汇总信息

- `TestContextProxySubportfolios`: Context集成测试 (4个测试)
  - 默认子账户
  - 设置子账户
  - 现金视图独立
  - 资金划转

### 3.2 验证命令

```bash
cd /Users/yuping/Downloads/git/jk2bt-main

# 运行新增测试
python3 -m pytest tests/test_subportfolios.py -v

# 运行原有测试确保兼容
python3 -m pytest tests/test_context_simulation.py -v
```

### 3.3 测试结果

```
tests/test_subportfolios.py::TestAssetRouter::test_group_by_type PASSED
tests/test_subportfolios.py::TestAssetRouter::test_helper_functions PASSED
tests/test_subportfolios.py::TestAssetRouter::test_identify_etf_15 PASSED
tests/test_subportfolios.py::TestAssetRouter::test_identify_etf_51 PASSED
tests/test_subportfolios.py::TestAssetRouter::test_identify_fund_of PASSED
tests/test_subportfolios.py::TestAssetRouter::test_identify_future_ccfx PASSED
tests/test_subportfolios.py::TestAssetRouter::test_identify_index PASSED
tests/test_subportfolios.py::TestAssetRouter::test_identify_stock_pure_code PASSED
tests/test_subportfolios.py::TestAssetRouter::test_identify_stock_sh PASSED
tests/test_subportfolios.py::TestAssetRouter::test_identify_stock_sz PASSED
tests/test_subportfolios.py::TestAssetRouter::test_identify_stock_with_prefix PASSED
tests/test_subportfolios.py::TestSubportfolioCashAccount::test_deposit PASSED
tests/test_subportfolios.py::TestSubportfolioCashAccount::test_initial_cash PASSED
tests/test_subportfolios.py::TestSubportfolioCashAccount::test_transactions_log PASSED
tests/test_subportfolios.py::TestSubportfolioCashAccount::test_withdraw_allow_negative PASSED
tests/test_subportfolios.py::TestSubportfolioCashAccount::test_withdraw_fail_insufficient PASSED
tests/test_subportfolios.py::TestSubportfolioCashAccount::test_withdraw_fail_negative PASSED
tests/test_subportfolios.py::TestSubportfolioCashAccount::test_withdraw_success PASSED
tests/test_subportfolios.py::TestSubportfolioProxy::test_add_position PASSED
tests/test_subportfolios.py::TestSubportfolioProxy::test_add_position_accumulate PASSED
tests/test_subportfolios.py::TestSubportfolioProxy::test_basic_properties PASSED
tests/test_subportfolios.py::TestSubportfolioProxy::test_deposit_withdraw PASSED
tests/test_subportfolios.py::TestSubportfolioManager::test_get_subportfolio PASSED
tests/test_subportfolios.py::TestSubportfolioManager::test_get_summary PASSED
tests/test_subportfolios.py::TestSubportfolioManager::test_set_subportfolios PASSED
tests/test_subportfolios.py::TestSubportfolioManager::test_transfer_cash PASSED
tests/test_subportfolios.py::TestSubportfolioManager::test_transfer_cash_fail_insufficient PASSED
tests/test_subportfolios.py::TestSubportfolioManager::test_transfer_from_main PASSED
tests/test_subportfolios.py::TestContextProxySubportfolios::test_context_cash_view_distinct PASSED
tests/test_subportfolios.py::TestContextProxySubportfolios::test_context_set_subportfolios PASSED
tests/test_subportfolios.py::TestContextProxySubportfolios::test_context_subportfolios_default PASSED
tests/test_subportfolios.py::TestContextProxySubportfolios::test_context_transfer_cash PASSED

======================== 32 passed =========================
```

---

## 4. 剩余风险 / 已知边界

| 风险项 | 说明 | 后续处理 |
|--------|------|----------|
| 场外基金 `.OF` | 仅识别，不支持交易 | 需要场外基金数据源接入 |
| 股指期货 `.CCFX` | 仅识别，不支持交易 | 需要期货撮合系统实现 |
| 子账户持仓联动 | 持仓暂未与主账户 broker 联动 | 后续期货 agent 可扩展 |
| 指数代码冲突 | `000001` 同时是上证指数和平安银行 | 已通过交易所后缀区分 |
| 子账户交易执行 | 下单时未自动路由到对应子账户 | 后续可扩展 `order_for_subportfolio()` |

---

## 5. 扩展点设计

### 5.1 期货扩展点

```python
# 后续期货 agent 可扩展
class FutureSubportfolioProxy(SubportfolioProxy):
    def __init__(self, config, subportfolio_id, parent_strategy):
        super().__init__(config, subportfolio_id, parent_strategy)
        self._margin_account = MarginAccount()
        self._positions_by_contract = {}
    
    def set_leverage(self, leverage: float):
        """设置杠杆"""
        pass
    
    def get_margin_usage(self) -> float:
        """获取保证金占用率"""
        pass
```

### 5.2 资产过滤扩展点

```python
# 子账户可配置资产过滤器
def stock_filter(code: str) -> bool:
    return is_stock(code) or is_etf(code)

def future_filter(code: str) -> bool:
    return is_future(code)

configs = [
    SubportfolioConfig(
        name="股票账户",
        type=SubportfolioType.STOCK,
        initial_cash=100000.0,
        asset_filter=stock_filter,  # 只能交易股票/ETF
    ),
]
```

---

## 6. 最小验证方式

```python
# 快速验证资产识别
from jqdata_akshare_backtrader_utility import identify_asset, is_stock, is_etf

print(identify_asset("600519.XSHG").asset_type)  # STOCK
print(identify_asset("510300.XSHG").asset_type)  # ETF
print(identify_asset("000001.OF").asset_type)    # FUND_OF
print(identify_asset("IF2312.CCFX").asset_type)  # FUTURE_CCFX

# 验证交易状态
info = identify_asset("000001.OF")
print(info.is_identified_only())  # True (场外基金仅识别)
print(info.is_supported())        # False

# 验证子账户模型
from jqdata_akshare_backtrader_utility import SubportfolioManager, SubportfolioConfig, SubportfolioType

manager = SubportfolioManager()
manager.initialize(100000.0)
configs = [
    SubportfolioConfig(name="股票", type=SubportfolioType.STOCK, initial_cash=50000.0),
    SubportfolioConfig(name="ETF", type=SubportfolioType.ETF, initial_cash=30000.0),
]
manager.set_subportfolios(configs)

print(manager.subportfolios[0].cash)  # 50000.0
print(manager.subportfolios[1].cash)  # 30000.0

manager.transfer_cash(0, 1, 10000.0)
print(manager.subportfolios[0].cash)  # 40000.0
print(manager.subportfolios[1].cash)  # 40000.0
```

---

## 7. 相关文件索引

| 文件 | 路径 |
|------|------|
| 资产路由 | `jqdata_akshare_backtrader_utility/asset_router.py` |
| 子账户模型 | `jqdata_akshare_backtrader_utility/subportfolios.py` |
| 基础策略类 | `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py` |
| 模块导出 | `jqdata_akshare_backtrader_utility/__init__.py` |
| 测试文件 | `tests/test_subportfolios.py` |
| 兼容性测试 | `tests/test_context_simulation.py` |