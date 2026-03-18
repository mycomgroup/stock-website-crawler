# {MCP_SERVICE_NAME} 服务说明文档

## 1. 基础信息

- **服务名称**: {Service Name}
- **服务描述**: {A brief description of what this MCP server does}
- **版本**: {Version}
- **基础 URL / Endpoint**: {Endpoint or connection method, e.g., stdio command or SSE URL}
- **官方文档**: [链接]({URL})

## 2. 连接与配置

- **传输协议**: {stdio / SSE}
- **认证方式**: {None / API Key / OAuth / etc.}
- **环境变量/配置项**:
  - `ENV_VAR_NAME`: {说明}

## 3. 核心能力 (Capabilities)

### 3.1 工具 (Tools)

该服务提供了以下可供大模型调用的工具：

#### 🔧 工具名称: `{tool_name}`
- **描述**: {工具的详细描述}
- **参数说明 (Schema)**:
  ```json
  {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "参数1描述"
      }
    },
    "required": ["param1"]
  }
  ```

*(根据实际 API 返回结果循环填充工具列表)*

### 3.2 提示词 (Prompts)

该服务提供了以下预设提示词模板：

#### 💬 提示词名称: `{prompt_name}`
- **描述**: {提示词的详细描述}
- **参数**:
  - `arg1` (类型): 描述

### 3.3 资源 (Resources)

该服务公开了以下数据资源：

#### 📄 资源: `{resource_name}`
- **描述**: {资源的详细描述}
- **URI / 模板**: `{resource_uri_template}`
- **MIME 类型**: `{mime_type}`

## 4. API 获取方式说明

> **说明**: 以下是获取上述 MCP 数据的 API 调用示例（如果该服务提供了 HTTP/REST 形式的查询 API，或者通过 MCP Inspector/Client 协议获取）。

### 获取服务元数据
```bash
# 示例：通过特定的 HTTP 端点或 MCP 协议握手获取
# TODO: 根据具体 MCP 服务的 API 补充
```

### 获取工具列表
```bash
# 示例：
# TODO: 根据具体 MCP 服务的 API 补充
```

## 5. 常见问题与限制 (FAQ & Limitations)

- **调用频率限制**: {Rate limits}
- **已知问题**: {Known issues}
- **其他**: {Others}
