# 需求文档

## 简介

为理杏仁股票筛选页面（`https://www.lixinger.com/analytics/screener/company-fundamental/cn`）开发一个 skill，放置在 `skills/lixinger-screener` 目录下。

由于理杏仁 Open API 不提供条件筛选接口，本 skill 使用 Playwright 浏览器自动化直接操作筛选页面 UI，从结果表格中抓取数据，最终输出 CSV 文件。

用户以自然语言描述筛选条件，skill 通过 LLM + 内置的 `metrics-catalog.json` 字段映射表将自然语言转换为页面真实操作参数，再由 Playwright 执行筛选并抓取结果。

## 词汇表

- **metrics-catalog.json**: skill 内置的字段映射表，手工维护，记录理杏仁筛选页面所有可用筛选字段的元数据（中文名、页面真实显示名、支持的操作符等）
- **ScreenerQuery**: LLM 输出的结构化筛选条件，字段名使用 metrics-catalog.json 中定义的页面真实显示名称

---

## 需求

### 需求 1：字段映射表（metrics-catalog.json）

**用户故事：** 作为开发者，我希望 skill 内置一份完整的字段映射表，以便 LLM 能准确地将自然语言映射到页面真实筛选字段。

#### 验收标准

1. THE skill SHALL 在 skill 目录下包含 `metrics-catalog.json` 文件，随 skill 一起加载
2. THE metrics-catalog.json SHALL 为每个筛选字段包含：中文名称、页面真实显示名称（用于 Playwright 操作时匹配 UI 元素）、支持的操作符列表、数值单位（如 %、亿元等）、字段分类（估值/盈利/成长/财务健康等）
3. THE metrics-catalog.json SHALL 覆盖理杏仁筛选页面上所有可用的筛选字段

---

### 需求 2：自然语言转换为筛选条件（LLM 驱动）

**用户故事：** 作为用户，我希望用自然语言描述筛选条件，skill 自动转换为页面可执行的筛选参数。

#### 验收标准

1. WHEN 用户输入自然语言查询，THE skill SHALL 将用户输入与完整的 `metrics-catalog.json` 内容一起发送给 LLM，由 LLM 输出结构化的 ScreenerQuery 对象
2. WHEN LLM 返回 ScreenerQuery 时，每个筛选条件中的字段名 SHALL 为 metrics-catalog.json 中定义的页面真实显示名称
3. THE skill SHALL 通过环境变量 `LLM_API_KEY`、`LLM_BASE_URL`、`LLM_MODEL` 配置 LLM（OpenAI 兼容接口）
4. IF LLM 无法解析用户输入，THEN THE skill SHALL 输出错误信息并提示可用的指标示例
5. IF `LLM_API_KEY` 未配置，THEN THE skill SHALL 输出错误提示并退出

---

### 需求 3：登录与会话管理

**用户故事：** 作为用户，我希望 skill 自动处理理杏仁网站登录，无需手动操作。

#### 验收标准

1. WHEN skill 首次运行且无持久化会话，THE skill SHALL 使用配置的账号密码通过 Playwright 自动完成登录
2. WHEN 登录成功后，THE skill SHALL 将 Cookie 持久化保存到本地文件，供后续复用
3. WHEN 存在持久化会话文件时，THE skill SHALL 优先加载该会话，跳过登录步骤
4. WHEN 检测到会话已失效，THE skill SHALL 自动重新登录并更新持久化会话文件
5. THE skill SHALL 从环境变量 `LIXINGER_USERNAME` 和 `LIXINGER_PASSWORD` 读取登录凭据
6. IF 登录凭据未配置，THEN THE skill SHALL 输出错误提示并退出

---

### 需求 4：Playwright 执行筛选并抓取结果

**用户故事：** 作为用户，我希望 skill 自动将筛选条件写入页面并抓取结果表格。

#### 验收标准

1. WHEN skill 接收到 ScreenerQuery，THE skill SHALL 导航至理杏仁筛选页面并清除已有筛选条件
2. THE skill SHALL 使用 ScreenerQuery 中的页面真实显示名称依次在页面筛选器中添加每个筛选条件（选择指标、设置操作符和阈值）
3. WHEN 所有筛选条件写入完成后，THE skill SHALL 等待页面结果更新，再从结果表格中提取所有行数据
4. WHEN 结果表格包含分页，THE skill SHALL 自动翻页并合并所有页面数据
5. IF 页面中找不到指定的字段名，THEN THE skill SHALL 输出错误信息并停止
6. IF 页面操作超时（默认 30 秒），THEN THE skill SHALL 输出超时错误并退出

---

### 需求 5：输出 CSV 文件

**用户故事：** 作为用户，我希望筛选结果以 CSV 文件形式保存，方便后续分析。

#### 验收标准

1. THE skill SHALL 将筛选结果输出为 CSV 文件，第一行为列标题（股票代码、股票名称及各指标列）
2. THE skill SHALL 将 CSV 文件保存到 `output/` 目录，文件名格式为 `screener-{timestamp}.csv`
3. THE skill SHALL 在命令行输出 CSV 文件的完整路径

---

### 需求 6：命令行接口

**用户故事：** 作为用户，我希望通过命令行运行 skill，传入自然语言查询并获得 CSV 结果。

#### 验收标准

1. THE skill SHALL 提供 `run-skill.js` 入口脚本，支持通过 `--query` 参数传入自然语言查询
2. THE skill SHALL 支持通过 `--headless` 参数控制浏览器是否以无头模式运行（默认无头）
3. THE skill SHALL 支持通过 `--limit` 参数限制返回结果数量（默认返回全部）
4. IF 必要的环境变量未配置，THEN THE skill SHALL 输出错误提示并以非零退出码退出
