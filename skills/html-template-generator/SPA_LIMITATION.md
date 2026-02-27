# SPA 应用限制说明

## 问题诊断

html-template-generator skill 在处理理杏仁网站时**完全失败**，无法提取任何内容。

## 根本原因

### 1. 理杏仁是 Vue.js 单页应用（SPA）

```html
<div id="app" class="position-absolute w-100 d-flex flex-column">
  <!-- 内容通过 JavaScript 动态渲染 -->
</div>
```

### 2. HTML 结构特点

- **初始 HTML 几乎为空**: 只有基本的 `<div id="app">` 容器
- **内容动态加载**: 所有数据通过 JavaScript/Vue 渲染
- **XPath 无法匹配**: 因为目标元素在初始 HTML 中不存在

### 3. 测试结果

```bash
Testing sections xpath: //div[@class='content']
Found sections: 0  # ❌ 找不到任何元素
```

## 为什么会失败

### 当前实现流程

```
1. Playwright 加载页面
2. 等待 networkidle (网络空闲)
3. 等待 1 秒
4. 获取 HTML
5. 使用 XPath 提取内容  # ❌ 此时 Vue 还在渲染
```

### SPA 的实际加载流程

```
1. 加载基础 HTML (几乎为空)
2. 加载 JavaScript 文件
3. JavaScript 执行
4. Vue 初始化
5. 发起 API 请求
6. 接收数据
7. 渲染 DOM  # ← 内容在这里才出现
```

## 解决方案

### 方案 1: 使用 API（推荐）

理杏仁有开放 API：`https://www.lixinger.com/open/api/doc`

```javascript
// 直接调用 API 获取数据
const response = await fetch('https://api.lixinger.com/...');
const data = await response.json();
```

**优点**:
- 直接获取结构化数据
- 不需要解析 HTML
- 速度快、稳定

### 方案 2: 等待特定元素（不推荐）

修改 HTMLFetcher 等待特定元素：

```javascript
// 等待内容加载
await page.waitForSelector('.content', { timeout: 30000 });
await page.waitForTimeout(2000); // 额外等待
```

**缺点**:
- 不同页面需要不同的等待策略
- 仍然可能不稳定
- 速度慢

### 方案 3: 使用 stock-crawler 的现有 parser

stock-crawler 已经有针对理杏仁的 parser：
- `src/parsers/generic-parser.js`
- `src/parsers/api-doc-parser.js`

这些 parser 已经处理了动态内容加载。

## 结论

**html-template-generator skill 不适合 SPA 应用**

### 适用场景

✅ 静态 HTML 网站
✅ 服务端渲染（SSR）网站
✅ 传统多页应用（MPA）

### 不适用场景

❌ Vue.js/React/Angular 单页应用
❌ 客户端渲染（CSR）应用
❌ 需要 JavaScript 执行才能看到内容的网站

## 建议

对于理杏仁网站：

1. **使用开放 API** - 最佳方案
   - 文档: https://www.lixinger.com/open/api/doc
   - 已有 web-api-generator skill 可以生成 API 文档

2. **使用 stock-crawler** - 已有的解决方案
   - 已经处理了动态加载
   - 已经有针对理杏仁的 parser

3. **不要使用 html-template-generator** - 不适合这个场景
   - 设计目标是静态 HTML
   - 无法处理 SPA 应用

## 技术细节

### 为什么 networkidle 不够

```javascript
await page.goto(url, { waitUntil: 'networkidle' });
```

`networkidle` 只等待网络请求完成，但不等待：
- JavaScript 执行
- Vue/React 渲染
- 异步数据加载
- DOM 更新

### SPA 检测

可以通过以下特征识别 SPA：

```html
<!-- Vue.js -->
<div id="app"></div>
<script src="/app.js"></script>

<!-- React -->
<div id="root"></div>

<!-- Angular -->
<app-root></app-root>
```

## 总结

html-template-generator 在理杏仁网站上的失败是**预期的**，因为：

1. 工具设计目标是静态 HTML
2. 理杏仁是 Vue.js SPA
3. 两者不兼容

**解决方案**: 使用理杏仁的开放 API 或 stock-crawler 的现有 parser。
