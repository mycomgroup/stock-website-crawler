"""
rule_library

YAML 驱动的量化选股规则库。外部项目只需要生成符合 schema 的 YAML，
本模块负责加载、执行、回测、打分。

公开接口:
    load_config(path)         — 加载 YAML 配置为 Strategy / SearchSpace
    apply_strategy(df, s)     — 在单日横截面应用策略，返回选中的 stock_id
    run_backtest(data, s)     — 在面板数据上跑回测，返回指标字典
    expand_search_space(sp)   — 把 SearchSpace 展开成 Strategy 列表
"""

from .schema import Rule, Strategy, SearchSpace
from .loader import load_aliases, load_strategy, load_search_space, load_base_filters
from .engine import apply_strategy
from .backtest import run_backtest, score
from .search import expand_search_space

__all__ = [
    "Rule",
    "Strategy",
    "SearchSpace",
    "load_aliases",
    "load_strategy",
    "load_search_space",
    "load_base_filters",
    "apply_strategy",
    "run_backtest",
    "score",
    "expand_search_space",
]
