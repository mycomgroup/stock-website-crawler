# Strategy Optimization Module

Complete parameter optimization framework with overfitting prevention.

## Overview

This module provides tools for optimizing strategy parameters while preventing overfitting:

- **Sensitivity Analysis**: Understand parameter impact
- **Grid Search**: Find optimal parameter combinations
- **Portfolio Tuning**: Optimize portfolio construction
- **Overfitting Detection**: Validate results

## Quick Start

### 1. Run Sensitivity Analysis (Recommended First Step)

```bash
cd skills/autoresearch_ml_joinquant_factor_v2
python3 run_sensitivity_analysis.py
```

This will:
- Test each parameter independently
- Generate sensitivity plots
- Identify most important parameters
- Provide optimization recommendations

**Output**: `output/optimization/sensitivity/`

### 2. Run Full Optimization Pipeline

```bash
# Quick mode (sensitivity only)
python3 run_full_optimization.py --quick

# Full mode (all steps)
python3 run_full_optimization.py
```

**Output**: `output/optimization/`

## Module Structure

```
v2/optimization/
├── __init__.py                 # Module exports
├── utils.py                    # Utilities and config
├── sensitivity.py              # Sensitivity analysis
├── grid_search.py              # Grid search with walk-forward
├── portfolio_tuning.py         # Portfolio construction tuning
├── overfitting_detection.py   # Overfitting tests
└── README.md                   # This file
```

## Usage Examples

### Sensitivity Analysis

```python
from v2.optimization import SensitivityAnalyzer, OptimizationConfig

# Create config
config = OptimizationConfig.from_phase2('output/phase2/run_snapshot_phase2.json')

# Run analysis
analyzer = SensitivityAnalyzer(config)
results = analyzer.run_all_scans('output/phase2/oof_predictions_phase2.csv')
analysis = analyzer.analyze_results(results)
analyzer.generate_plots(results)
analyzer.generate_report(results, analysis)
```

### Grid Search

```python
from v2.optimization import GridSearchOptimizer

optimizer = GridSearchOptimizer(config)
param_grid = {
    'n_stocks': [40, 50, 60],
    'max_turnover': [0.25, 0.3, 0.35],
}
results = optimizer.run_walk_forward_optimization(predictions_df, param_grid)
best_params = optimizer.select_best_params(results)
```

### Overfitting Detection

```python
from v2.optimization import OverfittingDetector

detector = OverfittingDetector(config)
oos_result = detector.test_oos_decay(val_predictions, holdout_predictions)
detector.generate_report(oos_result)
```

## Configuration

### OptimizationConfig

```python
@dataclass
class OptimizationConfig:
    # Data paths
    csv_path: str = "train_merged_all_with_2026.csv"
    output_dir: str = "output/optimization"
    
    # Time periods
    train_start_year: int = 2015
    train_end_year: int = 2024
    validation_year: int = 2025
    holdout_year: int = 2026
    
    # Base parameters (from Phase 2)
    n_stocks: int = 50
    max_single_weight: float = 0.03
    max_turnover: float = 0.3
    # ... more parameters
```

## Overfitting Prevention

### Data Split Strategy

```
Training:   2015-2024  (used for optimization)
Validation: 2025       (used for parameter selection)
Holdout:    2026       (final test, never touched during optimization)
```

### Overfitting Tests

1. **Out-of-Sample Decay Test**
   - Compare validation vs holdout performance
   - Decay < 20%: PASS
   - Decay 20-40%: WARNING
   - Decay > 40%: FAIL

2. **Parameter Stability Test**
   - Check if optimal parameters are consistent across time windows
   - High CV indicates instability

3. **Bootstrap Validation** (future)
   - Test robustness through resampling

## Integration with Existing v2 Infrastructure

This module integrates with:

- `v2/validation/walk_forward.py`: Walk-forward validation framework
- `v2/evaluation/metrics.py`: Evaluation metrics
- `v2/portfolio/optimizer.py`: Portfolio optimization
- `v2/evaluation/bootstrap.py`: Bootstrap testing

## Output Files

### Sensitivity Analysis

```
output/optimization/sensitivity/
├── sensitivity_results.csv      # Raw results
├── sensitivity_analysis.json    # Analysis summary
├── sensitivity_report.txt       # Text report
└── plots/
    ├── n_stocks_sensitivity.png
    ├── max_turnover_sensitivity.png
    └── ...
```

### Grid Search

```
output/optimization/grid_search/
└── grid_search_results.csv
```

### Overfitting Detection

```
output/optimization/overfitting/
└── overfitting_report.txt
```

## Best Practices

### 1. Always Start with Sensitivity Analysis

Understand which parameters matter before optimizing.

### 2. Use Validation Set for Parameter Selection

Never use holdout set for optimization decisions.

### 3. Check Overfitting After Optimization

Always validate on holdout set and check decay.

### 4. Document All Decisions

Keep track of why you chose certain parameters.

### 5. Be Conservative

When in doubt, choose simpler/more stable parameters.

## Troubleshooting

### Issue: "Predictions file not found"

**Solution**: Run Phase 2 training first:
```bash
python3 run_phase2.py
```

### Issue: "Insufficient data"

**Solution**: Check that you have data for validation and holdout years.

### Issue: "High overfitting detected"

**Solution**: 
1. Use fewer parameters
2. Increase regularization
3. Use more training data
4. Simplify model

## Future Enhancements

- [ ] Bootstrap validation
- [ ] Parameter stability across windows
- [ ] Automated parameter selection
- [ ] Multi-objective optimization
- [ ] Real-time monitoring

## References

- Walk-Forward Validation: `v2/validation/walk_forward.py`
- Evaluation Metrics: `v2/evaluation/metrics.py`
- Portfolio Optimization: `v2/portfolio/optimizer.py`

## Support

For issues or questions, check:
1. This README
2. `OPTIMIZATION_PLAN.md` in project root
3. Existing v2 module documentation
