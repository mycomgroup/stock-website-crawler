#!/usr/bin/env python3
"""
实盘情绪监控模块

用于实盘环境下的情绪指标监控和告警。

功能:
1. 从免费数据源获取涨停家数
2. 计算情绪指标
3. 定时任务调度
4. 告警通知（微信/邮件/钉钉）

使用方法:
    python live_sentiment_monitor.py --threshold 30 --notify wechat

依赖:
    pip install requests schedule
"""

import requests
import json
import time
import argparse
from datetime import datetime, timedelta
from typing import Dict, Optional, List


# ============ 数据源配置 ============


class SentimentDataSource:
    """情绪数据源基类"""

    def get_zt_count(self, date: str) -> int:
        raise NotImplementedError

    def get_dt_count(self, date: str) -> int:
        raise NotImplementedError


class EastMoneyDataSource(SentimentDataSource):
    """
    东方财富数据源

    数据接口:
    - 涨停板: http://push2.eastmoney.com/api/qt/clist/get
    - 跌停板: 同上，筛选条件不同
    """

    def __init__(self):
        self.zt_url = "http://push2.eastmoney.com/api/qt/clist/get"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def get_zt_count(self, date: str = None) -> int:
        """
        获取涨停家数

        参数:
            date: 日期，格式 '2024-01-01'，默认今日

        返回:
            涨停股票数量
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        params = {
            "fid": "f3",
            "po": "1",
            "pz": "500",
            "pn": "1",
            "np": "1",
            "fltt": "2",
            "invt": "2",
            "fs": "m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23",
            "fields": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87",
            # 涨停筛选条件
            "ut": "b2884a393a59ad64002292a3e90d46a5",
        }

        try:
            response = requests.get(
                self.zt_url, params=params, headers=self.headers, timeout=10
            )
            data = response.json()

            if data.get("data") and data["data"].get("diff"):
                # 筛选涨停股（涨幅>=9.8%）
                zt_stocks = [
                    s for s in data["data"]["diff"] if float(s.get("f3", 0)) >= 9.8
                ]
                return len(zt_stocks)
            return 0
        except Exception as e:
            print(f"获取涨停数据失败: {e}")
            return 0

    def get_dt_count(self, date: str = None) -> int:
        """
        获取跌停家数

        参数:
            date: 日期

        返回:
            跌停股票数量
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        params = {
            "fid": "f3",
            "po": "1",
            "pz": "500",
            "pn": "1",
            "np": "1",
            "fltt": "2",
            "invt": "2",
            "fs": "m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23",
            "fields": "f12,f14,f2,f3",
        }

        try:
            response = requests.get(
                self.zt_url, params=params, headers=self.headers, timeout=10
            )
            data = response.json()

            if data.get("data") and data["data"].get("diff"):
                # 筛选跌停股（涨幅<=-9.8%）
                dt_stocks = [
                    s for s in data["data"]["diff"] if float(s.get("f3", 0)) <= -9.8
                ]
                return len(dt_stocks)
            return 0
        except Exception as e:
            print(f"获取跌停数据失败: {e}")
            return 0


class TushareDataSource(SentimentDataSource):
    """
    Tushare数据源（需要Token）

    使用方法:
        1. 注册Tushare: https://tushare.pro/
        2. 获取Token
        3. 设置环境变量: export TUSHARE_TOKEN=your_token
    """

    def __init__(self, token: str = None):
        self.token = token
        if token:
            import tushare as ts

            ts.set_token(token)
            self.pro = ts.pro_api()

    def get_zt_count(self, date: str = None) -> int:
        if date is None:
            date = datetime.now().strftime("%Y%m")

        try:
            df = self.pro.limit_list(trade_date=date.replace("-", ""), limit_type="U")
            return len(df) if df is not None else 0
        except:
            return 0

    def get_dt_count(self, date: str = None) -> int:
        if date is None:
            date = datetime.now().strftime("%Y%m")

        try:
            df = self.pro.limit_list(trade_date=date.replace("-", ""), limit_type="D")
            return len(df) if df is not None else 0
        except:
            return 0


# ============ 告警通知 ============


class Notifier:
    """告警通知基类"""

    def send(self, title: str, content: str) -> bool:
        raise NotImplementedError


class WeChatNotifier(Notifier):
    """
    微信通知（Server酱）

    配置:
        1. 注册Server酱: https://sct.ftqq.com/
        2. 获取SendKey
        3. 设置环境变量: export SERVERCHAN_KEY=your_key
    """

    def __init__(self, send_key: str):
        self.send_key = send_key
        self.url = f"https://sctapi.ftqq.com/{send_key}.send"

    def send(self, title: str, content: str) -> bool:
        try:
            data = {"title": title, "desp": content}
            response = requests.post(self.url, data=data, timeout=10)
            return response.json().get("code") == 0
        except Exception as e:
            print(f"发送微信通知失败: {e}")
            return False


