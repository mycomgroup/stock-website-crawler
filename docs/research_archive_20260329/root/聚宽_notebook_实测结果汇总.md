# 聚宽 Notebook 实测结果汇总

## 测试时间
2026-03-27

## 测试环境
- 平台：聚宽量化研究环境
-  Notebook：test.ipynb
-  连接状态：✅ 正常

---

## 一、因子库测试

### 1.1 聚宽因子库查询
```
聚宽因子总数: 260
因子分类统计:
- quality (质量因子): 71
- basics (基础因子): 37
- emotion (情绪因子): 36
- momentum (动量因子): 34
- style (风格因子): 30
- technical (技术因子): 16
- pershare (每股因子): 15
- risk (风险因子): 12
- growth (成长因子): 9
```

---

## 二、股票过滤测试

### 2.1 股票池过滤
```
全市场股票数量: 5,192
科创板股票数量: 604
180天内新股数量: 41
排除科创板和180天新股后剩余: 4,563
```

### 2.2 过滤逻辑
- 排除科创板（688开头）
- 排除180天内新股
- 剩余为可用于回测的股票池

---

## 三、指数成分测试

### 3.1 主要指数成分股
```
沪深300: 300只
中证500: 500只
创业板50: 50只
```

---

## 四、市场情绪指标测试

### 4.1 市场宽度（MA20）
```
沪深300中13只股收盘价 > MA20 (26.0%)
状态：市场宽度 < 30%，偏底部区域
```

### 4.2 底部特征指标
```
破净占比: 6.28%
（底部信号通常 > 10%，当前接近但未达到）
```

### 4.3 FED指标 & 格雷厄姆指数
```
沪深300 PE中位数: 19.48
盈利收益率(1/PE): 5.13%
FED指标: 3.13 (>0 表示低估)
格雷厄姆指数: 2.56 (>1.5 表示低估)
状态：市场整体估值偏低
```

---

## 五、行业数据测试

### 5.1 申万一级行业
```
申万一级行业数量: 38
前10个行业:
- 国防军工I
- 采掘I
- 家用电器I
- 公用事业I
- 建筑建材I
- 通信I
- 农林牧渔I
- 食品饮料I
- 计算机I
- 有色金属I
```

---

## 六、综合判断

### 6.1 当前市场状态

| 指标 | 数值 | 判断 |
|------|------|------|
| 市场宽度 | 26.0% | 底部区域 (<30%) |
| 破净占比 | 6.28% | 接近底部 (<10%) |
| FED指标 | 3.13 | 低估 (>0) |
| 格雷厄姆指数 | 2.56 | 低估 (>1.5) |

### 6.2 结论

根据2026年3月27日的最新数据测试，市场呈现以下特征：

1. **市场宽度偏低** (26%)：只有26%的沪深300成分股收盘价高于MA20，说明市场整体偏弱
2. **估值偏低**：FED指标为正，格雷厄姆指数2.56（>1.5），显示市场整体估值处于历史低位区间
3. **情绪偏谨慎**：市场宽度不足30%，符合熊市底部特征

**综合判断：市场处于底部偏低估状态，建议关注但不建议立即重仓**

---

## 七、代码片段总结

### 7.1 因子库查询
```python
from jqfactor import get_all_factors
all_factors = get_all_factors()
```

### 7.2 股票过滤
```python
from jqdata import *
from datetime import datetime, timedelta

df = get_all_securities(types=['stock'], date=datetime.now().date())
kcb = list(df[df.index.str.startswith('688')].index.unique())
start_date = (datetime.now() - timedelta(days=180)).date()
df_new = df[df['start_date'] > start_date]
remaining = set(df.index) - set(df_new.index) - set(kcb)
```

### 7.3 FED指标计算
```python
hs300 = get_index_stocks("000300.XSHG")
pe_data = get_fundamentals(query(valuation.pe_ratio).filter(valuation.code.in_(hs300)), date=end_date)
pe_median = pe_data["pe_ratio"].median()
earnings_yield = 100 / pe_median
fed = earnings_yield - bond_yield
graham = earnings_yield / bond_yield
```

---

## 测试结论

1. ✅ 聚宽平台连接正常
2. ✅ 因子库API正常工作 (260个因子)
3. ✅ 股票过滤功能正常
4. ✅ 市场情绪指标计算正常
5. ✅ 行业数据获取正常

所有核心功能测试通过，可以继续使用这些notebook进行策略研究。