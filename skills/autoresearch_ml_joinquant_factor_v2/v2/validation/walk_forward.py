"""OOF Walk-Forward validation framework (Task 4.1-4.5).

This module implements the nested walk-forward validation framework for the weak factor
portfolio strategy, ensuring strict time causality and preventing data leakage.

Components:
- WalkForwardSplitter: Outer loop for generating train/test splits with embargo
- InnerLoopTuner: Hyperparameter selection inside outer-train using inner CV
- smooth_hyperparams: Exponential smoothing of hyperparameters across windows
- OOFPredictor: Ensures each (date, stock) has exactly one OOF prediction
- FinalHoldoutPartition: Freeze last 52-104 weeks for final validation

Corresponds to:
- Requirements: Requirement 9 (Nested OOF Walk-Forward Validation)
- Design: Section 6 (OOF Walk-Forward Design)
- Tasks: 4.1-4.5
"""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Task 4.1: WalkForwardSplitter — Outer loop
# ---------------------------------------------------------------------------

@dataclass
class WalkForwardSplit:
    """A single walk-forward split containing train/test/embargo date ranges.
    
    Attributes
    ----------
    train_dates : list
        Sorted list of training dates.
    test_dates : list
        Sorted list of test dates.
    embargo_dates : list
        Dates excluded between train end and test start (embargo period).
    """
    train_dates: list
    test_dates: list
    embargo_dates: list = field(default_factory=list)
    
    def __repr__(self) -> str:
        return (
            f"WalkForwardSplit(train={len(self.train_dates)} dates, "
            f"test={len(self.test_dates)} dates, embargo={len(self.embargo_dates)} dates)"
        )


