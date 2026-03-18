---
name: "parser-extractor-pro"
description: "用于开发高兼容性网页解析器的专家技能。当用户希望为新网站开发Parser，或需要解决复杂的网页抽取问题（如SPA、防爬、虚拟列表、折叠内容等）时调用此技能。"
---

# Parser Extractor Pro (网页抽取专家)

这个技能用于帮助开发者以**最少的迭代次数**开发出鲁棒性极强的新网站 Parser（解析器）。它内置了针对现代复杂网页（SPA、防爬机制、复杂表格、动态渲染等）的最佳实践和解决方案。

## 核心设计理念

当你被要求为新网站编写 Parser 时，**不要**直接写简单的 DOM 提取逻辑，因为这样通常会在测试时失败（比如拿不到数据、遇到长表格被截断等）。
你必须**前置性**地应用以下“抽取策略”：

### 1. 强制预处理 (Pre-Processing)
在提取 DOM 数据前，务必执行以下步骤（可直接复用 `BaseParser` 或参考 `GenericParser` 的实现）：
- **SPA 渲染等待**：不要只依赖 `domcontentloaded`，要通过 `waitForContent` 轮询页面文本长度或链接数，确保真实内容已渲染。
- **强制展开折叠内容**：调用或实现 `clickAllExpandButtons`，自动点击所有带有 "展开"、"更多" 字样或 `aria-expanded="false"` 的按钮、Tab和 `<details>` 标签。
- **处理无限滚动**：如果页面是信息流，调用或实现 `handleInfiniteScrollEnhanced`，滚动至底部加载所有懒加载节点。
- **后台 API 嗅探 (杀手锏)**：如果网站 DOM 混淆严重，必须开启 `page.on('response')`，拦截 `/api/` 或 `/data/` 返回的 JSON 数据作为兜底（Fallback）。

### 2. 复杂数据结构的抽取策略
- **长表格 (Pagination & Virtual Lists)**：
  - 如果有分页组件（`.pagination`），需模拟点击“下一页”并增量合并表格。
  - 如果是虚拟列表（如带有 `data-id` 或 `aria-rowindex`），需采用小步长滚动并利用主键去重的方法提取。
- **图表数据 (Canvas/SVG)**：金融数据网站常见，不要试图解析 DOM，直接通过 `page.evaluate` 获取 `window.echarts` 或 `window.Highcharts` 实例中的源数据。

## Parser 开发标准流程

当你执行开发任务时，请遵循以下 4 步以尽量达到“一次性成功”：

### Step 1: 智能分析
如果用户提供了目标 URL，先使用工具（如 `mcp` 的 Chrome devtools，或直接通过 Playwright 测试脚本）分析页面的加载特征：是不是 SPA？数据在 DOM 里还是需要拦截 API？

### Step 2: 编写代码
在 `src/parsers/` 下创建 `<name>-parser.js`。继承 `BaseParser`。
参考以下高兼容性模板结构：

```javascript
import BaseParser from './base-parser.js';

class NewWebsiteParser extends BaseParser {
  matches(url) {
    return url.includes('new-website.com');
  }

  getPriority() {
    return 100; // 确保优先级高于通用解析器
  }

  async parse(page, url, options = {}) {
    // 1. 设置 API 拦截器（作为最强兜底方案）
    const apiData = [];
    page.on('response', async (response) => {
      if (response.url().includes('/api/') && response.status() === 200) {
        try {
          const json = await response.json();
          apiData.push(json);
        } catch (e) {}
      }
    });

    // 2. 强制等待真实内容渲染
    await this.waitForContent(page, { minContentLength: 500, timeout: 15000 });

    // 3. 页面交互预处理 (展开折叠、滚动到底)
    // 根据具体网站实现或复用 base 逻辑
    await this.clickAllExpandButtons(page);
    await this.handleInfiniteScroll(page);

    // 4. 数据提取 (优先 DOM，DOM失败时用 apiData 兜底)
    const result = await page.evaluate(() => {
      // 复杂的 DOM 提取逻辑...
      return { title: document.title, items: [] };
    });

    return {
      type: 'new-website',
      url,
      apiDataFallback: apiData.length > 0 ? apiData : null,
      ...result
    };
  }

  // 辅助方法...
}

export default NewWebsiteParser;
```

### Step 3: 自动注册
在 `src/parsers/parser-manager.js` 中引入并注册该 Parser，确保其实际生效。

### Step 4: 快速验证
完成编写后，不要直接让用户去测。如果你有权限，运行项目中现有的测试脚本（如 `node test-parser.js <URL>`）来验证是否能正确抓取。如果有错，立即自我修复，以达到对用户“一次性完成”的体验。