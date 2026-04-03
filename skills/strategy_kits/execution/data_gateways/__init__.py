"""Data gateway adapters for JQ, TuShare, and Qlib."""

from .base import BaseDataGateway
from .factory import create_gateway

__all__ = [
    "BaseDataGateway",
    "create_gateway",
]
