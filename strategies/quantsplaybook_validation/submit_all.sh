#!/bin/bash
# 批量提交策略到RiceQuant (不等待回测完成，但会检查正在运行的数量避免超限)
cd /Users/fengzhi/Downloads/git/testlixingren/skills/ricequant_strategy

# 格式: "策略ID|文件路径"
STRATEGIES=(
  "2417178|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/01_icu_ma.py"
  "2417179|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/02_time_varying_sharpe.py"
  "2417180|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/03_diffusion_indicator.py"
  "2417186|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/04_ma_channel.py"
  "2417084|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/05_rsrs_optimized.py"
  "2417187|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/06_qrs.py"
  "2417188|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/07_low_lag_trend.py"
  "2417189|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/08_bull_bear_indicator.py"
  "2417190|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/09_price_volume_resonance.py"
  "2417192|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/10_alligator.py"
  "2417193|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/11_unidirectional_volatility.py"
  "2417194|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/12_higher_moments.py"
  "2417217|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/13_herd_effect.py"
  "2417198|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/14_trend_momentum.py"
  "2417199|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/15_northbound_fund.py"
  "2417200|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/16_volatility_factor.py"
  "2417203|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/17_point_efficiency.py"
  "2417204|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/18_investor_sentiment.py"
  "2417205|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/19_new_high_low.py"
  "2417206|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/20_wavelet_analysis.py"
  "2417207|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/21_cvix.py"
  "2417208|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/22_distribution_model.py"
  "2417219|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/23_trader_company.py"
  "2417212|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/24_pattern_recognition.py"
  "2417215|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/25_hht_model.py"
  "2417633|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/26_etf_intraday_momentum.py"
  "2417634|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/27_industry_top_bottom.py"
  "2417635|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/28_rounding_bottom_pattern.py"
  "2417636|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/29_high_quality_momentum.py"
  "2417637|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/30_smart_money_v2.py"
  "2417638|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/31_momentum_a_share.py"
  "2417639|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/32_chip_distribution_factor.py"
  "2417640|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/33_disposal_effect_factor.py"
  "2417641|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/34_cpv_factor.py"
  "2417642|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/35_industry_rotation_pv.py"
  "2417643|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/36_gold_stock_enhanced.py"
  "2417644|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/37_buy_sell_pressure.py"
  "2417645|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/38_overnight_intraday_network.py"
  "2417646|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/39_fund_overweight_factor.py"
  "2417647|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/40_stock_network_centrality.py"
  "2417648|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/41_fund_manager_alpha.py"
  "2417649|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/42_enterprise_lifecycle.py"
  "2417650|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/43_upper_lower_shadow.py"
  "2417651|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/44_pure_volatility_factor.py"
  "2417652|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/45_salience_str_factor.py"
  "2417653|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/46_factor_timing.py"
  "2417654|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/47_revisit_momentum.py"
  "2417655|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/48_amplitude_hidden_structure.py"
  "2417656|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/49_apm_factor.py"
  "2417657|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/50_team_coin_momentum.py"
  "2417658|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/51_microstructure_reversal.py"
  "2417659|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/52_multifactor_index_enhance.py"
  "2417660|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/53_ffscore_selection.py"
  "2417661|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/54_sw_cashflow_selection.py"
  "2417662|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/55_de_portfolio_optimization.py"
  "2417663|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/56_mlt_tsmom.py"
  "2417664|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/notebook_rsrs_dampened.py"
  "2417665|/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/strategies/notebook_rsrs_volume_weighted_dampened.py"
)

START_DATE="2026-01-01"
END_DATE="2026-04-01"
LOG_FILE="/Users/fengzhi/Downloads/git/testlixingren/strategies/quantsplaybook_validation/SUBMITTED_BACKTESTS.md"

echo "# RiceQuant 批量回测提交记录" > "$LOG_FILE"
echo "> 提交时间: $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "| 策略文件 | 策略ID | 回测ID | 状态 |" >> "$LOG_FILE"
echo "|----------|---------|---------|------|" >> "$LOG_FILE"

echo "============================================================"
echo "批量提交策略到 RiceQuant (Check-Wait 模式)"
echo "回测区间: $START_DATE 至 $END_DATE"
echo "日志文件: $LOG_FILE"
echo "============================================================"

for item in "${STRATEGIES[@]}"; do
  IFS="|" read -r id strategy <<< "$item"
  FILENAME=$(basename "$strategy")
  echo ""
  echo ">>> 提交: $FILENAME (ID: $id)"
  
  # 执行提交并捕获输出 (开启 wait-if-full 避免 403)
  OUTPUT=$(node run-skill.js --id "$id" --file "$strategy" --start "$START_DATE" --end "$END_DATE" --no-wait --wait-if-full 2>&1)
  echo "$OUTPUT"
  
  # 提取回测 ID
  BACKTEST_ID=$(echo "$OUTPUT" | grep "✓ Backtest started! ID:" | sed 's/.*ID: //')
  
  if [ -n "$BACKTEST_ID" ]; then
    echo "| $FILENAME | $id | $BACKTEST_ID | 🔄 已提交 |" >> "$LOG_FILE"
    echo "<<< 成功: $FILENAME -> BacktestID: $BACKTEST_ID"
  else
    echo "| $FILENAME | $id | N/A | ❌ 失败 |" >> "$LOG_FILE"
    echo "<<< 失败: $FILENAME"
  fi

  # 稍微等待一下让系统状态更新，然后再由于 wait-if-full 逻辑控制并发
  sleep 5
done

echo ""
echo "============================================================"
echo "全部策略提交任务已完成！"
echo "请查看日志获取所有回测ID: $LOG_FILE"
echo "============================================================"