# 解析器 (Parsers) 抽取方案总结

本文档总结了项目中现有的解析器（Parser）生态，特别是梳理了过去在抓取各种网站和API文档时遇到的问题以及相应的解决方案。这些经验将作为后续开发通用技能（Skill）和适配新网站的重要参考。

## 1. 解析器架构概览

目前项目中包含了近 **50个** 解析器，它们遵循面向对象的架构设计：
- **`base-parser.js`**：所有解析器的基类，提供基础的 DOM 等待、表格提取、代码块提取等通用工具。
- **`parser-manager.js`**：解析器注册和路由中心。根据目标 URL（`matches` 方法）或页面内容特征（`detectByContent` 置信度评分）智能分发给最合适的解析器。
- **Generic (通用) 解析器**：处理常见页面布局（如 `generic-parser.js`, `article-parser.js`, `list-page-parser.js` 等）。
- **Specific (专用) 解析器**：处理特定网站、平台或特定 API 厂商的非标准结构。

## 2. 已解决的核心问题与技术方案

在处理现代复杂 Web 页面时，系统已经沉淀了以下核心解决方案：

### 2.1 动态渲染与单页应用 (SPA)
- **问题**：很多网站使用 React/Vue，通过 `DOMContentLoaded` 时页面仍为空白。
- **解决方案**：在基类中引入 `waitForContent`。除了等待 `networkidle`，还通过检测全局变量（如 `window.Vue`, `__REACT_DEVTOOLS_GLOBAL_HOOK__`）识别 SPA，并使用 `page.waitForFunction` 轮询检查页面文本长度或链接数量，确保内容真实渲染完毕。

### 2.2 隐藏与折叠内容
- **问题**：许多关键数据被隐藏在 "展开更多"、手风琴折叠（Accordion）、Tab 切换页或 `<details>` 标签中。
- **解决方案**：`generic-parser.js` 实现了 `clickAllExpandButtons`，通过常见文本（"更多", "展开", "Load More"）、ARIA 属性 (`aria-expanded="false"`) 和常见类名遍历点击，自动展开所有折叠块，并在提取前触发重绘。对于 Tab 页，会自动遍历点击并捕捉状态变化后的 DOM。

### 2.3 复杂表格（分页与虚拟列表）
- **问题**：金融数据表格往往极长，有的通过 Ajax 分页，有的使用虚拟列表（Virtual DOM，如 React-Window），导致直接提取只能拿到当前视口的几行。
- **解决方案**：
  - **分页表格**：识别 `.pagination` 控件，模拟点击“下一页”并增量合并表格数据。
  - **虚拟表格**：在 `extractVirtualTable` 中，识别虚拟滚动容器（基于 `data-id` 或特定的 class），通过小步长自动滚动触发新数据渲染，利用主键（Row Key）去重，直到滚动到底部。

### 2.4 图表数据盲区 (Canvas / SVG)
- **问题**：金融页面的 K线图和柱状图多使用 ECharts 或 HighCharts 绘制，DOM 中只有 `<canvas>`，无法提取具体数值。
- **解决方案**：`extractChartData` 方案不直接读 DOM，而是拦截页面上下文中的图表实例（如 `window.echarts.getInstanceByDom(el)` 或 `window.Highcharts.charts`），直接抽取出底层绑定的 JSON 序列数据（X轴、Y轴、Series）。

### 2.5 后台 API 嗅探
- **问题**：某些页面的 DOM 结构极度复杂或做了混淆防爬。
- **解决方案**：在 `generic-parser` 中开启 Playwright 的 `page.on('response')` 拦截器。专门监听 `/api/`, `/data/` 等路径，如果返回 JSON 数组，直接将这些数据转换为结构化表格作为备用提取结果。

### 2.6 无限滚动 (Infinite Scroll)
- **问题**：信息流页面没有分页按钮，依靠滚动到底部加载更多。
- **解决方案**：`handleInfiniteScrollEnhanced` 结合了滚动窗口和滚动局部容器两种模式。通过对比页面 Hash（文本长度和末尾内容）判断是否还在加载新内容，同时识别“已经到底”等终止词汇防死循环。

### 2.7 交互式筛选 (如日期过滤)
- **问题**：默认页面只展示近期数据，需要手动筛选才能获取历史全量数据。
- **解决方案**：实现了 `findAndProcessDateFilters`，自动识别带有 "开始/结束" 语义的日期输入框，尝试填充诸如 "2000-01-01" 到今天的日期，并触发查询按钮获取全量历史表格。

### 2.8 特定平台的文档结构 (如 Mintlify, Apify, Finnhub)
- **问题**：通用解析器提取这些站点的文档时噪音太大（例如带入大量代码块旁边的 Copy 按钮文本）。
- **解决方案**：针对主流文档平台开发特定 Parser。例如 `mintlify-parser.js` 专攻 `.mdx-content` 类，并处理其特有的 `info`/`warning` 警告框；`finnhub-api-parser.js` 结合页面上挂载的 `window.docSchema` 直接与 DOM 进行映射匹配，精准抽出接口参数。

## 3. 现有解析器分类一览

| 类别 | 典型 Parser 文件 | 职责 / 适用场景 |
| :--- | :--- | :--- |
| **基础与通用** | `base-parser.js`, `generic-parser.js` | 提供兜底解析能力，集成了上述所有复杂的交互模拟方案。 |
| **页面布局类** | `article-parser.js`, `list-page-parser.js`, `api-doc-parser.js`, `ecommerce-parser.js` | 通过识别特定布局（如新闻正文、商品价格、API请求参数表格）来清洗侧边栏、广告等噪音。 |
| **SaaS/文档平台** | `mintlify-parser.js`, `apify-api-parser.js`, `tokenflux-parser.js` | 专门适配基于这类生成器搭建的站点，精准剥离框架带来的额外 DOM 节点。 |
| **金融与量化API** | `finnhub-api-parser.js`, `yfinance-api-parser.js`, `tushare-pro-api-parser.js`, `sanhulianghua-parser.js` | 解析特定提供商的文档结构，特别是针对他们非标准的表格排版和隐藏数据进行专项处理。 |
| **大模型MCP API** | `aliyun-bailian-mcp-parser.js`, `modelscope-mcp-parser.js` | 针对目前新兴的 AI 接口和 MCP 协议规范文档的专项抽取。 |

## 4. 后续开发 Skill 的启示

为了实现“如果有新的网站能尽可能多的一次性成功”，新的 Skill 可以借鉴以下思路：

1. **组合拳而非单一策略**：新网站进来时，优先使用内容特征检测（`detectByContent`）而非仅依赖 URL 匹配。
2. **先交互后抽取**：必须强制执行“滚动到底部”、“点击所有展开按钮”、“拦截 API 响应”这三步预处理，再进行 DOM 解析。
3. **数据兜底机制**：如果 DOM 提取失败或太乱，退而求其次去查看拦截到的后台 API JSON 数据，或者查看 ECharts 等图表实例的数据。
4. **内容清洗前置**：在提取前，通过统一的黑名单选择器（移除 nav, footer, sidebar, ads, script 等）先对 DOM 树进行净化。