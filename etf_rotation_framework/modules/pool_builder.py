# -*- coding: utf-8 -*-
"""
ETF候选池构建模块
基于notebook 66和86的逻辑
"""

import pandas as pd
import numpy as np
from datetime import datetime, date
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings

warnings.filterwarnings("ignore")


class ETFPoolBuilder:
    """ETF候选池构建器"""

    def __init__(self, config=None):
        """
        初始化候选池构建器

        Args:
            config: 配置字典，如果为None则使用默认配置
        """
        from config import POOL_CONFIG

        self.config = config or POOL_CONFIG
        self.etf_list = None
        self.filtered_etfs = None
        self.cluster_result = None
        self.final_pool = None

    def build_pool(self, get_all_securities_func, get_price_func, verbose=True):
        """
        构建ETF候选池

        Args:
            get_all_securities_func: 获取所有证券的函数
            get_price_func: 获取价格数据的函数
            verbose: 是否打印详细信息

        Returns:
            pd.DataFrame: 最终ETF候选池
        """
        if verbose:
            print("=" * 50)
            print("开始构建ETF候选池")
            print("=" * 50)

        # 步骤1: 获取所有ETF
        self.etf_list = self._get_etf_list(get_all_securities_func)
        if verbose:
            print(f"步骤1: 获取到 {len(self.etf_list)} 只ETF")

        # 步骤2: 流动性过滤
        self.filtered_etfs = self._filter_by_liquidity(get_price_func, verbose)
        if verbose:
            print(f"步骤2: 流动性过滤后剩余 {len(self.filtered_etfs)} 只ETF")

        # 步骤3: 获取价格数据用于聚类
        prices = self._get_price_data(get_price_func)
        if verbose:
            print(f"步骤3: 获取价格数据完成，共 {len(prices)} 天")

        # 步骤4: KMeans聚类
        self.cluster_result = self._cluster_etfs(prices, verbose)
        if verbose:
            print(
                f"步骤4: 聚类完成，共 {self.cluster_result['cluster_id'].nunique()} 个簇"
            )

        # 步骤5: 相关性过滤
        self.final_pool = self._filter_by_correlation(prices, verbose)
        if verbose:
            print(f"步骤5: 相关性过滤后最终候选池 {len(self.final_pool)} 只ETF")
            print("=" * 50)
            print("ETF候选池构建完成")
            print("=" * 50)

        return self.final_pool

    def _get_etf_list(self, get_all_securities_func):
        """获取所有ETF列表"""
        df = get_all_securities(["etf"])
        df = df.reset_index().rename(columns={"index": "code"})

        # 过滤成立时间
        threshold_date = datetime.strptime(
            self.config["start_date_threshold"], "%Y-%m-%d"
        ).date()
        df = df[df["start_date"] < threshold_date]

        # 过滤已退市ETF
        if self.config["end_date_check"]:
            df = df[df["end_date"] >= datetime.today().date()]

        return df

    def _filter_by_liquidity(self, get_price_func, verbose=True):
        """按流动性过滤"""
        codes = []
        min_volume = self.config["min_avg_volume"]
        volume_window = self.config["volume_window"]

        today = str(datetime.today().date())

        for _, row in self.etf_list.iterrows():
            code = row["code"]
            try:
                price = get_price_func(
                    code, end_date=today, count=volume_window
                ).dropna()
                if len(price) < volume_window * 0.8:  # 数据不足80%则跳过
                    continue

                avg_money = price["money"].mean()

                if avg_money > min_volume:
                    price["pchg"] = price["close"].pct_change()
                    codes.append(
                        {
                            "code": code,
                            "display_name": row["display_name"],
                            "start_date": row["start_date"],
                            "end_date": row["end_date"],
                            "avg_volume": avg_money / 1e8,  # 转换为亿
                            "pchg_mean": price["pchg"].mean(),
                            "pchg_std": price["pchg"].std(),
                        }
                    )
                elif verbose:
                    print(
                        f"排除 {code} {row['display_name']}, 成交额均值 {avg_money / 1e7:.2f}kw"
                    )
            except Exception as e:
                if verbose:
                    print(f"处理 {code} 时出错: {e}")
                continue

        return pd.DataFrame(codes)

    def _get_price_data(self, get_price_func):
        """获取价格数据用于聚类"""
        price_window = self.config["price_window"]
        today = str(datetime.today().date())

        prices = []
        valid_codes = []

        for code in self.filtered_etfs["code"]:
            try:
                price = get_price_func(
                    code, fields="close", end_date=today, count=price_window
                )
                if len(price) >= price_window * 0.8:
                    price["pchg"] = price["close"].pct_change()
                    prices.append(price["pchg"].values)
                    valid_codes.append(code)
            except:
                continue

        prices = np.array(prices).T
        prices = pd.DataFrame(prices, columns=valid_codes).iloc[1:]

        # 更新filtered_etfs只保留有效代码
        self.filtered_etfs = self.filtered_etfs[
            self.filtered_etfs["code"].isin(valid_codes)
        ]

        return prices

    def _cluster_etfs(self, prices, verbose=True):
        """使用KMeans对ETF进行聚类"""
        x = prices.T
        n_clusters = self.config["n_clusters"]

        # 如果ETF数量少于簇数，调整簇数
        if len(x) < n_clusters:
            n_clusters = max(2, len(x) // 2)

        cluster = KMeans(
            n_clusters=n_clusters, random_state=self.config["random_state"]
        )
        y_pred = cluster.fit_predict(x)

        # 计算轮廓系数
        silhouette = silhouette_score(x, y_pred)
        if verbose:
            print(f"聚类轮廓系数: {silhouette:.4f}")

        x["cluster_id"] = y_pred
        x = x.reset_index().rename(columns={"index": "code"})

        # 合并聚类结果
        result = self.filtered_etfs.merge(x[["code", "cluster_id"]], on="code")
        result = result.sort_values(["cluster_id", "start_date"])

        return result

    def _filter_by_correlation(self, prices, verbose=True):
        """使用相关系数过滤相似ETF"""
        corr_threshold = self.config["corr_threshold"]

        # 每个簇保留最早成立的ETF
        pool = self.cluster_result.groupby("cluster_id").first().reset_index()

        # 计算相关系数矩阵
        pool_codes = pool["code"].tolist()
        available_codes = [c for c in pool_codes if c in prices.columns]

        if len(available_codes) < 2:
            return pool

        corr = prices[available_codes].corr()

        # 找出高相关ETF对
        union = []
        for i in available_codes:
            for j in available_codes:
                if i >= j:
                    continue
                if corr.loc[i, j] > corr_threshold:
                    # 检查是否已在某个组中
                    found = False
                    for group in union:
                        if i in group or j in group:
                            group.add(i)
                            group.add(j)
                            found = True
                            break
                    if not found:
                        union.append({i, j})

        # 对每个高相关组，只保留最早成立的
        codes_to_remove = set()
        for group in union:
            group_list = list(group)
            group_df = pool[pool["code"].isin(group_list)]
            if len(group_df) > 1:
                # 保留最早成立的
                earliest = group_df.sort_values("start_date").iloc[0]
                for code in group_list:
                    if code != earliest["code"]:
                        codes_to_remove.add(code)

        # 移除高相关的ETF
        final_pool = pool[~pool["code"].isin(codes_to_remove)].copy()

        if verbose and codes_to_remove:
            print(f"相关性过滤移除了 {len(codes_to_remove)} 只ETF")

        return final_pool

    def get_pool_codes(self):
        """获取候选池ETF代码列表"""
        if self.final_pool is None:
            raise ValueError("请先调用build_pool构建候选池")
        return self.final_pool["code"].tolist()

    def save_pool(self, filepath):
        """保存候选池到文件"""
        if self.final_pool is None:
            raise ValueError("请先调用build_pool构建候选池")
        self.final_pool.to_csv(filepath, index=False)
        print(f"候选池已保存到 {filepath}")

    def load_pool(self, filepath):
        """从文件加载候选池"""
        self.final_pool = pd.read_csv(filepath)
        print(f"已从 {filepath} 加载候选池，共 {len(self.final_pool)} 只ETF")
        return self.final_pool
