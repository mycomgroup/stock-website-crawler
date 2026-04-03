"""
conftest.py
测试配置文件，设置正确的 Python 路径。
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
src_path = project_root / "src"

for _path in [str(src_path), str(project_root)]:
    if _path not in sys.path:
        sys.path.insert(0, _path)

try:
    import backtrader_base_strategy
except ImportError:
    pass

try:
    import factors
except ImportError:
    pass
