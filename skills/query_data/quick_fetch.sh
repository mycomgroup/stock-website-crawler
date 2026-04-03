#!/bin/bash
# 快速查询脚本 - 用于快速获取股票数据
# 使用方法: ./quick_fetch.sh <market> <code>

MARKET=${1:-HK}
CODE=${2:-09992}

echo "=========================================="
echo "快速数据查询 - $MARKET:$CODE"
echo "=========================================="

if [ "$MARKET" = "HK" ]; then
    echo ""
    echo "📊 正在获取港股财务数据 ($CODE)..."
    python3 << 'PYEOF'
import akshare as ak
import warnings
warnings.filterwarnings('ignore')

stock_code = '$CODE'
year_str = '2024-12-31 00:00:00'

try:
    print("1️⃣ 现金流量表数据:")
    cf = ak.stock_financial_hk_report_em(stock=stock_code, symbol='现金流量表')
    ocf = cf[(cf['REPORT_DATE'] == year_str) & (cf['STD_ITEM_NAME'] == '经营业务现金净额')]['AMOUNT']
    if len(ocf) > 0:
        print(f"   ✅ 经营现金流: {float(ocf.values[0])/1e8:.2f}亿人民币")
    else:
        print("   ❌ 经营现金流: 无数据")
    
    print("\\n2️⃣ 资产负债表数据:")
    bs = ak.stock_financial_hk_report_em(stock=stock_code, symbol='资产负债表')
    
    cash = bs[(bs['REPORT_DATE'] == year_str) & (bs['STD_ITEM_NAME'] == '现金及等价物')]['AMOUNT']
    if len(cash) > 0:
        print(f"   ✅ 现金及等价物: {float(cash.values[0])/1e8:.2f}亿人民币")
    
    inventory = bs[(bs['REPORT_DATE'] == year_str) & (bs['STD_ITEM_NAME'] == '存货')]['AMOUNT']
    if len(inventory) > 0:
        print(f"   ✅ 存货: {float(inventory.values[0])/1e8:.2f}亿人民币")
    
    total_assets = bs[(bs['REPORT_DATE'] == year_str) & (bs['STD_ITEM_NAME'] == '总资产')]['AMOUNT']
    if len(total_assets) > 0:
        print(f"   ✅ 总资产: {float(total_assets.values[0])/1e8:.2f}亿人民币")
    
    print("\\n3️⃣ 最新股价:")
    df = ak.stock_hk_hist(symbol=stock_code, period='daily', start_date='20250320', end_date='20260326', adjust='qfq')
    if not df.empty:
        latest = df.iloc[-1]
        close_price = latest['收盘']
        change_pct = latest['涨跌幅']
        print(f"   📈 最新股价: HK${close_price:.2f}")
        print(f"   📊 涨跌幅: {change_pct:.2f}%")
    
    print("\\n✅ 数据获取完成")
    
except Exception as e:
    print(f"\\n❌ 错误: {e}")
PYEOF

elif [ "$MARKET" = "US" ]; then
    echo ""
    echo "📊 正在获取美股财务数据 ($CODE)..."
    python3 << 'PYEOF'
import requests
import os

api_key = os.getenv('FINNHUB_API_KEY', 'd1iu8mhr01qhbuvsappgd1iu8mhr01qhbuvsapq0')
symbol = '$CODE'

url = f'https://finnhub.io/api/v1/stock/financials-reported?symbol={symbol}&token={api_key}&freq=annual'
resp = requests.get(url, timeout=30)

if resp.status_code == 200:
    data = resp.json()
    if 'data' in data and len(data['data']) > 0:
        latest = data['data'][0]
        year = latest.get('year', 'N/A')
        print(f'✅ 最新财年: {year}')
        
        if 'report' in latest and 'ic' in latest['report']:
            print('\\n📊 利润表关键数据:')
            for item in latest['report']['ic'][:8]:
                label = item.get('label', '')
                value = item.get('value')
                if value and isinstance(value, (int, float)) and abs(value) > 1e6:
                    print(f'   {label}: ${value/1e9:.2f}B')
    else:
        print('❌ 无财务数据')
else:
    print(f'❌ API错误: {resp.status_code}')
PYEOF

else
    echo "❌ 不支持的市场类型: $MARKET"
    echo "支持的市场: HK (港股), US (美股)"
    exit 1
fi

echo ""
echo "=========================================="
echo "查询完成"
echo "=========================================="
