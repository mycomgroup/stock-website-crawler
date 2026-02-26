# 模板配置文件文档

本目录包含模板配置文件的完整文档。

## 文档列表

### 1. [配置格式说明](./CONFIG_FORMAT.md)
**内容**: JSONL 格式和配置对象结构的完整说明

**包含**:
- JSONL 格式介绍
- 配置对象结构
- 所有字段的详细说明
- 配置验证规则
- 最佳实践
- 完整示例

**适合**: 
- 初次使用者了解配置文件格式
- 需要了解配置对象结构的开发者
- 需要验证配置文件的用户

### 2. [提取器配置指南](./EXTRACTOR_GUIDE.md)
**内容**: 如何配置数据提取器的详细指南

**包含**:
- 提取器结构说明
- 4种提取器类型详解（text、table、code、list）
- 每种类型的使用示例
- 提取器组合策略
- 错误处理
- 最佳实践
- 常见问题

**适合**:
- 需要配置数据提取的用户
- 需要了解如何使用CSS选择器的开发者
- 需要提取特定类型数据的用户

### 3. [过滤器配置指南](./FILTER_GUIDE.md)
**内容**: 如何配置数据过滤器的详细指南

**包含**:
- 过滤器结构说明
- 3种过滤器类型详解（remove、keep、transform）
- 目标类型说明
- 模式匹配技巧
- 自动生成规则
- 过滤器组合
- 调试技巧
- 常见场景

**适合**:
- 需要清理数据噪音的用户
- 需要过滤特定内容的开发者
- 需要优化提取结果的用户

### 4. [配置示例](./CONFIG_EXAMPLES.md)
**内容**: 各种场景下的完整配置示例

**包含**:
- 基础示例
- API文档页面配置
- 数据仪表板配置
- 新闻文章配置
- 产品列表配置
- 用户资料配置
- 搜索结果配置
- 高级示例
- JSONL 格式示例

**适合**:
- 需要快速上手的用户
- 需要参考实际配置的开发者
- 需要针对特定场景配置的用户

### 5. [使用指南](./USAGE_GUIDE.md)
**内容**: 如何使用配置文件的完整指南

**包含**:
- 快速开始
- 加载配置
- 创建解析器
- 解析页面
- 修改配置
- 调试配置
- 常见问题
- 测试脚本

**适合**:
- 需要集成配置文件的开发者
- 需要调试配置的用户
- 需要解决问题的用户

## 快速导航

### 我想...

#### 了解配置文件格式
→ 阅读 [配置格式说明](./CONFIG_FORMAT.md)

#### 配置数据提取
→ 阅读 [提取器配置指南](./EXTRACTOR_GUIDE.md)

#### 清理数据噪音
→ 阅读 [过滤器配置指南](./FILTER_GUIDE.md)

#### 查看实际示例
→ 阅读 [配置示例](./CONFIG_EXAMPLES.md)

#### 使用配置文件
→ 阅读 [使用指南](./USAGE_GUIDE.md)

#### 快速上手
1. 阅读 [配置格式说明](./CONFIG_FORMAT.md) 了解基础
2. 查看 [配置示例](./CONFIG_EXAMPLES.md) 找到类似场景
3. 参考 [提取器配置指南](./EXTRACTOR_GUIDE.md) 配置提取
4. 参考 [过滤器配置指南](./FILTER_GUIDE.md) 配置过滤
5. 阅读 [使用指南](./USAGE_GUIDE.md) 集成使用

## 文档结构

```
docs/
├── README.md                  # 本文件 - 文档导航
├── CONFIG_FORMAT.md           # 配置格式说明
├── EXTRACTOR_GUIDE.md         # 提取器配置指南
├── FILTER_GUIDE.md            # 过滤器配置指南
├── CONFIG_EXAMPLES.md         # 配置示例
└── USAGE_GUIDE.md             # 使用指南
```

## 相关资源

### 代码
- [ConfigLoader](../lib/config-loader.js) - 配置加载器实现
- [TemplateParser](../lib/template-parser.js) - 模板解析器实现
- [ContentAnalyzer](../lib/content-analyzer.js) - 内容分析器实现

### 示例
- [配置文件示例](../examples/template-config.jsonl) - 实际的 JSONL 配置文件
- [分析报告示例](../examples/analysis-report.json) - JSON 格式的分析报告
- [Markdown报告示例](../examples/analysis-report.md) - Markdown 格式的分析报告

### 测试
- [配置加载测试](../test/config-loader.test.js) - ConfigLoader 单元测试
- [模板解析测试](../test/template-parser.test.js) - TemplateParser 单元测试
- [内容分析测试](../test/content-analyzer.test.js) - ContentAnalyzer 单元测试

### 脚本
- [测试配置解析](../scripts/test-config-parsing.js) - 测试配置文件加载
- [测试模板解析器](../scripts/test-template-parser.js) - 测试解析器创建
- [测试真实页面](../scripts/test-real-pages.js) - 测试实际页面解析
- [生成配置](../scripts/generate-template-config.js) - 生成配置文件

## 贡献

如果您发现文档有误或需要改进，欢迎：
1. 提交 Issue
2. 提交 Pull Request
3. 联系维护者

## 许可证

MIT

---

**最后更新**: 2024-02-25  
**版本**: 1.0.0
