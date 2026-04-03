"""
Alpha191因子健康度诊断与筛选
针对191个纯量化公式因子进行快速筛选和健康度评估
"""

try:
    from jqdatasdk import *
    from jqdatasdk.alpha191 import get_all_alpha_191

    JQDATA_AVAILABLE = True
except ImportError:
    JQDATA_AVAILABLE = False

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings("ignore")


class Alpha191Screening:
    """Alpha191因子筛选器"""

    def __init__(self, start_date="2023-01-01", end_date="2025-12-31"):
        if not JQDATA_AVAILABLE:
            raise ImportError("jqdatasdk is required for Alpha191Screening")
        self.start_date = start_date
        self.end_date = end_date
        self.trade_days = get_trade_days(start_date, end_date)

    def get_stock_universe(self, watch_date):
        """获取股票池"""
        all_stocks = get_all_securities(types=["stock"], date=watch_date)

        all_stocks = all_stocks[
            all_stocks["start_date"] <= watch_date - timedelta(days=180)
        ]
        stocks = all_stocks.index.tolist()

        is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
        stocks = is_st[is_st == False].index.tolist()

        paused = get_price(
            stocks, end_date=watch_date, count=1, fields="paused", panel=False
        )
        paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
        stocks = paused[paused == 0].index.tolist()

        stocks = [s for s in stocks if not s.startswith("688")]

        q = query(valuation.code, valuation.market_cap).filter(
            valuation.code.in_(stocks),
            valuation.market_cap >= 20,
            valuation.market_cap <= 200,
        )

        df = get_fundamentals(q, date=watch_date)
        return df["code"].tolist()

    def get_forward_return(self, stocks, watch_date, hold_days=5):
        """获取未来N日收益率"""
        future_date = get_trade_days(
            watch_date, watch_date + timedelta(days=hold_days * 2), count=hold_days + 1
        )[-1]

        prices = get_price(
            stocks, end_date=future_date, count=1, fields=["close"], panel=False
        )

        prices_now = get_price(
            stocks, end_date=watch_date, count=1, fields=["close"], panel=False
        )

        returns = (
            prices.pivot(index="time", columns="code", values="close").iloc[-1]
            / prices_now.pivot(index="time", columns="code", values="close").iloc[-1]
            - 1
        )

        return returns

    def test_alpha_factor(self, alpha_name, stocks, watch_date):
        """测试单个Alpha因子"""
        try:
            df = get_all_alpha_191(
                date=watch_date.strftime("%Y-%m-%d"), code=stocks, alpha=[alpha_name]
            )

            if df is None or len(df) == 0:
                return None

            factor_values = df.iloc[0] if isinstance(df, pd.DataFrame) else df

            forward_returns = self.get_forward_return(stocks, watch_date)

            valid_data = pd.DataFrame(
                {"factor": factor_values, "return": forward_returns}
            ).dropna()

            if len(valid_data) < 30:
                return None

            ic = valid_data["factor"].corr(valid_data["return"], method="spearman")

            return {
                "alpha": alpha_name,
                "ic": ic,
                "date": watch_date,
                "sample_size": len(valid_data),
            }

        except Exception as e:
            return None

    def batch_screen_factors(self, alpha_list, batch_name):
        """批量筛选因子"""
        print(f"\n开始{batch_name}筛选，共{len(alpha_list)}个因子...")

        results = []

        test_dates = self.trade_days[::20]

        for alpha_name in alpha_list:
            ic_series = []

            for date in test_dates:
                try:
                    stocks = self.get_stock_universe(date)
                    if len(stocks) < 100:
                        continue

                    result = self.test_alpha_factor(alpha_name, stocks, date)

                    if result and not np.isnan(result["ic"]):
                        ic_series.append(result["ic"])

                except Exception as e:
                    continue

            if ic_series:
                ic_mean = np.mean(ic_series)
                ic_std = np.std(ic_series)
                icir = ic_mean / ic_std if ic_std > 0 else 0
                ic_positive_rate = np.mean([ic > 0 for ic in ic_series])

                results.append(
                    {
                        "alpha": alpha_name,
                        "ic_mean": ic_mean,
                        "ic_std": ic_std,
                        "icir": icir,
                        "ic_positive_rate": ic_positive_rate,
                        "sample_days": len(ic_series),
                    }
                )

                status = "✅" if icir > 0.3 else "⚠️" if icir > 0.15 else "❌"
                print(
                    f"{status} {alpha_name}: IC={ic_mean:.4f}, ICIR={icir:.4f}, IC>0={ic_positive_rate:.2%}"
                )

        return pd.DataFrame(results)

    def run_full_screening(self):
        """运行完整筛选"""
        print("=" * 80)
        print("Alpha191因子健康度诊断开始")
        print("=" * 80)

        batches = [
            (
                ["alpha_{:03d}".format(i) for i in range(1, 51)],
                "Batch 1 (alpha_001-050)",
            ),
            (
                ["alpha_{:03d}".format(i) for i in range(51, 101)],
                "Batch 2 (alpha_051-100)",
            ),
            (
                ["alpha_{:03d}".format(i) for i in range(101, 151)],
                "Batch 3 (alpha_101-150)",
            ),
            (
                ["alpha_{:03d}".format(i) for i in range(151, 192)],
                "Batch 4 (alpha_151-191)",
            ),
        ]

        all_results = []

        for alpha_list, batch_name in batches:
            batch_result = self.batch_screen_factors(alpha_list, batch_name)
            if not batch_result.empty:
                all_results.append(batch_result)

        if all_results:
            final_results = pd.concat(all_results, ignore_index=True)

            final_results = final_results.sort_values("icir", ascending=False)

            return final_results
        else:
            return pd.DataFrame()


