# FED估值指标 + 格雷厄姆指数

## 概述

FED模型和格雷厄姆指数用于判断大周期估值顶底，是长线策略的核心指标。

## 机制说明

1. **FED模型**: 沪深300盈利收益率(1/PE) - 10年期国债收益率
2. **格雷厄姆指数**: 沪深300 PE × 全市场PE / 国债收益率

## 阈值划分

| FED值 | 格雷厄姆值 | 市场状态 | 操作建议 |
|-------|-----------|----------|----------|
| **>2%** | >2.0 | 极低估 | 积极建仓 |
| **1-2%** | 1.5-2.0 | 低估 | 正常配置 |
| **0-1%** | 1.0-1.5 | 合理 | 维持仓位 |
| **<0%** | <1.0 | 高估 | 减仓防御 |

## 代码样例

```python
# fed_valuation.py
import numpy as np

class FEDValuation:
    """FED估值指标"""
    
    def __init__(self):
        self.bond_yield = None  # 10年期国债收益率
    
    def get_fed_value(self, pe_median, bond_yield):
        """计算FED值"""
        # FED = 1/PE - 国债收益率
        earnings_yield = 100 / pe_median  # PE转百分比
        return earnings_yield - bond_yield
    
    def get_graham_index(self, index_pe, market_pe, bond_yield):
        """计算格雷厄姆指数"""
        return (index_pe * market_pe) / bond_yield
    
    def get_market_state(self, fed_value, graham_index):
        """判断市场状态"""
        if fed_value > 2 and graham_index > 2.0:
            return '极低估', 1.2  # 可加仓
        elif fed_value > 1 and graham_index > 1.5:
            return '低估', 1.0
        elif fed_value > 0 and graham_index > 1.0:
            return '合理', 0.8
        else:
            return '高估', 0.5  # 减仓


# 使用示例
def initialize(context):
    context.fed = FEDValuation()

def get_weekly_signal(context):
    # 获取PE数据
    pe_median = get_fundamentals(
        query(indicator.pe).filter(indicator.code == '000300.XSHG'),
        date=context.previous_date
    )['pe'][0]
    
    # 国债收益率（需要数据源）
    bond_yield = 3.0  # 假设值
    
    fed_value = context.fed.get_fed_value(pe_median, bond_yield)
    
    return fed_value
```

## 适用策略

- ✅ RFScore
- ✅ 长线价值策略
- ✅ 大周期择时
