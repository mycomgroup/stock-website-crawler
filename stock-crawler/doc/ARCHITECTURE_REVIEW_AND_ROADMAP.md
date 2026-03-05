# 架构评估与升级路线图（stock-crawler）

## 1. 当前架构总体判断

当前项目的核心价值已经明确：围绕「可配置抓取 + 页面解析 + 结构化落盘」形成了可用的端到端流水线，并且具备登录、链接发现、分页/Tab/下拉等复杂页面处理能力。

但从工程演进角度看，主流程控制器偏重、边界不够清晰，导致后续迭代成本会随着功能增加而明显上升。

## 2. 关键架构问题（优先级排序）

### P0：编排层过重（单类职责过多）

`crawler-main.js` 同时承担了：

- 初始化与目录管理
- 登录策略编排
- 链接调度
- 单页处理与重试
- 多类型输出（Markdown/CSV/LLM附加）
- 统计与日志

这会带来：

1. 单文件改动冲突频繁。
2. 功能测试粒度偏大，问题定位慢。
3. 新增能力（例如分布式调度、多输出后端）时耦合面过宽。

### P0：领域模型弱，状态管理分散

当前链接状态（unfetched/fetching/fetched/failed）与重试逻辑分布在多处流程中，属于“脚本式状态机”。

风险：

- 状态迁移规则难以全局保证。
- 边界场景（崩溃恢复、部分成功）容易出现不一致。

### P1：解析层可扩展性仍可加强

虽然已有 parser 目录与 manager，但“页面类型识别 + 提取 + 结果标准化 + 输出映射”尚未形成稳定契约（Contract-first）。

影响：

- 增加新解析器时需要理解较多隐式上下文。
- 不同解析器的输出一致性依赖人工约束。

### P1：可观测性偏日志导向，缺乏结构化指标

当前日志较完整，但缺少统一 metrics/tracing 视角。运营期难回答：

- 哪类页面失败率最高？
- 登录失败是站点问题还是策略问题？
- 解析耗时主要瓶颈在哪一步？

### P2：配置治理能力可升级

配置具备灵活性，但可进一步增强：

- 配置 schema 严格校验
- 配置版本迁移（v1->v2）
- 环境覆盖（dev/staging/prod）
- 敏感信息管理（密钥、账号）

## 3. 推荐目标架构（分层）

建议重构为以下逻辑分层：

1. **Application Layer（编排层）**
   - `CrawlJobService`：负责任务生命周期（启动/暂停/恢复/结束）
   - `UrlProcessingService`：负责单 URL 处理编排（不做具体抓取细节）

2. **Domain Layer（领域层）**
   - `CrawlTask`、`UrlStateMachine`、`ExtractionResult` 等核心模型
   - 明确定义状态迁移：`unfetched -> fetching -> fetched|failed`

3. **Infrastructure Layer（基础设施层）**
   - BrowserAdapter（Playwright）
   - StorageAdapter（File/LanceDB）
   - MetricsAdapter（console/prometheus）

4. **Plugin Layer（插件层）**
   - `ParserPlugin`
   - `LinkDiscoveryPlugin`
   - `PostProcessPlugin`（如 LLM 结构化抽取）

核心原则：主流程只“编排”和“声明策略”，不直接承载大量 if/else 业务细节。

## 4. 可执行升级路线图

### 阶段 A（1~2 周）：低风险整理（建议立即做）

- 拆分 `crawler-main.js`：
  - `login-orchestrator.js`
  - `url-processor.js`
  - `output-writer.js`
- 给配置增加 JSON Schema 校验（启动即 fail-fast）。
- 增加结构化日志字段：`taskId`、`url`、`phase`、`durationMs`、`result`。

**收益**：降低认知复杂度，不改变现有业务能力。

### 阶段 B（2~4 周）：稳定性与可观测性

- 抽离 `UrlStateMachine`（单元测试覆盖所有状态迁移）。
- 将重试策略独立为 `RetryPolicy`（可按错误类型差异重试）。
- 增加 metrics：
  - crawl_success_rate
  - parse_success_rate
  - login_success_rate
  - avg_page_process_seconds

**收益**：运行质量可量化，线上问题定位速度显著提升。

### 阶段 C（4~8 周）：能力平台化

- 解析器插件化契约：`canHandle` / `extract` / `normalize`。
- 调度层支持并发队列与限速策略（按域名/页面类型限流）。
- 引入任务元数据存储（SQLite/Postgres 二选一）以支持多任务管理和历史追踪。

**收益**：从“单任务脚本”升级为“可持续扩展的抓取平台”。

## 5. 关键设计建议（细化）

### 5.1 先定义统一结果模型

建议所有解析结果统一成：

- `meta`（url/title/timestamps）
- `contentBlocks`（paragraph/table/code/list/chart）
- `artifacts`（markdown/csv/json）
- `quality`（完整度、异常标记）

这样输出端（Markdown、CSV、向量库）可以解耦成“多个消费者”。

### 5.2 将登录从“流程中的步骤”升级为“会话服务”

新增 `SessionService`：

- 负责会话有效性检测
- 统一处理登录续期
- 提供登录健康度指标

避免每个 URL 处理过程里重复注入登录判断。

### 5.3 将链接管理升级为可替换队列

给 `LinkManager` 设计最小接口：

- `enqueue(url)`
- `dequeue(batchSize)`
- `ack(url)`
- `nack(url, reason)`

默认实现仍可基于文件，后续可平滑替换 Redis/DB。

### 5.4 测试金字塔重排

- 保留现有单元测试。
- 新增“契约测试”（parser contract、storage contract）。
- 增加少量 E2E 回放测试（固定站点快照 + 断言输出）。

目标：在重构期保证行为一致性。

## 6. 优先级执行清单（建议）

1. 拆分 `crawler-main.js`（最优先）。
2. 建立 `UrlStateMachine` 与 `RetryPolicy`。
3. 配置 schema + 启动前校验。
4. 结构化日志 + 核心 metrics。
5. 解析器契约化与插件化。

## 7. 结论

项目当前已具备较强功能覆盖，下一步应从“功能继续堆叠”转向“架构治理与平台化升级”。

先做编排层瘦身和状态机抽离，可以在风险可控的前提下，显著提高后续功能交付速度与线上稳定性。
