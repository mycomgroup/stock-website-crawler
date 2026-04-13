import json
import os

def process_meta():
    input_file = '/Users/fengzhi/Downloads/git/testlixingren/skills/guorn_strategy/guorn_meta_full.json'
    output_md = '/Users/fengzhi/Downloads/git/testlixingren/skills/guorn_strategy/GUORN_INDICATORS_CATALOG.md'
    output_json = '/Users/fengzhi/Downloads/git/testlixingren/skills/guorn_strategy/indicator_mapping.json'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        meta = json.load(f)
        
    data = meta.get('data', {})
    
    catalog = {
        "functions": [],
        "indicators": []
    }
    
    # 1. Functions
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

    # 2. Indicators (from measures and first_measures)
    md_content += "## 2. 常用指标 (Standard Indicators)\n"
    
    # helper to clean IDs into middle names
    def to_middle_name(id_str):
        if id_str.startswith('0.'):
            # 0.M.Category_Name.0 -> Category_Name
            parts = id_str.split('.')
            if len(parts) >= 3:
                return parts[2]
        return id_str

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
        
    # Write MD
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    # Write Cleaned JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {output_md} and {output_json}")

if __name__ == "__main__":
    process_meta()
