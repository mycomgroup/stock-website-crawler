#!/usr/bin/env python3
"""批量顺序执行回测迭代，从 current_iter 跑到 target_iter"""
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

BASE = Path("trees/E_technical_trend/experiments/e1")
PRECISE = Path("run_precise.py")

# 预定义的方向列表 (mutation_summary, args)
# --set-formula 格式: "old->new" 或 "new_clause"
# --set-param 格式: "key=value"
MUTATIONS = [
    ("[参数] 止盈 18% → 30%", ["--set-param", "takeProfit=30"]),
    ("[参数] 止盈 18% → 40%", ["--set-param", "takeProfit=40"]),
    ("[参数] 止损 7% → 12%", ["--set-param", "stopLoss=12"]),
    ("[参数] 止损 7% → 15%", ["--set-param", "stopLoss=15"]),
    ("[参数] 追踪止损 8% → 5%", ["--set-param", "trailingStopLoss=5"]),
    ("[参数] 追踪止损 8% → 7%", ["--set-param", "trailingStopLoss=7"]),
    ("[参数] 追踪止损 8% → 10%", ["--set-param", "trailingStopLoss=10"]),
    ("[替换] 股价站上20日均线 → 股价站上60日均线", ["--set-formula", "股价站上20日均线->股价站上60日均线"]),
    ("[添加] 近5日涨跌幅大于0", ["--set-formula", "近5日涨跌幅大于0"]),
    ("[替换] 近20日涨跌幅大于0 → 近5日涨跌幅大于0", ["--set-formula", "近20日涨跌幅大于0->近5日涨跌幅大于0"]),
    ("[替换] 近20日涨跌幅大于0 → 近10日涨跌幅大于0", ["--set-formula", "近20日涨跌幅大于0->近10日涨跌幅大于0"]),
    ("[阈值] 市盈率 50 → 45", ["--set-formula", "市盈率小于50->市盈率小于45"]),
    ("[阈值] 净资产收益率 10% → 15%", ["--set-formula", "净资产收益率大于10%->净资产收益率大于15%"]),
    ("[阈值] 营业收入增长率 15% → 10%", ["--set-formula", "营业收入增长率大于15%->营业收入增长率大于10%"]),
    ("[添加] 动态市盈率大于0小于20", ["--set-formula", "动态市盈率大于0小于20"]),
    ("[添加] PEG小于1", ["--set-formula", "PEG小于1"]),
    ("[添加] 净利润同比增速递增", ["--set-formula", "净利润同比增速递增"]),
    ("[添加] 扣非净利润同比转正", ["--set-formula", "扣非净利润同比转正"]),
    ("[添加] 高送转预期", ["--set-formula", "高送转预期"]),
    ("[添加] 热点概念", ["--set-formula", "热点概念"]),
    ("[替换] 股价站上20日均线 → 突破20日均线", ["--set-formula", "股价站上20日均线->突破20日均线"]),
    ("[添加] 成交量放大", ["--set-formula", "成交量放大"]),
    ("[添加] 缩量下跌", ["--set-formula", "缩量下跌"]),
    ("[替换] 近20日涨跌幅大于0 → 近一月涨跌幅大于0", ["--set-formula", "近20日涨跌幅大于0->近一月涨跌幅大于0"]),
    ("[替换] 近20日涨跌幅大于0 → 近三月涨跌幅大于0", ["--set-formula", "近20日涨跌幅大于0->近三月涨跌幅大于0"]),
    ("[组合参数] stopLoss=9, trailingStopLoss=10", ["--set-param", "stopLoss=9", "--set-param", "trailingStopLoss=10"]),
    ("[组合参数] stopLoss=10, trailingStopLoss=12", ["--set-param", "stopLoss=10", "--set-param", "trailingStopLoss=12"]),
    ("[添加] 周成交量环比增长率大于5%", ["--set-formula", "周成交量环比增长率大于5%"]),
    ("[替换] 股价站上20日均线 → 均线多头排列", ["--set-formula", "股价站上20日均线->均线多头排列"]),
    ("[替换] 股价站上20日均线 → 5日均线上穿20日均线", ["--set-formula", "股价站上20日均线->5日均线上穿20日均线"]),
    ("[添加] MACD红柱", ["--set-formula", "MACD红柱"]),
    ("[添加] KDJ金叉", ["--set-formula", "KDJ金叉"]),
    ("[替换] 股价站上20日均线 → BOLL下轨反弹", ["--set-formula", "股价站上20日均线->BOLL下轨反弹"]),
    ("[添加] 下影线较长", ["--set-formula", "下影线较长"]),
    ("[替换] 近20日涨跌幅大于0 → 近20日涨跌幅排名前50%", ["--set-formula", "近20日涨跌幅大于0->近20日涨跌幅排名前50%"]),
    ("[添加] 股价创20日新高", ["--set-formula", "股价创20日新高"]),
    ("[添加] 股价创60日新高", ["--set-formula", "股价创60日新高"]),
    ("[替换] 股价站上20日均线 → 股价创20日新高", ["--set-formula", "股价站上20日均线->股价创20日新高"]),
    ("[添加] 主力资金净流入", ["--set-formula", "主力资金净流入"]),
    ("[添加] 龙虎榜", ["--set-formula", "龙虎榜"]),
    ("[添加] 北向资金持股", ["--set-formula", "北向资金持股"]),
    ("[替换] 市盈率小于50 → 市盈率大于0小于30", ["--set-formula", "市盈率小于50->市盈率大于0小于30"]),
    ("[添加] 股息率大于2%", ["--set-formula", "股息率大于2%"]),
    ("[添加] 每股净资产大于5元", ["--set-formula", "每股净资产大于5元"]),
    ("[替换] 营业收入增长率大于15% → 营业收入增长率大于20%", ["--set-formula", "营业收入增长率大于15%->营业收入增长率大于20%"]),
    ("[添加] 季度营收环比增长率大于10%", ["--set-formula", "季度营收环比增长率大于10%"]),
    ("[添加] 季度净利润环比增长率大于10%", ["--set-formula", "季度净利润环比增长率大于10%"]),
    ("[替换] 股价站上20日均线 → 股价大于5日均线", ["--set-formula", "股价站上20日均线->股价大于5日均线"]),
    ("[添加] 5日均线大于10日均线", ["--set-formula", "5日均线大于10日均线"]),
    ("[添加] 10日均线大于20日均线", ["--set-formula", "10日均线大于20日均线"]),
    ("[组合参数] dailyBuyCount=1", ["--set-param", "dailyBuyCount=1"]),
    ("[组合参数] dailyBuyCount=5", ["--set-param", "dailyBuyCount=5"]),
    ("[组合参数] takeProfit=15, stopLoss=5", ["--set-param", "takeProfit=15", "--set-param", "stopLoss=5"]),
    ("[组合参数] takeProfit=25, stopLoss=10", ["--set-param", "takeProfit=25", "--set-param", "stopLoss=10"]),
    ("[添加] 流通市值小于300亿", ["--set-formula", "流通市值小于300亿"]),
    ("[添加] 流通市值小于100亿", ["--set-formula", "流通市值小于100亿"]),
    ("[添加] 成交额大于2000万", ["--set-formula", "成交额大于2000万"]),
    ("[添加] 成交额大于3000万", ["--set-formula", "成交额大于3000万"]),
    ("[替换] 股价站上20日均线 → 收盘价大于开盘价", ["--set-formula", "股价站上20日均线->收盘价大于开盘价"]),
    ("[添加] 阳线", ["--set-formula", "阳线"]),
    ("[添加] 放量上涨", ["--set-formula", "放量上涨"]),
    ("[替换] 近20日涨跌幅大于0 → 近20日涨跌幅大于5%", ["--set-formula", "近20日涨跌幅大于0->近20日涨跌幅大于5%"]),
    ("[替换] 近20日涨跌幅大于0 → 近20日涨跌幅大于10%", ["--set-formula", "近20日涨跌幅大于0->近20日涨跌幅大于10%"]),
    ("[添加] RSI大于50", ["--set-formula", "RSI大于50"]),
    ("[添加] CCI大于0", ["--set-formula", "CCI大于0"]),
    ("[替换] 股价站上20日均线 → 股价站上30日均线", ["--set-formula", "股价站上20日均线->股价站上30日均线"]),
    ("[添加] OBV创新高", ["--set-formula", "OBV创新高"]),
    ("[添加] 量价齐升", ["--set-formula", "量价齐升"]),
    ("[替换] 市盈率小于50 → 市盈率小于100", ["--set-formula", "市盈率小于50->市盈率小于100"]),
    ("[替换] 净资产收益率大于10% → 净资产收益率大于8%", ["--set-formula", "净资产收益率大于10%->净资产收益率大于8%"]),
    ("[参数] 持仓天数 3,5 → 4,6", ["--set-param", "daysForSaleStrategy=4,6"]),
    ("[参数] 持仓天数 3,5 → 3,7", ["--set-param", "daysForSaleStrategy=3,7"]),
    ("[添加] 周成交量环比增长率大于10%", ["--set-formula", "周成交量环比增长率大于10%"]),
    ("[替换] 股价站上20日均线 → 股价大于60日均线", ["--set-formula", "股价站上20日均线->股价大于60日均线"]),
    ("[添加] 换手率大于5%", ["--set-formula", "换手率大于5%"]),
    ("[添加] 换手率大于8%", ["--set-formula", "换手率大于8%"]),
    ("[替换] 市盈率小于50 → 市盈率小于35", ["--set-formula", "市盈率小于50->市盈率小于35"]),
    ("[替换] 营业收入增长率大于15% → 营业收入增长率大于25%", ["--set-formula", "营业收入增长率大于15%->营业收入增长率大于25%"]),
    ("[添加] 净利润增长率大于20%", ["--set-formula", "净利润增长率大于20%"]),
    ("[添加] 净利润增长率大于30%", ["--set-formula", "净利润增长率大于30%"]),
    ("[替换] 股价站上20日均线 → 股价大于10日均线", ["--set-formula", "股价站上20日均线->股价大于10日均线"]),
    ("[添加] 市值从小到大", ["--set-formula", "市值从小到大"]),
    ("[添加] 成交额从大到小", ["--set-formula", "成交额从大到小"]),
    ("[添加] 涨跌幅从大到小", ["--set-formula", "涨跌幅从大到小"]),
    ("[参数] 止盈 18% → 15%", ["--set-param", "takeProfit=15"]),
    ("[参数] 止损 7% → 9%", ["--set-param", "stopLoss=9"]),
    ("[参数] 持仓天数 3,5 → 5,10", ["--set-param", "daysForSaleStrategy=5,10"]),
    ("[参数] 持仓天数 3,5 → 2", ["--set-param", "daysForSaleStrategy=2"]),
    ("[参数] 持仓天数 3,5 → 3", ["--set-param", "daysForSaleStrategy=3"]),
    ("[参数] maxPositions=2 → 3", ["--set-param", "maxPositions=3"]),
    ("[参数] maxPositions=2 → 1", ["--set-param", "maxPositions=1"]),
    ("[替换] 近20日涨跌幅大于0 → 近60日涨跌幅大于0", ["--set-formula", "近20日涨跌幅大于0->近60日涨跌幅大于0"]),
    ("[添加] 非科创板", ["--set-formula", "非科创板"]),
    ("[添加] 经营活动产生的现金流量净额大于0", ["--set-formula", "经营活动产生的现金流量净额大于0"]),
]


