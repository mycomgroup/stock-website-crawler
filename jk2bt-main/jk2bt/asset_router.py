"""Compatibility alias for jk2bt.asset_router."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.core.asset_router")
