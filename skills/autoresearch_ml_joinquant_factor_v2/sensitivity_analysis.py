"""
参数敏感性分析

目标: 了解每个参数对策略表现的影响，识别关键参数

方法: 单参数扫描 - 固定其他参数，只改变一个参数

验证: 2015-2024训练，2025验证，2026保留作为最终holdout
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / 'output' / 'optimization'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class SensitivityAnalyzer:
    """参数敏感性分析器"""
    
    def __init__(self):
        self.base_config = self._load_base_config()
        self.results = []
        
    def _load_base_config(self) -> Dict:
        """加载基准配置（Phase 2的配置）"""
        snapshot_path = BASE_DIR / 'output' / 'phase2' / 'run_snapshot_phase2.json'
        
        with open(snapshot_path, 'r') as f:
            snapshot = json.load(f)
        
        return snapshot['config']
    
    def define_param_ranges(self) -> Dict[str, List]:
        """定义参数扫描范围"""
        
        return {
            # 组合构建参数（最重要）
            'n_stocks': [30, 40, 50, 60, 80, 100],
            'max_single_weight': [0.02, 0.025, 0.03, 0.04, 0.05],
            'max_turnover': [0.2, 0.25, 0.3, 0.35, 0.4],
            
            # 因子合成参数
            'max_single_family_weight': [0.3, 0.35, 0.4, 0.45, 0.5],
            'weight_smoothing_halflife': [2, 3, 4, 5, 6, 8],
            
            # 因子处理参数
            'mad_multiplier': [3.0, 4.0, 5.0, 6.0, 7.0],
            'new_stock_cooldown_days': [30, 45, 60, 90, 120],
            
            # 回测参数
            'test_block': [26, 39, 52, 65],  # 半年、9个月、1年、1.25年
            'step': [2, 4, 6, 8],  # 滚动步长
        }
    
    def run_single_param_scan(self, param_name: str, param_values: List) -> List[Dict]:
        """运行单参数扫描"""
        
        logger.info(f"\n{'='*80}")
        logger.info(f"扫描参数: {param_name}")
        logger.info(f"测试值: {param_values}")
        logger.info(f"{'='*80}")
        
        results = []
        
        for i, param_value in enumerate(param_values):
            logger.info(f"\n[{i+1}/{len(param_values)}] 测试 {param_name} = {param_value}")
            
            try:
                # 创建配置
                config = self.base_config.copy()
                config[param_name] = param_value
                
                # 运行回测（这里需要调用实际的pipeline）
                # 为了演示，我们先用模拟数据
                metrics = self._run_backtest_with_config(config)
                
                result = {
                    'param_name': param_name,
                    'param_value': param_value,
                    'timestamp': datetime.now().isoformat(),
                    **metrics
                }
                
                results.append(result)
                
                logger.info(f"  IC均值: {metrics['ic_mean']:.4f}")
                logger.info(f"  IC IR: {metrics['ic_ir']:.4f}")
                logger.info(f"  年化收益: {metrics['annual_return']:.2f}%")
                logger.info(f"  夏普比率: {metrics['sharpe']:.2f}")
                
            except Exception as e:
                logger.error(f"  测试失败: {e}")
                continue
        
        return results
    
    def _run_backtest_with_config(self, config: Dict) -> Dict:
        """
        使用给定配置运行回测
        
        TODO: 这里需要实际调用pipeline
        现在先返回模拟数据用于框架测试
        """
        
        # 模拟数据 - 实际使用时需要替换
        # 可以调用 v2.pipeline.Pipeline(config).run()
        
        # 这里我们从已有的预测文件中加载数据进行快速测试
        predictions_path = BASE_DIR / 'output' / 'phase2' / 'oof_predictions_phase2.csv'
        
        if predictions_path.exists():
            df = pd.read_csv(predictions_path)
            df['date'] = pd.to_datetime(df['date'])
            
            # 筛选2025年数据作为验证集
            df_2025 = df[df['date'].dt.year == 2025]
            
            if len(df_2025) > 0:
                # 计算IC
                from scipy import stats
                
                ic_series = []
                for date in df_2025['date'].unique():
                    df_date = df_2025[df_2025['date'] == date]
                    valid = df_date['oof_prediction'].notna() & df_date['pchg'].notna()
                    
                    if valid.sum() > 10:
                        corr, _ = stats.spearmanr(
                            df_date.loc[valid, 'oof_prediction'],
                            df_date.loc[valid, 'pchg']
                        )
                        if np.isfinite(corr):
                            ic_series.append(corr)
                
                ic_mean = np.mean(ic_series) if ic_series else 0
                ic_std = np.std(ic_series) if ic_series else 0
                ic_ir = ic_mean / ic_std if ic_std > 0 else 0
                
                # 模拟组合收益（简化版）
                # 实际应该根据config['n_stocks']等参数构建组合
                n_stocks = config.get('n_stocks', 50)
                
                def simulate_portfolio(group):
                    top_n = group.nlargest(n_stocks, 'oof_prediction')
                    return top_n['pchg'].mean()
                
                portfolio_returns = df_2025.groupby('date').apply(simulate_portfolio)
                
                annual_return = (1 + portfolio_returns).prod() ** (52 / len(portfolio_returns)) - 1
                annual_return *= 100
                
                annual_vol = portfolio_returns.std() * np.sqrt(52) * 100
                sharpe = annual_return / annual_vol if annual_vol > 0 else 0
                
                return {
                    'ic_mean': ic_mean,
                    'ic_std': ic_std,
                    'ic_ir': ic_ir,
                    'ic_positive_ratio': sum(ic > 0 for ic in ic_series) / len(ic_series) if ic_series else 0,
                    'annual_return': annual_return,
                    'annual_vol': annual_vol,
                    'sharpe': sharpe,
                    'n_periods': len(ic_series),
                }
        
        # 如果没有数据，返回默认值
        return {
            'ic_mean': 0.05,
            'ic_std': 0.08,
            'ic_ir': 0.625,
            'ic_positive_ratio': 0.7,
            'annual_return': 5.0,
            'annual_vol': 20.0,
            'sharpe': 0.25,
            'n_periods': 52,
        }
    
    def run_all_scans(self) -> pd.DataFrame:
        """运行所有参数的扫描"""
        
        logger.info("\n" + "="*80)
        logger.info("开始参数敏感性分析")
        logger.info("="*80)
        
        param_ranges = self.define_param_ranges()
        
        all_results = []
        
        for param_name, param_values in param_ranges.items():
            results = self.run_single_param_scan(param_name, param_values)
            all_results.extend(results)
        
        df_results = pd.DataFrame(all_results)
        
        # 保存结果
        output_path = OUTPUT_DIR / 'sensitivity_analysis.csv'
        df_results.to_csv(output_path, index=False)
        logger.info(f"\n结果已保存: {output_path}")
        
        return df_results
    
    def analyze_results(self, df_results: pd.DataFrame) -> Dict:
        """分析敏感性结果"""
        
        logger.info("\n" + "="*80)
        logger.info("分析敏感性结果")
        logger.info("="*80)
        
        analysis = {}
        
        for param_name in df_results['param_name'].unique():
            df_param = df_results[df_results['param_name'] == param_name]
            
            # 计算敏感性指标
            ic_range = df_param['ic_mean'].max() - df_param['ic_mean'].min()
            ic_cv = df_param['ic_mean'].std() / df_param['ic_mean'].mean()
            
            sharpe_range = df_param['sharpe'].max() - df_param['sharpe'].min()
            sharpe_cv = df_param['sharpe'].std() / abs(df_param['sharpe'].mean())
            
            # 找到最优值
            best_idx = df_param['ic_ir'].idxmax()
            best_value = df_param.loc[best_idx, 'param_value']
            best_ic_ir = df_param.loc[best_idx, 'ic_ir']
            
            analysis[param_name] = {
                'ic_range': ic_range,
                'ic_cv': ic_cv,
                'sharpe_range': sharpe_range,
                'sharpe_cv': sharpe_cv,
                'best_value': best_value,
                'best_ic_ir': best_ic_ir,
                'sensitivity_score': (ic_cv + sharpe_cv) / 2,  # 综合敏感性
            }
            
            logger.info(f"\n{param_name}:")
            logger.info(f"  IC变化范围: {ic_range:.4f}")
            logger.info(f"  IC变异系数: {ic_cv:.4f}")
            logger.info(f"  最优值: {best_value}")
            logger.info(f"  最优IC IR: {best_ic_ir:.4f}")
            logger.info(f"  敏感性评分: {analysis[param_name]['sensitivity_score']:.4f}")
        
        # 保存分析结果
        analysis_path = OUTPUT_DIR / 'sensitivity_summary.json'
        with open(analysis_path, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        logger.info(f"\n分析结果已保存: {analysis_path}")
        
        return analysis
    
    def generate_plots(self, df_results: pd.DataFrame):
        """生成可视化图表"""
        
        logger.info("\n生成可视化图表...")
        
        plot_dir = OUTPUT_DIR / 'sensitivity_plots'
        plot_dir.mkdir(exist_ok=True)
        
        # 设置样式
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        
        for param_name in df_results['param_name'].unique():
            df_param = df_results[df_results['param_name'] == param_name]
            
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle(f'参数敏感性分析: {param_name}', fontsize=16, fontweight='bold')
            
            # IC均值
            axes[0, 0].plot(df_param['param_value'], df_param['ic_mean'], 'o-', linewidth=2, markersize=8)
            axes[0, 0].set_xlabel(param_name)
            axes[0, 0].set_ylabel('IC Mean')
            axes[0, 0].set_title('IC均值 vs 参数值')
            axes[0, 0].grid(True, alpha=0.3)
            
            # IC IR
            axes[0, 1].plot(df_param['param_value'], df_param['ic_ir'], 'o-', linewidth=2, markersize=8, color='orange')
            axes[0, 1].set_xlabel(param_name)
            axes[0, 1].set_ylabel('IC IR')
            axes[0, 1].set_title('IC信息比率 vs 参数值')
            axes[0, 1].grid(True, alpha=0.3)
            
            # 年化收益
            axes[1, 0].plot(df_param['param_value'], df_param['annual_return'], 'o-', linewidth=2, markersize=8, color='green')
            axes[1, 0].set_xlabel(param_name)
            axes[1, 0].set_ylabel('Annual Return (%)')
            axes[1, 0].set_title('年化收益 vs 参数值')
            axes[1, 0].grid(True, alpha=0.3)
            
            # 夏普比率
            axes[1, 1].plot(df_param['param_value'], df_param['sharpe'], 'o-', linewidth=2, markersize=8, color='red')
            axes[1, 1].set_xlabel(param_name)
            axes[1, 1].set_ylabel('Sharpe Ratio')
            axes[1, 1].set_title('夏普比率 vs 参数值')
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # 保存图表
            plot_path = plot_dir / f'{param_name}_sensitivity.png'
            plt.savefig(plot_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            logger.info(f"  已保存: {plot_path}")
        
        logger.info(f"\n所有图表已保存到: {plot_dir}")
    
    def generate_report(self, df_results: pd.DataFrame, analysis: Dict):
        """生成文字报告"""
        
        logger.info("\n生成敏感性分析报告...")
        
        report_lines = []
        report_lines.append("="*80)
        report_lines.append("参数敏感性分析报告")
        report_lines.append("="*80)
        report_lines.append("")
        report_lines.append(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"验证集: 2025年")
        report_lines.append(f"测试参数数量: {len(analysis)}")
        report_lines.append("")
        
        # 按敏感性排序
        sorted_params = sorted(
            analysis.items(),
            key=lambda x: x[1]['sensitivity_score'],
            reverse=True
        )
        
        report_lines.append("【一、参数敏感性排名】")
        report_lines.append("")
        report_lines.append("排名 | 参数名称 | 敏感性评分 | IC变异系数 | 最优值")
        report_lines.append("-" * 80)
        
        for rank, (param_name, metrics) in enumerate(sorted_params, 1):
            report_lines.append(
                f"{rank:2d}   | {param_name:30s} | {metrics['sensitivity_score']:>12.4f} | "
                f"{metrics['ic_cv']:>12.4f} | {metrics['best_value']}"
            )
        
        report_lines.append("")
        report_lines.append("【二、详细分析】")
        report_lines.append("")
        
        for param_name, metrics in sorted_params:
            report_lines.append(f"\n{param_name}:")
            report_lines.append(f"  敏感性: {'高' if metrics['sensitivity_score'] > 0.1 else '中' if metrics['sensitivity_score'] > 0.05 else '低'}")
            report_lines.append(f"  IC变化范围: {metrics['ic_range']:.4f}")
            report_lines.append(f"  IC变异系数: {metrics['ic_cv']:.4f}")
            report_lines.append(f"  夏普变化范围: {metrics['sharpe_range']:.4f}")
            report_lines.append(f"  最优参数值: {metrics['best_value']}")
            report_lines.append(f"  最优IC IR: {metrics['best_ic_ir']:.4f}")
        
        report_lines.append("")
        report_lines.append("【三、建议】")
        report_lines.append("")
        
        high_sensitivity = [p for p, m in sorted_params if m['sensitivity_score'] > 0.1]
        low_sensitivity = [p for p, m in sorted_params if m['sensitivity_score'] < 0.05]
        
        report_lines.append(f"高敏感参数（需要谨慎优化）: {', '.join(high_sensitivity)}")
        report_lines.append(f"低敏感参数（可以固定）: {', '.join(low_sensitivity)}")
        report_lines.append("")
        report_lines.append("建议优化顺序:")
        for rank, (param_name, _) in enumerate(sorted_params[:5], 1):
            report_lines.append(f"  {rank}. {param_name}")
        
        report_lines.append("")
        report_lines.append("="*80)
        
        # 保存报告
        report_path = OUTPUT_DIR / 'sensitivity_analysis_report.txt'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        logger.info(f"报告已保存: {report_path}")
        
        # 打印到控制台
        print('\n'.join(report_lines))


def main():
    """主函数"""
    
    try:
        analyzer = SensitivityAnalyzer()
        
        # 运行所有扫描
        df_results = analyzer.run_all_scans()
        
        # 分析结果
        analysis = analyzer.analyze_results(df_results)
        
        # 生成图表
        analyzer.generate_plots(df_results)
        
        # 生成报告
        analyzer.generate_report(df_results, analysis)
        
        logger.info("\n✅ 敏感性分析完成！")
        
        return True
        
    except Exception as e:
        logger.error(f"敏感性分析失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
