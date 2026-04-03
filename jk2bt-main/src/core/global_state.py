"""Compatibility alias for src.core.global_state."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.core.global_state")
