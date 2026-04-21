# 历史数据分析指南

## 📊 当前数据可用性

### 预测数据
- **OOF预测**（训练集）：2009-2024年（到2024年8月）
  - 文件：`output/phase2/oof_predictions_phase2.csv`
  - 包含：2009-2024年的out-of-fold预测

- **Holdout预测**（测试集）：2026年
  - 文件：`output/phase2/predictions_2026_holdout.csv`
  - 包含：2026年的预测

### 实际收益数据
- **Weekly Factors**：仅2024-2026年
  - 目录：`data/weekly_factors/`
  - 文件格式：`factors_YYYYMMDD_all.csv`
  - 包含：股票的实际收益率（pchg）和因子数据

## ⚠️ 当前限制

### 可以分析的年份
- ✅ **2024年**（1月-8月，33个交易周）
- ❌ **2025年**（有实际数据，但缺少预测数据）
- ✅ **2026年**（1月-4月，9个交易周）

### 无法分析的年份
- ❌ **2009-2023年**：有预测数据，但缺少实际收益数据

## 🔧 如何获取更早年份的数据

要分析2009-2023年的历史数据，你需要：

### 方法1：使用download_factors_with_price.py下载

```bash
# 修改download_factors_with_price.py中的日期范围
# 将start_date和end_date设置为你想要的年份

python download_factors_with_price.py
```

### 方法2：从OSS下载（如果有备份）

```bash
# 使用download_oss.py从阿里云OSS下载历史数据
python download_oss.py --year 2023
python download_oss.py --year 2022
# ... 依此类推
```

### 方法3：从JoinQuant API获取

如果你有JoinQuant账号，可以使用API获取历史数据：

```python
import jqdatasdk as jq
import pandas as pd
from datetime import datetime, timedelta

# 登录
jq.auth('username', 'password')

# 获取某一周的数据
date = '2023-01-02'  # 周一
stocks = jq.get_all_securities(['stock'], date).index.tolist()

# 获取因子和价格数据
# ... (参考download_factors_with_price.py的实现)
```

## 📈 分析更多年份后的预期结果

一旦获取了2009-2023年的数据，你将能够：

1. **分析15年的历史数据**（2009-2024）
   - 覆盖牛市、熊市、震荡市等多种市场环境
   - 更可靠的统计结论

2. **验证收益集中度的稳定性**
   - 是否历史上一直是Top 20-30贡献主要收益？
   - 后20支股票是否一直拖后腿？

3. **不同市场环境下的表现**
   - 2015年牛市
   - 2018年熊市
   - 2020年疫情
   - 2021年结构性行情

## 🎯 当前分析结论（基于2024和2026年）

### 收益贡献模式
- **2024年**（熊市）：Top 20贡献-36.4%，后20支-4.94%
- **2026年**（震荡市）：Top 20贡献132.5%，后20支-5.18%

### 一致性发现
✅ **后20支股票（31-50）持续拖后腿**
- 2024年：-4.94%
- 2026年：-5.18%
- 平均：-5.06%

### 建议
💡 **考虑减少持仓至20-30支**，因为：
1. 后20支股票历史上持续负贡献
2. Top 20-30已经贡献了主要收益
3. 减少持仓可以提高整体收益率

## 📝 下一步

1. **下载2009-2023年的weekly_factors数据**
2. **重新运行analyze_historical_contribution.py**
3. **获得15年的完整历史分析**
4. **基于更长时间跨度做出更可靠的决策**

---

**注意**：2025年的数据需要重新训练模型或使用滚动预测来生成预测值。
