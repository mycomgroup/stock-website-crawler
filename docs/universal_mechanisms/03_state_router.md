# 状态路由器 (State Router)

## 概述

基于市场广度(沪深300站上MA20比例)和情绪(涨停家数)双重路由，动态调整仓位。

## 机制说明

1. **计算市场广度**：站上MA20的股票占比
2. **计算情绪指标**：涨停家数
3. **根据双重指标判断市场状态**
4. **不同状态对应不同仓位**

## 状态档位

| 市场状态 | 广度阈值 | 情绪阈值 | 仓位 | 持仓数 |
|---------|---------|---------|------|-------|
| 极弱停手 | <15 | <30 | 0% | 0 |
| 底部防守 | 15-25 | 30-50 | 30% | 3 |
| 震荡平衡 | 25-35 | 50-80 | 50% | 5 |
| 趋势正常 | ≥35 | ≥80 | 70% | 7 |
| 强趋势 | ≥40 | ≥80 | 100% | 10 |

## 效果

- 回撤降低：40.1%（37.73% → 21.03%）
- 收益：从亏损转为盈利（+119.5%改善）

## 代码样例

```python
# state_router.py

class StateRouter:
    """状态路由器"""
    
    def __init__(self, index='000300.XSHG', ma_period=20):
        self.index = index
        self.ma_period = ma_period
    
    def calculate_breadth(self, context):
        """计算市场广度"""
        try:
            hs300 = get_index_stocks(self.index)[:300]
            current_data = get_current_data()
            stocks = [s for s in hs300 if s in current_data]
            
            prices = get_price(stocks, end_date=context.previous_date, 
                              fields='close', count=self.ma_period+1, panel=False)
            
            if prices is None:
                return 0.5
            
            price_df = prices.pivot(index='time', columns='code', values='close')
            ma = price_df.iloc[-self.ma_period:].mean()
            current = price_df.iloc[-1]
            
            return (current > ma).mean()
        except:
            return 0.5
    
    def calculate_sentiment(self, context):
        """计算情绪（涨停家数）"""
        try:
            all_stocks = get_all_securities("stock").index.tolist()
            all_stocks = [s for s in all_stocks if s[:2] != "68" and s[0] not in ["4", "8"]]
            
            df = get_price(all_stocks[:500], end_date=context.previous_date, 
                          fields=["close", "high_limit"], count=1, panel=False)
            return len(df[df["close"] >= df["high_limit"] * 0.99])
        except:
            return 50
    
    def route(self, context):
        """路由市场状态"""
        breadth = self.calculate_breadth(context)
        zt_count = self.calculate_sentiment(context)
        
        if breadth < 0.15 or zt_count < 30:
            return 0, "极弱停手"
        elif breadth < 0.25:
            return 0.3, "底部防守"
        elif breadth < 0.35:
            return 0.5, "震荡平衡"
        elif breadth >= 0.40 and zt_count >= 80:
            return 1.0, "强趋势"
        else:
            return 0.7, "趋势正常"


# 使用示例
def initialize(context):
    context.state_router = StateRouter()

def handle_data(context):
    position_ratio, state = context.state_router.route(context)
    log.info(f"市场状态: {state}, 建议仓位: {position_ratio}")
    
    # 根据仓位调整持仓
    target_value = context.portfolio.total_value * position_ratio
    
    for stock in context.portfolio.positions:
        pos = context.portfolio.positions[stock]
        if pos.value > target_value:
            order_target_value(stock, target_value * 0.5)
```

## 适用策略

- ✅ 小市值防守线
- ✅ RFScore（已有类似逻辑）
- ⚠️ 短线策略（可能过度过滤）
