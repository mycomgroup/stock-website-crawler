"""
conftest.py
factors 单元测试配置文件。
"""

import sys
from pathlib import Path

# 确保项目路径在 sys.path 中
project_root = Path(__file__).parent.parent.parent.parent
src_path = project_root / "src"

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))