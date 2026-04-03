# 通用机制库 (Universal Mechanisms)

本目录包含可在多个策略间复用的通用机制，帮助同时提升策略表现。

## 目录结构

```
universal_mechanisms/
├── README.md                              # 本文件，索引
├── code/                                  # 代码实现
│   ├── universal_risk_manager.py          # 通用风控管理器
│   ├── emotion_switch.py                  # 情绪开关
│   ├── pause_manager.py                   # 停手机制
│   ├── fscore_selector.py                 # F-Score选股器 (新)
│   ├── diffusion_index.py                 # 扩散指数择时 (新)
│   └── es_risk_parity.py                  # ES风险平价 (新)
│
├── ── 基础风控机制 ──
├── 01_emotion_switch.md                   # 情绪开关 ⭐最通用
├── 02_pause_mechanism.md                  # 停手机制 ⭐高通用
├── 03_state_router.md                     # 状态路由器
├── 04_base_filters.md                     # 基础股票池过滤 ⭐所有策略
├── 05_position_management.md              # 仓位管理
├── 06_exit_rules.md                       # 卖出规则模板
├── 07_attribution.md                      # 归因分析框架
│
├── ── 择时机制 ──
├── 08_rsrs_timing.md                      # RSRS择时 ⭐ETF必备
├── 09_north_money.md                      # 北向资金信号
├── 12_breadth_index.md                    # 扩散指数/市场广度
├── 18_multi_timeframe.md                  # 多周期共振过滤
├── 26_diffusion_index_timing.md           # 微盘扩散指数双均线 ⭐微盘必备 (新)
│
├── ── 风控机制 ──
├── 10_volatility_position.md              # 波动率仓位调整
├── 11_consistency_control.md              # 一致性风控 ⭐微盘必备
├── 15_crowding_detection.md               # 拥挤度检测
├── 16_macro_event_filter.md               # 宏观事件过滤
├── 17_trailing_stop.md                    # 移动止盈止损
├── 19_turnover_filter.md                  # 换手率/波动率过滤
│
├── ── 选股机制 ──
├── 13_sector_rotation.md                  # 行业/主题动量轮动
├── 14_auction_signal.md                   # 集合竞价信号
├── 24_fscore_selection.md                 # F-Score基本面选股 (新)
├── 28_dividend_quality_filter.md          # 高股息质量过滤 (新)
├── 29_mac_momentum_factor.md              # MAC动量因子 (新)
│
├── ── 组合优化 ──
├── 25_epo_portfolio.md                    # EPO增强型组合优化 (新)
├── 27_es_risk_parity.md                   # ES风险平价仓位管理 (新)
│
└── ── 宏观判断 ──
    ├── 20_fed_valuation.md                # FED估值+格雷厄姆指数 ⭐长线必备
    ├── 21_nhnl_indicator.md               # NH-NL净新高占比
    ├── 22_cvix_panic.md                   # C-VIX恐慌指数
    └── 23_bottom_signals.md               # 市场底部特征9项
```

---

## 机制速查表

### 按策略类型推荐

| 策略类型 | 核心机制 | 辅助机制 |
|---------|---------|---------|
| 小市值/微盘 | 01情绪开关 + 26扩散指数 + 11一致性 | 02停手 + 15拥挤度 + 29MAC动量 |
| 首板/二板 | 01情绪开关 + 02停手 + 14集合竞价 | 17移动止损 |
| ETF轮动 | 08RSRS + 13行业轮动 + 25EPO权重 | 09北向资金 + 10波动率仓位 |
| 基本面选股 | 24F-Score + 28高股息 + 29MAC动量 | 08RSRS择时 + 20FED估值 |
| 全天候/多资产 | 27ES风险平价 + 25EPO优化 | 20FED估值 + 08RSRS |
| 价值投资 | 20FED估值 + 28高股息 + 23底部信号 | 08RSRS + 01情绪开关 |

### 按使用频率

| 优先级 | 机制 | 适用范围 |
|--------|------|---------|
| P0 必用 | 01情绪开关、04基础过滤、08RSRS | 几乎所有策略 |
| P1 强推 | 02停手、10波动率仓位、17移动止损 | 大多数策略 |
| P2 推荐 | 11一致性、15拥挤度、26扩散指数 | 小市值/微盘 |
| P3 增强 | 24F-Score、28高股息、29MAC动量 | 基本面策略 |
| P4 高级 | 25EPO、27ES风险平价 | 多资产组合 |

---

## 已有通用机制（基础23项）

### 01. 情绪开关 ⭐最通用

通过市场涨停家数判断整体情绪，低于阈值时停止开仓。

| 策略 | 无开关 | 有开关(≥30) | 改善 |
|------|--------|-------------|------|
| 首板低开 | 年化- | 年化28.4% | 回撤-40% |
| 小市值 | 回撤35.2% | 回撤21.3% | 卡玛+113% |

### 02. 停手机制 ⭐高通用

连续亏损N笔后暂停交易M天，避免情绪失控连续亏损。

| 规则 | 回撤改善 | 卡玛提升 |
|------|---------|---------|
| 连亏3停3（推荐） | -28.4% | +68.6% |

