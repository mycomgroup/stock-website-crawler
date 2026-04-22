"""
因子计算基类与注册表
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import pandas as pd

from ..core.interface import DataSourceContext


class FactorBase(ABC):
    """
    因子基类
    
    所有因子都应继承此类并实现 compute 方法。
    
    使用示例:
        @FactorRegistry.register("ma_5", aliases=["MA5"])
        class MA5Factor(FactorBase):
            name = "ma_5"
            category = "technical"
            description = "5日移动平均线"
            
            def compute(self, symbol, end_date=None, **kwargs):
                from ..data.fetcher import get_ohlcv
                from ..core.indicators import ma
                df = get_ohlcv(symbol, end_date=end_date, count=100)
                return ma(df['close'], 5)
    """
    
    name: str = ""
    category: str = ""
    description: str = ""
    aliases: List[str] = []
    
    @abstractmethod
    def compute(
        self,
        symbol: str,
        end_date: Optional[str] = None,
        **kwargs
    ) -> pd.Series:
        """
        计算因子值
        
        Args:
            symbol: 股票代码
            end_date: 结束日期
            **kwargs: 其他参数
        
        Returns:
            因子值序列，索引为日期
        """
        pass
    
    @property
    def data_source(self):
        """获取数据源"""
        return DataSourceContext.get_data_source()


class FactorRegistry:
    """
    因子注册表
    
    管理所有因子的注册和获取。
    
    使用示例:
        # 注册因子
        @FactorRegistry.register("my_factor", aliases=["MY_FACTOR"])
        class MyFactor(FactorBase):
            ...
        
        # 获取因子
        factor = FactorRegistry.get("my_factor")
        
        # 列出所有因子
        factors = FactorRegistry.list_factors()
    """
    
    _factors: Dict[str, FactorBase] = {}
    _aliases: Dict[str, str] = {}
    
    @classmethod
    def register(cls, name: str, aliases: Optional[List[str]] = None):
        """
        注册因子装饰器
        
        Args:
            name: 因子名称
            aliases: 因子别名列表
        """
        def decorator(factor_class: type) -> type:
            factor = factor_class()
            factor.name = name
            cls._factors[name] = factor
            
            if aliases:
                for alias in aliases:
                    cls._aliases[alias.lower()] = name
            
            return factor_class
        return decorator
    
    @classmethod
    def get(cls, name: str) -> Optional[FactorBase]:
        """
        获取因子
        
        Args:
            name: 因子名称或别名
        
        Returns:
            因子实例，如果不存在返回 None
        """
        name_lower = name.lower()
        name = cls._aliases.get(name_lower, name_lower)
        return cls._factors.get(name)
    
    @classmethod
    def list_factors(cls, category: Optional[str] = None) -> List[str]:
        """
        列出所有因子
        
        Args:
            category: 按类别筛选
        
        Returns:
            因子名称列表
        """
        factors = list(cls._factors.keys())
        if category:
            factors = [f for f in factors if cls._factors[f].category == category]
        return factors
    
    @classmethod
    def list_categories(cls) -> List[str]:
        """列出所有类别"""
        categories = set()
        for factor in cls._factors.values():
            if factor.category:
                categories.add(factor.category)
        return list(categories)
    
    @classmethod
    def clear(cls) -> None:
        """清除所有注册（用于测试）"""
        cls._factors.clear()
        cls._aliases.clear()


def compute_factor(
    factor_name: str,
    symbol: str,
    end_date: Optional[str] = None,
    **kwargs
) -> pd.Series:
    """
    计算单个因子
    
    Args:
        factor_name: 因子名称或别名
        symbol: 股票代码
        end_date: 结束日期
        **kwargs: 其他参数
    
    Returns:
        因子值序列
    
    使用示例:
        ma5 = compute_factor("ma_5", "000001.SZ")
        pe = compute_factor("PE", "000001.SZ")  # 使用别名
    """
    factor = FactorRegistry.get(factor_name)
    if factor is None:
        raise ValueError(f"Unknown factor: {factor_name}")
    return factor.compute(symbol, end_date, **kwargs)


def compute_factors(
    factor_names: List[str],
    symbol: str,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """
    计算多个因子
    
    Args:
        factor_names: 因子名称列表
        symbol: 股票代码
        end_date: 结束日期
    
    Returns:
        DataFrame，每列为一个因子
    
    使用示例:
        factors = compute_factors(["ma_5", "rsi_14", "macd"], "000001.SZ")
    """
    result = {}
    for name in factor_names:
        try:
            factor = FactorRegistry.get(name)
            if factor is None:
                result[name] = pd.Series(dtype=float)
            else:
                computed = factor.compute(symbol, end_date)
                if isinstance(computed, pd.DataFrame):
                    for col in computed.columns:
                        result[f"{name}_{col}"] = computed[col]
                else:
                    result[name] = computed
        except Exception:
            result[name] = pd.Series(dtype=float)
    
    return pd.DataFrame(result)