"""
jk2bt/data_access/akshare_compat.py

AkShare version compatibility adapter.

Provides automatic function name aliasing, version detection, and fallback
mechanisms to shield jk2bt from akshare API changes across versions.

Simplified from akshare-one-enhanced: no custom logging_config, no get_logger.
Uses standard logging.getLogger(__name__) and traditional typing imports.
"""

import logging
from typing import Optional, Dict, List, Any, Tuple

import akshare
import pandas as pd

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Function alias map: old / deprecated name -> current name
# ---------------------------------------------------------------------------

FUNCTION_ALIASES: Dict[str, str] = {
    "stock_zh_a_daily": "stock_zh_a_hist",
    "stock_zh_a_daily_hfq": "stock_zh_a_hist",
    "stock_zh_a_spot": "stock_zh_a_spot_em",
    "stock_kcb_spot": "stock_kcb_spot_em",
    "stock_cyb_spot": "stock_cyb_spot_em",
    "stock_fund_flow_individual": "stock_individual_fund_flow",
    "stock_em_hsgt_north_net_flow_in": "stock_hsgt_hist_em",
    "stock_dzjy_sctj": "stock_dzjy_mrtj",
    "fund_etf_fund_info": "fund_etf_fund_info_em",
    "stock_info_a_code_name": "stock_info_a_code_name",
    "tool_trade_date_hist_sina": "tool_trade_date_hist_sina",
    "index_stock_cons": "index_stock_cons",
    "index_stock_cons_weight_csindex": "index_stock_cons_weight_csindex",
    "stock_board_industry_name_em": "stock_board_industry_name_em",
    "stock_board_concept_name_em": "stock_board_concept_name_em",
    "stock_board_industry_cons_em": "stock_board_industry_cons_em",
    "stock_board_concept_cons_em": "stock_board_concept_cons_em",
    "stock_zh_a_hist_min_em": "stock_zh_a_hist_min_em",
    "stock_zh_a_hist_pre_min_em": "stock_zh_a_hist_pre_min_em",
    "stock_individual_info_em": "stock_individual_info_em",
    "stock_financial_benefit_ths": "stock_financial_benefit_ths",
    "stock_profit_forecast": "stock_profit_forecast",
    "stock_profit_forecast_ths": "stock_profit_forecast_ths",
    "stock_lhb_detail_em": "stock_lhb_detail_em",
    "stock_tfp_em": "stock_tfp_em",
    "stock_info_sh_name_code": "stock_info_sh_name_code",
    "stock_info_sz_name_code": "stock_info_sz_name_code",
    "fund_etf_hist_em": "fund_etf_hist_em",
    "fund_lof_hist_em": "fund_lof_hist_em",
    "bond_zh_cov": "bond_zh_cov",
    "bond_zh_cov_daily": "bond_zh_cov_daily",
    "futures_zh_daily_sina": "futures_zh_daily_sina",
    "option_finance_board": "option_finance_board",
    "sw_index_first_info": "sw_index_first_info",
    "stock_restricted_release_summary_em": "stock_restricted_release_summary_em",
}

# Minimum supported akshare version
MIN_SUPPORTED_VERSION: Tuple[int, ...] = (1, 17, 80)


