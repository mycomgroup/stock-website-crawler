# 模板分析器 - 任务列表

## 当前状态总结

### 已完成的里程碑
- ✅ **M1: 基础分析功能** - 完全完成（URL模式分析器、模板内容分析器、集成测试）
- ✅ **M2: 配置生成功能** - 完全完成（配置生成器、模板解析器、文档）

### 进行中的里程碑
- 🔄 **M3: Skills封装和测试** - 部分完成
  - ✅ Skill 1 (url-pattern-analyzer): 算法库和测试完成，缺少main.js入口
  - ✅ Skill 2 (template-content-analyzer): 算法库和测试完成，缺少main.js入口
  - ❌ 整体测试和文档: 未开始

### 剩余工作
1. **创建main.js入口文件** (任务7.1.4, 8.1.4)
   - 为两个skills创建统一的入口文件
   - 实现命令行参数解析
   - 集成算法库调用
   
2. **整体测试** (任务9.1)
   - 测试两个skills独立运行
   - 测试完整工作流（Skill 1 → Skill 2）
   - 验证生成的配置质量
   
3. **完善文档** (任务9.2.4, 9.3)
   - 编写FAQ
   - 编写架构说明
   - 编写扩展指南

## 里程碑 M1: 基础分析功能（3天）

### 1. URL模式分析器
- [x] 1.1 创建URLPatternAnalyzer类
  - [x] 1.1.1 实现extractFeatures()方法 - 提取URL特征
  - [x] 1.1.2 实现calculateSimilarity()方法 - 计算URL相似度（不使用固定阈值）
  - [x] 1.1.3 实现clusterURLs()方法 - URL聚类（基于URL正则匹配和后端渲染判断）
  - [x] 1.1.4 实现generatePattern()方法 - 生成正则表达式
- [x] 1.2 创建links.txt读取器
  - [x] 1.2.1 实现readLinksFile()方法 - 读取JSON格式的links
  - [x] 1.2.2 实现parseURLs()方法 - 解析URL对象
  - [x] 1.2.3 添加错误处理 - 处理格式错误
- [x] 1.3 生成URL模式报告
  - [x] 1.3.1 实现generateJSONReport()方法 - 生成JSON报告
  - [x] 1.3.2 实现generateMarkdownReport()方法 - 生成Markdown报告
  - [x] 1.3.3 添加统计信息 - 模式数量、URL数量等
- [x] 1.4 单元测试
  - [x] 1.4.1 测试URL特征提取
  - [x] 1.4.2 测试相似度计算
  - [x] 1.4.3 测试聚类算法
  - [x] 1.4.4 测试正则表达式生成

### 2. 模板内容分析器
- [x] 2.1 创建TemplateContentAnalyzer类
  - [x] 2.1.1 实现extractContentBlocks()方法 - 提取内容块
  - [x] 2.1.2 实现normalizeText()方法 - 文本标准化
  - [x] 2.1.3 实现calculateFrequency()方法 - 计算频率
  - [x] 2.1.4 实现classifyContent()方法 - 内容分类
- [x] 2.2 创建markdown文件读取器
  - [x] 2.2.1 实现loadMarkdownPages()方法 - 批量加载页面
  - [x] 2.2.2 实现matchPagesToURLs()方法 - 匹配URL和文件
  - [x] 2.2.3 添加流式处理 - 避免内存溢出
- [x] 2.3 数据结构识别
  - [x] 2.3.1 实现identifyTableStructures()方法 - 识别表格
  - [x] 2.3.2 实现identifyCodeBlocks()方法 - 识别代码块
  - [x] 2.3.3 实现identifyLists()方法 - 识别列表
- [x] 2.4 生成清洗规则
  - [x] 2.4.1 实现generateCleaningRules()方法 - 生成规则
  - [x] 2.4.2 实现identifyNoisePatterns()方法 - 识别噪音
  - [x] 2.4.3 实现identifyDataPatterns()方法 - 识别数据
