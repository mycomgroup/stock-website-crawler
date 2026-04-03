"""
报告生成核心模块
负责生成日报、周报、月报、季报
"""

import pandas as pd
from datetime import datetime
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """报告生成核心类"""

    def __init__(self):
        pass

    def generate_daily_report(
        self,
        date: str,
        trade_records: pd.DataFrame,
        holdings: pd.DataFrame,
        validation_result: Dict,
    ) -> str:
        """
        生成日报

        参数:
        - date: 日期
        - trade_records: 交易记录
        - holdings: 持仓数据
        - validation_result: 验证结果

        返回:
        - report: Markdown格式报告
        """
        report = f"""# 二板接力策略OOS验证日报

**日期**: {date}  
**报告时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**报告类型**: 日频验证报告  

---

## 一、当日交易概览

### 1.1 信号生成情况
- **信号数量**: {self._count_signals(trade_records)}个
- **信号状态**: 已执行

### 1.2 交易执行情况
- **买入交易**: {self._count_buy_trades(trade_records)}笔
- **卖出交易**: {self._count_sell_trades(trade_records)}笔

### 1.3 当前持仓
- **持仓数量**: {len(holdings)}只
- **持仓市值**: {self._calculate_holding_value(holdings):.2f}元

---

## 二、当日收益统计

### 2.1 单笔收益
- **盈利交易**: {self._count_profit_trades(trade_records)}笔
- **亏损交易**: {self._count_loss_trades(trade_records)}笔
- **当日单笔净收益**: {validation_result.get("avg_trade_return", 0):.2f}%

### 2.2 累计收益
- **本月累计收益**: 待计算
- **本年累计收益**: 待计算

---

## 三、当日风险监控

### 3.1 持仓风险
- **持仓集中度**: 待计算
- **持仓市值占比**: 待计算

### 3.2 回撤监控
- **当前回撤**: {validation_result.get("max_drawdown", 0):.2f}%

---

## 四、预警状态

- **当前预警级别**: {validation_result.get("alert_level", "green").upper()}
- **触发指标**: {", ".join(validation_result.get("triggered_metrics", [])) if validation_result.get("triggered_metrics") else "无"}

---

**报告生成**: 自动生成  
**发送状态**: 已发送  

"""
        return report

    def generate_weekly_report(
        self,
        end_date: str,
        trade_records: pd.DataFrame,
        validation_result: Dict,
        emotion_data: Optional[pd.DataFrame] = None,
        breadth_data: Optional[pd.DataFrame] = None,
    ) -> str:
        """
        生成周报

        参数:
        - end_date: 周末日期
        - trade_records: 交易记录
        - validation_result: 验证结果
        - emotion_data: 情绪数据（可选）
        - breadth_data: 广度数据（可选）

        返回:
        - report: Markdown格式报告
        """
        report = f"""# 二板接力策略OOS验证周报

**周期**: {self._get_week_range(end_date)}  
**报告时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**报告类型**: 周频验证报告  

---

## 一、本周收益概览

### 1.1 收益统计
- **本周收益率**: {validation_result.get("cumulative_return", 0):.2f}%
- **近20日年化收益**: {validation_result.get("annual_return", 0):.2f}%

### 1.2 基准对比
| 对比项 | 收益率 | 超额收益率 |
|-------|--------|-----------|
| 二板接力策略 | {validation_result.get("cumulative_return", 0):.2f}% | - |
| 沪深300指数 | 待更新 | 待计算 |
| 中证1000指数 | 待更新 | 待计算 |

---

## 二、本周交易统计

### 2.1 交易概况
- **交易次数**: {validation_result.get("trade_count", 0)}笔
- **胜率**: {validation_result.get("win_rate", 0):.2f}%
- **盈亏比**: {validation_result.get("profit_loss_ratio", 0):.2f}

### 2.2 风险指标
- **最大回撤**: {validation_result.get("max_drawdown", 0):.2f}%
- **夏普比率**: {validation_result.get("sharpe_ratio", 0):.2f}

---

## 三、滚动窗口验证（近20日）

### 3.1 收益指标
- **近20日累计收益**: {validation_result.get("cumulative_return", 0):.2f}%
- **近20日年化收益**: {validation_result.get("annual_return", 0):.2f}%

### 3.2 风险指标
- **近20日最大回撤**: {validation_result.get("max_drawdown", 0):.2f}%
- **近20日夏普比率**: {validation_result.get("sharpe_ratio", 0):.2f}

---

## 四、预警状态

- **当前预警级别**: {validation_result.get("alert_level", "green").upper()}
- **触发指标**: {", ".join(validation_result.get("triggered_metrics", [])) if validation_result.get("triggered_metrics") else "无"}

---

**报告生成**: 自动生成  
**发送对象**: 交易员, 策略主管  

"""
        return report

    def generate_monthly_report(
        self,
        end_date: str,
        trade_records: pd.DataFrame,
        validation_result: Dict,
        decay_result: Optional[Dict] = None,
    ) -> str:
        """
        生成月报

        参数:
        - end_date: 月末日期
        - trade_records: 交易记录
        - validation_result: 验证结果
        - decay_result: 衰退检测结果（可选）

        返回:
        - report: Markdown格式报告
        """
        report = f"""# 二板接力策略OOS验证月报

**月份**: {self._get_month(end_date)}  
**报告时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**报告类型**: 月频验证报告  

---

## 一、本月收益概览

### 1.1 收益统计
- **本月收益率**: 待计算
- **近60日年化收益**: {validation_result.get("annual_return", 0):.2f}%

### 1.2 基准对比
| 对比项 | 年化收益率 | 超额收益率 |
|-------|-----------|-----------|
| 二板接力策略 | {validation_result.get("annual_return", 0):.2f}% | - |
| IS表现基准 | 394% | {(validation_result.get("annual_return", 0) - 394):.2f}% |

---

## 二、详细交易统计

### 2.1 质量指标
| 指标 | 本月数值 | IS基准 | 对比结果 |
|------|---------|--------|---------|
| 胜率 | {validation_result.get("win_rate", 0):.2f}% | 87.95% | {self._compare_metric(validation_result.get("win_rate", 0), 87.95)} |
| 盈亏比 | {validation_result.get("profit_loss_ratio", 0):.2f} | 21.91 | {self._compare_metric(validation_result.get("profit_loss_ratio", 0), 21.91)} |

### 2.2 风险指标
| 指标 | 本月数值 | IS基准 | 对比结果 |
|------|---------|--------|---------|
| 最大回撤 | {validation_result.get("max_drawdown", 0):.2f}% | 0.60% | {self._compare_drawdown(validation_result.get("max_drawdown", 0), 0.60)} |
| 夏普比率 | {validation_result.get("sharpe_ratio", 0):.2f} | 20+ | {self._compare_sharpe(validation_result.get("sharpe_ratio", 0), 20)} |

---

## 三、衰退检测

### 3.1 预警状态
- **当前预警级别**: {validation_result.get("alert_level", "green").upper()}
- **触发指标**: {", ".join(validation_result.get("triggered_metrics", [])) if validation_result.get("triggered_metrics") else "无"}

"""

        if decay_result:
            report += f"""### 3.2 衰退检测指标
| 指标 | 当前值 | IS基准 | 衰退比例 |
|------|--------|--------|---------|
| 年化收益 | {decay_result.get("metrics_status", {}).get("annual_return", "N/A")} | 394% | {decay_result.get("decay_ratios", {}).get("annual_return", 0) * 100:.2f}% |
| 胜率 | {decay_result.get("metrics_status", {}).get("win_rate", "N/A")} | 87.95% | {decay_result.get("decay_ratios", {}).get("win_rate", 0) * 100:.2f}% |

### 3.3 应对措施
"""
            for i, action in enumerate(decay_result.get("response_actions", []), 1):
                report += f"{i}. **{action['action']}**: {action['description']}\n"

        report += f"""
---

**报告生成**: 自动生成  
**发送对象**: 策略委员会, 风控部门  

"""
        return report

    def _count_signals(self, trade_records) -> int:
        """统计信号数量"""
        if isinstance(trade_records, pd.DataFrame):
            return len(trade_records) if not trade_records.empty else 0
        elif isinstance(trade_records, dict):
            return 1 if trade_records else 0
        else:
            return 0

    def _count_buy_trades(self, trade_records) -> int:
        """统计买入交易数量"""
        if isinstance(trade_records, pd.DataFrame):
            if trade_records.empty:
                return 0
            return len(
                trade_records[trade_records.get("execution_price", pd.Series()).notna()]
            )
        elif isinstance(trade_records, dict):
            return 1 if trade_records.get("execution_price") else 0
        else:
            return 0

    def _count_sell_trades(self, trade_records) -> int:
        """统计卖出交易数量"""
        if isinstance(trade_records, pd.DataFrame):
            if trade_records.empty:
                return 0
            return len(
                trade_records[trade_records.get("sell_price", pd.Series()).notna()]
            )
        elif isinstance(trade_records, dict):
            return 1 if trade_records.get("sell_price") else 0
        else:
            return 0

    def _count_profit_trades(self, trade_records: pd.DataFrame) -> int:
        """统计盈利交易数量"""
        if trade_records.empty or "profit_loss_pct" not in trade_records.columns:
            return 0
        return (trade_records["profit_loss_pct"] > 0).sum()

    def _count_loss_trades(self, trade_records: pd.DataFrame) -> int:
        """统计亏损交易数量"""
        if trade_records.empty or "profit_loss_pct" not in trade_records.columns:
            return 0
        return (trade_records["profit_loss_pct"] < 0).sum()

    def _calculate_holding_value(self, holdings: pd.DataFrame) -> float:
        """计算持仓市值"""
        if holdings.empty:
            return 0.0
        return holdings.get("market_value", pd.Series([0])).sum()

    def _get_week_range(self, end_date: str) -> str:
        """获取周范围"""
        date = pd.to_datetime(end_date)
        week_start = date - pd.Timedelta(days=date.weekday())
        return f"{week_start.strftime('%Y-%m-%d')} ~ {end_date}"

    def _get_month(self, end_date: str) -> str:
        """获取月份"""
        date = pd.to_datetime(end_date)
        return date.strftime("%Y年%m月")

    def _compare_metric(self, current: float, baseline: float) -> str:
        """对比指标"""
        if current >= baseline:
            return "达标"
        elif current >= baseline * 0.8:
            return "观察"
        else:
            return "警告"

    def _compare_drawdown(self, current: float, baseline: float) -> str:
        """对比回撤"""
        if current <= baseline:
            return "达标"
        elif current <= baseline * 1.5:
            return "观察"
        else:
            return "警告"

    def _compare_sharpe(self, current: float, baseline: float) -> str:
        """对比夏普比率"""
        if current >= baseline:
            return "达标"
        elif current >= baseline * 0.5:
            return "观察"
        else:
            return "警告"


if __name__ == "__main__":
    generator = ReportGenerator()

    test_trade_records = pd.DataFrame(
        [
            {
                "signal_date": "2024-01-01",
                "signal_stock_code": "000001.SZ",
                "profit_loss_pct": 0.05,
            }
        ]
    )

    test_validation = {
        "annual_return": 350,
        "cumulative_return": 15,
        "win_rate": 85,
        "profit_loss_ratio": 20,
        "max_drawdown": 3.0,
        "sharpe_ratio": 18,
        "alert_level": "green",
        "triggered_metrics": [],
    }

    report = generator.generate_daily_report(
        "2024-01-01", test_trade_records, pd.DataFrame(), test_validation
    )

    print(report)
