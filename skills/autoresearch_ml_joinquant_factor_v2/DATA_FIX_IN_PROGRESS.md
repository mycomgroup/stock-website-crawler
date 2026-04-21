# 数据修复进行中

## 当前状态
正在修复DuckDB中2026年2月-3月的0值价格数据。

## 已完成的步骤

### 1. 删除0值数据 ✅
- 删除了 **75,944条** 0值记录
- 涉及日期：2026-02-09 到 2026-03-09

### 2. 重新下载数据 🔄 进行中
- 脚本：`fix_and_redownload.py`
- 进程ID：查看后台进程
- 预计时间：约15-20分钟

**缺失日期（共15个）：**
- 2026-02-10, 2026-02-11, 2026-02-12, 2026-02-13
- 2026-02-16, 2026-02-17, 2026-02-18, 2026-02-19, 2026-02-20
- 2026-02-23, 2026-02-24, 2026-02-25, 2026-02-26, 2026-02-27
- 2026-03-02

**下载策略：**
- 批量下载：一次请求下载整个时间段（2026-02-10 到 2026-03-02）
- 股票数量：5,201只
- 请求间隔：0.2秒
- 预计总请求数：约5,201次

## 待完成的步骤

### 3. 验证数据修复
修复完成后，运行以下命令验证：

```python
python3 -c "
import duckdb
conn = duckdb.connect('/Users/yuping/Downloads/git/timesfm-cn-forecast-clean/data/market.duckdb', read_only=True)

result = conn.execute('''
    SELECT 
        date,
        COUNT(*) as total,
        COUNT(CASE WHEN close > 0 THEN 1 END) as positive_count,
        COUNT(CASE WHEN close = 0 THEN 1 END) as zero_count
    FROM daily_data 
    WHERE date >= '2026-02-09' AND date <= '2026-03-09'
    GROUP BY date
    ORDER BY date
''').fetchall()

print('日期统计:')
for row in result:
    status = '✅' if row[2] > row[3] else '❌'
    print(f'{row[0]}: {row[1]}只股票, 价格>0={row[2]}, 价格=0={row[3]} {status}')

conn.close()
"
```

### 4. 重新下载周数据
数据修复完成后，重新下载周数据：

```bash
cd skills/autoresearch_ml_joinquant_factor_v2
python3 download_factors_with_price.py weekly 2026-02-02 2026-03-02
```

这将重新生成以下周数据文件：
- `factors_20260202_all.csv`
- `factors_20260209_all.csv`
- `factors_20260223_all.csv`
- `factors_20260302_all.csv`

### 5. 验证周数据
检查pchg是否正常：

```python
import pandas as pd
import numpy as np

files = [
    'data/weekly_factors/factors_20260202_all.csv',
    'data/weekly_factors/factors_20260223_all.csv',
    'data/weekly_factors/factors_20260302_all.csv'
]

for filepath in files:
    df = pd.read_csv(filepath)
    valid_pchg = df['pchg'].notna().sum()
    total = len(df)
    valid_ratio = valid_pchg / total * 100
    
    print(f'{filepath.split("/")[-1]}:')
    print(f'  有效pchg: {valid_pchg}/{total} ({valid_ratio:.1f}%)')
    
    if valid_pchg > 0:
        print(f'  pchg范围: [{df["pchg"].min():.4f}, {df["pchg"].max():.4f}]')
    print()
```

## 检查进度

查看修复脚本的运行状态：

```bash
# 查看进程
ps aux | grep fix_and_redownload

# 查看最新日志（如果有输出到文件）
tail -f fix_and_redownload.log
```

## 问题根源

**DuckDB更新代码的问题：**
`/Users/yuping/Downloads/git/timesfm-cn-forecast-clean/code/duckdb_update.py`

在`convert_row_to_tuple`函数中，当字段缺失时使用0作为默认值：
```python
close_val = float(row.get("close") or row.get("收盘", 0) or 0)
```

**建议长期修复：**
修改代码，对无效数据返回None而不是插入0值：
```python
close_val = row.get("close") or row.get("收盘")
if not close_val or float(close_val) <= 0:
    return None  # 跳过无效数据
```

## 相关文档
- `DUCKDB_ZERO_PRICE_ISSUE.md` - 问题详细分析
- `WEEKLY_DATA_ISSUES_2026.md` - 周数据问题总结
- `fix_and_redownload.py` - 修复脚本
- `download_factors_with_price.py` - 周数据下载脚本（已修复）
