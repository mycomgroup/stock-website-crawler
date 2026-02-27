# 配置文件说明

## 概述

通过配置文件控制模板生成的所有参数，无需修改代码。支持多种配置文件和参数覆盖。

## 配置文件优先级

```
命令行参数 > 自定义配置文件 > default.json
```

## 使用方法

### 1. 使用默认配置

```bash
node run-skill.js api-doc \
  --input url-patterns.json \
  --output output/api-doc.json
```

### 2. 使用自定义配置文件

```bash
node run-skill.js api-doc \
  --input url-patterns.json \
  --output output/api-doc.json \
  --config config/my-config.json
```

### 3. 命令行覆盖配置

```bash
node run-skill.js api-doc \
  --input url-patterns.json \
  --output output/api-doc.json \
  --config config/my-config.json \
  --frequency-threshold 0.6 \
  --max-samples 10
```

## 配置参数详解

### browser - 浏览器配置

```json
{
  "browser": {
    "headless": true,           // 是否无头模式（调试时设为false）
    "timeout": 30000,           // 页面加载超时（毫秒）
    "userDataDir": "...",       // Chrome用户数据目录（保持登录状态）
    "channel": "chrome"         // 浏览器类型：chrome, chromium, firefox
  }
}
```

**使用场景**：
- 调试时设置 `headless: false` 查看浏览器行为
- 慢速网站增加 `timeout`
- 需要登录的网站配置 `userDataDir`

### fetching - 页面抓取配置

```json
{
  "fetching": {
    "maxSamples": 5,            // 最多抓取样本数
    "minSamples": 3,            // 最少样本数（不足则报错）
    "retryAttempts": 3,         // 失败重试次数
    "retryDelay": 1000,         // 重试延迟（毫秒）
    "waitForSelector": null,    // 等待特定元素出现（如：".content"）
    "waitTime": 2000            // 页面加载后额外等待时间（毫秒）
  }
}
```

**使用场景**：
- 快速测试时减少 `maxSamples` 到 2-3
- 动态加载页面增加 `waitTime`
- 等待特定内容加载设置 `waitForSelector`

### analysis - 分析配置

```json
{
  "analysis": {
    "frequencyThreshold": 0.8,  // 元素出现频率阈值（0.8 = 80%的样本中出现）
    "minElementCount": 2,       // 最少元素数量
    "maxDepth": 10,             // 最大DOM深度
    "ignoreEmptyElements": true,// 忽略空元素
    "detectPageType": true      // 自动检测页面类型
  }
}
```

**使用场景**：
- 页面结构差异大时降低 `frequencyThreshold` 到 0.6
- 复杂页面增加 `maxDepth`
- 需要手动指定页面类型时设置 `detectPageType: false`

### pageTypes - 页面类型配置

支持4种页面类型，每种类型有不同的提取策略：

#### list - 列表页

```json
{
  "pageTypes": {
    "list": {
      "description": "列表页 - 包含多个相似项目的页面",
      "indicators": {
        "hasRepeatingItems": true,
        "minItemCount": 5,
        "itemSelectors": ["li", "article", "div[class*='item']", "tr"]
      },
      "extraction": {
        "focusOnItems": true,
        "extractItemStructure": true,
        "groupByContainer": true
      }
    }
  }
}
```

**适用场景**：
- 搜索结果页
- 产品列表页
- 文章列表页
- 数据表格页

**提取重点**：
- 识别重复的列表项
- 提取每个项目的结构
- 按容器分组

#### detail - 正文页

```json
{
  "pageTypes": {
    "detail": {
      "description": "正文页 - 单个内容详情页面",
      "indicators": {
        "hasSingleMainContent": true,
        "hasDetailedSections": true
      },
      "extraction": {
        "focusOnMainContent": true,
        "extractFullHierarchy": true,
        "includeSidebar": false
      }
    }
  }
}
```

**适用场景**：
- 文章详情页
- 产品详情页
- API文档页
- 新闻内容页

**提取重点**：
- 聚焦主要内容区域
- 提取完整的标题层级
- 忽略侧边栏和导航

#### mixed - 混排页

```json
{
  "pageTypes": {
    "mixed": {
      "description": "混排页 - 包含多种内容类型的页面",
      "indicators": {
        "hasMultipleContentTypes": true
      },
      "extraction": {
        "extractAllSections": true,
        "preserveLayout": true,
        "groupBySectionType": true
      }
    }
  }
}
```

