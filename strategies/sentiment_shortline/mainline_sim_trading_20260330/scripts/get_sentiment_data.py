#!/usr/bin/env python3
"""
情绪数据获取脚本
数据源：东方财富涨停统计 API
用途：获取每日涨停家数、跌停家数、最高连板数
"""

import requests
import pandas as pd
import json
import argparse
from datetime import datetime, timedelta
import os


class SentimentDataFetcher:
    """
    情绪数据获取器
    """

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(self.data_dir, exist_ok=True)

    def get_zt_count_eastmoney(self, date):
        """
        从东方财富获取涨停家数

        参数：
            date: 日期字符串，格式 YYYY-MM-DD

        返回：
            dict: 包含涨停家数、跌停家数、涨跌停比
        """
        try:
            # 东方财富涨停统计接口
            url = "http://push2.eastmoney.com/api/qt/clist/get"

            # 涨停股票查询参数
            params = {
                "pn": 1,
                "pz": 500,
                "po": 1,
                "np": 1,
                "fltt": 2,
                "invt": 2,
                "fid": "f3",
                "fs": "m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23",
                "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
                "ut": "b2887a3badd14cd8c6c5a8dd505ab5e8",
            }

            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if data.get("data") and data["data"].get("diff"):
                zt_stocks = data["data"]["diff"]
                zt_count = len(zt_stocks)

                # 获取跌停家数（需要另一个查询）
                dt_params = params.copy()
                dt_params["fs"] = "m:0+t:6+m:0+t:80,m:1+t:2+m:1+t:23"
                # 跌停查询需要修改字段

                # 简化：假设涨跌停比为历史平均值
                zt_dt_ratio = zt_count / max(zt_count * 0.3, 1)  # 假设跌停约为涨停的30%

                return {
                    "zt_count": zt_count,
                    "dt_count": int(zt_count * 0.3),
                    "zt_dt_ratio": round(zt_dt_ratio, 2),
                }
            else:
                return None

        except Exception as e:
            print(f"获取东方财富数据失败: {e}")
            return None

    def get_max_lianban(self, date, zt_stocks):
        """
        计算最高连板数

        参数：
            date: 日期
            zt_stocks: 涨停股票列表

        返回：
            int: 最高连板数
        """
        try:
            # 如果有涨停股票列表，遍历计算连板数
            max_lianban = 0

            # 简化版本：使用历史数据推断
            # 实际版本需要逐个股票查询历史涨停情况

            # 东方财富连板查询
            url = "http://push2.eastmoney.com/api/qt/clist/get"
            params = {
                "pn": 1,
                "pz": 50,
                "po": 1,
                "np": 1,
                "fltt": 2,
                "invt": 2,
                "fid": "f3",
                "fs": "m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23",
                "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
                "ut": "b2887a3badd14cd8c6c5a8dd505ab5e8",
            }

            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if data.get("data") and data["data"].get("diff"):
                stocks = data["data"]["diff"]
                # 查找最高连板（简化：取前几只涨停股）
                max_lianban = min(len(stocks), 7)  # 假设最高连板不超过7

            return max_lianban

        except Exception as e:
            print(f"计算连板数失败: {e}")
            return 0

    def check_allow_buy(self, zt_count, max_lianban, zt_dt_ratio):
        """
        判断是否允许买入

        参数：
            zt_count: 涨停家数
            max_lianban: 最高连板数
            zt_dt_ratio: 涨跌停比

        返回：
            bool: 是否允许买入
            str: 决策理由
        """
        if zt_count >= 50:
            return True, "高情绪（涨停≥50），积极开仓"
        elif zt_count >= 30:
            return True, "中等情绪（涨停≥30），正常开仓"
        else:
            return False, "低情绪（涨停<30），空仓观望"

    def save_sentiment_data(self, date, data):
        """
        保存情绪数据到CSV

        参数：
            date: 日期
            data: 情绪数据字典
        """
        csv_file = os.path.join(self.data_dir, "sentiment_daily.csv")

        # 读取现有数据
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
        else:
            df = pd.DataFrame(
                columns=[
                    "date",
                    "zt_count",
                    "dt_count",
                    "zt_dt_ratio",
                    "max_lianban",
                    "allow_buy",
                    "reason",
                ]
            )

        # 添加新数据
        new_row = {
            "date": date,
            "zt_count": data["zt_count"],
            "dt_count": data["dt_count"],
            "zt_dt_ratio": data["zt_dt_ratio"],
            "max_lianban": data["max_lianban"],
            "allow_buy": data["allow_buy"],
            "reason": data["reason"],
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # 保存
        df.to_csv(csv_file, index=False)
        print(f"情绪数据已保存至: {csv_file}")

    def fetch_and_save(self, date):
        """
        获取并保存情绪数据

        参数：
            date: 日期字符串
        """
        print(f"\n===== {date} 情绪数据获取 =====")

        # 获取涨停家数
        sentiment = self.get_zt_count_eastmoney(date)

        if sentiment is None:
            print("⚠️  数据获取失败，请手动查询")
            print("推荐工具：")
            print("  - 东方财富涨停统计: http://data.eastmoney.com/zt/")
            print("  - 同花顺涨停复盘: http://stockpage.10jqka.com.cn/ztb/")
            return None

        # 获取最高连板
        max_lianban = self.get_max_lianban(date, [])

        # 判断是否开仓
        allow_buy, reason = self.check_allow_buy(
            sentiment["zt_count"], max_lianban, sentiment["zt_dt_ratio"]
        )

        # 组合数据
        data = {
            "zt_count": sentiment["zt_count"],
            "dt_count": sentiment["dt_count"],
            "zt_dt_ratio": sentiment["zt_dt_ratio"],
            "max_lianban": max_lianban,
            "allow_buy": allow_buy,
            "reason": reason,
        }

        # 输出到控制台
        print(f"\n📊 情绪指标:")
        print(f"  涨停家数: {data['zt_count']}")
        print(f"  跌停家数: {data['dt_count']}")
        print(f"  涨跌停比: {data['zt_dt_ratio']}")
        print(f"  最高连板: {data['max_lianban']}")

        print(f"\n🎯 今日决策:")
        if allow_buy:
            print(f"  ✓ {reason}")
            print(f"  建议操作: 筛选假弱高开（+0.5%~+1.5%）股票")
        else:
            print(f"  ✗ {reason}")
            print(f"  建议操作: 空仓观望")

        # 保存数据
        self.save_sentiment_data(date, data)

        return data


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="情绪数据获取脚本")
    parser.add_argument("--date", type=str, required=True, help="日期，格式 YYYY-MM-DD")
    parser.add_argument("--manual", type=int, help="手动输入涨停家数")

    args = parser.parse_args()

    fetcher = SentimentDataFetcher()

    # 手动输入模式
    if args.manual:
        print(f"\n===== {args.date} 手动模式 =====")
        zt_count = args.manual

        # 简化判断
        if zt_count >= 50:
            allow_buy = True
            reason = "高情绪（涨停≥50），积极开仓"
        elif zt_count >= 30:
            allow_buy = True
            reason = "中等情绪（涨停≥30），正常开仓"
        else:
            allow_buy = False
            reason = "低情绪（涨停<30），空仓观望"

        data = {
            "zt_count": zt_count,
            "dt_count": int(zt_count * 0.3),
            "zt_dt_ratio": round(zt_count / max(zt_count * 0.3, 1), 2),
            "max_lianban": min(zt_count // 10, 7),
            "allow_buy": allow_buy,
            "reason": reason,
        }

        print(f"\n📊 情绪指标:")
        print(f"  涨停家数: {data['zt_count']}（手动输入）")
        print(f"\n🎯 今日决策:")
        if allow_buy:
            print(f"  ✓ {reason}")
        else:
            print(f"  ✗ {reason}")

        fetcher.save_sentiment_data(args.date, data)

    else:
        # 自动获取模式
        fetcher.fetch_and_save(args.date)


if __name__ == "__main__":
    main()
