"""Compatibility alias for src.db.migrate_pickle."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.db.migrate_pickle")
