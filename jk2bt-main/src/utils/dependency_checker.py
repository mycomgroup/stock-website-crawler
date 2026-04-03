"""Compatibility alias for src.utils.dependency_checker."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.utils.dependency_checker")
