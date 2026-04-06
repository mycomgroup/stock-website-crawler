# QuantsPlaybook Migration Audit (2026-04-05)

## This Round

- Created `30` new same-stem `rq_*.py` files for placeholder strategies that share the same JoinQuant source URL with an existing RiceQuant implementation.
- Those `30` files are alias / reuse coverage, not `30` independently reimplemented and platform-verified migrations.
- Cleared the broad `avg_price -> avg_cost` compatibility issue across the strategy directory.
- Ran the existing local repair scripts and fixed another batch of mechanical compatibility errors.
- Repaired [`rq_58_Debug_多标的版ETF策略.py`](/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/rq_58_Debug_多标的版ETF策略.py) so its position debug output uses live price and correct daily value tracking.

## Current Counts

- Total placeholder `rq_*.txt`: `151`
- Placeholder titles that now also have a same-stem `rq_*.py`: `32`
- Placeholder titles still unresolved: `119`
- `check_comprehensive.py` residual compatibility warnings: `0`
- Deep static review still finds likely broken implementations: `27` `py` files

## Validation Position

- `check_comprehensive.py = 0` only means surface compatibility issues were cleared.
- It does **not** prove the migrated files are runnable end-to-end on the RiceQuant platform.
- Deep static review still flags `27` `py` files that likely have missing variables, broken bootstrapping, or incomplete logic.
- The `30` newly added same-stem `py` files are alias / reuse coverage only; this round did not individually platform-backtest and accept them.
- Therefore, we should **not** claim that "all done files in the current directory are runnable".

## Remaining Placeholder Problem Types

- `39` files: non-standard skip placeholders that still need manual inspection/rewrite
- `5` files: old "already migrated" placeholders, but still no same-stem `py`
- `5` files: multi-library skip cases (`jqfactor` + `jqlib` + ML / external data)
- `4` files: `jqlib.technical_analysis`-heavy ETF timing variants
- `3` files: futures / subportfolio strategies that need RiceQuant-specific redesign
- `2` files: source file missing / unreadable

Representative unresolved platform blockers:

- `jqfactor.get_factor_values`
- `jqlib.technical_analysis`
- `finance.run_query` / `finance.STK_*`
- `jqdata.macro`
- `talib`
- `sklearn` / `xgboost` / `PyTorch`
- futures-only constructs like `type='index_futures'`, `set_subportfolios`
- external research artifacts such as CSV / pickle / pretrained model files

## Remaining Broken `py` Files

These files still look incomplete from static inspection, mostly because `df` / stock-pool bootstrap code is missing or malformed inside a function:

- `rq_01_7年40倍高回撤低.py`
- `rq_02_7年40倍绩优低价小盘.py`
- `rq_06_国九小市值.py`
- `rq_07_为了积分实盘策略.py`
- `rq_100_全市场选股7年5倍.py`
- `rq_19_高股息低PE价投.py`
- `rq_25 低价股优化，18年至今10625.40%，加入防未来函数.py`
- `rq_25_低价股优化.py`
- `rq_36 最简强者恒强策略.py`
- `rq_37 三阳三阴战法.py`
- `rq_39_多因子线性回归APT.py`
- `rq_41 均线黏合突破选股法.py`
- `rq_53_微盘400每日再平衡.py`
- `rq_54_发一个学习策略5年70倍.py`
- `rq_55_价值投资改进版-6年9.5倍.py`
- `rq_59_基于Gyro大神的小市值策略的因子匹配研究.py`
- `rq_60_深度解析_资产负债与ROA模型.py`
- `rq_61_抄底神器2.0低回撤高成功率.py`
- `rq_66_PB-POE+双均线.py`
- `rq_68_胜率78%_6年36倍.py`
- `rq_76 小市值止损策略【年化104.11% 最大回撤30.65%】.py`
- `rq_77 超强单因子策略（EBITEV）.py`
- `rq_78 ffscore选股加rsrs择时.py`
- `rq_78 首板低开策略-终极版 最大回撤15%，年化50%.py`
- `rq_79 EPS+MS因子的大盘蓝筹策略.py`
- `rq_80 【深度解析 一】经典小市值深度研究模型.py`
- `rq_81 低PB小市值低换手策略总结.py`

## Notes

- The newly created alias `py` files are intentionally conservative: they reuse an existing migrated implementation only when the original JoinQuant post URL matches.
- This means the highest-value "duplicate / same-source" placeholders are now covered, but the remaining `119` placeholders still need true strategy-by-strategy migration work.
- A same-stem `py`, a historical cloud backtest, or a finished submission record should not be read as proof that the current local file is runnable.