class WalkForwardSplitter:
    """Generate walk-forward splits with embargo for outer loop validation.
    
    Parameters
    ----------
    min_train_periods : int, default=260
        Minimum number of periods (weeks) required for training.
        Default 260 weeks ≈ 5 years (conservative config for current project).
    test_block : int, default=52
        Number of periods (weeks) in each test block.
        Default 52 weeks ≈ 1 year.
    step : int, default=4
        Number of periods to advance between consecutive splits.
        Default 4 weeks = monthly rebalancing.
    embargo : int, default=1
        Number of periods to exclude between train end and test start.
        Prevents label overlap leakage.
        
    Notes
    -----
    - All periods are in weeks for the current project (weekly rebalancing).
    - Embargo must be >= max(label_horizon, execution_delay, feature_publication_lag).
    - The splitter uses expanding window by default (train window grows over time).
    """
    
    def __init__(
        self,
        min_train_periods: int = 260,
        test_block: int = 52,
        step: int = 4,
        embargo: int = 1,
    ):
        if min_train_periods < 1:
            raise ValueError(f"min_train_periods must be >= 1, got {min_train_periods}")
        if test_block < 1:
            raise ValueError(f"test_block must be >= 1, got {test_block}")
        if step < 1:
            raise ValueError(f"step must be >= 1, got {step}")
        if embargo < 0:
            raise ValueError(f"embargo must be >= 0, got {embargo}")
            
        self.min_train_periods = min_train_periods
        self.test_block = test_block
        self.step = step
        self.embargo = embargo
        
        logger.debug(
            "WalkForwardSplitter initialized: min_train=%d, test_block=%d, "
            "step=%d, embargo=%d",
            min_train_periods, test_block, step, embargo,
        )
    
    def split(self, dates: Sequence) -> list[WalkForwardSplit]:
        """Generate walk-forward splits from a sorted list of dates.
        
        Parameters
        ----------
        dates : Sequence
            Sorted list/array of unique dates (datetime or comparable).
            
        Returns
        -------
        list[WalkForwardSplit]
            List of walk-forward splits, each containing train/test/embargo dates.
            
        Raises
        ------
        ValueError
            If dates is empty or has insufficient length for min_train_periods.
        """
        if len(dates) == 0:
            raise ValueError("dates cannot be empty")
            
        # Convert to sorted list if needed
        dates_sorted = sorted(set(dates))
        n_dates = len(dates_sorted)
        
        if n_dates < self.min_train_periods + self.embargo + 1:
            raise ValueError(
                f"Insufficient dates: need at least {self.min_train_periods + self.embargo + 1} "
                f"(min_train={self.min_train_periods} + embargo={self.embargo} + 1), "
                f"got {n_dates}"
            )
        
        splits: list[WalkForwardSplit] = []
        
        # Start from min_train_periods
        train_end_idx = self.min_train_periods - 1
        
        while True:
            # Embargo period: [train_end_idx + 1, train_end_idx + embargo]
            embargo_start_idx = train_end_idx + 1
            embargo_end_idx = train_end_idx + self.embargo
            
            # Test period: [embargo_end_idx + 1, embargo_end_idx + test_block]
            test_start_idx = embargo_end_idx + 1
            test_end_idx = test_start_idx + self.test_block - 1
            
            # Check if we have enough data for test block
            if test_end_idx >= n_dates:
                logger.debug(
                    "WalkForwardSplitter.split: reached end of data at train_end_idx=%d, "
                    "generated %d splits",
                    train_end_idx, len(splits),
                )
                break
            
            # Extract date ranges
            train_dates = dates_sorted[:train_end_idx + 1]
            embargo_dates = (
                dates_sorted[embargo_start_idx:embargo_end_idx + 1]
                if self.embargo > 0
                else []
            )
            test_dates = dates_sorted[test_start_idx:test_end_idx + 1]
            
            split = WalkForwardSplit(
                train_dates=train_dates,
                test_dates=test_dates,
                embargo_dates=embargo_dates,
            )
            splits.append(split)
            
            logger.debug(
                "WalkForwardSplitter.split: created split %d, train=%d dates [%s to %s], "
                "embargo=%d dates, test=%d dates [%s to %s]",
                len(splits),
                len(train_dates), train_dates[0], train_dates[-1],
                len(embargo_dates),
                len(test_dates), test_dates[0], test_dates[-1],
            )
            
            # Advance by step
            train_end_idx += self.step
        
        logger.info(
            "WalkForwardSplitter.split: generated %d splits from %d dates",
            len(splits), n_dates,
        )
        
        return splits


# ---------------------------------------------------------------------------
# Task 4.2: InnerLoopTuner — Hyperparameter selection inside outer-train
# ---------------------------------------------------------------------------

