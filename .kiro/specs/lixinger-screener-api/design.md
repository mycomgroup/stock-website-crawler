# 设计文档：lixinger-screener-api

## 概述

本 skill 为理杏仁股票筛选页面提供自然语言驱动的自动化筛选能力。用户输入自然语言描述的筛选条件，skill 通过 LLM 将其转换为结构化查询，再由 Playwright 操作浏览器执行筛选，最终将结果表格导出为 CSV 文件。

整体设计遵循简单原则：单一目录、少量文件、无复杂抽象层。

## 架构

```
用户自然语言输入
        │
        ▼
  LLM（OpenAI 兼容）
  + metrics-catalog.json
        │
        ▼
  ScreenerQuery（结构化筛选条件）
        │
        ▼
  Playwright 操作浏览器
  https://www.lixinger.com/analytics/screener/company-fundamental/cn
        │
        ▼
  抓取结果表格（含分页）
        │
        ▼
  输出 CSV 文件（output/screener-{timestamp}.csv）
```

### 目录结构

```
skills/lixinger-screener/
├── run-skill.js          # CLI 入口，解析参数，调用 main.js
├── main.js               # 核心逻辑：LLM 转换 + Playwright 操作 + CSV 输出
├── metrics-catalog.json  # 字段映射表（手工维护）
└── .env.example          # 环境变量示例
```

## 组件与接口

### run-skill.js

CLI 入口，负责：
- 解析命令行参数（`--query`、`--headless`、`--limit`）
- 校验必要环境变量，缺失时输出错误并以非零退出码退出
- 调用 `main(options)` 并输出结果路径

```
node run-skill.js --query "PE小于20，ROE大于15%" [--headless] [--limit 100]
```

### main.js

核心逻辑，导出 `main(options)` 函数，内部分三个阶段：

**阶段 1：LLM 转换**
- 读取 `metrics-catalog.json`
- 构造 prompt，将用户查询 + catalog 发送给 LLM
- 解析 LLM 返回的 JSON，得到 `ScreenerQuery`

**阶段 2：Playwright 执行筛选**
- 加载或创建浏览器会话（Cookie 持久化）
- 导航至筛选页面，清除已有条件
- 按 `ScreenerQuery` 依次添加筛选条件
- 等待结果更新，抓取表格数据（含分页）

**阶段 3：输出 CSV**
- 将表格数据格式化为 CSV
- 保存到 `output/screener-{timestamp}.csv`
- 返回文件路径

### metrics-catalog.json

字段映射表，结构如下：

```json
[
  {
    "name": "市盈率(TTM)",
    "displayName": "市盈率(TTM)",
    "category": "估值",
    "unit": "倍",
    "operators": ["大于", "小于", "介于"]
  },
  {
    "name": "净资产收益率(TTM)",
    "displayName": "净资产收益率(TTM)",
    "category": "盈利",
    "unit": "%",
    "operators": ["大于", "小于", "介于"]
  }
]
```

字段说明：
- `name`：中文名称（用于 LLM 理解）
- `displayName`：页面真实显示名称（用于 Playwright 匹配 UI 元素）
- `category`：字段分类（估值/盈利/成长/财务健康等）
- `unit`：数值单位
- `operators`：支持的操作符列表

## 数据模型

### ScreenerQuery

LLM 输出的结构化筛选条件：

```typescript
interface ScreenerFilter {
  field: string;      // metrics-catalog.json 中的 displayName
  operator: string;   // 操作符，如 "大于"、"小于"、"介于"
  value: number | [number, number];  // 阈值，介于时为 [min, max]
}

interface ScreenerQuery {
  filters: ScreenerFilter[];
}
```

示例：
```json
{
  "filters": [
    { "field": "市盈率(TTM)", "operator": "小于", "value": 20 },
    { "field": "净资产收益率(TTM)", "operator": "大于", "value": 15 }
  ]
}
```

### TableRow

从页面抓取的一行数据：

```typescript
interface TableRow {
  [columnName: string]: string;  // 列名 -> 单元格值
}
```

