#!/usr/bin/env node
/**
 * RFScore PB10 数据异常快速验证
 * 简化版本，减少计算量
 */

import { runNotebookTest } from './request/test-joinquant-notebook.js';
import fs from 'fs';
import path from 'path';

const verificationScript = `
print("="*60)
print("RFScore PB10 数据异常快速验证")
print("="*60)

from jqdata import *
from jqfactor import Factor, calc_factors
from datetime import datetime
import pandas as pd
import numpy as np

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
        self.fscore = self.basic.apply(lambda x: np.where(x > 0, 1, 0)).sum(axis=1)

# 获取最近交易日
trade_day = get_trade_days(end_date=datetime.now().date(), count=1)[0]
trade_day_str = str(trade_day)

print(f"\\n验证日期: {trade_day_str}")

# 股票池：中证800
hs300 = set(get_index_stocks("000300.XSHG", date=trade_day))
zz500 = set(get_index_stocks("000905.XSHG", date=trade_day))
stocks = [s for s in (hs300 | zz500) if not s.startswith("688")]

# 基础过滤
sec = get_all_securities(types=["stock"], date=trade_day)
sec = sec.loc[sec.index.intersection(stocks)]
sec = sec[sec["start_date"] <= trade_day - pd.Timedelta(days=180)]
stocks = sec.index.tolist()

is_st = get_extras("is_st", stocks, end_date=trade_day, count=1).iloc[-1]
stocks = is_st[is_st == False].index.tolist()

paused = get_price(stocks, end_date=trade_day_str, count=1, fields="paused", panel=False)
paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
stocks = paused[paused == 0].index.tolist()

print(f"股票池数量: {len(stocks)}")

# 计算RFScore
factor = RFScore()
calc_factors(stocks, [factor], start_date=trade_day_str, end_date=trade_day_str)
df = factor.basic.copy()
df["RFScore"] = factor.fscore

# 获取估值数据
val = get_valuation(stocks, end_date=trade_day_str, 
                    fields=["pb_ratio", "pe_ratio", "circulating_market_cap"], count=1)
val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio", "circulating_market_cap"]]
df = df.join(val, how="left")

# 获取成交额（简化：只取最近5日平均）
price_data = get_price(stocks, end_date=trade_day_str, count=5, fields=["money"], panel=False)
daily_money = price_data.pivot(index="time", columns="code", values="money")
avg_amount = daily_money.mean()
df["avg_amount_5d"] = avg_amount
df["avg_amount_5d_yi"] = avg_amount / 1e8  # 转换为亿

# 清洗数据
df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["RFScore", "pb_ratio"])

# PB分位
df["pb_group"] = pd.qcut(df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop") + 1

# 获取名称
name_map = get_all_securities(types=["stock"], date=trade_day).loc[df.index, "display_name"].to_dict()
df["name"] = df.index.map(name_map)

# PB10%候选股
pb10_candidates = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)].copy()

print("\\n" + "="*60)
print("【验证结果】")
print("="*60)

print(f"\\n1. 候选股数量: {len(pb10_candidates)} 只")
if len(pb10_candidates) > 0:
    amounts = pb10_candidates["avg_amount_5d_yi"].dropna()
    caps = pb10_candidates["circulating_market_cap"].dropna()
    
    print(f"\\n2. 成交额统计（亿元）:")
    print(f"   最小值: {amounts.min():.2f}")
    print(f"   最大值: {amounts.max():.2f}")
    print(f"   平均值: {amounts.mean():.2f}")
    print(f"   中位数: {amounts.median():.2f}")
    
    print(f"\\n3. 流通市值统计（亿元）:")
    print(f"   最小值: {caps.min():.2f}")
    print(f"   最大值: {caps.max():.2f}")
    print(f"   平均值: {caps.mean():.2f}")
    print(f"   中位数: {caps.median():.2f}")
    
    # PE异常
    high_pe = pb10_candidates[pb10_candidates["pe_ratio"] > 100]
    print(f"\\n4. PE > 100 的候选股: {len(high_pe)} 只")
    if len(high_pe) > 0:
        for idx, row in high_pe.head(3).iterrows():
            print(f"   {row['name']}: PE={row['pe_ratio']:.2f}")
    
    # 低流动性
    low_amount = pb10_candidates[pb10_candidates["avg_amount_5d_yi"] < 0.5]  # 5000万
    print(f"\\n5. 成交额 < 5000万: {len(low_amount)} 只")
    if len(low_amount) > 0:
        for idx, row in low_amount.head(3).iterrows():
            print(f"   {row['name']}: 成交额={row['avg_amount_5d_yi']:.4f}亿")
    
    # 显示前10只候选股
    print(f"\\n6. 前10只候选股:")
    pb10_sorted = pb10_candidates.sort_values(["ROA", "OCFOA"], ascending=False)
    for idx, row in pb10_sorted.head(10).iterrows():
        print(f"   {row['name'][:8]:8} PB={row['pb_ratio']:.2f} PE={row['pe_ratio']:.2f} 市值={row['circulating_market_cap']:.0f}亿 成交={row['avg_amount_5d_yi']:.2f}亿")

print("\\n" + "="*60)
print("验证完成")
print("="*60)
`;

async function main() {
    const NOTEBOOK_URL = 'https://www.joinquant.com/research?target=research&url=/user/21333940833/notebooks/test.ipynb';
    
    console.log('开始快速验证RFScore PB10数据异常...');
    console.log('=' .repeat(60));
    
    try {
        const result = await runNotebookTest({
            notebookUrl: NOTEBOOK_URL,
            cellSource: verificationScript,
            timeoutMs: 300000,  // 5分钟
            appendCell: true
        });
        
        console.log('\\n验证完成！');
        
        // 输出结果
        if (result.executions && result.executions.length > 0) {
            const lastExecution = result.executions[result.executions.length - 1];
            if (lastExecution.textOutput) {
                console.log('\\n' + lastExecution.textOutput);
            }
        }
        
        return result;
    } catch (error) {
        console.error('验证失败:', error.message);
        throw error;
    }
}

main();
