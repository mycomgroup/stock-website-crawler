"""
2026年年初至今（YTD）数据分析和回测脚本

基于已下载的weekly_factors数据，分析2026年的因子表现和策略效果。

使用方法：
    python skills/autoresearch_ml_joinquant_factor_v2/analyze_2026_ytd.py

输出文件：
    - output/analysis/2026_ytd_report.txt (文本报告)
    - output/analysis/2026_ytd_summary.json (JSON摘要)
"""

from __future__ import annotations

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
import glob

import numpy as np
import pandas as pd
from scipy import stats

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "weekly_factors"
ANALYSIS_DIR = BASE_DIR / "output" / "analysis"


class YTD2026Analyzer:
    """2026年YTD数据分析器"""

    def __init__(self):
        self.df_all: pd.DataFrame | None = None
        self.ic_series: list[float] = []
        self.portfolio_returns: pd.Series | None = None
        self.market_returns: pd.Series | None = None
        self.data_files: list[str] = []
        
    def load_ytd_data(self):
        """加载2026年YTD数据"""
        logger.info("=" * 80)
        logger.info("加载2026年YTD数据...")
        logger.info("=" * 80)
        
        # 获取2026年的所有数据文件
        all_files = sorted(glob.glob(str(DATA_DIR / "factors_*.csv")))
        self.data_files = [f for f in all_files if "factors_2026" in f]
        
        if not self.data_files:
            raise FileNotFoundError(f"未找到2026年的数据文件: {DATA_DIR}")
        
        logger.info(f"  找到 {len(self.data_files)} 个数据文件")
        logger.info(f"  时间范围: {Path(self.data_files[0]).stem} 到 {Path(self.data_files[-1]).stem}")
        
        # 加载所有数据
        dfs = []
        for file_path in self.data_files:
            df = pd.read_csv(file_path)
            # 从文件名提取日期
            date_str = Path(file_path).stem.split('_')[1]
            df['date'] = pd.to_datetime(date_str)
            dfs.append(df)
        
        self.df_all = pd.concat(dfs, ignore_index=True)
        
        # 数据清洗
        if 'Unnamed: 0' in self.df_all.columns:
            self.df_all = self.df_all.rename(columns={'Unnamed: 0': 'stock_id'})
        
        # 过滤异常数据
        logger.info("  过滤异常数据...")
        
        # 按日期检查pchg的异常情况
        dates_to_remove = []
        for date in sorted(self.df_all['date'].unique()):
            df_date = self.df_all[self.df_all['date'] == date]
            pchg_valid = df_date['pchg'].dropna()
            
            if len(pchg_valid) == 0:
                logger.warning(f"    {date.strftime('%Y-%m-%d')}: 所有pchg为空，移除")
                dates_to_remove.append(date)
            elif (pchg_valid == -1.0).sum() > len(pchg_valid) * 0.5:
                logger.warning(f"    {date.strftime('%Y-%m-%d')}: 超过50%的pchg为-1.0，移除")
                dates_to_remove.append(date)
            elif np.isinf(pchg_valid).sum() > 0:
                logger.warning(f"    {date.strftime('%Y-%m-%d')}: 存在inf值，移除")
                dates_to_remove.append(date)
        
        if dates_to_remove:
            self.df_all = self.df_all[~self.df_all['date'].isin(dates_to_remove)]
            logger.info(f"  移除了 {len(dates_to_remove)} 个异常日期")
        
        logger.info(f"  总数据量: {len(self.df_all)} 行")
        logger.info(f"  覆盖周数: {self.df_all['date'].nunique()}")
        logger.info(f"  覆盖股票: {self.df_all['stock_id'].nunique()}")
        logger.info(f"  因子数量: {len([c for c in self.df_all.columns if c not in ['stock_id', 'date', 'pchg']])}")
        logger.info(f"  缺失值比例: {self.df_all.isnull().sum().sum() / (self.df_all.shape[0] * self.df_all.shape[1]) * 100:.2f}%")
        
    def preprocess_factors(self):
        """预处理因子数据"""
        logger.info("\n" + "=" * 80)
        logger.info("预处理因子...")
        logger.info("=" * 80)
        
        # 获取所有因子列（排除stock_id, date, pchg）
        factor_cols = [c for c in self.df_all.columns if c not in ['stock_id', 'date', 'pchg']]
        
        # 按日期分组进行截面标准化
        def standardize_cross_section(group):
            for col in factor_cols:
                if col in group.columns:
                    # Winsorize: 3倍标准差
                    mean = group[col].mean()
                    std = group[col].std()
                    if std > 0:
                        group[col] = group[col].clip(mean - 3*std, mean + 3*std)
                    
                    # 填充缺失值（用中位数）
                    group[col] = group[col].fillna(group[col].median())
                    
                    # 标准化
                    if std > 0:
                        group[col] = (group[col] - mean) / std
            return group
        
        logger.info("  执行截面标准化...")
        self.df_all = self.df_all.groupby('date', group_keys=False).apply(standardize_cross_section)
        
        logger.info("  预处理完成")
        
    def calculate_factor_ic(self):
        """计算因子IC"""
        logger.info("\n" + "=" * 80)
        logger.info("计算因子IC...")
        logger.info("=" * 80)
        
        factor_cols = [c for c in self.df_all.columns if c not in ['stock_id', 'date', 'pchg']]
        
        # 计算每个因子的IC
        factor_ic_dict = {}
        
        for factor in factor_cols:
            ic_list = []
            for date in sorted(self.df_all['date'].unique()):
                df_date = self.df_all[self.df_all['date'] == date]
                
                # 过滤有效数据
                valid_mask = df_date[factor].notna() & df_date['pchg'].notna()
                if valid_mask.sum() > 10:
                    corr, _ = stats.spearmanr(
                        df_date.loc[valid_mask, factor],
                        df_date.loc[valid_mask, 'pchg']
                    )
                    if np.isfinite(corr):
                        ic_list.append(corr)
            
            if ic_list:
                factor_ic_dict[factor] = {
                    'mean_ic': np.mean(ic_list),
                    'std_ic': np.std(ic_list),
                    'ir': np.mean(ic_list) / np.std(ic_list) if np.std(ic_list) > 0 else 0,
                    'positive_ratio': sum(ic > 0 for ic in ic_list) / len(ic_list)
                }
        
        # 按IR排序，选择Top因子
        factor_ic_df = pd.DataFrame(factor_ic_dict).T
        factor_ic_df = factor_ic_df.sort_values('ir', ascending=False)
        
        logger.info(f"  计算了 {len(factor_ic_df)} 个因子的IC")
        logger.info("\n  Top 20 因子（按IR排序）:")
        logger.info("  " + "-" * 70)
        logger.info(f"  {'因子名称':<40} {'平均IC':>8} {'IC_IR':>8} {'正比例':>8}")
        logger.info("  " + "-" * 70)
        
        for idx, (factor, row) in enumerate(factor_ic_df.head(20).iterrows(), 1):
            logger.info(f"  {idx:2d}. {factor:<37} {row['mean_ic']:>8.4f} {row['ir']:>8.4f} {row['positive_ratio']:>7.1%}")
        
        # 选择Top 50因子构建组合
        self.top_factors = factor_ic_df.head(50).index.tolist()
        logger.info(f"\n  选择Top 50因子构建组合")
        
        return factor_ic_df
        
    def build_composite_signal(self):
        """构建复合信号"""
        logger.info("\n" + "=" * 80)
        logger.info("构建复合信号...")
        logger.info("=" * 80)
        
        # 使用Top因子的等权平均作为复合信号
        self.df_all['composite_signal'] = self.df_all[self.top_factors].mean(axis=1)
        
        # 计算复合信号的IC
        dates = sorted(self.df_all['date'].unique())
        
        for date in dates:
            df_date = self.df_all[self.df_all['date'] == date]
            valid_mask = df_date['composite_signal'].notna() & df_date['pchg'].notna()
            
            if valid_mask.sum() > 10:
                corr, _ = stats.spearmanr(
                    df_date.loc[valid_mask, 'composite_signal'],
                    df_date.loc[valid_mask, 'pchg']
                )
                if np.isfinite(corr):
                    self.ic_series.append(corr)
        
        logger.info(f"  复合信号IC: {np.mean(self.ic_series):.4f} ± {np.std(self.ic_series):.4f}")
        logger.info(f"  复合信号IR: {np.mean(self.ic_series) / np.std(self.ic_series):.4f}")
        
    def backtest_strategy(self):
        """回测策略"""
        logger.info("\n" + "=" * 80)
        logger.info("回测策略...")
        logger.info("=" * 80)
        
        # Top-50组合策略
        def simulate_top50(group):
            # 按复合信号排序，选择Top 50
            top50 = group.nlargest(50, 'composite_signal')
            return top50['pchg'].mean()
        
        self.portfolio_returns = self.df_all.groupby('date', group_keys=False).apply(simulate_top50)
        self.market_returns = self.df_all.groupby('date')['pchg'].mean()
        
        # 计算收益指标
        n_weeks = len(self.portfolio_returns)
        port_cum = (1 + self.portfolio_returns).cumprod()
        mkt_cum = (1 + self.market_returns).cumprod()
        
        # 计算实际天数跨度
        date_range = self.portfolio_returns.index.max() - self.portfolio_returns.index.min()
        n_days = date_range.days
        
        # YTD收益（不年化）
        ytd_port = (port_cum.iloc[-1] - 1) * 100
        ytd_mkt = (mkt_cum.iloc[-1] - 1) * 100
        
        # 如果要年化，使用实际天数
        if n_days > 0:
            ann_port = ((port_cum.iloc[-1]) ** (365.25 / n_days) - 1) * 100
            ann_mkt = ((mkt_cum.iloc[-1]) ** (365.25 / n_days) - 1) * 100
        else:
            ann_port = 0
            ann_mkt = 0
        
        ann_vol_port = self.portfolio_returns.std() * np.sqrt(52) * 100
        ann_vol_mkt = self.market_returns.std() * np.sqrt(52) * 100
        
        logger.info(f"  数据跨度: {n_days}天 ({n_weeks}周)")
        logger.info(f"  组合YTD收益: {ytd_port:.2f}%")
        logger.info(f"  组合年化收益: {ann_port:.2f}%")
        logger.info(f"  组合年化波动: {ann_vol_port:.2f}%")
        logger.info(f"  组合夏普比率: {ann_port / ann_vol_port:.2f}")
        logger.info(f"  市场YTD收益: {ytd_mkt:.2f}%")
        logger.info(f"  市场年化收益: {ann_mkt:.2f}%")
        logger.info(f"  YTD超额收益: {ytd_port - ytd_mkt:.2f}%")
        logger.info(f"  年化超额收益: {ann_port - ann_mkt:.2f}%")
        
    def generate_report(self) -> str:
        """生成完整分析报告"""
        report_lines = []
        
        report_lines.append("=" * 80)
        report_lines.append("2026年年初至今（YTD）因子分析和回测报告")
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # 数据概况
        report_lines.append("【一、数据概况】")
        report_lines.append("")
        report_lines.append(f"数据文件数: {len(self.data_files)}")
        report_lines.append(f"时间范围: {self.df_all['date'].min().strftime('%Y-%m-%d')} ~ {self.df_all['date'].max().strftime('%Y-%m-%d')}")
        report_lines.append(f"覆盖周数: {self.df_all['date'].nunique()}")
        report_lines.append(f"覆盖股票: {self.df_all['stock_id'].nunique()}")
        report_lines.append(f"总数据量: {len(self.df_all)}")
        report_lines.append("")
        
        # IC分析
        report_lines.append("【二、复合信号IC分析】")
        report_lines.append("")
        report_lines.append(f"平均IC: {np.mean(self.ic_series):.4f}")
        report_lines.append(f"IC标准差: {np.std(self.ic_series):.4f}")
        report_lines.append(f"IC IR: {np.mean(self.ic_series) / np.std(self.ic_series):.4f}")
        report_lines.append(f"IC中位数: {np.median(self.ic_series):.4f}")
        report_lines.append(f"IC最大: {np.max(self.ic_series):.4f}")
        report_lines.append(f"IC最小: {np.min(self.ic_series):.4f}")
        report_lines.append(f"IC>0占比: {sum(ic > 0 for ic in self.ic_series) / len(self.ic_series) * 100:.2f}%")
        report_lines.append(f"IC>0.03占比: {sum(ic > 0.03 for ic in self.ic_series) / len(self.ic_series) * 100:.2f}%")
        report_lines.append(f"IC>0.05占比: {sum(ic > 0.05 for ic in self.ic_series) / len(self.ic_series) * 100:.2f}%")
        report_lines.append("")
        
        # 分组收益
        report_lines.append("【三、分组收益分析】")
        report_lines.append("")
        
        def calc_10groups(group):
            group['signal_rank'] = group['composite_signal'].rank(pct=True)
            group['group'] = pd.cut(
                group['signal_rank'],
                bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                labels=['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10']
            )
            return group
        
        df_groups = self.df_all.groupby('date', group_keys=False).apply(calc_10groups)
        group_returns = df_groups.groupby('group', observed=False)['pchg'].mean() * 100
        
        report_lines.append("10分组平均周收益:")
        report_lines.append("分组 | 平均收益 | 年化收益 | 说明")
        report_lines.append("-" * 50)
        for g, r in group_returns.items():
            ann_r = r * 52
            desc = "信号最弱" if g == 'G1' else "信号最强" if g == 'G10' else ""
            report_lines.append(f"{g}   | {r:.4f}%  | {ann_r:.2f}% | {desc}")
        report_lines.append("")
        spread = group_returns.iloc[-1] - group_returns.iloc[0]
        report_lines.append(f"G10-G1 spread: {spread:.4f}%/周 ({spread * 52:.2f}%/年)")
        report_lines.append("")
        
        # 策略回测
        report_lines.append("【四、策略回测（Top-50组合）】")
        report_lines.append("")
        
        n_weeks = len(self.portfolio_returns)
        port_cum = (1 + self.portfolio_returns).cumprod()
        mkt_cum = (1 + self.market_returns).cumprod()
        
        # 计算实际天数跨度
        date_range = self.portfolio_returns.index.max() - self.portfolio_returns.index.min()
        n_days = date_range.days
        
        ytd_port = (port_cum.iloc[-1] - 1) * 100
        ytd_mkt = (mkt_cum.iloc[-1] - 1) * 100
        
        if n_days > 0:
            ann_port = ((port_cum.iloc[-1]) ** (365.25 / n_days) - 1) * 100
            ann_mkt = ((mkt_cum.iloc[-1]) ** (365.25 / n_days) - 1) * 100
        else:
            ann_port = 0
            ann_mkt = 0
            
        ann_vol_port = self.portfolio_returns.std() * np.sqrt(52) * 100
        ann_vol_mkt = self.market_returns.std() * np.sqrt(52) * 100
        sharpe_port = ann_port / ann_vol_port if ann_vol_port > 0 else 0
        sharpe_mkt = ann_mkt / ann_vol_mkt if ann_vol_mkt > 0 else 0
        
        report_lines.append(f"数据跨度: {n_days}天 ({n_weeks}周)")
        report_lines.append("")
        
        port_dd = port_cum / port_cum.cummax() - 1
        mkt_dd = mkt_cum / mkt_cum.cummax() - 1
        
        report_lines.append("收益指标:")
        report_lines.append(f"  Top-50 YTD收益: {ytd_port:.2f}%")
        report_lines.append(f"  Top-50年化收益: {ann_port:.2f}%")
        report_lines.append(f"  Top-50年化波动: {ann_vol_port:.2f}%")
        report_lines.append(f"  Top-50夏普比率: {sharpe_port:.2f}")
        report_lines.append(f"  市场YTD收益: {ytd_mkt:.2f}%")
        report_lines.append(f"  市场年化收益: {ann_mkt:.2f}%")
        report_lines.append(f"  市场年化波动: {ann_vol_mkt:.2f}%")
        report_lines.append(f"  市场夏普比率: {sharpe_mkt:.2f}")
        report_lines.append(f"  YTD超额收益: {ytd_port - ytd_mkt:.2f}%")
        report_lines.append(f"  年化超额收益: {ann_port - ann_mkt:.2f}%")
        report_lines.append("")
        report_lines.append("风险指标:")
        report_lines.append(f"  Top-50最大回撤: {port_dd.min() * 100:.2f}%")
        report_lines.append(f"  市场最大回撤: {mkt_dd.min() * 100:.2f}%")
        if port_dd.min() < 0:
            report_lines.append(f"  Calmar比率: {ann_port / abs(port_dd.min() * 100):.2f}")
        report_lines.append("")
        report_lines.append("胜率指标:")
        report_lines.append(f"  周胜率: {(self.portfolio_returns > self.market_returns).mean() * 100:.2f}%")
        report_lines.append("")
        
        # 周度收益明细
        report_lines.append("【五、周度收益明细】")
        report_lines.append("")
        report_lines.append("日期       | 组合收益 | 市场收益 | 超额收益")
        report_lines.append("-" * 50)
        
        for date in sorted(self.portfolio_returns.index):
            port_ret = self.portfolio_returns[date] * 100
            mkt_ret = self.market_returns[date] * 100
            excess = port_ret - mkt_ret
            report_lines.append(f"{date.strftime('%Y-%m-%d')} | {port_ret:>7.2f}% | {mkt_ret:>7.2f}% | {excess:>7.2f}%")
        report_lines.append("")
        
        # 结论
        report_lines.append("【六、结论】")
        report_lines.append("")
        report_lines.append("2026年YTD表现:")
        report_lines.append(f"  ✅ 复合信号IC={np.mean(self.ic_series):.4f}")
        report_lines.append(f"  ✅ {sum(ic > 0 for ic in self.ic_series) / len(self.ic_series) * 100:.2f}%的周IC>0")
        report_lines.append(f"  ✅ YTD超额收益: {ytd_port - ytd_mkt:.2f}%")
        report_lines.append(f"  ✅ 夏普比率: {sharpe_port:.2f}")
        report_lines.append("")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def generate_summary_json(self) -> dict:
        """生成JSON摘要"""
        n_weeks = len(self.portfolio_returns)
        port_cum = (1 + self.portfolio_returns).cumprod()
        mkt_cum = (1 + self.market_returns).cumprod()
        
        # 计算实际天数跨度
        date_range = self.portfolio_returns.index.max() - self.portfolio_returns.index.min()
        n_days = date_range.days
        
        ytd_port = (port_cum.iloc[-1] - 1) * 100
        ytd_mkt = (mkt_cum.iloc[-1] - 1) * 100
        
        if n_days > 0:
            ann_port = ((port_cum.iloc[-1]) ** (365.25 / n_days) - 1) * 100
            ann_mkt = ((mkt_cum.iloc[-1]) ** (365.25 / n_days) - 1) * 100
        else:
            ann_port = 0
            ann_mkt = 0
        
        port_dd = port_cum / port_cum.cummax() - 1
        
        summary = {
            'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_coverage': {
                'n_files': len(self.data_files),
                'n_weeks': self.df_all['date'].nunique(),
                'n_stocks': self.df_all['stock_id'].nunique(),
                'n_days': n_days,
                'date_range': f"{self.df_all['date'].min().strftime('%Y-%m-%d')} ~ {self.df_all['date'].max().strftime('%Y-%m-%d')}",
            },
            'ic_analysis': {
                'mean': float(np.mean(self.ic_series)),
                'std': float(np.std(self.ic_series)),
                'ir': float(np.mean(self.ic_series) / np.std(self.ic_series)),
                'positive_ratio': float(sum(ic > 0 for ic in self.ic_series) / len(self.ic_series)),
            },
            'portfolio_performance': {
                'ytd_return_pct': float(ytd_port),
                'annual_return_pct': float(ann_port),
                'annual_vol_pct': float(self.portfolio_returns.std() * np.sqrt(52) * 100),
                'sharpe': float(ann_port / (self.portfolio_returns.std() * np.sqrt(52) * 100)),
                'max_drawdown_pct': float(port_dd.min() * 100),
                'weekly_win_rate': float((self.portfolio_returns > self.market_returns).mean()),
            },
            'market_baseline': {
                'ytd_return_pct': float(ytd_mkt),
                'annual_return_pct': float(ann_mkt),
                'annual_vol_pct': float(self.market_returns.std() * np.sqrt(52) * 100),
                'sharpe': float(ann_mkt / (self.market_returns.std() * np.sqrt(52) * 100)),
                'max_drawdown_pct': float((mkt_cum / mkt_cum.cummax() - 1).min() * 100),
            },
        }
        
        return summary
    
    def save_results(self, report_text: str, summary_json: dict):
        """保存结果到文件"""
        ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
        
        # 保存文本报告
        report_path = ANALYSIS_DIR / "2026_ytd_report.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        logger.info(f"\n文本报告已保存: {report_path}")
        
        # 保存JSON摘要
        summary_path = ANALYSIS_DIR / "2026_ytd_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary_json, f, indent=2, ensure_ascii=False)
        logger.info(f"JSON摘要已保存: {summary_path}")
    
    def run(self):
        """运行完整分析流程"""
        try:
            # 加载数据
            self.load_ytd_data()
            
            # 预处理因子
            self.preprocess_factors()
            
            # 计算因子IC
            self.calculate_factor_ic()
            
            # 构建复合信号
            self.build_composite_signal()
            
            # 回测策略
            self.backtest_strategy()
            
            # 生成报告
            report_text = self.generate_report()
            logger.info("\n" + report_text)
            
            # 生成JSON摘要
            summary_json = self.generate_summary_json()
            
            # 保存结果
            self.save_results(report_text, summary_json)
            
            logger.info("\n" + "=" * 80)
            logger.info("分析完成!")
            logger.info("=" * 80)
            
            return True
            
        except Exception as e:
            logger.error(f"分析失败: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """主函数"""
    analyzer = YTD2026Analyzer()
    success = analyzer.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
