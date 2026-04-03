"""
BigQuant DAI 全量数据表探测
目标：找出所有可用的数据表和字段
"""
import dai

def q(sql, filters=None):
    try:
        if filters:
            df = dai.query(sql, filters=filters).df()
        else:
            df = dai.query(sql).df()
        cols = list(df.columns)
        return "OK " + str(len(df)) + "rows cols=" + str(cols)
    except Exception as e:
        msg = str(e).split('\n')[0][:100]
        return "FAIL " + msg

print("=== BigQuant DAI 全量数据表探测 ===")
print("日期: 2024-01-02")
print()

D = "2024-01-02"
D_RANGE = ["2024-01-01", "2024-03-31"]

# ── 行情数据 ──────────────────────────────────────────
print("=== 行情数据 ===")
tables = {
    "cn_stock_bar1d":       "select * from cn_stock_bar1d where date='" + D + "' and instrument='000001.SZ'",
    "cn_stock_bar1m":       "select * from cn_stock_bar1m where date='" + D + "' limit 2",
    "cn_stock_bar5m":       "select * from cn_stock_bar5m where date='" + D + "' limit 2",
    "cn_stock_bar15m":      "select * from cn_stock_bar15m where date='" + D + "' limit 2",
    "cn_stock_bar30m":      "select * from cn_stock_bar30m where date='" + D + "' limit 2",
    "cn_stock_bar60m":      "select * from cn_stock_bar60m where date='" + D + "' limit 2",
    "cn_stock_bar1w":       "select * from cn_stock_bar1w where date='" + D + "' limit 2",
    "cn_stock_bar1mo":      "select * from cn_stock_bar1mo where date='" + D + "' limit 2",
}
for name, sql in tables.items():
    print(name + ": " + q(sql))

# ── 指数行情 ──────────────────────────────────────────
print("\n=== 指数行情 ===")
idx_tables = {
    "cn_index_bar1d":       "select * from cn_index_bar1d where date='" + D + "' limit 2",
    "cn_index_bar1m":       "select * from cn_index_bar1m where date='" + D + "' limit 2",
    "cn_index_bar1w":       "select * from cn_index_bar1w where date='" + D + "' limit 2",
    "cn_index_bar1mo":      "select * from cn_index_bar1mo where date='" + D + "' limit 2",
    "cn_index_components":  "select * from cn_index_components where date='" + D + "' limit 2",
    "cn_index_info":        "select * from cn_index_info limit 2",
}
for name, sql in idx_tables.items():
    print(name + ": " + q(sql))

# ── 估值数据 ──────────────────────────────────────────
print("\n=== 估值数据 ===")
val_tables = {
    "cn_stock_valuation":   "select * from cn_stock_valuation where date='" + D + "' and instrument='000001.SZ'",
    "cn_stock_valuation2":  "select * from cn_stock_valuation2 where date='" + D + "' limit 2",
}
for name, sql in val_tables.items():
    print(name + ": " + q(sql))

# ── 财务数据 ──────────────────────────────────────────
print("\n=== 财务数据 ===")
fin_tables = {
    "cn_stock_balance_sheet":       "select * from cn_stock_balance_sheet where instrument='000001.SZ' limit 1",
    "cn_stock_income_statement":    "select * from cn_stock_income_statement where instrument='000001.SZ' limit 1",
    "cn_stock_cash_flow":           "select * from cn_stock_cash_flow where instrument='000001.SZ' limit 1",
    "cn_stock_financial_indicator": "select * from cn_stock_financial_indicator where instrument='000001.SZ' limit 1",
    "cn_stock_financial_derivative":"select * from cn_stock_financial_derivative where instrument='000001.SZ' limit 1",
}
for name, sql in fin_tables.items():
    r = q(sql, filters={"date": D_RANGE}) if "balance" in name or "income" in name or "cash" in name else q(sql)
    print(name + ": " + r)

