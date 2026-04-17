# Task 29 Result

## 任务目标
补齐股指期货/期货策略真正需要的最小交易模型与合约信息 API。

## 修改文件

### 1. 新增模块
- `jqdata_akshare_backtrader_utility/market_data/futures.py` (798行)
  - 期货数据获取核心模块
  - 支持股指期货 (IF, IC, IH, IM) 和商品期货
  - 包含合约解析、主力合约识别、乘数/保证金信息

### 2. 修改文件
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
  - 在第8节添加期货合约API（2386-2650行之间）
  - 提供JQ风格包装函数

### 3. 新增测试
- `tests/test_futures_api.py` (310行)
  - 23个测试单元，覆盖所有API

## 已实现 API

### 核心API（聚宽风格）

#### 1. `get_future_contracts(product, exchange, date, include_expired)`
**功能**: 获取期货合约列表

**参数**:
- `product`: 产品代码 ('IF', 'IC', 'IH', 'IM', 'AU', 'CU'等)
- `exchange`: 交易所 ('CFFEX', 'SHFE', 'DCE', 'CZCE', 'INE')
- `date`: 查询日期
- `include_expired`: 是否包含已过期合约

**返回**: DataFrame
```python
columns: ['contract', 'product', 'exchange', 'year', 'month', 'is_trading', 'expire_date', 'display_name']
```

**示例**:
```python
df = get_future_contracts(product='IF', date='2023-12-01')
# 返回IF2312, IF2401, IF2403, IF2406等合约
```

#### 2. `get_dominant_contract(product, date)`
**功能**: 获取主力合约

**参数**:
- `product`: 产品代码
- `date`: 查询日期

**返回**: str（主力合约代码）

**示例**:
```python
contract = get_dominant_contract('IF')  # 'IF2604'
contract = get_dominant_contract('IC')  # 'IC2604'
```

#### 3. `get_contract_multiplier(contract_code)`
**功能**: 获取合约乘数

**参数**:
- `contract_code`: 合约代码

**返回**: float（合约乘数）

**示例**:
```python
multiplier = get_contract_multiplier('IF2312')  # 300
multiplier = get_contract_multiplier('IC2401')  # 200
multiplier = get_contract_multiplier('AU2312')  # 1000
```

#### 4. `get_margin_rate(contract_code)`
**功能**: 获取保证金比例

**参数**:
- `contract_code`: 合约代码

**返回**: float（保证金比例）

**示例**:
```python
rate = get_margin_rate('IF2312')  # 0.12 (12%)
rate = get_margin_rate('IC2401')  # 0.14 (14%)
```

#### 5. `calculate_position_value(price, quantity, contract_code)`
**功能**: 计算持仓价值

**参数**:
- `price`: 合约价格
- `quantity`: 持仓手数
- `contract_code`: 合约代码

**返回**: float（持仓价值）

**示例**:
```python
value = calculate_position_value(4000, 10, 'IF2312')
# 价值 = 4000 × 300 × 10 = 12,000,000
```

#### 6. `calculate_required_margin(price, quantity, contract_code)`
**功能**: 计算所需保证金

**参数**:
- `price`: 合约价格
- `quantity`: 持仓手数
- `contract_code`: 合约代码

**返回**: float（所需保证金）

**示例**:
```python
margin = calculate_required_margin(4000, 10, 'IF2312')
# 保证金 = 4000 × 300 × 10 × 0.12 = 1,440,000
```

#### 7. `get_future_daily(contract_code, start_date, end_date)`
**功能**: 获取期货日线数据

**参数**:
- `contract_code`: 合约代码
- `start_date`: 赋值日期
- `end_date`: 结束日期

**返回**: DataFrame
```python
columns: ['datetime', 'open', 'high', 'low', 'close', 'volume', 'openinterest', 'settle']
```

#### 8. `get_future_spot(contract_code)`
**功能**: 获取期货实时行情

**参数**:
- `contract_code`: 合约代码（可选）

**返回**: DataFrame

### 支持的交易所和产品

#### 中金所 (CFFEX)
| 产品 | 名称 | 乘数 | 保证金比例 |
|------|------|------|------------|
| IF | 沪深300股指期货 | 300 | 12% |
| IC | 中证500股指期货 | 200 | 14% |
| IH | 上证50股指期货 | 300 | 12% |
| IM | 中证1000股指期货 | 200 | 14% |
| TS | 2年期国债期货 | 200 | 2% |
| TF | 5年期国债期货 | 10000 | 2% |
| T | 10年期国债期货 | 10000 | 2% |

#### 上期所 (SHFE)
- AU(黄金), AG(白银), CU(铜), AL(铝), ZN(锌), PB(铅), NI(镍), SN(锡)
- SS(不锈钢), RB(螺纹钢), HC(热轧卷板), WR(线材), SP(纸浆)

#### 大商所 (DCE)
- C(玉米), CS(玉米淀粉), A(豆一), B(豆二), M(豆粕), Y(豆油), P(棕榈油)
- L(塑料), V(PVC), PP(聚丙烯), J(焦炭), JM(焦煤), I(铁矿石)

