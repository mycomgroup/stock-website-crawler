# 需求文档：lxr-cli

## 简介

`lxr` 是一个面向人类和 Agent 双重工作流的命令行工具，封装理杏仁（lixinger.com）股票筛选能力。

工具以"业务语义优先"为核心原则：用户通过 Canonical Query Schema（YAML 格式）描述筛选意图，不暴露任何 provider 实现细节。`lxr` 内部将 canonical query 编译为 provider 请求，通过 OpenAPI 或网页筛选器两个后端执行，最终以稳定的 JSON envelope 或表格/CSV 格式输出结果。

工具提供完整的命令树：认证管理（`auth`）、字典同步与查询（`dict`）、指标查询（`metric`）、筛选全生命周期（`screen init/validate/compile/explain/run`）、结果导出（`result export`）和环境自检（`doctor`）。

stdout 只放结果数据，日志/警告/进度一律走 stderr；TTY 时默认 table 格式，非 TTY 时默认 json 格式。

---

## 词汇表

- **CLI**：命令行界面（Command Line Interface），即 `lxr` 工具本身
- **Canonical Query**：业务语义优先的筛选查询描述，YAML 格式，不含 provider 细节，schemaVersion 字段标识版本
- **Provider**：筛选后端实现，目前支持 `openapi`（理杏仁 OpenAPI）和 `web-screener`（网页筛选器 Playwright 自动化）两种
- **Compiler**：将 Canonical Query 转换为 Provider Request 的内部模块
- **Catalog**：指标目录，记录所有可用筛选指标的元数据（名称、分类、单位、操作符等）
- **Dict**：字典，记录行业、指数、省份、交易所等可枚举实体的标准化数据
- **JSON Envelope**：统一的 JSON 输出结构，包含 `ok`、`schemaVersion`、`command`、`meta`、`rows`、`diagnostics` 等字段
- **TTY**：终端（teletypewriter），用于判断输出目标是否为交互式终端
- **Profile**：本地认证配置文件，存储 token 或 cookie/session 信息
- **Doctor**：环境自检命令，检查网络、认证、字典 freshness、目录权限等
- **Golden Test**：编译输出快照测试，验证 compile 阶段输出的确定性
- **Smoke Test**：冒烟测试，用固定 screener URL 跑全链路验证
- **Universe**：筛选股票池，包含市场、交易所、行业、指数、互联互通、省份、标志等过滤维度
- **Selector**：指标的子维度选择器，如 PE-TTM 的"10年"、"分位点%"
- **Exit Code**：进程退出码，用于标识命令执行结果类型

---

## 需求

### 需求 1：命令树与路由

**用户故事：** 作为用户，我希望通过统一的 `lxr` 命令入口访问所有子命令，以便在一个工具中完成认证、字典、筛选、导出的完整工作流。

#### 验收标准

1. THE CLI SHALL 提供以下子命令树：`auth login`、`auth status`、`auth logout`、`dict sync`、`dict list`、`dict search`、`dict get`、`metric search`、`metric get`、`screen import-url`、`screen init`、`screen validate`、`screen compile`、`screen explain`、`screen run`、`result export`、`doctor`
2. WHEN 用户执行 `lxr --help` 或 `lxr <subcommand> --help`，THE CLI SHALL 输出该命令的用法说明到 stderr
3. WHEN 用户执行不存在的子命令，THE CLI SHALL 输出错误提示到 stderr 并以退出码 2 退出
4. THE CLI SHALL 支持 `--version` 标志，输出当前版本号到 stdout
5. WHEN 输出目标为 TTY，THE CLI SHALL 默认使用 table 格式；WHEN 输出目标为非 TTY，THE CLI SHALL 默认使用 json 格式
6. THE CLI SHALL 将所有日志、警告、进度信息输出到 stderr，将结果数据输出到 stdout

---

### 需求 2：stdout/stderr 分离与输出格式

**用户故事：** 作为 Agent，我希望 stdout 只包含结构化结果数据，以便在管道中可靠地解析输出；作为人类用户，我希望在终端看到友好的表格格式。

#### 验收标准

