"""Compatibility alias for src.api.missing_apis."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.api.missing_apis")
