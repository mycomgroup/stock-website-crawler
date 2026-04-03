# 大模型使用指南

本文档专门为大模型（LLM）设计，帮助你高效使用 lixinger-api-docs plugin。

## 🎯 独立运行（重要）

`query_tool.py` 是完全独立的工具：
- ✅ **无需虚拟环境**：直接运行，不需要 `source .venv/bin/activate`
- ✅ **开箱即用**：只需 Python 3.x、所需依赖和 `token.cfg` 文件

**依赖安装**：
```bash
pip install pandas requests duckdb
```

**直接运行示例**：
```bash
# 不需要激活虚拟环境，直接运行
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"fsTableType": "bank"}' \
  --columns "stockCode,name"
```

## 核心原则

### 1. 始终使用增强参数

**不推荐**（返回所有字段，浪费 token）：
```bash
python3 query_tool.py --suffix "cn/company" --params '{"fsTableType": "bank"}'
```

**推荐**（只返回需要的字段）：
```bash
python3 query_tool.py \
  --suffix "cn/company" \
  --params '{"fsTableType": "bank"}' \
  --columns "stockCode,name,ipoDate"
```

### 2. 主动过滤数据

**不推荐**（返回所有数据，再手动筛选）：
```bash
python3 query_tool.py --suffix "cn/company/fundamental/non_financial" --params '{"date": "2024-12-10"}'
```

**推荐**（使用 --row-filter 过滤）：
```bash
python3 query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2024-12-10"}' \
  --row-filter '{"pe_ttm": {">": 10, "<": 20}}' \
  --columns "stockCode,name,pe_ttm"
```

### 3. 处理嵌套数据

**不推荐**（返回嵌套结构，难以处理）：
```bash
python3 query_tool.py --suffix "cn/index/constituents" --params '{"date": "2024-12-10", "stockCodes": ["000016"]}'
```

**推荐**（使用 --flatten 展开）：
```bash
python3 query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date": "2024-12-10", "stockCodes": ["000016"]}' \
  --flatten "constituents" \
  --columns "stockCode"
```

## 调用流程

### 步骤 1：理解用户需求

用户问："查询所有银行股的股票代码和名称"

分析：
- 需要的 API：`cn/company`（股票列表）
- 需要的参数：`fsTableType: bank`（银行股）
- 需要的字段：`stockCode, name`

### 步骤 2：查看 API 文档

打开 `lixinger-api-docs/docs/cn_company.md`，查看：
- 参数表格：了解 `fsTableType` 的用法
- API 试用示例：了解参数格式

### 步骤 3：构造命令

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"fsTableType": "bank"}' \
  --columns "stockCode,name"
```

### 步骤 4：执行并返回结果

输出（CSV 格式）：
```csv
stockCode,name
001227,兰州银行
601825,沪农商行
601528,瑞丰银行
```

## 常见场景

### 场景 1：查询股票列表

```bash
# 查询所有银行股
python3 query_tool.py \
  --suffix "cn/company" \
  --params '{"fsTableType": "bank"}' \
  --columns "stockCode,name"
```

### 场景 2：查询基本面数据

```bash
# 查询特定股票的 PE、PB
python3 query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2024-12-10", "stockCodes": ["600519", "000858"]}' \
  --columns "stockCode,name,pe_ttm,pb"
```

### 场景 3：筛选低估值股票

```bash
# PE < 15 且 PB < 2
python3 query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2024-12-10"}' \
  --row-filter '{"pe_ttm": {"<": 15}, "pb": {"<": 2}}' \
  --columns "stockCode,name,pe_ttm,pb" \
  --limit 20
```

### 场景 4：查询指数成分股

```bash
# 查询上证 50 中以 600 开头的股票
python3 query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date": "2024-12-10", "stockCodes": ["000016"]}' \
  --flatten "constituents" \
  --row-filter '{"stockCode": {"startswith": "600"}}' \
  --columns "stockCode"
```

## 参数构造技巧

### JSON 参数格式

**字符串**：
```json
{"fsTableType": "bank"}
```

**数组**：
```json
{"stockCodes": ["600519", "000858"]}
```

**日期**：
```json
{"date": "2024-12-10"}
```

**布尔值**：
```json
{"includeDelisted": true}
```

**组合**：
```json
{
  "date": "2024-12-10",
  "stockCodes": ["600519"],
  "metricsList": ["pe_ttm", "pb"]
}
```

### 过滤条件格式

**数值比较**：
```json
{"pe_ttm": {">": 10, "<": 20}}
```

**字符串匹配**：
```json
{"stockCode": {"startswith": "600"}}
```

**列表包含**：
```json
{"stockCode": {"in": ["600519", "000858"]}}
```

**多条件组合**：
```json
{
  "pe_ttm": {">": 10, "<": 20},
  "pb": {"<": 3}
}
```

## Token 优化建议

### 1. 使用 CSV 格式（默认）

CSV 比 JSON 节省 30-40% token：
```csv
stockCode,name
600519,贵州茅台
000858,五粮液
```

### 2. 只返回需要的字段

使用 `--columns` 减少无用数据：
```bash
--columns "stockCode,name"  # 只返回 2 个字段
```

### 3. 使用过滤减少数据量

使用 `--row-filter` 只返回符合条件的数据：
```bash
--row-filter '{"pe_ttm": {"<": 20}}'
```

### 4. 控制返回数量

使用 `--limit` 限制行数：
```bash
--limit 50  # 只返回 50 行
```

## 错误处理

### 常见错误 1：JSON 格式错误

**错误**：
```bash
--params '{"date": '2024-12-10'}'  # 内层使用单引号
```

**正确**：
```bash
--params '{"date": "2024-12-10"}'  # 内层使用双引号
```

### 常见错误 2：忘记展开嵌套数组

**错误**：
```bash
# 返回嵌套结构，难以处理
--suffix "cn/index/constituents" --params '...'
```

**正确**：
```bash
# 使用 --flatten 展开
--suffix "cn/index/constituents" --params '...' --flatten "constituents"
```

### 常见错误 3：返回所有字段

**错误**：
```bash
# 返回几十个字段，浪费 token
--suffix "cn/company" --params '...'
```

**正确**：
```bash
# 只返回需要的字段
--suffix "cn/company" --params '...' --columns "stockCode,name"
```

## 检查清单

在执行查询前，确认：

- [ ] 是否使用了 `--columns` 只返回需要的字段？
- [ ] 是否使用了 `--row-filter` 过滤数据？
- [ ] 是否使用了 `--limit` 控制数量？
- [ ] 对于嵌套数据，是否使用了 `--flatten`？
- [ ] JSON 参数格式是否正确（外层单引号，内层双引号）？
- [ ] 是否参考了 API 文档确认参数？

## 总结

**核心要点**：
1. 始终使用 `--columns` 只返回需要的字段
2. 主动使用 `--row-filter` 过滤数据
3. 处理嵌套数据时使用 `--flatten`
4. 参考 `lixinger-api-docs/docs/` 中的 API 文档
5. 默认 CSV 格式最节省 token

**目标**：
- 返回最有用的信息
- 最小化 token 消耗
- 一次生成正确的查询命令