1. THE CLI SHALL 将所有结果数据（rows、JSON envelope、CSV 内容）输出到 stdout
2. THE CLI SHALL 将所有进度信息、警告、错误消息输出到 stderr
3. WHEN `--format json` 被指定，THE CLI SHALL 输出符合 JSON Envelope 规范的 JSON 到 stdout
4. WHEN `--format table` 被指定，THE CLI SHALL 输出对齐的 ASCII 表格到 stdout
5. WHEN `--format csv` 被指定，THE CLI SHALL 输出 RFC 4180 兼容的 CSV 到 stdout
6. WHEN `--quiet` 标志被指定，THE CLI SHALL 抑制所有 stderr 输出（仅保留结果数据到 stdout）
7. THE JSON Envelope SHALL 包含字段：`ok`（boolean）、`schemaVersion`（integer）、`command`（string）、`meta`（object）、`rows`（array）、`diagnostics`（array）
8. WHEN `ok` 为 false，THE JSON Envelope SHALL 在 `diagnostics` 数组中包含至少一条错误描述

---

### 需求 3：退出码规范

**用户故事：** 作为 Agent，我希望通过退出码快速判断命令失败类型，以便在自动化流程中做出正确的错误处理决策。

#### 验收标准

1. WHEN 命令成功执行，THE CLI SHALL 以退出码 0 退出
2. WHEN 输入校验失败（query schema 不合法、参数缺失等），THE CLI SHALL 以退出码 2 退出
3. WHEN 认证失败（token 无效、cookie 过期、凭据错误），THE CLI SHALL 以退出码 3 退出
4. WHEN 网络或 provider 失败（请求超时、HTTP 错误、Playwright 操作失败），THE CLI SHALL 以退出码 4 退出
5. WHEN 字典解析存在歧义（搜索词匹配到多个结果且无法自动消歧），THE CLI SHALL 以退出码 5 退出
6. WHEN 部分成功（如分页抓取中途失败但已有部分数据），THE CLI SHALL 以退出码 6 退出

---

### 需求 4：认证管理（auth）

**用户故事：** 作为用户，我希望通过 `lxr auth` 命令管理理杏仁的认证凭据，以便在不同命令中复用已登录状态。

#### 验收标准

1. WHEN 用户执行 `lxr auth login`，THE CLI SHALL 引导用户输入凭据并将认证信息持久化到 Profile 文件
2. WHEN 用户执行 `lxr auth status`，THE CLI SHALL 检查当前认证状态并输出 token/cookie 的有效性和过期时间
3. WHEN 用户执行 `lxr auth logout`，THE CLI SHALL 清除本地 Profile 文件中的认证信息
4. THE CLI SHALL 按以下优先级读取认证信息：命令行参数 > 环境变量 > Profile 文件
5. THE CLI SHALL 支持两种认证类型：`token`（OpenAPI 使用）和 `cookie/session`（网页筛选器使用）
6. WHEN 环境变量 `LXR_TOKEN` 已设置，THE CLI SHALL 使用该值作为 OpenAPI token
7. WHEN 环境变量 `LIXINGER_USERNAME` 和 `LIXINGER_PASSWORD` 已设置，THE CLI SHALL 使用这些值进行网页登录
8. IF 认证信息缺失且命令需要认证，THEN THE CLI SHALL 输出明确的错误提示到 stderr 并以退出码 3 退出

---

### 需求 5：字典管理（dict）

**用户故事：** 作为用户，我希望通过 `lxr dict` 命令同步和查询行业、指数、省份等字典数据，以便在编写 Canonical Query 时使用正确的 code 和 source。

#### 验收标准

1. WHEN 用户执行 `lxr dict sync --area cn`，THE CLI SHALL 从 provider 拉取最新字典数据并缓存到本地
2. THE CLI SHALL 将字典文件缓存到 `~/.lxr/dicts/` 目录，文件名格式为 `{area}-{entityType}.json`
3. THE Dict 缓存文件 SHALL 包含统一字段：`schemaVersion`、`generatedAt`、`source`、`area`、`entityType`、`items`
4. THE Dict 缓存文件中每个 item SHALL 包含统一字段：`id`、`code`、`name`、`label`、`source`、`level`、`parentId`、`aliases`、`pinyin`
5. WHEN 用户执行 `lxr dict list --type industry`，THE CLI SHALL 列出指定类型的所有字典条目
6. WHEN 用户执行 `lxr dict search industry "银行"`，THE CLI SHALL 在指定类型字典中进行模糊匹配并返回匹配结果
7. WHEN 用户执行 `lxr dict get industry "760102"`，THE CLI SHALL 返回指定 code 的字典条目详情
8. WHEN 字典缓存不存在或已过期（默认 TTL 为 24 小时），THE CLI SHALL 在 stderr 输出提示并建议用户执行 `lxr dict sync`
9. IF 搜索词匹配到多个结果且无法自动消歧，THEN THE CLI SHALL 列出所有候选项并以退出码 5 退出

---

### 需求 6：指标查询（metric）