- [x] 2.5 生成模板分析报告
  - [x] 2.5.1 实现generateAnalysisJSON()方法 - JSON报告
  - [x] 2.5.2 实现generateAnalysisMarkdown()方法 - Markdown报告
  - [x] 2.5.3 添加清洗前后对比示例
- [x] 2.6 单元测试
  - [x] 2.6.1 测试内容块提取
  - [x] 2.6.2 测试频率计算
  - [x] 2.6.3 测试内容分类
  - [x] 2.6.4 测试数据结构识别

### 3. 集成和测试
- [x] 3.1 创建分析脚本
  - [x] 3.1.1 创建analyze-url-patterns.js脚本
  - [x] 3.1.2 创建analyze-page-template.js脚本
  - [x] 3.1.3 添加命令行参数解析
  - [x] 3.1.4 添加进度显示
- [x] 3.2 使用真实数据测试
  - [x] 3.2.1 测试理杏仁links.txt（8403个URL）
  - [x] 3.2.2 测试API文档页面（163个）
  - [x] 3.2.3 验证分析结果准确性
  - [x] 3.2.4 验证URL正则匹配和后端渲染判断
- [x] 3.3 性能优化
  - [x] 3.3.1 添加批量处理
  - [x] 3.3.2 添加缓存机制
  - [x] 3.3.3 添加并行处理
  - [x] 3.3.4 性能测试（目标：<30秒）

## 里程碑 M2: 配置生成功能（2天）

### 4. 模板配置生成器
- [x] 4.1 创建TemplateConfigGenerator类
  - [x] 4.1.1 实现generateConfig()方法 - 生成配置对象
  - [x] 4.1.2 实现generateExtractors()方法 - 生成提取器配置
  - [x] 4.1.3 实现generateFilters()方法 - 生成过滤器配置
  - [x] 4.1.4 实现saveAsJSONL()方法 - 保存为JSONL格式
- [x] 4.2 配置格式设计
  - [x] 4.2.1 定义配置schema - 基本信息、URL模式、提取器、过滤器
  - [x] 4.2.2 定义提取器类型 - text, table, code, list
  - [x] 4.2.3 定义过滤器类型 - remove, keep, transform
  - [x] 4.2.4 添加元数据字段 - 生成时间、版本、页面数量
- [x] 4.3 生成提取规则
  - [x] 4.3.1 实现generateTextExtractor()方法 - 文本提取配置
  - [x] 4.3.2 实现generateTableExtractor()方法 - 表格提取配置
  - [x] 4.3.3 实现generateCodeExtractor()方法 - 代码块提取配置
  - [x] 4.3.4 实现generateListExtractor()方法 - 列表提取配置
- [x] 4.4 生成过滤规则
  - [x] 4.4.1 基于高频内容生成移除规则
  - [x] 4.4.2 基于低频内容生成保留规则
  - [x] 4.4.3 添加规则说明和原因
- [x] 4.5 单元测试
  - [x] 4.5.1 测试配置生成
  - [x] 4.5.2 测试JSONL格式输出
  - [x] 4.5.3 测试提取器生成
  - [x] 4.5.4 测试过滤器生成

### 5. 模板解析器（配置驱动）
- [x] 5.1 创建TemplateParser类
  - [x] 5.1.1 实现构造函数 - 接收配置对象
  - [x] 5.1.2 实现matches()方法 - 基于配置的URL匹配
  - [x] 5.1.3 实现parse()方法 - 基于配置的数据提取
  - [x] 5.1.4 实现executeExtractor()方法 - 执行提取器
- [x] 5.2 创建ConfigLoader类
  - [x] 5.2.1 实现loadConfigs()方法 - 从JSONL加载配置
  - [x] 5.2.2 实现createParsers()方法 - 创建Parser实例
  - [x] 5.2.3 添加配置验证 - 检查必需字段
  - [x] 5.2.4 添加错误处理 - 处理格式错误
