#!/usr/bin/env python3
import argparse
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


def load_session(session_file: pathlib.Path) -> dict:
    return json.loads(session_file.read_text(encoding="utf-8"))


def resolve_direct_notebook_url(notebook_url: str) -> str:
    parsed = urllib.parse.urlparse(notebook_url)
    query = urllib.parse.parse_qs(parsed.query)
    embedded = query.get("url", [None])[0]
    if embedded and embedded.startswith("/"):
        return urllib.parse.urljoin(f"{parsed.scheme}://{parsed.netloc}", embedded)
    return notebook_url


def build_cookie_jar(session_payload: dict) -> CookieJar:
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


def make_opener(session_payload: dict) -> urllib.request.OpenerDirector:
    jar = build_cookie_jar(session_payload)
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def request_json(
    opener,
    url: str,
    xsrf_token: str,
    method: str = "GET",
    payload=None,
    referer: str | None = None,
):
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


def make_code_cell(source: str) -> dict:
    return {
        "metadata": {"trusted": True},
        "cell_type": "code",
        "source": source,
        "execution_count": None,
        "outputs": [],
    }


def close_session(
    opener, api_root: str, xsrf_token: str, session_id: str, referer: str
) -> bool:
    """
    关闭 Jupyter Notebook session

    Args:
        opener: urllib opener with cookies
        api_root: API base URL
        xsrf_token: XSRF token for authentication
        session_id: Session ID to close
        referer: Referer URL

    Returns:
        True if successfully closed, False otherwise
    """
    try:
        session_url = urllib.parse.urljoin(api_root, f"sessions/{session_id}")
        request_json(opener, session_url, xsrf_token, method="DELETE", referer=referer)
        return True
    except Exception as e:
        print(f"关闭 session 失败: {e}")
        return False


def execute_code(
    ws_url: str, cookie_header: str, origin: str, referer: str, code: str
) -> dict:
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
        while time.time() - start < 120:
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--session-file", default="data/session.json")
    parser.add_argument(
        "--notebook-url",
        default="https://www.joinquant.com/user/21333940833/notebooks/test.ipynb",
    )
    parser.add_argument("--cell-source", default='print("hello")')
    args = parser.parse_args()

    session_payload = load_session(pathlib.Path(args.session_file))
    opener = make_opener(session_payload)
    direct_notebook_url = resolve_direct_notebook_url(args.notebook_url)
    parsed = urllib.parse.urlparse(direct_notebook_url)
    path_parts = [segment for segment in parsed.path.split("/") if segment]
    user_id = path_parts[1]
    notebook_path = "/".join(path_parts[3:])
    base_url = (
        session_payload.get("pageState", {})
        .get("notebook", {})
        .get("baseUrl", f"/user/{user_id}/")
    )
    origin = f"{parsed.scheme}://{parsed.netloc}"
    api_root = urllib.parse.urljoin(origin, f"{base_url}api/")
    xsrf_token = next(
        item["value"] for item in session_payload["cookies"] if item["name"] == "_xsrf"
    )
    cookie_header = "; ".join(
        f"{item['name']}={str(item['value']).strip('"')}"
        for item in session_payload["cookies"]
        if item["domain"] == "www.joinquant.com"
    )

    notebook_url = urllib.parse.urljoin(
        api_root,
        f"contents/{urllib.parse.quote(notebook_path)}?type=notebook&_={int(time.time() * 1000)}",
    )
    notebook_model = request_json(
        opener, notebook_url, xsrf_token, referer=direct_notebook_url
    )
    notebook_content = notebook_model["content"]
    notebook_content["cells"].append(make_code_cell(args.cell_source))

    save_url = urllib.parse.urljoin(
        api_root, f"contents/{urllib.parse.quote(notebook_path)}"
    )
    request_json(
        opener,
        save_url,
        xsrf_token,
        method="PUT",
        payload={"type": "notebook", "content": notebook_content},
        referer=direct_notebook_url,
    )

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
        referer=direct_notebook_url,
    )

    session_id = session_info["id"]
    kernel_id = session_info["kernel"]["id"]

    try:
        cell_index = len(notebook_content["cells"]) - 1
        cell = notebook_content["cells"][cell_index]
        ws_origin = origin.replace("https://", "wss://").replace("http://", "ws://")
        ws_url = f"{ws_origin}{base_url}api/kernels/{kernel_id}/channels?session_id={uuid.uuid4().hex}"
        result = execute_code(
            ws_url, cookie_header, origin, direct_notebook_url, cell.get("source", "")
        )
        cell["execution_count"] = result["execution_count"]
        cell["outputs"] = result["outputs"]

        request_json(
            opener,
            save_url,
            xsrf_token,
            method="PUT",
            payload={"type": "notebook", "content": notebook_content},
            referer=direct_notebook_url,
        )

        print(result["text_output"])

    finally:
        close_session(opener, api_root, xsrf_token, session_id, direct_notebook_url)


if __name__ == "__main__":
    main()
