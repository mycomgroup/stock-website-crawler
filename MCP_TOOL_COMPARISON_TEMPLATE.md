# MCP Tool 数据交互与验证说明文档 (模板)

## 1. 基本信息
- **任务类别**: MCP (Model Context Protocol) 协议工具验证
- **MCP 服务/提供方**: [例如：阿里百炼、OpenAI、本地数据库 MCP 等]
- **工具名称 (Tool Name)**: `[如：fetch_stock_data]`
- **测试时间**: YYYY-MM-DD
- **测试人员**: [填写测试人员姓名]

## 2. 验证目标
通过 MCP (Model Context Protocol) 框架连接特定的服务端工具（如 LLM、搜索引擎、股票数据库），调用其内置的 Tools，测试其**上下文兼容性**、**输入输出格式**、**执行效率**以及**是否满足 Agent 交互标准**。

## 3. Tool 输入/输出结构分析

### 3.1 请求参数 (Input Parameters)
| 参数名 | 必填/选填 | 类型 (Type) | 描述 (Description) | 测试用例/示例值 |
| :--- | :--- | :--- | :--- | :--- |
| **`query`** | [必填] | String | 搜索查询内容 | "苹果公司最新财报" |
| **`limit`** | [选填] | Integer | 返回条数 | 5 |

### 3.2 响应数据 (Output Data)
| 输出字段 (JSON Key) | 数据类型 | 业务含义 | 验证结果 (符合预期/异常/缺失) | 异常说明 |
| :--- | :--- | :--- | :--- | :--- |
| **`results`** | Array | 返回的记录列表 | [符合预期] | 正常返回 5 条 |
| **`snippet`** | String | 摘要或上下文片段 | [异常] | 部分结果为 null 或过短 |
| **`url`** | String | 数据来源链接 | [符合预期] | |

## 4. MCP 上下文与 Agent 交互表现
- **工具描述 (Tool Description)**: 描述是否清晰？Agent (如 Trae、Cursor) 能否根据描述准确理解何时调用此工具？
  - *[分析结果：例如，描述包含 "查询股票行情"，Agent 触发精准。]*
- **错误处理 (Error Handling)**: 当输入无效参数时，MCP 返回的错误信息是否结构化？Agent 能否理解并自动修正？
  - *[分析结果：例如，传入非法日期时，MCP 抛出 400 Bad Request，但错误信息不够语义化。]*
- **响应延迟 (Latency)**: 工具调用的平均耗时？
  - *[分析结果：例如，请求大模型接口约 3-5 秒。]*

## 5. 结论与优化建议
### 5.1 结论概览
*[总结该 MCP Tool 的集成可行性。例如：工具可无缝接入 Agent 工作流，但需要优化 `description` 提示词以提高调用准确率。]*

### 5.2 优化与集成策略 (Next Steps)
- [ ] **直接接入**: [是/否] 接口稳定，提示词描述精准。
- [ ] **调整 Tool Description**: 重新编写 MCP 配置中的工具描述，增加调用示例（Few-Shot）。
- [ ] **参数预处理/后处理**: 增加一层中间件，将用户的自然语言更好地转化为工具所需参数结构，或将输出结果进行 Markdown 渲染后再返回给大模型。

---
**附录：MCP 调用日志示例**
```json
// Request to MCP
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "fetch_stock_data",
    "arguments": {
      "query": "AAPL",
      "limit": 5
    }
  },
  "id": 1
}

// Response from MCP
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[...结果内容...]"
      }
    ],
    "isError": false
  },
  "id": 1
}
```