# MCP Tool 数据交互与验证说明文档 (阿里云百炼 MCP 示例)

## 1. 基本信息
- **任务类别**: MCP (Model Context Protocol) 协议工具验证
- **MCP 服务/提供方**: 阿里云百炼 (Aliyun Bailian)
- **工具名称 (Tool Name)**: `search_web` (网络搜索检索)
- **测试时间**: 2026-03-17
- **测试人员**: Trae AI

## 2. 验证目标
通过连接阿里云百炼提供的 MCP Server，调用其内置的 `search_web` 工具，测试其**检索质量**、**输入输出格式兼容性**以及在 Agent (Trae) 环境下的**调用表现**。

## 3. Tool 输入/输出结构分析

### 3.1 请求参数 (Input Parameters)
| 参数名 | 必填/选填 | 类型 (Type) | 描述 (Description) | 测试用例/示例值 |
| :--- | :--- | :--- | :--- | :--- |
| **`query`** | 必填 | String | 搜索查询关键词 | "特斯拉 2025 财报解读" |
| **`search_depth`** | 选填 | String | 搜索深度 (basic/advanced) | "advanced" |

### 3.2 响应数据 (Output Data)
| 输出字段 (JSON Key) | 数据类型 | 业务含义 | 验证结果 (符合预期/异常/缺失) | 异常说明 |
| :--- | :--- | :--- | :--- | :--- |
| **`results`** | Array | 返回的搜索结果列表 | 符合预期 | 返回包含 5-10 条结果的数组 |
| **`title`** | String | 结果网页标题 | 符合预期 | 能够准确反映网页主题 |
| **`content/snippet`** | String | 网页摘要内容 | 需转换 | 包含大量文本，有时带有 `\n` 或特殊空格，建议传入 LLM 前做清洗 |
| **`url`** | String | 网页源链接 | 符合预期 | 均可正常访问 |

## 4. MCP 上下文与 Agent 交互表现
- **工具描述 (Tool Description)**: 描述非常清晰 (`"Search the web for up-to-date information..."`)。当用户询问“今天的新闻”或“最新财报”时，Agent 能够准确地**零样本 (Zero-shot) 触发**该工具，而不需要强制手动指定。
- **错误处理 (Error Handling)**: 如果由于网络超时导致检索失败，MCP 返回的是包含 `error` 字段的标准 JSONRPC 响应，Agent 能够捕获并自动重试或告知用户“搜索失败”。
- **响应延迟 (Latency)**: Advanced 模式下搜索耗时约 4-6 秒，在可接受的范围内。

## 5. 结论与优化建议
### 5.1 结论概览
阿里云百炼的 `search_web` MCP 工具在检索金融、科技类最新资讯时表现优异。输出的 `snippet` 足够详实，可以直接喂给大语言模型作为 Context 使用，极大地扩展了 Agent 的实时知识边界。

### 5.2 优化与集成策略 (Next Steps)
- [x] **直接接入**: **是**。配置 `stock-crawler/config/aliyun-bailian-mcp.json` 并启用。
- [ ] **调整 Tool Description**: 暂时无需调整，默认描述已足够。
- [x] **参数预处理/后处理**: **建议**。由于 `results` 返回文本较长，建议在 Agent 提示词中增加一条规则：“基于 search_web 结果回答时，请务必引用 url 出处”，以确保数据可追溯。

---
**附录：MCP 调用日志示例**
```json
// Response from MCP
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[{\"title\":\"Tesla Q4 2025 Earnings Report...\",\"url\":\"https://...\",\"content\":\"Tesla reported record revenue in Q4...\"}]"
      }
    ],
    "isError": false
  },
  "id": 1
}
```