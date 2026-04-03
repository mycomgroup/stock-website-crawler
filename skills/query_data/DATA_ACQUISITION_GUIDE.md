# 数据获取指南 (Data Acquisition Guide)

**版本**: 1.0  
**更新日期**: 2026-03-26  
**适用场景**: 港股、A股、美股财务数据获取

---

## 📊 数据源优先级矩阵

### Tier 1 - 主要数据源（优先使用）

| 数据源 | 市场 | 数据类型 | 状态 | 获取方式 |
|--------|------|----------|------|----------|
| **理杏仁API** | A股/港股 | 利润表、估值指标 | ⚠️ 部分免费 | `lixinger-api-docs/scripts/query_tool.py` |
| **AkShare** | A股/港股 | 完整财务报表 | ✅ 免费 | Python直接调用 |
| **Finnhub** | 美股 | 基础财务数据 | ⚠️ 免费版有限制 | API调用 |

### Tier 2 - 备用数据源

| 数据源 | 市场 | 数据类型 | 费用 | 状态 |
|--------|------|----------|------|------|
| **EODHD** | 全球 | 完整财务 | $19/月 | 需要付费 |
| **FMP** | 美股 | 详细财务 | $15/月 | 需要付费 |

### Tier 3 - 手动补充

| 来源 | 用途 | 获取方式 |
|------|------|----------|
| 公司年报 | 完整财务数据 | 官网IR页面下载 |
| 行业协会 | 市场份额 | 购买报告 |

---

## 🔧 标准数据获取流程

### 1. 港股财务数据获取（以泡泡玛特09992为例）

#### 步骤1: 获取利润表（理杏仁API）
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["09992"], "date": "latest", "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.gp_m.t", "q.ps.np_s_r.t"]}' \
  --columns "date,q.ps.toi.t,q.ps.np.t,q.ps.gp_m.t,q.ps.np_s_r.t"
```

**可用指标**:
- `q.ps.toi.t`: 营业收入
- `q.ps.np.t`: 净利润
- `q.ps.gp_m.t`: 毛利率
- `q.ps.np_s_r.t`: 净利率

#### 步骤2: 补充现金流量表和资产负债表（AkShare）
```python
import akshare as ak

# 现金流量表
cf = ak.stock_financial_hk_report_em(stock='09992', symbol='现金流量表')
# 关键字段: 经营业务现金净额

# 资产负债表
bs = ak.stock_financial_hk_report_em(stock='09992', symbol='资产负债表')
# 关键字段: 现金及等价物、存货、总资产、总负债
```

#### 步骤3: 获取股价数据
```python
import akshare as ak

# 历史股价
df = ak.stock_hk_hist(symbol='09992', period='daily', 
                      start_date='20250101', end_date='20260326', adjust='qfq')
```

### 2. 美股财务数据获取（以美泰MAT为例）

#### 方法1: Finnhub API（免费）
```python
import requests

api_key = 'd1iu8mhr01qhbuvsappgd1iu8mhr01qhbuvsapq0'
url = f'https://finnhub.io/api/v1/stock/financials-reported?symbol=MAT&token={api_key}&freq=annual'

resp = requests.get(url)
data = resp.json()
# 解析利润表数据
```

**优点**: 真实SEC数据，免费  
**缺点**: 只提供基础字段，格式较复杂

#### 方法2: EODHD API（付费）
```bash
curl "https://eodhd.com/api/fundamentals/MAT.US?api_token=YOUR_TOKEN&fmt=json"
```

**优点**: 数据结构清晰，包含完整财务报表  
**缺点**: 免费版不可用

### 3. A股财务数据获取

```python
import akshare as ak

# 财务分析指标
df = ak.stock_financial_analysis_indicator_em(symbol='002292')  # 奥飞娱乐

# 或者使用理杏仁
curl -s ".../cn/company/fs/non_financial" --params '{"stockCodes": ["002292"]}'
```

---

## 📋 数据字段映射表

### 港股财务数据字段对照

| 财务指标 | 理杏仁字段 | AkShare字段 | 说明 |
|----------|-----------|-------------|------|
| 营业收入 | `q.ps.toi.t` | 利润表查询 | 季度累积 |
| 净利润 | `q.ps.np.t` | 利润表查询 | 季度累积 |
| 毛利率 | `q.ps.gp_m.t` | 需计算 | (毛利/收入)*100 |
| 经营现金流 | ❌ 不支持 | `经营业务现金净额` | 需用AkShare补充 |
| 现金及等价物 | ❌ 不支持 | `现金及等价物` | 需用AkShare补充 |
| 存货 | ❌ 不支持 | `存货` | 需用AkShare补充 |

### 关键计算公式

```python
# 毛利率
gross_margin = (gross_profit / revenue) * 100

# 净利率
net_margin = (net_income / revenue) * 100

# OCF/净利润比率
ocf_to_ni_ratio = operating_cash_flow / net_income

# 自由现金流
fcf = operating_cash_flow - capex

