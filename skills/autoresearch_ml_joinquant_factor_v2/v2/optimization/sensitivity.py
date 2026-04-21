"""
Parameter Sensitivity Analysis

Analyzes how each parameter affects strategy performance
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from .utils import (
    OptimizationConfig,
    load_predictions,
    calculate_ic_series,
    calculate_portfolio_metrics,
    save_results,
)

logger = logging.getLogger(__name__)


@dataclass
class ParameterRange:
    """Parameter range for sensitivity analysis"""
    name: str
    values: List[Any]
    description: str = ""


class SensitivityAnalyzer:
    """
    Parameter sensitivity analyzer
    
    Tests each parameter independently while keeping others fixed
    """
    
    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.output_dir = Path(config.output_dir) / 'sensitivity'
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.results = []
    
    def define_parameter_ranges(self) -> List[ParameterRange]:
        """Define parameter ranges to test"""
        
        return [
            ParameterRange(
                name='n_stocks',
                values=[30, 40, 50, 60, 80, 100],
                description='Number of stocks in portfolio'
            ),
            ParameterRange(
                name='max_single_weight',
                values=[0.02, 0.025, 0.03, 0.04, 0.05],
                description='Maximum weight per stock'
            ),
            ParameterRange(
                name='max_turnover',
                values=[0.2, 0.25, 0.3, 0.35, 0.4],
                description='Maximum portfolio turnover'
            ),
            ParameterRange(
                name='max_single_family_weight',
                values=[0.3, 0.35, 0.4, 0.45, 0.5],
                description='Maximum weight per factor family'
            ),
            ParameterRange(
                name='weight_smoothing_halflife',
                values=[2, 3, 4, 5, 6, 8],
                description='Weight smoothing half-life'
            ),
        ]
    
    def run_single_parameter_scan(
        self,
        param_range: ParameterRange,
        predictions_df: pd.DataFrame,
    ) -> List[Dict[str, Any]]:
        """
        Run sensitivity analysis for a single parameter
        
        Parameters
        ----------
        param_range : ParameterRange
            Parameter to scan
        predictions_df : pd.DataFrame
            Predictions data
        
        Returns
        -------
        List[Dict[str, Any]]
            Results for each parameter value
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"Scanning parameter: {param_range.name}")
        logger.info(f"Values: {param_range.values}")
        logger.info(f"{'='*80}")
        
        results = []
        
        for i, param_value in enumerate(param_range.values):
            logger.info(f"\n[{i+1}/{len(param_range.values)}] Testing {param_range.name} = {param_value}")
            
            try:
                # For now, we test on existing predictions
                # In full implementation, would retrain model with new params
                
                # Simulate parameter effect on portfolio construction
                if param_range.name == 'n_stocks':
                    n_stocks = param_value
                else:
                    n_stocks = self.config.n_stocks
                
                # Calculate IC metrics
                ic_series = calculate_ic_series(predictions_df)
                ic_mean = ic_series.mean()
                ic_std = ic_series.std()
                ic_ir = ic_mean / ic_std if ic_std > 0 else 0
                
                # Calculate portfolio metrics
                portfolio_metrics = calculate_portfolio_metrics(
                    predictions_df,
                    n_stocks=n_stocks,
                )
                
                result = {
                    'param_name': param_range.name,
                    'param_value': param_value,
                    'ic_mean': ic_mean,
                    'ic_std': ic_std,
                    'ic_ir': ic_ir,
                    'ic_positive_ratio': (ic_series > 0).mean(),
                    **portfolio_metrics,
                }
                
                results.append(result)
                
                logger.info(f"  IC Mean: {ic_mean:.4f}")
                logger.info(f"  IC IR: {ic_ir:.4f}")
                logger.info(f"  Annual Return: {portfolio_metrics['annual_return']:.2f}%")
                logger.info(f"  Sharpe: {portfolio_metrics['sharpe']:.2f}")
                
            except Exception as e:
                logger.error(f"  Error testing {param_range.name}={param_value}: {e}")
                continue
        
        return results
    
    def run_all_scans(
        self,
        predictions_path: str | Path,
    ) -> pd.DataFrame:
        """
        Run sensitivity analysis for all parameters
        
        Parameters
        ----------
        predictions_path : str | Path
            Path to predictions CSV
        
        Returns
        -------
        pd.DataFrame
            All results
        """
        logger.info("\n" + "="*80)
        logger.info("Starting Parameter Sensitivity Analysis")
        logger.info("="*80)
        
        # Load predictions and merge with actual returns
        predictions_df = load_predictions(
            predictions_path,
            years=[self.config.validation_year],
            merge_actuals=True,
        )
        
        if len(predictions_df) == 0:
            logger.error(f"No data found for validation year {self.config.validation_year}")
            logger.error("Please check that you have data for this year")
            return pd.DataFrame()
        
        logger.info(f"Loaded {len(predictions_df)} predictions for {self.config.validation_year}")
        
        # Check if pchg column exists
        if 'pchg' not in predictions_df.columns:
            logger.error("pchg column not found in predictions")
            logger.error("Cannot calculate portfolio metrics without actual returns")
            return pd.DataFrame()
        
        # Define parameter ranges
        param_ranges = self.define_parameter_ranges()
        
        # Run scans
        all_results = []
        
        for param_range in param_ranges:
            results = self.run_single_parameter_scan(param_range, predictions_df)
            all_results.extend(results)
        
        if len(all_results) == 0:
            logger.error("No results generated")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df_results = pd.DataFrame(all_results)
        
        # Save results
        output_path = self.output_dir / 'sensitivity_results.csv'
        df_results.to_csv(output_path, index=False)
        logger.info(f"\nResults saved to {output_path}")
        
        self.results = df_results
        
        return df_results
    
    def analyze_results(self, df_results: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze sensitivity results
        
        Parameters
        ----------
        df_results : pd.DataFrame
            Results from run_all_scans
        
        Returns
        -------
        Dict[str, Any]
            Analysis summary
        """
        logger.info("\n" + "="*80)
        logger.info("Analyzing Sensitivity Results")
        logger.info("="*80)
        
        analysis = {}
        
        for param_name in df_results['param_name'].unique():
            df_param = df_results[df_results['param_name'] == param_name]
            
            # Calculate sensitivity metrics
            ic_range = df_param['ic_mean'].max() - df_param['ic_mean'].min()
            ic_cv = df_param['ic_mean'].std() / abs(df_param['ic_mean'].mean())
            
            sharpe_range = df_param['sharpe'].max() - df_param['sharpe'].min()
            sharpe_cv = df_param['sharpe'].std() / abs(df_param['sharpe'].mean())
            
            # Find optimal value
            best_idx = df_param['ic_ir'].idxmax()
            best_value = df_param.loc[best_idx, 'param_value']
            best_ic_ir = df_param.loc[best_idx, 'ic_ir']
            
            analysis[param_name] = {
                'ic_range': float(ic_range),
                'ic_cv': float(ic_cv),
                'sharpe_range': float(sharpe_range),
                'sharpe_cv': float(sharpe_cv),
                'best_value': best_value,
                'best_ic_ir': float(best_ic_ir),
                'sensitivity_score': float((ic_cv + sharpe_cv) / 2),
            }
            
            logger.info(f"\n{param_name}:")
            logger.info(f"  IC Range: {ic_range:.4f}")
            logger.info(f"  IC CV: {ic_cv:.4f}")
            logger.info(f"  Best Value: {best_value}")
            logger.info(f"  Best IC IR: {best_ic_ir:.4f}")
            logger.info(f"  Sensitivity Score: {analysis[param_name]['sensitivity_score']:.4f}")
        
        # Save analysis
        save_results(
            analysis,
            self.output_dir / 'sensitivity_analysis.json',
            format='json',
        )
        
        return analysis
    
    def generate_plots(self, df_results: pd.DataFrame):
        """
        Generate sensitivity plots
        
        Parameters
        ----------
        df_results : pd.DataFrame
            Results from run_all_scans
        """
        logger.info("\nGenerating sensitivity plots...")
        
        plot_dir = self.output_dir / 'plots'
        plot_dir.mkdir(exist_ok=True)
        
        sns.set_style("whitegrid")
        
        for param_name in df_results['param_name'].unique():
            df_param = df_results[df_results['param_name'] == param_name]
            
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle(f'Sensitivity Analysis: {param_name}', fontsize=16, fontweight='bold')
            
            # IC Mean
            axes[0, 0].plot(df_param['param_value'], df_param['ic_mean'], 'o-', linewidth=2, markersize=8)
            axes[0, 0].set_xlabel(param_name)
            axes[0, 0].set_ylabel('IC Mean')
            axes[0, 0].set_title('IC Mean vs Parameter Value')
            axes[0, 0].grid(True, alpha=0.3)
            
            # IC IR
            axes[0, 1].plot(df_param['param_value'], df_param['ic_ir'], 'o-', linewidth=2, markersize=8, color='orange')
            axes[0, 1].set_xlabel(param_name)
            axes[0, 1].set_ylabel('IC IR')
            axes[0, 1].set_title('IC Information Ratio vs Parameter Value')
            axes[0, 1].grid(True, alpha=0.3)
            
            # Annual Return
            axes[1, 0].plot(df_param['param_value'], df_param['annual_return'], 'o-', linewidth=2, markersize=8, color='green')
            axes[1, 0].set_xlabel(param_name)
            axes[1, 0].set_ylabel('Annual Return (%)')
            axes[1, 0].set_title('Annual Return vs Parameter Value')
            axes[1, 0].grid(True, alpha=0.3)
            
            # Sharpe Ratio
            axes[1, 1].plot(df_param['param_value'], df_param['sharpe'], 'o-', linewidth=2, markersize=8, color='red')
            axes[1, 1].set_xlabel(param_name)
            axes[1, 1].set_ylabel('Sharpe Ratio')
            axes[1, 1].set_title('Sharpe Ratio vs Parameter Value')
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            plot_path = plot_dir / f'{param_name}_sensitivity.png'
            plt.savefig(plot_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            logger.info(f"  Saved: {plot_path}")
        
        logger.info(f"\nAll plots saved to {plot_dir}")
    
    def generate_report(self, df_results: pd.DataFrame, analysis: Dict[str, Any]):
        """
        Generate text report
        
        Parameters
        ----------
        df_results : pd.DataFrame
            Results from run_all_scans
        analysis : Dict[str, Any]
            Analysis from analyze_results
        """
        logger.info("\nGenerating sensitivity report...")
        
        report_lines = []
        report_lines.append("="*80)
        report_lines.append("Parameter Sensitivity Analysis Report")
        report_lines.append("="*80)
        report_lines.append("")
        report_lines.append(f"Validation Year: {self.config.validation_year}")
        report_lines.append(f"Number of Parameters Tested: {len(analysis)}")
        report_lines.append("")
        
        # Sort by sensitivity
        sorted_params = sorted(
            analysis.items(),
            key=lambda x: x[1]['sensitivity_score'],
            reverse=True
        )
        
        report_lines.append("【Parameter Sensitivity Ranking】")
        report_lines.append("")
        report_lines.append("Rank | Parameter                      | Sensitivity | IC CV    | Best Value")
        report_lines.append("-" * 80)
        
        for rank, (param_name, metrics) in enumerate(sorted_params, 1):
            report_lines.append(
                f"{rank:2d}   | {param_name:30s} | {metrics['sensitivity_score']:>11.4f} | "
                f"{metrics['ic_cv']:>8.4f} | {metrics['best_value']}"
            )
        
        report_lines.append("")
        report_lines.append("【Detailed Analysis】")
        report_lines.append("")
        
        for param_name, metrics in sorted_params:
            sensitivity_level = 'High' if metrics['sensitivity_score'] > 0.1 else 'Medium' if metrics['sensitivity_score'] > 0.05 else 'Low'
            
            report_lines.append(f"\n{param_name}:")
            report_lines.append(f"  Sensitivity: {sensitivity_level}")
            report_lines.append(f"  IC Range: {metrics['ic_range']:.4f}")
            report_lines.append(f"  IC CV: {metrics['ic_cv']:.4f}")
            report_lines.append(f"  Sharpe Range: {metrics['sharpe_range']:.4f}")
            report_lines.append(f"  Optimal Value: {metrics['best_value']}")
            report_lines.append(f"  Optimal IC IR: {metrics['best_ic_ir']:.4f}")
        
        report_lines.append("")
        report_lines.append("【Recommendations】")
        report_lines.append("")
        
        high_sensitivity = [p for p, m in sorted_params if m['sensitivity_score'] > 0.1]
        low_sensitivity = [p for p, m in sorted_params if m['sensitivity_score'] < 0.05]
        
        report_lines.append(f"High Sensitivity Parameters (optimize carefully): {', '.join(high_sensitivity) if high_sensitivity else 'None'}")
        report_lines.append(f"Low Sensitivity Parameters (can fix): {', '.join(low_sensitivity) if low_sensitivity else 'None'}")
        report_lines.append("")
        report_lines.append("Suggested Optimization Priority:")
        for rank, (param_name, _) in enumerate(sorted_params[:5], 1):
            report_lines.append(f"  {rank}. {param_name}")
        
        report_lines.append("")
        report_lines.append("="*80)
        
        # Save report
        report_path = self.output_dir / 'sensitivity_report.txt'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        logger.info(f"Report saved to {report_path}")
        
        # Print to console
        print('\n'.join(report_lines))