**用户故事：** 作为用户，我希望通过 `lxr metric` 命令查询可用的筛选指标，以便在编写 Canonical Query 时使用正确的指标名称和 selectors。

#### 验收标准

1. WHEN 用户执行 `lxr metric search "PE"`，THE CLI SHALL 在 Catalog 中进行模糊匹配并返回匹配的指标列表
2. WHEN 用户执行 `lxr metric get "PE-TTM(扣非)统计值"`，THE CLI SHALL 返回该指标的完整元数据（名称、分类、单位、可用 operators、可用 selectors）
3. THE Catalog SHALL 覆盖理杏仁筛选页面所有可用指标，每个指标包含：`name`、`displayName`、`category`、`unit`、`operators`、`selectors`（可选）字段
4. WHEN 指标存在子维度选择器（selectors），THE CLI SHALL 在 `metric get` 输出中列出所有可用 selectors
5. IF 指标名称不存在，THEN THE CLI SHALL 输出错误提示并列出相近指标名称

---

### 需求 7：Canonical Query Schema

**用户故事：** 作为用户，我希望用业务语义优先的 YAML 格式描述筛选条件，不需要了解 provider 的实现细节，以便在不同 provider 之间无缝切换。

#### 验收标准

1. THE CLI SHALL 支持 `schemaVersion: 1` 的 Canonical Query YAML 格式
2. THE Canonical Query SHALL 支持 `universe` 字段，包含以下子字段：`market`、`stockBourseTypes`（含 include/exclude）、`industry`（含 source/level/code）、`index`（含 intersect）、`mutualMarkets`（含 include）、`multiMarketListedTypes`（含 exclude）、`province`（含 include）、`flags`（excludeBlacklist、excludeDelisted、excludeSpecialTreatment）
3. THE Canonical Query SHALL 支持 `conditions` 数组，每个条件包含：`metric`（指标名）、`category`（分类）、`selectors`（子维度，可选）、`between`/`gte`/`lte`/`eq`（操作符）
4. THE Canonical Query SHALL 支持 `sort` 字段，包含：`metric`、`selectors`（可选）、`order`（asc/desc）
5. THE Canonical Query SHALL 支持 `output` 字段，包含：`fields`（输出列）、`format`（csv/json/table）
6. WHEN Canonical Query 中的 `conditions[].metric` 值不在 Catalog 中，THE CLI SHALL 在 validate 阶段报告错误
7. WHEN Canonical Query 中的 `universe.industry.code` 值不在字典缓存中，THE CLI SHALL 在 validate 阶段报告警告

---

### 需求 8：筛选生命周期命令（screen）

**用户故事：** 作为用户，我希望通过 `screen` 子命令完成筛选的完整生命周期（初始化、校验、编译、解释、执行），以便在执行前充分验证查询的正确性。

#### 验收标准

1. WHEN 用户执行 `lxr screen init value-screen.yaml`，THE CLI SHALL 在当前目录生成包含示例内容的 Canonical Query YAML 文件
2. WHEN 用户执行 `lxr screen validate value-screen.yaml`，THE CLI SHALL 校验 YAML 文件是否符合 Canonical Query Schema，并输出所有错误和警告
3. WHEN 用户执行 `lxr screen compile value-screen.yaml --format json`，THE CLI SHALL 将 Canonical Query 编译为 Provider Request 并输出到 stdout，不执行实际筛选
4. WHEN 用户执行 `lxr screen explain value-screen.yaml`，THE CLI SHALL 以人类可读的自然语言解释筛选条件的含义
5. WHEN 用户执行 `lxr screen run value-screen.yaml`，THE CLI SHALL 执行筛选并将结果输出到 stdout
6. WHEN 用户执行 `lxr screen import-url <screener-url>`，THE CLI SHALL 解析理杏仁筛选页面 URL 并生成对应的 Canonical Query YAML 文件
7. WHEN `screen validate` 发现错误，THE CLI SHALL 以退出码 2 退出；WHEN 仅有警告，THE CLI SHALL 以退出码 0 退出
8. WHEN `screen run` 执行成功，THE CLI SHALL 在 JSON Envelope 的 `meta` 字段中包含：`area`、`total`（结果总数）、`latestTime`、`latestQuarter`
9. WHEN `screen run` 执行成功，THE CLI SHALL 在 JSON Envelope 的 `compiledRequest` 字段中包含编译后的 Provider Request

---

### 需求 9：Compiler（canonical query → provider request）

**用户故事：** 作为开发者，我希望 Compiler 模块将 Canonical Query 确定性地转换为 Provider Request，以便通过 golden test 验证编译输出的稳定性。

#### 验收标准

