# 聚宽因子库大规模验证设计文档

> 版本：1.0
> 日期：2026-03-31
> 目标：系统性验证聚宽因子库中所有可用因子的有效性

---

## 一、背景与目标

### 1.1 背景

- 聚宽因子库提供 **260+** 预计算因子
- 包含 **10 个因子类别**
- 另有 **Alpha191 因子**（191个）
- 需要系统性验证，找出真正有效的因子

### 1.2 目标

1. **全量验证**：对所有可用因子做 IC 检验
2. **分类统计**：按类别汇总因子有效性
3. **筛选 Top 因子**：找出 ICIR > 0.5 的有效因子
4. **评估可落地性**：数据稳定性、换手成本、与现有策略相关性

---

## 二、因子库结构

### 2.1 因子分类（260+ 因子）

| 类别 | 数量 | 主要内容 |
|------|------|----------|
| quality (质量) | 71 | 盈利能力、运营效率、财务健康度 |
| basics (基础) | 37 | 财务报表原始数据、TTM指标 |
| emotion (情绪) | 36 | 成交量、换手率、资金流、情绪指标 |
| momentum (动量) | 34 | 价格动量、趋势、乖离率、ROC |
| style (风格) | 30 | Barra风格因子、Beta、流动性 |
| technical (技术) | 16 | 布林线、EMA、MACD、MFI |
| pershare (每股) | 15 | EPS、每股净资产、每股现金流 |
| risk (风险) | 12 | 波动率、偏度、峰度、夏普比率 |
| growth (成长) | 9 | 营收增长率、净利润增长率、PEG |

### 2.2 Alpha191 因子

- 来源：WorldQuant Alpha101 的扩展版本
- 数量：191 个
- 特点：纯量化公式、无基本面依赖
- API：`get_all_alpha_191(date, code, alpha)`

### 2.3 风格因子（Barra CNE5）

| 因子 | 解释 |
|------|------|
| size | 对数市值 |
| beta | CAPM 贝塔 |
| momentum | 相对强弱动量 |
| residual_volatility | 残差波动率 |
| non_linear_size | 市值立方 |
| book_to_price_ratio | 账面市值比 |
| liquidity | 换手率流动性 |
| earnings_yield | 盈利收益率 |
| growth | 成长因子 |
| leverage | 杠杆因子 |

---

## 三、验证方法

### 3.1 IC 检验

```python
# 计算 Rank IC（Spearman）
ic, p_value = spearmanr(factor[common], ret[common])

# 统计指标
ic_mean     # IC 均值
ic_std      # IC 标准差
icir        # IC 均值 / IC 标准差
ic_positive # IC > 0 的比例
```

### 3.2 判断标准

| ICIR | 判断 | 建议 |
|------|------|------|
| ICIR > 0.5 | 有效 | 可工程化 |
| ICIR 0.3-0.5 | 弱有效 | 辅助因子 |
| ICIR 0.1-0.3 | 很弱 | 探索 |
| ICIR < 0.1 | 无效 | 放弃 |

### 3.3 验证参数

| 参数 | 值 | 说明 |
|------|------|------|
| 股票池 | 中证800（前300只） | 控制计算量 |
| 样本区间 | 2022-01-01 ~ 2025-12-31 | 覆盖牛熊 |
| 调仓频率 | 月度 | 标准检验 |
| 因子去极值 | 3σ | MAD方法 |
| 缺失值处理 | 0填充 | 保守估计 |

---

## 四、验证流程

### 4.1 第一轮：全量 IC 检验

```
输入：所有因子 (260 + 191 = 451个)
输出：每个因子的 IC 均值、ICIR、IC>0 比例
```

### 4.2 第二轮：筛选有效因子

```
筛选条件：
- ICIR > 0.3（正向有效）
- ICIR < -0.3（负向有效，可反转）
- IC>0 比例 > 55%（方向稳定）
```

### 4.3 第三轮：相关性分析

```
检验 Top 因子与现有策略的相关性：
- RFScore7
- ETF动量轮动
- 换手率因子
```

### 4.4 第四轮：分层回测

```
对 Top 因子做五分位分层：
- Q1（因子值最低） vs Q5（因子值最高）
- 收益差异 > 0 表示因子正向有效
```

---

## 五、验证代码设计

### 5.1 代码结构

```
verify_factors_full.py
├── 配置区
│   ├── 股票池
│   ├── 时间区间
│   └── 因子列表
├── 因子获取函数
│   ├── get_jq_factor()      # 聚宽因子
│   ├── get_alpha191()       # Alpha191因子
│   └── get_custom_factor()  # 自定义因子
├── IC 计算函数
│   ├── calc_ic()
│   └── calc_ic_series()
├── 主循环
│   ├── 遍历因子类别
│   ├── 计算 IC 序列
│   └── 汇总结果
└── 输出
    ├── 因子有效性排名
    ├── 按类别统计
    └── Top 因子详情
```

### 5.2 关键代码片段