class InnerLoopTuner:
    """Hyperparameter selection using inner loop cross-validation.
    
    Runs inside each outer-train window to select best hyperparameters without
    using outer-test information.
    
    Parameters
    ----------
    validation_block : int, default=13
        Number of periods (weeks) in each inner validation block.
        Default 13 weeks ≈ 1 quarter.
    window_type : {"expanding", "rolling"}, default="expanding"
        - "expanding": train window grows over time (for slow-decay factors).
        - "rolling": train window has fixed size (for fast-decay factors).
    min_inner_train : int, default=52
        Minimum number of periods for inner train window (only used in rolling mode).
        Default 52 weeks ≈ 1 year.
    """
    
    def __init__(
        self,
        validation_block: int = 13,
        window_type: str = "expanding",
        min_inner_train: int = 52,
    ):
        if validation_block < 1:
            raise ValueError(f"validation_block must be >= 1, got {validation_block}")
        if window_type not in ("expanding", "rolling"):
            raise ValueError(f"window_type must be 'expanding' or 'rolling', got {window_type}")
        if min_inner_train < 1:
            raise ValueError(f"min_inner_train must be >= 1, got {min_inner_train}")
            
        self.validation_block = validation_block
        self.window_type = window_type
        self.min_inner_train = min_inner_train
        
        logger.debug(
            "InnerLoopTuner initialized: validation_block=%d, window_type=%s, "
            "min_inner_train=%d",
            validation_block, window_type, min_inner_train,
        )
    
    def tune(
        self,
        dates: Sequence,
        model_fn: Callable,
        param_grid: dict[str, list],
        score_fn: Callable,
    ) -> dict[str, Any]:
        """Select best hyperparameters using inner loop CV.
        
        Parameters
        ----------
        dates : Sequence
            Sorted list of dates in the outer-train window.
        model_fn : Callable
            Function that takes (train_data, **params) and returns a fitted model.
            Signature: model_fn(train_dates, **params) -> model
        param_grid : dict[str, list]
            Dictionary mapping parameter names to lists of candidate values.
            Example: {"alpha": [0.001, 0.01, 0.1], "l1_ratio": [0.0, 0.1]}
        score_fn : Callable
            Function that takes (model, val_dates) and returns a score (higher is better).
            Signature: score_fn(model, val_dates) -> float
            
        Returns
        -------
        dict[str, Any]
            Best hyperparameters found by inner loop CV.
            
        Raises
        ------
        ValueError
            If dates is empty or param_grid is empty.
        """
        if len(dates) == 0:
            raise ValueError("dates cannot be empty")
        if not param_grid:
            raise ValueError("param_grid cannot be empty")
            
        dates_sorted = sorted(set(dates))
        n_dates = len(dates_sorted)
        
        # Generate inner splits
        inner_splits = self._generate_inner_splits(dates_sorted)
        
        if len(inner_splits) == 0:
            logger.warning(
                "InnerLoopTuner.tune: no inner splits generated (insufficient data), "
                "returning first param combination"
            )
            # Return first combination as fallback
            return {k: v[0] for k, v in param_grid.items()}
        
        logger.info(
            "InnerLoopTuner.tune: generated %d inner splits from %d dates",
            len(inner_splits), n_dates,
        )
        
        # Generate all parameter combinations
        param_combinations = self._generate_param_combinations(param_grid)
        
        logger.info(
            "InnerLoopTuner.tune: evaluating %d parameter combinations",
            len(param_combinations),
        )
        
        # Evaluate each combination
        best_score = -np.inf
        best_params = param_combinations[0]
        
        for params in param_combinations:
            scores = []
            
            for split in inner_splits:
                try:
                    # Fit model on inner train
                    model = model_fn(split.train_dates, **params)
                    
                    # Evaluate on inner validation
                    score = score_fn(model, split.test_dates)
                    
                    if np.isfinite(score):
                        scores.append(score)
                except Exception as e:  # pylint: disable=broad-except
                    logger.warning(
                        "InnerLoopTuner.tune: error evaluating params %s on split: %s",
                        params, e,
                    )
                    continue
            
            if len(scores) == 0:
                logger.warning(
                    "InnerLoopTuner.tune: no valid scores for params %s, skipping",
                    params,
                )
                continue
            
            avg_score = float(np.mean(scores))
            
            logger.debug(
                "InnerLoopTuner.tune: params=%s, avg_score=%.6f (from %d folds)",
                params, avg_score, len(scores),
            )
            
            if avg_score > best_score:
                best_score = avg_score
                best_params = params
        
        logger.info(
            "InnerLoopTuner.tune: best params=%s, best_score=%.6f",
            best_params, best_score,
        )
        
        return best_params
    
    def _generate_inner_splits(self, dates: list) -> list[WalkForwardSplit]:
        """Generate inner CV splits from outer-train dates."""
        n_dates = len(dates)
        splits = []
        
        if self.window_type == "expanding":
            # Expanding window: start from min_inner_train
            train_end_idx = self.min_inner_train - 1
        else:
            # Rolling window: fixed train size = min_inner_train
            train_end_idx = self.min_inner_train - 1
        
        while True:
            val_start_idx = train_end_idx + 1
            val_end_idx = val_start_idx + self.validation_block - 1
            
            if val_end_idx >= n_dates:
                break
            
            if self.window_type == "expanding":
                train_dates = dates[:train_end_idx + 1]
            else:
                # Rolling: keep train window size fixed
                train_start_idx = max(0, train_end_idx - self.min_inner_train + 1)
                train_dates = dates[train_start_idx:train_end_idx + 1]
            
            val_dates = dates[val_start_idx:val_end_idx + 1]
            
            split = WalkForwardSplit(
                train_dates=train_dates,
                test_dates=val_dates,
                embargo_dates=[],  # No embargo in inner loop (already handled in outer)
            )
            splits.append(split)
            
            # Advance by validation_block
            train_end_idx += self.validation_block
        
        return splits
    
    @staticmethod
    def _generate_param_combinations(param_grid: dict[str, list]) -> list[dict[str, Any]]:
        """Generate all combinations of parameters from grid."""
        keys = list(param_grid.keys())
        values = [param_grid[k] for k in keys]
        
        # Cartesian product
        combinations = []
        
        def _recurse(idx: int, current: dict):
            if idx == len(keys):
                combinations.append(current.copy())
                return
            
            key = keys[idx]
            for val in values[idx]:
                current[key] = val
                _recurse(idx + 1, current)
        
        _recurse(0, {})
        return combinations


