"""
Portfolio Construction Tuning

Tests different portfolio construction methods
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, Any

import pandas as pd
import numpy as np

from .utils import OptimizationConfig, calculate_portfolio_metrics

logger = logging.getLogger(__name__)


class PortfolioTuner:
    """
    Portfolio construction tuner
    
    Tests different weighting schemes and construction methods
    """
    
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.output_dir = Path(config.output_dir) / 'portfolio_tuning'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def test_holding_sizes(
        self,
        predictions_df: pd.DataFrame,
        sizes: list[int] = None,
    ) -> pd.DataFrame:
        """
        Test different portfolio sizes
        
        Parameters
        ----------
        predictions_df : pd.DataFrame
            Predictions data
        sizes : list[int]
            Portfolio sizes to test
        
        Returns
        -------
        pd.DataFrame
            Results for each size
        """
        if sizes is None:
            sizes = [30, 40, 50, 60, 80, 100]
        
        logger.info("\n" + "="*80)
        logger.info("Testing Portfolio Sizes")
        logger.info("="*80)
        
        results = []
        
        for size in sizes:
            logger.info(f"\nTesting n_stocks = {size}")
            
            metrics = calculate_portfolio_metrics(
                predictions_df,
                n_stocks=size,
            )
            
            result = {
                'n_stocks': size,
                **metrics,
            }
            
            results.append(result)
            
            logger.info(f"  IC IR: {metrics.get('sharpe', 0):.2f}")
            logger.info(f"  Annual Return: {metrics['annual_return']:.2f}%")
        
        df_results = pd.DataFrame(results)
        
        # Save results
        output_path = self.output_dir / 'holding_sizes.csv'
        df_results.to_csv(output_path, index=False)
        logger.info(f"\nResults saved to {output_path}")
        
        return df_results