- [x] 5.3 实现提取器执行
  - [x] 5.3.1 实现extractText()方法 - 文本提取
  - [x] 5.3.2 实现extractTable()方法 - 表格提取
  - [x] 5.3.3 实现extractCode()方法 - 代码块提取
  - [x] 5.3.4 实现extractList()方法 - 列表提取
- [x] 5.4 实现过滤器应用
  - [x] 5.4.1 实现applyFilters()方法 - 应用所有过滤器
  - [x] 5.4.2 实现removeFilter()方法 - 移除内容
  - [x] 5.4.3 实现keepFilter()方法 - 保留内容
  - [x] 5.4.4 实现transformFilter()方法 - 转换内容
- [x] 5.5 验证配置效果（不集成到爬虫系统）
  - [x] 5.5.1 创建独立测试脚本
  - [x] 5.5.2 加载配置文件
  - [x] 5.5.3 创建TemplateParser实例
  - [x] 5.5.4 测试配置驱动的解析
- [x] 5.6 单元测试
  - [x] 5.6.1 测试配置加载
  - [x] 5.6.2 测试Parser创建
  - [x] 5.6.3 测试提取器执行
  - [x] 5.6.4 测试过滤器应用

### 6. 生成脚本和文档
- [x] 6.1 创建生成脚本
  - [x] 6.1.1 创建generate-template-config.js脚本
  - [x] 6.1.2 添加命令行参数
  - [x] 6.1.3 添加交互式确认
  - [x] 6.1.4 添加生成报告
- [x] 6.2 配置文件文档
  - [x] 6.2.1 编写配置格式说明
  - [x] 6.2.2 编写提取器配置指南
  - [x] 6.2.3 编写过滤器配置指南
  - [x] 6.2.4 提供配置示例
- [x] 6.3 生成使用文档
  - [x] 6.3.1 如何加载配置文件
  - [x] 6.3.2 如何修改配置
  - [x] 6.3.3 如何调试配置
  - [x] 6.3.4 常见问题FAQ
- [x] 6.4 集成测试
  - [x] 6.4.1 生成api-doc配置
  - [x] 6.4.2 验证配置格式正确
  - [x] 6.4.3 验证配置驱动的解析效果
  - [x] 6.4.4 对比手写Parser的效果

## 里程碑 M3: Skills封装和测试（1天）

### 7. 创建Skill 1: url-pattern-analyzer
- [x] 7.1 创建skill目录结构
  - [x] 7.1.1 创建 `skills/url-pattern-analyzer/` 目录
  - [x] 7.1.2 创建README.md - Skill说明文档
  - [x] 7.1.3 创建skill.json - Skill配置
  - [x] 7.1.4 创建main.js - 入口文件
- [x] 7.2 实现算法库
  - [x] 7.2.1 创建lib/url-clusterer.js - URL聚类算法（基于URL正则匹配和后端渲染判断）
  - [x] 7.2.2 创建lib/links-reader.js - links.txt读取器
  - [x] 7.2.3 创建lib/report-generator.js - 报告生成器
- [ ] 7.3 集成到main.js
  - [x] 7.3.1 读取links.txt
  - [x] 7.3.2 调用算法库进行分析
  - [x] 7.3.3 生成url-patterns.json
  - [x] 7.3.4 返回结果给大模型
- [x] 7.4 测试
  - [x] 7.4.1 创建test/url-clusterer.test.js
  - [x] 7.4.2 测试URL聚类
  - [x] 7.4.3 测试正则表达式生成
  - [x] 7.4.4 使用真实数据测试

### 8. 创建Skill 2: template-content-analyzer
- [x] 8.1 创建skill目录结构
  - [x] 8.1.1 创建 `skills/template-content-analyzer/` 目录
  - [x] 8.1.2 创建README.md - Skill说明文档
  - [x] 8.1.3 创建skill.json - Skill配置
  - [x] 8.1.4 创建main.js - 入口文件
