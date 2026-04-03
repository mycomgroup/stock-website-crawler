# 任务 3: JQ 行情 API 兼容层 - 完成报告

**执行时间**: 2026-03-30

---

## 1. 修改的文件

| 文件 | 操作 | 说明 |
|------|------|------|
| `jqdata_akshare_backtrader_utility/market_api.py` | 新建 | 统一行情 API 兼容层核心实现 |
| `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py` | 修改 | 更新 get_price_jq, history, attribute_history, get_bars_jq 使用新兼容层 |
| `jqdata_akshare_backtrader_utility/__init__.py` | 修改 | 导出新模块 |
| `jqdata_akshare_backtrader_utility/asset_router.py` | 修复 | 修复其他 agent 引入的缩进错误 |
| `tests/test_market_api.py` | 新建 | 行情 API 兼容层测试 |
| `tests/test_api_compatibility.py` | 修改 | 修复参数名兼容问题 |

---

## 2. 完成的内容

### 2.1 统一参数签名

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `count` | 历史数据条数 | - |
| `start_date` | 起始日期 'YYYY-MM-DD' | None |
| `end_date` | 结束日期 'YYYY-MM-DD' | None |
| `frequency` | 频率 ('daily', '1m', '5m', '15m', '30m', '60m') | 'daily' |
| `fields` | 字段列表 | None |
| `panel` | 返回格式 (True=dict, False=DataFrame) | True |
| `df` | 是否返回 DataFrame | True |
| `fq/adjust` | 复权方式 ('pre'=前复权, 'post'=后复权, 'none'=不复权) | 'pre'/'qfq' |
| `fill_paused` | 是否填充停牌数据 | True |
| `skip_paused` | 是否跳过停牌数据 | True |

### 2.2 统一返回结构

| 函数 | 单标的返回 | 多标的返回 (panel=True) | 多标的返回 (panel=False) |
|------|-----------|------------------------|-------------------------|
| `get_price` | DataFrame | dict{symbol: DataFrame} | DataFrame (含 code 列) |
| `history` | - | DataFrame (index=日期, columns=股票代码) | dict{symbol: array} (df=False) |
| `attribute_history` | DataFrame (index=日期, columns=字段) | - | dict{field: array} (df=False) |
| `get_bars` | DataFrame | dict{symbol: DataFrame} | - |

### 2.3 高频字段支持

| 字段 | 说明 | 推导方式 |
|------|------|----------|
| `open` | 开盘价 | AkShare 原生 |
| `high` | 最高价 | AkShare 原生 |
| `low` | 最低价 | AkShare 原生 |
| `close` | 收盘价 | AkShare 原生 |
| `volume` | 成交量 | AkShare 原生 |
| `money` | 成交额 | AkShare 原生 |
| `paused` | 停牌状态 (0/1) | volume=0 时为 1 |
| `pre_close` | 前收盘价 | close.shift(1) |
| `high_limit` | 涨停价 | pre_close * (1 + 涨幅比例) |
| `low_limit` | 跌停价 | pre_close * (1 - 跌幅比例) |

### 2.4 涨跌停价计算规则

| 板块 | 涨停比例 | 跌停比例 |
|------|---------|---------|
| 主板 (600xxx, 000xxx) | 10% | 10% |
| 创业板 (300xxx) | 20% | 20% |
| 科创板 (688xxx) | 20% | 20% |
| ST 股 | 5% | 5% |

---

## 3. API 签名详解

### 3.1 get_price

```python
def get_price(
    security,          # str or list - 股票代码
    start_date=None,   # str - 起始日期 'YYYY-MM-DD'
    end_date=None,     # str - 结束日期 'YYYY-MM-DD'
    frequency='daily', # str - 频率
    fields=None,       # list - 字段列表
    skip_paused=True,  # bool - 是否跳过停牌
    fq='pre',          # str - 复权方式
    count=None,        # int - 历史数据条数
    panel=True,        # bool - 返回格式
    fill_paused=True,  # bool - 是否填充停牌
):
    """
    获取历史行情数据（聚宽风格）
    
    返回:
        单标的: DataFrame
        多标的 panel=True: dict{symbol: DataFrame}
        多标的 panel=False: DataFrame (含 code 列，可直接 pivot)
    """
```

### 3.2 history

```python
def history(
    count,              # int - 历史数据条数
    unit='1d',          # str - 时间单位
    field='close',      # str - 字段名
    security_list=None, # list - 股票代码列表
    df=True,            # bool - 是否返回 DataFrame
    skip_paused=True,   # bool - 是否跳过停牌
    fq='pre',           # str - 复权方式
    end_date=None,      # str - 结束日期
):
    """
    获取多个标的单个字段的历史数据
    
    返回:
        df=True: DataFrame(index=日期, columns=股票代码)
        df=False: dict{symbol: array}
    """
```

