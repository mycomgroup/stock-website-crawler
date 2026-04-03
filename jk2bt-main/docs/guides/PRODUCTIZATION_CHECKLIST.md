# 产品化收口清单

更新时间：2026-04-03

## 目标标准

- [x] 安装后可直接导入主包与兼容包
- [x] 核心策略可稳定跑通（含 UTF-8/GBK 策略文件）
- [x] 回归测试可稳定收集，避免导入期崩溃
- [x] 关键 smoke 用例可重复通过
- [x] 文档提供“安装后验收”命令

## 已完成的关键修复

- [x] `statsmodels` 改为可选导入，并提供回退计算逻辑
- [x] `txt_strategy_normalizer` 去除 `chardet` 硬依赖（内置编码检测回退）
- [x] 补齐兼容导入层（`src/*`、顶层包别名、`jk2bt.indicators`）
- [x] 补齐样本策略目录兼容路径 `tests/sample_strategies`
- [x] `run_strategies_parallel._classify_run_status` 兼容旧签名与旧调用方式
- [x] DuckDB 并发读写配置冲突时自动降级连接策略，提升稳定性
- [x] `pytest.ini` 增加 `integration/regression/slow/unit` markers，消除未知标记告警

## 验证命令（建议作为发布前 gate）

```bash
python3 -c "import jk2bt; print(jk2bt.__version__)"
pytest --collect-only -q
pytest -q tests/test_package_import.py tests/integration/test_jq_runner.py tests/test_txt_strategy_normalizer.py tests/test_batch_runner_smoke.py tests/test_batch_runner_extended.py tests/api_compatibility/test_date_api.py
```

## 最近一次验证结果

- `pytest --collect-only -q`：4298 tests collected
- 核心产品化回归命令（见上）：217 passed
- 其中包含安装导入、编码兼容、批量运行器、日期 API、策略执行等关键链路

## 仍需持续关注（非阻塞）

- 全量 4000+ 测试的定期 CI（建议分层并行执行）
- 数据源波动导致的结果漂移监控（建议固定样本+基线快照）
- 结果可解释性报告（建议统一输出版本号、数据时间戳、关键参数）
