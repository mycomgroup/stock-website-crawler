"""Compatibility bridge for ``src.txt_strategy_normalizer``."""

from importlib import import_module

_target_module = import_module("jk2bt.strategy.txt_strategy_normalizer")
globals().update(vars(_target_module))
