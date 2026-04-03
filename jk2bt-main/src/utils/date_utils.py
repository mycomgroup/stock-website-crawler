"""Compatibility alias for src.utils.date_utils."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.utils.date_utils")