### 3.3 attribute_history

```python
def attribute_history(
    security,       # str - 股票代码
    count,          # int - 历史数据条数
    unit='1d',      # str - 时间单位
    fields=None,    # list - 字段列表
    skip_paused=True, # bool - 是否跳过停牌
    df=True,        # bool - 是否返回 DataFrame
    fq='pre',       # str - 复权方式
    end_date=None,  # str - 结束日期
):
    """
    获取单个标的多字段历史数据
    
    返回:
        df=True: DataFrame(index=日期, columns=字段)
        df=False: dict{field: array}
    """
```

### 3.4 get_bars

```python
def get_bars(
    security,       # str or list - 股票代码
    count,          # int - 历史数据条数
    unit='1d',      # str - 时间单位
    fields=None,    # list - 字段列表
    include_now=False, # bool - 是否包含当前 bar
    end_dt=None,    # datetime - 结束时间
    fq='pre',       # str - 复权方式
    skip_paused=False, # bool - 是否跳过停牌
):
    """
    获取历史 K 线数据
    
    返回:
        DataFrame
    """
```

---

## 4. 测试验证

### 4.1 测试覆盖范围

| 测试类 | 测试内容 |
|--------|----------|
| `TestGetPriceSignature` | 参数签名测试 |
| `TestGetPriceReturnStructure` | 返回结构测试 |
| `TestHighFrequencyFields` | 高频字段测试 (paused, pre_close, high_limit, low_limit) |
| `TestHistorySignature` | history 参数签名测试 |
| `TestAttributeHistorySignature` | attribute_history 参数签名测试 |
| `TestGetBarsSignature` | get_bars 参数签名测试 |
| `TestPanelParameter` | panel 参数行为测试 |
| `TestLimitPriceCalculation` | 涨跌停价计算测试 |
| `TestCodeFormatCompatibility` | 代码格式兼容性测试 |
| `TestIntegrationWithBacktraderBaseStrategy` | 集成测试 |

### 4.2 验证命令

```bash
# 运行行情 API 测试
python3 -m pytest tests/test_market_api.py -v

# 运行兼容性测试
python3 -m pytest tests/test_api_compatibility.py -v -k "GetPrice or GetBars"
```

### 4.3 测试结果

```
tests/test_market_api.py::TestGetPriceSignature::test_required_params_only PASSED
tests/test_market_api.py::TestGetPriceSignature::test_count_param PASSED
tests/test_market_api.py::TestGetPriceSignature::test_fields_param PASSED
tests/test_market_api.py::TestGetPriceSignature::test_fq_param PASSED
tests/test_market_api.py::TestGetPriceSignature::test_frequency_param PASSED
tests/test_market_api.py::TestGetPriceReturnStructure::test_single_security_returns_dataframe PASSED
tests/test_market_api.py::TestGetPriceReturnStructure::test_multiple_securities_returns_dict PASSED
tests/test_market_api.py::TestGetPriceReturnStructure::test_panel_false_returns_dataframe PASSED
tests/test_market_api.py::TestGetPriceReturnStructure::test_dataframe_has_datetime_column PASSED
tests/test_market_api.py::TestHighFrequencyFields::test_paused_field PASSED
tests/test_market_api.py::TestHighFrequencyFields::test_pre_close_field PASSED
tests/test_market_api.py::TestHighFrequencyFields::test_high_limit_field PASSED
tests/test_market_api.py::TestHighFrequencyFields::test_low_limit_field PASSED
tests/test_market_api.py::TestHighFrequencyFields::test_all_high_frequency_fields PASSED
tests/test_market_api.py::TestHistorySignature::test_basic_params PASSED
tests/test_market_api.py::TestHistorySignature::test_df_false PASSED
tests/test_market_api.py::TestHistorySignature::test_end_date_param PASSED
tests/test_market_api.py::TestAttributeHistorySignature::test_basic_params PASSED
tests/test_market_api.py::TestAttributeHistorySignature::test_df_false PASSED
tests/test_market_api.py::TestAttributeHistorySignature::test_high_frequency_fields PASSED
tests/test_market_api.py::TestGetBarsSignature::test_daily_bars PASSED
tests/test_market_api.py::TestGetBarsSignature::test_fields_param PASSED
tests/test_market_api.py::TestGetBarsSignature::test_end_dt_param PASSED
tests/test_market_api.py::TestPanelParameter::test_panel_true_returns_dict PASSED
tests/test_market_api.py::TestPanelParameter::test_panel_false_can_pivot PASSED
tests/test_market_api.py::TestLimitPriceCalculation::test_mainboard_limit_ratio PASSED
tests/test_market_api.py::TestLimitPriceCalculation::test_gem_limit_ratio PASSED
tests/test_market_api.py::TestCodeFormatCompatibility::test_jq_format PASSED
tests/test_market_api.py::TestCodeFormatCompatibility::test_sh_prefix PASSED
tests/test_market_api.py::TestCodeFormatCompatibility::test_pure_code PASSED
tests/test_market_api.py::TestIntegrationWithBacktraderBaseStrategy::test_get_price_jq_unified PASSED
tests/test_market_api.py::TestIntegrationWithBacktraderBaseStrategy::test_history_unified PASSED
tests/test_market_api.py::TestIntegrationWithBacktraderBaseStrategy::test_attribute_history_unified PASSED
tests/test_market_api.py::TestIntegrationWithBacktraderBaseStrategy::test_get_bars_jq_unified PASSED

======================== 34 passed ========================
```

