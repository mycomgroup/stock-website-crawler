"""Compatibility alias for factors.financial_metrics."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.factors.financial_metrics")
