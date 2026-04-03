"""
数据管理核心模块
负责数据的获取、存储、质量检查和更新
"""

import sqlite3
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataManager:
    """数据管理核心类"""

    def __init__(self, db_path: str = "secondboard_oos.db"):
        self.db_path = db_path
        self.conn = None
        self._init_database()

    def _init_database(self):
        """初始化数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()
        logger.info(f"数据库初始化完成: {self.db_path}")

    def _create_tables(self):
        """创建数据表"""
        cursor = self.conn.cursor()

        # 行情数据表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_price (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code TEXT NOT NULL,
                trade_date DATE NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                amount REAL,
                pct_change REAL,
                turnover_rate REAL,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(stock_code, trade_date)
            )
        """)

        # 情绪数据表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emotion_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_date DATE NOT NULL UNIQUE,
                limit_up_count INTEGER,
                limit_down_count INTEGER,
                limit_up_limit_down_ratio REAL,
                max_consecutive_board INTEGER,
                board_distribution TEXT,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 广度数据表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS breadth_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trade_date DATE NOT NULL,
                index_code TEXT NOT NULL,
                above_ma_20_pct REAL,
                above_count INTEGER,
                total_count INTEGER,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(trade_date, index_code)
            )
        """)

        # 交易记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trade_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_date DATE,
                signal_stock_code TEXT,
                signal_price REAL,
                execution_date DATE,
                execution_price REAL,
                execution_volume INTEGER,
                sell_date DATE,
                sell_price REAL,
                sell_reason TEXT,
                profit_loss_pct REAL,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 数据质量检查记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_quality_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                check_date DATE NOT NULL,
                data_type TEXT NOT NULL,
                quality_score REAL,
                quality_level TEXT,
                completeness_score REAL,
                accuracy_score REAL,
                timeliness_score REAL,
                issues TEXT,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 策略验证结果表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS validation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                validation_date DATE NOT NULL,
                validation_type TEXT NOT NULL,
                window_type TEXT,
                annual_return REAL,
                cumulative_return REAL,
                win_rate REAL,
                profit_loss_ratio REAL,
                max_drawdown REAL,
                sharpe_ratio REAL,
                alert_level TEXT,
                triggered_metrics TEXT,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

    def save_price_data(self, data: pd.DataFrame) -> bool:
        """
        保存行情数据

        参数:
        - data: DataFrame，包含行情数据

        返回:
        - success: 是否成功
        """
        try:
            for idx, row in data.iterrows():
                self.conn.execute(
                    """
                    INSERT OR REPLACE INTO daily_price
                    (stock_code, trade_date, open, high, low, close, 
                     volume, amount, pct_change, turnover_rate)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        row.get("stock_code"),
                        row.get("trade_date"),
                        row.get("open"),
                        row.get("high"),
                        row.get("low"),
                        row.get("close"),
                        row.get("volume"),
                        row.get("amount"),
                        row.get("pct_change"),
                        row.get("turnover_rate"),
                    ),
                )

            self.conn.commit()
            logger.info(f"保存行情数据成功: {len(data)}条记录")
            return True

        except Exception as e:
            logger.error(f"保存行情数据失败: {e}")
            return False

    def save_emotion_data(self, data: Dict) -> bool:
        """
        保存情绪数据

        参数:
        - data: 字典，包含情绪指标

        返回:
        - success: 是否成功
        """
        try:
            self.conn.execute(
                """
                INSERT OR REPLACE INTO emotion_metrics
                (trade_date, limit_up_count, limit_down_count, 
                 limit_up_limit_down_ratio, max_consecutive_board,
                 board_distribution)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    data.get("trade_date"),
                    data.get("limit_up_count"),
                    data.get("limit_down_count"),
                    data.get("limit_up_limit_down_ratio"),
                    data.get("max_consecutive_board"),
                    json.dumps(data.get("board_distribution", {})),
                ),
            )

            self.conn.commit()
            logger.info(f"保存情绪数据成功: {data.get('trade_date')}")
            return True

        except Exception as e:
            logger.error(f"保存情绪数据失败: {e}")
            return False

    def save_breadth_data(self, data: Dict, index_code: str) -> bool:
        """
        保存广度数据

        参数:
        - data: 字典，包含广度指标
        - index_code: 指数代码

        返回:
        - success: 是否成功
        """
        try:
            self.conn.execute(
                """
                INSERT OR REPLACE INTO breadth_metrics
                (trade_date, index_code, above_ma_20_pct, 
                 above_count, total_count)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    data.get("trade_date"),
                    index_code,
                    data.get("above_ma_20_pct"),
                    data.get("above_count"),
                    data.get("total_count"),
                ),
            )

            self.conn.commit()
            logger.info(f"保存广度数据成功: {data.get('trade_date')} - {index_code}")
            return True

        except Exception as e:
            logger.error(f"保存广度数据失败: {e}")
            return False

    def save_trade_record(self, record: Dict) -> bool:
        """
        保存交易记录

        参数:
        - record: 字典，包含交易记录

        返回:
        - success: 是否成功
        """
        try:
            self.conn.execute(
                """
                INSERT INTO trade_records
                (signal_date, signal_stock_code, signal_price,
                 execution_date, execution_price, execution_volume,
                 sell_date, sell_price, sell_reason, profit_loss_pct)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    record.get("signal_date"),
                    record.get("signal_stock_code"),
                    record.get("signal_price"),
                    record.get("execution_date"),
                    record.get("execution_price"),
                    record.get("execution_volume"),
                    record.get("sell_date"),
                    record.get("sell_price"),
                    record.get("sell_reason"),
                    record.get("profit_loss_pct"),
                ),
            )

            self.conn.commit()
            logger.info(f"保存交易记录成功: {record.get('signal_stock_code')}")
            return True

        except Exception as e:
            logger.error(f"保存交易记录失败: {e}")
            return False

    def query_price_data(
        self, start_date: str, end_date: str, stock_codes: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        查询行情数据

        参数:
        - start_date: 开始日期
        - end_date: 结束日期
        - stock_codes: 股票代码列表（可选）

        返回:
        - DataFrame: 行情数据
        """
        try:
            if stock_codes:
                placeholders = ",".join(["?"] * len(stock_codes))
                query = f"""
                    SELECT * FROM daily_price
                    WHERE trade_date BETWEEN ? AND ?
                    AND stock_code IN ({placeholders})
                """
                params = [start_date, end_date] + stock_codes
            else:
                query = """
                    SELECT * FROM daily_price
                    WHERE trade_date BETWEEN ? AND ?
                """
                params = [start_date, end_date]

            df = pd.read_sql_query(query, self.conn, params=params)
            logger.info(f"查询行情数据成功: {len(df)}条记录")
            return df

        except Exception as e:
            logger.error(f"查询行情数据失败: {e}")
            return pd.DataFrame()

    def query_emotion_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        查询情绪数据

        参数:
        - start_date: 开始日期
        - end_date: 结束日期

        返回:
        - DataFrame: 情绪数据
        """
        try:
            query = """
                SELECT * FROM emotion_metrics
                WHERE trade_date BETWEEN ? AND ?
            """
            df = pd.read_sql_query(query, self.conn, params=[start_date, end_date])

            if "board_distribution" in df.columns:
                df["board_distribution"] = df["board_distribution"].apply(
                    lambda x: json.loads(x) if x else {}
                )

            logger.info(f"查询情绪数据成功: {len(df)}条记录")
            return df

        except Exception as e:
            logger.error(f"查询情绪数据失败: {e}")
            return pd.DataFrame()

    def query_trade_records(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        查询交易记录

        参数:
        - start_date: 开始日期
        - end_date: 结束日期

        返回:
        - DataFrame: 交易记录
        """
        try:
            query = """
                SELECT * FROM trade_records
                WHERE signal_date BETWEEN ? AND ?
                OR execution_date BETWEEN ? AND ?
            """
            df = pd.read_sql_query(
                query, self.conn, params=[start_date, end_date, start_date, end_date]
            )
            logger.info(f"查询交易记录成功: {len(df)}条记录")
            return df

        except Exception as e:
            logger.error(f"查询交易记录失败: {e}")
            return pd.DataFrame()

    def check_data_completeness(self, data_type: str, date: str) -> Dict:
        """
        检查数据完整性

        参数:
        - data_type: 数据类型
        - date: 日期

        返回:
        - completeness_report: 完整性报告
        """
        try:
            if data_type == "price":
                query = "SELECT COUNT(*) FROM daily_price WHERE trade_date = ?"
                expected_fields = ["open", "high", "low", "close", "volume"]

            elif data_type == "emotion":
                query = "SELECT COUNT(*) FROM emotion_metrics WHERE trade_date = ?"
                expected_fields = ["limit_up_count", "limit_down_count"]

            else:
                return {"is_complete": False, "error": "未知数据类型"}

            cursor = self.conn.cursor()
            cursor.execute(query, (date,))
            record_count = cursor.fetchone()[0]

            is_complete = record_count > 0

            return {
                "data_type": data_type,
                "date": date,
                "is_complete": is_complete,
                "record_count": record_count,
            }

        except Exception as e:
            logger.error(f"检查数据完整性失败: {e}")
            return {"is_complete": False, "error": str(e)}

    def log_data_quality(self, quality_report: Dict):
        """
        记录数据质量检查结果

        参数:
        - quality_report: 质量检查报告
        """
        try:
            self.conn.execute(
                """
                INSERT INTO data_quality_log
                (check_date, data_type, quality_score, quality_level,
                 completeness_score, accuracy_score, timeliness_score, issues)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    quality_report.get("check_date"),
                    quality_report.get("data_type"),
                    quality_report.get("quality_score"),
                    quality_report.get("quality_level"),
                    quality_report.get("completeness_score"),
                    quality_report.get("accuracy_score"),
                    quality_report.get("timeliness_score"),
                    json.dumps(quality_report.get("issues", [])),
                ),
            )

            self.conn.commit()

        except Exception as e:
            logger.error(f"记录数据质量失败: {e}")

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            logger.info("数据库连接已关闭")


if __name__ == "__main__":
    dm = DataManager("test_secondboard_oos.db")

    test_price_data = pd.DataFrame(
        [
            {
                "stock_code": "000001.SZ",
                "trade_date": "2024-01-01",
                "open": 10.0,
                "high": 10.5,
                "low": 9.8,
                "close": 10.2,
                "volume": 1000000,
                "amount": 10200000,
                "pct_change": 0.02,
                "turnover_rate": 0.05,
            }
        ]
    )

    dm.save_price_data(test_price_data)

    completeness = dm.check_data_completeness("price", "2024-01-01")
    print(f"数据完整性: {completeness}")

    dm.close()
