# 需求文档

## 简介

autoresearch-guorn-strategy 系统是一个针对果仁网量化交易策略的自动化参数优化框架。它将经过验证的 autoresearch_ricequant-wizard 架构适配到果仁网基于 Node.js 的策略执行基础设施上,通过变异、回测和评分实现策略参数的自主迭代优化。

## 术语表

- **Guorn_Platform**(果仁平台): Guorn.com 量化交易平台,提供基于浏览器的策略回测功能
- **Strategy_Config**(策略配置): 定义果仁策略参数的 JSON 配置(筛选条件、排序规则、股票池、调仓周期)
- **Autoresearch_System**(自动研究系统): 基于 Python 的优化框架,管理迭代参数探索
- **Mutation_Engine**(变异引擎): 通过应用 8 种预定义变异类型生成候选配置的组件
- **Executor**(执行器): 向果仁提交策略配置并获取回测结果的组件
- **Scorer**(评分器): 使用 Calmar、Sortino 和信息比率指标评估回测结果的组件
- **Experiment**(实验): 具有自己的目录、状态和历史记录的命名优化会话
- **Champion_Config**(冠军配置): 实验中当前表现最佳的策略配置
- **Mock_Mode**(模拟模式): 模拟回测而不调用真实果仁 API 的测试模式

## 需求

### 需求 1: 实验初始化

**用户故事:** 作为量化研究员,我希望使用种子策略配置初始化一个新的优化实验,以便开始自动化参数探索。

#### 验收标准

1. 当用户使用实验名称和种子配置运行初始化命令时,自动研究系统应创建实验目录结构
2. 自动研究系统应将种子配置复制到实验目录作为初始冠军配置
3. 自动研究系统应使用种子配置执行基准回测
4. 自动研究系统应在 state.json 中记录基准结果,包含 champion_score、champion_iter 和 current_iter 字段
5. 自动研究系统应在实验目录中初始化 Git 仓库并提交基准
6. 自动研究系统应创建 history/iterations.tsv 文件,包含用于跟踪所有迭代的列标题
7. 自动研究系统应在实验目录中生成 program.md 和 README.md 文档文件

### 需求 2: 策略配置变异

**用户故事:** 作为优化代理,我希望通过智能变异生成候选策略配置,以便系统地探索参数空间。

#### 验收标准

1. 变异引擎应支持 8 种变异类型: add_filter(添加筛选)、remove_filter(移除筛选)、adjust_filter_threshold(调整筛选阈值)、add_ranking(添加排序)、adjust_ranking_weight(调整排序权重)、adjust_holding_num(调整持仓数量)、adjust_rebalance_interval(调整调仓间隔)、change_pool(更换股票池)
2. 当请求变异但未指定类型时,变异引擎应从 8 种可用变异类型中随机选择
3. 当请求变异并指定类型时,变异引擎应仅应用该变异类型
4. 变异引擎应维护一个包含至少 20 个果仁兼容指标的因子候选库
5. 当添加筛选条件时,变异引擎应从未使用的因子中选择并生成适当的操作符和阈值
6. 当调整阈值时,变异引擎应应用 ±20% 到 ±50% 的乘数,同时遵守因子值范围
7. 变异引擎应返回变异后的配置和人类可读的变异描述
8. 变异引擎应防止无效变异(例如,当不存在筛选条件时移除筛选),通过回退到替代变异类型

### 需求 3: 果仁策略执行

**用户故事:** 作为优化系统,我希望以编程方式执行果仁策略回测,以便自动评估候选配置。

#### 验收标准

1. 执行器应与现有 guorn_strategy skill 的 strategy-runner.js 模块集成
2. 当提交回测时,执行器应使用 config-normalizer.js 规范化策略配置
3. 执行器应启动无头浏览器,注入策略配置,并通过 scrat.utility.ajaxDispatch 触发回测
4. 执行器应轮询回测完成状态,可配置超时时间(默认 90 秒)
5. 当回测完成时,执行器应提取摘要指标,包括 annualReturn(年化收益)、maxDrawdown(最大回撤)、winRate(胜率)、informationRatio(信息比率)、avgHoldingDays(平均持仓天数)和 sellCount(卖出次数)
6. 执行器应将完整的回测结果 JSON 保存到实验的历史目录
7. 如果回测超时或失败,执行器应抛出带有诊断信息的适当异常

### 需求 4: 回测结果评分

**用户故事:** 作为优化系统,我希望使用复合评分函数评估回测结果,以便客观地比较策略配置。

#### 验收标准

1. 评分器应计算 Calmar 比率为 annual_return / max(abs(max_drawdown), 0.01)
2. 评分器应计算复合得分为: calmar × 0.55 + sortino × 0.25 + information_ratio × 0.20
3. 评分器应在评分前验证回测状态表明成功完成
4. 评分器应强制执行硬约束: abs(max_drawdown) > 0.35 触发自动回滚
5. 当比较得分时,评分器应要求 new_score 严格大于 champion_score 才做出保留决策
6. 评分器应返回决策("keep"保留 或 "rollback"回滚)和详细原因字符串
7. 评分器应通过可选参数支持可配置的权重和硬约束

