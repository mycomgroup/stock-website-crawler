import { chromium } from 'playwright';

async function inspectToolsSection() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  const url = 'https://modelscope.cn/mcp/servers/@baidu-maps/mcp';
  console.log(`Inspecting: ${url}\n`);

  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(5000);

  // 查找工具相关的元素
  const toolsInfo = await page.evaluate(() => {
    const result = {
      toolSections: [],
      toolCards: [],
      codeElements: []
    };

    // 查找 "Available Tools" 或 "工具" 标题
    const allH2 = document.querySelectorAll('h2');
    allH2.forEach(h2 => {
      const text = h2.textContent.trim().toLowerCase();
      if (text.includes('tool') || text.includes('工具')) {
        result.toolSections.push({
          text: h2.textContent.trim(),
          className: h2.className,
          id: h2.id
        });
      }
    });

    const allH3 = document.querySelectorAll('h3');
    allH3.forEach(h3 => {
      const text = h3.textContent.trim().toLowerCase();
      if (text.includes('tool') || text.includes('工具')) {
        result.toolSections.push({
          text: h3.textContent.trim(),
          className: h3.className,
          id: h3.id
        });
      }
    });

    // 查找可能包含工具信息的卡片或列表
    const toolCards = document.querySelectorAll('[class*="tool"], [class*="function"], [class*="api"]');
    toolCards.forEach(card => {
      const text = card.textContent.trim().substring(0, 200);
      if (text.length > 10 && text.length < 500) {
        result.toolCards.push({
          className: card.className,
          text: text
        });
      }
    });

    // 查找代码块
    const codeElements = document.querySelectorAll('pre, code, [class*="code"]');
    codeElements.forEach(el => {
      const text = el.textContent.trim();
      const parent = el.parentElement;
      const parentClass = parent?.className || '';
      result.codeElements.push({
        tag: el.tagName,
        className: el.className,
        parentClass: parentClass,
        text: text.substring(0, 300),
        length: text.length
      });
    });

    return result;
  });

  console.log('Tool sections found:');
  toolsInfo.toolSections.forEach((s, i) => console.log(`  ${i + 1}. ${s.text}`));

  console.log('\nTool cards found:');
  toolsInfo.toolCards.slice(0, 5).forEach((c, i) => {
    console.log(`  ${i + 1}. [${c.className}]: ${c.text.substring(0, 100)}...`);
  });

  console.log('\nCode elements (first 10):');
  toolsInfo.codeElements.slice(0, 10).forEach((c, i) => {
    console.log(`  ${i + 1}. ${c.tag}.${c.className || 'no-class'} (parent: ${c.parentClass?.substring(0, 30) || 'none'})`);
    console.log(`     Length: ${c.length}`);
    console.log(`     Preview: ${c.text.substring(0, 80)}...`);
  });

  // 获取完整的工具信息
  const detailedTools = await page.evaluate(() => {
    const tools = [];

    // 尝试找到工具描述的结构
    // ModelScope 可能在特定容器中显示工具信息

    // 查找工具名称 - 通常在某个特定元素中
    const main = document.querySelector('main');
    const text = main?.innerText || '';

    // 尝试解析工具信息
    // 工具通常有类似这样的格式：
    // map_geocode - 地理编码服务
    // 参数: address (string, required)

    const lines = text.split('\n');
    let currentTool = null;

    lines.forEach((line, i) => {
      const trimmed = line.trim();

      // 检测工具定义行 (工具名 - 描述 或 工具名(参数))
      const toolMatch = trimmed.match(/^([a-z_][a-z0-9_]*)\s*[-–]\s*(.+)$/i);
      if (toolMatch) {
        if (currentTool) tools.push(currentTool);
        currentTool = {
          name: toolMatch[1],
          description: toolMatch[2],
          parameters: []
        };
      }

      // 检测参数行
      const paramMatch = trimmed.match(/^([a-z_][a-z0-9_]*)\s*[\(（]?\s*(string|integer|boolean|number|object|array)?\s*,?\s*(required|optional)?\s*[\)）]?\s*[-–:]?\s*(.*)$/i);
      if (paramMatch && currentTool) {
        currentTool.parameters.push({
          name: paramMatch[1],
          type: paramMatch[2] || 'string',
          required: paramMatch[3] === 'required',
          description: paramMatch[4] || ''
        });
      }
    });

    if (currentTool) tools.push(currentTool);

    return {
      tools,
      rawText: text
    };
  });

  console.log('\n\nParsed tools:');
  detailedTools.tools.forEach((t, i) => {
    console.log(`\n${i + 1}. ${t.name}: ${t.description}`);
    if (t.parameters.length > 0) {
      t.parameters.forEach(p => {
        console.log(`   - ${p.name} (${p.type}, ${p.required ? 'required' : 'optional'}): ${p.description}`);
      });
    }
  });

  // 查看原始文本中的工具部分
  const toolSectionText = await page.evaluate(() => {
    const main = document.querySelector('main');
    const text = main?.innerText || '';

    // 找到 "Available Tools" 部分
    const toolsIndex = text.toLowerCase().indexOf('available tools');
    if (toolsIndex >= 0) {
      return text.substring(toolsIndex, toolsIndex + 2000);
    }

    // 或找 "工具" 部分
    const toolsCnIndex = text.indexOf('工具');
    if (toolsCnIndex >= 0) {
      return text.substring(toolsCnIndex, toolsCnIndex + 2000);
    }

    return text.substring(0, 3000);
  });

  console.log('\n\nTools section from raw text:');
  console.log(toolSectionText);

  await browser.close();
}

inspectToolsSection().catch(console.error);