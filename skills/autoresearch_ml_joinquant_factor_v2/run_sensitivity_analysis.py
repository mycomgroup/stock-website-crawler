"""
Run Parameter Sensitivity Analysis

Usage:
    python3 run_sensitivity_analysis.py
"""

import sys
import logging
from pathlib import Path

# Add v2 to path
sys.path.insert(0, str(Path(__file__).parent))

from v2.optimization.sensitivity import SensitivityAnalyzer
from v2.optimization.utils import OptimizationConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function"""
    
    try:
        logger.info("="*80)
        logger.info("Parameter Sensitivity Analysis")
        logger.info("="*80)
        
        # Load configuration from Phase 2
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
        logger.info(f"  Base n_stocks: {config.n_stocks}")
        logger.info(f"  Base max_turnover: {config.max_turnover}")
        
        # Create analyzer
        analyzer = SensitivityAnalyzer(config)
        
        # Run sensitivity analysis
        predictions_path = base_dir / 'output' / 'phase2' / 'oof_predictions_phase2.csv'
        
        if not predictions_path.exists():
            logger.error(f"Predictions file not found: {predictions_path}")
            logger.error("Please run Phase 2 training first")
            return False
        
        logger.info(f"\nUsing predictions from: {predictions_path}")
        
        # Run all scans
        df_results = analyzer.run_all_scans(predictions_path)
        
        # Analyze results
        analysis = analyzer.analyze_results(df_results)
        
        # Generate plots
        analyzer.generate_plots(df_results)
        
        # Generate report
        analyzer.generate_report(df_results, analysis)
        
        logger.info("\n" + "="*80)
        logger.info("✅ Sensitivity Analysis Complete!")
        logger.info("="*80)
        logger.info(f"\nResults saved to: {analyzer.output_dir}")
        logger.info(f"  - sensitivity_results.csv")
        logger.info(f"  - sensitivity_analysis.json")
        logger.info(f"  - sensitivity_report.txt")
        logger.info(f"  - plots/*.png")
        
        return True
        
    except Exception as e:
        logger.error(f"Sensitivity analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
