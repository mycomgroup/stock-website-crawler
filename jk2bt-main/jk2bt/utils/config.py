"""
统一配置管理模块
提供集中化的配置管理，支持文件加载和环境变量

使用方式:
    from jk2bt.utils.config import get_config

    # 获取全局配置
    config = get_config()

    # 使用配置
    print(config.cache.ttl_hours)
    print(config.backtest.initial_capital)
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any
import json


@dataclass
class CacheConfig:
    """缓存配置"""
    enabled: bool = True
    ttl_hours: int = 24
    max_memory_items: int = 5000
    cache_dir: str = "data/cache"
    duckdb_path: str = "data/jk2bt.duckdb"


@dataclass
class DataSourceConfig:
    """数据源配置"""
    provider: str = "akshare"
    timeout: int = 30
    retry_count: int = 3
    retry_delay: float = 1.0


@dataclass
class LoggingConfig:
    """日志配置"""
    level: str = "INFO"
    log_file: str = "logs/jk2bt.log"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@dataclass
class BacktestConfig:
    """回测配置"""
    initial_capital: float = 1000000.0
    commission_rate: float = 0.0003
    slippage: float = 0.0
    benchmark: str = "000300.XSHG"


@dataclass
class Config:
    """主配置类"""
    cache: CacheConfig = field(default_factory=CacheConfig)
    data_source: DataSourceConfig = field(default_factory=DataSourceConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    backtest: BacktestConfig = field(default_factory=BacktestConfig)

    @classmethod
    def from_file(cls, config_path: str) -> "Config":
        """从JSON文件加载配置"""
        with open(config_path) as f:
            data = json.load(f)
        return cls(
            cache=CacheConfig(**data.get("cache", {})),
            data_source=DataSourceConfig(**data.get("data_source", {})),
            logging=LoggingConfig(**data.get("logging", {})),
            backtest=BacktestConfig(**data.get("backtest", {})),
        )

    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量加载配置"""
        return cls(
            cache=CacheConfig(
                enabled=os.environ.get("JK2BT_CACHE_ENABLED", "true").lower() == "true",
                cache_dir=os.environ.get("JK2BT_CACHE_DIR", "data/cache"),
            ),
            logging=LoggingConfig(
                level=os.environ.get("JK2BT_LOG_LEVEL", "INFO"),
            ),
        )

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "cache": {
                "enabled": self.cache.enabled,
                "ttl_hours": self.cache.ttl_hours,
                "max_memory_items": self.cache.max_memory_items,
                "cache_dir": self.cache.cache_dir,
                "duckdb_path": self.cache.duckdb_path,
            },
            "data_source": {
                "provider": self.data_source.provider,
                "timeout": self.data_source.timeout,
                "retry_count": self.data_source.retry_count,
                "retry_delay": self.data_source.retry_delay,
            },
            "logging": {
                "level": self.logging.level,
                "log_file": self.logging.log_file,
                "format": self.logging.format,
            },
            "backtest": {
                "initial_capital": self.backtest.initial_capital,
                "commission_rate": self.backtest.commission_rate,
                "slippage": self.backtest.slippage,
                "benchmark": self.backtest.benchmark,
            },
        }

    def save(self, config_path: str):
        """保存配置到文件"""
        with open(config_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)


# 全局配置实例
_config: Config = None


def get_config() -> Config:
    """获取全局配置"""
    global _config
    if _config is None:
        config_file = os.environ.get("JK2BT_CONFIG_FILE")
        if config_file and Path(config_file).exists():
            _config = Config.from_file(config_file)
        else:
            # 尝试加载默认配置文件
            default_config_path = Path(__file__).parent.parent.parent / "config" / "default.json"
            if default_config_path.exists():
                _config = Config.from_file(str(default_config_path))
            else:
                _config = Config.from_env()
    return _config


def set_config(config: Config):
    """设置全局配置"""
    global _config
    _config = config


def reset_config():
    """重置全局配置（用于测试）"""
    global _config
    _config = None