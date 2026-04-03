"""Compatibility alias for jk2bt.runtime_io."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.core.io")
