"""探测更多 DAI 表"""
import dai

def q(table, extra="where date='2024-01-02' limit 2"):
    sql = "select * from " + table + " " + extra
    try:
        df = dai.query(sql).df()
        cols = list(df.columns)[:6]
        return "OK " + str(len(df)) + "rows cols=" + str(cols)
    except Exception as e:
        return "FAIL " + str(e).split('\n')[0][:80]

# 指数数据
print("=== 指数 ===")
for t in ['cn_index_bar1d', 'cn_index_bar1m', 'index_1d', 'cn_index_1d', 'cn_index_daily']:
    print(t + ": " + q(t))

# 用 filters 参数
print("\n=== cn_stock_instruments (filters) ===")
try:
    df = dai.query("select * from cn_stock_instruments", filters={"date": ["2024-01-02"]}).df()
    print("OK " + str(len(df)) + " rows cols=" + str(list(df.columns)[:8]))
    if len(df) > 0:
        print(df.head(2).to_string())
except Exception as e:
    print("FAIL " + str(e)[:200])

# 涨跌停
print("\n=== 涨跌停 ===")
for t in ['cn_stock_limit', 'cn_stock_limit_up_down', 'cn_stock_price_limit', 'cn_stock_bar1d_limit']:
    print(t + ": " + q(t))

# 财务
print("\n=== 财务 ===")
for t in ['cn_stock_financial_indicator', 'cn_stock_income_statement', 'cn_stock_cash_flow', 'cn_stock_financial']:
    print(t + ": " + q(t))

# 因子
print("\n=== 因子 ===")
for t in ['cn_stock_factor', 'cn_stock_alpha_factor', 'cn_stock_technical_factor']:
    print(t + ": " + q(t))

# 估值完整字段
print("\n=== cn_stock_valuation 完整字段 ===")
try:
    df = dai.query("select * from cn_stock_valuation where date='2024-01-02' and instrument='000001.SZ'").df()
    print("cols: " + str(list(df.columns)))
    print(df.to_string())
except Exception as e:
    print("FAIL " + str(e)[:200])

# cn_stock_bar1d 完整字段
print("\n=== cn_stock_bar1d 完整字段 ===")
try:
    df = dai.query("select * from cn_stock_bar1d where date='2024-01-02' and instrument='000001.SZ'").df()
    print("cols: " + str(list(df.columns)))
    print(df.to_string())
except Exception as e:
    print("FAIL " + str(e)[:200])

# balance_sheet 字段
print("\n=== cn_stock_balance_sheet 字段 ===")
try:
    df = dai.query("select * from cn_stock_balance_sheet where instrument='000001.SZ' limit 1").df()
    print("cols: " + str(list(df.columns)))
except Exception as e:
    print("FAIL " + str(e)[:200])

print("\n=== 完成 ===")
