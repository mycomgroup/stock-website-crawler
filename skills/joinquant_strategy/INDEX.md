# 聚宽策略批量提交系统 - 文档索引

## 📚 快速导航

### 🚀 新手入门
1. [README.md](README.md) - **从这里开始**
   - 快速开始指南
   - 安装和配置
   - 基本使用方法

2. [FINAL_SUMMARY.md](FINAL_SUMMARY.md) - **项目总览**
   - 项目完成状态
   - 三批次数据汇总
   - Top10策略列表
   - 快速参考

### 📖 详细文档
3. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - **项目结构**
   - 完整目录结构
   - 文件说明
   - 工作流程
   - 配置文件

4. [CHECKLIST.md](CHECKLIST.md) - **检查清单**
   - 完整性检查
   - 验证命令
   - 待办事项

5. [MIGRATION_COMPLETE.md](MIGRATION_COMPLETE.md) - **迁移报告**
   - 迁移内容
   - 验证结果
   - 数据统计

### 📊 数据报告
6. [data/THREE_BATCHES_SUMMARY.md](data/THREE_BATCHES_SUMMARY.md) - **三批次总结**
   - 执行概况
   - 批次详情
   - Top10策略
   - 经验总结

7. [data/TOP100_README.md](data/TOP100_README.md) - **Top100说明**
   - 筛选标准
   - 统计信息
   - 使用方法

8. [data/all_batches_summary.md](data/all_batches_summary.md) - **汇总分析**
   - 总体概况
   - 各批次详情
   - 盈利策略（待收集）

### 🛠️ 工具脚本
9. [verify_setup.sh](verify_setup.sh) - **验证脚本**
   - 项目完整性检查
   - 自动验证所有组件

---

## 📂 核心脚本

### 策略筛选
- `select_top_strategies.js` - 智能筛选策略

### 批量提交
- `batch_submit_jq558_async.js` - 通用提交脚本
- `batch_submit_selected.js` - Top100提交脚本
- `batch_submit_top100.sh` - Shell包装脚本

### 结果收集
- `collect_jq558_results.js` - 收集回测结果
- `analyze_all_batches.js` - 汇总分析

### 会话管理
- `browser/capture-session.js` - 捕获登录会话
- `request/ensure-session.js` - 确保会话有效

### API客户端
- `request/joinquant-strategy-client.js` - 聚宽API封装

---

## 📁 数据目录

### 批次数据
- `data/jq558_batch_20260403/` - 批次1（21个策略）
- `data/jq558_batch_20260404/` - 批次2（585个策略）
- `data/jq558_top100_20260405/` - 批次3（100个策略）

### 筛选和汇总
- `data/selected_top100.json` - Top100筛选结果
- `data/all_batches_summary.json` - 汇总数据
- `data/session.json` - 登录会话

---

## 🎯 按任务查找

### 我想了解项目
→ [README.md](README.md) + [FINAL_SUMMARY.md](FINAL_SUMMARY.md)

### 我想查看三批次结果
→ [data/THREE_BATCHES_SUMMARY.md](data/THREE_BATCHES_SUMMARY.md)

### 我想了解项目结构
→ [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

### 我想验证项目完整性
→ 运行 `bash verify_setup.sh`

### 我想查看Top10策略
→ [FINAL_SUMMARY.md](FINAL_SUMMARY.md) 或 [data/THREE_BATCHES_SUMMARY.md](data/THREE_BATCHES_SUMMARY.md)

### 我想提交新策略
→ [README.md](README.md) 的"快速开始"部分

### 我想收集回测结果
→ [README.md](README.md) 的"使用示例"部分

### 我想查看迁移详情
→ [MIGRATION_COMPLETE.md](MIGRATION_COMPLETE.md)

---

## 📊 数据统计

### 三批次汇总
```
总提交: 706个
成功:   303个 (42.92%)
失败:   403个 (57.08%)
```

### 各批次
- 批次1: 21个提交，16个成功 (76.19%)
- 批次2: 585个提交，211个成功 (36.07%)
- 批次3: 100个提交，76个成功 (76.00%)

---

## 🔗 快速链接

### 主要文档
- [README.md](README.md) - 主文档
- [FINAL_SUMMARY.md](FINAL_SUMMARY.md) - 最终总结
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构
- [CHECKLIST.md](CHECKLIST.md) - 检查清单

### 数据报告
- [三批次总结](data/THREE_BATCHES_SUMMARY.md)
- [Top100说明](data/TOP100_README.md)
- [汇总分析](data/all_batches_summary.md)

### 工具
- [验证脚本](verify_setup.sh)

---

## 💡 常用命令

### 查看文档
```bash
cat README.md                      # 主文档
cat FINAL_SUMMARY.md               # 最终总结
cat PROJECT_STRUCTURE.md           # 项目结构
cat data/THREE_BATCHES_SUMMARY.md  # 三批次总结
```

### 验证项目
```bash
bash verify_setup.sh
```

### 核心操作
```bash
node select_top_strategies.js              # 筛选策略
node batch_submit_selected.js              # 提交Top100
node collect_jq558_results.js --dir ...    # 收集结果
node analyze_all_batches.js                # 生成报告
```

---

## 📍 项目位置
```
/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/
```

---

**最后更新**: 2026-04-06

**文档数量**: 9个主要文档

**项目状态**: ✅ 就绪可用
