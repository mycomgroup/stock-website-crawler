# 策略增强 V3：Entry Overlay 作为根目录独立项目

## 本次完善重点

根据评审意见，本次把增强模块从 `strategies/enhancements` 提升为**仓库根目录独立项目**：

- 独立目录：`/entry_overlay`
- 独立文档：`entry_overlay/README.md`、`entry_overlay/docs/PRODUCT.md`
- 独立测试：`entry_overlay/tests/*`
- 兼容旧路径：`strategies/enhancements/ta_entry_overlay.py` 和 `strategies/enhancements/entry_overlay/__init__.py` 继续可用

---

## 目录结构（清晰化）

```text
entry_overlay/
  __init__.py
  README.md
  data_sources.py
  factors.py
  profiles.py
  engine.py
  offline.py
  run_offline_validation.py
  docs/
    PRODUCT.md
  tests/
    test_factors.py
    test_engine.py
    test_offline.py
```

---

## 功能覆盖（可增强所有策略）

1. **数据兼容层**：JoinQuant / Akshare / Pandas。
2. **双模式介入**：
   - `rank_filter`：选股后排序过滤；
   - `timing_only`：必须买，仅择时。
3. **通用因子能力**：15 TA 因子统一标准化评分。
4. **内置风格模板**：general / trend / reversal。
5. **离线验证能力**：事件回测 + 网格搜索 + CLI。

---

## 上线建议

1. 先离线：`python -m entry_overlay.run_offline_validation ...`
2. 再灰度：单策略 A/B 对比。
3. 最后推广：多策略复用同一 overlay 项目。

