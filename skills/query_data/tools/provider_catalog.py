#!/usr/bin/env python3
"""Provider catalog tool for listing and filtering data providers.

Usage:
    python3 tools/provider_catalog.py
    python3 tools/provider_catalog.py --capability cn_equity_fundamental
    python3 tools/provider_catalog.py --has-query --format json
    python3 tools/provider_catalog.py --generate-index
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


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
                meta = parse_yaml(content)
            meta["_source_dir"] = subdir.name
            providers.append(meta)
        except Exception as e:
            print(f"[WARN] Failed to load {provider_yaml}: {e}", file=sys.stderr)
    
    return providers


def parse_yaml(content: str) -> dict:
    """Simple YAML parser for the provider.yaml structure."""
    result: dict = {}
    current = result
    stack: list[tuple[dict, int]] = []
    current_key = None
    current_list: list | None = None
    
    for line in content.split("\n"):
        # Skip empty lines and comments
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        
        # Calculate indentation
        indent = len(line) - len(line.lstrip())
        
        # Handle list items
        if stripped.startswith("- "):
            item = stripped[2:].strip()
            # Check if it's a simple list item or key-value in a list
            if ": " in item:
                key, value = item.split(": ", 1)
                if current_list is None:
                    current_list = []
                    if current_key:
                        current[current_key] = current_list
                current_list.append({key: parse_value(value)})
            else:
                if current_list is None:
                    current_list = []
                    if current_key:
                        current[current_key] = current_list
                current_list.append(parse_value(item))
            continue
        
        # Reset list context when moving to a new key
        current_list = None
        
        # Handle key-value pairs
        if ": " in stripped:
            key, value = stripped.split(": ", 1)
            key = key.strip()
            value = value.strip()
            
            # Pop stack if indentation decreased
            while stack and stack[-1][1] >= indent:
                stack.pop()
                if stack:
                    current = stack[-1][0]
            
            parsed_value = parse_value(value)
            if parsed_value is None:  # Nested object indicator
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


def parse_value(value: str) -> Any:
    """Parse a YAML value to appropriate Python type."""
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
    
    # Try integer
    try:
        return int(value)
    except ValueError:
        pass
    
    # Try float
    try:
        return float(value)
    except ValueError:
        pass
    
    # String (remove quotes if present)
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    
    return value


def filter_providers(
    providers: list[dict],
    capability: str | None = None,
    status: str | None = None,
    has_query: bool | None = None,
) -> list[dict]:
    """Filter providers based on criteria."""
    result = providers
    
    if capability:
        result = [
            p for p in result
            if capability in p.get("capabilities", [])
        ]
    
    if status:
        result = [
            p for p in result
            if p.get("status") == status
        ]
    
    if has_query is not None:
        entrypoints = [p.get("entrypoints", {}) for p in result]
        if has_query:
            result = [
                p for p, e in zip(result, entrypoints)
                if "query" in e
            ]
        else:
            result = [
                p for p, e in zip(result, entrypoints)
                if "query" not in e
            ]
    
    return result


def print_table(providers: list[dict]) -> None:
    """Print providers in table format."""
    if not providers:
        print("No providers found.")
        return
    
    # Headers
    headers = ["Provider", "Kind", "Status", "Capabilities", "Query"]
    
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    
    rows = []
    for p in providers:
        entrypoints = p.get("entrypoints", {})
        has_query = "✓" if "query" in entrypoints else ""
        caps = ", ".join(p.get("capabilities", [])[:2])
        if len(p.get("capabilities", [])) > 2:
            caps += "..."
        
        row = [
            p.get("provider_key", "N/A"),
            p.get("kind", "N/A"),
            p.get("status", "N/A"),
            caps,
            has_query,
        ]
        rows.append(row)
        
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Print header
    header_line = " | ".join(
        h.ljust(col_widths[i]) for i, h in enumerate(headers)
    )
    print(header_line)
    print("-" * len(header_line))
    
    # Print rows
    for row in rows:
        print(" | ".join(
            str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)
        ))
    
    print(f"\nTotal: {len(providers)} provider(s)")


def print_json(providers: list[dict]) -> None:
    """Print providers in JSON format."""
    # Remove internal fields
    clean_providers = []
    for p in providers:
        clean = {k: v for k, v in p.items() if not k.startswith("_")}
        clean_providers.append(clean)
    
    print(json.dumps(clean_providers, indent=2, ensure_ascii=False))


def generate_index(base_dir: Path, providers: list[dict]) -> dict:
    """Generate provider index structure."""
    index_providers = []
    
    for p in providers:
        entrypoints = p.get("entrypoints", {})
        index_entry = {
            "provider_key": p.get("provider_key", ""),
            "display_name": p.get("display_name", ""),
            "kind": p.get("kind", ""),
            "status": p.get("status", ""),
            "capabilities": p.get("capabilities", []),
            "has_query_entrypoint": "query" in entrypoints,
            "has_smoke_test": "smoke_test" in entrypoints,
            "auth_env_vars": p.get("auth", {}).get("env_vars", []),
            "docs_primary_index": p.get("docs", {}).get("primary_index", ""),
        }
        index_providers.append(index_entry)
    
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provider_count": len(index_providers),
        "providers": index_providers,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Query data provider catalog"
    )
    parser.add_argument(
        "--capability",
        help="Filter by capability (e.g., cn_equity_fundamental)",
    )
    parser.add_argument(
        "--has-query",
        action="store_true",
        help="Only show providers with query entrypoint",
    )
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="Output format",
    )
    parser.add_argument(
        "--generate-index",
        action="store_true",
        help="Generate generated/provider_index.json",
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=None,
        help="Base directory for providers (default: parent of tools/)",
    )
    
    args = parser.parse_args()
    
    # Determine base directory
    if args.base_dir:
        base_dir = args.base_dir
    else:
        # Default: parent of tools/ directory
        base_dir = Path(__file__).parent.parent
    
    # Load all providers
    providers = load_all_providers(base_dir)
    
    # Filter if needed
    filtered = filter_providers(
        providers,
        capability=args.capability,
        has_query=args.has_query if args.has_query else None,
    )
    
    # Generate index or print output
    if args.generate_index:
        index = generate_index(base_dir, providers)
        output_file = base_dir / "generated" / "provider_index.json"
        output_file.parent.mkdir(exist_ok=True)
        output_file.write_text(
            json.dumps(index, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"Generated: {output_file}")
        print(f"Providers: {index['provider_count']}")
    elif args.format == "json":
        print_json(filtered)
    else:
        print_table(filtered)
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
