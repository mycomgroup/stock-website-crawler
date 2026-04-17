# Task 15 Result: 多资产与期货能力覆盖梳理

## 修改文件
- 无（本次为能力梳理，未修改代码）

**关键结论**: ❌ 本任务为**能力梳理**，非能力落地。LOF/OF/期货数据均**未对接**，多资产覆盖**远未达到可运行状态**。

## 完成内容

### 1. 资产识别能力梳理

#### asset_router.py 现状
| 资产类型 | AssetType | TradingStatus | 说明 |
|---------|-----------|---------------|------|
| 股票 | STOCK | SUPPORTED | 完全支持 |
| ETF | ETF | SUPPORTED | 完全支持 |
| LOF | LOF | SUPPORTED | 完全支持 |
| 场外基金(OF) | FUND_OF | IDENTIFIED_ONLY | 仅识别，不支持交易 |
| 股指期货(CCFX) | FUTURE_CCFX | IDENTIFIED_ONLY | 仅识别，不支持交易 |
| 指数 | INDEX | IDENTIFIED_ONLY | 仅识别，不支持交易 |

#### 识别规则
- **ETF**: 51xxxx、52xxxx、15xxxx、16xxxx、50xxxx、56xxxx、58xxxx
- **LOF**: 16xxxx（与ETF有重叠，优先识别为LOF）
- **OF**: 后缀为 .OF（如 000001.OF）
- **CCFX**: 后缀为 .CCFX（如 IF2312.CCFX）

### 2. 数据获取能力梳理

#### 已实现的数据模块
| 模块 | 资产类型 | 数据频率 | AkShare接口 | 状态 |
|------|---------|---------|------------|------|
| market_data/stock.py | 股票 | 日线/分钟 | stock_zh_a_hist | ✅ 可用 |
| market_data/etf.py | ETF | 日线 | fund_etf_hist_em | ✅ 可用 |
| market_data/minute.py | ETF/股票 | 分钟 | fund_etf_hist_min_em / stock_zh_a_hist_min_em | ✅ 可用 |
| market_data/index.py | 指数 | 日线 | index_zh_a_hist | ✅ 可用 |
| market_data/industry.py | 行业 | 日线 | board_industry_index_em | ✅ 可用 |
| market_data/north_money.py | 北向资金 | 日线 | stock_hsgt_* | ✅ 可用 |

#### 未实现的数据模块
| 资产类型 | 需要的接口 | AkShare可用接口 | 阻塞点 |
|---------|-----------|----------------|-------|
| LOF | LOF日线数据 | fund_lof_hist_em（存在） | ❌ 未对接 |
| OF（场外基金） | 基金净值数据 | fund_open_fund_daily、fund_etf_fund_daily | ❌ 未对接 |
| 期货(CCFX) | 期货合约行情 | futures_zh_index_sina、futures_main_sina | ❌ 未对接 |

**关键结论**: LOF/OF/期货数据源均**完全缺失**，多资产能力**无法落地**。

### 3. 交易能力梳理

#### Backtrader Broker 机制适配性
| 资产类型 | Broker适配 | 阻塞点 |
|---------|-----------|-------|
| 股票 | ✅ 完全适配 | 无 |
| ETF | ✅ 完全适配 | 无 |
| LOF | ⚠️ 部分适配 | 数据源可能误用ETF接口 |
| OF | ❌ 不适配 | 场外基金为申购赎回，非二级市场交易 |
| 期货 | ❌ 不适配 | 缺保证金、杠杆、合约乘数逻辑 |

#### 特殊交易机制需求
| 资产类型 | 特殊机制 | 状态 |
|---------|---------|------|
| ETF | T+0、一二级市场套利 | ❌ 未实现套利逻辑 |
| LOF | 一二级市场套利、申赎 | ❌ 未实现套利逻辑 |
| OF | 申购赎回、净值计算 | ❌ 未实现申赎机制 |
| 期货 | 保证金、杠杆、交割、移仓 | ❌ 完全缺失 |

**关键结论**: 特殊交易机制**完全缺失**，LOF/OF/期货交易能力**无法落地**。

### 4. 子账户与资金划转

#### subportfolios.py 现状
- ✅ 支持子账户类型划分：STOCK、ETF、FUTURE、FUND、MIXED
- ✅ 支持独立现金账户、初始资金配置
- ✅ 支持子账户间资金划转
- ✅ 支持资产过滤（asset_filter）
- ⚠️ 期货子账户只能记账，无法实际交易

