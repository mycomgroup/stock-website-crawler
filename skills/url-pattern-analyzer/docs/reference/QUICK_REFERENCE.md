# URL Pattern Analyzer - 快速参考

## 一行命令

```bash
node run-skill.js <项目名> [选项]
```

## 常用命令

```bash
# 默认参数
node run-skill.js lixinger-crawler

# 推荐配置
node run-skill.js lixinger-crawler --min-group-size 10 --max-patterns 20

# 细粒度分析
node run-skill.js lixinger-crawler --min-group-size 3

# 粗粒度分析
node run-skill.js lixinger-crawler --min-group-size 20 --max-patterns 10
```

## 参数速查

| 参数 | 默认 | 说明 |
|------|------|------|
| `--min-group-size <n>` | 5 | 最小分组大小 |
| `--max-patterns <n>` | 无限 | 最大模式数量 |
| `--sample-count <n>` | 5 | 示例URL数量 |
| `--no-markdown` | false | 不生成MD报告 |

## 输出文件

```
stock-crawler/output/{项目名}/
├── url-patterns.json        # 完整数据
├── url-patterns.md          # 可读报告
└── url-patterns-stats.md    # 统计分析 ⭐
```

## 参数选择指南

### 网站规模

| 规模 | URL数 | min-group-size |
|------|-------|----------------|
| 小型 | <1000 | 3-5 |
| 中型 | 1000-5000 | 5-10 |
| 大型 | >5000 | 10-20 |

### 分析目标

| 目标 | 配置 |
|------|------|
| 快速了解 | `--min-group-size 20 --max-patterns 10` |
| 详细分析 | `--min-group-size 3` |
| 平衡模式 | `--min-group-size 10 --max-patterns 20` ⭐ |

## 质量评级

| 覆盖率 | 评级 | 建议 |
|--------|------|------|
| >90% | ✅ Excellent | 保持当前参数 |
| 70-90% | ⚠️ Good | 可降低min-group-size |
| <70% | ❌ Poor | 降低min-group-size |

## 在Kiro中使用

```
"分析 lixinger-crawler 项目的URL模式"
"用最小分组10分析URL"
"显示URL模式统计报告"
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 覆盖率低 | 降低 `--min-group-size` |
| 模式太多 | 提高 `--min-group-size` 或设置 `--max-patterns` |
| 找不到文件 | 检查项目名是否正确 |

## 下一步

```bash
# 分析完URL模式后，进行模板内容分析
cd ../template-content-analyzer
node run-skill.js lixinger-crawler
```

## 帮助

```bash
node run-skill.js --help
```