# ---------------------------------------------------------------------------
# Task 4.3: smooth_hyperparams — Exponential smoothing of hyperparameters
# ---------------------------------------------------------------------------

def smooth_hyperparams(
    current_params: dict[str, float],
    prev_params: dict[str, float] | None,
    alpha: float = 0.3,
) -> dict[str, float]:
    """Apply exponential smoothing to hyperparameters across windows.
    
    Formula: θ_t = alpha * θ_t_star + (1 - alpha) * θ_{t-1}
    
    This prevents hyperparameters from jumping wildly between consecutive windows,
    improving stability and reducing overfitting to recent data.
    
    Parameters
    ----------
    current_params : dict[str, float]
        Hyperparameters selected by inner loop for current window (θ_t_star).
    prev_params : dict[str, float] or None
        Hyperparameters from previous window (θ_{t-1}).
        If None (first window), returns current_params unchanged.
    alpha : float, default=0.3
        Smoothing factor in [0, 1].
        - alpha=1.0: no smoothing (use current_params as-is).
        - alpha=0.0: full smoothing (use prev_params as-is).
        - alpha=0.3: 30% current + 70% previous (recommended default).
        
    Returns
    -------
    dict[str, float]
        Smoothed hyperparameters (θ_t).
        
    Notes
    -----
    - Only numeric parameters are smoothed. Non-numeric parameters (e.g., strings)
      are taken from current_params without smoothing.
    - Causal constraint: only uses current and past windows, never future windows.
    """
    if not 0.0 <= alpha <= 1.0:
        raise ValueError(f"alpha must be in [0, 1], got {alpha}")
    
    if prev_params is None:
        logger.debug("smooth_hyperparams: first window, no smoothing applied")
        return current_params.copy()
    
    smoothed = {}
    
    for key, current_val in current_params.items():
        if key not in prev_params:
            # New parameter, no smoothing
            smoothed[key] = current_val
            logger.debug(
                "smooth_hyperparams: param '%s' not in prev_params, using current value",
                key,
            )
            continue
        
        prev_val = prev_params[key]
        
        # Only smooth numeric parameters
        if isinstance(current_val, (int, float)) and isinstance(prev_val, (int, float)):
            smoothed_val = alpha * current_val + (1 - alpha) * prev_val
            smoothed[key] = smoothed_val
            
            logger.debug(
                "smooth_hyperparams: param '%s': current=%.6f, prev=%.6f, "
                "smoothed=%.6f (alpha=%.2f)",
                key, current_val, prev_val, smoothed_val, alpha,
            )
        else:
            # Non-numeric, use current value
            smoothed[key] = current_val
            logger.debug(
                "smooth_hyperparams: param '%s' is non-numeric, using current value",
                key,
            )
    
    return smoothed


