"""Compatibility alias for src.strategy.txt_normalizer."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.strategy.txt_normalizer")
