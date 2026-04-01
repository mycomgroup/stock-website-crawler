#!/usr/bin/env node
/**
 * RFScore PB10 数据异常验证脚本
 * 验证5项数据异常：成交额、市值、候选股数量、PE异常、低流动性
 */

import { runNotebookTest } from './request/test-joinquant-notebook.js';
import fs from 'fs';
import path from 'path';

const verificationScript = `
print("="*80)
print("RFScore PB10 数据异常验证")
print("="*80)

from jqdata import *
from jqfactor import Factor, calc_factors
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# RFScore Factor 定义
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
print("="*80)

# 股票池：中证800（沪深300 + 中证500）
hs300 = set(get_index_stocks("000300.XSHG", date=trade_day))
zz500 = set(get_index_stocks("000905.XSHG", date=trade_day))
stocks = [s for s in (hs300 | zz500) if not s.startswith("688")]

print(f"\\n中证800成分股总数: {len(hs300) + len(zz500)}")
print(f"剔除科创板后: {len(stocks)}")

# 基础过滤：IPO天数、ST、停牌
sec = get_all_securities(types=["stock"], date=trade_day)
sec = sec.loc[sec.index.intersection(stocks)]
sec = sec[sec["start_date"] <= trade_day - pd.Timedelta(days=180)]
stocks = sec.index.tolist()

is_st = get_extras("is_st", stocks, end_date=trade_day, count=1).iloc[-1]
stocks = is_st[is_st == False].index.tolist()

paused = get_price(stocks, end_date=trade_day_str, count=1, fields="paused", panel=False)
paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
stocks = paused[paused == 0].index.tolist()

print(f"经过IPO/ST/停牌过滤后: {len(stocks)}")

# 计算RFScore
factor = RFScore()
calc_factors(stocks, [factor], start_date=trade_day_str, end_date=trade_day_str)
df = factor.basic.copy()
df["RFScore"] = factor.fscore

# 获取估值和市值数据
val = get_valuation(stocks, end_date=trade_day_str, 
                    fields=["pb_ratio", "pe_ratio", "circulating_market_cap", "market_cap"], count=1)
val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio", "circulating_market_cap", "market_cap"]]
df = df.join(val, how="left")

# 获取成交额数据（过去20日平均）
print("\\n正在获取20日成交额数据...")
price_data = get_price(stocks, end_date=trade_day_str, count=20, fields=["volume", "money"], panel=False)
daily_money = price_data.pivot(index="time", columns="code", values="money")
avg_amount = daily_money.mean()
df["avg_amount_20d"] = avg_amount
df["avg_amount_20d_wan"] = avg_amount / 10000  # 转换为万元

# 清洗数据
df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["RFScore", "pb_ratio"])

# PB分位（10组）
df["pb_group"] = pd.qcut(df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop") + 1

# 获取股票名称和行业
name_map = get_all_securities(types=["stock"], date=trade_day).loc[df.index, "display_name"].to_dict()
df["name"] = df.index.map(name_map)

industry_map = {}
for code in df.index:
    info = get_industry(code, date=trade_day)
    industry_map[code] = info.get(code, {}).get("sw_l1", {}).get("industry_name", "Unknown")
df["industry"] = df.index.map(industry_map)

print("\\n" + "="*80)
print("异常1：成交额统计口径验证")
print("="*80)

# PB10%候选股
pb10_candidates = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)].copy()
pb10_candidates = pb10_candidates.sort_values(["ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
                                               ascending=[False, False, False, False, True])

print(f"\\nPB10%候选股数量: {len(pb10_candidates)}")

if len(pb10_candidates) > 0:
    # 成交额统计
    amounts = pb10_candidates["avg_amount_20d"].dropna()
    print(f"\\n20日平均成交额统计（万元）:")
    print(f"  最小值: {amounts.min()/10000:.2f}万")
    print(f"  最大值: {amounts.max()/10000:.2f}万")
    print(f"  平均值: {amounts.mean()/10000:.2f}万")
    print(f"  中位数: {amounts.median()/10000:.2f}万")
    print(f"\\n  分位分布:")
    for q in [0.1, 0.25, 0.5, 0.75, 0.9]:
        print(f"    {int(q*100)}%分位: {amounts.quantile(q)/10000:.2f}万")
    
    # 与压力测试数据对比
    print(f"\\n⚠️  异常验证:")
    print(f"  压力测试声称范围: 1.5亿 - 24.0亿（15000万 - 240000万）")
    print(f"  实际最小值: {amounts.min()/10000:.2f}万")
    print(f"  实际最大值: {amounts.max()/10000:.2f}万")
    if amounts.min() < 15000:
        print(f"  ❌ 异常：存在成交额低于1.5亿的股票")
    if amounts.max() > 240000:
        print(f"  ❌ 异常：存在成交额超过24亿的股票")

print("\\n" + "="*80)
print("异常2：市值范围验证")
print("="*80)

if len(pb10_candidates) > 0:
    market_caps = pb10_candidates["circulating_market_cap"].dropna()
    print(f"\\n流通市值统计（亿元）:")
    print(f"  最小值: {market_caps.min():.2f}亿")
    print(f"  最大值: {market_caps.max():.2f}亿")
    print(f"  平均值: {market_caps.mean():.2f}亿")
    print(f"  中位数: {market_caps.median():.2f}亿")
    
    print(f"\\n⚠️  异常验证:")
    print(f"  压力测试声称范围: 143亿 - 9946亿")
    print(f"  实际最大值: {market_caps.max():.2f}亿")
    if market_caps.max() > 5000:
        print(f"  ⚠️  警示：存在超大市值股票，需确认是否为中证800成分股")
        # 显示超大市值股票
        large_cap = pb10_candidates[pb10_candidates["circulating_market_cap"] > 3000]
        if len(large_cap) > 0:
            print(f"\\n  超大市值股票（>3000亿）:")
            print(large_cap[["name", "industry", "circulating_market_cap"]].to_string())

print("\\n" + "="*80)
print("异常3：候选股数量波动验证")
print("="*80)

print(f"\\n当前RFScore=7的股票总数: {len(df[df['RFScore'] == 7])}")
print(f"当前PB10%（group=1）的股票数: {len(df[df['pb_group'] == 1])}")
print(f"当前PB10% & RFScore=7的候选股: {len(pb10_candidates)}")

print(f"\\n⚠️  异常验证:")
print(f"  历史声称范围: 10-50只")
print(f"  当前实际数量: {len(pb10_candidates)}只")
if len(pb10_candidates) < 10:
    print(f"  ❌ 异常：候选股数量过少（<10），可能触发备用池")
elif len(pb10_candidates) > 40:
    print(f"  ⚠️  警示：候选股数量较多（>40），可能存在质量分化")

# 显示候选股列表
if len(pb10_candidates) > 0:
    print(f"\\n当前候选股列表:")
    display_cols = ["name", "industry", "pb_ratio", "pe_ratio", "circulating_market_cap", "avg_amount_20d_wan"]
    print(pb10_candidates[display_cols].head(30).round(2).to_string())

print("\\n" + "="*80)
print("异常4：PE异常高验证")
print("="*80)

high_pe = pb10_candidates[pb10_candidates["pe_ratio"] > 100]
print(f"\\nPE > 100的候选股数量: {len(high_pe)}")

if len(high_pe) > 0:
    print(f"❌ 发现PE异常高的候选股:")
    print(high_pe[["name", "industry", "pb_ratio", "pe_ratio", "ROA"]].round(2).to_string())
else:
    print(f"✅ 未发现PE > 100的候选股")

# PE分布
pe_values = pb10_candidates["pe_ratio"].dropna()
pe_values = pe_values[pe_values > 0]  # 剔除负值
print(f"\\nPE分布统计:")
print(f"  最小值: {pe_values.min():.2f}")
print(f"  最大值: {pe_values.max():.2f}")
print(f"  平均值: {pe_values.mean():.2f}")
print(f"  中位数: {pe_values.median():.2f}")

print("\\n" + "="*80)
print("异常5：低流动性验证（成交额<5000万）")
print("="*80)

low_amount = pb10_candidates[pb10_candidates["avg_amount_20d"] < 50000000]  # 5000万
print(f"\\n成交额 < 5000万的候选股数量: {len(low_amount)}")

if len(low_amount) > 0:
    print(f"❌ 发现低流动性候选股:")
    print(low_amount[["name", "industry", "pb_ratio", "avg_amount_20d_wan"]].round(2).to_string())
else:
    print(f"✅ 未发现成交额 < 5000万的候选股")

# 成交额分布
amount_values = pb10_candidates["avg_amount_20d"].dropna()
print(f"\\n成交额分布统计（万元）:")
print(f"  < 5000万的股票: {len(amount_values[amount_values < 50000000])}")
print(f"  5000万-1亿: {len(amount_values[(amount_values >= 50000000) & (amount_values < 100000000)])}")
print(f"  1亿-5亿: {len(amount_values[(amount_values >= 100000000) & (amount_values < 500000000)])}")
print(f"  > 5亿: {len(amount_values[amount_values >= 500000000])}")

print("\\n" + "="*80)
print("验证总结")
print("="*80)

print(f"\\n候选股总数: {len(pb10_candidates)}")
print(f"数据质量检查:")
print(f"  - PE > 100: {len(high_pe)}只")
print(f"  - 成交额 < 5000万: {len(low_amount)}只")
print(f"  - 超大市值(>3000亿): {len(pb10_candidates[pb10_candidates['circulating_market_cap'] > 3000])}只")

if len(high_pe) > 0 or len(low_amount) > 0:
    print(f"\\n⚠️  建议增加的硬过滤条件:")
    print(f"  1. PE_ratio < 100")
    print(f"  2. avg_amount_20d > 50000000 (5000万)")
    print(f"  3. ROA > 0.5%")

print("\\n" + "="*80)
print("验证完成")
print("="*80)
`;

