---
name: joinquant_nookbook-request-runner
overview: 在 `skills/joinquant_nookbook` 新建一套 JoinQuant Notebook 自动化能力：先通过浏览器获取并持久化登录 cookie，后续仅通过 request API 完成 notebook cell 新增、部分/全部运行，并将执行结果落本地文件。
todos:
  - id: create-skill-skeleton
    content: 用 [skill:skill-creator] 和 [subagent:code-explorer] 搭建 joinquant_nookbook 技能骨架
    status: completed
  - id: capture-joinquant-contract
    content: 用 [skill:playwright] 抓取登录会话与 notebook 请求契约
    status: completed
    dependencies:
      - create-skill-skeleton
  - id: build-request-client
    content: 实现 request 会话库与 notebook 读改存接口
    status: completed
    dependencies:
      - create-skill-skeleton
      - capture-joinquant-contract
  - id: implement-run-flow
    content: 实现部分运行、全部运行、结果轮询与本地落盘
    status: completed
    dependencies:
      - build-request-client
  - id: finish-docs-and-test
    content: 补充 Python 验证脚本与 README/SKILL，完成测试闭环
    status: completed
    dependencies:
      - implement-run-flow
---

## User Requirements

- 在 `skills/joinquant_nookbook` 新建独立目录，面向指定的 JoinQuant Research notebook 提供修改与运行能力。
- 首次允许通过浏览器登录获取会话；后续直接复用本地保存的会话完成请求调用。
- notebook 修改内容为新增一个代码单元，内容是 `print("hello")`。
- 运行需同时支持部分运行和全部运行，并把接口返回结果保存到本地文件。
- 成功标准为：本地可通过接口触发该 notebook 执行，并成功获取执行结果。

## Product Overview

- 该能力围绕指定 notebook URL 工作：读取 notebook、追加测试单元、保存修改、触发运行、轮询结果并输出本地文件。
- 可见效果为：命令行显示会话状态、保存状态、运行进度和结果摘要；本地生成会话文件、接口原始结果文件和测试结果文件。

## Core Features

- 会话获取与复用
- notebook 内容读取、追加与保存
- 部分运行与全部运行
- 运行结果轮询与本地落盘
- Python 调用验证

## Tech Stack Selection

- 主实现沿用仓库现有 skill 习惯，使用 Node.js ESM 结构，复用 `skills/lixinger-screener` 已验证的目录组织、环境加载、CLI 与会话持久化模式。
- 请求层优先使用 Node 内置 `fetch`，避免新增不必要的 HTTP 依赖。
- 浏览器只用于首次登录与请求契约确认，方式参考：
- `skills/lixinger-screener/browser/main.js`
- `skills/lixinger-screener/request/inspect-lixinger-screener.js`
- 会话与结果持久化使用本地 JSON 文件，风格参考：
- `skills/lixinger-screener/load-env.js`
- `skills/lixinger-screener/paths.js`
- `skills/lixinger-screener/.session.json`
- 为满足“本地 Python 可调用”的验收，额外提供一个轻量 Python 3 标准库验证脚本；主实现仍保持 Node.js。

## Implementation Approach

采用“两阶段”方案：第一阶段只做一次浏览器登录和抓包确认，产出可复用的本地会话文件与已验证的 notebook 请求契约；第二阶段全部通过 request 方式执行 notebook 读取、修改、保存、运行和结果获取。

核心技术决策：

- 将“浏览器登录取会话”与“request 操作 notebook”严格隔离。这样既满足用户对 request 的要求，也能兼容 JoinQuant 可能存在的登录校验、csrf 或额外请求头依赖。
- 会话文件不只保存 cookie；如果实际抓包确认 notebook API 还依赖 csrf、xsrf、referer、特定 header，也一并归档到统一 session 文件，后续请求端统一装配，避免每个脚本重复处理。
- notebook 修改优先走“读取当前 notebook JSON → 在内存中追加 cell → 保存整本或按接口要求回写”的模型，而不是模拟页面点击。这样稳定、可测试、对 DOM 变化不敏感。
- 部分运行优先按已验证接口支持的最小粒度实现，通常是 cell id、cell index 或从某个单元开始运行；全部运行走 notebook 级执行接口。若 JoinQuant 实际契约不同，则由 runner 统一映射，不把不确定性扩散到 CLI。
- 执行结果采用“启动运行 → 轮询任务状态 → 拉取输出内容 → 本地落盘”的闭环。网络复杂度主要为 O(n) 的 notebook 单元处理和 O(p) 的轮询请求；瓶颈是远端执行耗时与轮询次数。通过最小化 notebook 重读、限制轮询间隔、设置超时与失败快照来控制耗时和排障成本。

## Implementation Notes