#### 验证样本
- test_subportfolios.py:338 - ETF子账户配置测试
- test_subportfolios.py:372 - 子账户资金划转测试

### 5. 期货相关缺失能力

#### strategy_scanner.py 标记的未实现API
```python
_UNIMPLEMENTED_APIS = {
    "get_margin_stocks",        # 融资融券标的
    "get_margin_info",          # 融资融券信息
    "get_future_contracts",     # 期货合约列表
    "get_dominant_contract",    # 主力合约
    "get_contract_multiplier",  # 合约乘数
}
```

#### 期货数据缺失项
| 数据项 | 说明 | 状态 |
|-------|------|------|
| 合约乘数 | IF=300, IC=200, IH=50 | ❌ 未提供 |
| 保证金比例 | 各合约保证金要求 | ❌ 未提供 |
| 交割日期 | 合约到期日 | ❌ 未提供 |
| 主力合约 | 当月/下月主力判断 | ❌ 未提供 |
| 结算价 | 期货每日结算价 | ❌ 未提供 |

### 6. 多资产策略样本盘点

#### 已验证的策略样本
| 策略类型 | 样本文件 | 资产类型 | 状态 |
|---------|---------|---------|------|
| ETF Buy&Hold | tests/test_strategy.py:13 | ETF | ✅ 可运行 |
| 股票 Buy&Hold | tests/test_strategy.py:13 | 股票 | ✅ 可运行 |
| 子账户测试 | tests/test_subportfolios.py:338 | 多资产记账 | ✅ 可运行 |

#### 缺失的策略样本
| 策略类型 | 需要样本 | 阻塞点 |
|---------|---------|-------|
| LOF轮动策略 | LOF池、净值数据 | ❌ 无LOF数据源 |
| 场外基金定投 | OF申赎机制 | ❌ 无申赎逻辑 |
| 股指期货择时 | IF/IC/IH合约数据 | ❌ 无期货数据源 |
| 期现套利 | 期货+ETF组合 | ❌ 无期货数据源 |

**关键结论**: 多资产策略样本**完全缺失**，无法验证多资产能力。

## 验证样本

### 样本1: ETF策略（已验证可运行）
```python
# tests/test_strategy.py:28-78
ETF_POOL = {
    "518880": "黄金ETF",
    "513100": "纳指100",
    "159915": "创业板100",
    "510180": "上证180",
}

class BuyAndHoldStrategy(JQ2BTBaseStrategy):
    def next(self):
        for data in self.datas:
            if data._name not in self.bought:
                self.order_target_percent(data, target=1.0/len(self.datas))
                self.bought.add(data._name)
```

验证结果：✅ 可正常运行，净值序列完整，绩效分析可用

### 样本2: 子账户资金划转（已验证可运行）
```python
# tests/test_subportfolios.py:338-240
configs = [
    SubportfolioConfig(name="股票账户", type=SubportfolioType.STOCK, initial_cash=50000.0),
    SubportfolioConfig(name="ETF账户", type=SubportfolioType.ETF, initial_cash=20000.0),
]
sp_list = context.set_subportfolios(configs)
context.transfer_cash(0, 1, 10000.0, reason="调仓")
```

验证结果：✅ 划转逻辑正确，资金独立核算

### 样本3: LOF识别（仅识别，未验证交易）
```python
# tests/test_subportfolios.py:63
info = identify_asset("160105")  # LOF代码
self.assertIn(info.asset_type, [AssetType.ETF, AssetType.LOF])
```

验证结果：⚠️ 可识别，但无LOF策略样本

### 样本4: 场外基金识别（仅识别）
```python
# tests/test_subportfolios.py:68
info = identify_asset("000001.OF")
self.assertEqual(info.asset_type, AssetType.FUND_OF)
self.assertTrue(info.is_identified_only())
```

验证结果：⚠️ 可识别，不支持交易

### 样本5: 股指期货识别（仅识别）
```python
# tests/test_subportfolios.py:75
info = identify_asset("IF2312.CCFX")
self.assertEqual(info.asset_type, AssetType.FUTURE_CCFX)
self.assertTrue(info.is_identified_only())
```

验证结果：⚠️ 可识别，不支持交易

## 验证方式