**适用场景**：
- 首页
- 仪表板页面
- 综合信息页
- 包含多个模块的页面

**提取重点**：
- 提取所有区域
- 保持布局结构
- 按内容类型分组

#### table - 表格页

```json
{
  "pageTypes": {
    "table": {
      "description": "表格页 - 以表格为主的数据页面",
      "indicators": {
        "hasLargeTables": true,
        "minTableRows": 10
      },
      "extraction": {
        "focusOnTables": true,
        "extractTableMetadata": true,
        "handleComplexHeaders": true
      }
    }
  }
}
```

**适用场景**：
- 数据报表页
- 财务数据页
- 统计信息页
- 参数说明表

**提取重点**：
- 聚焦表格数据
- 提取表格元数据（标题、说明）
- 处理复杂表头（合并单元格）

### xpath - XPath生成配置

```json
{
  "xpath": {
    "preferAttributes": ["id", "class", "data-*", "role"],
    "avoidAttributes": ["style", "onclick"],
    "useTextContent": true,
    "generateRelativePaths": true,
    "optimizeForStability": true
  }
}
```

**参数说明**：
- `preferAttributes`: 优先使用的属性（稳定性高）
- `avoidAttributes`: 避免使用的属性（易变化）
- `useTextContent`: 是否使用文本内容辅助定位
- `generateRelativePaths`: 生成相对路径（更灵活）
- `optimizeForStability`: 优化XPath稳定性

### filters - 过滤配置

```json
{
  "filters": {
    "autoDetectNoise": true,
    "removeSelectors": [
      "nav", "header", "footer", "aside",
      "[class*='ad']", "[id*='ad']"
    ],
    "keepSelectors": [],
    "cleanWhitespace": true,
    "removeEmptyElements": true
  }
}
```

**参数说明**：
- `autoDetectNoise`: 自动检测并移除噪音元素
- `removeSelectors`: 强制移除的选择器
- `keepSelectors`: 强制保留的选择器（优先级最高）
- `cleanWhitespace`: 清理多余空白
- `removeEmptyElements`: 移除空元素

### patterns - URL模式过滤

```json
{
  "patterns": {
    "include": ["api-doc", "detail-*"],
    "exclude": ["test-*", "*-backup"],
    "priority": ["api-doc", "detail-sh", "detail-sz"]
  }
}
```

**参数说明**：
- `include`: 只处理匹配的模式（支持通配符）
- `exclude`: 排除匹配的模式（优先级高于include）
- `priority`: 优先处理的模式（按顺序）

**示例**：

```json
{
  "patterns": {
    "include": ["detail-*", "api-*"],
    "exclude": ["*-test", "*-backup"],
    "priority": ["api-doc", "detail-sh"]
  }
}
```

这将：
1. 只处理 `detail-*` 和 `api-*` 开头的模式
2. 排除 `*-test` 和 `*-backup` 结尾的模式
3. 优先处理 `api-doc` 和 `detail-sh`

## 配置文件示例

### 示例1：快速测试配置

```json
{
  "description": "快速测试 - 少量样本，显示浏览器",
  "browser": {
    "headless": false,
    "timeout": 60000
  },
  "fetching": {
    "maxSamples": 2,
    "minSamples": 1,
    "waitTime": 3000
  },
  "analysis": {
    "frequencyThreshold": 0.5
  },
  "patterns": {
    "include": ["api-doc"]
  }
}
```

保存为 `config/quick-test.json`，使用：

```bash
node run-skill.js api-doc \
  --input url-patterns.json \
  --output output/api-doc.json \
  --config config/quick-test.json
```

### 示例2：生产环境配置

```json
{
  "description": "生产环境 - 完整样本，严格阈值",
  "browser": {
    "headless": true,
    "timeout": 30000
  },
  "fetching": {
    "maxSamples": 10,
    "minSamples": 5,
    "retryAttempts": 5
  },
  "analysis": {
    "frequencyThreshold": 0.9,
    "minElementCount": 3
  },
  "output": {
    "includeStatistics": true,
    "generatePreview": true
  }
}
```

### 示例3：列表页专用配置

