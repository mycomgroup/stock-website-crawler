from jqdata import *
import pandas as pd

print("=" * 60)
print("PB10 策略验证 - 最简版")
print("=" * 60)

test_date = "2024-06-01"
print(f"\n测试日期: {test_date}")

try:
    print("获取沪深300成分股...")
    hs300 = get_index_stocks("000300.XSHG", date=test_date)
    print(f"股票数: {len(hs300)}")
    
    print("\n获取估值数据...")
    val = get_valuation(hs300, end_date=test_date, fields=["pb_ratio", "pe_ratio", "market_cap"], count=1)
    val = val.drop_duplicates("code").set_index("code")
    print(f"有效数据: {len(val)}")
    
    print("\n筛选条件:")
    print("  - PB > 0")
    print("  - PE > 0")
    print("  - PE < 100")
    
    df = val[(val["pb_ratio"] > 0) & (val["pe_ratio"] > 0) & (val["pe_ratio"] < 100)].copy()
    print(f"筛选后: {len(df)}只")
    
    print("\n按PB分组...")
    df['pb_group'] = pd.qcut(df['pb_ratio"].rank(method='first'), 10, labels=False, duplicates='drop') + 1
    
    low_pb = df[df['pb_group'] == 1].sort_values('market_cap', ascending=False)
    
    print(f"\nPB最低10%的股票 ({len(low_pb)}只):")
    print("前15只:")
    for i, (code, row) in enumerate(low_pb.head(15).iterrows()):
        name = get_security_info(code).display_name
        print(f"  {i+1:2d}. {code} {name[:10]:10s} PB={row['pb_ratio']:.2f} PE={row['pe_ratio']:.2f} 市值={row['market_cap']/1e8:.0f}亿")
    
    print("\n行业分布:")
    industries = {}
    for code in low_pb.head(15).index:
        ind = get_industry(code, date=test_date).get(code, {}).get('sw_l1', {}).get('industry_name', 'Unknown')
        industries[ind] = industries.get(ind, 0) + 1
    
    for ind, count in sorted(industries.items(), key=lambda x: -x[1]):
        print(f"  {ind}: {count}只 ({count/15:.1%})")
    
    print(f"\n最大行业比例: {max(industries.values())/15:.1%}")
    
    print("\n验证成功！低PB策略选出股票。")
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)