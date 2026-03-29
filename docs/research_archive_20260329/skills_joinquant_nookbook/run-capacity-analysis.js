#!/usr/bin/env node
/**
 * RFScore PB10 容量与执行仿真分析
 * 获取真实成交额、候选分布，并进行容量上限计算
 */

import { runNotebookTest } from './request/test-joinquant-notebook.js';
import fs from 'fs';
import path from 'path';

const cellSource = `
from jqdata import *
from jqfactor import Factor, calc_factors
from datetime import datetime
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

# 获取当前交易日
trade_day = get_trade_days(end_date=datetime.now().date(), count=1)[0]
trade_day_str = str(trade_day)

print(f"trade_day: {trade_day_str}")
print("="*80)

# 股票池：中证800（沪深300 + 中证500）
hs300 = set(get_index_stocks("000300.XSHG", date=trade_day))
zz500 = set(get_index_stocks("000905.XSHG", date=trade_day))
stocks = [s for s in (hs300 | zz500) if not s.startswith("688")]

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

print(f"universe_count: {len(stocks)}")

# 计算RFScore
factor = RFScore()
calc_factors(stocks, [factor], start_date=trade_day_str, end_date=trade_day_str)
df = factor.basic.copy()
df["RFScore"] = factor.fscore

# 获取估值数据
val = get_valuation(stocks, end_date=trade_day_str, fields=["pb_ratio", "pe_ratio", "circulating_market_cap"], count=1)
val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio", "circulating_market_cap"]]
df = df.join(val, how="left")

# 获取成交额数据（过去20日平均）
price_data = get_price(stocks, end_date=trade_day_str, count=20, fields=["volume", "money"], panel=False)
daily_money = price_data.pivot(index="time", columns="code", values="money")
avg_amount = daily_money.mean()
df["avg_amount_20d"] = avg_amount

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
print("PB10% 候选股（RFScore=7 & pb_group=1）")
print("="*80)
pb10_candidates = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)].copy()
pb10_candidates = pb10_candidates.sort_values(["ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
                                               ascending=[False, False, False, False, True])
print(f"count: {len(pb10_candidates)}")

if len(pb10_candidates) > 0:
    display_cols = ["name", "industry", "RFScore", "pb_ratio", "pe_ratio", "avg_amount_20d", "circulating_market_cap", "ROA"]
    print(pb10_candidates[display_cols].head(30).round(4).to_string())
    
    # 容量分析
    print("\\n" + "="*80)
    print("容量分析（PB10% 候选股）")
    print("="*80)
    print(f"候选股数量: {len(pb10_candidates)}")
    print(f"平均20日成交额: {pb10_candidates['avg_amount_20d'].mean()/1e8:.2f}亿")
    print(f"最小20日成交额: {pb10_candidates['avg_amount_20d'].min()/1e8:.2f}亿")
    print(f"最大20日成交额: {pb10_candidates['avg_amount_20d'].max()/1e8:.2f}亿")
    print(f"中位数20日成交额: {pb10_candidates['avg_amount_20d'].median()/1e8:.2f}亿")
    print(f"平均流通市值: {pb10_candidates['circulating_market_cap'].mean():.2f}亿")
    print(f"总流通市值: {pb10_candidates['circulating_market_cap'].sum():.2f}亿")
    
    # 行业分布
    print("\\n行业分布:")
    print(pb10_candidates["industry"].value_counts().head(10).to_string())
    
    # 成交额分位
    print("\\n成交额分布:")
    amount_quantiles = pb10_candidates["avg_amount_20d"].quantile([0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0])
    for q, v in amount_quantiles.items():
        print(f"  {int(q*100)}%分位: {v/1e8:.2f}亿")

# 不同持仓数量的容量上限计算
print("\\n" + "="*80)
print("仓位容量上限估算")
print("="*80)

# 假设冲击成本限制：单日成交量不超过5%
impact_limit = 0.05

for hold_num in [10, 15, 20, 25, 30]:
    if len(pb10_candidates) >= hold_num:
        top_n = pb10_candidates.head(hold_num)
        
        # 等权配置下，每只股票的目标仓位
        # 假设总资金为X，每只股票X/hold_num
        # 限制条件: X/hold_num <= avg_amount * impact_limit
        # 所以 X <= avg_amount * impact_limit * hold_num
        
        min_amount = top_n["avg_amount_20d"].min()
        max_capacity = min_amount * impact_limit * hold_num / 1e8  # 转换为亿
        avg_capacity = top_n["avg_amount_20d"].mean() * impact_limit * hold_num / 1e8
        
        print(f"\\n持仓{hold_num}只:")
        print(f"  按最小成交额计算最大容量: {max_capacity:.2f}亿")
        print(f"  按平均成交额计算最大容量: {avg_capacity:.2f}亿")
        print(f"  单票最小成交额: {min_amount/1e8:.2f}亿")
        
        # 建议仓位上限（保守估计：取平均容量的50%）
        suggested_capacity = avg_capacity * 0.5
        print(f"  建议仓位上限(保守): {suggested_capacity:.2f}亿")

# 异常值检测
print("\\n" + "="*80)
print("异常值审计")
print("="*80)

# PE异常高
pe_threshold = 100
high_pe = df[(df["RFScore"] == 7) & (df["pb_group"] == 1) & (df["pe_ratio"] > pe_threshold)]
if len(high_pe) > 0:
    print(f"\\n[PE > {pe_threshold}] 异常高PE股票({len(high_pe)}只):")
    print(high_pe[["name", "industry", "pb_ratio", "pe_ratio", "ROA"]].round(4).to_string())

# ROE异常低（ROA * 4 估算 ROE）
roe_proxy = df["ROA"] * 4  # 近似ROE
low_roe = df[(df["RFScore"] == 7) & (df["pb_group"] == 1) & (roe_proxy < 2)]
if len(low_roe) > 0:
    print(f"\\n[ROE < 2%] 低盈利能力股票({len(low_roe)}只):")
    print(low_roe[["name", "industry", "pb_ratio", "pe_ratio", "ROA"]].round(4).to_string())

# PB异常低（可能存在基本面问题）
low_pb = df[(df["RFScore"] == 7) & (df["pb_ratio"] < 0.4)]
if len(low_pb) > 0:
    print(f"\\n[PB < 0.4] 超低PB股票({len(low_pb)}只，可能基本面问题):")
    print(low_pb[["name", "industry", "pb_ratio", "pe_ratio", "ROA"]].round(4).to_string())

# 成交额异常低（流动性风险）
low_amount = df[(df["RFScore"] == 7) & (df["pb_group"] == 1) & (df["avg_amount_20d"] < 5e7)]
if len(low_amount) > 0:
    print(f"\\n[成交额<5000万] 低流动性股票({len(low_amount)}只):")
    print(low_amount[["name", "industry", "pb_ratio", "avg_amount_20d"]].round(4).to_string())

# 统计汇总
print("\\n" + "="*80)
print("统计汇总")
print("="*80)
print(f"总股票池: {len(df)}")
print(f"RFScore=7 数量: {len(df[df['RFScore'] == 7])}")
print(f"PB10% (group=1) 数量: {len(df[df['pb_group'] == 1])}")
print(f"PB10% & RFScore=7 数量: {len(pb10_candidates)}")
print(f"PE>100 的RFScore7候选股: {len(high_pe)}")
print(f"ROE<2% 的RFScore7候选股: {len(low_roe)}")
print(f"成交额<5000万的RFScore7候选股: {len(low_amount)}")
`;

