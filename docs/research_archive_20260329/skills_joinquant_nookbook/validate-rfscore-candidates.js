#!/usr/bin/env node
/**
 * RFScore PB10 候选股验证脚本
 * 用于检测当前候选股中的异常值和口径不一致问题
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
val = get_valuation(stocks, end_date=trade_day_str, fields=["pb_ratio", "pe_ratio"], count=1)
val = val.drop_duplicates("code").set_index("code")[["pb_ratio", "pe_ratio"]]
df = df.join(val, how="left")

# 清洗数据
df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["RFScore", "pb_ratio"])

# PB分位（10组）
df["pb_group"] = pd.qcut(df["pb_ratio"].rank(method="first"), 10, labels=False, duplicates="drop") + 1

# 获取股票名称
name_map = get_all_securities(types=["stock"], date=trade_day).loc[df.index, "display_name"].to_dict()
df["name"] = df.index.map(name_map)

# 获取行业信息
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
    display_cols = ["name", "industry", "RFScore", "pb_ratio", "pe_ratio", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN"]
    print(pb10_candidates[display_cols].head(20).round(4).to_string())

print("\\n" + "="*80)
print("PB20% 候选股（RFScore=7 & pb_group<=2）")
print("="*80)
pb20_candidates = df[(df["RFScore"] == 7) & (df["pb_group"] <= 2)].copy()
pb20_candidates = pb20_candidates.sort_values(["ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN", "pb_ratio"],
                                               ascending=[False, False, False, False, True])
print(f"count: {len(pb20_candidates)}")
if len(pb20_candidates) > 0:
    display_cols = ["name", "industry", "RFScore", "pb_ratio", "pe_ratio", "ROA", "OCFOA", "DELTA_MARGIN", "DELTA_TURN"]
    print(pb20_candidates[display_cols].head(20).round(4).to_string())

# 异常值检测
print("\\n" + "="*80)
print("异常值审计")
print("="*80)

# PE异常高
pe_threshold = 100
high_pe = df[(df["RFScore"] == 7) & (df["pb_group"] <= 2) & (df["pe_ratio"] > pe_threshold)]
if len(high_pe) > 0:
    print(f"\\n[PE > {pe_threshold}] 异常高PE股票：")
    print(high_pe[["name", "industry", "RFScore", "pb_ratio", "pe_ratio", "ROA"]].round(4).to_string())

# ROE异常低（ROA * 4 估算 ROE）
roe_proxy = df["ROA"] * 4  # 近似ROE
low_roe = df[(df["RFScore"] == 7) & (df["pb_group"] <= 2) & (roe_proxy < 2)]
if len(low_roe) > 0:
    print(f"\\n[ROE < 2%] 低盈利能力股票：")
    print(low_roe[["name", "industry", "RFScore", "pb_ratio", "pe_ratio", "ROA"]].round(4).to_string())

# PB异常低（可能存在基本面问题）
low_pb = df[(df["RFScore"] == 7) & (df["pb_ratio"] < 0.4)]
if len(low_pb) > 0:
    print(f"\\n[PB < 0.4] 超低PB股票（可能基本面问题）：")
    print(low_pb[["name", "industry", "RFScore", "pb_ratio", "pe_ratio", "ROA"]].round(4).to_string())

# 统计汇总
print("\\n" + "="*80)
print("统计汇总")
print("="*80)
print(f"总股票池: {len(df)}")
print(f"RFScore=7 数量: {len(df[df['RFScore'] == 7])}")
print(f"PB10% (group=1) 数量: {len(df[df['pb_group'] == 1])}")
print(f"PB10% & RFScore=7 数量: {len(pb10_candidates)}")
print(f"PB20% (group<=2) & RFScore=7 数量: {len(pb20_candidates)}")
print(f"PE>100 的RFScore7候选股: {len(high_pe)}")
print(f"ROE<2% 的RFScore7候选股: {len(low_roe)}")
`;

async function main() {
    const resultFile = '/Users/fengzhi/Downloads/git/testlixingren/output/rfscore_candidate_validation.json';
    
    console.log('开始执行RFScore候选股验证...');
    
    try {
        const result = await runNotebookTest({
            cellSource: cellSource,
            timeoutMs: 120000,
            appendCell: true
        });
        
        // 保存结果
        fs.mkdirSync(path.dirname(resultFile), { recursive: true });
        fs.writeFileSync(resultFile, JSON.stringify(result, null, 2));
        
        console.log('验证完成，结果已保存到:', resultFile);
        
        if (result.stdout) {
            console.log('\\n=== 候选股验证输出 ===');
            console.log(result.stdout);
        }
        
        if (result.stderr) {
            console.log('\\n=== 错误输出 ===');
            console.log(result.stderr);
        }
        
        return result;
    } catch (error) {
        console.error('验证失败:', error);
        throw error;
    }
}

main();
