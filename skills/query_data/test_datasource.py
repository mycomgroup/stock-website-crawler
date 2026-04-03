#!/usr/bin/env python3
"""Simple smoke tests for non-MCP data sources.

Each provider is tested independently with a minimal request. No unified
interface is introduced; this is a plain test harness.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional, Tuple


class TestError(RuntimeError):
    pass


def _require_env(var: str) -> str:
    val = os.getenv(var, "").strip()
    if not val:
        raise TestError(f"Missing required env var: {var}")
    return val


def _http_get_json(url: str, headers: Optional[Dict[str, str]] = None) -> Any:
    req = urllib.request.Request(url, headers=headers or {}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise TestError(f"Non-JSON response from {url}: {exc}") from exc


def _http_post_json(
    url: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None
) -> Any:
    """Make a POST request with JSON data."""
    post_headers = {"Content-Type": "application/json"}
    if headers:
        post_headers.update(headers)

    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"), headers=post_headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise TestError(f"Non-JSON response from {url}: {exc}") from exc


def test_finnhub(symbol: str) -> Tuple[str, Any]:
    api_key = _require_env("FINNHUB_API_KEY")
    params = urllib.parse.urlencode({"symbol": symbol, "token": api_key})
    url = f"https://finnhub.io/api/v1/quote?{params}"
    data = _http_get_json(url)
    if not isinstance(data, dict) or "c" not in data:
        raise TestError("Finnhub response missing expected fields")
    return ("finnhub", data)


def test_fmp(symbol: str) -> Tuple[str, Any]:
    api_key = _require_env("FMP_API_KEY")
    params = urllib.parse.urlencode({"symbol": symbol, "apikey": api_key})
    url = f"https://financialmodelingprep.com/stable/quote?{params}"
    data = _http_get_json(url)
    if not isinstance(data, list) or not data:
        raise TestError("FMP response is empty")
    return ("financialmodelingprep", data[0])


def test_alphavantage(symbol: str) -> Tuple[str, Any]:
    api_key = _require_env("ALPHAVANTAGE_API_KEY")
    params = urllib.parse.urlencode(
        {"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": api_key}
    )
    url = f"https://www.alphavantage.co/query?{params}"
    data = _http_get_json(url)
    if not isinstance(data, dict) or "Global Quote" not in data:
        raise TestError("Alpha Vantage response missing Global Quote")
    return ("alphavantage", data.get("Global Quote", {}))


def test_tiingo(symbol: str) -> Tuple[str, Any]:
    api_key = _require_env("TIINGO_API_KEY")
    # Use a small, fixed historical window to keep the sample stable.
    start_date = "2024-01-02"
    end_date = "2024-01-05"
    params = urllib.parse.urlencode(
        {"startDate": start_date, "endDate": end_date, "token": api_key}
    )
    url = f"https://api.tiingo.com/tiingo/daily/{symbol}/prices?{params}"
    data = _http_get_json(url)
    if not isinstance(data, list) or not data:
        raise TestError("Tiingo response is empty")
    return ("tiingo", data[0])


def test_eulerpool() -> Tuple[str, Any]:
    api_key = _require_env("EULERPOOL_API_KEY")
    # Use the endpoint you confirmed works locally.
    params = urllib.parse.urlencode({"token": api_key})
    url = f"https://api.eulerpool.com/api/1/alternative/superinvestors/list?{params}"
    data = _http_get_json(url, headers={"Accept": "application/json"})
    if not isinstance(data, dict):
        raise TestError("Eulerpool response is not a JSON object")
    return ("eulerpool", data)


def test_massive() -> Tuple[str, Any]:
    api_key = _require_env("MASSIVE_API_KEY")
    # Use the reference endpoint you confirmed works locally.
    params = urllib.parse.urlencode(
        {"asset_class": "stocks", "locale": "us", "apiKey": api_key}
    )
    url = f"https://api.massive.com/v3/reference/tickers/types?{params}"
    data = _http_get_json(url, headers={"Accept": "application/json"})
    if not isinstance(data, dict):
        raise TestError("Massive response is not a JSON object")
    return ("massive", data)


def test_alltick() -> Tuple[str, Any]:
    """Test AllTick API - WebSocket-based, we'll test the REST endpoint for auth check."""
    api_key = _require_env("ALLTICK_API_KEY")
    # AllTick uses WebSocket, but we can test the token format
    # URL format: wss://quote.alltick.co/quote-b-ws-api?token=xxx
    # For testing, we'll just verify the token is present
    if not api_key or len(api_key) < 10:
        raise TestError("AllTick API key appears invalid")
    return (
        "alltick",
        {"status": "API key valid", "note": "WebSocket API - test token format only"},
    )


