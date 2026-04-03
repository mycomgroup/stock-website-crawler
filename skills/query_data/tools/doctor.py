#!/usr/bin/env python3
"""Doctor tool for checking plugin integrity.

Usage:
    python3 tools/doctor.py
    python3 tools/doctor.py --provider lixinger
    python3 tools/doctor.py --fix-hints
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class Issue:
    level: Literal["ERROR", "WARN", "INFO"]
    file: str
    message: str
    fix_hint: str = ""


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


def check_plugin_manifest(base_dir: Path) -> list[Issue]:
    """Check if plugin.json exists and is valid."""
    issues = []
    manifest_path = base_dir / ".claude-plugin" / "plugin.json"
    
    if not manifest_path.exists():
        issues.append(Issue(
            level="ERROR",
            file=".claude-plugin/plugin.json",
            message="Plugin manifest not found",
            fix_hint="Create .claude-plugin/plugin.json with name, version, description, author fields"
        ))
        return issues
    
    try:
        content = manifest_path.read_text(encoding="utf-8")
        manifest = json.loads(content)
        
        required_fields = ["name", "version", "description", "author"]
        for field in required_fields:
            if field not in manifest:
                issues.append(Issue(
                    level="ERROR",
                    file=".claude-plugin/plugin.json",
                    message=f"Missing required field: {field}",
                    fix_hint=f"Add '{field}' field to plugin.json"
                ))
        
        if manifest.get("name") != "query_data":
            issues.append(Issue(
                level="WARN",
                file=".claude-plugin/plugin.json",
                message=f"Plugin name should be 'query_data', got '{manifest.get('name')}'",
                fix_hint="Set name to 'query_data'"
            ))
            
    except json.JSONDecodeError as e:
        issues.append(Issue(
            level="ERROR",
            file=".claude-plugin/plugin.json",
            message=f"Invalid JSON: {e}",
            fix_hint="Fix JSON syntax errors"
        ))
    
    return issues


def check_provider_metadata(provider_dir: Path) -> list[Issue]:
    """Check provider.yaml for required fields."""
    issues = []
    yaml_path = provider_dir / "provider.yaml"
    provider_name = provider_dir.name
    
    if not yaml_path.exists():
        issues.append(Issue(
            level="WARN",
            file=f"{provider_name}/provider.yaml",
            message="Provider metadata not found",
            fix_hint=f"Create {provider_name}/provider.yaml with required fields"
        ))
        return issues
    
    try:
        content = yaml_path.read_text(encoding="utf-8")
        if HAS_YAML:
            meta = yaml.safe_load(content)
        else:
            meta = load_yaml_simple(content)
        
        required_fields = ["provider_key", "display_name", "kind", "status", "auth", "capabilities", "entrypoints", "docs"]
        for field in required_fields:
            if field not in meta:
                issues.append(Issue(
                    level="ERROR",
                    file=f"{provider_name}/provider.yaml",
                    message=f"Missing required field: {field}",
                    fix_hint=f"Add '{field}' field to provider.yaml"
                ))
        
        # Check entrypoints.smoke_test
        entrypoints = meta.get("entrypoints", {})
        if "smoke_test" not in entrypoints:
            issues.append(Issue(
                level="WARN",
                file=f"{provider_name}/provider.yaml",
                message="Missing smoke_test entrypoint",
                fix_hint="Add entrypoints.smoke_test.command"
            ))
        
        # Check docs.primary_index exists
        docs = meta.get("docs", {})
        primary_index = docs.get("primary_index", "")
        if primary_index:
            index_path = base_dir = provider_dir.parent
            full_path = index_path / primary_index
            if not full_path.exists():
                issues.append(Issue(
                    level="WARN",
                    file=f"{provider_name}/provider.yaml",
                    message=f"Docs path does not exist: {primary_index}",
                    fix_hint="Update docs.primary_index to existing file path"
                ))
                
    except Exception as e:
        issues.append(Issue(
            level="ERROR",
            file=f"{provider_name}/provider.yaml",
            message=f"Failed to parse: {e}",
            fix_hint="Fix YAML syntax errors"
        ))
    
    return issues


def check_env_var_naming(provider_dir: Path) -> list[Issue]:
    """Check that env vars use UPPER_SNAKE_CASE."""
    issues = []
    yaml_path = provider_dir / "provider.yaml"
    provider_name = provider_dir.name
    
    if not yaml_path.exists():
        return issues
    
    try:
        content = yaml_path.read_text(encoding="utf-8")
        if HAS_YAML:
            meta = yaml.safe_load(content)
        else:
            meta = load_yaml_simple(content)
        
        auth = meta.get("auth", {})
        env_vars = auth.get("env_vars", [])
        
        # Pattern: UPPER_SNAKE_CASE (starts with uppercase letter, only uppercase, digits, underscore)
        pattern = re.compile(r"^[A-Z][A-Z0-9_]*$")
        
        for var in env_vars:
            if not pattern.match(var):
                issues.append(Issue(
                    level="WARN",
                    file=f"{provider_name}/provider.yaml",
                    message=f"Env var '{var}' should be UPPER_SNAKE_CASE",
                    fix_hint=f"Rename to {var.upper().replace('-', '_')}"
                ))
                
    except Exception:
        pass  # Parsing errors handled in check_provider_metadata
    
    return issues


def check_stale_paths(base_dir: Path) -> list[Issue]:
    """Check for stale path references in documentation."""
    issues = []
    
    stale_patterns = [
        ("skills/lixinger-data-query", ".claude/plugins/query_data/lixinger-api-docs"),
        (".claude/skills/lixinger-data-query", ".claude/plugins/query_data/lixinger-api-docs"),
        ("api_new/api-docs/", "lixinger-api-docs/docs/"),
        ("plugins/query_data/lixinger-api-docs/scripts/query_tool.py", 
         ".claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py"),
    ]
    
    for md_file in base_dir.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            rel_path = md_file.relative_to(base_dir)
            
            for stale, replacement in stale_patterns:
                if stale in content:
                    issues.append(Issue(
                        level="INFO",
                        file=str(rel_path),
                        message=f"Found stale path reference: {stale}",
                        fix_hint=f"Replace with: {replacement}"
                    ))
        except Exception:
            pass
    
    return issues


def run_all_checks(base_dir: Path, provider_filter: str | None = None) -> tuple[list[Issue], list[Issue], list[Issue]]:
    """Run all checks and return categorized issues."""
    errors = []
    warnings = []
    infos = []
    
    # Check plugin manifest
    manifest_issues = check_plugin_manifest(base_dir)
    for issue in manifest_issues:
        if issue.level == "ERROR":
            errors.append(issue)
        elif issue.level == "WARN":
            warnings.append(issue)
        else:
            infos.append(issue)
    
    # Check providers
    provider_dirs = [d for d in base_dir.iterdir() if d.is_dir() and (d / "provider.yaml").exists()]
    
    for provider_dir in provider_dirs:
        if provider_filter and provider_dir.name != provider_filter:
            continue
        
        meta_issues = check_provider_metadata(provider_dir)
        for issue in meta_issues:
            if issue.level == "ERROR":
                errors.append(issue)
            elif issue.level == "WARN":
                warnings.append(issue)
            else:
                infos.append(issue)
        
        env_issues = check_env_var_naming(provider_dir)
        for issue in env_issues:
            if issue.level == "ERROR":
                errors.append(issue)
            elif issue.level == "WARN":
                warnings.append(issue)
            else:
                infos.append(issue)
    
    # Check stale paths
    stale_issues = check_stale_paths(base_dir)
    for issue in stale_issues:
        if issue.level == "ERROR":
            errors.append(issue)
        elif issue.level == "WARN":
            warnings.append(issue)
        else:
            infos.append(issue)
    
    return errors, warnings, infos


def print_report(errors: list[Issue], warnings: list[Issue], infos: list[Issue], show_hints: bool = False) -> None:
    """Print check report."""
    total = len(errors) + len(warnings) + len(infos)
    
    if total == 0:
        print("[OK] All checks passed!")
        return
    
    for issue in errors:
        print(f"[ERROR] {issue.file}: {issue.message}")
        if show_hints and issue.fix_hint:
            print(f"        Fix: {issue.fix_hint}")
    
    for issue in warnings:
        print(f"[WARN]  {issue.file}: {issue.message}")
        if show_hints and issue.fix_hint:
            print(f"        Fix: {issue.fix_hint}")
    
    for issue in infos:
        print(f"[INFO]  {issue.file}: {issue.message}")
        if show_hints and issue.fix_hint:
            print(f"        Tip: {issue.fix_hint}")
    
    print(f"\nSummary: {len(errors)} ERROR, {len(warnings)} WARN, {len(infos)} INFO")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check plugin integrity"
    )
    parser.add_argument(
        "--provider",
        help="Check specific provider only",
    )
    parser.add_argument(
        "--fix-hints",
        action="store_true",
        help="Show fix hints",
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
    
    errors, warnings, infos = run_all_checks(base_dir, args.provider)
    print_report(errors, warnings, infos, args.fix_hints)
    
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