class DingTalkNotifier(Notifier):
    """
    钉钉机器人通知

    配置:
        1. 创建钉钉群机器人
        2. 获取Webhook URL
    """

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, title: str, content: str) -> bool:
        try:
            data = {
                "msgtype": "markdown",
                "markdown": {"title": title, "text": content},
            }
            response = requests.post(
                self.webhook_url,
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            return response.json().get("errcode") == 0
        except Exception as e:
            print(f"发送钉钉通知失败: {e}")
            return False


class EmailNotifier(Notifier):
    """邮件通知（SMTP）"""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        sender: str,
        password: str,
        receiver: str,
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender = sender
        self.password = password
        self.receiver = receiver

    def send(self, title: str, content: str) -> bool:
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            msg = MIMEMultipart()
            msg["From"] = self.sender
            msg["To"] = self.receiver
            msg["Subject"] = title
            msg.attach(MIMEText(content, "plain", "utf-8"))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receiver, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"发送邮件失败: {e}")
            return False


# ============ 监控主程序 ============


class SentimentMonitor:
    """情绪监控器"""

    def __init__(
        self,
        data_source: SentimentDataSource,
        notifier: Notifier = None,
        threshold: int = 30,
    ):
        self.data_source = data_source
        self.notifier = notifier
        self.threshold = threshold
        self.history = []

    def check(self) -> Dict:
        """
        检查当前情绪状态

        返回:
            {
                'zt_count': 涨停家数,
                'dt_count': 跌停家数,
                'zt_dt_ratio': 涨跌停比,
                'status': 'good'/'normal'/'bad',
                'action': '开仓'/'谨慎'/'空仓'
            }
        """
        zt_count = self.data_source.get_zt_count()
        dt_count = self.data_source.get_dt_count()
        zt_dt_ratio = zt_count / max(dt_count, 1)

        # 判断状态
        if zt_count >= 50:
            status = "good"
            action = "积极开仓"
        elif zt_count >= self.threshold:
            status = "normal"
            action = "正常开仓"
        else:
            status = "bad"
            action = "空仓观望"

        result = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "zt_count": zt_count,
            "dt_count": dt_count,
            "zt_dt_ratio": round(zt_dt_ratio, 2),
            "status": status,
            "action": action,
            "threshold": self.threshold,
        }

        self.history.append(result)
        return result

    def alert(self, result: Dict) -> bool:
        """
        发送告警

        参数:
            result: check()返回的结果

        返回:
            是否发送成功
        """
        if self.notifier is None:
            return False

        title = f"情绪监控: {result['action']}"
        content = f"""
## 情绪监控报告

**时间**: {result["time"]}

**涨停家数**: {result["zt_count"]}

**跌停家数**: {result["dt_count"]}

**涨跌停比**: {result["zt_dt_ratio"]}

**状态**: {result["status"]}

**建议操作**: {result["action"]}

**阈值**: {result["threshold"]}
"""
        return self.notifier.send(title, content)

    def run_schedule(self, times: List[str] = ["09:25", "13:00", "14:30"]):
        """
        定时运行监控

        参数:
            times: 检查时间点列表，如 ['09:25', '13:00']
        """
        import schedule

        for t in times:
            schedule.every().day.at(t).do(self._run_check)

        print(f"监控已启动，将在 {times} 执行检查...")

        while True:
            schedule.run_pending()
            time.sleep(60)

    def _run_check(self):
        """执行检查并发送告警"""
        result = self.check()
        print(
            f"\n{result['time']} - 涨停: {result['zt_count']}, 状态: {result['status']}, 建议: {result['action']}"
        )

        # 低情绪告警
        if result["status"] == "bad":
            self.alert(result)


def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(description="情绪监控")
    parser.add_argument("--threshold", type=int, default=30, help="情绪阈值")
    parser.add_argument(
        "--notify",
        choices=["wechat", "dingtalk", "email", "none"],
        default="none",
        help="通知方式",
    )
    parser.add_argument("--once", action="store_true", help="只执行一次")
    args = parser.parse_args()

    # 创建数据源
    data_source = EastMoneyDataSource()

    # 创建通知器
    notifier = None
    if args.notify == "wechat":
        import os

        key = os.environ.get("SERVERCHAN_KEY")
        if key:
            notifier = WeChatNotifier(key)
    elif args.notify == "dingtalk":
        import os

        webhook = os.environ.get("DINGTALK_WEBHOOK")
        if webhook:
            notifier = DingTalkNotifier(webhook)

    # 创建监控器
    monitor = SentimentMonitor(
        data_source=data_source, notifier=notifier, threshold=args.threshold
    )

    if args.once:
        # 只执行一次
        result = monitor.check()
        print(f"\n{'=' * 50}")
        print(f"时间: {result['time']}")
        print(f"涨停家数: {result['zt_count']}")
        print(f"跌停家数: {result['dt_count']}")
        print(f"涨跌停比: {result['zt_dt_ratio']}")
        print(f"状态: {result['status']}")
        print(f"建议操作: {result['action']}")
        print(f"{'=' * 50}")
    else:
        # 定时运行
        monitor.run_schedule()


if __name__ == "__main__":
    main()
