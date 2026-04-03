"""Compatibility alias for src.db.duckdb_manager."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.db.duckdb_manager")
