import browser_cookie3
import json
import sys
import os

def extract_cookies():
    try:
        # 尝试通过 browser_cookie3 从 Chrome 提取 Cookie
        # 它会自动处理 macOS Keychain 解密
        cj = browser_cookie3.chrome(domain_name='.10jqka.com.cn')
        
        cookies_list = []
        for cookie in cj:
            cookies_list.append({
                'name': cookie.name,
                'value': cookie.value,
                'domain': cookie.domain,
                'path': cookie.path,
                'expires': cookie.expires,
                'httpOnly': False, # cj 对象中通常没有这个，默认为 False
                'secure': cookie.secure
            })
            
        if not cookies_list:
            # 尝试更大范围的域名匹配
            cj = browser_cookie3.chrome(domain_name='10jqka.com.cn')
            for cookie in cj:
                cookies_list.append({
                    'name': cookie.name,
                    'value': cookie.value,
                    'domain': cookie.domain,
                    'path': cookie.path,
                    'expires': cookie.expires,
                    'httpOnly': False,
                    'secure': cookie.secure
                })

        return cookies_list
    except Exception as e:
        print(f"Error extracting cookies: {str(e)}", file=sys.stderr)
        return []

if __name__ == "__main__":
    cookies = extract_cookies()
    if cookies:
        print(json.dumps(cookies, indent=2))
        sys.exit(0)
    else:
        sys.exit(1)
