"""Compatibility alias for src.api.billboard."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.api.billboard")