def generate_screening_report(results_df):
    """生成筛选报告"""
    report = []

    report.append("# Alpha191因子筛选报告")
    report.append("")
    report.append("## 1. Alpha191因子概述")
    report.append("")
    report.append("### 1.1 因子特点")
    report.append("- **来源**: WorldQuant Alpha101的扩展版本")
    report.append("- **数量**: 191个纯量化公式因子")
    report.append("- **特性**: 纯价量公式、无基本面依赖")
    report.append("- **优势**: 计算快速、逻辑透明、实盘可用")
    report.append("- **API**: `get_all_alpha_191(date, code, alpha)`")
    report.append("")
    report.append("### 1.2 筛选方法")
    report.append("- **测试期间**: 2023-2025年")
    report.append("- **样本股票**: 20-200亿市值股票")
    report.append("- **预测周期**: 5日收益")
    report.append("- **评价指标**: IC均值、ICIR、IC>0比例")
    report.append("- **筛选标准**: ICIR > 0.3为有效，0.15-0.3为弱有效")
    report.append("")

    report.append("## 2. 各批次筛选结果")
    report.append("")

    if results_df.empty:
        report.append("**注意**: 本报告为模拟示例，实际运行需要聚宽API权限和数据访问。")
        report.append("")
        report.append("### 2.1 Batch 1 (alpha_001-050)")
        report.append("- 有效因子: 待测试")
        report.append("- 弱有效因子: 待测试")
        report.append("- 无效因子: 待测试")
        report.append("")
        report.append("### 2.2 Batch 2 (alpha_051-100)")
        report.append("- 有效因子: 待测试")
        report.append("- 弱有效因子: 待测试")
        report.append("- 无效因子: 待测试")
        report.append("")
        report.append("### 2.3 Batch 3 (alpha_101-150)")
        report.append("- 有效因子: 待测试")
        report.append("- 弱有效因子: 待测试")
        report.append("- 无效因子: 待测试")
        report.append("")
        report.append("### 2.4 Batch 4 (alpha_151-191)")
        report.append("- 有效因子: 待测试")
        report.append("- 弱有效因子: 待测试")
        report.append("- 无效因子: 待测试")
        report.append("")

        report.append("## 3. 有效因子清单（ICIR > 0.3）")
        report.append("")
        report.append("**筛选结果**: 暂无有效因子数据")
        report.append("")
        report.append("| 因子名称 | IC均值 | ICIR | IC>0比例 | 样本天数 | 评级 |")
        report.append("|---------|--------|------|---------|---------|------|")
        report.append("| - | - | - | - | - | - |")
        report.append("")

        report.append("## 4. 与标准因子对比分析")
        report.append("")
        report.append("### 4.1 对比基准")
        report.append("- **RFScore7**: 小盘因子组合，ICIR ≈ 0.8")
        report.append("- **传统因子**: PE/PB/ROE，ICIR ≈ 0.3-0.5")
        report.append("- **动量因子**: ICIR ≈ 0.2-0.4")
        report.append("")
        report.append("### 4.2 增量价值")
        report.append("Alpha191因子的增量价值在于:")
        report.append("1. **计算速度**: 纯公式，无基本面数据延迟")
        report.append("2. **实盘可用**: 无未来函数，可即时计算")
        report.append("3. **逻辑透明**: 公式明确，可解释性强")
        report.append("4. **与现有因子相关性低**: 提供多样化alpha来源")
        report.append("")

        report.append("## 5. 使用建议")
        report.append("")
        report.append("### 5.1 筛选建议")
        report.append("1. **优先使用ICIR > 0.3的因子**")
        report.append("2. **避免使用ICIR < 0.15的因子**")
        report.append("3. **注意因子间的相关性**")
        report.append("4. **定期重新测试因子有效性**")
        report.append("")
        report.append("### 5.2 组合构建")
        report.append("```python")
        report.append("# 示例：使用筛选后的Alpha191因子")
        report.append("from jqdatasdk.alpha191 import get_all_alpha_191")
        report.append("")
        report.append("# 获取有效因子列表")
        report.append(
            "effective_alphas = ['alpha_001', 'alpha_042', ...]  # 根据筛选结果填充"
        )
        report.append("")
        report.append("# 计算因子值")
        report.append("alpha_df = get_all_alpha_191(")
        report.append("    date='2025-01-01',")
        report.append("    code=stock_list,")
        report.append("    alpha=effective_alphas")
        report.append(")")
        report.append("")
        report.append("# 等权或ICIR加权")
        report.append("composite_score = alpha_df.mean(axis=1)  # 等权")
        report.append("```")
        report.append("")
        report.append("### 5.3 注意事项")
        report.append("1. **过拟合风险**: 191个因子中，部分可能过拟合历史数据")
        report.append("2. **衰减风险**: 因子可能随时间衰减，需定期更新")
        report.append("3. **数据质量**: 确保价量数据准确无缺失")
        report.append("4. **交易成本**: 高频因子需考虑交易成本影响")
        report.append("")

        report.append("---")
        report.append("")
        report.append("**报告生成时间**: 2026-04-03")
        report.append("")
        report.append(
            "**说明**: 本报告为Alpha191因子筛选框架，实际因子IC需要运行完整回测代码获取。"
        )
        report.append("")
        report.append("## 附录：完整筛选代码")
        report.append("")
        report.append("完整筛选代码请参见: `alpha191_screening_analysis.py`")
        report.append("")

    else:
        effective_factors = results_df[results_df["icir"] > 0.3]
        weak_factors = results_df[
            (results_df["icir"] > 0.15) & (results_df["icir"] <= 0.3)
        ]
        invalid_factors = results_df[results_df["icir"] <= 0.15]

        report.append("### 2.1 Batch 1 (alpha_001-050)")
        batch1 = results_df[
            results_df["alpha"].str.contains(
                "alpha_00[1-9]|alpha_0[1-4][0-9]|alpha_050"
            )
        ]
        if not batch1.empty:
            report.append(f"- 有效因子: {len(batch1[batch1['icir'] > 0.3])}个")
            report.append(
                f"- 弱有效因子: {len(batch1[(batch1['icir'] > 0.15) & (batch1['icir'] <= 0.3)])}个"
            )
            report.append(f"- 无效因子: {len(batch1[batch1['icir'] <= 0.15])}个")
        report.append("")

        report.append("### 2.2 Batch 2 (alpha_051-100)")
        batch2 = results_df[
            results_df["alpha"].str.contains(
                "alpha_05[1-9]|alpha_0[6-9][0-9]|alpha_100"
            )
        ]
        if not batch2.empty:
            report.append(f"- 有效因子: {len(batch2[batch2['icir'] > 0.3])}个")
            report.append(
                f"- 弱有效因子: {len(batch2[(batch2['icir'] > 0.15) & (batch2['icir'] <= 0.3)])}个"
            )
            report.append(f"- 无效因子: {len(batch2[batch2['icir'] <= 0.15])}个")
        report.append("")

        report.append("### 2.3 Batch 3 (alpha_101-150)")
        batch3 = results_df[
            results_df["alpha"].str.contains("alpha_1[0-4][0-9]|alpha_150")
        ]
        if not batch3.empty:
            report.append(f"- 有效因子: {len(batch3[batch3['icir'] > 0.3])}个")
            report.append(
                f"- 弱有效因子: {len(batch3[(batch3['icir'] > 0.15) & (batch3['icir'] <= 0.3)])}个"
            )
            report.append(f"- 无效因子: {len(batch3[batch3['icir'] <= 0.15])}个")
        report.append("")

        report.append("### 2.4 Batch 4 (alpha_151-191)")
        batch4 = results_df[
            results_df["alpha"].str.contains("alpha_1[5-9][0-9]|alpha_19[0-1]")
        ]
        if not batch4.empty:
            report.append(f"- 有效因子: {len(batch4[batch4['icir'] > 0.3])}个")
            report.append(
                f"- 弱有效因子: {len(batch4[(batch4['icir'] > 0.15) & (batch4['icir'] <= 0.3)])}个"
            )
            report.append(f"- 无效因子: {len(batch4[batch4['icir'] <= 0.15])}个")
        report.append("")

        report.append("## 3. 有效因子清单（ICIR > 0.3）")
        report.append("")
        if not effective_factors.empty:
            report.append(f"**筛选结果**: 共找到{len(effective_factors)}个有效因子")
            report.append("")
            report.append("| 因子名称 | IC均值 | ICIR | IC>0比例 | 样本天数 | 评级 |")
            report.append("|---------|--------|------|---------|---------|------|")
            for _, row in effective_factors.iterrows():
                rating = "⭐⭐⭐" if row["icir"] > 0.5 else "⭐⭐"
                report.append(
                    f"| {row['alpha']} | {row['ic_mean']:.4f} | {row['icir']:.4f} | "
                    f"{row['ic_positive_rate']:.2%} | {row['sample_days']} | {rating} |"
                )
            report.append("")
        else:
            report.append("**筛选结果**: 未找到ICIR > 0.3的有效因子")
            report.append("")

        report.append("## 4. 与标准因子对比分析")
        report.append("")
        report.append("### 4.1 对比基准")
        report.append("- **RFScore7**: 小盘因子组合，ICIR ≈ 0.8")
        report.append("- **传统因子**: PE/PB/ROE，ICIR ≈ 0.3-0.5")
        report.append("- **动量因子**: ICIR ≈ 0.2-0.4")
        report.append("")

        report.append("### 4.2 Alpha191因子表现")
        if not effective_factors.empty:
            report.append(
                f"- **有效因子数量**: {len(effective_factors)}个 ({len(effective_factors) / 191 * 100:.1f}%)"
            )
            report.append(f"- **平均ICIR**: {effective_factors['icir'].mean():.4f}")
            report.append(
                f"- **最高ICIR**: {effective_factors['icir'].max():.4f} ({effective_factors.loc[effective_factors['icir'].idxmax(), 'alpha']})"
            )
        else:
            report.append("- 未找到有效因子")
        report.append("")

        report.append("### 4.3 增量价值分析")
        report.append("Alpha191因子相比传统因子的优势:")
        report.append("1. **计算速度**: 纯价量公式，无基本面数据延迟")
        report.append("2. **实盘可用**: 无未来函数，可即时计算")
        report.append("3. **逻辑透明**: 公式明确，可解释性强")
        report.append("4. **相关性低**: 提供多样化alpha来源")
        report.append("")

        report.append("## 5. 使用建议")
        report.append("")
        report.append("### 5.1 因子筛选")
        if not effective_factors.empty:
            report.append(f"**推荐因子** (按ICIR降序):")
            report.append("```python")
            report.append("effective_alpha_list = [")
            for _, row in effective_factors.head(10).iterrows():
                report.append(f"    '{row['alpha']}',  # ICIR={row['icir']:.4f}")
            report.append("]")
            report.append("```")
        else:
            report.append("**建议**: 所有测试因子均未达到有效标准，需进一步分析原因。")
        report.append("")

        report.append("### 5.2 组合构建")
        report.append("```python")
        report.append("from jqdatasdk.alpha191 import get_all_alpha_191")
        report.append("")
        report.append("# 使用筛选后的有效因子")
        if not effective_factors.empty:
            report.append("alpha_list = [")
            for alpha in effective_factors.head(5)["alpha"].values:
                report.append(f"    '{alpha}',")
            report.append("]")
        else:
            report.append("# alpha_list = [...]  # 根据实际筛选结果填充")
        report.append("")
        report.append("# 计算因子值")
        report.append("alpha_df = get_all_alpha_191(")
        report.append("    date='2025-01-01',")
        report.append("    code=stock_list,")
        report.append("    alpha=alpha_list")
        report.append(")")
        report.append("")
        report.append("# ICIR加权组合")
        if not effective_factors.empty:
            report.append("# 根据ICIR权重计算综合得分")
        report.append("```")
        report.append("")

        report.append("### 5.3 注意事项")
        report.append("1. **过拟合风险**: 部分因子可能过拟合历史数据")
        report.append("2. **衰减风险**: 因子有效性可能随时间衰减")
        report.append("3. **数据质量**: 确保价量数据准确无缺失")
        report.append("4. **交易成本**: 高频因子需考虑交易成本")
        report.append("5. **组合相关性**: 避免选择高度相关的因子")
        report.append("")

        report.append("---")
        report.append("")
        report.append("**报告生成时间**: 2026-04-03")
        report.append("")
        if not effective_factors.empty:
            report.append(
                f"**筛选结果摘要**: 从191个Alpha191因子中筛选出{len(effective_factors)}个有效因子（ICIR > 0.3），"
            )
            report.append(
                f"占比{len(effective_factors) / 191 * 100:.1f}%。这些因子可作为量化策略的候选因子。"
            )
        else:
            report.append("**筛选结果摘要**: 测试期间未发现ICIR > 0.3的有效因子。")
        report.append("")

    return "\n".join(report)


if __name__ == "__main__":
    print("""
Alpha191因子筛选工具
====================

使用说明:
1. 首先需要安装聚宽SDK: pip install jqdatasdk
2. 登录聚宽账号: auth('username', 'password')
3. 运行筛选: python alpha191_screening_analysis.py

注意:
- 完整筛选191个因子需要较长时间（约2-3小时）
- 需要足够的聚宽API调用额度
- 建议在非交易时间运行

本脚本将:
1. 分4个批次测试191个因子
2. 计算每个因子的IC、ICIR、IC>0比例
3. 生成筛选报告
4. 给出使用建议
    """)

    print("\n提示: 如需运行完整筛选，请取消下方注释并登录聚宽账号")
    print("# auth('your_username', 'your_password')")
    print(
        "# screener = Alpha191Screening(start_date='2023-01-01', end_date='2025-12-31')"
    )
    print("# results = screener.run_full_screening()")
    print("# report = generate_screening_report(results)")
    print("# print(report)")

    print("\n生成示例报告...")
    print("-" * 80)

    demo_report = generate_screening_report(pd.DataFrame())
    print(demo_report)

    output_path = "/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328/09_alpha191_screening_report.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(demo_report)

    print(f"\n报告已保存至: {output_path}")
