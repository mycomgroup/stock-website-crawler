# 分层清理后并行开发计划（10个互相影响子模块）

> 目标：基于当前已落地的 `application / domain / infrastructure` 分层，拆成 10 个可并行、但有清晰依赖边界的后续迭代模块。

## 总体规则

- **Domain 先行**：状态机、任务模型、错误模型先固化，再扩展上层编排。
- **Application 只做编排**：不允许直接写复杂解析细节和底层持久化细节。
- **Infrastructure 可替换**：文件存储、指标、队列后端保持适配器接口。
- **跨模块变更必须补契约测试**：避免并行开发互相踩边界。

---

## M1. 任务生命周期模块（CrawlJob Lifecycle）

- 负责人：应用编排同学
- 范围：任务启动、暂停、恢复、结束；任务级状态持久化
- 输出：`CrawlJobService` 扩展为完整任务生命周期管理
- 依赖：M3（状态机）、M4（任务仓储）
- 反向影响：M6（CLI）、M8（监控）

## M2. URL 调度模块（URL Scheduling）

- 负责人：应用编排同学
- 范围：批次选择、优先级策略、域名级限流
- 输出：调度策略接口 + 默认实现
- 依赖：M3（状态机）、M5（队列抽象）
- 反向影响：M7（解析流水线吞吐）

## M3. 领域状态机模块（Domain State Machine）

- 负责人：领域建模同学
- 范围：`unfetched -> fetching -> fetched|failed` 全状态图与非法迁移约束
- 输出：`UrlStateMachine` + 迁移事件（可审计）
- 依赖：无（基础模块）
- 反向影响：M1、M2、M9

## M4. 任务与链接仓储模块（Task/Link Repository）

- 负责人：存储同学
- 范围：任务元数据、链接状态、重试信息存储接口
- 输出：Repository 接口 + file/sqlite 双实现
- 依赖：M3（状态约束）
- 反向影响：M1、M2、M9

## M5. 队列抽象模块（Queue Adapter）

- 负责人：基础设施同学
- 范围：`enqueue/dequeue/ack/nack` 统一接口
- 输出：in-memory/file 实现（后续可接 Redis）
- 依赖：M3、M4
- 反向影响：M2（调度器）、M1（恢复机制）

## M6. CLI 与任务控制台模块（CLI & Control Plane）

- 负责人：工具链同学
- 范围：CLI 子命令：start/pause/resume/status
- 输出：统一命令入口 + 任务状态展示
- 依赖：M1
- 反向影响：M8（指标曝光）、M10（发布流程）

## M7. 解析流水线模块（Parser Pipeline）

- 负责人：抓取解析同学
- 范围：页面分类、抽取、标准化、输出块模型
- 输出：Parser contract + pipeline stages
- 依赖：M3（状态）、M4（结果持久化）
- 反向影响：M8（解析指标）、M9（失败重试分类）

## M8. 可观测性模块（Metrics/Logging/Tracing）

- 负责人：SRE/平台同学
- 范围：结构化日志、metrics 指标、trace 关联ID
- 输出：指标标准：crawl_success_rate/login_success_rate/parse_success_rate
- 依赖：M1、M2、M7（事件来源）
- 反向影响：M10（稳定性门禁）

## M9. 错误与重试策略模块（Failure Taxonomy & RetryPolicy）

- 负责人：稳定性同学
- 范围：错误分类（网络/鉴权/解析/限流），按错误类型动态重试
- 输出：策略化 `RetryPolicy`（可配置）
- 依赖：M3、M4
- 反向影响：M1、M2、M7

## M10. 交付与质量门禁模块（Release & Quality Gates）

- 负责人：测试平台同学
- 范围：契约测试、回归基线、发布门禁
- 输出：CI 流程：domain contract + app integration + smoke e2e
- 依赖：M6、M8、M9
- 反向影响：全模块

---

## 并行节奏建议（4 周）

- **第 1 周**：M3、M4、M5 同时启动；M1 先做接口对齐。
- **第 2 周**：M1、M2、M9 启动；M6 开始 CLI 编排。
- **第 3 周**：M7、M8 启动并接入前两周事件流。
- **第 4 周**：M10 收口，建立发布门禁与回归基线。

## 模块协作协议（必须执行）

1. 每个模块必须提供：`README + 接口定义 + 契约测试`。
2. 任何跨层调用（例如 app 直接操作 fs）一律拒绝。
3. 领域对象变更必须走 RFC（至少包含迁移影响评估）。
4. 合并前必须通过对应契约测试集合。
