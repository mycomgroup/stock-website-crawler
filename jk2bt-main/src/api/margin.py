"""Compatibility alias for src.api.margin."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.api.margin")
