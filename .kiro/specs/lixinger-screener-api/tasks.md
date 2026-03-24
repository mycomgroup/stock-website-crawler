# 实现计划：lixinger-screener-api

## 概述

按三阶段流程实现：初始化项目结构 → 核心逻辑（LLM 转换 + Playwright 筛选 + CSV 输出）→ CLI 入口与集成。

## 任务

- [x] 1. 初始化项目结构与依赖
  - 在 `skills/lixinger-screener/` 下创建 `package.json`，声明依赖：`playwright`、`openai`、`dotenv`、`fast-check`
  - 创建 `.env.example`，列出所有必要环境变量：`LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL`、`LIXINGER_USERNAME`、`LIXINGER_PASSWORD`
  - _需求：6.4_

- [x] 2. 创建 metrics-catalog.json
  - [x] 2.1 编写 `metrics-catalog.json`，覆盖理杏仁筛选页面所有可用字段
    - 每条目包含 `name`、`displayName`、`category`、`unit`、`operators` 五个字段
    - `operators` 为非空数组，包含 `"大于"`、`"小于"`、`"介于"` 等操作符
    - 覆盖估值、盈利、成长、财务健康等分类
    - _需求：1.1、1.2、1.3_

  - [x] 2.2 为 metrics-catalog 结构完整性编写属性测试
    - **属性 1：metrics-catalog 结构完整性**
    - **验证需求：1.2**
    - 使用 fast-check 生成随机 catalog 条目，验证结构校验函数能正确识别合法/非法条目
    - 测试文件：`skills/lixinger-screener/test/catalog.test.js`

- [x] 3. 实现 main.js 阶段一：LLM 转换
  - [x] 3.1 实现环境变量校验函数 `validateEnv()`
    - 检查必要变量是否存在，缺失时返回具体变量名列表
    - _需求：2.3、2.5、3.5、3.6_

  - [x] 3.2 实现 LLM 转换函数 `queryToScreenerQuery(userQuery, catalog)`
    - 读取 `metrics-catalog.json`，构造 prompt 发送给 LLM（OpenAI 兼容接口）
    - 解析 LLM 返回的 JSON，得到 `ScreenerQuery`
    - LLM 无法解析时输出错误信息 + 可用指标示例
    - _需求：2.1、2.2、2.4_

  - [x] 3.3 实现字段合法性校验函数 `validateScreenerQuery(query, catalog)`
    - 验证每个 filter 的 `field` 值能在 catalog 的 `displayName` 列表中找到
    - 不合法时列出相近字段
    - _需求：2.2_

  - [x] 3.4 为 LLM 转换字段合法性编写属性测试
    - **属性 2：LLM 转换字段合法性**
    - **验证需求：2.1、2.2**
    - 使用 fast-check 生成随机 catalog 和随机 ScreenerQuery，验证 `validateScreenerQuery` 函数
    - 测试文件：`skills/lixinger-screener/test/screener-query.test.js`

- [x] 4. 实现 main.js 阶段二：Playwright 执行筛选
  - [x] 4.1 实现会话管理函数 `loadOrCreateSession(browser)`
    - 从 `.session.json` 加载持久化 Cookie，不存在时使用账号密码登录
    - 登录成功后将 `storageState` 写入 `.session.json`
    - 检测会话失效时自动重新登录并更新文件
    - _需求：3.1、3.2、3.3、3.4_

  - [x] 4.2 实现筛选条件写入函数 `applyFilters(page, filters)`
    - 导航至筛选页面，清除已有条件
    - 按 `ScreenerQuery.filters` 依次添加筛选条件（选择指标、设置操作符和阈值）
    - 找不到字段名时输出错误并停止；操作超时（30 秒）时输出超时错误
    - _需求：4.1、4.2、4.5、4.6_

  - [x] 4.3 实现分页数据抓取函数 `scrapeAllPages(page)`
    - 等待结果更新后抓取当前页表格数据
    - 检测分页控件，自动翻页并合并所有页面数据
    - 返回 `TableRow[]`
    - _需求：4.3、4.4_

  - [x] 4.4 为分页数据合并完整性编写属性测试
    - **属性 3：分页数据合并完整性**
    - **验证需求：4.4**
    - 使用 fast-check 生成随机多页数据，验证合并后行数等于各页之和且无重复行
    - 测试文件：`skills/lixinger-screener/test/pagination.test.js`

- [x] 5. 检查点 - 确保所有测试通过
  - 确保所有测试通过，如有问题请告知。

- [x] 6. 实现 main.js 阶段三：CSV 输出
  - [x] 6.1 实现 limit 截断函数 `applyLimit(rows, limit)`
    - 当 limit 为正整数时截断结果，不超过原始行数
    - _需求：6.3_

  - [x] 6.2 为 limit 参数截断编写属性测试
    - **属性 5：limit 参数截断**
    - **验证需求：6.3**
    - 使用 fast-check 生成随机结果集和随机正整数 limit，验证截断行为
    - 测试文件：`skills/lixinger-screener/test/limit.test.js`

  - [x] 6.3 实现 CSV 格式化函数 `formatCsv(rows)`
    - 第一行为列标题，后续每行字段数与标题一致
    - 处理含逗号、引号的单元格值（RFC 4180 转义）
    - _需求：5.1_

  - [x] 6.4 为 CSV 格式正确性编写属性测试
    - **属性 4：CSV 格式正确性**
    - **验证需求：5.1**
    - 使用 fast-check 生成随机表格数据，验证 CSV 输出格式（标题行、字段数一致性）
    - 测试文件：`skills/lixinger-screener/test/csv.test.js`

  - [x] 6.5 实现 CSV 文件写入逻辑
    - 确保 `output/` 目录存在，写入 `output/screener-{timestamp}.csv`
    - 在命令行输出完整文件路径
    - _需求：5.2、5.3_

- [x] 7. 组装 main.js 导出函数
  - 将三个阶段串联为 `main(options)` 函数：`validateEnv` → `queryToScreenerQuery` → `validateScreenerQuery` → `loadOrCreateSession` → `applyFilters` → `scrapeAllPages` → `applyLimit` → `formatCsv` → 写入文件
  - _需求：2.1–2.5、3.1–3.6、4.1–4.6、5.1–5.3_

- [ ] 8. 实现 run-skill.js CLI 入口
  - 解析 `--query`、`--headless`（默认 true）、`--limit` 参数
  - 加载 `.env`，调用 `validateEnv()`，缺失时输出错误并以退出码 1 退出
  - 调用 `main(options)` 并输出结果路径
  - _需求：6.1、6.2、6.3、6.4_

- [ ] 9. 最终检查点 - 确保所有测试通过
  - 确保所有测试通过，如有问题请告知。

## 备注

- 标有 `*` 的子任务为可选属性测试，可跳过以加快 MVP 进度
- 每个任务引用具体需求条款以保证可追溯性
- 属性测试使用 fast-check，每个属性至少运行 100 次
- 单元测试与属性测试互补，共同覆盖 5 个正确性属性
