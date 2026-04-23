# Entry Overlay（独立策略增强项目）

`entry_overlay` 是放在仓库根目录的独立项目，用于增强所有策略的买点执行质量。

## 设计目标

- 不改动原策略“选股/仓位/卖出风控”主流程。
- 统一接入 JoinQuant / Akshare / 本地数据。
- 支持两种模式：
  - `rank_filter`：选股后的最终排序与过滤。
  - `timing_only`：必须买，仅选择更好的买入时机。
- 提供离线回测与参数搜索，先离线定参再线上接入。

## 目录结构

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

## 快速使用

```python
from entry_overlay import EntryOverlayConfig, EntryOverlayEngine, EntryMode, JQDataAdapter

adapter = JQDataAdapter()
engine = EntryOverlayEngine(
    EntryOverlayConfig(mode=EntryMode.RANK_FILTER, profile="trend", min_score_to_buy=0.60)
)

bars = adapter.get_bars(code="000001.XSHE", start=None, end=context.current_dt, freq="1m", count=240)
decision = engine.decide(bars)
if decision.should_buy:
    order_target_value("000001.XSHE", 100000)
```

## 离线参数搜索

```bash
python -m entry_overlay.run_offline_validation \
  --bars data/minute_bars.csv \
  --events data/events.csv \
  --mode rank_filter \
  --out overlay_grid_result.csv
```

## 运行测试

```bash
python -m pytest -q entry_overlay/tests
```
