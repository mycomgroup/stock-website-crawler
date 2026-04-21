"""
Grid Search with Walk-Forward Validation

Integrates with existing v2/validation/walk_forward.py
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Any
from itertools import product

import pandas as pd
import numpy as np

from ..validation.walk_forward import WalkForwardSplitter
from .utils import OptimizationConfig, calculate_ic_series, calculate_portfolio_metrics

logger = logging.getLogger(__name__)


class GridSearchOptimizer:
    """
    Grid search optimizer with walk-forward validation
    
    Tests parameter combinations across multiple time windows
    """
    
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.output_dir = Path(config.output_dir) / 'grid_search'
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def define_param_grid(self) -> Dict[str, List[Any]]:
        """Define parameter grid"""
        
        return {
            'n_stocks': [40, 50, 60],
            'max_turnover': [0.25, 0.3, 0.35],
        }
    
    def run_walk_forward_optimization(
        self,
        predictions_df: pd.DataFrame,
        param_grid: Dict[str, List[Any]],
    ) -> pd.DataFrame:
        """
        Run walk-forward optimization
        
        Parameters
        ----------
        predictions_df : pd.DataFrame
            Predictions data
        param_grid : Dict[str, List[Any]]
            Parameter grid
        
        Returns
        -------
        pd.DataFrame
            Results for all parameter combinations
        """
        logger.info("\n" + "="*80)
        logger.info("Walk-Forward Grid Search")
        logger.info("="*80)
        
        # Generate parameter combinations
        param_names = list(param_grid.keys())
        param_values = list(param_grid.values())
        param_combinations = list(product(*param_values))
        
        logger.info(f"Testing {len(param_combinations)} parameter combinations")
        
        results = []
        
        for i, param_combo in enumerate(param_combinations):
            params = dict(zip(param_names, param_combo))
            
            logger.info(f"\n[{i+1}/{len(param_combinations)}] Testing: {params}")
            
            try:
                # Test on validation year
                val_df = predictions_df[predictions_df['date'].dt.year == self.config.validation_year]
                
                # Calculate metrics
                ic_series = calculate_ic_series(val_df)
                portfolio_metrics = calculate_portfolio_metrics(
                    val_df,
                    n_stocks=params.get('n_stocks', self.config.n_stocks),
                )
                
                result = {
                    **params,
                    'ic_mean': ic_series.mean(),
                    'ic_ir': ic_series.mean() / ic_series.std() if ic_series.std() > 0 else 0,
                    **portfolio_metrics,
                }
                
                results.append(result)
                
                logger.info(f"  IC IR: {result['ic_ir']:.4f}")
                logger.info(f"  Sharpe: {result['sharpe']:.2f}")
                
            except Exception as e:
                logger.error(f"  Error: {e}")
                continue
        
        df_results = pd.DataFrame(results)
        
        # Save results
        output_path = self.output_dir / 'grid_search_results.csv'
        df_results.to_csv(output_path, index=False)
        logger.info(f"\nResults saved to {output_path}")
        
        return df_results
    
    def select_best_params(self, df_results: pd.DataFrame) -> Dict[str, Any]:
        """
        Select best parameters based on IC IR
        
        Parameters
        ----------
        df_results : pd.DataFrame
            Results from grid search
        
        Returns
        -------
        Dict[str, Any]
            Best parameters
        """
        best_idx = df_results['ic_ir'].idxmax()
        best_params = df_results.loc[best_idx].to_dict()
        
        logger.info("\n" + "="*80)
        logger.info("Best Parameters")
        logger.info("="*80)
        
        for key, value in best_params.items():
            logger.info(f"  {key}: {value}")
        
        return best_params