class AkShareCompatAdapter:
    """AkShare version compatibility adapter.

    Responsibilities:
        1. Detect installed akshare version and warn if too old.
        2. Resolve deprecated function names via FUNCTION_ALIASES.
        3. Cache function existence checks to avoid repeated getattr.
        4. Provide a unified ``call()`` entry point with automatic fallback.
    """

    def __init__(self) -> None:
        self._version: str = ""
        self._version_tuple: Tuple[int, ...] = ()
        self._func_cache: Dict[str, bool] = {}
        self._detect_version()
        self._validate_version()

    # ------------------------------------------------------------------
    # Version detection
    # ------------------------------------------------------------------

    def _detect_version(self) -> None:
        """Parse akshare.__version__ and store as string + tuple."""
        raw = getattr(akshare, "__version__", "unknown")
        self._version = raw
        try:
            parts = raw.split(".")
            self._version_tuple = tuple(int(p) for p in parts[:3])
        except (ValueError, AttributeError):
            self._version_tuple = (0, 0, 0)
        logger.info(
            "akshare version detected: %s (tuple: %s)", raw, self._version_tuple
        )

    def _validate_version(self) -> None:
        """Warn if installed version is below MIN_SUPPORTED_VERSION."""
        if self._version_tuple and self._version_tuple < MIN_SUPPORTED_VERSION:
            min_ver = ".".join(str(v) for v in MIN_SUPPORTED_VERSION)
            logger.warning(
                "akshare version %s is below minimum supported %s. "
                "Some functions may not work correctly.",
                self._version,
                min_ver,
            )

    @property
    def version(self) -> str:
        """Return the detected akshare version string."""
        return self._version

    @property
    def version_tuple(self) -> Tuple[int, ...]:
        """Return the detected akshare version as a tuple."""
        return self._version_tuple

    # ------------------------------------------------------------------
    # Function existence cache
    # ------------------------------------------------------------------

    def _has_function(self, name: str) -> bool:
        """Check whether *name* exists as a callable in the akshare module.

        Results are cached to avoid repeated ``hasattr`` / ``getattr`` calls.
        """
        if name not in self._func_cache:
            self._func_cache[name] = hasattr(akshare, name) and callable(
                getattr(akshare, name, None)
            )
        return self._func_cache[name]

    # ------------------------------------------------------------------
    # Name resolution
    # ------------------------------------------------------------------

    def resolve_function_name(self, name: str) -> str:
        """Resolve a function name, trying direct -> alias -> original.

        1. If *name* exists in akshare, return it as-is.
        2. If *name* is in FUNCTION_ALIASES and the target exists, return the target.
        3. Otherwise return *name* unchanged (caller will get an error on call).
        """
        if self._has_function(name):
            return name
        alias = FUNCTION_ALIASES.get(name)
        if alias is not None and self._has_function(alias):
            logger.debug("Resolved alias: %s -> %s", name, alias)
            return alias
        return name

    # ------------------------------------------------------------------
    # Unified call entry point
    # ------------------------------------------------------------------

    def call(
        self,
        func_name: str,
        fallback_func: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """Call an akshare function with automatic alias resolution and fallback.

        Steps:
            1. Resolve *func_name* to *actual_name* via ``resolve_function_name``.
            2. Try ``getattr(akshare, actual_name)(**kwargs)``.
            3. If that fails and *fallback_func* is provided, try the fallback.
            4. If both fail, raise ``RuntimeError`` with a detailed message.

        Args:
            func_name: The akshare function name to call (may be deprecated).
            fallback_func: Optional fallback function name if primary fails.
            **kwargs: Arguments forwarded to the akshare function.

        Returns:
            The result of the akshare function call (typically a DataFrame).

        Raises:
            RuntimeError: If both primary and fallback calls fail.
        """
        actual_name = self.resolve_function_name(func_name)

        # Primary attempt
        primary_err = None
        try:
            func = getattr(akshare, actual_name)
            return func(**kwargs)
        except Exception as e:
            primary_err = e
            logger.debug(
                "Primary call failed: %s(%s) -> %s",
                actual_name,
                kwargs,
                primary_err,
            )

        # Fallback attempt
        if fallback_func is not None:
            fallback_resolved = self.resolve_function_name(fallback_func)
            try:
                func = getattr(akshare, fallback_resolved)
                result = func(**kwargs)
                logger.info(
                    "Fallback succeeded: %s -> %s", func_name, fallback_resolved
                )
                return result
            except Exception as fallback_err:
                raise RuntimeError(
                    f"AkShare call failed. Primary '{actual_name}' error: {primary_err}. "
                    f"Fallback '{fallback_resolved}' error: {fallback_err}"
                ) from fallback_err

        raise RuntimeError(
            f"AkShare call failed: '{actual_name}' with args {kwargs}. "
            f"Error: {primary_err}"
        ) from primary_err

    # ------------------------------------------------------------------
    # Proxy attribute access
    # ------------------------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        """Proxy attribute access to resolved akshare functions.

        Allows usage like ``adapter.stock_zh_a_hist(...)`` which will
        automatically resolve aliases if the original name is missing.
        """
        if name.startswith("_"):
            raise AttributeError(name)
        resolved = self.resolve_function_name(name)
        if self._has_function(resolved):
            return getattr(akshare, resolved)
        raise AttributeError(
            f"akshare has no function '{name}' (resolved to '{resolved}')"
        )


# ---------------------------------------------------------------------------
# Singleton
# ---------------------------------------------------------------------------

_global_adapter: Optional[AkShareCompatAdapter] = None


def get_compat_adapter() -> AkShareCompatAdapter:
    """Return the global singleton AkShareCompatAdapter instance."""
    global _global_adapter
    if _global_adapter is None:
        _global_adapter = AkShareCompatAdapter()
    return _global_adapter