- 复用现有 skill 的 `load-env.js`、`paths.js`、参数解析和 session 文件思路，不引入跨目录耦合，不改动 `skills/lixinger-screener` 现有逻辑。
- 所有日志和调试文件必须脱敏：账号、密码、cookie、token、authorization、set-cookie 一律打码；原始响应只保留必要字段或截断内容，避免泄露与日志膨胀。
- 对 401、403、会话失效、csrf 失配等错误采用 fail-fast；提示重新执行会话抓取，而不是自动无限重试。
- 结果落盘需区分三类：会话文件、接口契约快照、运行结果文件；文件名带时间戳，降低覆盖和排查难度。
- 只在新增目录内实现，保持 blast radius 最小；不做与当前需求无关的通用化重构。

## Architecture Design

本次改动在新 skill 内部保持分层：

- `browser` 层：一次性登录、抓取并标准化会话与 notebook 请求契约。
- `request` 层：统一 HTTP 客户端、会话装配、notebook 读改存与运行轮询。
- `entry` 层：CLI 入口与默认测试流程，负责串联“追加 hello 单元并执行”。
- `examples/python`：读取同一份本地会话文件，验证 Python 端能复用该 API 闭环。
- `data`：运行态输出目录，保存 session、原始响应、运行结果和调试快照。

数据流：
浏览器首次登录 → 保存 session 与请求契约 → request 读取 notebook → 追加 `print("hello")` → 保存 notebook → 部分运行或全部运行 → 轮询结果 → 落盘 JSON → Python 脚本复用 session 再次验证

## Directory Structure

### Directory Structure Summary

本次改动仅新增到 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook`，不修改现有 `skills/lixinger-screener`。目录名按用户要求保留 `joinquant_nookbook`。

### Files

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/package.json` [NEW]  
独立 skill 包配置。定义 `capture`、`run`、`test` 等脚本，保持与现有 skill 的 Node ESM 风格一致，尽量只声明必要依赖。

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/README.md` [NEW]  
使用说明文档。描述首次登录、会话复用、追加测试单元、部分运行、全部运行、结果文件位置与常见故障处理。

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/SKILL.md` [NEW]  
Skill 说明文档。面向仓库内 skill 生态，概述能力边界、输入输出、典型命令和限制。

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/load-env.js` [NEW]  
环境变量加载入口。沿用 `lixinger-screener` 模式，从 skill 根目录 `.env` 读取账号与本地配置并统一导出路径常量。

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/paths.js` [NEW]  
路径常量定义。统一管理 skill 根目录、`browser`、`request`、`data`、session 文件与结果文件位置，避免脚本内硬编码路径。

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/main.js` [NEW]  
默认编排入口。对外暴露“读取指定 notebook、追加 hello 单元、保存并运行、落盘结果”的主流程，供 CLI 与后续扩展复用。

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/run-skill.js` [NEW]  
命令行薄入口。解析用户参数并调用 `main.js`，保持与现有 skill 入口习惯一致。

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/browser/capture-joinquant-session.js` [NEW]  
一次性浏览器辅助脚本。用于登录 JoinQuant、抓取 notebook 保存与运行相关请求、提取 cookie 与必要 header，并写入标准化 session 文件与原始契约快照。

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/request/session-store.js` [NEW]  
会话存储模块。负责加载、校验、更新本地 session JSON，统一对外提供 cookie、csrf、referer 等请求上下文。

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/request/joinquant-client.js` [NEW]  
通用请求客户端。封装请求头拼装、超时、错误处理、重试边界、响应落盘和脱敏日志，是所有 notebook API 调用的唯一出口。

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/request/notebook-runner.js` [NEW]  
notebook 业务核心。基于已验证契约实现 notebook 读取、追加 cell、保存、部分运行、全部运行、状态轮询和结果提取，保持无浏览器依赖。

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/request/test-joinquant-notebook.js` [NEW]  
测试场景入口。针对当前指定 notebook 固化“新增 `print("hello")` 单元并执行”的验证流程，生成本地结果文件，作为交付与回归入口。

- `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/examples/python/run_joinquant_notebook_test.py` [NEW]  
Python 验证脚本。读取同一份本地 session 文件，调用已验证的 notebook API，证明 Python 端也能完成执行与结果获取。

### Runtime Outputs

运行时文件统一落在 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/data/`，包括：

- `session.json` 或同类标准化会话文件
- `api-contract.json` 或同类请求契约快照
- `notebook-*.json` notebook 快照
- `run-result-*.json` 执行结果
- `raw-*.json` 脱敏后的原始响应调试文件

## Agent Extensions

### Skill

- **skill-creator**
- Purpose: 按仓库现有 skill 习惯组织 `joinquant_nookbook` 的入口、文档和目录结构
- Expected outcome: 新 skill 目录结构清晰、说明完整、可直接复用与维护

- **playwright**
- Purpose: 完成首次 JoinQuant 登录、抓取 notebook 保存与运行相关请求、提取可复用会话
- Expected outcome: 产出稳定的本地 session 文件与已验证的请求契约快照，后续 notebook 操作全部走 request

### SubAgent

- **code-explorer**
- Purpose: 复核 `skills/lixinger-screener` 中可复用的路径、会话、CLI 与模块拆分模式
- Expected outcome: 新 skill 的文件拆分与现有仓库约定保持一致，降低实现偏差与回归风险