### 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `LLM_API_KEY` | 是 | LLM API 密钥 |
| `LLM_BASE_URL` | 否 | LLM API 地址（默认 OpenAI） |
| `LLM_MODEL` | 否 | 模型名称（默认 gpt-4o） |
| `LIXINGER_USERNAME` | 是 | 理杏仁账号 |
| `LIXINGER_PASSWORD` | 是 | 理杏仁密码 |

### Cookie 持久化

会话文件保存路径：`~/.lixinger-screener/session.json`（或 skill 目录下的 `.session.json`）

格式为 Playwright 的 `storageState` JSON 格式。

## 正确性属性

*属性（Property）是在系统所有有效执行中都应成立的特征或行为——本质上是对系统应该做什么的形式化陈述。属性是人类可读规范与机器可验证正确性保证之间的桥梁。*

### 属性 1：metrics-catalog 结构完整性

*对于* metrics-catalog.json 中的任意条目，该条目都应包含 `name`、`displayName`、`category`、`unit`、`operators` 五个字段，且 `operators` 为非空数组。

**验证需求：1.2**

### 属性 2：LLM 转换字段合法性

*对于* 任意用户输入，LLM 返回的 ScreenerQuery 中每个 filter 的 `field` 值都应能在 metrics-catalog.json 的 `displayName` 列表中找到。

**验证需求：2.1、2.2**

### 属性 3：分页数据合并完整性

*对于* 任意包含多页的结果表格，合并后的数据行数应等于各页行数之和，且不存在重复行。

**验证需求：4.4**

### 属性 4：CSV 格式正确性

*对于* 任意非空的表格数据，生成的 CSV 文件第一行应为列标题，后续每行应与对应的数据行字段数一致。

**验证需求：5.1**

### 属性 5：limit 参数截断

*对于* 任意结果集和任意正整数 limit，应用 limit 后返回的行数应不超过 limit，且不超过原始行数。

**验证需求：6.3**

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| 必要环境变量缺失 | 输出具体缺失的变量名，以退出码 1 退出 |
| LLM 返回无效 JSON | 输出错误信息 + 可用指标示例，退出 |
| LLM 返回字段名不在 catalog 中 | 输出错误信息，列出相近字段，退出 |
| 页面中找不到指定字段名 | 输出错误信息，停止执行 |
| 页面操作超时（30 秒） | 输出超时错误，退出 |
| 登录失败 | 输出错误信息，退出 |
| 会话失效 | 自动重新登录，更新 session 文件 |

## 测试策略

### 单元测试

针对纯函数逻辑，不依赖浏览器或 LLM：

- `metrics-catalog.json` 结构验证（属性 1）
- CSV 格式化函数（属性 4）
- limit 截断函数（属性 5）
- 分页数据合并函数（属性 3）
- 环境变量校验函数（示例测试）
- 参数解析函数（示例测试）

### 属性测试

使用 [fast-check](https://github.com/dubzzz/fast-check)（JavaScript PBT 库），每个属性测试运行最少 100 次：

**属性测试 1：metrics-catalog 结构完整性**
```
// Feature: lixinger-screener-api, Property 1: metrics-catalog 结构完整性
// 生成随机 catalog 条目，验证结构校验函数能正确识别合法/非法条目
```

**属性测试 2：LLM 转换字段合法性**
```
// Feature: lixinger-screener-api, Property 2: LLM 转换字段合法性
// 生成随机 catalog 和随机 ScreenerQuery，验证字段合法性校验函数
```

**属性测试 3：分页数据合并完整性**
```
// Feature: lixinger-screener-api, Property 3: 分页数据合并完整性
// 生成随机多页数据，验证合并后行数等于各页之和
```

**属性测试 4：CSV 格式正确性**
```
// Feature: lixinger-screener-api, Property 4: CSV 格式正确性
// 生成随机表格数据，验证 CSV 输出格式
```

**属性测试 5：limit 参数截断**
```
// Feature: lixinger-screener-api, Property 5: limit 参数截断
// 生成随机结果集和随机 limit 值，验证截断行为
```

### 集成测试（手动）

- 完整流程端到端测试（需要真实账号和网络）
- 登录 + 筛选 + CSV 输出验证
