"""Compatibility alias for src.api.money_flow_api."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.api.money_flow_api")