```json
{
  "description": "列表页优化配置",
  "analysis": {
    "frequencyThreshold": 0.7,
    "detectPageType": true
  },
  "pageTypes": {
    "list": {
      "indicators": {
        "minItemCount": 3
      },
      "extraction": {
        "focusOnItems": true,
        "extractItemStructure": true
      }
    }
  },
  "patterns": {
    "include": ["*-list", "*-index", "search-*"]
  }
}
```

### 示例4：API文档配置

```json
{
  "description": "API文档页面配置",
  "fetching": {
    "maxSamples": 5,
    "waitForSelector": ".api-content"
  },
  "analysis": {
    "frequencyThreshold": 0.8
  },
  "pageTypes": {
    "detail": {
      "extraction": {
        "focusOnMainContent": true,
        "extractFullHierarchy": true
      }
    }
  },
  "filters": {
    "removeSelectors": [
      "nav", "aside", ".sidebar",
      "[class*='ad']"
    ]
  },
  "patterns": {
    "include": ["api-*", "doc-*"]
  }
}
```

## 命令行参数映射

所有配置都可以通过命令行覆盖：

| 配置路径 | 命令行参数 | 示例 |
|---------|-----------|------|
| `browser.headless` | `--headless` | `--headless false` |
| `browser.timeout` | `--timeout` | `--timeout 60000` |
| `fetching.maxSamples` | `--max-samples` | `--max-samples 10` |
| `fetching.minSamples` | `--min-samples` | `--min-samples 3` |
| `fetching.waitTime` | `--wait-time` | `--wait-time 5000` |
| `analysis.frequencyThreshold` | `--frequency-threshold` | `--frequency-threshold 0.6` |
| `analysis.detectPageType` | `--detect-page-type` | `--detect-page-type false` |
| `patterns.include` | `--include-patterns` | `--include-patterns "api-*,detail-*"` |
| `patterns.exclude` | `--exclude-patterns` | `--exclude-patterns "*-test"` |
| `output.generatePreview` | `--generate-preview` | `--generate-preview true` |

## 工作流程建议

### 阶段1：探索和测试（2-3个模板）

使用 `config/quick-test.json`：

```bash
# 生成并测试单个模板
node scripts/generate-and-test.js api-doc \
  --input url-patterns.json \
  --output-dir output/templates \
  --preview-dir output/previews \
  --config config/quick-test.json
```

**检查点**：
1. 查看 `output/previews/api-doc.md`
2. 确认内容提取是否完整
3. 检查表格、列表格式
4. 验证标题层级

### 阶段2：调整参数（根据效果）

根据预览效果调整配置：

**问题：提取内容不完整**
```json
{
  "analysis": {
    "frequencyThreshold": 0.6  // 降低阈值
  }
}
```

**问题：包含太多噪音**
```json
{
  "filters": {
    "removeSelectors": [
      "nav", "aside", ".sidebar", ".ad"
    ]
  }
}
```

**问题：表格提取不正确**
```json
{
  "pageTypes": {
    "table": {
      "extraction": {
        "handleComplexHeaders": true
      }
    }
  }
}
```

### 阶段3：批量生成（确认后）

使用优化后的配置批量生成：

```bash
node scripts/batch-generate-templates.js \
  --input url-patterns.json \
  --output-dir output/templates \
  --config config/production.json \
  --include-patterns "api-*,detail-*" \
  --generate-preview
```

## 最佳实践

1. **先测试后批量**：始终先用1-2个模板测试配置
2. **保存配置**：为不同场景创建配置文件
3. **版本控制**：将配置文件纳入Git管理
4. **文档化**：在配置文件中添加 `description` 说明用途
5. **渐进调整**：每次只调整1-2个参数，观察效果
6. **备份模板**：保存生成的模板，便于对比

## 故障排查

### 问题：配置不生效

检查：
1. 配置文件路径是否正确
2. JSON格式是否有效（使用 `jsonlint` 验证）
3. 命令行参数是否正确覆盖

### 问题：提取效果不理想

调整：
1. 降低 `frequencyThreshold`
2. 增加 `maxSamples`
3. 调整 `pageTypes` 配置
4. 检查 `filters.removeSelectors`

### 问题：生成速度慢

优化：
1. 减少 `maxSamples`
2. 降低 `timeout`
3. 减少 `waitTime`
4. 使用 `patterns.include` 限制范围
