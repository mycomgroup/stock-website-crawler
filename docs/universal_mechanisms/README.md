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
├── 24_fscore_selection.md                 # F-Score / FFScore基本面选股 (新)
├── 28_dividend_quality_filter.md          # 高股息质量过滤 (新)
├── 29_mac_momentum_factor.md              # MAC动量因子 (新)
│
├── ── 模块库 / 主仓底座 / 流程规范 ──
├── 30_signalmaker_filters.md              # SignalMaker过滤器模块库 ⭐确认层 (新)
├── 31_index_enhancement_base.md           # 指数增强主仓底座 ⭐主仓候选 (新)
├── 32_master_portfolio_assembly.md        # 主仓组合装配图 ⭐统一流程 (新)
├── 33_master_validation_pipeline.md       # 主仓统一验证指标框架 ⭐必跑 (新)
├── 34_alpha_weight_mapping.md             # Alpha到目标权重映射 ⭐执行规范 (新)
├── 35_enhancement_replay_checklist.md     # 验证后增强回放清单 ⭐统一重跑 (新)
├── 36_data_benchmark_cost_spec.md         # 数据/基准/成本统一口径 ⭐对比基线 (新)
├── 37_signal_confirmation_interface.md    # SignalMaker投票/双确认/再进场 ⭐确认接口 (新)
├── 38_strategy_admission_oos.md           # 准入/淘汰/OOS接续标准 ⭐落地门槛 (新)
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
| 基本面选股 | 24F-Score / FFScore + 28高股息 + 29MAC动量 | 08RSRS择时 + 20FED估值 |
| 低频主仓/指数增强 | 31指数增强底座 + 03状态路由 + 24FFScore | 25EPO + 30SignalMaker + 10波动率仓位 |
| 全天候/多资产 | 27ES风险平价 + 25EPO优化 | 20FED估值 + 08RSRS |
| 价值投资 | 20FED估值 + 28高股息 + 23底部信号 | 08RSRS + 01情绪开关 |

### 按使用频率

| 优先级 | 机制 | 适用范围 |
|--------|------|---------|
| P0 必用 | 01情绪开关、04基础过滤、08RSRS | 几乎所有策略 |
| P1 强推 | 03状态路由、10波动率仓位、17移动止损、32主仓装配图、36统一口径 | 主仓统一流程 |
| P2 推荐 | 30SignalMaker过滤器库、33验证框架、34权重映射、35增强回放、37确认接口、38准入/OOS | 主仓增强与复用 |
| P3 增强 | 11一致性、15拥挤度、24F-Score/FFScore、28高股息、29MAC动量 | 分支alpha / 风控增强 |
| P4 高级 | 25EPO、27ES风险平价、31指数增强底座 | 多资产组合 / 主仓工程化 |

### 主仓默认骨架（统一流程）

> 以后任何策略进入正式验证前，默认先映射到这一套装配流程。

```text
04基础过滤
→ Alpha层（24FFScore / 28高股息质量 / 其他候选因子）
→ 03状态路由 / 08RSRS
→ 30SignalMaker二级确认
→ 10波动率仓位缩放
→ 31指数增强底座执行
→ 17退出保护
→ 07归因与统一验证
```

分支说明：
- ETF / 多资产：在权重层优先接 `25EPO` 或 `27ES风险平价`
- 微盘 / 小市值：改走 `26 + 11 + 15 + 29` 分支，不直接套用全局主仓默认骨架
- 事件驱动 / 短线：不纳入主仓默认流，需独立验证后再决定是否接入组合层

### 验证完成后的统一增强闭环

> 新策略第一次验证跑完后，默认必须再走这一遍。

```text
36 统一数据/基准/成本口径
→ 32 主仓装配图分型
→ 37 确认层 / 双确认 / 再进场
→ 34 目标权重映射
→ 31 指数增强底座执行
→ 33 统一验证报告
→ 38 准入 / OOS / 淘汰定档
```

目的：
- 把“单点策略验证”升级成“主仓体系验证”
- 让增强前后具备可比较性
- 让所有策略最终都能被归类和复用

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

## 新增通用机制（补充含 QuantsPlaybook 结论）

### 24. F-Score / FFScore基本面选股

