"""股票代码标准化工具：统一使用聚宽风格作为 canonical 格式。"""


def to_jq(code: str) -> str:
    """
    将各种格式转为聚宽风格：000001.XSHE / 600000.XSHG
    支持：sh600000, sz000001, 600000, 000001, 000001.SZ, 600000.SH, SZ000001, SH600000
    """
    c = code.strip()
    # 去掉 SH/SZ 前缀（大小写）
    if len(c) == 8 and c.upper().startswith(("SH", "SZ")):
        c = c[2:]
    # 去掉 sh/sz 小写前缀
    if len(c) == 8 and c.lower().startswith(("sh", "sz")):
        c = c[2:]
    # 去掉 .SH / .SZ / .XSHG / .XSHE 后缀
    if "." in c:
        c = c.split(".")[0]
    c = c.zfill(6)
    prefix = "XSHG" if c.startswith("6") else "XSHE"
    return f"{c}.{prefix}"


def to_ak(code: str) -> str:
    """转为 akshare 风格：sh600000 / sz000001"""
    jq = to_jq(code)
    num, suffix = jq.split(".")
    prefix = "sh" if suffix == "XSHG" else "sz"
    return f"{prefix}{num}"


def to_ts(code: str) -> str:
    """转为 tushare 风格：000001.SZ / 600000.SH"""
    jq = to_jq(code)
    num, suffix = jq.split(".")
    ts_suffix = "SH" if suffix == "XSHG" else "SZ"
    return f"{num}.{ts_suffix}"


def to_qlib(code: str) -> str:
    """转为 qlib 风格：SH600000 / SZ000001"""
    jq = to_jq(code)
    num, suffix = jq.split(".")
    prefix = "SH" if suffix == "XSHG" else "SZ"
    return f"{prefix}{num}"


def canonicalize(code: str) -> str:
    """返回统一的 canonical 格式（聚宽风格）"""
    return to_jq(code)
