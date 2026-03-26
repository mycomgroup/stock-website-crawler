import ModelscopeMcpParser from '../src/parsers/modelscope-mcp-parser.js';
import MarkdownGenerator from '../src/parsers/markdown-generator.js';

describe('Modelscope MCP parser + markdown', () => {
  test('parseToolsFromText should extract tool definitions from mixed content', () => {
    const parser = new ModelscopeMcpParser();
    const text = `
工具
网页获取 fetch_page
获取网页内容
输入: url 目标地址
输出: content, status

Search_items
Search tool for remote docs
输入: query 查询词
`;

    const tools = parser.parseToolsFromText(text);
    expect(tools.length).toBeGreaterThan(0);
    expect(tools.some(t => t.name === 'fetch_page')).toBe(true);
  });

  test('generate should keep MCP markdown table rows valid when values include pipes/newlines', () => {
    const generator = new MarkdownGenerator();
    const markdown = generator.generate({
      type: 'modelscope-mcp-server',
      url: 'https://modelscope.cn/mcp/servers/example',
      title: 'Example MCP',
      description: 'desc',
      stats: {
        users: '1,234',
        calls: '56,789',
        avgTime: '120ms',
        toolCount: '12'
      },
      tools: [{
        name: 'search_items',
        displayName: '搜索工具',
        description: '支持关键词 | 过滤',
        inputs: [{ name: 'keyword', type: 'string', required: false, description: '查询词\n支持多行' }],
        outputs: ['items|count']
      }],
      links: []
    });

    expect(markdown).toContain('## 统计数据');
    expect(markdown).toContain('**用户数**: 1,234');
    expect(markdown).toContain('| `keyword` | string | 否 | 查询词<br>支持多行 |');
    expect(markdown).toContain('`items\\|count`');
  });
});
