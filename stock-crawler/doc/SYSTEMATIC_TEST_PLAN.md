# 大规模系统化测试计划（Stock Website Crawler）

本计划用于把当前测试体系升级为“可分层、可观测、可回归”的大规模测试流程，适用于爬虫类项目的持续演进。

## 1. 测试目标

- **正确性**：保证配置解析、链接发现、页面解析、输出落盘的核心逻辑不回退。
- **稳定性**：在网络抖动、页面结构变化、登录态失效等情况下可重试、可恢复。
- **可扩展性**：在站点数量增长、链接规模增长时，吞吐和错误率仍在阈值内。
- **可追踪性**：每次测试可定位到配置、代码版本、输出结果和日志。

## 2. 分层测试策略

### L1 - 快速层（每次提交必跑）

**目标**：分钟级反馈，阻止明显回归。

- 范围：不依赖真实浏览器和网络的单元测试、属性测试。
- 命令：

```bash
npm test -- config-manager.test.js
npm test -- link-manager.test.js
npm test -- url-utils.test.js
npm test -- markdown-generator.test.js
```

### L2 - 集成层（每次 PR 或每日多次）

**目标**：验证模块联动行为。

- 范围：parser-manager、crawler-main 等跨模块测试。
- 建议：优先对 I/O 边界做 mock，减少外部依赖波动。
- 命令示例：

```bash
npm test -- parser-manager.test.js
npm test -- crawler-main.test.js
npm test -- page-parser.test.js
```

### L3 - 浏览器层（每日回归）

**目标**：验证真实页面交互路径（登录、分页、链接提取）。

- 前置：安装 Playwright 浏览器。

```bash
npx playwright install
```

- 命令：

```bash
npm run test:login config/lixinger.json
npm run test:pagination
npm test -- link-finder.test.js
```

### L4 - 大规模回归层（夜间或里程碑前）

**目标**：验证真实长链路稳定性与恢复能力。

- 运行多个配置（至少 3 类站点：公开页/动态页/登录页）。
- 强制注入异常场景：超时、429、DOM 缺失、登录过期。
- 关注长时间运行指标（至少 30~120 分钟）。

## 3. 测试矩阵（建议）

| 维度 | 建议取值 |
|---|---|
| 站点类型 | 公开静态、JS 动态、需登录 |
| 数据规模 | 小样本（50 链接）、中样本（500）、大样本（5000+） |
| 关键参数 | headless、timeout、maxRetries、batchSize |
| 故障注入 | 5xx、429、超时、页面结构变更、登录失效 |
| 执行频率 | 提交级、PR级、每日级、里程碑级 |

## 4. 验收指标（KPI）

建议在每次 L3/L4 任务后统一输出以下指标：

- **通过率**：`passed_tests / total_tests`
- **抓取成功率**：`fetched_links / discovered_links`
- **重试修复率**：`retry_success / retry_total`
- **恢复成功率**：中断恢复后继续完成的任务比例
- **性能指标**：平均页面耗时、P95 页面耗时、总吞吐（页/分钟）
- **质量指标**：页面解析字段完整率（标题、表格、代码块等）

建议阈值（可按业务调整）：

- 抓取成功率 ≥ 95%
- 恢复成功率 ≥ 98%
- 关键字段完整率 ≥ 97%
- P95 页面耗时环比波动 ≤ 20%

## 5. 执行与产出规范

每次系统化测试建议保留以下产物：

- 代码版本：Git commit SHA
- 测试配置：使用的 config 文件快照
- 命令记录：执行命令与开始/结束时间
- 输出目录：`output/<project-name>/pages-*/`
- 日志目录：`output/<project-name>/logs/`
- 链接状态：`output/<project-name>/links.txt`

## 6. 建议实施节奏（1 周）

- **Day 1**：确认 L1/L2/L3/L4 分层与矩阵。
- **Day 2**：补齐命令分组脚本（可在 package.json 新增 test:l1/test:l2/test:l3）。
- **Day 3**：跑第一版基线，记录 KPI。
- **Day 4**：补故障注入场景与恢复测试。
- **Day 5**：接入定时任务（如 nightly），稳定产出日报。

## 7. 当前仓库的立即行动建议

1. 先安装 Playwright 浏览器，避免浏览器相关测试批量失败。
2. 优先建立 L1 快速门禁（5~10 分钟内完成）。
3. 对登录与分页场景单独出回归报告，避免与纯单测混跑后定位困难。
4. 将大规模测试结果沉淀为固定模板（指标 + 异常 TopN + 对策）。
