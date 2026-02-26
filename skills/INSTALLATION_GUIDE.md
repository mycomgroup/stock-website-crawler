# Skills 安装指南

本指南介绍如何安装和配置模板分析器的两个核心Skills。

## 概述

模板分析器包含两个独立的Skills：

1. **url-pattern-analyzer** - URL模式分析器
   - 分析links.txt中的URL，识别URL模式并分组
   - 生成URL模式报告（JSON格式）

2. **template-content-analyzer** - 模板内容分析器
   - 分析markdown页面内容，识别模板和独特数据
   - 生成模板配置文件（JSONL格式）

## 系统要求

### 必需环境

- **Node.js**: >= 14.0.0
- **npm**: >= 6.0.0
- **操作系统**: Windows, macOS, Linux

### 验证环境

```bash
# 检查Node.js版本
node --version
# 应输出: v14.0.0 或更高

# 检查npm版本
npm --version
# 应输出: 6.0.0 或更高
```

## 安装步骤

### 方式一：从项目根目录安装（推荐）

如果你已经克隆了完整的项目，Skills已经包含在 `skills/` 目录中。

```bash
# 1. 进入项目根目录
cd /path/to/your/project

# 2. 安装 url-pattern-analyzer 依赖
npm install --prefix skills/url-pattern-analyzer

# 3. 安装 template-content-analyzer 依赖
cd ../template-content-analyzer
npm install

# 4. 返回项目根目录
cd ../..
```

### 方式二：独立安装

如果你想单独使用这些Skills：

```bash
# 1. 创建skills目录
mkdir -p skills
cd skills

# 2. 复制skill目录（假设从源位置复制）
cp -r /path/to/source/url-pattern-analyzer ./
cp -r /path/to/source/template-content-analyzer ./

# 3. 安装依赖
cd url-pattern-analyzer
npm install

cd ../template-content-analyzer
npm install
```

## 依赖说明

### url-pattern-analyzer

**开发依赖**:
- `jest@^29.7.0` - 测试框架

**无运行时依赖** - 仅使用Node.js内置模块

### template-content-analyzer

**无任何依赖** - 完全使用Node.js内置模块

这意味着安装非常轻量，不会引入额外的包。

## 验证安装

### 验证 url-pattern-analyzer

```bash
# 运行单元测试
npm test

# 运行演示脚本
node test/test-full-workflow.js

# 预期输出：
# ✓ LinksReader tests passed
# ✓ URLPatternAnalyzer tests passed
# ✓ Full workflow completed successfully
```

### 验证 template-content-analyzer

```bash
cd skills/template-content-analyzer

# 运行单元测试
npm test

# 运行演示脚本
node test/content-analyzer.test.js

# 预期输出：
# ✓ Content extraction tests passed
# ✓ Frequency calculation tests passed
# ✓ Content classification tests passed
```

## 目录结构

安装完成后，你的目录结构应该如下：

```
project-root/
├── skills/
│   ├── url-pattern-analyzer/
│   │   ├── lib/                    # 核心算法库
│   │   │   ├── links-reader.js     # links.txt读取器
│   │   │   ├── url-clusterer.js    # URL聚类算法
│   │   │   └── report-generator.js # 报告生成器
│   │   ├── test/                   # 测试文件
│   │   ├── scripts/                # 脚本工具
│   │   ├── node_modules/           # npm依赖（安装后生成）
│   │   ├── package.json            # npm配置
│   │   ├── skill.json              # Skill配置
│   │   └── README.md               # Skill文档
│   │
│   └── template-content-analyzer/
│       ├── lib/                    # 核心算法库
│       │   ├── content-analyzer.js # 内容分析器
│       │   ├── config-loader.js    # 配置加载器
│       │   ├── template-parser.js  # 模板解析器
│       │   └── template-config-generator.js # 配置生成器
│       ├── test/                   # 测试文件
│       ├── scripts/                # 脚本工具
│       ├── docs/                   # 详细文档
│       ├── examples/               # 示例代码
│       ├── package.json            # npm配置
│       ├── skill.json              # Skill配置
│       └── README.md               # Skill文档
│
└── stock-crawler/                  # 爬虫项目（如果存在）
    └── output/                     # 输出目录
```

## 常见安装问题

### 问题1: npm install 失败

**症状**:
```
npm ERR! code EACCES
npm ERR! syscall access
```

**解决方案**:
```bash
# 方案1: 使用sudo（不推荐）
sudo npm install

# 方案2: 修复npm权限（推荐）
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 问题2: Node.js版本过低

**症状**:
```
Error: Unsupported Node.js version
```

**解决方案**:
```bash
# 使用nvm安装最新版本
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

### 问题3: 测试失败

**症状**:
```
FAIL test/xxx.test.js
```