# ── 股票基本信息 ──────────────────────────────────────
print("\n=== 股票基本信息 ===")
info_tables = {
    "cn_stock_instruments":     "select * from cn_stock_instruments limit 3",
    "cn_stock_industry":        "select * from cn_stock_industry limit 3",
    "cn_stock_concept":         "select * from cn_stock_concept limit 3",
    "cn_stock_sw_industry":     "select * from cn_stock_sw_industry limit 3",
    "cn_stock_zjh_industry":    "select * from cn_stock_zjh_industry limit 3",
}
for name, sql in info_tables.items():
    if "instruments" in name:
        print(name + ": " + q(sql, filters={"date": [D]}))
    else:
        print(name + ": " + q(sql))

# ── 特殊数据 ──────────────────────────────────────────
print("\n=== 特殊数据 ===")
special_tables = {
    "cn_stock_margin":          "select * from cn_stock_margin where date='" + D + "' limit 2",
    "cn_stock_holder":          "select * from cn_stock_holder where date='" + D + "' limit 2",
    "cn_stock_pledge":          "select * from cn_stock_pledge where date='" + D + "' limit 2",
    "cn_stock_repurchase":      "select * from cn_stock_repurchase where date='" + D + "' limit 2",
    "cn_stock_announcement":    "select * from cn_stock_announcement where date='" + D + "' limit 2",
    "cn_stock_dividend":        "select * from cn_stock_dividend where date='" + D + "' limit 2",
    "cn_stock_rights_issue":    "select * from cn_stock_rights_issue where date='" + D + "' limit 2",
    "cn_stock_split":           "select * from cn_stock_split where date='" + D + "' limit 2",
    "cn_stock_suspend":         "select * from cn_stock_suspend where date='" + D + "' limit 2",
    "cn_stock_st":              "select * from cn_stock_st where date='" + D + "' limit 2",
    "cn_stock_moneyflow":       "select * from cn_stock_moneyflow where date='" + D + "' limit 2",
    "cn_stock_tick":            "select * from cn_stock_tick where date='" + D + "' limit 2",
}
for name, sql in special_tables.items():
    print(name + ": " + q(sql))

# ── 宏观数据 ──────────────────────────────────────────
print("\n=== 宏观数据 ===")
macro_tables = {
    "cn_macro_money_supply":    "select * from cn_macro_money_supply limit 2",
    "cn_macro_cpi":             "select * from cn_macro_cpi limit 2",
    "cn_macro_ppi":             "select * from cn_macro_ppi limit 2",
    "cn_macro_gdp":             "select * from cn_macro_gdp limit 2",
    "cn_macro_pmi":             "select * from cn_macro_pmi limit 2",
}
for name, sql in macro_tables.items():
    print(name + ": " + q(sql))

# ── cn_stock_bar1d 完整字段 ───────────────────────────
print("\n=== cn_stock_bar1d 完整字段 ===")
try:
    df = dai.query("select * from cn_stock_bar1d where date='" + D + "' and instrument='000001.SZ'").df()
    print("字段列表: " + str(list(df.columns)))
    print(df.to_string())
except Exception as e:
    print("FAIL: " + str(e)[:200])

# ── cn_stock_valuation 完整字段 ──────────────────────
print("\n=== cn_stock_valuation 完整字段 ===")
try:
    df = dai.query("select * from cn_stock_valuation where date='" + D + "' and instrument='000001.SZ'").df()
    print("字段列表: " + str(list(df.columns)))
    print(df.to_string())
except Exception as e:
    print("FAIL: " + str(e)[:200])

# ── cn_stock_industry 完整字段 ───────────────────────
print("\n=== cn_stock_industry 完整字段 ===")
try:
    df = dai.query("select * from cn_stock_industry limit 2").df()
    print("字段列表: " + str(list(df.columns)))
    print(df.to_string())
except Exception as e:
    print("FAIL: " + str(e)[:200])

print("\n=== 探测完成 ===")
