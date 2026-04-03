#!/usr/bin/env python3
"""Unified smoke test runner for data providers.

Usage:
    python3 tools/provider_smoke_test.py --provider lixinger
    python3 tools/provider_smoke_test.py --all
    python3 tools/provider_smoke_test.py --all --format json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class SmokeResult:
    provider_key: str
    status: Literal["ok", "fail", "skipped"]
    message: str
    duration_ms: int | None = None
    exit_code: int | None = None


def load_yaml_simple(content: str) -> dict:
    """Simple YAML parser."""
    result: dict = {}
    current = result
    stack: list[tuple[dict, int]] = []
    current_key = None
    current_list: list | None = None
    
    for line in content.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        
        indent = len(line) - len(line.lstrip())
        
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            if ": " in item:
                key, value = item.split(": ", 1)
                if current_list is None:
                    current_list = []
                    if current_key:
                        current[current_key] = current_list
                current_list.append({key: parse_yaml_value(value)})
            else:
                if current_list is None:
                    current_list = []
                    if current_key:
                        current[current_key] = current_list
                current_list.append(parse_yaml_value(item))
            continue
        
        current_list = None
        
        if ": " in stripped:
            key, value = stripped.split(": ", 1)
            key = key.strip()
            value = value.strip()
            
            while stack and stack[-1][1] >= indent:
                stack.pop()
                if stack:
                    current = stack[-1][0]
            
            parsed_value = parse_yaml_value(value)
            if parsed_value is None:
                new_dict = {}
                current[key] = new_dict
                stack.append((current, indent))
                current = new_dict
                current_key = None
            else:
                current[key] = parsed_value
                current_key = key
        elif stripped.endswith(":"):
            key = stripped[:-1].strip()
            
            while stack and stack[-1][1] >= indent:
                stack.pop()
                if stack:
                    current = stack[-1][0]
            
            new_dict = {}
            current[key] = new_dict
            stack.append((current, indent))
            current = new_dict
            current_key = None
    
    return result


def parse_yaml_value(value: str):
    """Parse YAML value."""
    value = value.strip()
    
    if value == "":
        return None
    if value.lower() in ("true", "yes"):
        return True
    if value.lower() in ("false", "no"):
        return False
    if value == "[]":
        return []
    if value == "{}":
        return {}
    
    try:
        return int(value)
    except ValueError:
        pass
    
    try:
        return float(value)
    except ValueError:
        pass
    
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    
    return value


def load_all_providers(base_dir: Path) -> list[dict]:
    """Scan all provider directories and load provider.yaml files."""
    providers = []
    
    for subdir in sorted(base_dir.iterdir()):
        if not subdir.is_dir():
            continue
        
        provider_yaml = subdir / "provider.yaml"
        if not provider_yaml.exists():
            continue
        
        try:
            content = provider_yaml.read_text(encoding="utf-8")
            if HAS_YAML:
                meta = yaml.safe_load(content)
            else:
                meta = load_yaml_simple(content)
            meta["_source_dir"] = subdir.name
            providers.append(meta)
        except Exception as e:
            print(f"[WARN] Failed to load {provider_yaml}: {e}", file=sys.stderr)
    
    return providers


def run_smoke_test(provider_key: str, provider_meta: dict, base_dir: Path) -> SmokeResult:
    """Run smoke test for a single provider."""
    entrypoints = provider_meta.get("entrypoints", {})
    smoke_test = entrypoints.get("smoke_test", {})
    command = smoke_test.get("command", "")
    
    if not command:
        return SmokeResult(
            provider_key=provider_key,
            status="skipped",
            message="No smoke_test entrypoint defined",
            duration_ms=None,
            exit_code=None
        )
    
    start_time = time.time()
    
    try:
        # Split command safely (simple approach)
        import shlex
        cmd_parts = shlex.split(command)
        
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=base_dir
        )
        
        duration_ms = int((time.time() - start_time) * 1000)
        
        if result.returncode == 0:
            # Extract success message from output
            stdout_preview = result.stdout.strip().split("\n")[0][:100]
            return SmokeResult(
                provider_key=provider_key,
                status="ok",
                message=stdout_preview or "Test passed",
                duration_ms=duration_ms,
                exit_code=0
            )
        else:
            stderr_preview = result.stderr.strip().split("\n")[0][:100]
            return SmokeResult(
                provider_key=provider_key,
                status="fail",
                message=stderr_preview or f"Exit code: {result.returncode}",
                duration_ms=duration_ms,
                exit_code=result.returncode
            )
            
    except subprocess.TimeoutExpired:
        duration_ms = int((time.time() - start_time) * 1000)
        return SmokeResult(
            provider_key=provider_key,
            status="fail",
            message="Test timed out after 60s",
            duration_ms=duration_ms,
            exit_code=-1
        )
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        return SmokeResult(
            provider_key=provider_key,
            status="fail",
            message=str(e),
            duration_ms=duration_ms,
            exit_code=-1
        )


def run_all(providers: list[dict], base_dir: Path) -> list[SmokeResult]:
    """Run smoke tests for all providers."""
    results = []
    
    for provider in providers:
        provider_key = provider.get("provider_key", "unknown")
        result = run_smoke_test(provider_key, provider, base_dir)
        results.append(result)
    
    return results


def print_results(results: list[SmokeResult]) -> None:
    """Print results in standard format."""
    for r in results:
        duration_str = f" ({r.duration_ms}ms)" if r.duration_ms else ""
        if r.status == "ok":
            print(f"[OK]      {r.provider_key:<15} - {r.message}{duration_str}")
        elif r.status == "fail":
            print(f"[FAIL]    {r.provider_key:<15} - {r.message}{duration_str}")
        else:  # skipped
            print(f"[SKIPPED] {r.provider_key:<15} - {r.message}")
    
    # Summary
    ok_count = sum(1 for r in results if r.status == "ok")
    fail_count = sum(1 for r in results if r.status == "fail")
    skip_count = sum(1 for r in results if r.status == "skipped")
    print(f"\nSummary: {ok_count} OK, {fail_count} FAIL, {skip_count} SKIPPED")


def print_json_results(results: list[SmokeResult]) -> None:
    """Print results in JSON format."""
    data = [asdict(r) for r in results]
    print(json.dumps(data, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run provider smoke tests"
    )
    parser.add_argument(
        "--provider",
        help="Run test for specific provider",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run tests for all providers",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=None,
        help="Base directory (default: parent of tools/)",
    )
    
    args = parser.parse_args()
    
    if args.base_dir:
        base_dir = args.base_dir
    else:
        base_dir = Path(__file__).parent.parent
    
    # Load providers
    providers = load_all_providers(base_dir)
    
    if args.provider:
        # Run single provider
        provider = next(
            (p for p in providers if p.get("provider_key") == args.provider),
            None
        )
        if not provider:
            print(f"[ERROR] Provider not found: {args.provider}", file=sys.stderr)
            return 1
        
        result = run_smoke_test(args.provider, provider, base_dir)
        results = [result]
    elif args.all:
        # Run all providers
        results = run_all(providers, base_dir)
    else:
        parser.print_help()
        return 1
    
    # Output results
    if args.format == "json":
        print_json_results(results)
    else:
        print_results(results)
    
    # Return non-zero if any failures
    return 1 if any(r.status == "fail" for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