**解决方案**:
```bash
# 1. 确保依赖已安装
npm install

# 2. 清除缓存
npm cache clean --force

# 3. 重新安装
rm -rf node_modules package-lock.json
npm install

# 4. 再次运行测试
npm test
```

### 问题4: 找不到模块

**症状**:
```
Error: Cannot find module './lib/xxx'
```

**解决方案**:
```bash
# 确保在正确的目录
pwd
# 应该在 skills/url-pattern-analyzer 或 skills/template-content-analyzer

# 检查文件是否存在
ls -la lib/

# 如果文件缺失，重新复制skill目录
```

## 配置说明

### url-pattern-analyzer 配置

Skill配置文件: `skills/url-pattern-analyzer/skill.json`

```json
{
  "name": "url-pattern-analyzer",
  "version": "1.0.0",
  "entry": "main.js",
  "inputs": {
    "linksFile": "links.txt文件路径",
    "outputFile": "输出JSON文件路径",
    "minGroupSize": "最小分组大小（可选，默认5）"
  }
}
```

### template-content-analyzer 配置

Skill配置文件: `skills/template-content-analyzer/skill.json`

```json
{
  "name": "template-content-analyzer",
  "version": "1.0.0",
  "entry": "main.js",
  "inputs": {
    "urlPatternsFile": "url-patterns.json文件路径",
    "pagesDir": "markdown页面目录",
    "outputFile": "输出JSONL文件路径",
    "sampleUrls": "样例URL数组（可选）",
    "frequencyThresholds": "频率阈值（可选）"
  }
}
```

## 快速开始

安装完成后，你可以立即开始使用：

### 1. 分析URL模式

```bash
# 使用测试脚本
node scripts/analyze-url-patterns.js \
  --input ../../stock-crawler/output/lixinger-crawler/links.txt \
  --output ../../stock-crawler/output/lixinger-crawler/url-patterns.json
```

### 2. 分析模板内容

```bash
cd skills/template-content-analyzer

# 使用测试脚本
node scripts/analyze-page-template.js \
  --patterns ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --pages ../../stock-crawler/output/lixinger-crawler/pages \
  --output ../../stock-crawler/output/lixinger-crawler/template-rules.jsonl
```

### 3. 查看生成的配置

```bash
# 查看URL模式
cat stock-crawler/output/lixinger-crawler/url-patterns.json | jq

# 查看模板配置（JSONL格式，每行一个JSON对象）
cat stock-crawler/output/lixinger-crawler/template-rules.jsonl | jq
```

## 性能测试

### url-pattern-analyzer 性能

```bash
node skills/url-pattern-analyzer/test/performance.test.js

# 预期结果：
# ✓ 分析8403个URL < 10秒
# ✓ 内存使用 < 100MB
```

### template-content-analyzer 性能

```bash
cd skills/template-content-analyzer
node test/performance.test.js

# 预期结果：
# ✓ 分析163个页面 < 30秒
# ✓ 生成配置 < 1秒
# ✓ 内存使用 < 200MB
```

## 卸载

如果需要卸载Skills：

```bash
# 删除整个skills目录
rm -rf skills/

# 或者只删除特定skill
rm -rf skills/url-pattern-analyzer
rm -rf skills/template-content-analyzer
```

## 更新

更新到最新版本：

```bash
# 1. 备份现有配置（如果有自定义）
cp skills/url-pattern-analyzer/skill.json ~/backup/
cp skills/template-content-analyzer/skill.json ~/backup/

# 2. 拉取最新代码
git pull origin main

# 3. 重新安装依赖
npm install --prefix skills/url-pattern-analyzer

cd ../template-content-analyzer
npm install

# 4. 运行测试验证
npm test
```

## 下一步

安装完成后，建议阅读以下文档：

1. **使用指南**: `skills/USAGE_GUIDE.md` - 如何使用Skills
2. **url-pattern-analyzer文档**: `skills/url-pattern-analyzer/README.md`
3. **template-content-analyzer文档**: `skills/template-content-analyzer/README.md`
4. **配置格式说明**: `skills/template-content-analyzer/docs/CONFIG_FORMAT.md`
5. **API文档**: 各个skill的README中的API部分

## 获取帮助

如果遇到问题：

1. 查看 **常见问题FAQ**: `skills/FAQ.md`
2. 查看 **故障排除指南**: `skills/TROUBLESHOOTING.md`
3. 提交Issue到项目仓库
4. 查看测试文件了解使用示例

## 贡献

欢迎贡献代码和文档！请参考：

- **贡献指南**: `CONTRIBUTING.md`
- **开发文档**: `skills/DEVELOPMENT.md`
- **代码规范**: `CODE_STYLE.md`

## 许可证

MIT License - 详见 `LICENSE` 文件
