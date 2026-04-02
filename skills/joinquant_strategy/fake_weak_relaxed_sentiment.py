>from jqdata import *
import datetime as dt

def initialize(context):
    set_option('use_real_price', True)
    set_option('avoid_future_data', True)
    log.set_level('system', 'error')
    
    g.trades = 0
    g.wins = 0
    g.blocked = 0
    
    run_daily(check_sentiment, '9:00')
    run_daily(buy_stocks, '09:35')
    run_daily(sell_stocks, '14:50')

def check_sentiment(context):
    """放宽条件: 涨停≥20 或 跌停≤15 或 最高连板≥2"""
    g.allow = True
    prev = context.previous_date.strftime('%Y-%m-%d')
    
    all_stocks = get_all_securities('stock', prev).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in '483' and s[:2] != '68']
    
    try:
        df = get_price(all_stocks, end_date=prev, frequency='daily',
                       fields=['close', 'high_limit', 'low_limit'], count=1, panel=False)
        df = df.dropna()
        up = len(df[df['close'] == df['high_limit']])
        down = len(df[df['close'] == df['low_limit']])
        
        # 放宽条件
        if up < 20 or down > 15:
            g.allow = False
            g.blocked += 1
    except:
        pass

def buy_stocks(context):
    if not g.allow:
        return
    
    prev = context.previous_date.strftime('%Y-%m-%d')
    all_stocks = get_all_securities('stock', prev).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in '483' and s[:2] != '68']
    all_stocks = [s for s in all_stocks if (context.previous_date - get_security_info(s).start_date).days > 250]
    
    try:
        st_df = get_extras('is_st', all_stocks, start_date=prev, end_date=prev, df=True).T
        st_df.columns = ['is_st']
        all_stocks = list(st_df[st_df['is_st'] == False].index)
    except:
        pass
    
    df = get_price(all_stocks, end_date=prev, frequency='daily',
                   fields=['close', 'high_limit'], count=1, panel=False)
    df = df.dropna()
    df = df[df['close'] == df['high_limit']]
    hl = list(df['code'])
    
    if not hl:
        return
    
    cd = get_current_data()
    selected = []
    
    for s in hl:
        if s not in cd or cd[s].paused:
            continue
        pre = cd[s].pre_close
        open_p = cd[s].day_open
        if pre <= 0:
            continue
        limit_p = pre * 1.1
        open_pct = (open_p / limit_p - 1) * 100
        
        if 0.5 <= open_pct <= 1.5:
            try:
                val = get_valuation(s, end_date=context.previous_date, count=1)
                if val is not None and len(val) > 0:
                    cap = val['circulating_market_cap'].iloc[0]
                    if 30 <= cap <= 200:
                        selected.append(s)
            except:
                pass
    
    if selected:
        cash = context.portfolio.available_cash / min(len(selected), 3)
        for s in selected[:3]:
            order_value(s, cash)
            g.trades += 1

def sell_stocks(context):
    cd = get_current_data()
    for s in list(context.portfolio.positions):
        pos = context.portfolio.positions[s]
        if pos.closeable_amount > 0:
            if s in cd:
                pnl = (cd[s].last_price - pos.avg_cost) / pos.avg_cost * 100
                if pnl > 0:
                    g.wins += 1
            order_target(s, 0)