# Parser 模块重构设计文档

## 1. 背景与目标 (Background & Goals)

当前 `stock-crawler` 项目中包含大量页面解析器（Parsers），用于从各类网页和 API 文档中提取数据。随着支持的网站类型和复杂页面交互（如无限滚动、虚拟表格、复杂分页、图表提取）的增加，Parser 模块的代码逐渐暴露出一些架构上的缺陷，影响了代码的可维护性和扩展性。

**重构目标：**
* **消除“上帝类” (God Class)**：拆分庞大臃肿的类，使其符合单一职责原则 (SRP)。
* **提高复用性**：通过“组合优于继承”的设计，让所有具体的 Parser 都能轻松复用通用交互和提取能力。
* **解耦与动态加载**：消除管理器中的硬编码依赖，使其符合开闭原则 (OCP)。
* **清晰的生命周期**：规范解析流程，使调试和二次开发更加直观。

## 2. 当前架构痛点分析 (Pain Points Analysis)

1. **`GenericParser` 极度臃肿 (上帝类)**
   * 目前 `GenericParser` 的代码量高达 3400+ 行。
   * 它将 DOM 提取（表格、列表、图表）、网络拦截（API 抓取）、复杂页面交互（点击展开、无限滚动、分页、日期筛选）等所有逻辑揉合在了一起。这导致代码极其难以阅读、维护和编写单元测试。
2. **`ParserManager` 硬编码注册**
   * `ParserManager` 的 `registerDefaultParsers` 方法中硬编码了 40 多个具体 Parser 的 `import` 和 `new` 实例化过程。每次新增一个解析器，都需要修改这个核心管理类，严重违背了开闭原则。
3. **功能难以复用 (继承的局限性)**
   * 具体的解析器（如 `ArticleParser`, `FinnhubApiParser`）目前大多直接继承自 `BaseParser`。
   * 如果 `ArticleParser` 也想使用 `GenericParser` 中的“无限滚动”或“自动点击展开”功能，目前无法直接复用，只能复制代码或强行继承 `GenericParser`（这会引入大量不需要的负担）。
4. **解析流程缺乏标准生命周期**
   * 目前 `parse` 方法内部是线性的流水账代码（先拦截 API -> 提取基本信息 -> 点击展开 -> 滚动 -> 提取图表 -> 提取表格），缺乏标准化的生命周期钩子（Hooks），难以在特定阶段插入自定义逻辑。

## 3. 重构架构设计 (Refactoring Architecture)

核心思路：**策略模式 (Strategy) + 组合优于继承 (Composition) + 插件化生命周期 (Lifecycle/Plugins)**

### 3.1 模块目录拆分
建议在 `src/parsers/` 下建立更清晰的子目录组织结构：
```text
src/parsers/
├── core/                   # 核心骨架
│   ├── base-parser.js      # 提供生命周期和组件编排能力
│   ├── parser-manager.js   # 解析器注册与分发（改为动态扫描加载）
│   └── parser-context.js   # 传递给各个组件的上下文对象 (包含 page, url, options 等)
├── extractors/             # 数据提取组件 (负责只读 DOM 分析)
│   ├── table-extractor.js  # 表格提取 (包含虚拟表格检测)
│   ├── media-extractor.js  # 图片、音视频提取与下载
│   ├── chart-extractor.js  # Canvas/SVG/ECharts 运行时数据提取
│   └── text-extractor.js   # 标题、正文、Markdown 生成
├── interactors/            # 页面交互组件 (负责触发 DOM 改变)
│   ├── scroll-handler.js   # 无限滚动处理
│   ├── expand-handler.js   # 点击展开/更多处理
│   ├── pagination-handler.js# 分页控制
│   └── form-handler.js     # 下拉框、时间筛选等表单交互
├── interceptors/           # 网络层组件
│   └── api-interceptor.js  # XHR/Fetch 拦截与数据转换
├── detectors/              # 页面特征检测
│   └── feature-detector.js # 识别 portal, article, list 等特征
└── sites/                  # 具体的站点解析器 (原有的各类 api-parser 等)
    ├── finnhub-api-parser.js
    ├── article-parser.js
    └── ...
```

