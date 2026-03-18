/**
 * Debug script to test tokenflux parser for parameter extraction
 */
import TokenfluxParser from './src/parsers/tokenflux-parser.js';
import MarkdownGenerator from './src/parsers/markdown-generator.js';

async function main() {
  const parser = new TokenfluxParser();
  const testUrl = 'https://tokenflux.ai/mcps/EXA_AI';

  console.log(`Testing: ${testUrl}`);
  console.log(`Is MCP detail page: ${parser.isMcpDetailPage(testUrl)}`);

  const mcpId = parser.extractMcpId(testUrl);
  console.log(`MCP ID: ${mcpId}`);

  // 直接测试 API 获取
  console.log('\n=== Testing API Fetch ===');
  const mcpData = await parser.fetchMcpApiData(mcpId);

  if (mcpData) {
    console.log('\n=== MCP Data Summary ===');
    console.log(`Name: ${mcpData.name}`);
    console.log(`Display Name: ${mcpData.display_name}`);
    console.log(`Tools Count: ${mcpData.tools?.length || 0}`);

    // 测试构建 API 端点
    console.log('\n=== API Endpoints ===');
    const apiEndpoints = parser.buildApiEndpointsFromApiData(mcpData);

    for (const ep of apiEndpoints) {
      console.log(`\n${ep.name}:`);
      console.log(`  Method: ${ep.method}`);
      console.log(`  Endpoint: ${ep.endpoint}`);
      console.log(`  Parameters (${ep.parameters.length}):`);
      ep.parameters.slice(0, 5).forEach(p => {
        const req = p.required ? '[Required]' : '[Optional]';
        console.log(`    - ${p.name} (${p.type}) ${req}`);
        if (p.description) {
          console.log(`      ${p.description.substring(0, 60)}...`);
        }
      });
      if (ep.parameters.length > 5) {
        console.log(`    ... and ${ep.parameters.length - 5} more parameters`);
      }
    }

    // 测试完整解析结果
    console.log('\n=== Testing Full Parse ===');
    const content = parser.generateContentFromApiData(mcpData);

    const result = {
      type: 'tokenflux-mcp',
      url: testUrl,
      title: mcpData.display_name || mcpData.name,
      description: mcpData.description || '',
      content,
      links: [],
      method: apiEndpoints.length === 1 ? apiEndpoints[0].method : '',
      endpoint: apiEndpoints.length === 1 ? apiEndpoints[0].endpoint : '',
      parameters: apiEndpoints.length === 1 ? apiEndpoints[0].parameters : [],
      metadata: {
        platform: 'tokenflux',
        mcpId: mcpData.name,
        provider: mcpData.provider,
        toolsCount: mcpData.tools?.length || 0,
        securitySchemes: mcpData.security_schemes,
        apiEndpoints
      }
    };

    console.log('Result metadata.apiEndpoints count:', result.metadata.apiEndpoints?.length);
    console.log('First endpoint params:', result.metadata.apiEndpoints?.[0]?.parameters?.length);

    // 测试 Markdown 生成
    console.log('\n=== Testing Markdown Generation ===');
    const mdGenerator = new MarkdownGenerator();
    const markdown = mdGenerator.generate(result);

    console.log('\n--- Markdown Output (first 3000 chars) ---\n');
    console.log(markdown.substring(0, 3000));

    // 检查参数表格是否正确生成
    console.log('\n\n--- Checking Parameter Table ---');
    const paramTableMatch = markdown.match(/## 请求参数[\s\S]*?(?=##|$)/);
    if (paramTableMatch) {
      console.log('Found Parameters section:');
      console.log(paramTableMatch[0].substring(0, 500));
    } else {
      console.log('No Parameters section found in markdown');
    }

  } else {
    console.log('Failed to fetch MCP data from API');
  }
}

main().catch(console.error);