### 需求 5: 保留/回滚决策逻辑

**用户故事:** 作为优化系统,我希望自动决定是保留还是回滚候选配置,以便实验收敛到最优参数。

#### 验收标准

1. 当新回测完成时,自动研究系统应计算新配置的得分
2. 如果回测失败或超时,自动研究系统应回滚并增加 consecutive_failures 计数器
3. 如果 abs(max_drawdown) 超过 0.35,自动研究系统应回滚,无论得分如何
4. 如果 new_score 严格大于 champion_score,自动研究系统应保留新配置
5. 当保留时,自动研究系统应更新 wizard_config.json、state.json 冠军字段,并将 consecutive_failures 重置为 0
6. 当回滚时,自动研究系统应从冠军恢复 wizard_config.json,增加 consecutive_failures,并保留 current_iter
7. 自动研究系统应在 history/iterations.tsv 和 history/<iter>.json 中记录决策和原因

### 需求 6: 迭代执行工作流

**用户故事:** 作为优化代理,我希望使用单个命令执行完整的迭代(变异 → 回测 → 评分 → 决策),以便自动化优化循环。

#### 验收标准

1. 自动研究系统应提供 run_iteration.py CLI,接受 --base、--mutation-summary 和可选的 --mutation-type 参数
2. 当 run_iteration.py 执行时,自动研究系统应从实验目录加载当前状态和冠军配置
3. 自动研究系统应使用变异引擎生成候选配置
4. 自动研究系统应通过执行器向果仁提交候选配置
5. 自动研究系统应等待回测完成并获取结果
6. 自动研究系统应计算得分并做出保留/回滚决策
7. 自动研究系统应更新 state.json,保存历史文件,并将更改提交到 Git
8. 自动研究系统应以退出码 0 表示保留,1 表示回滚,2 表示崩溃

### 需求 7: 实验状态管理

**用户故事:** 作为优化系统,我希望在迭代之间维护持久状态,以便实验可以可靠地暂停和恢复。

#### 验收标准

1. 自动研究系统应在 state.json 中存储实验状态,包含字段: strategy_id、champion_score、champion_iter、current_iter、consecutive_failures
2. 当迭代完成时,自动研究系统应原子性地更新 state.json
3. 自动研究系统应维护 history/iterations.tsv,包含制表符分隔的列: iter、timestamp、mutation_summary、decision、score、champion_score、annual_return、max_drawdown、sharpe、sortino、information_ratio
4. 自动研究系统应将每次迭代的配置快照保存为 history/<iter>_config.json
5. 自动研究系统应将每次迭代的完整回测结果保存为 history/<iter>.json
6. 自动研究系统应在每次迭代后使用描述性提交消息将状态更改提交到 Git

### 需求 8: 测试用模拟模式

**用户故事:** 作为开发者,我希望在不进行真实果仁 API 调用的情况下测试优化工作流,以便快速验证系统行为。

#### 验收标准

1. 当 GUORN_MOCK_MODE 环境变量设置为 "1" 时,执行器应跳过真实的浏览器自动化
2. 在模拟模式下,执行器应基于配置复杂度生成模拟回测指标
3. 执行器应模拟真实延迟(配置更新 0.5 秒,回测提交 1 秒,完成 2 秒)
4. 执行器应生成合理范围的指标: annualReturn [0.08, 0.25]、maxDrawdown [0.05, 0.15]、sharpe [1.0, 2.5]
5. 自动研究系统应通过评分和决策管道以相同方式处理模拟结果和真实结果
6. 自动研究系统应为所有模拟操作记录 "[Mock]" 前缀,以区分真实执行

### 需求 9: 因子候选库

**用户故事:** 作为优化系统,我希望访问果仁平台支持的完整指标库,以便变异可以探索多样化的策略维度。

#### 验收标准

