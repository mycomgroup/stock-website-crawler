# URL Pattern Analyzer - 质量检查功能总结

## 新增功能

### 1. 质量检查脚本

**文件**: `scripts/validate-patterns.js`

**功能**: 自动检查URL模式分析结果的质量，发现潜在问题

**使用方法**:
```bash
node scripts/validate-patterns.js ../../stock-crawler/output/lixinger-crawler/url-patterns.json
```

### 2. 8个质量检查规则

| 规则 | 级别 | 说明 |
|------|------|------|
| 过大簇检查 | warning | 检查URL数量 > 500 的模式 |
| 样本一致性检查 | error | 检查样本URL路径深度是否一致 |
| 重复名称检查 | warning | 检查是否有相同名称的模式 |
| 过度泛化检查 | warning | 检查路径模板参数占比是否过高 |
| 不一致段检查 | error | 检查样本中是否有半固定段 |
| 模式数量检查 | info | 检查模式总数是否合理 |
| 覆盖率检查 | warning | 检查分类覆盖率是否 >90% |
| 主导簇检查 | warning | 检查最大模式是否占比 >30% |

### 3. 自动优化建议

脚本会根据发现的问题自动生成优化建议：

- 发现大簇 → 建议使用 `--strict-top-n` 或 `--try-refine-top-n`
- 发现样本不一致 → 建议增加 `--refine-max-values` 和减少 `--refine-min-count`
- 模式太多 → 建议增加 `--min-group-size`
- 模式太少 → 建议减少 `--min-group-size` 或启用细分参数
- 覆盖率低 → 建议降低 `--min-group-size`

### 4. 质量标准

#### 优秀 (可以停止迭代)
- ✅ 无错误
- ✅ 警告 ≤ 2个
- ✅ 覆盖率 > 95%
- ✅ 最大簇 < 500 个URL
- ✅ 模式数量在合理范围

#### 良好 (可选继续优化)
- ✅ 无错误
- ⚠️ 警告 3-5个
- ✅ 覆盖率 > 90%
- ⚠️ 最大簇 < 1000 个URL

#### 需要优化 (必须继续)
- ❌ 有错误
- ⚠️ 警告 > 5个
- ❌ 覆盖率 < 90%
- ❌ 最大簇 > 1000 个URL

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

### 优化建议

脚本自动生成的建议：
1. 尝试使用 --try-refine-top-n 10 参数智能拆分大簇
2. 或使用 --strict-top-n 5 --strict-match-ratio 0.85 对大簇应用严格规则
3. 发现样本不一致，建议增加 --refine-max-values 12 --refine-min-count 5 启用更激进的细分

### 下一步行动

```bash
# 方案A: 使用严格模式
node run-skill.js lixinger-crawler \
  --refine-max-values 12 \
  --refine-min-count 5 \
  --strict-top-n 10

# 方案B: 更激进的细分
node run-skill.js lixinger-crawler \
  --min-group-size 10 \
  --refine-max-values 15 \
  --refine-min-count 3 \
  --strict-top-n 15 \
  --strict-match-ratio 0.9
```

## 文档更新

### 新增文档

1. **scripts/validate-patterns.js** - 质量检查脚本
2. **docs/guides/QUALITY_CHECK_WORKFLOW.md** - 质量检查工作流指南
3. **QUALITY_CHECK_SUMMARY.md** - 本文档

### 更新文档

1. **SKILL.md** - 添加质量检查和迭代优化章节
2. **README.md** - 添加质量检查的引用

## AI 使用建议

作为 AI，你应该：

1. **自动化流程**: 每次分析后自动运行质量检查
   ```
   分析 lixinger-crawler 项目的URL模式
   → 运行 run-skill.js
   → 自动运行 validate-patterns.js
   → 解读检查结果
   → 提出优化方案
   ```

2. **解读结果**: 理解每个错误和警告的含义
   - 错误 = 必须修复
   - 警告 = 建议优化
   - 信息 = 参考

3. **生成方案**: 根据问题提出2-3个参数调整方案
   - 方案A: 保守优化
   - 方案B: 激进优化
   - 方案C: 平衡优化

4. **反复迭代**: 最多尝试3-5次
   - 第1次: 默认参数
   - 第2次: 根据问题调整
   - 第3次: 微调优化
   - 第4-5次: 如果需要

5. **记录过程**: 在最终报告中说明优化历程
   ```markdown
   ## 优化过程
   
   ### 第1次分析
   - 参数: 默认
   - 结果: 93个模式，923个最大簇
   - 问题: 93个错误，62个警告
   
   ### 第2次分析
   - 参数: --refine-max-values 12 --refine-min-count 5
   - 结果: 120个模式，450个最大簇
   - 问题: 15个错误，20个警告
   - 改进: 错误减少84%，最大簇减少51%
   
   ### 最终结果
   - 质量: 良好
   - 建议: 可以使用
   ```

## 优势

### 1. 系统化
- 不再凭感觉判断
- 有明确的检查规则
- 有量化的质量标准

### 2. 自动化
- 脚本自动检查
- 自动生成建议
- 减少人工判断

### 3. 可迭代
- 支持反复优化
- 每次都有改进方向
- 最终达到满意结果

### 4. 可解释
- 每个问题都有说明
- 每个建议都有理由
- 优化过程可追溯

## 总结

通过添加质量检查功能，URL Pattern Analyzer 现在支持：

1. ✅ **自动发现问题**: 8个检查规则覆盖常见问题
2. ✅ **自动生成建议**: 根据问题提出具体参数调整
3. ✅ **反复迭代优化**: 支持多次优化直到满意
4. ✅ **质量标准明确**: 优秀/良好/需要优化三个等级
5. ✅ **完整工作流**: 从分析到检查到优化的闭环

这使得 AI 可以更智能地使用这个 skill，不仅能分析，还能自我检查和优化。

---

**添加时间**: 2026-02-26  
**版本**: v1.5.0
