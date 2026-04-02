# 市场底部特征 (9项综合)

## 概述

9个底部信号的满足比例，用于识别极端市场底部。

## 9个信号列表

1. 市场宽度<0.15
2. FED>2%
3. 格雷厄姆>2.0
4. C-VIX>30
5. NH-NL<-30%
6. 拥挤率<15%
7. 两市成交额<5000亿
8. 新股破发率>80%
9. 融资余额下降>30%

## 阈值划分

| 满足项数 | 底部置信度 | 操作建议 |
|----------|------------|----------|
| **≥7项** | 极高置信 | 重仓抄底 |
| **5-6项** | 高置信 | 加仓 |
| **3-4项** | 中等置信 | 试探性建仓 |
| **<3项** | 低置信 | 观望 |

## 代码样例

```python
# bottom_signals.py
import numpy as np

class BottomSignalsChecker:
    """市场底部信号检查器"""
    
    def __init__(self):
        self.signals = [
            ('breadth', 0.15, '<'),    # 市场宽度<0.15
            ('fed', 2.0, '>'),         # FED>2%
            ('graham', 2.0, '>'),      # 格雷厄姆>2.0
            ('cvix', 30, '>'),         # C-VIX>30
            ('nhnl', -30, '<'),        # NH-NL<-30%
            ('crowding', 15, '<'),      # 拥挤率<15%
        ]
    
    def check_breadth(self, context):
        """检查市场宽度"""
        from breadth_index import BreadthIndicator
        breadth = BreadthIndicator()
        data = breadth.calculate_breadth(context)
        return data['breadth'] if data else 0.5
    
    def check_fed(self, context):
        """检查FED"""
        # 需要PE和国债收益率数据
        return 1.5  # 示例返回值
    
    def check_graham(self, context):
        """检查格雷厄姆指数"""
        return 1.5  # 示例返回值
    
    def check_cvix(self, context):
        """检查C-VIX"""
        return 20  # 示例返回值
    
    def check_nhnl(self, context):
        """检查NH-NL"""
        from nhnl_indicator import NHNLIndicator
        nhnl = NHNLIndicator()
        stocks = get_all_securities('stock').index.tolist()
        return nhnl.calculate_nhnl_pct(stocks, context.previous_date)
    
    def check_crowding(self, context):
        """检查拥挤率"""
        from crowding_detection import CrowdingDetector
        crowding = CrowdingDetector()
        data = crowding.calculate_concentration(context)
        return data['concentration'] * 100 if data else 30
    
    def check_all(self, context):
        """检查所有信号"""
        checks = {
            'breadth': self.check_breadth(context),
            'fed': self.check_fed(context),
            'graham': self.check_graham(context),
            'cvix': self.check_cvix(context),
            'nhnl': self.check_nhnl(context),
            'crowding': self.check_crowding(context),
        }
        
        # 满足条件计数
        satisfied = 0
        for signal_name, threshold, direction in self.signals:
            value = checks.get(signal_name, 0)
            if direction == '<':
                if value < threshold:
                    satisfied += 1
            elif direction == '>':
                if value > threshold:
                    satisfied += 1
        
        return satisfied, checks
    
    def get_signal(self, satisfied_count):
        """获取信号"""
        if satisfied_count >= 7:
            return 'EXTREME_BOTTOM', '极高置信,重仓抄底'
        elif satisfied_count >= 5:
            return 'HIGH_BOTTOM', '高置信,加仓'
        elif satisfied_count >= 3:
            return 'MEDIUM_BOTTOM', '中等置信,试探建仓'
        else:
            return 'NOT_BOTTOM', '观望'


# 使用示例
def initialize(context):
    context.bottom_checker = BottomSignalsChecker()

def get_monthly_bottom_check(context):
    satisfied, checks = context.bottom_checker.check_all(context)
    signal, desc = context.bottom_checker.get_signal(satisfied)
    
    log.info(f"底部信号满足: {satisfied}/9项, 信号: {desc}")
    log.info(f"详细: {checks}")
    
    return satisfied, signal
```

## 适用策略

- ✅ 极端底部识别
- ✅ 抄底时机判断
- ✅ 风险预警
