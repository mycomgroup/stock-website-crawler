# Hao123 站点爬虫抓取与页面结构验证说明文档 (模板)

## 1. 基本信息
- **任务类别**: Hao123 导航站关联网站抓取
- **目标站点/平台**: [如：新浪体育、东方财富网等]
- **入口 URL**: `[如：http://finance.sina.com.cn/]`
- **测试时间**: YYYY-MM-DD
- **测试人员**: [填写测试人员姓名]

## 2. 抓取目标与范围
针对 Hao123 导航链接进入的各个垂直网站，分析其页面结构、导航菜单、列表页以及详情页的 DOM 树特征，测试并验证 XPath 或 CSS Selector 规则的准确性和鲁棒性。

## 3. 页面结构与提取规则 (Selectors) 验证

| 数据维度 | 页面展示元素 | 提取规则 (XPath/Selector) | 测试结果 (提取成功/异常/空) | 备注/规则修正建议 |
| :--- | :--- | :--- | :--- | :--- |
| **导航菜单 (Nav)** | 顶部全部分类链接 | `//div[@class='nav']//a/@href` | [提取成功] | 获取到 15 个一级类目 |
| **列表项标题 (Title)** | 首页新闻列表区 | `.list-item h2 a` | [提取成功] | 但混杂了广告标题，需过滤 |
| **列表项链接 (Link)** | 新闻的跳转 URL | `.list-item h2 a[href]` | [需修正] | 有部分链接为相对路径 `/a/b/c.html` |
| **发布时间 (Time)** | 列表项旁的日期 | `.time-span` | [异常] | 页面动态渲染，HTML 中无此节点 |
| **正文内容 (Article)** | 详情页主体文字 | `#article-content p` | [提取成功] | |
| **分页 (Pagination)** | 底部“下一页” | `a:contains("下一页")` | [缺失] | 该站使用下拉无限加载 (Infinite Scroll) |

## 4. 动态渲染与反爬分析
- **SPA/客户端渲染**: 页面内容是否由 JavaScript (如 Vue/React) 动态生成？
  - *[分析结果：例如，列表页为静态直出，但价格走势图为 WebSocket 或 Ajax 异步加载。]*
- **验证码/登录墙 (Captcha/Login)**: 访问几页后是否弹出验证码或强制登录？
  - *[分析结果：例如，连续访问 50 页后出现滑块验证。]*
- **IP 封禁风险**: 是否容易触发 403 Forbidden？
  - *[分析结果：例如，单 IP 频次过高被封 24 小时，需配置代理池。]*

## 5. 结论与后续抓取方案
### 5.1 结论概览
*[总结该 Hao123 关联站点的抓取难度。例如：静态页面居多，结构规范，易于解析；但部分链接为相对路径需拼接，且缺乏明确的分页结构，需模拟下拉。]*

### 5.2 爬虫接入策略 (Next Steps)
- [ ] **纯静态抓取 (Cheerio/Axios)**: 页面直出，无反爬，配置快速。
- [ ] **动态渲染抓取 (Puppeteer/Playwright)**: [是/否] 必须等待 JS 执行完毕或模拟滚动，需配置 Headless 浏览器。
- [ ] **代理与频控**: 必须使用高匿代理，设置请求间隔 (Delay: 3s)。
- [ ] **重构解析规则**: [列出需要修改的 XPath 或 CSS 选择器]

---
**附录：典型 HTML 结构片段与解析代码**
### 目标 DOM 结构示例
```html
<div class="news-list">
  <div class="item">
    <h2><a href="/news/123.html">今日股市行情...</a></h2>
    <span class="date">2023-10-27</span>
  </div>
</div>
```

### 调试代码片段 (Puppeteer/Cheerio)
```javascript
// 在此处粘贴调试通过的核心提取逻辑
const items = $('.news-list .item').map((i, el) => {
  return {
    title: $(el).find('h2 a').text().trim(),
    link: 'https://example.com' + $(el).find('h2 a').attr('href'),
    date: $(el).find('.date').text().trim()
  };
}).get();
```