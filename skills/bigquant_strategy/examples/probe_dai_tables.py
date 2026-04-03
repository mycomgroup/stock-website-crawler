"""
探测 BigQuant DAI 数据库的所有可用表
"""
import dai

print("=== DAI 可用数据表 ===\n")

# 列出所有表
try:
    tables = dai.query("SHOW TABLES").df()
    print(f"总表数: {len(tables)}")
    for _, row in tables.iterrows():
        print(f"  {row.iloc[0]}")
except Exception as e:
    print(f"SHOW TABLES 失败: {e}")

# 尝试常见表名
print("\n=== 测试常见表 ===")
test_tables = [
    # K线数据
    ("cn_stock_bar1d", "select date,instrument,open,high,low,close,volume,amount from cn_stock_bar1d where date='2024-01-02' limit 3"),
    ("cn_stock_bar1m", "select date,instrument,close from cn_stock_bar1m where date='2024-01-02' limit 3"),
    # 指数
    ("cn_index_bar1d", "select date,instrument,close from cn_index_bar1d where date='2024-01-02' limit 3"),
    ("index_bar1d", "select date,instrument,close from index_bar1d where date='2024-01-02' limit 3"),
    # 估值
    ("cn_stock_valuation", "select date,instrument,pe_ttm,pb from cn_stock_valuation where date='2024-01-02' limit 3"),
    ("cn_stock_valuation_factor", "select * from cn_stock_valuation_factor where date='2024-01-02' limit 3"),
    # 财务
    ("cn_stock_financial_indicator", "select * from cn_stock_financial_indicator where date='2024-01-02' limit 3"),
    ("cn_stock_balance_sheet", "select * from cn_stock_balance_sheet where date='2024-01-02' limit 3"),
    # 行情
    ("cn_stock_prefactored_bar1d", "select * from cn_stock_prefactored_bar1d where date='2024-01-02' limit 3"),
    # 涨跌停
    ("cn_stock_limit", "select * from cn_stock_limit where date='2024-01-02' limit 3"),
    # 行业
    ("cn_stock_industry", "select * from cn_stock_industry limit 3"),
    # 基本信息
    ("cn_stock_instruments", "select * from cn_stock_instruments limit 3"),
    ("instruments", "select * from instruments where market='CN' limit 3"),
]

for name, sql in test_tables:
    try:
        df = dai.query(sql).df()
        cols = list(df.columns)
        print(f"✓ {name}: {len(df)} rows, cols={cols[:8]}")
    except Exception as e:
        err = str(e).split('\n')[0][:80]
        print(f"✗ {name}: {err}")

print("\n=== 完成 ===")