1. THE Compiler SHALL 将 Canonical Query 中的 `conditions[].metric` 映射到 Catalog 中对应的 provider 字段名
2. THE Compiler SHALL 将 Canonical Query 中的 `universe.industry` 映射到 provider 所需的行业筛选参数
3. THE Compiler SHALL 将 Canonical Query 中的 `universe.index` 映射到 provider 所需的指数筛选参数
4. WHEN 相同的 Canonical Query 输入两次，THE Compiler SHALL 产生完全相同的 Provider Request 输出（确定性）
5. THE Compiler SHALL 支持 `openapi` 和 `web-screener` 两种 provider 目标，通过 `--provider` 参数或配置文件指定
6. IF Canonical Query 中包含 provider 不支持的字段，THEN THE Compiler SHALL 在 `diagnostics` 中报告警告而非报错

---

### 需求 10：Provider 执行

**用户故事：** 作为用户，我希望 `lxr` 能通过 OpenAPI 或网页筛选器两种后端执行筛选，以便在 API 不支持某些条件时自动降级到网页筛选器。

#### 验收标准

1. THE CLI SHALL 支持 `openapi` provider，通过理杏仁 OpenAPI 执行筛选请求
2. THE CLI SHALL 支持 `web-screener` provider，通过 Playwright 自动化操作理杏仁网页筛选器执行筛选
3. WHEN `web-screener` provider 执行时，THE CLI SHALL 支持 `--headless` 标志控制浏览器是否以无头模式运行（默认无头）
4. WHEN provider 请求超时（默认 30 秒），THE CLI SHALL 输出超时错误到 stderr 并以退出码 4 退出
5. WHEN `web-screener` provider 在页面中找不到指定指标，THE CLI SHALL 输出错误到 stderr 并以退出码 4 退出
6. WHEN 结果包含分页，THE CLI SHALL 自动翻页并合并所有页面数据
7. WHEN 用户指定 `--limit <n>`，THE CLI SHALL 在合并分页后截取前 n 条结果

---

### 需求 11：结果导出（result export）

**用户故事：** 作为用户，我希望通过 `lxr result export` 命令将筛选结果导出为文件，以便在外部工具中进一步分析。

#### 验收标准

1. WHEN 用户执行 `lxr result export value-screen.yaml --format csv`，THE CLI SHALL 将筛选结果以 CSV 格式写入文件
2. THE CLI SHALL 将导出文件保存到 `output/` 目录，文件名格式为 `{query-name}-{timestamp}.{ext}`
3. WHEN `--output <path>` 被指定，THE CLI SHALL 将导出文件写入指定路径
4. THE CSV 导出 SHALL 符合 RFC 4180 规范，第一行为列标题
5. WHEN 导出成功，THE CLI SHALL 将导出文件的完整路径输出到 stdout

---

### 需求 12：doctor 自检

**用户故事：** 作为用户，我希望通过 `lxr doctor` 命令快速检查工具的运行环境，以便在出现问题时快速定位原因。

#### 验收标准

1. WHEN 用户执行 `lxr doctor`，THE CLI SHALL 检查并报告以下项目：网络连通性（能否访问理杏仁）、认证状态（token/cookie 是否有效）、字典 freshness（缓存是否存在且未过期）、目录权限（`~/.lxr/` 是否可读写）、依赖版本（Node.js、Playwright 等）
2. WHEN 所有检查项通过，THE CLI SHALL 以退出码 0 退出
3. WHEN 任意检查项失败，THE CLI SHALL 输出具体失败原因和修复建议，并以退出码 1 退出
4. THE CLI SHALL 将 doctor 检查结果输出到 stdout，格式为 table（TTY）或 json（非 TTY）

---

### 需求 13：工程配套

**用户故事：** 作为开发者，我希望工具提供完整的测试套件和示例文件，以便验证工具的正确性并快速上手。

#### 验收标准

1. THE CLI SHALL 在 `examples/` 目录提供至少 5 个常见筛选场景的 Canonical Query YAML 示例文件
2. THE CLI SHALL 提供 golden tests，对 `screen compile` 的输出进行快照测试，验证编译输出的确定性
3. THE CLI SHALL 提供 smoke tests，使用固定的 screener URL 跑全链路验证（需要真实网络和认证）
4. THE CLI SHALL 支持 `lxr schema export` 命令，将 Canonical Query 的 JSON Schema 输出到 stdout，供 Agent 或 IDE 校验 query 文件
5. WHEN 字典缓存存在时，THE CLI SHALL 在 `~/.lxr/dicts/` 目录下维护缓存文件，并记录 `generatedAt` 时间戳用于 TTL 判断