```python
# 获取聚宽因子
def get_jq_factor(stocks, date, factor_name):
    """获取聚宽因子"""
    df = get_factor_values(
        stocks, factor_name, 
        end_date=date, count=1
    )[factor_name].iloc[-1]
    return df.dropna()

# 获取 Alpha191 因子
def get_alpha191_factor(stocks, date, alpha_name):
    """获取 Alpha191 因子"""
    df = get_all_alpha_191(date, code=stocks, alpha=[alpha_name])
    return df[alpha_name].dropna()
```

---

## 六、执行计划

### 6.1 分批执行

由于因子数量较多（451个），建议分批执行：

| 批次 | 因子类别 | 数量 | 执行时间 |
|------|----------|------|----------|
| Batch 1 | quality | 71 | ~5分钟 |
| Batch 2 | basics | 37 | ~3分钟 |
| Batch 3 | emotion | 36 | ~3分钟 |
| Batch 4 | momentum | 34 | ~3分钟 |
| Batch 5 | style + technical | 46 | ~4分钟 |
| Batch 6 | pershare + risk + growth | 36 | ~3分钟 |
| Batch 7 | alpha191 | 191 | ~15分钟 |

### 6.2 总预计时间

- 单批次：3-5 分钟
- 全量验证：~40 分钟
- 建议：分多次运行，避免超时

---

## 七、输出物

### 7.1 因子有效性排名表

| 排名 | 因子名称 | 类别 | IC均值 | ICIR | IC>0 | 判断 |
|------|----------|------|--------|------|------|------|
| 1 | xxx | quality | 0.08 | 0.65 | 72% | 有效 |
| 2 | yyy | emotion | 0.07 | 0.58 | 68% | 有效 |
| ... | ... | ... | ... | ... | ... | ... |

### 7.2 按类别统计

| 类别 | 因子总数 | 有效数(>0.5) | 弱有效(0.3-0.5) | 有效率 |
|------|----------|--------------|-----------------|--------|
| quality | 71 | 5 | 12 | 7.0% |
| emotion | 36 | 3 | 8 | 8.3% |
| ... | ... | ... | ... | ... |

### 7.3 Top 20 因子详情

每个因子的：
- IC 时间序列图
- 五分位分层收益
- 与基准因子的相关性

---

## 八、技术实现

### 8.1 验证代码

```python
# 文件：/tmp/verify_all_factors.py
# 环境：聚宽 Research

from jqdata import *
from jqdatasdk.alpha191 import get_all_alpha_191
import pandas as pd
import numpy as np
from scipy import stats

# 配置
START = "2022-01-01"
END = "2025-12-31"
UNIVERSE = "000906.XSHG"
BATCH_SIZE = 30  # 每批因子数

# 因子列表（按类别）
FACTOR_CATEGORIES = {
    "quality": [...],  # 质量因子列表
    "emotion": [...],  # 情绪因子列表
    "momentum": [...], # 动量因子列表
    ...
}

# 主验证函数
def verify_factors(factor_list, batch_name):
    """批量验证因子"""
    results = []
    for factor_name in factor_list:
        ic_stats = calc_ic_series(factor_name)
        if ic_stats:
            results.append(ic_stats)
    return pd.DataFrame(results)
```

### 8.2 执行命令

```bash
cd /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_notebook

# Batch 1: Quality factors
node run-skill.js \
  --notebook-url "https://www.joinquant.com/user/21333940833/notebooks/test.ipynb" \
  --cell-source "$(cat /tmp/verify_factors_batch1.py)" \
  --timeout-ms 600000
```

---

## 九、预期成果

### 9.1 量化指标

- 验证因子总数：~451个
- 预期有效因子：~20-40个（ICIR > 0.3）
- 可工程化因子：~5-10个（ICIR > 0.5）

### 9.2 最终交付

1. **因子有效性数据库**：所有因子的 IC 统计
2. **Top 因子榜单**：前 20 名有效因子
3. **相关性矩阵**：Top 因子与现有策略的相关性
4. **工程化建议**：每个因子适合接入的母策略

---

## 十、风险与注意事项

### 10.1 潜在问题

| 问题 | 解决方案 |
|------|----------|
| 数据缺失 | 缺失值用 0 填充 |
| 计算超时 | 分批执行 |
| 过拟合 | 样本内验证后做样本外检验 |
| 因子正交性 | 计算相关性矩阵 |

### 10.2 注意事项

1. Alpha191 因子计算复杂，建议单独批次
2. 部分因子有前瞻偏差，需检查数据时间点
3. 行业因子不做验证（分类而非选股）
4. 风格因子主要用于风险归因，不做选股因子验证

---

## 附录

### A. 聚宽因子 API

```python
# 获取所有可用因子
df_factors = get_all_factors()

# 获取因子值
df = get_factor_values(stocks, factors, end_date, count)

# 获取 Alpha191
df = get_all_alpha_191(date, code, alpha)
```

### B. 完整因子列表（待补充）

在验证代码中自动生成完整因子清单。

---

*文档完成*
