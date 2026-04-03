"""Compatibility alias for src.strategy.runtime_resource_pack."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.strategy.runtime_resource_pack")