1. 变异引擎应基于 `skills/guorn_strategy/GUORN_INDICATORS_CATALOG.md` 维护完整的果仁指标库,包括:
   - **系统函数** (~100+ 函数): 日期回溯(Ref、BarRef、Delta)、时间窗口(MA、EMA、Sum、Max、Min、Stdev等)、时序回归(Forcast、Slope、Neutralize)、K线聚合(KFirst、KLast、KMax)、股票统计(HMax、HMin、HAvg、HRank)、股票池统计(SMax、SMin、SAvg、SRank)、数学函数(abs、ln、sqrt、exp)、逻辑函数(And、Or、Not)、合并函数(IF、Greater、Less)、金叉死叉(crossover、crossunder)、日期统计(CountDays、CountBars、DaysLast)、择时(timing)、条件取值(LastValue)、指标数据(TickerValue、IsNULL)、交易日(DayW、DayM、DayQ)、反身(ticker、industry、sector)、季报(RefQ、TTM、SumQ)、分钟线(Level)等
   - **常用指标**: K线形态(曙光初现、身怀六甲、挽袖线、红三兵、一阳三线、金针探底、两阳夹一阴、假阳线、阳十字星、均线粘合)、技术指标(MACD金叉、MA金叉、KDJ金叉、布林线突破上轨、成交量金叉、RSI、60日乖离率、20日波动率)、行情数据(收盘价、成交金额、日换手率、大单净流入金额、尾盘涨跌幅、股价振幅、总市值、流通市值)、财务指标(市盈率、市净率、每股净资产、净资产收益率、每股收益、每股资本公积金、营业收入增长、营业利润增长)、财报条目(年报审计意见、资产总计、负债合计、营业收入、营业成本、销售费用、净利润、扣非净利润、未分配利润、经营现金流量净额、归属母公司股东权益合计)、公司数据(10大股东持股比例、国家队持股比例、社保持股比例、信托持股比例、龙虎榜标记、未来20日新增流通股数、股权质押比例、预期ST戴帽)、分析师数据(分析师评级分、预期盈利增长率、预期营收增长率、预期目标价、预期目标价变化率、预期净利润变化率、净利润超预期比率)
2. 每个因子条目应包括: name(名称)、expression(表达式)、description(说明)、type(类型,筛选/排序)、operators(操作符,>、<、between)、value_range(值范围)和 default_threshold(默认阈值)
3. 变异引擎应使用参数缓存将因子名称映射到果仁的内部指标 ID
4. 变异引擎应支持从配置文件动态加载和扩展因子库
5. 变异引擎应验证所有因子表达式符合果仁语法规范

### 需求 10: 代理自动化接口

**用户故事:** 作为 AI 代理,我希望获得清晰的指令和停止条件,以便在没有人工干预的情况下自主运行优化循环。

#### 验收标准

1. 自动研究系统应在每个实验目录中生成包含完整代理指令的 program.md
2. program.md 应记录迭代工作流: 读取状态 → 分析历史 → 选择变异 → 执行迭代 → 更新搜索笔记
3. program.md 应定义停止条件: (consecutive_failures >= 5 且所有方向已探索) 或 current_iter >= 100
4. program.md 应指定 search_notes.md 格式,包含章节: 已验证有效、已验证无效、待探索方向、规律总结
5. program.md 应要求代理在每次迭代后更新 search_notes.md
6. program.md 应禁止代理修改基础设施文件(executor、mutator、scorer、run_iteration.py)
7. program.md 应要求代理继续循环而不询问用户许可

### 需求 11: 配置规范化

**用户故事:** 作为优化系统,我希望将高级策略配置规范化为果仁的内部格式,以便变异可以使用人类可读的配置。

#### 验收标准

1. 自动研究系统应接受具有高级字段名称的策略配置(filters、rankings、pool、rebalanceCycle)
2. 自动研究系统应将筛选对象规范化为果仁的字符串格式: "ID OPERATOR VALUE"
3. 自动研究系统应将排序对象规范化为果仁的 rank 格式,包含 id、weight、asc、industry 字段
4. 自动研究系统应使用参数缓存将股票池名称(例如 "hs300")解析为果仁股票池 ID
5. 自动研究系统应使用参数缓存将指标名称(例如 "pe_ttm")解析为果仁因子 ID
6. 自动研究系统应将基准名称(hs300、zz500、zz1000)规范化为果仁参考代码
7. 自动研究系统应保持所有其他回测参数(start、end、trade_cost、count、period)不变

### 需求 12: 会话管理

**用户故事:** 作为优化系统,我希望维护有效的果仁会话凭证,以便回测可以在没有手动登录的情况下执行。

#### 验收标准

1. 执行器应从 skills/guorn_strategy/data/session.json 加载会话 cookie
2. 当 session.json 不存在时,执行器应抛出错误,并提供运行 ensure-session.js 的说明
3. 执行器应在提交回测前通过检查用户配置文件来验证会话
4. 执行器应在所有浏览器上下文请求中包含会话 cookie
5. 如果会话在迭代期间过期,执行器应抛出错误并停止执行
6. 执行器应记录用户级别信息(level=1 表示约 1 年的回测窗口限制)

### 需求 13: 自然语言种子配置生成

**用户故事:** 作为量化研究员,我希望通过填写自然语言模板来生成种子配置,以便快速创建符合我投资逻辑的策略起点。

#### 验收标准

1. 自动研究系统应提供 SEED_TEMPLATE.md 模板文件,包含策略描述的结构化章节
2. 模板应包含以下章节: 策略基本信息、股票池设置、筛选条件、排序规则、回测参数、优化目标、循环参数
3. 模板应提供至少 2 个完整的示例策略(低估值高股息、高质量成长)
4. 模板应包含常用指标参考表,列出估值、盈利、成长、红利、财务质量、市场等类别的指标
5. 模板应说明如何将自然语言描述转换为 seed_config.json 格式
6. 模板应提供注意事项,包括指标名称规范、权重约束、阈值范围等
7. 用户应能够通过填写模板并转换为 JSON 来生成有效的种子配置文件

