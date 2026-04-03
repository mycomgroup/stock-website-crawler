"""Compatibility alias for src.api.gap_analyzer."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.api.gap_analyzer")
