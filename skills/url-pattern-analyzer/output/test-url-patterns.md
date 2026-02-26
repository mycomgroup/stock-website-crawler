# URL模式分析报告

**生成时间**: 2026/2/25 20:58:57

## 统计摘要

- **URL总数**: 8
- **模式数量**: 3
- **平均每模式URL数**: 3

## 模式分布

| 序号 | 模式名称 | URL数量 | 占比 | 路径模板 |
|------|----------|---------|------|----------|
| 1 | api-doc | 4 | 50.0% | `/open/api/doc` |
| 2 | analytics-dashboard | 3 | 37.5% | `/analytics/{param1}/dashboard` |
| 3 | about | 1 | 12.5% | `/about` |

## 模式详情

### 1. api-doc

**路径模板**: `/open/api/doc`

**正则表达式**: `^https://www\.lixinger\.com/open/api/doc\?api-key=([^&]+)$`

**查询参数**: `api-key`

**URL数量**: 4

**示例URL**:

1. `https://www.lixinger.com/open/api/doc?api-key=cn/company`
2. `https://www.lixinger.com/open/api/doc?api-key=hk/index`
3. `https://www.lixinger.com/open/api/doc?api-key=us/stock`
4. `https://www.lixinger.com/open/api/doc?api-key=cn/index`

### 2. analytics-dashboard

**路径模板**: `/analytics/{param1}/dashboard`

**正则表达式**: `^https://www\.lixinger\.com/analytics/([^/]+)/dashboard$`

**URL数量**: 3

**示例URL**:

1. `https://www.lixinger.com/analytics/company/dashboard`
2. `https://www.lixinger.com/analytics/index/dashboard`
3. `https://www.lixinger.com/analytics/stock/dashboard`

### 3. about

**路径模板**: `/about`

**正则表达式**: `https://www\.lixinger\.com/about`

**URL数量**: 1

**示例URL**:

1. `https://www.lixinger.com/about`