# ---------------------------------------------------------------------------
# Task 4.4: OOFPredictor — Ensures each (date, stock) has exactly one OOF prediction
# ---------------------------------------------------------------------------

class OOFPredictor:
    """Ensures each (date, stock) has exactly one out-of-fold (OOF) prediction.
    
    Uses WalkForwardSplitter to generate splits, fits model on train, predicts on test,
    and assembles predictions into a single Series indexed by (date, stock_id).
    
    Parameters
    ----------
    splitter : WalkForwardSplitter
        Walk-forward splitter for generating train/test splits.
    """
    
    def __init__(self, splitter: WalkForwardSplitter):
        self.splitter = splitter
        logger.debug("OOFPredictor initialized with splitter: %s", splitter)
    
    def predict(
        self,
        df: pd.DataFrame,
        model_fn: Callable,
        **model_kwargs,
    ) -> pd.Series:
        """Generate OOF predictions for all (date, stock) pairs.
        
        Parameters
        ----------
        df : pd.DataFrame
            Panel data with columns: date, stock_id, and features.
            Must be sorted by [date, stock_id].
        model_fn : Callable
            Function that takes (train_df, **kwargs) and returns a fitted model.
            The model must have a predict(test_df) method.
            Signature: model_fn(train_df, **kwargs) -> model
        **model_kwargs
            Additional keyword arguments passed to model_fn.
            
        Returns
        -------
        pd.Series
            OOF predictions indexed by (date, stock_id).
            Each (date, stock) pair appears exactly once.
            
        Raises
        ------
        ValueError
            If df is empty or missing required columns.
        """
        if df.empty:
            raise ValueError("df cannot be empty")
        if "date" not in df.columns or "stock_id" not in df.columns:
            raise ValueError("df must contain 'date' and 'stock_id' columns")
        
        # Get unique dates
        dates = sorted(df["date"].unique())
        
        # Generate splits
        splits = self.splitter.split(dates)
        
        logger.info(
            "OOFPredictor.predict: generated %d splits from %d dates",
            len(splits), len(dates),
        )
        
        # Collect predictions
        oof_predictions = []
        
        for i, split in enumerate(splits):
            logger.debug(
                "OOFPredictor.predict: processing split %d/%d, train=%d dates, test=%d dates",
                i + 1, len(splits), len(split.train_dates), len(split.test_dates),
            )
            
            # Extract train and test data
            train_df = df[df["date"].isin(split.train_dates)]
            test_df = df[df["date"].isin(split.test_dates)]
            
            if train_df.empty:
                logger.warning(
                    "OOFPredictor.predict: split %d has empty train data, skipping",
                    i + 1,
                )
                continue
            
            if test_df.empty:
                logger.warning(
                    "OOFPredictor.predict: split %d has empty test data, skipping",
                    i + 1,
                )
                continue
            
            try:
                # Fit model on train
                model = model_fn(train_df, **model_kwargs)
                
                # Predict on test
                predictions = model.predict(test_df)
                
                # Store predictions with (date, stock_id) index
                pred_series = pd.Series(
                    predictions,
                    index=pd.MultiIndex.from_frame(
                        test_df[["date", "stock_id"]],
                        names=["date", "stock_id"],
                    ),
                )
                oof_predictions.append(pred_series)
                
                logger.debug(
                    "OOFPredictor.predict: split %d generated %d predictions",
                    i + 1, len(pred_series),
                )
            except Exception as e:  # pylint: disable=broad-except
                logger.error(
                    "OOFPredictor.predict: error processing split %d: %s",
                    i + 1, e,
                )
                continue
        
        if len(oof_predictions) == 0:
            logger.warning("OOFPredictor.predict: no predictions generated")
            return pd.Series(dtype=float)
        
        # Concatenate all predictions
        oof_series = pd.concat(oof_predictions)
        
        # Validate: no duplicate predictions
        if oof_series.index.duplicated().any():
            n_duplicates = oof_series.index.duplicated().sum()
            warnings.warn(
                f"OOFPredictor.predict: found {n_duplicates} duplicate (date, stock_id) pairs. "
                "This violates the OOF guarantee. Keeping first occurrence.",
                UserWarning,
                stacklevel=2,
            )
            oof_series = oof_series[~oof_series.index.duplicated(keep="first")]
        
        logger.info(
            "OOFPredictor.predict: generated %d OOF predictions (no duplicates)",
            len(oof_series),
        )
        
        return oof_series


