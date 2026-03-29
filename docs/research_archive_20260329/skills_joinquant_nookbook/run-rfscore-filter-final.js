#!/usr/bin/env node
/**
 * RFScore 过滤器终审回测脚本
 * 使用 joinquant_nookbook 计算信号和回测
 */

import { runNotebookTest } from './request/test-joinquant-notebook.js';
import fs from 'fs';
import path from 'path';

const cellSource = `
from jqdata import *
from jqfactor import Factor, calc_factors
import pandas as pd
import numpy as np
import json

# 配置参数
START_DATE = "2022-01-01"
END_DATE = "2025-12-31"
HOLD_NUM = 20
IPO_DAYS = 180

def sign(ser):
    return ser.apply(lambda x: np.where(x > 0, 1, 0))

class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = [
        "roa", "roa_4",
        "net_operate_cash_flow", "net_operate_cash_flow_1", "net_operate_cash_flow_2", "net_operate_cash_flow_3",
        "total_assets", "total_assets_1", "total_assets_2", "total_assets_3", "total_assets_4", "total_assets_5",
        "total_non_current_liability", "total_non_current_liability_1",
        "gross_profit_margin", "gross_profit_margin_4",
        "operating_revenue", "operating_revenue_4",
    ]

    def calc(self, data):
        roa = data["roa"]
        delta_roa = roa / data["roa_4"] - 1
        cfo_sum = (
            data["net_operate_cash_flow"] + data["net_operate_cash_flow_1"] +
            data["net_operate_cash_flow_2"] + data["net_operate_cash_flow_3"]
        )
        ta_ttm = (data["total_assets"] + data["total_assets_1"] + 
                  data["total_assets_2"] + data["total_assets_3"]) / 4
        ocfoa = cfo_sum / ta_ttm
        accrual = ocfoa - roa * 0.01
        leveler = data["total_non_current_liability"] / data["total_assets"]
        leveler1 = data["total_non_current_liability_1"] / data["total_assets_1"]
        delta_leveler = -(leveler / leveler1 - 1)
        delta_margin = data["gross_profit_margin"] / data["gross_profit_margin_4"] - 1
        turnover = data["operating_revenue"] / (data["total_assets"] + data["total_assets_1"]).mean()
        turnover_1 = data["operating_revenue_4"] / (data["total_assets_4"] + data["total_assets_5"]).mean()
        delta_turn = turnover / turnover_1 - 1
        
        indicator_tuple = (roa, delta_roa, ocfoa, accrual, delta_leveler, delta_margin, delta_turn)
        self.basic = pd.concat(indicator_tuple).T.replace([-np.inf, np.inf], np.nan)
        self.basic.columns = ["ROA", "DELTA_ROA", "OCFOA", "ACCRUAL", "DELTA_LEVELER", "DELTA_MARGIN", "DELTA_TURN"]
        self.fscore = self.basic.apply(sign).sum(axis=1)

def get_monthly_dates(start_date, end_date):
    trade_days = get_trade_days(start_date=start_date, end_date=end_date)
    dates = []
    current_month = None
    for day in trade_days:
        if day.month != current_month:
            dates.append(day)
            current_month = day.month
    return dates

def get_universe(date):
    hs300 = set(get_index_stocks("000300.XSHG", date=date))
    zz500 = set(get_index_stocks("000905.XSHG", date=date))
    stocks = [s for s in (hs300 | zz500) if not s.startswith("688")]
    
    sec = get_all_securities(types=["stock"], date=date)
    sec = sec.loc[sec.index.intersection(stocks)]
    sec = sec[sec["start_date"] <= date - pd.Timedelta(days=IPO_DAYS)]
    stocks = sec.index.tolist()
    
    is_st = get_extras("is_st", stocks, end_date=date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()
    
    paused = get_price(stocks, end_date=date, count=1, fields="paused", panel=False)
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()
    return stocks

def calc_turnover(stocks, date):
    """计算20日平均换手率"""
    df = get_price(stocks, end_date=date, count=20, fields=["volume", "money"], panel=False)
    if df.empty:
        return pd.Series(dtype=float)
    
    vol = df.pivot(index="time", columns="code", values="volume")
    val = df.pivot(index="time", columns="code", values="money")
    avg_money = val.mean()
    
    cap = get_valuation(stocks, end_date=date, fields=["circulating_market_cap"], count=1)
    cap = cap.drop_duplicates("code").set_index("code")["circulating_market_cap"]
    
    turnover = avg_money / (cap * 1e8 + 1)
    return turnover

def calc_cgo(stocks, date, lookback=260):
    """计算CGO (Capital Gains Overhang)"""
    prices = get_price(stocks, end_date=date, count=lookback, fields=["close"], panel=False)
    if prices.empty:
        return pd.Series(dtype=float)
    
    close = prices.pivot(index="time", columns="code", values="close")
    current_price = close.iloc[-1]
    avg_price = close.mean()
    cgo = (current_price - avg_price) / (current_price + 1e-10)
    return cgo

def fetch_industry_info(stocks, date):
    """获取股票所属行业"""
    industry = get_industry(stocks, date=date)
    result = {}
    for stock in stocks:
        if stock in industry and "sw_l1" in industry[stock]:
            result[stock] = industry[stock]["sw_l1"]["industry_name"]
        else:
            result[stock] = "Unknown"
    return pd.Series(result)

def calc_rfscore_frame(stocks, date):
    factor = RFScore()
    calc_factors(stocks, [factor], start_date=date, end_date=date)
    
    basic = factor.basic.copy()
    basic["RFScore"] = factor.fscore
    
    val = get_valuation(stocks, end_date=date, fields=["pb_ratio", "pe_ratio", "circulating_market_cap"], count=1)
    val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio", "circulating_market_cap"]]
    
    basic = basic.join(val, how="left")
    basic = basic.replace([np.inf, -np.inf], np.nan).dropna(subset=["RFScore", "pb_ratio"])
    basic["pb_group"] = pd.qcut(basic["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop") + 1
    
    basic = basic.sort_values(["RFScore", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN"],
                               ascending=[False, False, False, False, False])
    return basic

def choose_portfolio(frame, variant, extra_data=None):
    df = frame.copy()
    
    if variant == "rfscore_pb10":
        df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)]
    elif variant == "rfscore_pb10_turnover_filter":
        if extra_data is not None and "turnover" in extra_data:
            turnover = extra_data["turnover"]
            df = df.join(turnover.rename("turnover"), how="left")
            turnover_threshold = df["turnover"].quantile(0.8)
            df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1) & (df["turnover"] < turnover_threshold)]
        else:
            df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)]
    elif variant == "rfscore_pb10_cgo_filter":
        if extra_data is not None and "cgo" in extra_data:
            cgo = extra_data["cgo"]
            df = df.join(cgo.rename("cgo"), how="left")
            cgo_threshold = df["cgo"].quantile(0.8)
            df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1) & (df["cgo"] < cgo_threshold)]
        else:
            df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)]
    elif variant == "rfscore_pb10_combined_filter":
        if extra_data is not None and "turnover" in extra_data and "cgo" in extra_data:
            turnover = extra_data["turnover"]
            cgo = extra_data["cgo"]
            df = df.join(turnover.rename("turnover"), how="left").join(cgo.rename("cgo"), how="left")
            turnover_threshold = df["turnover"].quantile(0.8)
            cgo_threshold = df["cgo"].quantile(0.8)
            df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1) & 
                    (df["turnover"] < turnover_threshold) & (df["cgo"] < cgo_threshold)]
        else:
            df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)]
    elif variant == "rfscore_pb10_industry_cap":
        df = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)]
    else:
        raise ValueError("unknown variant")
    
    if df.empty:
        return []
    return df.index.tolist()[:HOLD_NUM]

def apply_industry_cap(stocks, industry_map, max_per_industry=5):
    """应用行业集中度上限"""
    if not stocks:
        return []
    
    industry_count = {}
    result = []
    for stock in stocks:
        ind = industry_map.get(stock, "Unknown")
        count = industry_count.get(ind, 0)
        if count < max_per_industry:
            result.append(stock)
            industry_count[ind] = count + 1
        if len(result) >= HOLD_NUM:
            break
    return result

def get_forward_return(stocks, start_date, end_date):
    if not stocks:
        return 0.0
    px0 = get_price(stocks, end_date=start_date, count=1, fields=["close"], panel=False)
    px1 = get_price(stocks, end_date=end_date, count=1, fields=["close"], panel=False)
    px0 = px0.pivot(index="time", columns="code", values="close").iloc[-1]
    px1 = px1.pivot(index="time", columns="code", values="close").iloc[-1]
    ret = (px1 / px0 - 1).dropna()
    if len(ret) == 0:
        return 0.0
    return float(ret.mean())

def calc_max_drawdown(nav_series):
    if len(nav_series) == 0:
        return 0.0
    nav = pd.Series(nav_series)
    cummax = nav.cummax()
    drawdown = (nav - cummax) / cummax
    return float(drawdown.min())

def calc_sharpe(returns, annual_factor=12):
    if len(returns) == 0:
        return 0.0
    ret = pd.Series(returns)
    if ret.std() == 0:
        return 0.0
    return float(ret.mean() / ret.std() * np.sqrt(annual_factor))

# 主测试流程
print("="*80)
print("RFScore PB10 过滤器终审回测")
print("="*80)
print(f"测试期间: {START_DATE} 至 {END_DATE}")
print(f"持仓数量: {HOLD_NUM}")
print()

variants = [
    "rfscore_pb10",
    "rfscore_pb10_turnover_filter",
    "rfscore_pb10_cgo_filter",
    "rfscore_pb10_combined_filter",
    "rfscore_pb10_industry_cap",
]

results = {name: [] for name in variants}
stock_counts = {name: [] for name in variants}

dates = get_monthly_dates(START_DATE, END_DATE)
print(f"月度调仓次数: {len(dates)-1}")
print()

for i in range(len(dates) - 1):
    if i % 12 == 0:
        print(f"进度: {i}/{len(dates) - 1} ({i / (len(dates) - 1) * 100:.1f}%)")
    
    date = pd.Timestamp(dates[i]).date()
    next_date = pd.Timestamp(dates[i + 1]).date()
    date_str = str(date)
    next_date_str = str(next_date)
    
    stocks = get_universe(date)
    frame = calc_rfscore_frame(stocks, date_str)
    
    # 计算过滤信号
    turnover = calc_turnover(stocks, date_str)
    cgo = calc_cgo(stocks, date_str)
    industry_map = fetch_industry_info(stocks, date_str)
    
    extra_data = {"turnover": turnover, "cgo": cgo, "industry": industry_map}
    
    rf7_pb10_count = len(frame[(frame["RFScore"] == 7) & (frame["pb_group"] == 1)])
    
    for variant in variants:
        selected = choose_portfolio(frame, variant, extra_data)
        
        if variant == "rfscore_pb10_industry_cap":
            selected = apply_industry_cap(selected, industry_map, max_per_industry=5)
        
        stock_counts[variant].append(len(selected))
        period_return = get_forward_return(selected, date_str, next_date_str)
        results[variant].append(period_return)

# 汇总结果
print()
print("="*80)
print("过滤器终审结果汇总")
print("="*80)

final_results = {}

for name in variants:
    ser = pd.Series(results[name])
    nav = (1 + ser).cumprod()
    cum = nav.iloc[-1] - 1
    ann = (1 + cum) ** (12 / len(ser)) - 1 if len(ser) else 0
    mdd = calc_max_drawdown(nav)
    sharpe = calc_sharpe(results[name])
    win_rate = (ser > 0).mean()
    avg_count = np.mean(stock_counts[name])
    
    final_results[name] = {
        "cumulative_return": float(cum),
        "annual_return": float(ann),
        "max_drawdown": float(mdd),
        "sharpe_ratio": float(sharpe),
        "win_rate": float(win_rate),
        "avg_stock_count": float(avg_count),
        "monthly_returns": [float(r) for r in results[name]]
    }
    
    print(f"\\n{name}:")
    print(f"  累计收益: {cum:.4f}")
    print(f"  年化收益: {ann:.4f}")
    print(f"  最大回撤: {mdd:.4f}")
    print(f"  夏普比率: {sharpe:.4f}")
    print(f"  月胜率: {win_rate:.4f}")
    print(f"  平均候选股数: {avg_count:.1f}")

# 对比表
print()
print("="*80)
print("过滤器对比表")
print("="*80)
print(f"{'过滤器':<35} {'年化':<10} {'回撤':<10} {'夏普':<10} {'胜率':<10} {'股数':<10}")
print("-"*85)

for name in variants:
    r = final_results[name]
    print(f"{name:<35} {r['annual_return']:.4f}    {r['max_drawdown']:.4f}    {r['sharpe_ratio']:.4f}    {r['win_rate']:.4f}    {r['avg_stock_count']:.1f}")

# 与基准对比
print()
print("="*80)
print("相对基准改善 (vs rfscore_pb10)")
print("="*80)

baseline = final_results["rfscore_pb10"]
for name in variants[1:]:
    r = final_results[name]
    ann_diff = r['annual_return'] - baseline['annual_return']
    mdd_diff = r['max_drawdown'] - baseline['max_drawdown']
    sharpe_diff = r['sharpe_ratio'] - baseline['sharpe_ratio']
    count_diff = r['avg_stock_count'] - baseline['avg_stock_count']
    
    print(f"\\n{name}:")
    print(f"  年化收益变化: {ann_diff:+.4f} ({ann_diff/baseline['annual_return']*100:+.1f}%)")
    print(f"  最大回撤变化: {mdd_diff:+.4f} ({'改善' if mdd_diff > 0 else '恶化'})")
    print(f"  夏普比率变化: {sharpe_diff:+.4f}")
    print(f"  候选股数变化: {count_diff:+.1f}")

# 保存结果
output_path = "/Users/fengzhi/Downloads/git/testlixingren/tmp/rfscore_filter_final_results.json"
with open(output_path, "w") as f:
    json.dump(final_results, f, indent=2)

print(f"\\n结果已保存到: {output_path}")
`;

async function main() {
    const resultFile = '/Users/fengzhi/Downloads/git/testlixingren/tmp/rfscore_filter_final_output.json';
    
    console.log('开始执行RFScore过滤器终审回测...');
    console.log('测试期间: 2022-01-01 至 2025-12-31');
    console.log('这大约需要 3-5 分钟...\n');
    
    try {
        const result = await runNotebookTest({
            cellSource: cellSource,
            timeoutMs: 600000,  // 10分钟超时
            appendCell: true
        });
        
        // 保存完整结果
        fs.mkdirSync(path.dirname(resultFile), { recursive: true });
        fs.writeFileSync(resultFile, JSON.stringify(result, null, 2));
        
        console.log('\n✓ 回测完成！');
        console.log('完整结果已保存到:', resultFile);
        
        // 输出stdout
        if (result.executions && result.executions.length > 0) {
            const lastExecution = result.executions[result.executions.length - 1];
            if (lastExecution.textOutput) {
                console.log('\n=== 回测输出 ===');
                console.log(lastExecution.textOutput);
            }
        }
        
        return result;
    } catch (error) {
        console.error('回测失败:', error);
        throw error;
    }
}

main();
