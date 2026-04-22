import json
import os
from typing import Optional, Dict, Any, List

DEFAULT_INPUT_FILE = os.path.join(os.path.dirname(__file__), 'guorn_meta_full.json')
DEFAULT_OUTPUT_MD = os.path.join(os.path.dirname(__file__), 'GUORN_INDICATORS_CATALOG.md')
DEFAULT_OUTPUT_JSON = os.path.join(os.path.dirname(__file__), 'indicator_mapping.json')


def to_middle_name(id_str: Optional[str]) -> str:
    """
    Extract middle name from ID string.
    
    Args:
        id_str: ID string in format '0.M.Category_Name.0' or any string
        
    Returns:
        Extracted middle name or original string if format doesn't match
        
    Examples:
        >>> to_middle_name('0.M.行情数据.0')
        '行情数据'
        >>> to_middle_name('0.M.Test.0')
        'Test'
        >>> to_middle_name('invalid')
        'invalid'
        >>> to_middle_name('')
        ''
        >>> to_middle_name(None)
        ''
    """
    if not id_str:
        return ''
    
    if id_str.startswith('0.'):
        parts = id_str.split('.')
        if len(parts) >= 3:
            return parts[2]
    return id_str


def process_meta(
    input_file: Optional[str] = None,
    output_md: Optional[str] = None,
    output_json: Optional[str] = None
) -> Dict[str, Any]:
    """
    Process guorn meta data and generate catalog files.
    
    Args:
        input_file: Path to input JSON file. Defaults to guorn_meta_full.json in same directory.
        output_md: Path to output Markdown file. Defaults to GUORN_INDICATORS_CATALOG.md in same directory.
        output_json: Path to output JSON file. Defaults to indicator_mapping.json in same directory.
        
    Returns:
        Dictionary containing the generated catalog with 'functions' and 'indicators' lists.
        
    Raises:
        FileNotFoundError: If input file doesn't exist.
        json.JSONDecodeError: If input file contains invalid JSON.
        PermissionError: If cannot write to output files.
    """
    input_file = input_file or DEFAULT_INPUT_FILE
    output_md = output_md or DEFAULT_OUTPUT_MD
    output_json = output_json or DEFAULT_OUTPUT_JSON
    
    with open(input_file, 'r', encoding='utf-8') as f:
        meta = json.load(f)
        
    data = meta.get('data', {})
    
    catalog: Dict[str, List[Dict[str, Any]]] = {
        "functions": [],
        "indicators": []
    }
    
    functions_blocks = data.get('function', {}).get('measures', [])
    md_content = "# 果仁网指标与函数全量手册 (Guorn Indicators Catalog)\n\n"
    md_content += "> 此文档由全量元数据自动生成，包含各分类下的函数与技术指标说明。\n\n"
    
    md_content += "## 1. 系统函数 (Functions)\n"
    for block in functions_blocks:
        cat_name = block.get('name', '未分类')
        md_content += f"### {cat_name}\n"
        md_content += "| 函数名 | 表达式 | 说明 |\n"
        md_content += "| :--- | :--- | :--- |\n"
        for val in block.get('values', []):
            name = val.get('name', '')
            expr = val.get('expr', '').replace('|', '\\|')
            desc = val.get('desc', '').replace('<br/>', ' ').replace('\n', ' ')
            md_content += f"| {name} | `{expr}` | {desc} |\n"
            catalog["functions"].append({"name": name, "expr": expr, "desc": desc, "category": cat_name})
        md_content += "\n"

    md_content += "## 2. 常用指标 (Standard Indicators)\n"

    first_measures = data.get('first_measures', [])
    for block in first_measures:
        cat_name = block.get('name', '未分类')
        md_content += f"### {cat_name}\n"
        md_content += "| 界面名 | 限定名 (建议) | 说明 |\n"
        md_content += "| :--- | :--- | :--- |\n"
        for val in block.get('values', []):
            name = val.get('name', '')
            id_val = val.get('id', '')
            middle_name = to_middle_name(id_val)
            desc = val.get('desc', '').replace('<br/>', ' ').replace('\n', ' ')
            md_content += f"| {name} | `{middle_name}` | {desc} |\n"
            
            indicator_entry = {
                "name": name, 
                "middle_name": middle_name,
                "id": id_val, 
                "desc": desc, 
                "category": cat_name,
                "expr": val.get('expr', '')
            }
            catalog["indicators"].append(indicator_entry)
        md_content += "\n"
        
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {output_md} and {output_json}")
    
    return catalog

if __name__ == "__main__":
    process_meta()
