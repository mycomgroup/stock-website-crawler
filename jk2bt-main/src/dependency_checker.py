"""Compatibility alias for src.dependency_checker."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.dependency_checker")