- [x] 8.2 实现算法库（2个skills架构）
  - [x] 8.2.1 创建lib/content-analyzer.js - 内容分析
  - [x] 8.2.2 创建lib/template-config-generator.js - 配置生成器（包含频率计算）
  - [x] 8.2.3 创建lib/template-parser.js - 模板解析器
  - [x] 8.2.4 创建lib/config-loader.js - 配置加载器
- [x] 8.3 集成到main.js
  - [x] 8.3.1 读取url-patterns.json
  - [x] 8.3.2 对每个pathTemplate进行分析（基于模板抽取和URL正则匹配）
  - [x] 8.3.3 生成TemplateConfig对象
  - [x] 8.3.4 保存为template-rules.jsonl
  - [x] 8.3.5 返回结果给大模型
- [x] 8.4 测试
  - [x] 8.4.1 创建test/content-analyzer.test.js
  - [x] 8.4.2 测试内容分析
  - [x] 8.4.3 测试配置生成
  - [x] 8.4.4 使用真实数据测试

### 9. 整体测试和文档（2个skills）
- [x] 9.1 整体测试
  - [x] 9.1.1 测试Skill 1独立运行
  - [x] 9.1.2 测试Skill 2独立运行
  - [x] 9.1.3 测试完整工作流（Skill 1 → Skill 2）
  - [x] 9.1.4 验证生成的配置质量
- [x] 9.2 编写用户文档
  - [x] 9.2.1 编写Skills安装指南
  - [x] 9.2.2 编写Skills使用手册（README.md已完成）
  - [x] 9.2.3 编写配置文件格式说明（docs/已完成）
  - [x] 9.2.4 编写常见问题FAQ
- [x] 9.3 编写开发文档
  - [x] 9.3.1 编写2个Skills架构说明
  - [x] 9.3.2 编写算法库API文档
  - [x] 9.3.3 编写扩展指南
  - [x] 9.3.4 编写贡献指南

## 可选任务

### 9. 高级功能（可选）
- [ ] 9.1 可视化分析报告
  - [ ] 9.1.1 生成HTML格式报告
  - [ ] 9.1.2 添加图表展示
  - [ ] 9.1.3 添加交互式浏览
- [ ] 9.2 配置验证和测试
  - [ ] 9.2.1 实现配置schema验证
  - [ ] 9.2.2 实现配置测试工具
  - [ ] 9.2.3 生成配置测试报告
- [ ] 9.3 增量分析
  - [ ] 9.3.1 支持增量更新分析
  - [ ] 9.3.2 支持差异对比
  - [ ] 9.3.3 支持版本管理
- [ ] 9.4 多网站支持
  - [ ] 9.4.1 创建网站配置系统
  - [ ] 9.4.2 支持自定义规则
  - [ ] 9.4.3 创建网站模板库
- [ ] 9.5 配置优化建议
  - [ ] 9.5.1 分析配置使用情况
  - [ ] 9.5.2 生成优化建议
  - [ ] 9.5.3 自动优化配置

## 验收标准

### M1验收
- [x] URL模式分析准确率 > 90%
- [x] 模板内容识别准确率 > 85%
- [x] 分析8403个URL < 10秒
- [x] 分析163个页面 < 30秒
- [x] 生成完整的分析报告

### M2验收
- [x] 生成的配置文件格式正确（JSONL）
- [x] 配置包含完整的提取器和过滤器
- [x] TemplateParser能正确加载配置
- [x] 配置驱动的解析效果与手写Parser相当
- [x] 配置包含完整的注释和元数据
- [x] 生成时间 < 1秒
- [x] 大模型可以轻松修改配置

