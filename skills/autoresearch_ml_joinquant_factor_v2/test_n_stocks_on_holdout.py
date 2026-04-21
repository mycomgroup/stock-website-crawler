#!/usr/bin/env python3
"""
Test optimal n_stocks parameter on 2026 holdout set.

This script validates whether the n_stocks=100 parameter found optimal on 2024
validation set also performs well on the 2026 holdout set (never seen during optimization).

Purpose: Detect overfitting by comparing validation vs holdout performance.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

# Import optimization modules
from v2.optimization.utils import (
    load_predictions,
    calculate_ic_series,
    calculate_portfolio_metrics
)


def test_n_stocks_values(predictions_df, test_values=[50, 80, 100], year=2026):
    """
    Test different n_stocks values on holdout set.
    
    Args:
        predictions_df: DataFrame with predictions and returns
        test_values: List of n_stocks values to test
        year: Year to test on (default 2026 holdout)
    
    Returns:
        DataFrame with results for each n_stocks value
    """
    print(f"\n{'='*80}")
    print(f"Testing n_stocks on {year} Holdout Set")
    print(f"{'='*80}")
    print(f"Data points: {len(predictions_df)}")
    print(f"Date range: {predictions_df['date'].min()} to {predictions_df['date'].max()}")
    print(f"Unique dates: {predictions_df['date'].nunique()}")
    
    # Determine prediction column name
    if 'oof_prediction' in predictions_df.columns:
        pred_col = 'oof_prediction'
    elif 'prediction' in predictions_df.columns:
        pred_col = 'prediction'
    else:
        raise ValueError("No prediction column found (expected 'oof_prediction' or 'prediction')")
    
    print(f"Using prediction column: {pred_col}")
    
    results = []
    
    for n_stocks in test_values:
        print(f"\n{'-'*80}")
        print(f"Testing n_stocks = {n_stocks}")
        print(f"{'-'*80}")
        
        # Calculate IC metrics (same for all n_stocks)
        ic_series = calculate_ic_series(predictions_df, pred_col=pred_col)
        ic_mean = ic_series.mean()
        ic_std = ic_series.std()
        ic_ir = ic_mean / ic_std if ic_std > 0 else 0
        
        # Calculate portfolio metrics with this n_stocks
        portfolio_metrics = calculate_portfolio_metrics(
            predictions_df,
            n_stocks=n_stocks,
            pred_col=pred_col,
        )
        
        # Store results
        result = {
            'n_stocks': n_stocks,
            'year': year,
            'ic_mean': ic_mean,
            'ic_std': ic_std,
            'ic_ir': ic_ir,
            'ic_positive_ratio': (ic_series > 0).mean(),
            **portfolio_metrics
        }
        results.append(result)
        
        # Print key metrics
        print(f"  IC Mean: {ic_mean:.4f}")
        print(f"  IC IR: {ic_ir:.4f}")
        print(f"  Annual Return: {portfolio_metrics['annual_return']:.2f}%")
        print(f"  Annual Excess: {portfolio_metrics['annual_excess']:.2f}%")
        print(f"  Sharpe: {portfolio_metrics['sharpe']:.4f}")
        print(f"  Annual Vol: {portfolio_metrics['annual_vol']:.2f}%")
    
    return pd.DataFrame(results)


def compare_validation_vs_holdout(validation_results, holdout_results):
    """
    Compare validation (2024) vs holdout (2026) performance.
    
    Calculates decay rates to detect overfitting.
    """
    print(f"\n{'='*80}")
    print(f"Validation (2024) vs Holdout (2026) Comparison")
    print(f"{'='*80}")
    
    comparison = []
    
    for n_stocks in validation_results['n_stocks'].unique():
        val_row = validation_results[validation_results['n_stocks'] == n_stocks].iloc[0]
        hold_row = holdout_results[holdout_results['n_stocks'] == n_stocks].iloc[0]
        
        # Calculate decay rates
        ic_decay = (val_row['ic_ir'] - hold_row['ic_ir']) / val_row['ic_ir'] * 100
        sharpe_decay = (val_row['sharpe'] - hold_row['sharpe']) / val_row['sharpe'] * 100
        excess_decay = (val_row['annual_excess'] - hold_row['annual_excess']) / val_row['annual_excess'] * 100
        
        # Determine if passed overfitting test
        passed = ic_decay < 20 and sharpe_decay < 20 and excess_decay < 20
        
        comp = {
            'n_stocks': n_stocks,
            'val_ic_ir': val_row['ic_ir'],
            'hold_ic_ir': hold_row['ic_ir'],
            'ic_decay_pct': ic_decay,
            'val_sharpe': val_row['sharpe'],
            'hold_sharpe': hold_row['sharpe'],
            'sharpe_decay_pct': sharpe_decay,
            'val_annual_excess': val_row['annual_excess'],
            'hold_annual_excess': hold_row['annual_excess'],
            'excess_decay_pct': excess_decay,
            'overfitting_test': 'PASS' if passed else 'FAIL'
        }
        comparison.append(comp)
        
        # Print comparison
        print(f"\n{'-'*80}")
        print(f"n_stocks = {n_stocks}")
        print(f"{'-'*80}")
        print(f"IC IR:          {val_row['ic_ir']:.4f} → {hold_row['ic_ir']:.4f} (decay: {ic_decay:+.1f}%)")
        print(f"Sharpe:         {val_row['sharpe']:.4f} → {hold_row['sharpe']:.4f} (decay: {sharpe_decay:+.1f}%)")
        print(f"Annual Excess:  {val_row['annual_excess']:.2f}% → {hold_row['annual_excess']:.2f}% (decay: {excess_decay:+.1f}%)")
        print(f"Overfitting Test: {comp['overfitting_test']}")
        
        if passed:
            print("✅ PASSED - Performance decay < 20% on all metrics")
        else:
            print("❌ FAILED - Performance decay >= 20% on some metrics")
    
    return pd.DataFrame(comparison)


def generate_recommendation(comparison_df):
    """Generate final recommendation based on comparison."""
    print(f"\n{'='*80}")
    print(f"FINAL RECOMMENDATION")
    print(f"{'='*80}")
    
    # Find best n_stocks that passed overfitting test
    passed = comparison_df[comparison_df['overfitting_test'] == 'PASS']
    
    if len(passed) == 0:
        print("\n❌ NO PARAMETER PASSED OVERFITTING TEST")
        print("\nRecommendation: Keep current n_stocks=50")
        print("Reason: All tested values show >20% performance decay on holdout")
        return None
    
    # Among passed, find best holdout Sharpe
    best_idx = passed['hold_sharpe'].idxmax()
    best = passed.loc[best_idx]
    
    print(f"\n✅ RECOMMENDED: n_stocks = {int(best['n_stocks'])}")
    print(f"\nPerformance on 2026 Holdout:")
    print(f"  IC IR: {best['hold_ic_ir']:.4f}")
    print(f"  Sharpe: {best['hold_sharpe']:.4f}")
    print(f"  Annual Excess: {best['hold_annual_excess']:.2f}%")
    
    print(f"\nDecay from Validation:")
    print(f"  IC IR: {best['ic_decay_pct']:+.1f}%")
    print(f"  Sharpe: {best['sharpe_decay_pct']:+.1f}%")
    print(f"  Annual Excess: {best['excess_decay_pct']:+.1f}%")
    
    print(f"\n✅ All decay rates < 20% - No overfitting detected")
    
    # Compare to baseline (n_stocks=50)
    baseline = comparison_df[comparison_df['n_stocks'] == 50].iloc[0]
    sharpe_improvement = best['hold_sharpe'] - baseline['hold_sharpe']
    excess_improvement = best['hold_annual_excess'] - baseline['hold_annual_excess']
    
    print(f"\nImprovement vs Baseline (n_stocks=50):")
    print(f"  Sharpe: {baseline['hold_sharpe']:.4f} → {best['hold_sharpe']:.4f} (+{sharpe_improvement:.4f})")
    print(f"  Annual Excess: {baseline['hold_annual_excess']:.2f}% → {best['hold_annual_excess']:.2f}% (+{excess_improvement:.2f}%)")
    
    return int(best['n_stocks'])


def main():
    """Main execution function."""
    print("="*80)
    print("Testing n_stocks Parameter on 2026 Holdout Set")
    print("="*80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load predictions with returns for holdout year (2026)
    print("\n[1/5] Loading 2026 holdout predictions...")
    predictions_df = load_predictions(
        predictions_path='output/phase2/predictions_2026_holdout.csv',
        years=None,  # Load all years from this file (should only be 2026)
        merge_actuals=True
    )
    
    if len(predictions_df) == 0:
        print("ERROR: No data found in 2026 holdout file")
        print("Please check that Phase 2 generated 2026 predictions")
        return
    
    print(f"  Loaded {len(predictions_df)} rows")
    print(f"  Date range: {predictions_df['date'].min()} to {predictions_df['date'].max()}")
    print(f"  Years: {sorted(predictions_df['date'].dt.year.unique())}")
    
    # Load validation results (2024)
    print("\n[2/5] Loading validation results (2024)...")
    validation_results = pd.read_csv('output/optimization/sensitivity/sensitivity_results.csv')
    validation_results = validation_results[validation_results['param_name'] == 'n_stocks'].copy()
    validation_results = validation_results.rename(columns={'param_value': 'n_stocks'})
    validation_results['year'] = 2024
    print(f"  Loaded {len(validation_results)} validation results")
    
    # Test on holdout (2026)
    print("\n[3/5] Testing on holdout set (2026)...")
    test_values = [30, 40, 50, 60, 80, 100]  # Same values as sensitivity analysis
    holdout_results = test_n_stocks_values(
        predictions_df=predictions_df,
        test_values=test_values,
        year=2026
    )
    
    # Compare validation vs holdout
    print("\n[4/5] Comparing validation vs holdout...")
    comparison = compare_validation_vs_holdout(validation_results, holdout_results)
    
    # Generate recommendation
    print("\n[5/5] Generating recommendation...")
    recommended_n_stocks = generate_recommendation(comparison)
    
    # Save results
    output_dir = Path('output/optimization/holdout_test')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    holdout_results.to_csv(output_dir / 'holdout_results_2026.csv', index=False)
    comparison.to_csv(output_dir / 'validation_vs_holdout_comparison.csv', index=False)
    
    # Save recommendation
    recommendation = {
        'test_date': datetime.now().isoformat(),
        'validation_year': 2024,
        'holdout_year': 2026,
        'tested_values': test_values,
        'recommended_n_stocks': recommended_n_stocks,
        'baseline_n_stocks': 50,
        'comparison': comparison.to_dict('records')
    }
    
    with open(output_dir / 'recommendation.json', 'w') as f:
        json.dump(recommendation, f, indent=2)
    
    print(f"\n{'='*80}")
    print(f"Results saved to: {output_dir}")
    print(f"  - holdout_results_2026.csv")
    print(f"  - validation_vs_holdout_comparison.csv")
    print(f"  - recommendation.json")
    print(f"{'='*80}")
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    main()
