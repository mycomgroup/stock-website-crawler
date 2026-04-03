"""Compatibility alias for utils.data_source_backup."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.utils.data_source_backup")