async function main() {
    const outputDir = '/Users/fengzhi/Downloads/git/testlixingren/output';
    const resultFile = path.join(outputDir, 'rfscore_capacity_analysis.json');
    
    // JoinQuant notebook URL
    const NOTEBOOK_URL = 'https://www.joinquant.com/research?target=research&url=/user/21333940833/notebooks/test.ipynb';
    
    console.log('开始执行RFScore PB10容量分析...');
    console.log('获取真实成交额数据和候选分布...');
    
    try {
        const result = await runNotebookTest({
            notebookUrl: NOTEBOOK_URL,
            cellSource: cellSource,
            timeoutMs: 180000,
            appendCell: true
        });
        
        // 保存结果
        fs.mkdirSync(outputDir, { recursive: true });
        fs.writeFileSync(resultFile, JSON.stringify(result, null, 2));
        
        console.log('\\n容量分析完成！');
        console.log('结果已保存到:', resultFile);
        
        // 输出分析结果
        if (result.executions && result.executions.length > 0) {
            const lastExecution = result.executions[result.executions.length - 1];
            if (lastExecution.textOutput) {
                console.log('\\n=== 容量分析输出 ===');
                console.log(lastExecution.textOutput);
            }
            
            if (lastExecution.outputs && lastExecution.outputs.length > 0) {
                const errorOutput = lastExecution.outputs.find(o => o.output_type === 'error');
                if (errorOutput) {
                    console.log('\\n=== 执行错误 ===');
                    console.log(errorOutput);
                }
            }
        }
        
        return result;
    } catch (error) {
        console.error('容量分析失败:', error);
        throw error;
    }
}

main();