def load_state():
    with open(BASE / "state.json", encoding="utf-8") as f:
        return json.load(f)


def append_search_notes(iter_id, summary, decision, score, annual, dd):
    notes_path = BASE / "search_notes.md"
    line = f"| {iter_id} | {summary} | {decision} | {score:.4f} | {annual:.2%} | {dd:.2%} |\n"
    with open(notes_path, "a", encoding="utf-8") as f:
        f.write(line)


def main():
    target_iter = 200
    crash_count = 0
    max_crash = 10

    while True:
        state = load_state()
        current_iter = state.get("current_iter", 1)
        if current_iter >= target_iter:
            print(f"Reached target iter {current_iter}. Stopping.")
            break

        idx = current_iter - 100
        if idx < 0 or idx >= len(MUTATIONS):
            # fallback: random mutation via run_iteration.py
            summary = "[随机探索] 自动随机变异"
            cmd = [
                sys.executable, "run_iteration.py",
                "--base", str(BASE),
                "--mutation-summary", summary,
            ]
        else:
            summary, extra_args = MUTATIONS[idx]
            cmd = [
                sys.executable, str(PRECISE),
                "--base", str(BASE),
                "--mutation-summary", summary,
            ] + extra_args

        print(f"\n=== Running iter {current_iter:04d}: {summary} ===")
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout + result.stderr
        print(output)

        # parse decision from output
        decision = "crash"
        score = 0.0
        annual = 0.0
        dd = 0.0
        if "decision=keep" in output or "决策: keep" in output:
            decision = "keep"
        elif "decision=rollback" in output or "决策: rollback" in output:
            decision = "rollback"
        else:
            decision = "crash"

        # parse metrics
        for line in output.splitlines():
            if "score=" in line and "champion=" in line:
                # [0125] score=6.5508 champion=42.7997 annual=300.00% dd=10.00% decision=rollback
                try:
                    score = float(line.split("score=")[1].split()[0])
                    annual_str = line.split("annual=")[1].split()[0].replace("%", "").replace(",", "")
                    annual = float(annual_str) / 100.0 if annual_str else 0.0
                    dd_str = line.split("dd=")[1].split()[0].replace("%", "").replace(",", "")
                    dd = float(dd_str) / 100.0 if dd_str else 0.0
                except Exception:
                    pass

        if decision == "crash":
            crash_count += 1
            print(f"Crash count: {crash_count}")
            if crash_count >= max_crash:
                print("Too many consecutive crashes. Stopping.")
                break
        else:
            crash_count = 0

        append_search_notes(f"{current_iter:04d}", summary, decision, score, annual, dd)

        # small delay to avoid rate limit
        import time
        time.sleep(2)


if __name__ == "__main__":
    main()
