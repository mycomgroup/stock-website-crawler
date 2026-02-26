# Skills 使用指南

## 已安装的Skills

两个skills已通过软连接安装到 `~/.kiro/skills/`：

1. **url-pattern-analyzer** - URL模式分析器
2. **template-content-analyzer** - 模板内容分析器

## 软连接位置

```bash
~/.kiro/skills/url-pattern-analyzer -> /Users/fengzhi/Downloads/git/testlixingren/skills/url-pattern-analyzer
~/.kiro/skills/template-content-analyzer -> /Users/fengzhi/Downloads/git/testlixingren/skills/template-content-analyzer
```

**优势**: 修改项目中的skills代码会立即生效，无需重新安装。

## 使用方式

### 方式1: 直接运行（命令行）

#### Skill 1: URL Pattern Analyzer

```bash
# 基本使用
cd ~/.kiro/skills/url-pattern-analyzer
node main.js <links.txt路径> <输出文件.json>

# 示例
node main.js ~/Downloads/git/testlixingren/stock-crawler/output/lixinger-crawler/links.txt ./url-patterns.json

# 生成Markdown报告
node main.js <links.txt路径> <输出文件.json> --markdown

# 自定义参数
node main.js <links.txt路径> <输出文件.json> --min-group-size 10 --sample-count 3
```

#### Skill 2: Template Content Analyzer

```bash
# 基本使用
cd ~/.kiro/skills/template-content-analyzer
node main.js <url-patterns.json> <pages目录> <输出文件.jsonl>

# 示例
node main.js ./url-patterns.json ~/Downloads/git/testlixingren/stock-crawler/output/lixinger-crawler/pages ./template-rules.jsonl

# 自定义阈值
node main.js <url-patterns.json> <pages目录> <输出文件.jsonl> --template-threshold 0.9 --unique-threshold 0.1
```

### 方式2: 完整工作流

```bash
# 在项目根目录运行完整工作流
cd ~/Downloads/git/testlixingren
node skills/test-complete-workflow.js
```

### 方式3: 通过Kiro调用（推荐）

在Kiro中，你可以直接要求我运行这些skills：

```
"帮我分析 stock-crawler/output/lixinger-crawler/links.txt 中的URL模式"
"使用url-pattern-analyzer分析URL"
"生成模板配置文件"
```

## 测试数据位置

- **links.txt**: `stock-crawler/output/lixinger-crawler/links.txt`
- **pages目录**: `stock-crawler/output/lixinger-crawler/pages/`
- **输出目录**: `stock-crawler/output/lixinger-crawler/`

## 快速测试

### 测试Skill 1

```bash
cd ~/.kiro/skills/url-pattern-analyzer
node main.js ~/Downloads/git/testlixingren/stock-crawler/output/lixinger-crawler/links.txt ./test-output.json --markdown
```

### 测试Skill 2

```bash
cd ~/.kiro/skills/template-content-analyzer
node main.js ~/Downloads/git/testlixingren/stock-crawler/output/lixinger-crawler/url-patterns.json ~/Downloads/git/testlixingren/stock-crawler/output/lixinger-crawler/pages ./test-template-rules.jsonl
```

## 查看帮助

```bash
# Skill 1 帮助
node ~/.kiro/skills/url-pattern-analyzer/main.js --help

# Skill 2 帮助
node ~/.kiro/skills/template-content-analyzer/main.js --help
```

## 卸载Skills

如果需要卸载，只需删除软连接：

```bash
rm ~/.kiro/skills/url-pattern-analyzer
rm ~/.kiro/skills/template-content-analyzer
```

## 更新Skills

由于使用软连接，直接修改项目中的代码即可：

```bash
cd ~/Downloads/git/testlixingren/skills/url-pattern-analyzer
# 修改代码...
# 修改会立即生效，无需重新安装
```

## 文档位置

- **Skill 1 README**: `~/.kiro/skills/url-pattern-analyzer/README.md`
- **Skill 2 README**: `~/.kiro/skills/template-content-analyzer/README.md`
- **Skill 2 详细文档**: `~/.kiro/skills/template-content-analyzer/docs/`
- **架构说明**: `~/Downloads/git/testlixingren/skills/ARCHITECTURE.md`

## 下一步

现在你可以：

1. 在Kiro中直接要求我运行这些skills
2. 使用命令行手动测试
3. 查看生成的报告和配置文件
4. 根据需要修改和调整skills代码

祝使用愉快！🎉
