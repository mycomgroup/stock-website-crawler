"""
OOS验证系统主入口
整合所有模块，提供统一的API接口
"""

import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import argparse
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_manager import DataManager
from core.decay_detector import DecayDetector
from validation.validation_engine import ValidationEngine
from reports.report_generator import ReportGenerator


class OOSValidationSystem:
    """OOS验证系统集成类"""

    def __init__(self, db_path: str = "secondboard_oos.db"):
        """
        初始化OOS验证系统

        参数:
        - db_path: 数据库路径
        """
        self.db_path = db_path

        self.data_manager = DataManager(db_path)
        self.decay_detector = DecayDetector(
            {
                "annual_return": 394,
                "win_rate": 87.95,
                "max_drawdown": 0.60,
                "sharpe_ratio": 20,
                "profit_loss_ratio": 21.91,
            }
        )
        self.validation_engine = ValidationEngine(db_path)
        self.report_generator = ReportGenerator()

        logger.info(f"OOS验证系统初始化完成: {db_path}")

    def run_daily_validation(self, date: str, save_report: bool = True) -> dict:
        """
        执行日频验证

        参数:
        - date: 验证日期
        - save_report: 是否保存报告

        返回:
        - result: 验证结果
        """
        logger.info(f"执行日频验证: {date}")

        result = self.validation_engine.run_daily_validation(date)

        if save_report:
            trade_records = self.data_manager.query_trade_records(date, date)
            report = self.report_generator.generate_daily_report(
                date, trade_records, pd.DataFrame(), result
            )
            self._save_report("daily", date, report)

        logger.info(f"日频验证完成: {date} - 预警级别: {result['alert_level']}")
        return result

    def run_weekly_validation(self, end_date: str, save_report: bool = True) -> dict:
        """
        执行周频验证

        参数:
        - end_date: 周末日期
        - save_report: 是否保存报告

        返回:
        - result: 验证结果
        """
        logger.info(f"执行周频验证: {end_date}")

        result = self.validation_engine.run_weekly_validation(end_date)

        if save_report:
            start_date = self._get_week_start(end_date)
            trade_records = self.data_manager.query_trade_records(start_date, end_date)
            report = self.report_generator.generate_weekly_report(
                end_date, trade_records, result
            )
            self._save_report("weekly", end_date, report)

        logger.info(f"周频验证完成: {end_date} - 预警级别: {result['alert_level']}")
        return result

    def run_monthly_validation(self, end_date: str, save_report: bool = True) -> dict:
        """
        执行月频验证

        参数:
        - end_date: 月末日期
        - save_report: 是否保存报告

        返回:
        - result: 验证结果
        """
        logger.info(f"执行月频验证: {end_date}")

        result = self.validation_engine.run_monthly_validation(end_date)

        if save_report:
            start_date = self._get_month_start(end_date)
            trade_records = self.data_manager.query_trade_records(start_date, end_date)

            decay_result = result.get("decay_result", {})

            report = self.report_generator.generate_monthly_report(
                end_date, trade_records, result, decay_result
            )
            self._save_report("monthly", end_date, report)

        logger.info(f"月频验证完成: {end_date} - 预警级别: {result['alert_level']}")
        return result

    def add_trade_record(self, record: dict) -> bool:
        """
        添加交易记录

        参数:
        - record: 交易记录字典

        返回:
        - success: 是否成功
        """
        return self.data_manager.save_trade_record(record)

    def add_price_data(self, data: pd.DataFrame) -> bool:
        """
        添加行情数据

        参数:
        - data: 行情数据DataFrame

        返回:
        - success: 是否成功
        """
        return self.data_manager.save_price_data(data)

    def check_data_quality(self, data_type: str, date: str) -> dict:
        """
        检查数据质量

        参数:
        - data_type: 数据类型
        - date: 日期

        返回:
        - quality_report: 质量报告
        """
        return self.data_manager.check_data_completeness(data_type, date)

    def _save_report(self, report_type: str, date: str, report: str):
        """保存报告"""
        try:
            report_dir = f"reports/{report_type}"
            os.makedirs(report_dir, exist_ok=True)

            filename = f"{report_dir}/report_{date}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report)

            logger.info(f"报告已保存: {filename}")

        except Exception as e:
            logger.error(f"保存报告失败: {e}")

    def _get_week_start(self, end_date: str) -> str:
        """获取周初日期"""
        date = pd.to_datetime(end_date)
        week_start = date - timedelta(days=date.weekday())
        return week_start.strftime("%Y-%m-%d")

    def _get_month_start(self, end_date: str) -> str:
        """获取月初日期"""
        date = pd.to_datetime(end_date)
        month_start = date.replace(day=1)
        return month_start.strftime("%Y-%m-%d")

    def close(self):
        """关闭系统"""
        self.validation_engine.close()
        self.data_manager.close()
        logger.info("OOS验证系统已关闭")


def main():
    """主函数 - 命令行入口"""
    parser = argparse.ArgumentParser(description="二板接力策略OOS验证系统")
    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        choices=["daily", "weekly", "monthly", "test"],
        help="验证模式",
    )
    parser.add_argument(
        "--date",
        type=str,
        required=False,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="验证日期",
    )
    parser.add_argument(
        "--db", type=str, default="secondboard_oos.db", help="数据库路径"
    )

    args = parser.parse_args()

    system = OOSValidationSystem(args.db)

    try:
        if args.mode == "daily":
            result = system.run_daily_validation(args.date)
            print(f"\n日频验证完成:")
            print(f"  预警级别: {result['alert_level']}")
            print(f"  年化收益: {result.get('annual_return', 0):.2f}%")
            print(f"  胜率: {result.get('win_rate', 0):.2f}%")

        elif args.mode == "weekly":
            result = system.run_weekly_validation(args.date)
            print(f"\n周频验证完成:")
            print(f"  预警级别: {result['alert_level']}")
            print(f"  年化收益: {result.get('annual_return', 0):.2f}%")
            print(f"  夏普比率: {result.get('sharpe_ratio', 0):.2f}")

        elif args.mode == "monthly":
            result = system.run_monthly_validation(args.date)
            print(f"\n月频验证完成:")
            print(f"  预警级别: {result['alert_level']}")
            print(f"  年化收益: {result.get('annual_return', 0):.2f}%")
            print(f"  夏普比率: {result.get('sharpe_ratio', 0):.2f}")
            print(
                f"  衰退程度: {result.get('decay_result', {}).get('decay_degree', 'none')}"
            )

        elif args.mode == "test":
            print("\n运行测试验证...")

            test_trade = {
                "signal_date": "2024-01-01",
                "signal_stock_code": "000001.SZ",
                "signal_price": 10.0,
                "execution_date": "2024-01-01",
                "execution_price": 10.1,
                "execution_volume": 1000,
                "sell_date": "2024-01-02",
                "sell_price": 10.5,
                "sell_reason": "高位回落",
                "profit_loss_pct": 0.04,
            }
            system.add_trade_record(test_trade)

            result = system.run_daily_validation("2024-01-01")

            print(f"\n测试验证完成:")
            print(f"  预警级别: {result['alert_level']}")
            print(f"  累计收益: {result.get('cumulative_return', 0):.2f}%")
            print(f"  胜率: {result.get('win_rate', 0):.2f}%")

    except Exception as e:
        logger.error(f"验证失败: {e}")
        import traceback

        traceback.print_exc()

    finally:
        system.close()


if __name__ == "__main__":
    main()
