"""
生成沪深300等权股票池 pool_panel.csv
用法：python strategies/local_backtest/gen_hs300_pool.py

依赖：pip install akshare pandas
"""
import pandas as pd
import akshare as ak

START = "2021-01-01"
END   = "2026-01-01"
OUT   = "strategies/local_backtest/pool_panel.csv"

# ── 1. 拉沪深300当前成分股 ────────────────────────────────────────────────────
print("获取沪深300成分股...")
cons = ak.index_stock_cons_weight_csindex(symbol="000300")
# 列名：成分券代码、成分券名称、交易所、权重(%)
codes_raw = cons["成分券代码"].tolist()

# ── 2. 转换代码格式：6位数字 → JQ格式 ─────────────────────────────────────────
def to_jq(code: str) -> str:
    """600xxx/688xxx → .XSHG，其余 → .XSHE"""
    if code.startswith("6"):
        return f"{code}.XSHG"
    return f"{code}.XSHE"

codes = [to_jq(c) for c in codes_raw]
weight = round(1.0 / len(codes), 6)
print(f"成分股数量: {len(codes)}，等权权重: {weight:.4%}")

# ── 3. 生成每个交易日的持仓记录 ───────────────────────────────────────────────
print("生成交易日序列...")
# 用 akshare 获取 A 股交易日历
cal = ak.tool_trade_date_hist_sina()
cal["trade_date"] = pd.to_datetime(cal["trade_date"])
dates = cal[
    (cal["trade_date"] >= START) & (cal["trade_date"] <= END)
]["trade_date"].sort_values()

print(f"交易日数量: {len(dates)}")

# ── 4. 组装 DataFrame ─────────────────────────────────────────────────────────
rows = []
for d in dates:
    date_str = d.strftime("%Y-%m-%d")
    for i, code in enumerate(codes):
        rows.append({
            "date": date_str,
            "code": code,
            "weight": weight,
            "score": weight,   # score 列 strategy_kits 也会用到
            "rank": i + 1,
        })

df = pd.DataFrame(rows)
df.to_csv(OUT, index=False)
print(f"\n已生成: {OUT}")
print(f"总行数: {len(df):,}  ({len(dates)} 天 × {len(codes)} 只)")
print(df.head(3).to_string())
