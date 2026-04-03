#!/bin/bash
# 批量提交策略到RiceQuant
cd /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy

# 格式: "策略ID|文件路径"
STRATEGIES=(
  "2417178|quantsplaybook_validation/strategies/01_icu_ma.py"
  "2417179|quantsplaybook_validation/strategies/02_time_varying_sharpe.py"
  "2417180|quantsplaybook_validation/strategies/03_diffusion_indicator.py"
  "2417186|quantsplaybook_validation/strategies/04_ma_channel.py"
  "2417084|quantsplaybook_validation/strategies/05_rsrs_optimized.py"
  "2417187|quantsplaybook_validation/strategies/06_qrs.py"
  "2417188|quantsplaybook_validation/strategies/07_low_lag_trend.py"
  "2417189|quantsplaybook_validation/strategies/08_bull_bear_indicator.py"
  "2417190|quantsplaybook_validation/strategies/09_price_volume_resonance.py"
  "2417192|quantsplaybook_validation/strategies/10_alligator.py"
  "2417193|quantsplaybook_validation/strategies/11_unidirectional_volatility.py"
  "2417194|quantsplaybook_validation/strategies/12_higher_moments.py"
  "2417217|quantsplaybook_validation/strategies/13_herd_effect.py"
  "2417198|quantsplaybook_validation/strategies/14_trend_momentum.py"
  "2417199|quantsplaybook_validation/strategies/15_northbound_fund.py"
  "2417200|quantsplaybook_validation/strategies/16_volatility_factor.py"
  "2417203|quantsplaybook_validation/strategies/17_point_efficiency.py"
  "2417204|quantsplaybook_validation/strategies/18_investor_sentiment.py"
  "2417205|quantsplaybook_validation/strategies/19_new_high_low.py"
  "2417206|quantsplaybook_validation/strategies/20_wavelet_analysis.py"
  "2417207|quantsplaybook_validation/strategies/21_cvix.py"
  "2417208|quantsplaybook_validation/strategies/22_distribution_model.py"
  "2417219|quantsplaybook_validation/strategies/23_trader_company.py"
  "2417212|quantsplaybook_validation/strategies/24_pattern_recognition.py"
  "2417215|quantsplaybook_validation/strategies/25_hht_model.py"
)

START_DATE="2025-01-01"
END_DATE="2026-04-01"

echo "============================================================"
echo "批量提交策略到 RiceQuant"
echo "回测区间: $START_DATE 至 $END_DATE"
echo "============================================================"

for item in "${STRATEGIES[@]}"; do
  IFS="|" read -r id strategy <<< "$item"
  echo ""
  echo ">>> 提交: $strategy (ID: $id)"
  node run-skill.js --id "$id" --file "$strategy" --start "$START_DATE" --end "$END_DATE"
  echo "<<< 完成: $strategy"
  echo ""

  # 避免API限流，等待5秒
  sleep 5
done

echo "============================================================"
echo "全部策略提交完成"
echo "============================================================"