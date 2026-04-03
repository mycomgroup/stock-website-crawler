"""Compatibility alias for src.api.factor_api."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.api.factor_api")
