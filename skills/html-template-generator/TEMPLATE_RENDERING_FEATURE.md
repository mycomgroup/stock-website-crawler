# 模板渲染功能实现总结

## 新增功能

为 html-template-generator skill 添加了模板渲染功能，支持使用生成的 XPath 模板将 HTML 内容提取并渲染为 Markdown 格式。

## 新增文件

### 1. lib/template-renderer.js
模板渲染器，核心功能：
- 加载 JSON 模板文件
- 使用 XPath 规则提取 HTML 内容
- 渲染为格式化的 Markdown
- 支持表格、列表、标题、段落等元素

### 2. scripts/test-render-template.js
测试渲染脚本：
```bash
node scripts/test-render-template.js <template-file> <url> [output-file]
```

### 3. scripts/generate-and-test.js
生成并测试脚本（推荐使用）：
```bash
node scripts/generate-and-test.js <template-name> \
  --input <patterns-file> \
  --output-dir <templates-dir> \
  --preview-dir <previews-dir>
```

### 4. scripts/batch-generate-templates.js
批量生成脚本：
```bash
node scripts/batch-generate-templates.js \
  --input <patterns-file> \
  --output-dir <templates-dir>
```

## 工作流程

### Phase 1: 生成并测试单个模板（需人工确认）

```bash
cd skills/html-template-generator

# 生成 api-doc 模板并预览
node scripts/generate-and-test.js api-doc \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --preview-dir ../../stock-crawler/output/lixinger-crawler/previews
```

**输出**:
- `templates/api-doc.json` - XPath 提取模板
- `previews/api-doc.md` - 渲染的预览 Markdown

**人工检查**:
1. 打开 `previews/api-doc.md`
2. 确认内容提取是否完整
3. 检查表格、列表格式
4. 验证标题层级

### Phase 2: 批量生成所有模板（确认后执行）

```bash
# 批量生成所有 106 个模板
node scripts/batch-generate-templates.js \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates
```

**可选参数**:
- `--start-from <n>` - 从第 n 个开始
- `--limit <n>` - 只处理 n 个
- `--headless false` - 显示浏览器（调试用）

## 模板结构

### 输入: Template JSON
```json
{
  "templateName": "api-doc",
  "description": "开放API文档",
  "version": "1.0.0",
  "generatedAt": "2026-02-26T12:00:00Z",
  "samples": ["https://example.com/api/doc"],
  "xpaths": {
    "title": "//h1/text()",
    "sections": {
      "xpath": "//main",
      "extract": {
        "heading": ".//h2/text()",
        "table": {
          "xpath": ".//table",
          "headers": ".//thead/tr/th/text()",
          "rows": ".//tbody/tr"
        }
      }
    }
  }
}
```

### 输出: Preview Markdown
```markdown
## 模板信息

- **模板名称**: api-doc
- **描述**: 开放API文档
- **生成时间**: 2026-02-26T12:00:00Z
- **版本**: 1.0.0
- **样本数量**: 5

---

## 提取内容

### API Documentation

#### Parameters

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| api_key | string | Yes | Your API key |
```

## 技术实现

### 1. XPath 提取
使用 jsdom + xpath 库：
- 解析 HTML 为 DOM
- 使用 XPath 表达式选择节点
- 提取文本和属性

### 2. Markdown 渲染
支持的元素：
- 标题 (h1-h6)
- 表格 (table)
- 列表 (ul/ol)
- 段落 (p)
- 代码块 (pre/code)

### 3. 错误处理
- XPath 执行失败时继续处理
- 记录警告信息
- 返回部分结果

## 修改的文件

### 1. lib/pattern-reader.js
- 支持 `{patterns: [...]}` 和 `[...]` 两种格式
- 兼容 url-pattern-analyzer 的输出

### 2. lib/template-writer.js
- 添加 `description` 字段到模板
- 传递模板描述信息

### 3. main.js
- 传递 `description` 到 templateWriter
- 保留模板元数据

### 4. SKILL.md
- 更新工作流程说明
- 添加人工确认步骤
- 说明批量生成流程

## 使用示例

### 示例 1: 测试单个模板
```bash
# 生成并预览 api-doc 模板
node scripts/generate-and-test.js api-doc \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --preview-dir ../../stock-crawler/output/lixinger-crawler/previews

# 查看预览
cat ../../stock-crawler/output/lixinger-crawler/previews/api-doc.md
```

### 示例 2: 批量生成前 5 个模板
```bash
node scripts/batch-generate-templates.js \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --limit 5
```

### 示例 3: 从第 10 个开始生成
```bash
node scripts/batch-generate-templates.js \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --start-from 10 \
  --limit 10
```

## 下一步

1. ✅ 生成单个模板并预览（已完成）
2. ⏳ **人工确认预览效果**（需要你检查）
3. ⏳ 确认无误后批量生成所有 106 个模板
4. ⏳ 使用生成的模板提取实际页面内容

## 注意事项

1. **必须人工确认**: Phase 1 生成的预览必须人工检查
2. **浏览器会话**: 使用 stock-crawler 的 Chrome 用户数据目录
3. **登录状态**: 自动复用已登录的会话
4. **超时设置**: 默认 30 秒，可在配置中调整
5. **错误处理**: 单个模板失败不影响其他模板

## 版本历史

- **1.1.0** (2026-02-26): 添加模板渲染功能
  - 新增 TemplateRenderer 类
  - 新增 generate-and-test 脚本
  - 新增 batch-generate-templates 脚本
  - 支持 Markdown 预览
  - 人工确认工作流
