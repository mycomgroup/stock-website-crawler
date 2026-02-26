# URL Pattern Analyzer - 质量检查工作流

## 概述

这个文档描述了如何使用质量检查脚本来发现问题并反复优化URL模式分析结果。

## 工作流程

```
1. 初次分析
   ↓
2. 质量检查 ← ┐
   ↓          │
3. 发现问题   │
   ↓          │
4. 调整参数   │
   ↓          │
5. 重新分析 ──┘
   ↓
6. 满意结果
```

## 详细步骤

### 步骤1: 初次分析

使用默认参数进行第一次分析：

```bash
node run-skill.js lixinger-crawler
```

### 步骤2: 质量检查

运行验证脚本检查结果质量：

```bash
node scripts/validate-patterns.js ../../stock-crawler/output/lixinger-crawler/url-patterns.json
```

### 步骤3: 解读检查结果

#### 错误级别 (❌ Error)
**必须修复**，表示分类有明显问题：
- 样本一致性检查失败
- 不一致段检查失败

#### 警告级别 (⚠️ Warning)
**建议优化**，表示可以改进：
- 过大簇（>500 URLs）
- 重复名称
- 过度泛化
- 覆盖率低
- 主导簇占比过高

#### 信息级别 (ℹ️ Info)
**参考信息**：
- 模式数量统计

### 步骤4: 根据问题调整参数

#### 问题类型1: 发现大簇（>500 URLs）

**症状**:
```
⚠️ 模式 "analytics-chart-maker" 包含 923 个URL
```

**解决方案**:
```bash
# 方案A: 使用严格模式
node run-skill.js lixinger-crawler --strict-top-n 10 --strict-match-ratio 0.85

# 方案B: 增加细分参数
node run-skill.js lixinger-crawler --refine-max-values 12 --refine-min-count 5
```

#### 问题类型2: 样本不一致

**症状**:
```
❌ 模式 "detail-sz" 的样本中发现半固定段
```

**解决方案**:
```bash
# 启用更激进的细分
node run-skill.js lixinger-crawler \
  --refine-max-values 12 \
  --refine-min-count 5 \
  --strict-top-n 10
```

#### 问题类型3: 重复名称

**症状**:
```
⚠️ 模式名称 "detail-sz" 重复出现
```

**解决方案**:
```bash
# 增加细分参数，让相同名称的模式进一步分开
node run-skill.js lixinger-crawler \
  --refine-max-values 10 \
  --refine-min-count 8
```

#### 问题类型4: 模式数量过多

**症状**:
```
ℹ️ 模式数量 150 可能过多
```

**解决方案**:
```bash
# 增加最小分组大小
node run-skill.js lixinger-crawler --min-group-size 20
```

#### 问题类型5: 覆盖率低

**症状**:
```
⚠️ 覆盖率 85% 较低
```

**解决方案**:
```bash
# 降低最小分组大小
node run-skill.js lixinger-crawler --min-group-size 3
```

### 步骤5: 重新分析并检查

```bash
# 使用新参数重新分析
node run-skill.js lixinger-crawler [新参数]

# 再次质量检查
node scripts/validate-patterns.js ../../stock-crawler/output/lixinger-crawler/url-patterns.json
```

### 步骤6: 判断是否满意

#### 优秀标准 (可以停止)
- ✅ 无错误
- ✅ 警告 ≤ 2个
- ✅ 覆盖率 > 95%
- ✅ 最大簇 < 500 个URL
- ✅ 模式数量在合理范围

#### 良好标准 (可选继续)
- ✅ 无错误
- ⚠️ 警告 3-5个
- ✅ 覆盖率 > 90%
- ⚠️ 最大簇 < 1000 个URL

#### 需要优化 (必须继续)
- ❌ 有错误
- ⚠️ 警告 > 5个
- ❌ 覆盖率 < 90%
- ❌ 最大簇 > 1000 个URL

## 实战案例: lixinger-crawler

### 第1次分析

```bash
node run-skill.js lixinger-crawler
```

**结果**:
- 模式数量: 93
- 最大簇: 923 个URL
- 覆盖率: 100%

### 第1次质量检查

```bash
node scripts/validate-patterns.js ../../stock-crawler/output/lixinger-crawler/url-patterns.json
```

**发现问题**:
- ❌ 93个错误: 所有模式都有半固定段
- ⚠️ 3个警告: 有大簇（>500 URLs）
- ⚠️ 59个警告: 重复名称

**分析**:
- 主要问题是半固定段未被识别
- 需要更激进的细分策略

### 第2次分析

```bash
node run-skill.js lixinger-crawler \
  --refine-max-values 12 \
  --refine-min-count 5 \
  --strict-top-n 10
```

**预期改进**:
- 半固定段会被识别和细分
- 大簇会被进一步拆分
- 重复名称会减少

### 第2次质量检查

```bash
node scripts/validate-patterns.js ../../stock-crawler/output/lixinger-crawler/url-patterns.json
```

**评估结果**:
- 如果错误减少到 < 10个: 继续优化
- 如果错误仍然很多: 尝试更激进的参数

### 第3次分析（如果需要）

```bash
node run-skill.js lixinger-crawler \
  --min-group-size 10 \
  --refine-max-values 15 \
  --refine-min-count 3 \
  --strict-top-n 15 \
  --strict-match-ratio 0.9
```

## 参数调优速查表

| 问题 | 参数调整 | 效果 |
|------|---------|------|
| 大簇 (>500) | `--strict-top-n 10` | 细分大簇 |
| 样本不一致 | `--refine-max-values 12` | 识别半固定段 |
| 重复名称 | `--refine-min-count 5` | 更激进细分 |
| 模式太多 | `--min-group-size 20` | 减少模式 |
| 模式太少 | `--min-group-size 3` | 增加模式 |
| 覆盖率低 | `--min-group-size 3` | 包含更多小簇 |

## 常见参数组合

### 保守模式（减少模式）
```bash
node run-skill.js lixinger-crawler \
  --min-group-size 20 \
  --refine-max-values 5 \
  --refine-min-count 20
```

### 平衡模式（默认）
```bash
node run-skill.js lixinger-crawler \
  --min-group-size 10 \
  --refine-max-values 8 \
  --refine-min-count 10
```

### 激进模式（增加模式）
```bash
node run-skill.js lixinger-crawler \
  --min-group-size 5 \
  --refine-max-values 15 \
  --refine-min-count 3 \
  --strict-top-n 15
```

## AI 使用建议

作为 AI，你应该：

1. **自动化流程**: 每次分析后自动运行质量检查
2. **解读结果**: 理解每个错误和警告的含义
3. **生成方案**: 根据问题提出2-3个参数调整方案
4. **反复迭代**: 最多尝试3-5次
5. **记录过程**: 在最终报告中说明优化历程

### 示例对话流程

```
AI: 我已完成初次分析，现在运行质量检查...

[运行质量检查]

AI: 发现以下问题:
- 93个错误: 半固定段未识别
- 3个警告: 大簇问题
- 59个警告: 重复名称

建议使用更激进的细分参数。我将尝试方案A...

[重新分析]

AI: 第2次分析完成，再次检查质量...

[再次质量检查]

AI: 改进情况:
- 错误减少到 15个
- 警告减少到 8个
- 覆盖率保持 99%

继续优化...
```

## 总结

质量检查工作流的核心是：
1. **发现问题**: 使用验证脚本
2. **理解问题**: 分析错误和警告
3. **解决问题**: 调整参数
4. **验证效果**: 重新检查
5. **反复迭代**: 直到满意

通过这个流程，可以系统性地提升URL模式分析的质量。
