# 后续改进与重构路线图（Stock Website Crawler）

> 目标：在不牺牲抓取能力的前提下，降低维护成本、提升可测试性与稳定性。

## 1. 先修“当前不稳定点”（1~2 周）

### 1.1 修复测试与实现漂移
- 当前 `ParserManager` 只做“按 URL matches 的顺序选择”，没有分类器/override 流程，和测试预期存在偏差。
- 当前 `LinkFinder` 的实现与单测约定不一致（例如缺少 `getDefaultPrioritizedPatterns`，且 `extractLinks` 对 `page.waitForFunction` 有强依赖，导致 mock page 易失败）。
- 建议先统一“代码即规范”或“测试即规范”：
  - 若以现代码为准：更新测试用例；
  - 若以测试为准：补齐分类器 + override 机制，并恢复 `LinkFinder` 的可测试接口。

### 1.2 为浏览器依赖型测试加分层开关
- 部分测试依赖 Playwright 浏览器二进制，当前环境缺失时会失败。
- 建议将测试拆分为：
  - **纯单元层**（不依赖浏览器，可在 CI 默认执行）；
  - **集成层**（依赖 Playwright，可 nightly 或按需执行）。

## 2. 架构重构（2~4 周）

### 2.1 拆分 `crawler-main`（编排层瘦身）
`crawler-main` 当前承担了配置加载、目录初始化、任务排序、登录流程、抓取主循环、统计收尾等多职责。建议拆为：
- `BootstrapService`：配置与运行目录初始化；
- `CrawlScheduler`：seed + unfetched 的优先级与批次策略；
- `CrawlExecutor`：URL 处理与状态转换；
- `RunSummaryService`：统计、日志收口。

### 2.2 抽离统一“链接发现策略”
`LinkFinder` 里混合了 DOM 提取、无限滚动、站点特化规则（如 finnhub、api-key 规则）。建议按策略模式拆分：
- `DomLinkExtractionStrategy`
- `SpaScrollStrategy`
- `SiteSpecificLinkPolicy`

这样可以做到：
- 新站点只新增策略，不改核心流程；
- 单测可以针对策略做最小 mock。

### 2.3 限定 `GenericParser` 职责边界
`GenericParser` 目前聚合了 API 拦截、文本提取、图表提取、表格分页、时间筛选等能力，且包含“临时注释待修复”的 tab/dropdown 功能。
- 建议拆为可组合的 `Extractor` 管线：
  - `TextExtractor` / `TableExtractor` / `ChartExtractor` / `ApiResponseExtractor` / `InteractiveContentExtractor`
- 每个 extractor 输出标准化片段，再由 `AggregationStage` 合并。

## 3. 可观测性与质量保障（并行推进）

### 3.1 引入统一错误码与失败原因分类
- 将“解析失败/网络失败/登录失败/选择器失效”分类上报。
- 配合现有日志，形成可统计的 failure taxonomy，便于后续稳定性治理。

### 3.2 建立回归数据集（黄金页面）
- 选 10~20 个典型页面（静态页、SPA、表格分页、图表页、需要登录页）。
- 形成“输入 URL -> 关键字段断言”的快照回归。
- 每次改 parser/link-finder 都跑这套回归，防止能力倒退。

### 3.3 性能指标基线
- 记录每页耗时、滚动次数、提取元素数量、markdown 体积。
- 设定阈值告警（如平均每页耗时 > N 秒）。

## 4. 研发体验优化（低风险高收益）

### 4.1 增加统一 CLI 子命令
把 `test-*`、`inspect-*`、`run-*-loop.sh` 逐步归一到单一 CLI：
- `crawl run --config ...`
- `crawl inspect --url ...`
- `crawl replay --fixture ...`
- `crawl test --suite unit|integration`

### 4.2 配置 Schema 化
- 用 JSON Schema/Zod 对配置做强校验与默认值注入。
- 输出“可读的配置错误路径”，降低排障成本。

## 5. 推荐落地顺序（执行优先级）
1. **P0**：修复测试漂移（ParserManager / LinkFinder）+ 测试分层。  
2. **P1**：拆 `crawler-main` 编排职责，稳定主流程。  
3. **P1**：拆 `GenericParser` 为 extractor 管线，恢复并重做 tab/dropdown。  
4. **P2**：引入黄金页面回归 + 指标基线。  
5. **P2**：CLI 统一与配置 schema 化。

## 6. 预期收益
- 迭代速度：新增站点/规则时，改动范围更小。
- 稳定性：功能回归可被更早发现。
- 可维护性：模块职责清晰，排障路径短。
- 团队协作：测试分层后，CI 反馈更稳定、更快。
