"""Compatibility alias for src.db.meta_cache_api."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.db.meta_cache_api")