# ---------------------------------------------------------------------------
# Task 4.5: FinalHoldoutPartition — Freeze last 52-104 weeks
# ---------------------------------------------------------------------------

class FinalHoldoutPartition:
    """Freeze last 52-104 weeks for final validation.
    
    Tracks access count and warns if accessed more than once to prevent data snooping.
    
    Parameters
    ----------
    holdout_periods : int, default=52
        Number of periods (weeks) to freeze for final holdout.
        Default 52 weeks ≈ 1 year.
        Recommended range: 52-104 weeks (1-2 years).
    """
    
    def __init__(self, holdout_periods: int = 52):
        if holdout_periods < 1:
            raise ValueError(f"holdout_periods must be >= 1, got {holdout_periods}")
        
        self.holdout_periods = holdout_periods
        self._access_count = 0
        
        logger.debug(
            "FinalHoldoutPartition initialized: holdout_periods=%d",
            holdout_periods,
        )
    
    def get_holdout_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Get holdout slice and increment access counter.
        
        Parameters
        ----------
        df : pd.DataFrame
            Panel data with 'date' column, sorted by date.
            
        Returns
        -------
        pd.DataFrame
            Holdout slice (last holdout_periods dates).
            
        Warns
        -----
        UserWarning
            If accessed more than once (data snooping risk).
        """
        self._access_count += 1
        
        if self._access_count > 1:
            warnings.warn(
                f"FinalHoldoutPartition.get_holdout_data: accessed {self._access_count} times. "
                "Accessing final holdout more than once increases data snooping risk. "
                "Consider using research OOS for iterative development.",
                UserWarning,
                stacklevel=2,
            )
            logger.warning(
                "FinalHoldoutPartition.get_holdout_data: access count=%d (> 1), "
                "data snooping risk",
                self._access_count,
            )
        
        dates = sorted(df["date"].unique())
        
        if len(dates) < self.holdout_periods:
            logger.warning(
                "FinalHoldoutPartition.get_holdout_data: insufficient dates (%d < %d), "
                "returning all data",
                len(dates), self.holdout_periods,
            )
            return df
        
        holdout_dates = dates[-self.holdout_periods:]
        holdout_df = df[df["date"].isin(holdout_dates)]
        
        logger.info(
            "FinalHoldoutPartition.get_holdout_data: returning %d rows from %d dates "
            "(access_count=%d)",
            len(holdout_df), len(holdout_dates), self._access_count,
        )
        
        return holdout_df
    
    def get_research_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Get non-holdout slice (research OOS + train).
        
        Parameters
        ----------
        df : pd.DataFrame
            Panel data with 'date' column, sorted by date.
            
        Returns
        -------
        pd.DataFrame
            Non-holdout slice (all dates except last holdout_periods).
        """
        dates = sorted(df["date"].unique())
        
        if len(dates) < self.holdout_periods:
            logger.warning(
                "FinalHoldoutPartition.get_research_data: insufficient dates (%d < %d), "
                "returning empty DataFrame",
                len(dates), self.holdout_periods,
            )
            return df.iloc[:0]
        
        research_dates = dates[:-self.holdout_periods]
        research_df = df[df["date"].isin(research_dates)]
        
        logger.info(
            "FinalHoldoutPartition.get_research_data: returning %d rows from %d dates",
            len(research_df), len(research_dates),
        )
        
        return research_df
    
    @property
    def access_count(self) -> int:
        """Number of times get_holdout_data has been called."""
        return self._access_count