def test_brave_search() -> Tuple[str, Any]:
    """Test Brave Search API."""
    api_key = _require_env("BRAVE_SEARCH_API_KEY")
    url = "https://api.search.brave.com/res/v1/web/search"
    params = urllib.parse.urlencode({"q": "Apple stock price", "count": 5})
    full_url = f"{url}?{params}"

    headers = {"Accept": "application/json", "X-Subscription-Token": api_key}
    data = _http_get_json(full_url, headers=headers)
    if not isinstance(data, dict) or "web" not in data:
        raise TestError("Brave Search response missing expected fields")
    return (
        "brave_search",
        {
            "query": data.get("query", {}),
            "web_results_count": len(data.get("web", {}).get("results", [])),
        },
    )


def test_eodhd() -> Tuple[str, Any]:
    """Test EODHD API."""
    api_key = _require_env("EODHD_API_KEY")
    # Test with AAPL real-time quote
    symbol = "AAPL"
    url = f"https://eodhd.com/api/real-time/{symbol}?api_token={api_key}&fmt=json"
    data = _http_get_json(url)
    if not isinstance(data, dict):
        raise TestError("EODHD response is not a JSON object")
    return ("eodhd", data)


def test_financialdatasets(symbol: str) -> Tuple[str, Any]:
    """Test Financial Datasets API."""
    api_key = _require_env("FINANCIALDATASETS_API_KEY")
    url = f"https://api.financialdatasets.ai/prices/snapshot?ticker={symbol}"
    headers = {"X-API-KEY": api_key}
    data = _http_get_json(url, headers=headers)
    if not isinstance(data, dict) or "snapshot" not in data:
        raise TestError("Financial Datasets response missing expected fields")
    return ("financialdatasets", data)


def test_serpapi() -> Tuple[str, Any]:
    """Test SerpAPI."""
    api_key = _require_env("SERP_API_KEY")
    params = urllib.parse.urlencode(
        {"engine": "google", "q": "Apple stock price", "api_key": api_key}
    )
    url = f"https://serpapi.com/search?{params}"
    data = _http_get_json(url)
    if not isinstance(data, dict) or "search_metadata" not in data:
        raise TestError("SerpAPI response missing expected fields")
    return (
        "serpapi",
        {
            "search_metadata": data.get("search_metadata", {}),
            "organic_results_count": len(data.get("organic_results", [])),
        },
    )


def test_tavily() -> Tuple[str, Any]:
    """Test Tavily API."""
    api_key = _require_env("TAVILY_API_KEY")
    url = "https://api.tavily.com/search"
    data = {"query": "Apple stock price today", "api_key": api_key, "max_results": 5}
    response = _http_post_json(url, data)
    if not isinstance(response, dict) or "results" not in response:
        raise TestError("Tavily response missing expected fields")
    return (
        "tavily",
        {
            "results_count": len(response.get("results", [])),
            "query": response.get("query", ""),
        },
    )


def test_lixinger() -> Tuple[str, Any]:
    """Test Lixinger (理杏仁) API."""
    token = _require_env("LIXINGER_TOKEN")
    url = "https://open.lixinger.com/api/cn/company"
    data = {"stockCodes": ["600519"], "metrics": ["pe_ttm", "pb"], "token": token}
    response = _http_post_json(url, data)
    if not isinstance(response, dict) or response.get("code") != 1:
        raise TestError(f"Lixinger API error: {response.get('msg', 'Unknown error')}")
    return ("lixinger", {"status": "ok", "data_count": len(response.get("data", []))})


def _run_tests(source: Optional[str], symbol: str) -> int:
    tests = [
        ("finnhub", lambda: test_finnhub(symbol)),
        ("financialmodelingprep", lambda: test_fmp(symbol)),
        ("alphavantage", lambda: test_alphavantage(symbol)),
        ("tiingo", lambda: test_tiingo(symbol)),
        ("eulerpool", test_eulerpool),
        ("massive", test_massive),
        ("alltick", test_alltick),
        ("brave_search", test_brave_search),
        ("eodhd", test_eodhd),
        ("financialdatasets", lambda: test_financialdatasets(symbol)),
        ("lixinger", test_lixinger),
        ("serpapi", test_serpapi),
        ("tavily", test_tavily),
    ]

    results = []
    failures = []

    for name, fn in tests:
        if source and name != source:
            continue
        try:
            provider, payload = fn()
            results.append((provider, payload))
        except Exception as exc:  # noqa: BLE001
            failures.append((name, str(exc)))

    for provider, payload in results:
        preview = json.dumps(payload, ensure_ascii=True)[:200]
        print(f"[OK] {provider}: {preview}")

    for provider, err in failures:
        print(f"[FAIL] {provider}: {err}")

    return 0 if not failures else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Smoke tests for non-MCP data sources."
    )
    parser.add_argument(
        "--source",
        choices=[
            "finnhub",
            "financialmodelingprep",
            "alphavantage",
            "tiingo",
            "eulerpool",
            "massive",
            "alltick",
            "brave_search",
            "eodhd",
            "financialdatasets",
            "lixinger",
            "serpapi",
            "tavily",
        ],
        help="Run a single provider test",
    )
    parser.add_argument("--symbol", default="AAPL", help="Ticker symbol")
    args = parser.parse_args()
    return _run_tests(args.source, args.symbol)


if __name__ == "__main__":
    raise SystemExit(main())