### 08. RSRS择时 ⭐ETF必备

利用最高价/最低价线性回归斜率判断市场阻力支撑强度。

| 策略 | 年化收益 | 最大回撤 |
|------|---------|---------|
| ETF动量+RSRS | 80-150% | 10-15% |

### 11. 一致性风控 ⭐微盘必备

基于市场一致性程度（涨跌幅落在区间的比例）进行风控，极端一致时预警。

### 20. FED估值 ⭐长线必备

FED模型+格雷厄姆指数判断大周期估值顶底，实测2024年FED=3.26%（极度低估）。

---

## 新增通用机制（从聚宽558策略提取）

### 24. F-Score基本面选股

Piotroski 9因子财务健康评分，≥8分为高质量公司。

| 策略 | 年化收益 | 说明 |
|------|---------|------|
| F-Score≥8全市场 | 80%+ | 聚宽回测 |
| FFScore+RSRS | 40-50% | 加入择时后更稳 |

### 25. EPO增强型组合优化

通过收缩相关性矩阵解决MVO过拟合，比等权分配夏普比率提升20-30%。

### 26. 扩散指数双均线择时 ⭐微盘必备

KS指数双均线（EMA6/EMA28）择时，专为微盘股设计，回撤改善38%。

### 27. ES风险平价

基于Expected Shortfall的风险平价，比波动率平价更能捕捉极端风险。

### 28. 高股息质量过滤

近3年累计股息率+PE+PEG+ROE+成长率多维过滤，菜场大妈策略核心机制。

### 29. MAC动量因子

移动均线交叉动量（MAC20/MAC120），比简单N日收益率动量更稳定，12年120倍策略核心。

---

## 待调研机制

从聚宽558策略中识别出以下有价值但尚未文档化的机制：

| 机制 | 来源策略 | 优先级 | 说明 |
|------|---------|--------|------|
| GSISI投资者情绪指数 | 93 国信投资者情绪指数 | P2 | 行业Beta秩相关，信号稳定 |
| 天量卖出机制 | 28 韶华研究之十九 | P2 | 持仓股出现天量时卖出 |
| 财报季空仓 | 多个策略 | P1 | 1月/4月/7月/10月回避财报雷 |
| 涨停打开卖出 | 多个策略 | P1 | 昨日涨停今日打开即卖出 |
| 北向资金持股比 | 51 北上资金持股比 | P3 | 外资持股比例作为选股因子 |
| 缠论笔/线段 | 11 缠论交易策略 | P4 | 技术分析，实现复杂 |
| 海龟突破系统 | 45 海龟突破系统 | P3 | 经典趋势跟踪 |
| 可转债双低轮动 | 86/95 可转债双低 | P2 | 低价格+低溢价率轮动 |
| BOLL择时 | 26 近几年有效的BOLL择时 | P2 | 布林带择时，简单有效 |
| 动量ETF+EPO | 32 EPO优化低相关ETF | P2 | 已有EPO文档，需整合 |

---

## 快速使用

### 组合1：微盘股防守线

```python
from code.emotion_switch import EmotionSwitch
from code.pause_manager import PauseManager
from code.diffusion_index import DiffusionIndexTimer

emotion = EmotionSwitch(threshold=30)
pause = PauseManager(loss_limit=3, pause_days=3)
diffusion = DiffusionIndexTimer(index='000852.XSHG')

def handle_data(context):
    # 三重过滤
    can_trade, zt = emotion.check(context)
    if not can_trade:
        return
    
    should_clear, _ = diffusion.get_timing_signal(context)
    if should_clear:
        # 清仓
        return
    
    if not pause.can_trade():
        return
    
    # 正常选股交易...
```

### 组合2：ETF轮动

```python
from code.universal_risk_manager import UniversalRiskManager

risk_mgr = UniversalRiskManager()  # 包含RSRS+情绪+波动率

def handle_data(context):
    can_trade, info = risk_mgr.pre_trade_check(context)
    if not can_trade:
        return
    position_ratio = info['position_ratio']
    # ETF选股 + EPO权重...
```

### 组合3：基本面价值策略

```python
from code.fscore_selector import FScoreSelector

fscore = FScoreSelector(min_score=8)

def monthly_trade(context):
    # F-Score选股
    stocks = fscore.get_high_score_stocks(context)
    # RSRS择时过滤
    # 高股息过滤
    # 调仓...
```

### 组合4：全天候多资产

```python
from code.es_risk_parity import ESRiskParity

es_rp = ESRiskParity(confidence_level=2.58)

asset_groups = {
    'equity':    ['510300.XSHG'],
    'commodity': ['518880.XSHG'],
    'bond':      ['511010.XSHG'],
    'overseas':  ['513100.XSHG'],
}

def monthly_rebalance(context):
    es_rp.execute_rebalance(context, asset_groups)
```

---

## 更新日志

- 2026-04-03: 新增6项机制（24-29），深化20/23文档，新增3个代码文件，补充待调研清单
- 2026-04-02: 初始版本，包含23种通用机制
