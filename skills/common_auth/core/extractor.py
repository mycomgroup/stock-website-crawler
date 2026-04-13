import browser_cookie3
import json
import sys
import os
import glob

def get_chrome_profiles():
    # macOS Chrome 默认路径
    base_path = os.path.expanduser('~/Library/Application Support/Google/Chrome/')
    
    # 获取 Default 和 Profile * 目录
    profiles = glob.glob(os.path.join(base_path, 'Default')) + \
               glob.glob(os.path.join(base_path, 'Profile *'))
    
    # 按 Cookies 文件的最后修改时间排序，活跃的排在后面（覆盖前面的）
    profile_info = []
    for p in profiles:
        c_path = os.path.join(p, 'Cookies')
        if os.path.exists(c_path):
            profile_info.append((p, os.path.getmtime(c_path)))
    
    # 按修改时间升序排序，这样修改时间最新的 profile 会在循环中最后被处理，从而覆盖前面的旧数据
    profile_info.sort(key=lambda x: x[1])
    return [p[0] for p in profile_info]

def extract_cookies_from_all_profiles(domain):
    all_cookies = {}
    profiles = get_chrome_profiles()
    
    if not profiles:
        try:
            cj = browser_cookie3.chrome(domain_name=domain)
            return format_cookies(cj)
        except:
            return []

    for profile_path in profiles:
        cookie_file = os.path.join(profile_path, 'Cookies')
        try:
            cj = browser_cookie3.chrome(cookie_file=cookie_file, domain_name=domain)
            for cookie in cj:
                key = f"{cookie.name}|{cookie.domain}|{cookie.path}"
                # 智能合并逻辑：活跃 Profile 的非空 Cookie 优先
                if key not in all_cookies or cookie.value:
                    all_cookies[key] = {
                        'name': cookie.name,
                        'value': cookie.value,
                        'domain': cookie.domain,
                        'path': cookie.path,
                        'expires': cookie.expires,
                        'secure': bool(cookie.secure)
                    }
        except Exception:
            continue
            
    return list(all_cookies.values())

def format_cookies(cj):
    cookies_list = []
    for cookie in cj:
        cookies_list.append({
            'name': cookie.name,
            'value': cookie.value,
            'domain': cookie.domain,
            'path': cookie.path,
            'expires': cookie.expires,
            'secure': bool(cookie.secure)
        })
    return cookies_list

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extractor.py <domain>", file=sys.stderr)
        sys.exit(1)
        
    domain_to_extract = sys.argv[1]
    # 如果域名是以 . 开头，尝试提取带点和不带点的两种情况
    domains = [domain_to_extract]
    if domain_to_extract.startswith('.'):
        domains.append(domain_to_extract[1:])
    else:
        domains.append(f".{domain_to_extract}")
        
    results = []
    seen_keys = set()
    
    for d in set(domains):
        cookies = extract_cookies_from_all_profiles(d)
        for c in cookies:
            key = f"{c['name']}|{c['domain']}|{c['path']}"
            if key not in seen_keys:
                results.append(c)
                seen_keys.add(key)
    
    if results:
        print(json.dumps(results, indent=2))
        sys.exit(0)
    else:
        sys.exit(1)
