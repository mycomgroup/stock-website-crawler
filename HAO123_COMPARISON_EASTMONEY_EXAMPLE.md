# Hao123 站点爬虫抓取与页面结构验证说明文档 (东方财富示例)

## 1. 基本信息
- **任务类别**: Hao123 导航站关联网站抓取
- **目标站点/平台**: 东方财富网 (EastMoney)
- **入口 URL**: `http://finance.eastmoney.com/` (由 Hao123 财经频道引流)
- **测试时间**: 2026-03-17
- **测试人员**: Trae AI

## 2. 抓取目标与范围
针对东方财富网首页及新闻列表页，分析其 DOM 结构特征，验证提取“新闻标题”、“发布时间”及“文章链接”的 XPath 或 CSS Selector 规则，并评估其反爬严格程度。

## 3. 页面结构与提取规则 (Selectors) 验证

| 数据维度 | 页面展示元素 | 提取规则 (XPath/Selector) | 测试结果 (提取成功/异常/空) | 备注/规则修正建议 |
| :--- | :--- | :--- | :--- | :--- |
| **导航菜单 (Nav)** | 顶部黑色导航条 | `.nav-bar .menu-item > a` | 提取成功 | 可获取到 股票、理财、基金 等子频道 |
| **列表项标题 (Title)** | 中部滚动新闻列表 | `#newsList li .title a` | 提取成功 | 需要过滤包含 `class="ad"` 的推广链接 |
| **列表项链接 (Link)** | 新闻的跳转 URL | `#newsList li .title a[href]` | 需修正 | 获取的 URL 为 `//finance.eastmoney.com/a/123.html`，缺少 `http:` 协议头，需用代码补全 |
| **发布时间 (Time)** | 列表项旁的日期 | `#newsList li .time` | 异常 | 首页仅显示 `MM-DD`，不含年份；需进入详情页获取完整时间 |
| **正文内容 (Article)** | 详情页主体文字 | `#ContentBody p` | 提取成功 | 包含多段文本，使用 `.map((i, el) => $(el).text()).join('\n')` 提取 |
| **分页 (Pagination)** | 底部“下一页” | `.page .next` | 缺失 | 首页为 Ajax 异步加载，非传统 `<a>` 标签分页 |

## 4. 动态渲染与反爬分析
- **SPA/客户端渲染**: 
  - 新闻列表**首屏**是服务端直出 (SSR)，可直接用 Cheerio 抓取。
  - **下拉加载 (Load More)** 是通过 Ajax 请求 `/api/news/list` 动态拉取 JSON 数据。
- **验证码/登录墙 (Captcha/Login)**: 暂未发现强制登录墙，但在极高频并发下 (如 >50 qps)，会弹出图形验证码拦截。
- **IP 封禁风险**: 较高。频繁刷新行情接口会导致单 IP 临时封禁 (403 Forbidden)。

## 5. 结论与后续抓取方案
### 5.1 结论概览
东方财富网的 HTML 结构相对稳定，首屏抓取非常容易。但它采用了典型的混合渲染机制：首屏静态 + 滚动动态。如果只抓取最新 Top 20，静态爬虫足以胜任；如果需要深度遍历，必须破解其 API 或使用自动化浏览器。

### 5.2 爬虫接入策略 (Next Steps)
- [ ] **纯静态抓取 (Cheerio/Axios)**: 仅适用于只抓取首页首屏新闻的需求。
- [x] **动态渲染抓取 (Puppeteer/Playwright)**: **推荐**。配置 Playwright 并模拟页面向下滚动，触发并拦截 `/api/news/list` 的 Ajax 响应。
- [x] **重构解析规则**: 
  - 将相对协议链接 `//finance.eastmoney.com` 补全为 `https://finance.eastmoney.com`。
  - 时间字段改为从 Ajax 响应的 JSON 中直接读取时间戳，而不是从 HTML 提取。

---
**附录：典型 HTML 结构片段与解析代码**
### 调试代码片段 (Playwright 拦截)
```javascript
// 使用 Playwright 拦截 Ajax 接口，比解析 DOM 更稳定
page.on('response', async response => {
  if (response.url().includes('/api/news/list') && response.status() === 200) {
    const data = await response.json();
    const articles = data.items.map(item => ({
      title: item.title,
      link: item.url,
      time: item.publish_time // 直接获取精确时间
    }));
    console.log(articles);
  }
});
```