---

## 5. 使用示例

### 5.1 单标的日线

```python
from jqdata_akshare_backtrader_utility import get_price

df = get_price('600519.XSHG', start_date='2023-01-01', end_date='2023-12-31')
```

### 5.2 多标的 count 参数

```python
result = get_price(['600519.XSHG', '000001.XSHE'], end_date='2023-12-31', count=30)
# result: dict{symbol: DataFrame}
```

### 5.3 panel=False 可直接 pivot

```python
df = get_price(['600519.XSHG', '000001.XSHE'], end_date='2023-12-31', count=30, 
               fields=['close'], panel=False)
# df 包含 datetime, close, code 列
pivoted = df.pivot(index='datetime', columns='code', values='close')
```

### 5.4 高频字段

```python
df = get_price('600519.XSHG', start_date='2023-01-01', end_date='2023-01-31',
               fields=['open', 'close', 'paused', 'pre_close', 'high_limit', 'low_limit'])
```

### 5.5 history 多标单字段

```python
from jqdata_akshare_backtrader_utility import history

prices = history(10, '1d', 'close', ['600519.XSHG', '000001.XSHE'])
# prices: DataFrame(index=日期, columns=['600519.XSHG', '000001.XSHE'])
```

### 5.6 attribute_history 单标多字段

```python
from jqdata_akshare_backtrader_utility import attribute_history

df = attribute_history('600519.XSHG', 10, fields=['open', 'close', 'high_limit', 'low_limit'])
```

---

## 6. 已知边界 / 剩余风险

| 风险项 | 说明 | 影响 |
|--------|------|------|
| `paused` 推导 | 通过 volume=0 推导，非实际停牌查询 | 低 |
| ST 涨跌停 | 未实现 ST 列表查询，ST 股涨跌停比例仍按主板计算 | 中 |
| 分钟线高频字段 | 分钟线的 pre_close/high_limit/low_limit 推导可能不准确 | 中 |
| 网络依赖 | 依赖 akshare 获取数据，网络不可用时失败 | 中 |

---

## 7. 最小验证方式

```bash
cd /Users/yuping/Downloads/git/jk2bt-main

python3 -c "
from jqdata_akshare_backtrader_utility import get_price, history, attribute_history

# 单标的测试
df = get_price('600519.XSHG', start_date='2023-01-01', end_date='2023-01-10',
               fields=['open', 'close', 'paused', 'pre_close', 'high_limit', 'low_limit'])
print('单标的测试:')
print(df.head())
print('字段:', list(df.columns))

# 多标的 panel=False 测试
result = get_price(['600519.XSHG', '000001.XSHE'], end_date='2023-12-31', count=5,
                   fields=['close'], panel=False)
print('\n多标的 panel=False:')
print(result.head())

# history 测试
hist = history(5, '1d', 'close', ['600519.XSHG'])
print('\nhistory 测试:')
print(hist)

# attribute_history 测试
attr = attribute_history('600519.XSHG', 5, fields=['open', 'close', 'high_limit'])
print('\nattribute_history 测试:')
print(attr)
"
```

---

## 8. 相关文件索引

| 文件 | 路径 |
|------|------|
| 行情 API 兼容层 | `jqdata_akshare_backtrader_utility/market_api.py` |
| 基础策略类 | `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py` |
| 模块导出 | `jqdata_akshare_backtrader_utility/__init__.py` |
| 测试文件 | `tests/test_market_api.py` |
| 兼容性测试 | `tests/test_api_compatibility.py` |