#### 郑商所 (CZCE)
- CF(棉花), SR(白糖), TA(PTA), MA(甲醇), FG(玻璃), RM(菜粕)
- OI(菜油), ZC(动力煤), AP(苹果), CJ(红枣)

#### 能源中心 (INE)
- SC(原油), NR(20号胶)

## 验证样本

### 1. 合约解析验证
```python
parse_future_contract('IF2312')
# {'product': 'IF', 'year': '23', 'month': '12', 'exchange': 'CFFEX', 'full_code': 'IF2312'}
```

### 2. 合约列表验证
```python
df = get_future_contracts(product='IF', date='2023-12-01')
# 返回4个合约: IF2312, IF2401, IF2403, IF2406
```

### 3. 主力合约验证
```python
get_dominant_contract('IF')  # IF2604 (2026年3月30日测试)
get_dominant_contract('IC')  # IC2604
get_dominant_contract('IH')  # IH2604
```

### 4. 合约乘数验证
```python
get_contract_multiplier('IF2312') == 300  ✓
get_contract_multiplier('IC2401') == 200  ✓
get_contract_multiplier('AU2312') == 1000  ✓
```

### 5. 保证金计算验证
```python
# IF2312: 价格4000, 10手
calculate_position_value(4000, 10, 'IF2312') == 12,000,000  ✓
calculate_required_margin(4000, 10, 'IF2312') == 1,440,000  ✓
```

## 验证方式

### 1. 单元测试
- 文件: `tests/test_futures_api.py`
- 23个测试单元，覆盖合约解析、合约列表、主力合约、乘数、保证金、持仓价值等

### 2. 集成测试
- 完整工作流测试: 从获取合约列表 → 主力合约 → 乘数 → 保证金 → 持仓价值计算

### 3. 实时数据验证
- 使用akshare获取实时期货数据
- 主力合约识别基于成交量判断
- 兜底逻辑处理数据异常

## 已知边界

### 1. 数据源限制
- **主力合约识别**: 依赖akshare `futures_zh_spot()` 实时数据
- **历史数据**: akshare `futures_zh_daily_sina()` 数据可能不完整
- **合约详情**: 商品期货的到期日期需要额外查询

### 2. 功能边界
- **交易执行**: 未实现期货撮合系统（仅信息查询）
- **保证金动态调整**: 未实现交易所保证金动态调整逻辑
- **跨期套利**: 未实现跨期合约价差计算
- **结算价**: 部分合约可能缺少结算价数据

### 3. 交易状态
- **asset_router.py**: 期货资产状态为 `IDENTIFIED_ONLY`（已识别，暂不支持交易执行）
- **后续扩展**: 需要实现期货撮合系统才能支持完整交易流程

### 4. 兜底策略
- 主力合约获取失败时，返回最近可交易合约
- 合约乘数/保证金使用静态配置表（交易所官方数据）
- 数据异常时有完整的错误处理和日志记录

## 设计特点

### 1. 最小可运行路径
- **信息查询**: 完整的合约信息API
- **价值计算**: 持仓价值和保证金计算
- **主力识别**: 基于成交量的主力合约识别

### 2. 聚宽API兼容
- 所有API提供 `_jq` 后缀的聚宽风格包装
- 参数命名与聚宽保持一致
- 返回格式符合聚宽规范

### 3. 静态配置表
- 交易所信息 (`CHINA_FUTURE_EXCHANGE_INFO`)
- 合约乘数、保证金比例预配置
- 不依赖外部数据库，离线可用

### 4. 错误处理
- 网络失败时的兜底逻辑
- 数据格式异常的容错处理
- 完整的日志记录

## 后续扩展建议

### 1. 短期扩展
- 实现期货历史分钟数据
- 完善商品期货到期日期计算
- 实现主力合约切换历史查询

### 2. 中期扩展
- 实现期货撮合系统
- 动态保证金调整
- 跨期套利价差计算

### 3. 长期扩展
- 期货风控系统（持仓限额、保证金监控）
- 期权合约支持
- 期货组合策略支持

## 任务总结

✅ **已完成核心目标**:
1. 创建了完整的期货数据获取模块 (`market_data/futures.py`)
2. 实现了6个核心API（合约列表、主力合约、乘数、保证金、持仓价值、保证金计算）
3. 在 `backtrader_base_strategy.py` 中集成了JQ风格包装函数
4. 创建了完整的测试套件（23个测试单元）
5. 验证了所有API在真实数据下的正确性

✅ **建立了最小可运行路径**:
- 期货策略可以通过这些API获取合约信息
- 计算持仓价值和所需保证金
- 确定主力合约进行交易

⏸️ **暂未实现**:
- 完整的期货撮合系统
- 动态保证金调整
- 实际交易执行

📊 **代码统计**:
- 新增代码: ~800行
- 测试代码: ~310行
- API数量: 8个核心函数
- 支持产品: 50+ 期货品种