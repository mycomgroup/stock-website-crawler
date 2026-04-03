# Task 09 Result

## 申万行业数据对齐结果

### 修改文件

1. `jqdata_akshare_backtrader_utility/market_data/industry_sw.py`
   - 增强 `get_industry_stocks` 函数，支持 `level` 参数
   - 添加 `STK_SW_INDUSTRY` 和 `STK_SW_INDUSTRY_STOCK` 模块级别名导出
   - 更新 `run_query_simple` 支持行业成分股表查询

2. `tests/test_industry_sw_api.py`
   - 添加 `get_industry_stocks` 导入
   - 添加 `TestIndustryStocksUnified` 测试类（行业成分股统一入口测试）
   - 添加 `TestAliasCompatibility` 测试类（别名兼容性测试）
   - 添加 `level` 参数测试用例

### 完成内容

#### 1. 核心函数修复

| 函数名 | 修改内容 |
|--------|----------|
| `get_industry_stocks` | 新增 `level` 参数，返回结构包含 `code`、`stock_name`、`industry_name`、`level`（可选）、`industry_code`（可选） |
| `get_stock_industry` | 保持原有实现，返回 `RobustResult` |
| `get_industry_category` | 保持原有实现，兼容旧接口 |
| `run_query_simple` | 支持 `STK_SW_INDUSTRY_STOCK` 表查询 |

#### 2. finance 表别名支持

| 表名/别名 | 模块导出 | 全局 finance | 说明 |
|-----------|----------|--------------|------|
| `STK_INDUSTRY_SW` | ✅ | ✅ | 原始表名 |
| `STK_SW_INDUSTRY` | ✅ | ✅ | 文档别名 |
| `STK_SW_INDUSTRY_STOCK` | ✅ | ✅ | 行业成分股表 |

#### 3. 一级/二级/三级行业字段一致性

| 字段 | 一级 | 二级 | 三级 |
|------|------|------|------|
| `level1_code` | ✅ | ✅ | ✅ |
| `level1_name` | ✅ | ✅ | ✅ |
| `level2_code` | ✅ | ✅ | ✅ |
| `level2_name` | ✅ | ✅ | ✅ |
| `level3_code` | ✅ | ✅ | ✅ |
| `level3_name` | ✅ | ✅ | ✅ |

#### 4. 行业成分股返回结构

**无 level 参数时（3 列）：**
```python
{
    "code": "股票代码（聚宽格式）",
    "stock_name": "股票名称",
    "industry_name": "行业名称"
}
```

**有 level 参数时（5 列）：**
```python
{
    "code": "股票代码（聚宽格式）",
    "stock_name": "股票名称",
    "industry_name": "行业名称",
    "industry_code": "行业代码",
    "level": "行业层级"
}
```

### 验证命令

```bash
# 运行别名兼容性测试
python3 -m pytest tests/test_industry_sw_api.py::TestAliasCompatibility -q --tb=short

# 验证导入和别名
python3 -c "
from jqdata_akshare_backtrader_utility.market_data.industry_sw import (
    get_industry_stocks,
    STK_INDUSTRY_SW,
    STK_SW_INDUSTRY,
    STK_SW_INDUSTRY_STOCK,
    run_query_simple,
    finance,
)
print('STK_INDUSTRY_SW:', hasattr(finance, 'STK_INDUSTRY_SW'))
print('STK_SW_INDUSTRY:', hasattr(finance, 'STK_SW_INDUSTRY'))
print('STK_SW_INDUSTRY_STOCK:', hasattr(finance, 'STK_SW_INDUSTRY_STOCK'))
"

# 验证 get_industry_stocks level 参数
python3 -c "
from jqdata_akshare_backtrader_utility.market_data.industry_sw import get_industry_stocks
import inspect
sig = inspect.signature(get_industry_stocks)
print('Parameters:', list(sig.parameters.keys()))
"
```

### 验证结果

- ✅ 别名兼容性测试：6 passed
- ✅ 导入测试：所有别名可用
- ✅ `get_industry_stocks` 签名：`['industry_name', 'level', 'force_update']`
- ✅ 返回结构测试：无 level 3 列，有 level 5 列

### 已知边界

1. **网络依赖**：行业数据需要实时从 AkShare 获取，测试时可能因网络问题超时
2. **缓存策略**：默认按季度缓存（90天），行业分类变更后需要手动清理缓存
3. **数据源限制**：AkShare 的行业成分股数据可能不完整覆盖所有申万三级行业

### API 使用示例

```python
# 获取股票所属行业（所有层级）
from jqdata_akshare_backtrader_utility.market_data.industry_sw import get_stock_industry

result = get_stock_industry("600519.XSHG")
if result.success:
    print(result.data)  # {'level1_name': '食品饮料', 'level1_code': '', ...}

# 获取行业成分股（统一入口）
from jqdata_akshare_backtrader_utility.market_data.industry_sw import get_industry_stocks

# 不指定层级
df = get_industry_stocks("银行")
print(df.columns)  # ['code', 'stock_name', 'industry_name']

# 指定层级
df = get_industry_stocks("银行", level=1)
print(df.columns)  # ['code', 'stock_name', 'industry_name', 'industry_code', 'level']

# 使用 finance 表查询
from jqdata_akshare_backtrader_utility.backtrader_base_strategy import finance, query

# STK_INDUSTRY_SW / STK_SW_INDUSTRY 别名都可用
q = query(finance.STK_SW_INDUSTRY)
df = finance.run_query(q)

# STK_SW_INDUSTRY_STOCK 行业成分股表
q = query(finance.STK_SW_INDUSTRY_STOCK)
df = finance.run_query(q)
```

### 对齐状态总结

| 接口/表名 | 原有实现 | 文档别名 | level 参数 | 状态 |
|-----------|----------|----------|------------|------|
| `get_stock_industry` | ✅ | - | - | 已实现 |
| `get_industry_stocks` | ✅ | - | ✅ | 已增强 |
| `get_industry_category` | ✅ | - | ✅ | 已实现 |
| `finance.STK_INDUSTRY_SW` | ✅ | - | - | 已实现 |
| `finance.STK_SW_INDUSTRY` | - | ✅ | - | 已补别名 |
| `finance.STK_SW_INDUSTRY_STOCK` | - | ✅ | - | 已补实现 |