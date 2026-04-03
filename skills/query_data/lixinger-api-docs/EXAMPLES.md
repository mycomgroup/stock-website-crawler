# 理杏仁数据查询示例

本文档包含详细的使用示例和工作流。

## 基础查询示例

### 1. 查询银行股列表
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"fsTableType": "bank"}'
```

### 2. 查询指数基本面数据
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.index.fundamental" \
  --params '{"date": "2024-12-10", "stockCodes": ["000016"], "metricsList": ["pe_ttm.mcw", "mc"]}'
```

### 3. 只返回指定字段
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"fsTableType": "bank"}' \
  --columns "stockCode,name,ipoDate" \
  --limit 5
```

### 4. 使用行过滤（PE 在 10-20 之间）
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.company.fundamental.non_financial" \
  --params '{"date": "2024-12-10"}' \
  --row-filter '{"pe_ttm": {">": 10, "<": 20}}' \
  --columns "stockCode,name,pe_ttm"
```

### 5. 嵌套数组展开（获取指数成分股中以 600 开头的股票）
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.index.constituents" \
  --params '{"date": "2024-12-10", "stockCodes": ["000016"]}' \
  --flatten "constituents" \
  --row-filter '{"stockCode": {"startswith": "600"}}' \
  --columns "stockCode"
```

## 高级工作流

### 工作流 1：分析特定行业的平均估值

**步骤 1：获取行业股票代码**
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"fsTableType": "bank"}' \
  --columns "stockCode" \
  --save-list "bank_stocks"
```

**步骤 2：获取这些股票的基本面数据**
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.company.fundamental.non_financial" \
  --params '{"date": "2024-12-10"}' \
  --use-list "bank_stocks" \
  --columns "stockCode,name,pe_ttm,pb" \
  --format csv > bank_fundamentals.csv
```

**步骤 3：本地计算平均值**
```python
import pandas as pd
df = pd.read_csv('bank_fundamentals.csv')
print(f"平均 PE: {df['pe_ttm'].mean():.2f}")
print(f"平均 PB: {df['pb'].mean():.2f}")
```

### 工作流 2：筛选低估值股票

**获取 PE < 15 且 PB < 2 的股票**
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.company.fundamental.non_financial" \
  --params '{"date": "2024-12-10"}' \
  --row-filter '{"pe_ttm": {"<": 15}, "pb": {"<": 2}}' \
  --columns "stockCode,name,pe_ttm,pb" \
  --format csv > undervalued_stocks.csv
```

### 工作流 3：分析指数成分股分布

**步骤 1：获取上证 50 成分股**
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.index.constituents" \
  --params '{"date": "2024-12-10", "stockCodes": ["000016"]}' \
  --flatten "constituents" \
  --columns "stockCode" \
  --save-list "sh50_constituents"
```

**步骤 2：按交易所分类统计**
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.index.constituents" \
  --params '{"date": "2024-12-10", "stockCodes": ["000016"]}' \
  --flatten "constituents" \
  --columns "stockCode,market" \
  --format csv
```

统计结果：
```python
import pandas as pd
df = pd.read_csv('sh50_constituents.csv')
print(df['market'].value_counts())
```

### 工作流 4：多指数对比分析

**获取多个指数的估值数据**
```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn.index.fundamental" \
  --params '{"date": "2024-12-10", "stockCodes": ["000016", "000300", "000905"], "metricsList": ["pe_ttm.mcw", "pb"]}' \
  --format csv > indices_valuation.csv
```

## 输出格式对比

### CSV 格式（默认，推荐）
```bash
--format csv
```
输出：
```csv
stockCode,name,pe_ttm
600519,贵州茅台,35.2
000858,五粮液,28.5
```

### JSON 格式（适合程序处理）
```bash
--format json
```
输出：
```json
{
  "code": 1,
  "data": [
    {"stockCode": "600519", "name": "贵州茅台", "pe_ttm": 35.2}
  ]
}
```

### Text 格式（表格形式）
```bash
--format text
```
输出：
```
  stockCode  name      pe_ttm
0    600519  贵州茅台    35.2
```

## 过滤操作符完整示例

### 数值比较
```bash
# 等于
--row-filter '{"pe_ttm": {"==": 15}}'

# 不等于
--row-filter '{"pe_ttm": {"!=": 15}}'

# 大于
--row-filter '{"pe_ttm": {">": 10}}'

# 大于等于
--row-filter '{"pe_ttm": {">=": 10}}'

# 小于
--row-filter '{"pe_ttm": {"<": 20}}'

# 小于等于
--row-filter '{"pe_ttm": {"<=": 20}}'

# 范围（组合条件）
--row-filter '{"pe_ttm": {">": 10, "<": 20}}'
```

### 列表操作
```bash
# 在列表中
--row-filter '{"stockCode": {"in": ["600519", "000858", "000333"]}}'

# 不在列表中
--row-filter '{"stockCode": {"not_in": ["600519", "000858"]}}'
```

### 字符串操作
```bash
# 开头匹配
--row-filter '{"stockCode": {"startswith": "600"}}'

# 结尾匹配
--row-filter '{"stockCode": {"endswith": "19"}}'

# 包含
--row-filter '{"name": {"contains": "银行"}}'
```

### 多条件组合
```bash
# 同时满足多个条件（AND）
--row-filter '{"pe_ttm": {">": 10, "<": 20}, "pb": {"<": 3}}'
```

## 常见问题

### Q: 如何处理大量数据？
A: 使用 `--limit` 参数限制返回行数，或使用 `--row-filter` 过滤数据。

### Q: 如何保存查询结果？
A: 使用重定向：`> output.csv` 或 `--save-list` 保存股票代码列表。

### Q: 如何查看所有可用字段？
A: 先不使用 `--columns` 参数查询一次，查看返回的所有字段。

### Q: 缓存如何工作？
A: 默认缓存 1 天，使用 `--no-cache` 禁用缓存。

## 性能优化建议

1. **使用字段过滤**：只请求需要的字段，减少数据传输
2. **使用行过滤**：在服务端过滤数据（如果 API 支持），否则使用 `--row-filter`
3. **使用缓存**：重复查询会使用缓存，加快响应速度
4. **批量查询**：一次查询多个股票代码，而不是多次单独查询
5. **使用会话列表**：保存常用的股票代码列表，避免重复查询
