# DuckDB价格为0问题分析

## 问题发现
在下载2026年周数据时，发现以下日期的pchg计算异常，追查后发现是DuckDB数据库中的价格数据为0。

## 根本原因

### 1. 数据库中的异常数据
DuckDB数据库中以下日期的价格数据**全部或大部分为0**：

| 日期范围 | 状态 | 说明 |
|---------|------|------|
| 2026-02-09 到 2026-02-27 | ❌ 全为0 | 约19天数据异常 |
| 2026-03-02 到 2026-03-09 | ❌ 全为0 | 约8天数据异常 |
| 2026-03-10 之后 | ✅ 正常 | 数据恢复正常 |

具体统计：
```
2026-02-09: 5176只股票, 1693只价格>0, 3483只价格=0 (67.3%为0)
2026-02-10: 5178只股票, 全部价格=0 (100%为0)
2026-02-11: 5177只股票, 全部价格=0 (100%为0)
2026-02-12: 5181只股票, 全部价格=0 (100%为0)
2026-02-13: 5179只股票, 全部价格=0 (100%为0)
2026-02-24: 5179只股票, 全部价格=0 (100%为0)
2026-02-25: 5176只股票, 全部价格=0 (100%为0)
2026-02-26: 5174只股票, 全部价格=0 (100%为0)
2026-02-27: 5174只股票, 全部价格=0 (100%为0)
2026-03-02: 5173只股票, 全部价格=0 (100%为0)
2026-03-03: 5175只股票, 仅3只价格>0 (99.9%为0)
2026-03-04: 5176只股票, 仅3只价格>0 (99.9%为0)
2026-03-05: 5177只股票, 仅3只价格>0 (99.9%为0)
2026-03-06: 5177只股票, 仅3只价格>0 (99.9%为0)
2026-03-09: 5180只股票, 仅3只价格>0 (99.9%为0)
```

### 2. 代码问题分析

#### duckdb_update.py中的问题
在`convert_row_to_tuple`函数中，当字段缺失时使用0作为默认值：

```python
def convert_row_to_tuple(self, row):
    open_val = float(row.get("open") or row.get("开盘", 0) or 0)
    close_val = float(row.get("close") or row.get("收盘", 0) or 0)
    # ... 其他字段类似
```

**问题**：
- 如果akshare返回的数据中价格字段为空字符串`""`，会被转换为0
- 如果CSV解析出错，缺失字段也会被设置为0
- 这导致无效数据被插入数据库，而不是被跳过

#### 更新日志显示的问题
查看update_log发现：
```
2026-02-11更新: before=2026-02-09 -> after=2026-02-10, 新增1行
2026-03-03更新: before=2026-02-10 -> after=2026-03-02, 新增8行
```

**2月10日到3月2日有20天，但只新增了8行数据**，说明：
- 大部分日期没有有效的交易数据（可能是节假日）
- 但数据库中却有这些日期的记录，且价格全为0
- 这些0值记录可能是在某次错误的批量导入时产生的

### 3. akshare数据验证
测试akshare在这些日期返回的数据：

```python
# 测试sz000001在2026-02-13的数据
df = ak.stock_zh_a_daily(symbol='sz000001', start_date='20260210', end_date='20260214', adjust='qfq')
# 返回: 2026-02-13, open=10.96, close=10.91 ✅ 数据正常
```

**结论**：akshare能返回正常数据，问题出在数据库导入/更新过程中。

## 解决方案

### 方案1: 删除0值数据并重新更新（推荐）

1. **删除异常数据**
```sql
DELETE FROM daily_data 
WHERE date >= '2026-02-09' AND date <= '2026-03-09' 
AND close = 0;
```

2. **运行更新脚本**
```bash
cd /Users/yuping/Downloads/git/timesfm-cn-forecast-clean/code
python3 duckdb_update.py
```

### 方案2: 使用修复脚本（已提供）

运行修复脚本：
```bash
cd skills/autoresearch_ml_joinquant_factor_v2
python3 fix_zero_prices.py
```

该脚本会：
1. 自动识别价格异常的日期
2. 删除0值记录
3. 提示运行原始更新脚本重新下载

### 方案3: 改进duckdb_update.py（长期方案）

修改`convert_row_to_tuple`函数，对无效数据返回None而不是插入0值：

```python
def convert_row_to_tuple(self, row):
    try:
        # 获取价格字段
        close_val = row.get("close") or row.get("收盘")
        
        # 如果价格为空或0，返回None（跳过这条记录）
        if not close_val or float(close_val) <= 0:
            return None
        
        # 其他字段类似处理...
        
    except Exception as e:
        logger.error(f"转换数据行失败: {e}")
        return None
```

然后在`parse_csv_and_insert`中过滤掉None值：

```python
for row in reader:
    data_tuple = self.convert_row_to_tuple(row)
    if data_tuple:  # 只添加有效数据
        rows_to_insert.append(data_tuple)
```

## 对周数据的影响

由于这些日期的价格数据为0，导致周收益率计算异常：

| 周一日期 | 问题 | 原因 |
|---------|------|------|
| 20260202 | pchg全为nan | 下周(2026-02-13)价格全为0 |
| 20260223 | pchg全为nan | 本周(2026-02-27)价格全为0 |
| 20260302 | pchg全为nan | 本周(2026-03-06)价格全为0 |

**已修复**：修改了`download_factors_with_price.py`，在计算pchg时过滤掉价格≤0的数据，避免产生错误的计算结果。

## 建议

1. **立即执行**：运行方案1删除0值数据并重新更新
2. **长期改进**：修改duckdb_update.py，避免插入0值数据
3. **数据验证**：在数据导入后增加验证步骤，检查是否有异常的0值
4. **监控告警**：定期检查数据库中是否有新的0值数据出现

## 验证修复

修复后运行以下SQL验证：

```sql
-- 检查是否还有0值数据
SELECT 
    date,
    COUNT(*) as total,
    COUNT(CASE WHEN close = 0 THEN 1 END) as zero_count
FROM daily_data 
WHERE date >= '2026-02-01' AND date < '2026-04-01'
GROUP BY date
HAVING zero_count > 0
ORDER BY date;
```

如果返回空结果，说明修复成功。

## 相关文件

- DuckDB数据库: `/Users/yuping/Downloads/git/timesfm-cn-forecast-clean/data/market.duckdb`
- 更新脚本: `/Users/yuping/Downloads/git/timesfm-cn-forecast-clean/code/duckdb_update.py`
- 修复脚本: `skills/autoresearch_ml_joinquant_factor_v2/fix_zero_prices.py`
- 周数据下载: `skills/autoresearch_ml_joinquant_factor_v2/download_factors_with_price.py`
