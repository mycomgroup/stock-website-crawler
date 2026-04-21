"""
Complete Optimization Pipeline

Runs the full optimization workflow:
1. Sensitivity Analysis
2. Grid Search (optional)
3. Portfolio Tuning
4. Overfitting Detection

Usage:
    python3 run_full_optimization.py [--quick]
    
    --quick: Run quick version (sensitivity only)
"""

import sys
import argparse
import logging
from pathlib import Path

# Add v2 to path
sys.path.insert(0, str(Path(__file__).parent))

from v2.optimization.sensitivity import SensitivityAnalyzer
from v2.optimization.grid_search import GridSearchOptimizer
from v2.optimization.portfolio_tuning import PortfolioTuner
from v2.optimization.overfitting_detection import OverfittingDetector
from v2.optimization.utils import OptimizationConfig, load_predictions

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def run_quick_optimization(config: OptimizationConfig, base_dir: Path) -> bool:
    """Run quick optimization (sensitivity only)"""
    
    logger.info("\n" + "="*80)
    logger.info("QUICK OPTIMIZATION MODE")
    logger.info("="*80)
    
    # 1. Sensitivity Analysis
    logger.info("\n【Step 1/1: Sensitivity Analysis】")
    
    analyzer = SensitivityAnalyzer(config)
    predictions_path = base_dir / 'output' / 'phase2' / 'oof_predictions_phase2.csv'
    
    if not predictions_path.exists():
        logger.error(f"Predictions file not found: {predictions_path}")
        return False
    
    df_results = analyzer.run_all_scans(predictions_path)
    analysis = analyzer.analyze_results(df_results)
    analyzer.generate_plots(df_results)
    analyzer.generate_report(df_results, analysis)
    
    return True


def run_full_optimization(config: OptimizationConfig, base_dir: Path) -> bool:
    """Run full optimization pipeline"""
    
    logger.info("\n" + "="*80)
    logger.info("FULL OPTIMIZATION PIPELINE")
    logger.info("="*80)
    
    predictions_path = base_dir / 'output' / 'phase2' / 'oof_predictions_phase2.csv'
    
    if not predictions_path.exists():
        logger.error(f"Predictions file not found: {predictions_path}")
        return False
    
    # Load predictions
    predictions_df = load_predictions(predictions_path)
    
    # 1. Sensitivity Analysis
    logger.info("\n【Step 1/4: Sensitivity Analysis】")
    
    analyzer = SensitivityAnalyzer(config)
    df_sensitivity = analyzer.run_all_scans(predictions_path)
    analysis = analyzer.analyze_results(df_sensitivity)
    analyzer.generate_plots(df_sensitivity)
    analyzer.generate_report(df_sensitivity, analysis)
    
    # 2. Grid Search (simplified)
    logger.info("\n【Step 2/4: Grid Search】")
    
    grid_search = GridSearchOptimizer(config)
    param_grid = grid_search.define_param_grid()
    df_grid = grid_search.run_walk_forward_optimization(predictions_df, param_grid)
    best_params = grid_search.select_best_params(df_grid)
    
    # 3. Portfolio Tuning
    logger.info("\n【Step 3/4: Portfolio Tuning】")
    
    tuner = PortfolioTuner(config)
    val_predictions = predictions_df[predictions_df['date'].dt.year == config.validation_year]
    df_sizes = tuner.test_holding_sizes(val_predictions)
    
    # 4. Overfitting Detection
    logger.info("\n【Step 4/4: Overfitting Detection】")
    
    detector = OverfittingDetector(config)
    
    # Load holdout predictions
    holdout_path = base_dir / 'output' / 'phase2' / 'predictions_2026_holdout.csv'
    
    if holdout_path.exists():
        holdout_predictions = load_predictions(holdout_path, years=[config.holdout_year])
        
        oos_result = detector.test_oos_decay(val_predictions, holdout_predictions)
        detector.generate_report(oos_result)
    else:
        logger.warning(f"Holdout predictions not found: {holdout_path}")
        logger.warning("Skipping overfitting detection")
    
    return True


def main():
    """Main function"""
    
    parser = argparse.ArgumentParser(description='Run optimization pipeline')
    parser.add_argument('--quick', action='store_true', help='Run quick mode (sensitivity only)')
    args = parser.parse_args()
    
    try:
        logger.info("="*80)
        logger.info("Strategy Optimization Pipeline")
        logger.info("="*80)
        
        # Load configuration
        base_dir = Path(__file__).parent
        phase2_snapshot = base_dir / 'output' / 'phase2' / 'run_snapshot_phase2.json'
        
        if phase2_snapshot.exists():
            config = OptimizationConfig.from_phase2(phase2_snapshot)
            logger.info("Loaded configuration from Phase 2")
        else:
            config = OptimizationConfig()
            logger.info("Using default configuration")
        
        logger.info(f"\nConfiguration:")
        logger.info(f"  Validation Year: {config.validation_year}")
        logger.info(f"  Holdout Year: {config.holdout_year}")
        logger.info(f"  Output Directory: {config.output_dir}")
        
        # Run optimization
        if args.quick:
            success = run_quick_optimization(config, base_dir)
        else:
            success = run_full_optimization(config, base_dir)
        
        if success:
            logger.info("\n" + "="*80)
            logger.info("✅ Optimization Pipeline Complete!")
            logger.info("="*80)
            logger.info(f"\nResults saved to: {config.output_dir}")
            logger.info("\nNext steps:")
            logger.info("  1. Review sensitivity analysis results")
            logger.info("  2. Check overfitting detection report")
            logger.info("  3. Select optimal parameters")
            logger.info("  4. Re-train model with optimal parameters")
            logger.info("  5. Validate on 2026 holdout")
        
        return success
        
    except Exception as e:
        logger.error(f"Optimization pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