# 资产负债率
debt_ratio = (total_liabilities / total_assets) * 100
```

---

## ⚠️ 常见问题与解决方案

### 问题1: 理杏仁API返回部分字段无效
**现象**: `ValidationError: metricsList contains invalid fields`

**原因**: 港股fs API只支持利润表字段(`q.ps.*`)，不支持资产负债表(`q.bs.*`)和现金流(`q.cf.*`)

**解决**: 使用AkShare补充缺失数据
```python
# 理杏仁获取利润表数据
# AkShare获取现金流和资产负债表数据
```

### 问题2: Finnhub返回403错误
**现象**: `Status: 403 Forbidden`

**原因**: API token无效或超出免费额度

**解决**: 检查.env文件中的FINNHUB_API_KEY
```bash
cat .env | grep FINNHUB
```

### 问题3: AkShare数据格式不匹配
**现象**: `KeyError: 'STD_REPORT_DATE' not in index`

**原因**: 不同数据源返回的DataFrame列名不同

**解决**: 先查看列名
```python
df = ak.stock_financial_hk_report_em(stock='09992', symbol='现金流量表')
print(df.columns.tolist())  # 查看实际列名
# 常见列名: 'REPORT_DATE', 'STD_ITEM_NAME', 'AMOUNT'
```

### 问题4: 美股数据获取失败
**现象**: FMP返回402错误，EODHD返回403

**原因**: 免费版不支持财务报表数据

**解决**: 
1. 使用Finnhub免费版（基础数据）
2. 或升级到付费版（EODHD $19/月，FMP $15/月）
3. 或从公司官网IR页面下载年报手动提取

### 问题5: 数据缺失或不完整
**现象**: 某些字段返回None或0

**原因**: 
- 公司未披露该数据
- 数据时间范围不匹配

**解决**: 
1. 检查数据日期范围
2. 使用多个数据源交叉验证
3. 在分析报告中标注数据缺失

---

## ✅ 数据质量检查清单

获取数据后，必须检查以下项目：

- [ ] **数据完整性**: 所有关键字段是否都有值？
- [ ] **数据合理性**: 数值是否在合理范围内？（如毛利率0-100%）
- [ ] **时间一致性**: 所有数据是否来自同一报告期？
- [ ] **来源标注**: 是否记录了数据来源和日期？
- [ ] **缺失声明**: 如有缺失数据，是否在报告中说明？

---

## 📝 代码模板

### 完整财务数据获取函数

```python
import akshare as ak
import pandas as pd
import json

def get_hk_financial_data(stock_code, year_str='2024-12-31 00:00:00'):
    """
    获取港股完整财务数据
    
    参数:
        stock_code: 股票代码，如 '09992'
        year_str: 报告日期，如 '2024-12-31 00:00:00'
    
    返回:
        dict: 包含完整财务数据的字典
    """
    try:
        # 获取现金流量表
        cf = ak.stock_financial_hk_report_em(stock=stock_code, symbol='现金流量表')
        ocf = cf[(cf['REPORT_DATE'] == year_str) & 
                 (cf['STD_ITEM_NAME'] == '经营业务现金净额')]['AMOUNT']
        
        # 获取资产负债表
        bs = ak.stock_financial_hk_report_em(stock=stock_code, symbol='资产负债表')
        cash = bs[(bs['REPORT_DATE'] == year_str) & 
                  (bs['STD_ITEM_NAME'] == '现金及等价物')]['AMOUNT']
        inventory = bs[(bs['REPORT_DATE'] == year_str) & 
                       (bs['STD_ITEM_NAME'] == '存货')]['AMOUNT']
        
        return {
            'operating_cash_flow': float(ocf.values[0]) if len(ocf) > 0 else None,
            'cash': float(cash.values[0]) if len(cash) > 0 else None,
            'inventory': float(inventory.values[0]) if len(inventory) > 0 else None,
            'data_source': 'AkShare',
            'date': year_str
        }
    except Exception as e:
        print(f'获取失败: {e}')
        return None

def validate_financial_data(data):
    """验证财务数据完整性"""
    required_fields = ['operating_cash_flow', 'cash', 'inventory']
    missing = [f for f in required_fields if data.get(f) is None]
    
    if missing:
        print(f"⚠️ 缺失字段: {missing}")
        return False
    return True
```

---

## 🔐 API Key 配置

确保以下环境变量已配置：

```bash
# 查看当前配置
cat /Users/fengzhi/Downloads/git/lixinger-openapi/.env

# 必需
LIXINGER_TOKEN=xxx
FINNHUB_API_KEY=d1iu8mhr01qhbuvsappgd1iu8mhr01qhbuvsapq0

# 可选（付费）
EODHD_API_KEY=xxx
FMP_API_KEY=xxx
```

---

## 📚 相关文档

- **API关键词索引**: `API_KEYWORD_INDEX.md`
- **理杏仁使用指南**: `lixinger-api-docs/SKILL.md`
- **LLM使用指南**: `LLM_USAGE_GUIDE.md`

---

**维护者**: AI Assistant  
**最后更新**: 2026-03-26  
**更新说明**: 基于泡泡玛特分析经验整理的数据获取最佳实践