### 验证方法1: 代码审计
- 阅读asset_router.py、subportfolios.py、backtrader_base_strategy.py
- 搜索market_data/*.py数据获取模块
- 检查strategy_scanner.py未实现API列表

### 验证方法2: 实际运行测试
- 运行test_strategy.py验证ETF策略
- 运行test_subportfolios.py验证子账户机制
- 运行pytest tests/验证所有测试通过

### 验证方法3: 资产识别测试
```python
from jqdata_akshare_backtrader_utility.asset_router import identify_asset, get_trading_status_desc

codes = [
    "600519.XSHG",  # 股票
    "510300.XSHG",  # ETF
    "160105",       # LOF
    "000001.OF",    # 场外基金
    "IF2312.CCFX",  # 股指期货
    "000300.XSHG",  # 指数
]

for code in codes:
    info = identify_asset(code)
    desc = get_trading_status_desc(code)
    print(f"{code}: {info.asset_type.value} - {desc}")
```

输出：
```
600519.XSHG: stock - 支持交易
510300.XSHG: etf - 支持交易
160105: lof - 支持交易
000001.OF: fund_of - 已识别(暂不支持交易)
IF2312.CCFX: future_ccfx - 已识别(暂不支持交易)
000300.XSHG: index - 已识别(暂不支持交易)
```

## 已知边界

### 边界1: ETF/LOF数据源重叠
- 问题：LOF代码（16xxxx）与ETF代码模式重叠，market_api.py可能误判为ETF
- 影响：LOF分钟数据可能调用fund_etf_hist_min_em而非LOF专用接口
- 建议：market_api.py增加LOF专用判断逻辑，对接fund_lof_hist_em

### 边界2: 场外基金无二级市场交易
- 问题：OF为申购赎回机制，非二级市场交易，Backtrader broker无法直接处理
- 影响：OF策略只能做净值跟踪，无法做交易回测
- 建议：设计专门的OF申赎模拟机制（净值计算+申赎费用）

### 边界3: 期货保证金机制缺失
- 问题：Backtrader默认broker为股票现货，无保证金、杠杆概念
- 影响：期货策略无法模拟真实盈亏（保证金占用、强平风险）
- 建议：实现期货专用broker或position管理逻辑

### 边界4: 期货合约信息缺失
- 问题：缺少合约乘数、保证金比例、交割日期等元数据
- 影响：无法计算真实盈亏、无法判断主力合约、无法模拟移仓
- 建议：对接AkShare期货元数据接口（futures_contract_detail）

### 边界5: 资产路由器能力声明过于乐观
- 问题：asset_router.py声称ETF/LOF为TradingStatus.SUPPORTED，但LOF实际数据源不完整
- 影响：误导用户认为LOF完全可用
- 建议：LOF状态调整为IDENTIFIED_ONLY直到数据源完善

## 最小可行路径（MVP）

### 已可用的最小路径
| 资产类型 | MVP路径 | 状态 |
|---------|--------|------|
| 股票 | 数据获取 + Backtrader交易 + 绩效分析 | ✅ 完整可用 |
| ETF | 数据获取 + Backtrader交易 + 绩效分析 | ✅ 完整可用 |
| 指数 | 数据获取（基准比较） | ✅ 基准可用 |

### 需补充的最小路径
| 资产类型 | MVP路径 | 需补充项 | 优先级 |
|---------|--------|---------|-------|
| LOF | 数据获取 + Backtrader交易 | market_data/lof.py + LOF专用接口 | P1 |
| OF | 净值获取 + 申赎模拟 | market_data/fund_of.py + 申赎逻辑 | P2 |
| 期货 | 合约数据 + 保证金broker | market_data/future.py + 期货broker | P3 |

### 最小可行路径优先级
1. **P0（已有）**: 股票、ETF完整可用
2. **P1（最易）**: LOF数据对接（AkShare接口已存在）
3. **P2（中等）**: OF净值数据对接 + 简化申赎逻辑
4. **P3（最难）**: 期货数据对接 + 保证金机制

## 多资产推进路线图

### Phase 1: LOF能力补齐（预计工作量：2天）
**目标**: 实现LOF完整数据获取和交易能力

**步骤**:
1. 创建market_data/lof.py，对接AkShare fund_lof_hist_em接口
2. market_api.py增加LOF判断逻辑（区分16开头的LOF与ETF）
3. asset_router.py保持LOF为SUPPORTED状态
4. 编写LOF策略测试样本（LOF轮动/套利）
5. 验证LOF数据获取和交易流程

**验证标准**:
- LOF日线数据可获取（至少3个LOF样本）
- LOF策略可运行并输出净值曲线
- test_lof_strategy.py测试通过

### Phase 2: OF（场外基金）能力补齐（预计工作量：3天）
**目标**: 实现OF净值获取和简化申赎模拟

**步骤**:
1. 创建market_data/fund_of.py，对接fund_open_fund_daily接口
2. 设计OF申赎模拟机制（净值跟踪 + 申赎费用）
3. 实现OFPosition类（申购份额、赎回逻辑）
4. asset_router.py将OF状态调整为SUPPORTED（仅限申赎模拟）
5. 编写OF定投策略样本

**验证标准**:
- OF净值数据可获取（至少3个OF样本）
- OF申赎模拟逻辑正确（申购费用、赎回费用、份额计算）
- test_of_strategy.py测试通过

### Phase 3: 期货基础数据对接（预计工作量：3天）
**目标**: 实现期货合约行情数据获取

**步骤**:
1. 创建market_data/future.py，对接futures_zh_index_sina等接口
2. 创建futures_metadata.py，提供合约乘数、保证金、交割日等元数据
3. 实现get_future_contracts、get_dominant_contract、get_contract_multiplier API
4. asset_router.py保持期货为IDENTIFIED_ONLY
5. 编写期货数据获取测试样本

**验证标准**:
- IF/IC/IH主力合约数据可获取
- 合约元数据（乘数、保证金）可查询
- test_future_data.py测试通过

### Phase 4: 期货交易能力补齐（预计工作量：5天）
**目标**: 实现期货保证金交易模拟

**步骤**:
1. 实现FutureBroker类，支持保证金、杠杆、强平逻辑
2. 实现FuturePosition类，支持多头/空头、持仓管理
3. asset_router.py将期货状态调整为SUPPORTED
4. 编写期货择时策略样本
5. 编写期现套利策略样本

**验证标准**:
- 期货策略可运行并模拟保证金占用
- 强平逻辑正确（保证金不足时强平）
- test_future_strategy.py测试通过

### Phase 5: 多资产组合策略（预计工作量：2天）
**目标**: 实现跨资产类型组合策略

**步骤**:
1. 完善subportfolios.py跨资产资金划转逻辑
2. 编写多资产组合策略样本（股票+ETF+期货）
3. 编写风险平价策略样本
4. 编写资产配置策略样本

**验证标准**:
- 多资产策略可运行
- 子账户资金划转逻辑正确
- test_multi_asset_strategy.py测试通过

## 总结

### 当前可用的资产类型
- ✅ **股票**: 完整可用（数据 + 交易 + 绩效）
- ✅ **ETF**: 完整可用（数据 + 交易 + 绩效）
- ⚠️ **LOF**: 可识别，数据源不完整，建议补齐
- ⚠️ **指数**: 可识别，仅基准比较可用

### 当前不可用的资产类型
- ❌ **场外基金(OF)**: 仅识别，缺净值数据和申赎机制
- ❌ **股指期货(CCFX)**: 仅识别，缺合约数据、保证金机制

### 阻塞点优先级
1. **LOF数据源对接**: 最易解决，AkShare接口已存在
2. **OF净值数据对接**: 中等难度，需设计申赎机制
3. **期货数据对接**: 中等难度，接口存在但需整理元数据
4. **期货保证金机制**: 最难，需重写broker逻辑

### 建议推进顺序
1. **Phase 1 (LOF)**: 2天工作量，快速补齐LOF能力
2. **Phase 2 (OF)**: 3天工作量，补齐OF净值+申赎
3. **Phase 3 (期货数据)**: 3天工作量，先解决数据获取
4. **Phase 4 (期货交易)**: 5天工作量，最后解决交易机制
5. **Phase 5 (多资产)**: 2天工作量，完善组合策略

### 真实阻塞点总结
| 阻塞点 | 影响资产 | 解决难度 | AkShare接口可用性 |
|-------|---------|---------|-----------------|
| LOF数据源未对接 | LOF | 低 | ✅ fund_lof_hist_em可用 |
| OF净值数据未对接 | OF | 中 | ✅ fund_open_fund_daily可用 |
| OF申赎机制未实现 | OF | 中 | ❌ 需自行设计 |
| 期货数据未对接 | 期货 | 中 | ✅ futures_zh_index_sina可用 |
| 期货元数据缺失 | 期货 | 中 | ⚠️ 部分可用 |
| 期货保证金机制未实现 | 期货 | 高 | ❌ 需自行设计 |