const fs = require('fs');
const path = require('path');

/**
 * 将从 API 获取的 MCP 服务说明 JSON 数据转换为统一的 Markdown 格式
 * @param {Object} mcpData API 返回的 MCP 服务数据
 * @param {string} outputPath 输出的 Markdown 文件路径
 */
function generateMcpMarkdown(mcpData, outputPath) {
    const templatePath = path.join(__dirname, 'MCP_SERVICE_TEMPLATE.md');
    let template = fs.readFileSync(templatePath, 'utf-8');

    // 1. 基础信息替换
    template = template.replace(/{MCP_SERVICE_NAME}/g, mcpData.name || '未知 MCP 服务');
    template = template.replace(/{Service Name}/g, mcpData.name || '未知服务');
    template = template.replace(/{A brief description of what this MCP server does}/g, mcpData.description || '无描述');
    template = template.replace(/{Version}/g, mcpData.version || '1.0.0');
    template = template.replace(/{Endpoint or connection method, e.g., stdio command or SSE URL}/g, mcpData.endpoint || '未提供');
    template = template.replace(/\[链接\]\({URL}\)/g, mcpData.documentationUrl ? `[官方文档](${mcpData.documentationUrl})` : '无');

    // 2. 连接与配置替换
    template = template.replace(/{stdio \/ SSE}/g, mcpData.transport || '未提供');
    template = template.replace(/{None \/ API Key \/ OAuth \/ etc.}/g, mcpData.authType || '未提供');
    
    // 环境变量处理
    if (mcpData.envVars && Object.keys(mcpData.envVars).length > 0) {
        const envStr = Object.entries(mcpData.envVars)
            .map(([key, desc]) => `  - \`${key}\`: ${desc}`)
            .join('\n');
        template = template.replace(/  - `ENV_VAR_NAME`: {说明}/g, envStr);
    } else {
        template = template.replace(/  - `ENV_VAR_NAME`: {说明}/g, '  - 无需特殊环境变量');
    }

    // 3. 核心能力 (Capabilities)
    // 3.1 工具 (Tools)
    const toolsSectionRegex = /#### 🔧 工具名称: `{tool_name}`[\s\S]*?(?=\n### 3\.2|\n## 4)/;
    if (mcpData.tools && mcpData.tools.length > 0) {
        const toolsMarkdown = mcpData.tools.map(tool => {
            return `#### 🔧 工具名称: \`${tool.name}\`\n- **描述**: ${tool.description || '无描述'}\n- **参数说明 (Schema)**:\n  \`\`\`json\n  ${JSON.stringify(tool.inputSchema, null, 2).replace(/\n/g, '\n  ')}\n  \`\`\``;
        }).join('\n\n');
        template = template.replace(toolsSectionRegex, toolsMarkdown);
    } else {
        template = template.replace(toolsSectionRegex, '当前服务未提供任何工具。');
    }

    // 3.2 提示词 (Prompts)
    const promptsSectionRegex = /#### 💬 提示词名称: `{prompt_name}`[\s\S]*?(?=\n### 3\.3|\n## 4)/;
    if (mcpData.prompts && mcpData.prompts.length > 0) {
        const promptsMarkdown = mcpData.prompts.map(prompt => {
            const argsStr = prompt.arguments ? prompt.arguments.map(arg => `  - \`${arg.name}\` (${arg.required ? '必填' : '可选'}): ${arg.description}`).join('\n') : '  - 无参数';
            return `#### 💬 提示词名称: \`${prompt.name}\`\n- **描述**: ${prompt.description || '无描述'}\n- **参数**:\n${argsStr}`;
        }).join('\n\n');
        template = template.replace(promptsSectionRegex, promptsMarkdown);
    } else {
        template = template.replace(promptsSectionRegex, '当前服务未提供预设提示词。');
    }

    // 3.3 资源 (Resources)
    const resourcesSectionRegex = /#### 📄 资源: `{resource_name}`[\s\S]*?(?=\n## 4)/;
    if (mcpData.resources && mcpData.resources.length > 0) {
        const resourcesMarkdown = mcpData.resources.map(res => {
            return `#### 📄 资源: \`${res.name}\`\n- **描述**: ${res.description || '无描述'}\n- **URI / 模板**: \`${res.uriTemplate || res.uri}\`\n- **MIME 类型**: \`${res.mimeType || '未知'}\``;
        }).join('\n\n');
        template = template.replace(resourcesSectionRegex, resourcesMarkdown);
    } else {
        template = template.replace(resourcesSectionRegex, '当前服务未公开任何资源。');
    }

    // 写入文件
    fs.writeFileSync(outputPath, template, 'utf-8');
    console.log(`✅ 成功生成 MCP 说明文档: ${outputPath}`);
}

// ================= 测试 / 示例用法 =================
// 假设这是通过 API (如 fetch('https://api.example.com/mcp/info')) 获取到的数据
const mockApiResponse = {
    name: "Weather-MCP-Service",
    description: "提供全球实时天气查询和预报能力的 MCP 服务",
    version: "1.2.0",
    endpoint: "https://mcp.weather-example.com/sse",
    documentationUrl: "https://docs.weather-example.com",
    transport: "SSE",
    authType: "API Key (Bearer Token)",
    envVars: {
        "WEATHER_API_KEY": "访问天气数据的必需密钥",
        "MCP_DEBUG": "是否开启调试模式 (true/false)"
    },
    tools: [
        {
            name: "get_current_weather",
            description: "获取指定城市的当前天气情况",
            inputSchema: {
                type: "object",
                properties: {
                    city: { type: "string", description: "城市名称，如 'Beijing'" },
                    unit: { type: "string", enum: ["celsius", "fahrenheit"], description: "温度单位" }
                },
                required: ["city"]
            }
        }
    ],
    prompts: [
        {
            name: "weather_report_summary",
            description: "根据当前天气生成一份给用户的出行建议报告",
            arguments: [
                { name: "city", required: true, description: "需要报告的城市" }
            ]
        }
    ],
    resources: [
        {
            name: "supported_cities",
            description: "支持查询的城市列表",
            uriTemplate: "weather://cities/supported",
            mimeType: "application/json"
        }
    ]
};

// 执行生成
const outDir = path.join(__dirname, 'output', 'mcp-docs');
if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
}
const outFile = path.join(outDir, `${mockApiResponse.name}.md`);
generateMcpMarkdown(mockApiResponse, outFile);
