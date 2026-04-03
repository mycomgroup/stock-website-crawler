"""Compatibility alias for src.core.io."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.core.io")
