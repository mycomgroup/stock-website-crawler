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


def test_connection():
    session_file = pathlib.Path(
        "/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook/data/session.json"
    )
    session_payload = load_session(session_file)

    print(f"Session loaded from: {session_file}")
    print(f"Cookies count: {len(session_payload.get('cookies', []))}")

    # Test connection
    opener = make_opener(session_payload)
    test_url = "https://www.joinquant.com/user/21333940833/"

    try:
        request = urllib.request.Request(test_url, headers={"User-Agent": USER_AGENT})
        with opener.open(request, timeout=10) as response:
            print(f"Connection test: SUCCESS (Status {response.status})")
            return True
    except Exception as e:
        print(f"Connection test: FAILED - {e}")
        return False


if __name__ == "__main__":
    test_connection()
