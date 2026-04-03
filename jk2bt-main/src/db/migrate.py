"""Compatibility alias for src.db.migrate."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.db.migrate")
