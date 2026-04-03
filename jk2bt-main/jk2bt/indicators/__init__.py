"""Compatibility package for historical ``jk2bt.indicators`` imports."""

from importlib import import_module
import sys

_SIGNALS_MODULE = import_module("jk2bt.signals")

# Re-export public symbols from jk2bt.signals
for _name, _value in vars(_SIGNALS_MODULE).items():
    if _name.startswith("_"):
        continue
    globals()[_name] = _value

_SUBMODULES = (
    "cross_signals",
    "extreme_signals",
    "breakthrough_signals",
    "divergence_signals",
    "rsrs",
    "market_sentiment",
    "fields",
)

for _submodule in _SUBMODULES:
    sys.modules[f"{__name__}.{_submodule}"] = import_module(
        f"jk2bt.signals.{_submodule}"
    )

__all__ = getattr(
    _SIGNALS_MODULE,
    "__all__",
    [name for name in globals() if not name.startswith("_")],
)