### M3验收（2个skills）
- [ ] Skill 1能独立运行并生成url-patterns.json
- [ ] Skill 2能独立运行并生成template-rules.jsonl
- [ ] 2个skills能完整串联运行
- [x] 判断依据正确：URL正则匹配、后端渲染、模板抽取
- [x] 不依赖similarityThreshold参数
- [x] Skills安装到根目录skills/
- [x] 文档完整清晰
- [x] 示例代码可运行
- [x] 错误处理完善

## 时间估算

| 里程碑 | 任务数 | 预计时间 | 实际状态 | 优先级 |
|--------|--------|---------|---------|--------|
| M1: 基础分析 | 30 | 3天 | ✅ 已完成 | P0 |
| M2: 配置生成 | 24 | 2天 | ✅ 已完成 | P1 |
| M3: Skills封装（2个skills） | 23 | 1天 | 🔄 部分完成（剩余3个任务） | P2 |
| 可选功能 | 15 | 2-3天 | ⏸️ 未开始 | P3 |

**M3剩余工作**: 约0.5天
- 创建main.js入口文件（2个）: 2-3小时
- 整体测试: 1-2小时
- 完善文档: 1-2小时

**总计**: M1-M3已完成约90%，剩余约0.5天工作量

## 依赖关系

```
M1 (基础分析)
  ├─ 1. URL模式分析器 (无依赖)
  ├─ 2. 模板内容分析器 (依赖: 1)
  └─ 3. 集成和测试 (依赖: 1, 2)

M2 (配置生成)
  ├─ 4. 模板配置生成器 (依赖: M1)
  ├─ 5. 模板解析器 (依赖: 4)
  └─ 6. 生成脚本和文档 (依赖: 4, 5)

M3 (Skills封装 - 2个skills)
  ├─ 7. 创建Skill 1: url-pattern-analyzer (依赖: M1)
  ├─ 8. 创建Skill 2: template-content-analyzer (依赖: M2)
  └─ 9. 整体测试和文档 (依赖: 7, 8)
```

**注意**：
- 只有2个skills：url-pattern-analyzer 和 template-content-analyzer
- Skills放在项目根目录 `skills/`
- 由大模型执行，可调用算法库
- 判断依据：URL正则匹配、页面是否同一个后端渲染、模板抽取结果
- 不使用similarityThreshold参数

## 风险和缓解

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| URL模式识别不准确 | 高 | 中 | 使用URL正则匹配和后端渲染判断 |
| 内容频率阈值难确定 | 中 | 高 | 提供可配置阈值 |
| 配置格式设计不合理 | 高 | 中 | 参考现有Parser设计 |
| 后端渲染判断不准确 | 中 | 中 | 结合模板抽取结果验证 |
| 配置难以调试 | 中 | 中 | 提供配置验证工具 |
| 文档不完善 | 低 | 中 | 预留文档时间 |

## 下一步行动

### 立即可执行的任务

1. **任务7.1.4 & 8.1.4**: 创建main.js入口文件
   - 为url-pattern-analyzer创建main.js
   - 为template-content-analyzer创建main.js
   - 实现命令行参数解析和算法库调用
   - 预计时间: 2-3小时

2. **任务9.1**: 整体测试
   - 测试Skill 1独立运行
   - 测试Skill 2独立运行
   - 测试完整工作流
   - 预计时间: 1-2小时

3. **任务9.2.4 & 9.3**: 完善文档
   - 编写FAQ
   - 编写架构说明
   - 编写扩展指南
   - 预计时间: 1-2小时

### 建议执行顺序

1. 先完成main.js入口文件（任务7.1.4, 8.1.4）
2. 然后进行整体测试（任务9.1）
3. 最后完善文档（任务9.2.4, 9.3）

### 已完成的工作

- ✅ M1和M2的所有功能已完全实现并测试
- ✅ 两个skills的算法库已完成
- ✅ 单元测试和集成测试已完成
- ✅ 基础文档（README、配置指南）已完成
- ✅ 性能测试已通过
