#!/bin/bash
# 批量提交策略到RiceQuant
# 每个策略创建独立ID，不覆盖

cd /Users/yuping/Downloads/git/jk2bt-main/lib/stock-website-crawler/skills/ricequant_strategy

STRATEGIES=(
  "quantsplaybook_validation/strategies/01_icu_ma.py"
  "quantsplaybook_validation/strategies/02_time_varying_sharpe.py"
  "quantsplaybook_validation/strategies/03_diffusion_indicator.py"
  "quantsplaybook_validation/strategies/04_ma_channel.py"
  "quantsplaybook_validation/strategies/05_rsrs_optimized.py"
  "quantsplaybook_validation/strategies/06_qrs.py"
  "quantsplaybook_validation/strategies/07_low_lag_trend.py"
  "quantsplaybook_validation/strategies/08_bull_bear_indicator.py"
  "quantsplaybook_validation/strategies/09_price_volume_resonance.py"
  "quantsplaybook_validation/strategies/10_alligator.py"
)

START_DATE="2015-01-01"
END_DATE="2024-12-31"

echo "============================================================"
echo "批量提交策略到 RiceQuant"
echo "每个策略创建独立ID"
echo "============================================================"
echo "策略数量: ${#STRATEGIES[@]}"
echo "回测区间: $START_DATE 至 $END_DATE"
echo "============================================================"

for strategy in "${STRATEGIES[@]}"; do
  echo ""
  echo ">>> 提交: $strategy"
  node run-skill.js --file "$strategy" --start "$START_DATE" --end "$END_DATE"
  echo "<<< 完成: $strategy"
  echo ""

  # 避免API限流，等待5秒
  sleep 5
done

echo "============================================================"
echo "全部策略提交完成"
echo "============================================================"