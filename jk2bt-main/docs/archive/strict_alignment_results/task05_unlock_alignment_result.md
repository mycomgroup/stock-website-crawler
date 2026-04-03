# Task 05 Result

## 修改文件
- `jqdata_akshare_backtrader_utility/finance_data/unlock.py`
- `jqdata_akshare_backtrader_utility/finance_data/__init__.py`
- `tests/test_unlock_api.py`

## 完成内容

### 1. 补充缺失的表别名和类定义

在 `unlock.py` 的 `FinanceQuery` 类中新增：
- `STK_UNLOCK_DATE` 类（文档别名，与 STK_LOCK_UNLOCK 一致）
- `STK_LOCK_SHARE` 类（限售股份信息表）

### 2. 补充缺失的 query_lock_share 函数

新增函数 `query_lock_share()`：
- 对应 JoinQuant 文档中的 STK_LOCK_SHARE 表
- 返回固定 schema: code, unlock_date, lock_amount, lock_type, shareholder_name, shareholder_type
- 使用 akshare 的 `stock_restricted_release_queue_sina` 和 `stock_restricted_release_summary_em` 接口
- 支持缓存机制（7天有效期）
- 代码格式兼容（.XSHG/.XSHE/sh/sz/纯数字）

### 3. 新增辅助函数

- `_parse_lock_share_row()`：解析限售股份信息行（新浪数据源）
- `_parse_lock_share_summary_row()`：解析限售股份汇总信息行（东方财富数据源）

### 4. 定义稳定的 schema

新增 `_LOCK_SHARE_SCHEMA` 常量：
```python
_LOCK_SHARE_SCHEMA = [
    "code",
    "unlock_date",
    "lock_amount",
    "lock_type",
    "shareholder_name",
    "shareholder_type",
]
```

### 5. 更新 run_query 方法

`FinanceQuery.run_query()` 方法现在支持：
- `STK_RESTRICTED_RELEASE`
- `STK_UNLOCK_INFO`
- `STK_LOCK_UNLOCK`
- `STK_UNLOCK_DATE`（新增别名）
- `STK_LOCK_SHARE`（新增）

### 6. 更新模块导出

在 `finance_data/__init__.py` 中导出：
- `query_lock_share`（新增）

### 7. 增强测试覆盖

在 `test_unlock_api.py` 中新增测试：
- `TestFinanceQuery.test_stk_unlock_date_alias`：测试别名存在性
- `TestFinanceQuery.test_stk_lock_share_table`：测试 STK_LOCK_SHARE 表属性
- `TestQueryLockShare` 类：全面测试 query_lock_share 函数
  - 返回类型验证
  - schema 列验证
  - 多格式兼容测试
  - 空结果 schema 验证
- `TestSchemaDefinition.test_lock_share_schema`：测试 schema 定义

## 验证命令

```bash
python3 -m pytest tests/test_unlock_api.py -v
```

## 验证结果

- 测试数量：89 个测试
- 通过：89 passed
- 失败：0
- 时间：1.97s

所有新增测试通过，原有功能未受影响。

## 已知边界

1. **数据源依赖**：
   - 依赖 akshare 的 `stock_restricted_release_queue_sina` 和 `stock_restricted_release_summary_em` 接口
   - 如果 akshare 接口变更，可能需要调整解析逻辑

2. **历史数据完整性**：
   - akshare 提供的解禁数据可能不如 JoinQuant 原始数据完整
   - 部分字段可能缺失（如 unlock_market_value）

3. **预计解禁 vs 实际解禁**：
   - 当前实现使用统一的 schema 覆盖两种场景
   - 预计解禁和实际解禁的区别主要通过 unlock_type 字段体现
   - 如需严格区分，建议在更高层封装时增加过滤逻辑

4. **日期范围查询**：
   - 日期范围过滤在内存中执行（而非数据库层面）
   - 大数据量时性能可能受影响

5. **别名一致性**：
   - `STK_UNLOCK_DATE` 已在 `FinanceQuery` 类和 `backtrader_base_strategy.py` 的 `_FinanceModule` 中同时定义
   - 两个别名指向同一查询逻辑，确保行为一致

## 对齐状态总结

对照清单 `docs/strict_data_api_comparison.md` 中任务 5 的要求：

| 要求项 | 状态 | 说明 |
|--------|------|------|
| `get_unlock_schedule` | ✅ 已实现 | 别名接口，调用 get_unlock |
| `get_unlock_pressure` | ✅ 已实现 | 计算解禁压力指标 |
| `get_unlock_calendar` | ✅ 已实现 | 全市场解禁日历 |
| `get_upcoming_unlocks` | ✅ 已实现 | 即将解禁股票列表 |
| `get_unlock_history` | ✅ 已实现 | 历史解禁记录 |
| `analyze_unlock_impact` | ✅ 已实现 | 解禁影响分析 |
| `finance.STK_LOCK_UNLOCK` | ✅ 已实现 | FinanceQuery 类定义 |
| `finance.STK_LOCK_SHARE` | ✅ 新增实现 | 本次补齐 |
| `finance.STK_UNLOCK_DATE` | ✅ 新增实现 | 本次补齐文档别名 |

**结论**：任务 5 限售解禁数据接口已完全对齐，所有文档别名和核心接口均已实现并验证。