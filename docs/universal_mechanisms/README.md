# 通用机制库 (Universal Mechanisms)

本目录包含可在多个策略间复用的通用机制，帮助同时提升策略表现。

## 目录结构

```
universal_mechanisms/
├── README.md                        # 本文件，索引
├── code/                            # 代码实现
│   ├── universal_risk_manager.py    # 通用风控管理器
│   ├── emotion_switch.py            # 情绪开关
│   └── pause_manager.py             # 停手机制
├── 00_emotion_switch.md             # 情绪开关 ⭐最通用
├── 00_pause_mechanism.md            # 停手机制 ⭐高通用
├── 00_state_router.md               # 状态路由器 ⭐中通用
├── 00_base_filters.md               # 基础股票池过滤 ⭐所有策略通用
├── 00_position_management.md        # 仓位管理 ⭐通用
├── 00_exit_rules.md                 # 卖出规则模板 ⭐通用
├── 00_attribution.md                # 归因分析框架 ⭐研究通用
├── 01_rsrs_timing.md               # RSRS择时机制
├── 02_north_money.md               # 北向资金信号机制
├── 03_volatility_position.md       # 波动率仓位调整
├── 04_consistency_control.md       # 一致性风控机制
├── 05_breadth_index.md             # 扩散指数/市场广度
├── 06_sector_rotation.md           # 行业/主题动量轮动
├── 07_auction_signal.md            # 集合竞价信号
├── 08_crowding_detection.md        # 拥挤度检测机制
├── 09_macro_event_filter.md        # 宏观事件过滤
├── 10_trailing_stop.md             # 移动止盈止损
├── 11_multi_timeframe.md           # 多周期共振过滤
└── 12_turnover_filter.md           # 换手率/波动率因子过滤
```

---

## 已有通用机制（基于原始策略库总结）

### 1. 情绪开关 (Emotion Switch) ⭐最通用

通过市场涨停家数判断整体情绪，低于阈值时停止开仓。

| 策略 | 无开关 | 有开关(≥30) | 改善 |
|------|--------|-------------|------|
| 首板低开 | 年化- | 年化28.4% | 回撤-40% |
| 小市值 | 回撤35.2% | 回撤21.3% | 卡玛+113% |

### 2. 停手机制 (Pause Mechanism) ⭐高通用

连续亏损N笔后暂停交易M天，避免情绪失控连续亏损。

| 规则 | 回撤改善 | 卡玛提升 | 收益影响 |
|------|---------|---------|---------|
| 连亏3停3（推荐） | -28.4% | +68.6% | +20.7% |
| 连亏2停2 | -35% | +45% | -15% |

### 3. 状态路由器 (State Router) ⭐中通用

基于市场广度和情绪双重路由，动态调整仓位。

| 市场状态 | 仓位 | 持仓数 |
|---------|------|-------|
| 极弱停手 | 0% | 0 |
| 底部防守 | 30% | 3 |
| 震荡平衡 | 50% | 5 |
| 趋势正常 | 70% | 7 |
| 强趋势 | 100% | 10 |

### 4. 基础股票池过滤 ⭐所有策略通用

排除科创板、北交所、ST、停牌、次新股。

### 5. 可买入过滤 ⭐交易型策略通用

排除涨停、停牌、ST等无法买入的股票。

### 6. 卖出规则模板 ⭐通用

- 时间退出
- 止盈止损退出
- 移动止盈止损

### 7. 仓位管理 ⭐通用

- 等权分配
- 动态仓位（基于状态）

### 8. 归因分析框架 ⭐研究通用

- 市值归因
- 行业归因
- 风格归因

---

## 新增通用机制（从策略库调研发现）

| 编号 | 机制 | 优先级 |
|------|------|--------|
| 01 | RSRS择时 | P0 |
| 02 | 北向资金信号 | P1 |
| 03 | 波动率仓位调整 | P0 |
| 04 | 一致性风控 | P2 |
| 05 | 市场广度 | P2 |
| 06 | 行业轮动 | P2 |
| 07 | 集合竞价信号 | P1 |
| 08 | 拥挤度检测 | P2 |
| 09 | 宏观事件过滤 | P3 |
| 10 | 移动止盈止损 | P1 |
| 11 | 多周期共振 | P3 |
| 12 | 换手率过滤 | P2 |

---

## 市场综合判断方案（来自完整市场判断方案）

| 编号 | 机制 | 用途 | 优先级 |
|------|------|------|--------|
| 13 | FED估值+格雷厄姆指数 | 大周期顶底 | P1 |
| 14 | NH-NL净新高占比 | 行业顶底 | P2 |
| 15 | C-VIX恐慌指数 | 恐慌程度 | P3 |
| 16 | 市场底部特征9项 | 极端底部 | P2 |

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
