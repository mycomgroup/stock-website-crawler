"""
BigQuant 数据 API 探测
测试各类数据接口是否可用
"""
import traceback

results = {}

def test(name, fn):
    try:
        r = fn()
        results[name] = ('OK', str(r)[:200] if r is not None else 'None')
        print(f"✓ {name}: {str(r)[:100]}")
    except Exception as e:
        results[name] = ('FAIL', str(e)[:100])
        print(f"✗ {name}: {e}")

print("=== BigQuant 数据 API 探测 ===\n")

# 1. DAI (Data Access Interface) - BigQuant 核心数据接口
print("--- DAI API ---")
try:
    import dai
    test("dai.query stocks", lambda: dai.query("select date, instrument, open, high, low, close, volume from cn_stock_bar1d where date='2024-01-02' limit 5").df())
    test("dai.query fundamentals", lambda: dai.query("select date, instrument, pe_ttm, pb from cn_stock_valuation where date='2024-01-02' limit 5").df())
    test("dai.query index", lambda: dai.query("select date, instrument, close from cn_index_bar1d where instrument='000300.SH' and date>='2024-01-01' limit 5").df())
except ImportError as e:
    print(f"✗ dai 模块不可用: {e}")

# 2. BigQuant 内置 API
print("\n--- BigQuant 内置 API ---")
try:
    import bigquant
    print(f"✓ bigquant 版本: {bigquant.__version__ if hasattr(bigquant, '__version__') else 'unknown'}")
    test("bigquant.get_instruments", lambda: bigquant.get_instruments(market='CN', type='stock', date='2024-01-02')[:3] if hasattr(bigquant, 'get_instruments') else 'N/A')
except ImportError as e:
    print(f"✗ bigquant 模块: {e}")

# 3. 尝试 bq 模块
print("\n--- bq 模块 ---")
try:
    import bq
    print(f"✓ bq 可用")
    test("bq.get_price", lambda: bq.get_price('000001.SZA', start_date='2024-01-01', end_date='2024-01-05') if hasattr(bq, 'get_price') else 'N/A')
except ImportError as e:
    print(f"✗ bq 模块: {e}")

# 4. 尝试 pandas_datareader 或其他
print("\n--- 其他数据模块 ---")
for mod in ['akshare', 'tushare', 'yfinance', 'pandas_datareader']:
    try:
        m = __import__(mod)
        print(f"✓ {mod} 可用: {getattr(m, '__version__', 'unknown')}")
    except ImportError:
        print(f"✗ {mod} 不可用")

# 5. 列出所有可用模块
print("\n--- 已安装的量化相关包 ---")
import pkg_resources
quant_pkgs = [p for p in pkg_resources.working_set if any(k in p.project_name.lower() for k in ['quant', 'finance', 'stock', 'bigquant', 'dai', 'bq', 'akshare', 'tushare', 'rqalpha', 'zipline'])]
for p in quant_pkgs:
    print(f"  {p.project_name} {p.version}")

print("\n=== 探测完成 ===")
