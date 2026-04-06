#!/bin/bash
cd /Users/yuping/Downloads/git/stock-website-crawler/skills/ricequant_strategy

START_DATE="2023-01-01"
END_DATE="2026-04-01"

echo "Submitting 01_icu_ma.py (ID:2417178)"
node run-skill.js --id 2417178 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/01_icu_ma.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 02_time_varying_sharpe.py (ID:2417179)"
node run-skill.js --id 2417179 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/02_time_varying_sharpe.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 03_diffusion_indicator.py (ID:2417180)"
node run-skill.js --id 2417180 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/03_diffusion_indicator.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 04_ma_channel.py (ID:2417186)"
node run-skill.js --id 2417186 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/04_ma_channel.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 05_rsrs_optimized.py (ID:2417084)"
node run-skill.js --id 2417084 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/05_rsrs_optimized.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 06_qrs.py (ID:2417187)"
node run-skill.js --id 2417187 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/06_qrs.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 07_low_lag_trend.py (ID:2417188)"
node run-skill.js --id 2417188 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/07_low_lag_trend.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 08_bull_bear_indicator.py (ID:2417189)"
node run-skill.js --id 2417189 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/08_bull_bear_indicator.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 09_price_volume_resonance.py (ID:2417190)"
node run-skill.js --id 2417190 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/09_price_volume_resonance.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 10_alligator.py (ID:2417192)"
node run-skill.js --id 2417192 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/10_alligator.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 11_unidirectional_volatility.py (ID:2417193)"
node run-skill.js --id 2417193 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/11_unidirectional_volatility.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 12_higher_moments.py (ID:2417194)"
node run-skill.js --id 2417194 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/12_higher_moments.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 13_herd_effect.py (ID:2417217)"
node run-skill.js --id 2417217 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/13_herd_effect.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 14_trend_momentum.py (ID:2417198)"
node run-skill.js --id 2417198 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/14_trend_momentum.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 15_northbound_fund.py (ID:2417199)"
node run-skill.js --id 2417199 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/15_northbound_fund.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 16_volatility_factor.py (ID:2417200)"
node run-skill.js --id 2417200 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/16_volatility_factor.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 17_point_efficiency.py (ID:2417203)"
node run-skill.js --id 2417203 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/17_point_efficiency.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 18_investor_sentiment.py (ID:2417204)"
node run-skill.js --id 2417204 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/18_investor_sentiment.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 19_new_high_low.py (ID:2417205)"
node run-skill.js --id 2417205 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/19_new_high_low.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 20_wavelet_analysis.py (ID:2417206)"
node run-skill.js --id 2417206 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/20_wavelet_analysis.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 21_cvix.py (ID:2417207)"
node run-skill.js --id 2417207 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/21_cvix.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 22_distribution_model.py (ID:2417208)"
node run-skill.js --id 2417208 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/22_distribution_model.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 23_trader_company.py (ID:2417219)"
node run-skill.js --id 2417219 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/23_trader_company.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 24_pattern_recognition.py (ID:2417212)"
node run-skill.js --id 2417212 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/24_pattern_recognition.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 25_hht_model.py (ID:2417215)"
node run-skill.js --id 2417215 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/25_hht_model.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 26_etf_intraday_momentum.py (ID:2417633)"
node run-skill.js --id 2417633 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/26_etf_intraday_momentum.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 27_industry_top_bottom.py (ID:2417634)"
node run-skill.js --id 2417634 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/27_industry_top_bottom.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 28_rounding_bottom_pattern.py (ID:2417635)"
node run-skill.js --id 2417635 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/28_rounding_bottom_pattern.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 29_high_quality_momentum.py (ID:2417636)"
node run-skill.js --id 2417636 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/29_high_quality_momentum.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 30_smart_money_v2.py (ID:2417637)"
node run-skill.js --id 2417637 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/30_smart_money_v2.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 31_momentum_a_share.py (ID:2417638)"
node run-skill.js --id 2417638 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/31_momentum_a_share.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 32_chip_distribution_factor.py (ID:2417639)"
node run-skill.js --id 2417639 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/32_chip_distribution_factor.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 33_disposal_effect_factor.py (ID:2417640)"
node run-skill.js --id 2417640 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/33_disposal_effect_factor.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 34_cpv_factor.py (ID:2417641)"
node run-skill.js --id 2417641 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/34_cpv_factor.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 35_industry_rotation_pv.py (ID:2417642)"
node run-skill.js --id 2417642 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/35_industry_rotation_pv.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 36_gold_stock_enhanced.py (ID:2417643)"
node run-skill.js --id 2417643 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/36_gold_stock_enhanced.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 37_buy_sell_pressure.py (ID:2417644)"
node run-skill.js --id 2417644 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/37_buy_sell_pressure.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 38_overnight_intraday_network.py (ID:2417645)"
node run-skill.js --id 2417645 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/38_overnight_intraday_network.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 39_fund_overweight_factor.py (ID:2417646)"
node run-skill.js --id 2417646 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/39_fund_overweight_factor.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 40_stock_network_centrality.py (ID:2417647)"
node run-skill.js --id 2417647 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/40_stock_network_centrality.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 41_fund_manager_alpha.py (ID:2417648)"
node run-skill.js --id 2417648 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/41_fund_manager_alpha.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 42_enterprise_lifecycle.py (ID:2417649)"
node run-skill.js --id 2417649 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/42_enterprise_lifecycle.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 43_upper_lower_shadow.py (ID:2417650)"
node run-skill.js --id 2417650 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/43_upper_lower_shadow.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 44_pure_volatility_factor.py (ID:2417651)"
node run-skill.js --id 2417651 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/44_pure_volatility_factor.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 45_salience_str_factor.py (ID:2417652)"
node run-skill.js --id 2417652 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/45_salience_str_factor.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 46_factor_timing.py (ID:2417653)"
node run-skill.js --id 2417653 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/46_factor_timing.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 47_revisit_momentum.py (ID:2417654)"
node run-skill.js --id 2417654 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/47_revisit_momentum.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 48_amplitude_hidden_structure.py (ID:2417655)"
node run-skill.js --id 2417655 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/48_amplitude_hidden_structure.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 49_apm_factor.py (ID:2417656)"
node run-skill.js --id 2417656 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/49_apm_factor.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 50_team_coin_momentum.py (ID:2417657)"
node run-skill.js --id 2417657 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/50_team_coin_momentum.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 51_microstructure_reversal.py (ID:2417658)"
node run-skill.js --id 2417658 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/51_microstructure_reversal.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 52_multifactor_index_enhance.py (ID:2417659)"
node run-skill.js --id 2417659 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/52_multifactor_index_enhance.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 53_ffscore_selection.py (ID:2417660)"
node run-skill.js --id 2417660 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/53_ffscore_selection.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 54_sw_cashflow_selection.py (ID:2417661)"
node run-skill.js --id 2417661 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/54_sw_cashflow_selection.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 55_de_portfolio_optimization.py (ID:2417662)"
node run-skill.js --id 2417662 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/55_de_portfolio_optimization.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting 56_mlt_tsmom.py (ID:2417663)"
node run-skill.js --id 2417663 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/56_mlt_tsmom.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting notebook_rsrs_dampened.py (ID:2417664)"
node run-skill.js --id 2417664 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/notebook_rsrs_dampened.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3

echo "Submitting notebook_rsrs_volume_weighted_dampened.py (ID:2417665)"
node run-skill.js --id 2417665 --file "/Users/yuping/Downloads/git/stock-website-crawler/strategies/quantsplaybook_validation/strategies/notebook_rsrs_volume_weighted_dampened.py" --start $START_DATE --end $END_DATE --no-wait
sleep 3
