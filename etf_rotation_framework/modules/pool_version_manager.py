# -*- coding: utf-8 -*-
"""
候选池版本管理模块
用于版本化管理ETF候选池
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
from pathlib import Path


class PoolVersionManager:
    """候选池版本管理器"""

    def __init__(self, base_dir="./pool_versions"):
        """
        初始化版本管理器

        Args:
            base_dir: 版本存储基础目录
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.base_dir / "metadata.json"
        self.metadata = self._load_metadata()

    def _load_metadata(self):
        """加载元数据"""
        if self.metadata_file.exists():
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"versions": [], "latest_version": None}

    def _save_metadata(self):
        """保存元数据"""
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def create_version(self, pool_df, config, description="", tags=None):
        """
        创建新版本

        Args:
            pool_df: 候选池DataFrame
            config: 配置参数
            description: 版本描述
            tags: 标签列表

        Returns:
            str: 版本ID
        """
        # 生成版本ID
        version_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        version_dir = self.base_dir / version_id
        version_dir.mkdir(parents=True, exist_ok=True)

        # 保存候选池数据
        pool_file = version_dir / "pool.csv"
        pool_df.to_csv(pool_file, index=False)

        # 保存配置
        config_file = version_dir / "config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        # 创建版本信息
        version_info = {
            "version_id": version_id,
            "created_at": datetime.now().isoformat(),
            "description": description,
            "tags": tags or [],
            "pool_count": len(pool_df),
            "config_file": str(config_file),
            "pool_file": str(pool_file),
            "statistics": self._calculate_statistics(pool_df),
        }

        # 保存版本信息
        info_file = version_dir / "version_info.json"
        with open(info_file, "w", encoding="utf-8") as f:
            json.dump(version_info, f, ensure_ascii=False, indent=2)

        # 更新元数据
        self.metadata["versions"].append(version_info)
        self.metadata["latest_version"] = version_id
        self._save_metadata()

        print(f"版本 {version_id} 创建成功")
        print(f"候选池数量: {len(pool_df)}")
        print(f"保存路径: {version_dir}")

        return version_id

    def _calculate_statistics(self, pool_df):
        """计算候选池统计信息"""
        stats = {
            "total_count": len(pool_df),
            "code_list": pool_df["code"].tolist() if "code" in pool_df.columns else [],
        }

        # 如果有聚类信息
        if "cluster_id" in pool_df.columns:
            stats["cluster_count"] = pool_df["cluster_id"].nunique()

        # 如果有成交额信息
        if "avg_volume" in pool_df.columns:
            stats["avg_volume_mean"] = pool_df["avg_volume"].mean()
            stats["avg_volume_min"] = pool_df["avg_volume"].min()
            stats["avg_volume_max"] = pool_df["avg_volume"].max()

        # 如果有成立时间信息
        if "start_date" in pool_df.columns:
            stats["earliest_start"] = str(pool_df["start_date"].min())
            stats["latest_start"] = str(pool_df["start_date"].max())

        return stats

    def get_version(self, version_id=None):
        """
        获取指定版本

        Args:
            version_id: 版本ID，如果为None则返回最新版本

        Returns:
            dict: 版本信息
        """
        if version_id is None:
            version_id = self.metadata["latest_version"]

        if version_id is None:
            raise ValueError("没有找到任何版本")

        for version in self.metadata["versions"]:
            if version["version_id"] == version_id:
                return version

        raise ValueError(f"未找到版本: {version_id}")

    def load_pool(self, version_id=None):
        """
        加载指定版本的候选池

        Args:
            version_id: 版本ID

        Returns:
            pd.DataFrame: 候选池数据
        """
        version_info = self.get_version(version_id)
        pool_file = version_info["pool_file"]

        if not os.path.exists(pool_file):
            raise FileNotFoundError(f"候选池文件不存在: {pool_file}")

        return pd.read_csv(pool_file)

    def load_config(self, version_id=None):
        """
        加载指定版本的配置

        Args:
            version_id: 版本ID

        Returns:
            dict: 配置参数
        """
        version_info = self.get_version(version_id)
        config_file = version_info["config_file"]

        if not os.path.exists(config_file):
            raise FileNotFoundError(f"配置文件不存在: {config_file}")

        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_versions(self, tag=None):
        """
        列出所有版本

        Args:
            tag: 按标签过滤

        Returns:
            list: 版本信息列表
        """
        versions = self.metadata["versions"]

        if tag:
            versions = [v for v in versions if tag in v.get("tags", [])]

        return sorted(versions, key=lambda x: x["created_at"], reverse=True)

    def compare_versions(self, version_id1, version_id2):
        """
        比较两个版本

        Args:
            version_id1: 版本1 ID
            version_id2: 版本2 ID

        Returns:
            dict: 比较结果
        """
        v1 = self.get_version(version_id1)
        v2 = self.get_version(version_id2)

        pool1 = self.load_pool(version_id1)
        pool2 = self.load_pool(version_id2)

        codes1 = set(pool1["code"].tolist())
        codes2 = set(pool2["code"].tolist())

        comparison = {
            "version1": version_id1,
            "version2": version_id2,
            "pool_count_v1": len(pool1),
            "pool_count_v2": len(pool2),
            "common_codes": list(codes1 & codes2),
            "only_in_v1": list(codes1 - codes2),
            "only_in_v2": list(codes2 - codes1),
            "overlap_ratio": len(codes1 & codes2) / len(codes1 | codes2)
            if codes1 | codes2
            else 0,
        }

        return comparison

    def delete_version(self, version_id):
        """
        删除指定版本

        Args:
            version_id: 版本ID
        """
        version_dir = self.base_dir / version_id

        if not version_dir.exists():
            raise ValueError(f"版本不存在: {version_id}")

        # 删除目录
        import shutil

        shutil.rmtree(version_dir)

        # 更新元数据
        self.metadata["versions"] = [
            v for v in self.metadata["versions"] if v["version_id"] != version_id
        ]

        if self.metadata["latest_version"] == version_id:
            if self.metadata["versions"]:
                self.metadata["latest_version"] = self.metadata["versions"][-1][
                    "version_id"
                ]
            else:
                self.metadata["latest_version"] = None

        self._save_metadata()
        print(f"版本 {version_id} 已删除")

    def export_version(self, version_id, export_dir):
        """
        导出指定版本

        Args:
            version_id: 版本ID
            export_dir: 导出目录
        """
        version_dir = self.base_dir / version_id
        export_path = Path(export_dir) / version_id

        import shutil

        shutil.copytree(version_dir, export_path)
        print(f"版本 {version_id} 已导出到 {export_path}")

    def generate_report(self, version_id=None):
        """
        生成版本报告

        Args:
            version_id: 版本ID

        Returns:
            str: 报告文本
        """
        version_info = self.get_version(version_id)
        stats = version_info["statistics"]

        report = f"""
ETF候选池版本报告
{"=" * 50}

版本信息
-------
版本ID: {version_info["version_id"]}
创建时间: {version_info["created_at"]}
描述: {version_info["description"]}
标签: {", ".join(version_info["tags"]) if version_info["tags"] else "无"}

候选池统计
---------
总数量: {stats["total_count"]} 只ETF
"""

        if "cluster_count" in stats:
            report += f"聚类簇数: {stats['cluster_count']}\n"

        if "avg_volume_mean" in stats:
            report += f"""
成交额统计
---------
平均成交额: {stats["avg_volume_mean"]:.2f} 亿
最小成交额: {stats["avg_volume_min"]:.2f} 亿
最大成交额: {stats["avg_volume_max"]:.2f} 亿
"""

        if "earliest_start" in stats:
            report += f"""
成立时间统计
-----------
最早成立: {stats["earliest_start"]}
最晚成立: {stats["latest_start"]}
"""

        report += f"""
{"=" * 50}
"""

        return report
