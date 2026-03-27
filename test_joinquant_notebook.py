#!/usr/bin/env python3
import json
import pathlib
import ssl
import time
import urllib.parse
import urllib.request
import uuid
from http.cookiejar import Cookie, CookieJar

try:
    import websocket
except ImportError as exc:
    raise SystemExit("请先安装 websocket-client: pip install websocket-client") from exc

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"


def load_session(session_file):
    return json.loads(session_file.read_text(encoding="utf-8"))


def build_cookie_jar(session_payload):
    jar = CookieJar()
    for item in session_payload.get("cookies", []):
        cookie = Cookie(
            version=0,
            name=item["name"],
            value=str(item["value"]).strip('"'),
            port=None,
            port_specified=False,
            domain=item["domain"],
            domain_specified=True,
            domain_initial_dot=item["domain"].startswith("."),
            path=item.get("path", "/"),
            path_specified=True,
            secure=bool(item.get("secure")),
            expires=None if item.get("expires", -1) == -1 else int(item["expires"]),
            discard=item.get("expires", -1) == -1,
            comment=None,
            comment_url=None,
            rest={"HttpOnly": item.get("httpOnly", False)},
            rfc2109=False,
        )
        jar.set_cookie(cookie)
    return jar


def make_opener(session_payload):
    jar = build_cookie_jar(session_payload)
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def request_json(opener, url, xsrf_token, method="GET", payload=None, referer=None):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "X-Requested-With": "XMLHttpRequest",
        "X-Xsrftoken": xsrf_token,
        "Referer": referer or url,
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with opener.open(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def make_code_cell(source):
    return {
        "metadata": {"trusted": True},
        "cell_type": "code",
        "source": source,
        "execution_count": None,
        "outputs": [],
    }


def execute_code(ws_url, cookie_header, origin, referer, code):
    websocket.enableTrace(False)
    msg_id = uuid.uuid4().hex
    ws_session_id = uuid.uuid4().hex
    request_payload = {
        "header": {
            "msg_id": msg_id,
            "username": "username",
            "session": ws_session_id,
            "msg_type": "execute_request",
            "version": "5.2",
        },
        "metadata": {},
        "content": {
            "code": code,
            "silent": False,
            "store_history": True,
            "user_expressions": {},
            "allow_stdin": True,
            "stop_on_error": True,
        },
        "buffers": [],
        "parent_header": {},
        "channel": "shell",
    }
    outputs = []
    reply = None
    execution_count = None
    idle = False

    ws = websocket.create_connection(
        ws_url,
        timeout=30,
        sslopt={"cert_reqs": ssl.CERT_NONE},
        origin=origin,
        cookie=cookie_header,
        header=[
            f"Referer: {referer}",
            f"User-Agent: {USER_AGENT}",
            "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8",
        ],
    )
    try:
        ws.send(json.dumps(request_payload))
        start = time.time()
        while time.time() - start < 30:
            message = json.loads(ws.recv())
            if message.get("parent_header", {}).get("msg_id") != msg_id:
                continue
            msg_type = message.get("msg_type")
            content = message.get("content", {})
            if msg_type == "execute_input":
                execution_count = content.get("execution_count", execution_count)
            elif msg_type == "stream":
                outputs.append(
                    {
                        "output_type": "stream",
                        "name": content.get("name", "stdout"),
                        "text": content.get("text", ""),
                    }
                )
            elif msg_type == "error":
                outputs.append(
                    {
                        "output_type": "error",
                        "ename": content.get("ename"),
                        "evalue": content.get("evalue"),
                        "traceback": content.get("traceback", []),
                    }
                )
            elif msg_type == "execute_result":
                outputs.append(
                    {
                        "output_type": "execute_result",
                        "data": content.get("data", {}),
                        "metadata": content.get("metadata", {}),
                        "execution_count": content.get("execution_count"),
                    }
                )
            elif msg_type in ("display_data", "update_display_data"):
                outputs.append(
                    {
                        "output_type": "display_data",
                        "data": content.get("data", {}),
                        "metadata": content.get("metadata", {}),
                    }
                )
            elif msg_type == "execute_reply":
                reply = content
                execution_count = content.get("execution_count", execution_count)
            elif msg_type == "status" and content.get("execution_state") == "idle":
                idle = True
            if idle and reply is not None:
                return {
                    "msg_id": msg_id,
                    "execution_count": execution_count,
                    "outputs": outputs,
                    "reply": reply,
                    "text_output": "".join(
                        output.get("text", "")
                        for output in outputs
                        if output.get("output_type") == "stream"
                    ),
                }
        raise RuntimeError("执行超时")
    finally:
        ws.close()


def test_notebook(cell_source):
    session_file = pathlib.Path(
        "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/data/session.json"
    )
    session_payload = load_session(session_file)
    notebook_url = session_payload["directNotebookUrl"]
    opener = make_opener(session_payload)

    parsed = urllib.parse.urlparse(notebook_url)
    path_parts = [segment for segment in parsed.path.split("/") if segment]
    user_id = path_parts[1]
    notebook_path = "test.ipynb"
    base_url = f"/user/{user_id}/"
    origin = f"{parsed.scheme}://{parsed.netloc}"
    api_root = urllib.parse.urljoin(origin, f"{base_url}api/")

    xsrf_token = next(
        (
            item["value"]
            for item in session_payload["cookies"]
            if item["name"] == "_xsrf"
        ),
        None,
    )
    cookie_header = "; ".join(
        f"{item['name']}={str(item['value']).strip('"')}"
        for item in session_payload["cookies"]
        if item["domain"] == "www.joinquant.com"
    )

    # Get notebook content
    notebook_url_api = urllib.parse.urljoin(
        api_root,
        f"contents/{urllib.parse.quote(notebook_path)}?type=notebook&_={int(time.time() * 1000)}",
    )
    notebook_model = request_json(
        opener, notebook_url_api, xsrf_token, referer=notebook_url
    )
    notebook_content = notebook_model["content"]

    # Add new cell
    notebook_content["cells"].append(make_code_cell(cell_source))

    # Save notebook
    save_url = urllib.parse.urljoin(
        api_root, f"contents/{urllib.parse.quote(notebook_path)}"
    )
    request_json(
        opener,
        save_url,
        xsrf_token,
        method="PUT",
        payload={"type": "notebook", "content": notebook_content},
        referer=notebook_url,
    )

    # Create session
    session_url = urllib.parse.urljoin(api_root, "sessions")
    session_info = request_json(
        opener,
        session_url,
        xsrf_token,
        method="POST",
        payload={
            "path": notebook_path,
            "type": "notebook",
            "name": "",
            "kernel": {"id": None, "name": "python3"},
        },
        referer=notebook_url,
    )

    # Execute the cell
    kernel_id = session_info["kernel"]["id"]
    cell_index = len(notebook_content["cells"]) - 1
    ws_origin = origin.replace("https://", "wss://").replace("http://", "ws://")
    ws_url = f"{ws_origin}{base_url}api/kernels/{kernel_id}/channels?session_id={uuid.uuid4().hex}"

    result = execute_code(ws_url, cookie_header, origin, notebook_url, cell_source)

    print(f"Execution count: {result['execution_count']}")
    print(f"Outputs: {result['outputs']}")
    return result


if __name__ == "__main__":
    # Test 1: 打印测试
    print("=" * 40)
    print("测试1: 打印测试")
    print("=" * 40)
    result = test_notebook(
        'print("测试连接成功，当前时间:", __import__("datetime").datetime.now())'
    )
    print(f"Result: {result.get('text_output', '')}")

    # Test 2: 获取聚宽因子库
    print("\n" + "=" * 40)
    print("测试2: 获取聚宽因子库")
    print("=" * 40)
    code = """
from jqfactor import get_all_factors
all_factors = get_all_factors()
print(f"聚宽因子总数: {len(all_factors)}")
print("因子分类统计:")
print(all_factors['category'].value_counts())
"""
    result = test_notebook(code)
    print(f"Result: {result.get('text_output', '')}")

    # Test 3: 过滤函数测试
    print("\n" + "=" * 40)
    print("测试3: 过滤函数测试")
    print("=" * 40)
    code = """
from jqdata import *
from datetime import datetime, timedelta

# 使用 get_current_data 测试
curr_data = get_current_data()
print(f"当前市场股票数量: {len(curr_data)}")

# 统计ST股票
st_count = sum(1 for s in curr_data.values() if s.is_st)
paused_count = sum(1 for s in curr_data.values() if s.paused)
print(f"ST股票数量: {st_count}")
print(f"停牌股票数量: {paused_count}")
"""
    result = test_notebook(code)
    if result.get("outputs"):
        for output in result["outputs"]:
            if output.get("output_type") == "execute_result":
                print(f"Result: {output}")
            elif output.get("output_type") == "stream":
                print(f"Stream: {output.get('text', '')}")
    else:
        print(f"Text output: {result.get('text_output', '')}")
