# 数据获取指南

使用 `query_tool.py` 获取 equity-pledge-risk-monitor 所需的数据。

---

## 查询示例

### 查询 Cn.Company.Pledge（股权质押）

**API 路径**: `cn/company/pledge`

**必需参数**:
- `stockCode`: 股票代码
- `startDate`: 起始日期

**查询示例**:

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/pledge" \
  --params '{"stockCode": "600519", "startDate": "2025-01-01", "endDate": "2026-02-26"}' \
  --columns "date,pledgor,pledgee,pledgeAmount,pledgePercentageOfTotalEquity,accumulatedPledgePercentageOfTotalEquity" \
  --limit 20
```

**常用字段**:
- `date`: 数据时间
- `pledgor`: 出质人
- `pledgee`: 质权人
- `pledgeAmount`: 质押数量
- `pledgePercentageOfTotalEquity`: 占总股比例
- `accumulatedPledgePercentageOfTotalEquity`: 累计质押占总股比例
- `pledgeStartDate`: 质押起始日
- `pledgeEndDate`: 质押终止日

---

## 参数说明

- `--suffix`: API 路径（使用斜杠格式，如 `cn/company/pledge`）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

- `cn/company/pledge`: 股权质押数据

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../../plugins/query_data/lixinger-api-docs/SKILL.md`

