# Autoresearch 系统常见问题解答

## 通用问题

### Q1: 什么是 Autoresearch 系统？

Autoresearch 是一套自动化策略优化系统，通过 AI Agent 自主迭代探索参数空间，寻找最优策略配置。

### Q2: 系统如何决策 keep 还是 rollback？

评分公式：
```python
calmar = annual_return / max(abs(max_drawdown), 0.01)
score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20
```

决策规则：
1. **硬约束检查**：`abs(max_drawdown) > 0.35` → 直接 rollback
2. **分数比较**：`new_score > champion_score` → keep，否则 rollback
3. **严格大于**：必须严格大于，相等也会 rollback

### Q3: 如何查看实验进度？

```bash
# 查看迭代历史
cat experiments/<name>/iterations.tsv

# 查看详细分析
python analyze.py --base experiments/<name>

# 查看当前状态
cat experiments/<name>/state.json
```

---

## 初始化问题

### Q4: 初始化失败怎么办？

**常见原因**：
1. **种子配置不存在**：检查 `seed_config.json` 是否存在
2. **权限问题**：确保有写入权限
3. **Git 未安装**：系统需要 git 进行版本管理

**解决方法**：
```bash
# 检查 git
git --version

# 检查权限
ls -la experiments/

# 使用 verbose 模式查看详细错误
python setup.py --name test --verbose
```

### Q5: 如何使用自定义种子配置？

```bash
# 复制并修改种子配置
cp seed_config.json my_seed.json
# 编辑 my_seed.json...

# 使用自定义配置初始化
python setup.py --name my_exp --seed-config my_seed.json
```

---

## 迭代问题

### Q6: 迭代一直 rollback 怎么办？

**可能原因**：
1. **变异幅度太大**：尝试更小的参数调整
2. **方向错误**：尝试不同的变异类型
3. **局部最优**：考虑重新初始化或调整评分权重

**建议策略**：
```bash
# 1. 先做小幅调整
python run_iteration.py --base experiments/<name> \
    --mutation-summary "微调：持仓数量 30 → 32" \
    --mutation-type adjust_holding_num

# 2. 查看历史成功的变异类型
grep "keep" experiments/<name>/iterations.tsv

# 3. 分析失败原因
python analyze.py --base experiments/<name>
```

### Q7: 回测超时怎么办？

**默认超时**：300 秒（5 分钟）

**解决方法**：
```bash
# 增加超时时间（秒）
python run_iteration.py --base experiments/<name> \
    --mutation-summary "..." \
    --timeout 600
```

### Q8: 如何手动回滚到某个版本？

```bash
cd experiments/<name>

# 查看 git 历史
git log --oneline

# 回滚到指定 commit
git checkout <commit_hash> -- wizard_config.json

# 更新 state.json 中的 champion_iter
```

---

## 配置问题

### Q9: 如何验证配置是否合法？

```bash
python validate.py --config experiments/<name>/wizard_config.json
python validate.py --config experiments/<name>/wizard_config.json --strict
```

### Q10: 配置中的因子名称从哪里来？

查看 `skills/ricequant-wizard/shared/factor-catalog.json` 或访问 RiceQuant 官方文档。

### Q11: 如何调整评分权重？

修改 `scorer.py` 中的 `DEFAULT_WEIGHTS`：

```python
DEFAULT_WEIGHTS = {
    "calmar": 0.55,      # Calmar 比率权重
    "sortino": 0.25,     # Sortino 比率权重
    "information": 0.20, # 信息比率权重
}
```

---

## 性能问题

### Q12: 如何加速迭代？

1. **并行运行**：在不同实验目录同时运行多个迭代
2. **缩短回测周期**：调整 `start_date`（但可能影响结果可靠性）
3. **使用 Mock 模式**：开发测试时使用模拟数据

```bash
# Mock 模式（仅测试用）
export RICEQUANT_MOCK_MODE=1
```

### Q13: 历史文件太多怎么办？

```bash
# 清理旧实验（保留最近 N 次）
python analyze.py --base experiments/<name> --cleanup --keep 50

# 归档旧实验
tar -czf experiments_backup_$(date +%Y%m%d).tar.gz experiments/
```

---

## 故障排查

### Q14: 系统完全无法运行

**检查清单**：
```bash
# 1. Python 版本
python --version  # 需要 >= 3.8

# 2. 依赖安装
pip install -e .

# 3. 环境变量
env | grep RICEQUANT

# 4. 平台连接
python -c "from wizard_executor import validate_session; print(validate_session())"

# 5. 文件权限
ls -la experiments/
```

### Q15: 如何重置实验？

```bash
# 完全重置（删除所有历史）
rm -rf experiments/<name>
python setup.py --name <name>

# 保留历史，重置状态
cd experiments/<name>
git log --oneline  # 找到 baseline commit
git reset --hard <baseline_commit>
# 手动编辑 state.json，重置 current_iter 和 champion_score
```

---

## 最佳实践

### Q16: 有哪些使用建议？

1. **从小改动开始**：先做微调，验证系统正常工作
2. **定期备份**：重要实验定期备份 `experiments/` 目录
3. **记录笔记**：在 `search_notes.md` 中记录思路
4. **监控指标**：关注 max_drawdown，避免过度优化
5. **多样化探索**：尝试不同的变异类型，避免局部最优
6. **版本管理**：利用 git 历史追溯每次改动
7. **参数范围**：设置合理的参数边界，避免极端值
8. **回测周期**：使用足够长的回测周期（建议 >= 3 年）