async function main() {
    const outputDir = '/Users/fengzhi/Downloads/git/testlixingren/output';
    const resultFile = path.join(outputDir, 'rfscore_verification_result.json');
    
    const NOTEBOOK_URL = 'https://www.joinquant.com/research?target=research&url=/user/21333940833/notebooks/test.ipynb';
    
    console.log('开始验证RFScore PB10数据异常...');
    console.log('=' .repeat(80));
    
    try {
        const result = await runNotebookTest({
            notebookUrl: NOTEBOOK_URL,
            cellSource: verificationScript,
            timeoutMs: 600000,  // 10分钟超时
            appendCell: true
        });
        
        fs.mkdirSync(outputDir, { recursive: true });
        fs.writeFileSync(resultFile, JSON.stringify(result, null, 2));
        
        console.log('\\n验证完成！');
        console.log('结果已保存到:', resultFile);
        
        // 输出执行结果
        if (result.executions && result.executions.length > 0) {
            const lastExecution = result.executions[result.executions.length - 1];
            if (lastExecution.textOutput) {
                console.log('\\n' + '='.repeat(80));
                console.log('验证输出结果');
                console.log('='.repeat(80));
                console.log(lastExecution.textOutput);
            }
            
            if (lastExecution.outputs && lastExecution.outputs.length > 0) {
                const errorOutput = lastExecution.outputs.find(o => o.output_type === 'error');
                if (errorOutput) {
                    console.log('\\n' + '='.repeat(80));
                    console.log('执行错误');
                    console.log('='.repeat(80));
                    console.log(JSON.stringify(errorOutput, null, 2));
                }
            }
        }
        
        return result;
    } catch (error) {
        console.error('验证失败:', error);
        throw error;
    }
}

main();
