"""
Overfitting Detection Suite

Tests for overfitting using multiple methods
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import numpy as np

from .utils import OptimizationConfig, calculate_ic_series, calculate_portfolio_metrics

logger = logging.getLogger(__name__)


class OverfittingDetector:
    """
    Overfitting detection suite
    
    Implements multiple tests to detect overfitting
    """
    
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.output_dir = Path(config.output_dir) / 'overfitting'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def test_oos_decay(
        self,
        val_predictions: pd.DataFrame,
        holdout_predictions: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Test out-of-sample performance decay
        
        Parameters
        ----------
        val_predictions : pd.DataFrame
            Validation set predictions
        holdout_predictions : pd.DataFrame
            Holdout set predictions
        
        Returns
        -------
        Dict[str, Any]
            Decay test results
        """
        logger.info("\n" + "="*80)
        logger.info("Out-of-Sample Decay Test")
        logger.info("="*80)
        
        # Calculate metrics on validation
        val_ic_series = calculate_ic_series(val_predictions)
        val_ic = val_ic_series.mean()
        val_metrics = calculate_portfolio_metrics(val_predictions)
        
        # Calculate metrics on holdout
        holdout_ic_series = calculate_ic_series(holdout_predictions)
        holdout_ic = holdout_ic_series.mean()
        holdout_metrics = calculate_portfolio_metrics(holdout_predictions)
        
        # Calculate decay
        ic_decay = (val_ic - holdout_ic) / abs(val_ic) if abs(val_ic) > 1e-8 else np.nan
        sharpe_decay = (val_metrics['sharpe'] - holdout_metrics['sharpe']) / abs(val_metrics['sharpe']) if abs(val_metrics['sharpe']) > 1e-8 else np.nan
        
        # Determine verdict
        ic_verdict = 'PASS' if ic_decay < 0.2 else 'WARNING' if ic_decay < 0.4 else 'FAIL'
        sharpe_verdict = 'PASS' if sharpe_decay < 0.2 else 'WARNING' if sharpe_decay < 0.4 else 'FAIL'
        
        result = {
            'val_ic': val_ic,
            'holdout_ic': holdout_ic,
            'ic_decay': ic_decay,
            'ic_verdict': ic_verdict,
            'val_sharpe': val_metrics['sharpe'],
            'holdout_sharpe': holdout_metrics['sharpe'],
            'sharpe_decay': sharpe_decay,
            'sharpe_verdict': sharpe_verdict,
        }
        
        logger.info(f"\nValidation IC: {val_ic:.4f}")
        logger.info(f"Holdout IC: {holdout_ic:.4f}")
        logger.info(f"IC Decay: {ic_decay*100:.1f}% [{ic_verdict}]")
        logger.info(f"\nValidation Sharpe: {val_metrics['sharpe']:.2f}")
        logger.info(f"Holdout Sharpe: {holdout_metrics['sharpe']:.2f}")
        logger.info(f"Sharpe Decay: {sharpe_decay*100:.1f}% [{sharpe_verdict}]")
        
        return result
    
    def generate_report(
        self,
        oos_decay_result: Dict[str, Any],
    ) -> str:
        """
        Generate overfitting detection report
        
        Parameters
        ----------
        oos_decay_result : Dict[str, Any]
            OOS decay test results
        
        Returns
        -------
        str
            Report text
        """
        report_lines = []
        report_lines.append("="*80)
        report_lines.append("Overfitting Detection Report")
        report_lines.append("="*80)
        report_lines.append("")
        
        report_lines.append("【Out-of-Sample Decay Test】")
        report_lines.append("")
        report_lines.append(f"Validation IC:  {oos_decay_result['val_ic']:.4f}")
        report_lines.append(f"Holdout IC:     {oos_decay_result['holdout_ic']:.4f}")
        report_lines.append(f"IC Decay:       {oos_decay_result['ic_decay']*100:.1f}% [{oos_decay_result['ic_verdict']}]")
        report_lines.append("")
        report_lines.append(f"Validation Sharpe: {oos_decay_result['val_sharpe']:.2f}")
        report_lines.append(f"Holdout Sharpe:    {oos_decay_result['holdout_sharpe']:.2f}")
        report_lines.append(f"Sharpe Decay:      {oos_decay_result['sharpe_decay']*100:.1f}% [{oos_decay_result['sharpe_verdict']}]")
        report_lines.append("")
        
        report_lines.append("【Interpretation】")
        report_lines.append("")
        report_lines.append("Decay < 20%:  Normal (PASS)")
        report_lines.append("Decay 20-40%: Mild overfitting (WARNING)")
        report_lines.append("Decay > 40%:  Severe overfitting (FAIL)")
        report_lines.append("")
        
        overall_verdict = 'PASS' if oos_decay_result['ic_verdict'] == 'PASS' and oos_decay_result['sharpe_verdict'] == 'PASS' else 'WARNING' if 'FAIL' not in [oos_decay_result['ic_verdict'], oos_decay_result['sharpe_verdict']] else 'FAIL'
        
        report_lines.append(f"【Overall Verdict】: {overall_verdict}")
        report_lines.append("")
        report_lines.append("="*80)
        
        report_text = '\n'.join(report_lines)
        
        # Save report
        report_path = self.output_dir / 'overfitting_report.txt'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        logger.info(f"\nReport saved to {report_path}")
        
        # Print to console
        print(report_text)
        
        return report_text