### 3.2 核心组件重构方案

#### 3.2.1 动态注册的 ParserManager
摒弃手动 `import`，使用文件系统扫描（在 Node.js 环境下利用 `fs.readdir` 或动态 `import()`）或使用统一的 `index.js` 导出数组，自动注册所有符合规则的解析器。

#### 3.2.2 插件化的 BaseParser
`BaseParser` 应具备插件/中间件注册能力，使得具体的 Parser 可以像拼积木一样组合能力。

```javascript
class BaseParser {
  constructor() {
    this.extractors = [];
    this.interactors = [];
  }

  // 注册能力
  useExtractor(extractor) { this.extractors.push(extractor); }
  useInteractor(interactor) { this.interactors.push(interactor); }

  // 标准化生命周期
  async parse(page, url, options) {
    const context = { page, url, options, data: {} };
    
    await this.beforeLoad(context);
    await this.waitForContent(page, options);
    await this.onLoad(context);
    
    // 交互阶段 (展开、滚动等)
    for (const interactor of this.interactors) {
      await interactor.execute(context);
    }
    
    // 提取阶段 (表格、文本、图表)
    for (const extractor of this.extractors) {
      const result = await extractor.extract(context);
      Object.assign(context.data, result);
    }
    
    return this.afterExtract(context);
  }
}
```

#### 3.2.3 瘦身的 GenericParser
重构后的 `GenericParser` 将不再包含几千行的实现逻辑，它仅仅是一个装配器（Assembler）：

```javascript
class GenericParser extends BaseParser {
  constructor() {
    super();
    // 注册需要的提取器和交互器
    this.useExtractor(new TextExtractor());
    this.useExtractor(new TableExtractor({ supportVirtual: true, supportPagination: true }));
    this.useExtractor(new MediaExtractor());
    this.useExtractor(new ChartExtractor());
    
    this.useInteractor(new ExpandHandler());
    this.useInteractor(new ScrollHandler({ maxScrolls: 30 }));
  }
  
  matches(url) { return true; }
  getPriority() { return 0; }
}
```

## 4. 实施与迁移步骤 (Migration Steps)

为了保证重构过程中的稳定性，建议采取渐进式替换策略：

* **Step 1: 基础设施搭建** 
  创建 `extractors` 和 `interactors` 目录。定义标准的接口契约（如所有 Extractor 必须实现 `async extract(page, context)` 方法）。
* **Step 2: 逐步抽离 GenericParser 逻辑**
  将 `GenericParser` 中的独立功能（如 `extractTablesWithPaginationAndVirtual`）平滑迁移到 `TableExtractor` 类中。此时 `GenericParser` 内部改为调用 `new TableExtractor().extract(...)`。
  重复此步骤，抽离滚动、点击展开、图表提取等功能。
* **Step 3: 引入生命周期与上下文**
  修改 `BaseParser` 的 `parse` 方法，引入完整的生命周期。将 `GenericParser` 改造成基于组合的模式。
* **Step 4: 改造 ParserManager**
  实现基于文件系统或统一注册表的动态加载机制，删除几百行的硬编码注册代码。
* **Step 5: 特定 Parser 的按需升级**
  对于 `ArticleParser`、`FinnhubApiParser` 等具体解析器，检查是否可以利用新拆分出的 `TextExtractor` 等组件来简化自身代码。

## 5. 预期收益 (Expected Benefits)

1. **代码行数大幅下降**：`GenericParser` 从 3400+ 行缩减至 200 行以内的组装逻辑，各个 Extractor 维持在 200-500 行，便于阅读和单测。
2. **高可复用**：如果一个特定的电商 API 解析器需要虚拟表格支持，只需 `this.useExtractor(new TableExtractor())` 即可。
3. **开闭原则**：新增特定网站的解析器只需在 `sites/` 目录下新建文件，系统自动识别，无需修改核心调度代码。
4. **健壮性提升**：隔离了可能引发异常的 DOM 交互（如拉取图表失败不会影响文本提取，因为它们在不同的 Extractor 中独立 `try/catch` 运行）。