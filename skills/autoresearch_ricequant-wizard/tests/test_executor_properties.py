"""
属性测试：wizard_executor.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hypothesis import given, settings
from hypothesis import strategies as st

from wizard_executor import _extract_backtest_id


# ── Property 9: backtestId 解析正确性 ─────────────────────────────────────────

# Feature: autoresearch-ricequant-wizard, Property 9: backtestId 解析正确性
@settings(max_examples=100)
@given(bid=st.from_regex(r'\d{5,10}', fullmatch=True))
def test_extract_backtest_id_correctness(bid):
    """Property 9: 将 backtestId 嵌入 '回测已启动: <id>' 后应能被正确提取"""
    output = f"回测已启动: {bid}"
    result = _extract_backtest_id(output)
    assert result == bid, (
        f"Expected '{bid}' but got '{result}' from output: {output!r}"
    )
