"""
Optimization utilities and configuration management
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class OptimizationConfig:
    """Configuration for optimization experiments"""
    
    # Data paths
    csv_path: str = "train_merged_all_with_2026.csv"
    output_dir: str = "output/optimization"
    
    # Time periods
    train_start_year: int = 2015
    train_end_year: int = 2023
    validation_year: int = 2024  # Use 2024 as validation (last year in OOF)
    holdout_year: int = 2026
    
    # Base parameters (from Phase 2)
    n_stocks: int = 50
    max_single_weight: float = 0.03
    max_turnover: float = 0.3
    max_single_family_weight: float = 0.4
    weight_smoothing_halflife: int = 4
    mad_multiplier: float = 5.0
    new_stock_cooldown_days: int = 60
    test_block: int = 52
    step: int = 4
    embargo: int = 1
    
    # Optimization settings
    random_state: int = 42
    n_bootstrap: int = 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> OptimizationConfig:
        """Create from dictionary"""
        return cls(**d)
    
    @classmethod
    def from_phase2(cls, phase2_snapshot_path: str | Path) -> OptimizationConfig:
        """Create config from Phase 2 snapshot"""
        with open(phase2_snapshot_path, 'r') as f:
            snapshot = json.load(f)
        
        config_dict = snapshot.get('config', {})
        
        return cls(
            n_stocks=config_dict.get('n_stocks', 50),
            max_single_weight=config_dict.get('max_single_weight', 0.03),
            max_turnover=config_dict.get('max_turnover', 0.3),
            max_single_family_weight=config_dict.get('max_single_family_weight', 0.4),
            weight_smoothing_halflife=config_dict.get('weight_smoothing_halflife', 4),
            test_block=config_dict.get('test_block', 52),
            step=config_dict.get('step', 4),
            embargo=config_dict.get('embargo', 1),
        )


def load_phase_data(
    csv_path: str | Path,
    years: List[int] | None = None,
) -> pd.DataFrame:
    """
    Load and filter data for specific years
    
    Parameters
    ----------
    csv_path : str | Path
        Path to CSV file
    years : List[int] | None
        Years to filter (None = all years)
    
    Returns
    -------
    pd.DataFrame
        Filtered data
    """
    logger.info(f"Loading data from {csv_path}")
    
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    
    if 'Unnamed: 0' in df.columns:
        df = df.rename(columns={'Unnamed: 0': 'stock_id'})
    
    if years is not None:
        df = df[df['date'].dt.year.isin(years)]
        logger.info(f"Filtered to years {years}: {len(df)} rows")
    
    logger.info(f"Loaded {len(df)} rows, {df['date'].nunique()} dates")
    
    return df


def load_predictions(
    predictions_path: str | Path,
    years: List[int] | None = None,
    merge_actuals: bool = True,
    csv_path: str | Path | None = None,
) -> pd.DataFrame:
    """
    Load OOF predictions and optionally merge with actual returns
    
    Parameters
    ----------
    predictions_path : str | Path
        Path to predictions CSV
    years : List[int] | None
        Years to filter
    merge_actuals : bool
        Whether to merge with actual returns from CSV
    csv_path : str | Path | None
        Path to CSV with actual returns (if merge_actuals=True)
    
    Returns
    -------
    pd.DataFrame
        Predictions with date, stock_id, oof_prediction, pchg (if merged)
    """
    logger.info(f"Loading predictions from {predictions_path}")
    
    df = pd.read_csv(predictions_path)
    df['date'] = pd.to_datetime(df['date'])
    
    if years is not None:
        df = df[df['date'].dt.year.isin(years)]
    
    logger.info(f"Loaded {len(df)} predictions")
    
    # Merge with actual returns if requested
    if merge_actuals and 'pchg' not in df.columns:
        if csv_path is None:
            # Try to find CSV path automatically
            base_dir = Path(predictions_path).parent.parent.parent
            csv_path = base_dir / 'train_merged_all_with_2026.csv'
        
        if Path(csv_path).exists():
            logger.info(f"Merging with actual returns from {csv_path}")
            
            # Load actual data
            df_actual = pd.read_csv(csv_path, usecols=['date', 'Unnamed: 0', 'pchg'])
            df_actual['date'] = pd.to_datetime(df_actual['date'])
            df_actual = df_actual.rename(columns={'Unnamed: 0': 'stock_id'})
            
            # Merge
            df = df.merge(df_actual, on=['date', 'stock_id'], how='left')
            logger.info(f"Merged {len(df)} rows with actual returns")
        else:
            logger.warning(f"CSV file not found: {csv_path}, cannot merge actual returns")
    
    return df


def calculate_ic_metrics(
    predictions: pd.Series,
    actuals: pd.Series,
) -> Dict[str, float]:
    """
    Calculate IC metrics
    
    Parameters
    ----------
    predictions : pd.Series
        Predicted values
    actuals : pd.Series
        Actual values
    
    Returns
    -------
    Dict[str, float]
        IC metrics
    """
    from scipy import stats
    
    # Align indices
    common_idx = predictions.index.intersection(actuals.index)
    
    if len(common_idx) < 10:
        return {
            'ic_mean': np.nan,
            'ic_std': np.nan,
            'ic_ir': np.nan,
            'ic_positive_ratio': np.nan,
        }
    
    pred = predictions.loc[common_idx]
    actual = actuals.loc[common_idx]
    
    # Remove NaN
    valid = pred.notna() & actual.notna()
    pred = pred[valid]
    actual = actual[valid]
    
    if len(pred) < 10:
        return {
            'ic_mean': np.nan,
            'ic_std': np.nan,
            'ic_ir': np.nan,
            'ic_positive_ratio': np.nan,
        }
    
    # Calculate IC
    ic, _ = stats.spearmanr(pred, actual)
    
    return {
        'ic_mean': float(ic),
        'ic_std': 0.0,  # Single value, no std
        'ic_ir': float(ic),  # For single value, IR = IC
        'ic_positive_ratio': 1.0 if ic > 0 else 0.0,
    }


def calculate_ic_series(
    df: pd.DataFrame,
    pred_col: str = 'oof_prediction',
    actual_col: str = 'pchg',
) -> pd.Series:
    """
    Calculate IC time series by date
    
    Parameters
    ----------
    df : pd.DataFrame
        Data with date, pred_col, actual_col
    pred_col : str
        Prediction column name
    actual_col : str
        Actual column name
    
    Returns
    -------
    pd.Series
        IC series indexed by date
    """
    from scipy import stats
    
    ic_list = []
    
    for date in sorted(df['date'].unique()):
        df_date = df[df['date'] == date]
        
        valid = df_date[pred_col].notna() & df_date[actual_col].notna()
        
        if valid.sum() < 10:
            continue
        
        pred = df_date.loc[valid, pred_col]
        actual = df_date.loc[valid, actual_col]
        
        ic, _ = stats.spearmanr(pred, actual)
        
        if np.isfinite(ic):
            ic_list.append({'date': date, 'ic': ic})
    
    if not ic_list:
        return pd.Series(dtype=float)
    
    ic_df = pd.DataFrame(ic_list).set_index('date')
    return ic_df['ic']


def calculate_portfolio_metrics(
    df: pd.DataFrame,
    pred_col: str = 'oof_prediction',
    actual_col: str = 'pchg',
    n_stocks: int = 50,
    transaction_cost: float = 0.002,
) -> Dict[str, float]:
    """
    Calculate portfolio performance metrics
    
    Parameters
    ----------
    df : pd.DataFrame
        Data with date, stock_id, pred_col, actual_col
    pred_col : str
        Prediction column
    actual_col : str
        Actual return column
    n_stocks : int
        Number of stocks in portfolio
    transaction_cost : float
        One-way transaction cost
    
    Returns
    -------
    Dict[str, float]
        Portfolio metrics
    """
    # Simulate top-N portfolio
    def simulate_top_n(group):
        top_n = group.nlargest(n_stocks, pred_col)
        return top_n[actual_col].mean()
    
    portfolio_returns = df.groupby('date').apply(simulate_top_n)
    market_returns = df.groupby('date')[actual_col].mean()
    
    # Calculate metrics
    n_periods = len(portfolio_returns)
    
    if n_periods == 0:
        return {
            'ytd_return': np.nan,
            'annual_return': np.nan,
            'annual_vol': np.nan,
            'sharpe': np.nan,
            'ytd_excess': np.nan,
            'annual_excess': np.nan,
        }
    
    # Cumulative returns
    port_cum = (1 + portfolio_returns).prod()
    mkt_cum = (1 + market_returns).prod()
    
    # YTD returns
    ytd_port = (port_cum - 1) * 100
    ytd_mkt = (mkt_cum - 1) * 100
    
    # Annualize
    date_range = portfolio_returns.index.max() - portfolio_returns.index.min()
    n_days = date_range.days
    
    if n_days > 0:
        ann_port = ((port_cum) ** (365.25 / n_days) - 1) * 100
        ann_mkt = ((mkt_cum) ** (365.25 / n_days) - 1) * 100
    else:
        ann_port = 0
        ann_mkt = 0
    
    # Volatility and Sharpe
    ann_vol = portfolio_returns.std() * np.sqrt(52) * 100
    sharpe = ann_port / ann_vol if ann_vol > 0 else 0
    
    return {
        'ytd_return': ytd_port,
        'annual_return': ann_port,
        'annual_vol': ann_vol,
        'sharpe': sharpe,
        'ytd_excess': ytd_port - ytd_mkt,
        'annual_excess': ann_port - ann_mkt,
    }


def save_results(
    results: Dict[str, Any],
    output_path: str | Path,
    format: str = 'json',
):
    """
    Save results to file
    
    Parameters
    ----------
    results : Dict[str, Any]
        Results to save
    output_path : str | Path
        Output file path
    format : str
        Format ('json' or 'csv')
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if format == 'json':
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
    elif format == 'csv':
        if isinstance(results, dict):
            df = pd.DataFrame([results])
        else:
            df = pd.DataFrame(results)
        df.to_csv(output_path, index=False)
    
    logger.info(f"Results saved to {output_path}")
