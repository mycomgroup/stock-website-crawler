# 贡献指南

感谢你对 Template Analyzer Skills 项目的贡献！

## 开发环境设置

### 1. 克隆仓库

```bash
git clone <repository-url>
cd skills
```

### 2. 安装依赖

```bash
cd url-pattern-analyzer
npm install

cd ../template-content-analyzer
npm install
```

### 3. 运行测试

```bash
# URL Pattern Analyzer
cd url-pattern-analyzer
npm test

# Template Content Analyzer
cd template-content-analyzer
npm test
```

## 代码规范

### JavaScript 风格

- 使用 ES6+ 语法
- 使用 2 空格缩进
- 使用单引号
- 添加 JSDoc 注释

示例:

```javascript
/**
 * 分析模板内容
 * @param {Array<string>} pages - 页面内容数组
 * @param {Object} options - 选项
 * @returns {Object} 分析结果
 */
analyzeTemplate(pages, options = {}) {
  // 实现...
}
```

### 命名约定

- 类名: PascalCase (`TemplateParser`)
- 方法名: camelCase (`extractContent`)
- 常量: UPPER_SNAKE_CASE (`MAX_PAGES`)
- 文件名: kebab-case (`content-analyzer.js`)

## 测试要求

### 单元测试

每个新功能都需要单元测试:

```javascript
describe('FeatureName', () => {
  test('should work correctly', () => {
    const result = feature.execute();
    expect(result).toBeDefined();
  });
  
  test('should handle errors', () => {
    expect(() => feature.execute(null)).toThrow();
  });
});
```

### 测试覆盖率

- 目标覆盖率: 80%+
- 运行覆盖率报告: `npm run test:coverage`

## 提交流程

### 1. 创建分支

```bash
git checkout -b feature/your-feature-name
```

### 2. 提交更改

```bash
git add .
git commit -m "feat: add new feature"
```

提交信息格式:
- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `test:` 测试相关
- `refactor:` 代码重构

### 3. 推送并创建 Pull Request

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

## Pull Request 检查清单

- [ ] 代码通过所有测试
- [ ] 添加了新功能的测试
- [ ] 更新了相关文档
- [ ] 代码符合风格指南
- [ ] 提交信息清晰明确

## 文档更新

如果你的更改影响了 API 或用法，请更新:

- `README.md` - 主文档
- `docs/API.md` - API 文档
- `docs/USAGE_GUIDE.md` - 使用指南
- `docs/FAQ.md` - 常见问题

## 报告问题

在 GitHub Issues 中报告问题时，请包含:

1. 问题描述
2. 重现步骤
3. 预期行为
4. 实际行为
5. 环境信息 (Node.js 版本等)

## 获取帮助

- 查看 [文档](./template-content-analyzer/docs/)
- 查看 [示例](./template-content-analyzer/examples/)
- 提交 Issue
- 联系维护者

感谢你的贡献！
