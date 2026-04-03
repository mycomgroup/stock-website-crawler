# Task 03 Result

## 修改文件

- `jqdata_akshare_backtrader_utility/finance_data/dividend.py`
- `jqdata_akshare_backtrader_utility/finance_data/__init__.py`
- `tests/test_dividend_api.py`

## 完成内容

### 1. 字段统一
- 统一分红送股字段名：`bonus_ratio_rmb`（每股派息）、`bonus_share_ratio`（送股比例）、`transfer_ratio`（转增比例）
- 修复 `get_adjust_factor` 使用正确的字段名（之前错误使用了 `bonus_ratio`）
- 修复 `get_rights_issue` 使用正确的字段名并扩充返回字段
- 修复 `get_next_dividend` 使用正确的字段名并扩充返回字段

### 2. Schema 定义
新增常量定义：
- `_RIGHTS_ISSUE_SCHEMA`：配股信息表 schema
- `_NEXT_DIVIDEND_SCHEMA`：下次分红信息表 schema
- `_ADJUST_FACTOR_SCHEMA`：复权因子表 schema（新增字段）

### 3. 表别名兼容
- `FinanceQuery` 类新增 `STK_DIVIDEND_RIGHT` 内嵌类
- `run_query_simple` 支持 `STK_DIVIDEND_RIGHT` 表名查询
- 确保 `STK_XR_XD` 和 `STK_DIVIDEND_RIGHT` 返回一致

### 4. 包级导出
- `__init__.py` 新增导出：`FinanceQuery`, `finance`, `_DIVIDEND_SCHEMA`, `_RIGHTS_ISSUE_SCHEMA`, `_NEXT_DIVIDEND_SCHEMA`, `_ADJUST_FACTOR_SCHEMA`
- 确保 `get_rights_issue`, `get_next_dividend` 可通过包级调用

### 5. 测试补充
- 新增 `TestFinanceQuery.test_stk_xr_xd_and_dividend_right_consistency` 测试
- 新增 `TestPackageLevelExports` 测试类验证包级导出
- 新增 `TestSchemaStability` 测试类验证 schema 字段稳定性
- 新增 `TestAdjustFactorCalculation` 测试类验证复权因子计算稳定性

## 验证命令

```bash
python3 -m pytest tests/test_dividend_api.py -v
```

## 验证结果

- 全部 81 个测试通过
- `STK_XR_XD` 和 `STK_DIVIDEND_RIGHT` 一致性测试通过
- 包级导出测试通过
- Schema 字段稳定性测试通过
- 复权因子计算稳定性测试通过

## 已知边界

1. 配股比例字段 `rights_issue_ratio` 暂不支持，数据源（AkShare）暂无该字段
2. `finance.STK_XR_XD` 在 `backtrader_base_strategy.py` 中已存在，与 `dividend.py` 中 `FinanceQuery` 类的表定义并行
3. 复权因子计算采用聚宽标准公式，与某些第三方数据源的计算可能有微小差异
4. 空表返回时统一使用对应 schema 列定义，保证 DataFrame 结构一致

## 接口对照表

| 聚宽文档表名 | 本模块接口 | 别名支持 |
|---|---|---|
| STK_XR_XD | `get_dividend_info()` | ✓ |
| STK_DIVIDEND_RIGHT | `query_dividend_right()` | ✓ |
| STK_DIVIDEND_INFO | `get_dividend_info()` | ✓ |

## 核心接口函数

```python
# 分红送股信息
get_dividend_info(security, start_date, end_date) -> DataFrame

# 复权因子
get_adjust_factor(symbol, start_date, end_date) -> DataFrame
# 字段: code, ex_dividend_date, adjust_factor, bonus_ratio_rmb, bonus_share_ratio, transfer_ratio

# 配股信息
get_rights_issue(symbol) -> DataFrame
# 字段: code, ex_dividend_date, bonus_ratio_rmb, bonus_share_ratio, transfer_ratio, record_date, rights_issue_ratio

# 下次分红信息
get_next_dividend(symbol) -> DataFrame
# 字段: code, report_date, bonus_ratio_rmb, bonus_share_ratio, transfer_ratio, ex_dividend_date, board_plan_pub_date

# finance.run_query 兼容
finance.run_query(finance.STK_XR_XD)
finance.run_query(finance.STK_DIVIDEND_RIGHT)
```