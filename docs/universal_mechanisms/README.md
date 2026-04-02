# 通用机制库 (Universal Mechanisms)

本目录包含可在多个策略间复用的通用机制，帮助同时提升策略表现。

## 目录结构

```
universal_mechanisms/
├── README.md                    # 本文件，索引
├── 01_rsrs_timing.md           # RSRS择时机制
├── 02_north_money.md           # 北向资金信号机制
├── 03_volatility_position.md    # 波动率仓位调整
├── 04_consistency_control.md    # 一致性风控机制
├── 05_breadth_index.md          # 扩散指数/市场广度
├── 06_sector_rotation.md        # 行业/主题动量轮动
├── 07_auction_signal.md         # 集合竞价信号
├── 08_crowding_detection.md     # 拥挤度检测机制
├── 09_macro_event_filter.md     # 宏观事件过滤
├── 10_trailing_stop.md          # 移动止盈止损
├── 11_multi_timeframe.md        # 多周期共振过滤
├── 12_turnover_filter.md        # 换手率/波动率因子过滤
└── code/
    ├── universal_risk_manager.py # 通用风控管理器
    ├── rsrs_impl.py             # RSRS实现
    ├── emotion_switch.py        # 情绪开关
    └── pause_manager.py         # 停手机制
```

## 机制优先级

| 优先级 | 机制 | 提升潜力 | 实现难度 |
|--------|------|---------|---------|
| P0 | RSRS择时 | ⭐⭐⭐⭐⭐ | 中 |
| P0 | 波动率仓位调整 | ⭐⭐⭐⭐⭐ | 低 |
| P1 | 移动止盈止损 | ⭐⭐⭐⭐ | 低 |
| P1 | 北向资金信号 | ⭐⭐⭐⭐ | 中 |
| P1 | 集合竞价信号 | ⭐⭐⭐⭐ | 中 |
| P2 | 一致性风控 | ⭐⭐⭐ | 中 |
| P2 | 拥挤度检测 | ⭐⭐⭐ | 中 |
| P2 | 行业轮动 | ⭐⭐⭐⭐ | 高 |
| P3 | 宏观事件过滤 | ⭐⭐ | 低 |
| P3 | 多周期共振 | ⭐⭐ | 高 |

## 快速使用

### 组合1：防守线策略（小市值、RFScore）

```python
from universal_risk_manager import UniversalRiskManager

risk_mgr = UniversalRiskManager()

def handle_data(context):
    # 交易前检查
    can_trade, info = risk_mgr.pre_trade_check(context)
    if not can_trade:
        return
    
    # 获取仓位比例
    position_ratio = info['position_ratio']
    
    # 执行选股和交易逻辑
    stocks = select_stocks(context)
    target_count = int(10 * position_ratio)
    # ... 交易逻辑
```

### 组合2：进攻线策略（首板、二板）

```python
from auction_signal import get_auction_signal, filter_auction_stocks
from emotion_switch import check_emotion
from pause_manager import PauseManager

pause_mgr = PauseManager()

def handle_data(context):
    # 情绪检查
    emotion_ok, zt_count = check_emotion(context, threshold=30)
    if not emotion_ok:
        return
    
    # 停机检查
    if not pause_mgr.can_trade():
        return
    
    # 集合竞价选股
    stocks = filter_auction_stocks(context, all_stocks)
    # ... 交易逻辑
```

## 适用策略类型

| 策略类型 | 推荐机制组合 |
|---------|------------|
| 小市值防守 | 情绪开关 + 停手机制 + 状态路由器 + 一致性风控 + 拥挤度检测 |
| 首板低开 | 情绪开关 + 停手机制 + 集合竞价信号 + 移动止盈止损 |
| 二板接力 | 情绪开关 + 停手机制 + 集合竞价信号 + 移动止盈止损 |
| ETF轮动 | RSRS择时 + 北向资金信号 + 波动率仓位 + 行业轮动 |
| 弱转强 | 情绪开关 + 停手机制 + 集合竞价信号 |
| RFScore | 状态路由器 + 波动率仓位 + 停手机制(慎用) |

## 更新日志

- 2026-04-02: 初始版本，包含12种通用机制
