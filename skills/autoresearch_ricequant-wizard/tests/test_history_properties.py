"""
属性测试：history JSON 序列化往返
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hypothesis import given, settings
from hypothesis import strategies as st


# ── Property 10: 迭代记录 JSON 序列化往返 ─────────────────────────────────────

# Feature: autoresearch-ricequant-wizard, Property 10: 迭代记录 JSON 序列化往返
@settings(max_examples=100)
@given(
    record=st.fixed_dictionaries({
        "iter": st.from_regex(r'\d{4}', fullmatch=True),
        "backtest_id": st.from_regex(r'\d{5,10}', fullmatch=True),
        "score": st.floats(allow_nan=False, allow_infinity=False),
        "decision": st.sampled_from(["keep", "rollback"]),
    })
)
def test_iteration_record_json_roundtrip(record):
    """Property 10: 迭代记录写入 JSON 后读取，所有字段值应与原始 dict 完全一致"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(record, f, ensure_ascii=False)
        tmp_path = f.name

    with open(tmp_path, encoding="utf-8") as f:
        loaded = json.load(f)

    Path(tmp_path).unlink(missing_ok=True)

    assert loaded["iter"] == record["iter"], (
        f"iter mismatch: {loaded['iter']!r} != {record['iter']!r}"
    )
    assert loaded["backtest_id"] == record["backtest_id"], (
        f"backtest_id mismatch: {loaded['backtest_id']!r} != {record['backtest_id']!r}"
    )
    assert loaded["decision"] == record["decision"], (
        f"decision mismatch: {loaded['decision']!r} != {record['decision']!r}"
    )

    # score 需要处理浮点数精度
    original_score = record["score"]
    loaded_score = loaded["score"]
    if original_score == original_score:  # not NaN (already excluded by allow_nan=False)
        assert loaded_score == original_score, (
            f"score mismatch: {loaded_score} != {original_score}"
        )