Piotroski 9因子财务健康评分是经典起点，但A股更应优先测试本土化 `FFScore` 版本，而不是默认原始 F-Score 一定占优。

| 策略 | 年化收益 | 说明 |
|------|---------|------|
| F-Score≥8全市场 | 80%+ | 聚宽回测原型 |
| FFScore+RSRS | 40-50% | A股本土化 + 择时后更稳 |

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

### 30. SignalMaker过滤器模块库

`QRS`、鳄鱼线、`AO/MACD`、北向资金分位信号更适合作为过滤器/确认层，而不是直接当成主仓单策略。

### 31. 指数增强主仓底座

月频调仓 + 基准对齐 + 目标权重执行 + 成本统一设置，是当前最像“低频高确定性主仓”的工程底座之一。

### 32. 主仓组合装配图

把 `主路由 / 过滤层 / Alpha层 / 权重层 / 执行层 / 退出层 / 验证层` 收敛成统一流程，要求任何策略先过装配图再进入正式验证。

### 33. 主仓统一验证指标框架

统一 `原策略 / 统一口径版 / 装配增强版 / 完整底座版` 的结果报告，避免只看单一收益图。

### 34. Alpha 到目标权重映射规范

把 `FFScore / RFScore / 红利质量 / 轮动分数` 统一落成标准化 `目标权重表`，让研究层和执行层彻底分离。

### 35. 验证后增强回放清单

规定任何新策略完成第一版验证后，必须再走一次统一增强流程，重新输出增强前后对照报告。

### 36. 数据 / 基准 / 成本统一口径

统一 benchmark、样本切分、真实价格、未来函数规避、手续费与滑点设置，保证增强前后可比较。

### 37. SignalMaker 投票 / 双确认 / 再进场接口

把 `QRS`、鳄鱼线、`AO/MACD`、北向分位信号收敛成统一确认接口，服务于状态升降档与再进场。

### 38. 准入 / 淘汰 / OOS 接续标准

统一定义主仓候选、过滤器候选、战略辅助、OOS观察池与淘汰策略的定档标准。

---

## 还缺的工程化工作（从文档到自动化）

现在 `32~38` 已经把统一增强闭环文档化了，接下来真正还缺的，不再是“再找一个机制”，而是把这些规范变成可复用的自动化组件：

| 工程项 | 优先级 | 说明 |
|------|--------|------|
| 目标权重表导出器 | P1 | 把 `FFScore / RFScore / 红利质量 / 轮动分数` 统一输出成 `34` 规定的标准表 |
| 统一增强回放脚本 | P1 | 新策略验证完成后，自动补跑 `V0 / V1 / V2 / V3` 四版对照 |
| 统一报告生成器 | P1 | 按 `33` 输出收益、回撤、Calmar、换手、成本后结果、样本外、归因 |
| 主仓 OOS 接线 | P1 | 参考 `strategies/secondboard_oos_system`，把 A/B 档策略接入持续监控 |
| SignalMaker 适配器实现 | P2 | 把 `QRS / 鳄鱼线 / AO/MACD / 北向` 统一适配到 `37` 的 `-1/0/1` 接口 |
| 数据代理偏差对照层 | P2 | 把“策略失效”和“代理数据失真”拆开验证，避免误判 |
| 基准与成本配置库 | P2 | 把 `36` 的 benchmark / slippage / commission 变成统一配置模板 |
| 策略准入登记表 | P3 | 把 `38` 的定档结果标准化存档，便于主仓/过滤器/OOS复用 |

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

- 2026-04-03: 新增 `33~38` 六份统一流程规范文档，补齐“验证完成后统一增强再跑一遍”的闭环；同步更新目录、优先级与工程化待办
- 2026-04-03: 新增 `32_master_portfolio_assembly.md`，明确任何策略先过统一装配流程；同步更新默认主仓骨架与分支规则
- 2026-04-03: 补充 `30_signalmaker_filters.md` 与 `31_index_enhancement_base.md`，修正 `24_fscore_selection` 的 FFScore 定位，更新主仓/过滤器分类
- 2026-04-03: 新增6项机制（24-29），深化20/23文档，新增3个代码文件，补充待调研清单
- 2026-04-02: 初始版本，包含23种通用机制
