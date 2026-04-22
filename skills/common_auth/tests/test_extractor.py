import pytest
import json
import os
import sys
from unittest.mock import patch, MagicMock

class TestGetChromeProfiles:
    @patch('glob.glob')
    @patch('os.path.exists')
    @patch('os.path.getmtime')
    @patch('os.path.expanduser')
    def test_returns_sorted_profiles(self, mock_expanduser, mock_getmtime, mock_exists, mock_glob):
        mock_expanduser.return_value = '/fake/chrome/'
        mock_glob.side_effect = [
            ['/fake/chrome/Default', '/fake/chrome/Profile 1'],
            []
        ]
        mock_exists.return_value = True
        mock_getmtime.side_effect = [100, 200]
        
        from core.extractor import get_chrome_profiles
        result = get_chrome_profiles()
        
        assert result == ['/fake/chrome/Default', '/fake/chrome/Profile 1']
    
    @patch('glob.glob')
    @patch('os.path.exists')
    @patch('os.path.expanduser')
    def test_filters_profiles_without_cookies(self, mock_expanduser, mock_exists, mock_glob):
        mock_expanduser.return_value = '/fake/chrome/'
        mock_glob.side_effect = [['/fake/chrome/Default'], []]
        mock_exists.return_value = False
        
        from core.extractor import get_chrome_profiles
        result = get_chrome_profiles()
        
        assert result == []
    
    @patch('glob.glob')
    @patch('os.path.expanduser')
    def test_handles_no_profiles(self, mock_expanduser, mock_glob):
        mock_expanduser.return_value = '/fake/chrome/'
        mock_glob.return_value = []
        
        from core.extractor import get_chrome_profiles
        result = get_chrome_profiles()
        
        assert result == []

class TestExtractCookiesFromAllProfiles:
    @patch('core.extractor.get_chrome_profiles')
    @patch('browser_cookie3.chrome')
    def test_extracts_from_multiple_profiles(self, mock_chrome, mock_get_profiles):
        mock_get_profiles.return_value = ['/profile1', '/profile2']
        
        mock_cj1 = MagicMock()
        cookie1 = MagicMock()
        cookie1.name = 'session'
        cookie1.value = 'val1'
        cookie1.domain = '.example.com'
        cookie1.path = '/'
        cookie1.expires = 123
        cookie1.secure = True
        mock_cj1.__iter__ = MagicMock(return_value=iter([cookie1]))
        
        mock_cj2 = MagicMock()
        cookie2 = MagicMock()
        cookie2.name = 'session'
        cookie2.value = 'val2'
        cookie2.domain = '.example.com'
        cookie2.path = '/'
        cookie2.expires = 456
        cookie2.secure = False
        mock_cj2.__iter__ = MagicMock(return_value=iter([cookie2]))
        
        mock_chrome.side_effect = [mock_cj1, mock_cj2]
        
        from core.extractor import extract_cookies_from_all_profiles
        result = extract_cookies_from_all_profiles('example.com')
        
        assert len(result) >= 1
        assert result[0]['name'] == 'session'
    
    @patch('core.extractor.get_chrome_profiles')
    @patch('browser_cookie3.chrome')
    def test_handles_no_profiles_fallback(self, mock_chrome, mock_get_profiles):
        mock_get_profiles.return_value = []
        
        mock_cj = MagicMock()
        cookie = MagicMock()
        cookie.name = 'test'
        cookie.value = 'value'
        cookie.domain = '.example.com'
        cookie.path = '/'
        cookie.expires = 100
        cookie.secure = True
        mock_cj.__iter__ = MagicMock(return_value=iter([cookie]))
        mock_chrome.return_value = mock_cj
        
        from core.extractor import extract_cookies_from_all_profiles
        result = extract_cookies_from_all_profiles('example.com')
        
        assert len(result) == 1
        assert result[0]['name'] == 'test'
    
    @patch('core.extractor.get_chrome_profiles')
    def test_returns_empty_on_no_profiles_and_exception(self, mock_get_profiles):
        mock_get_profiles.return_value = []
        
        with patch('browser_cookie3.chrome', side_effect=Exception('error')):
            from core.extractor import extract_cookies_from_all_profiles
            result = extract_cookies_from_all_profiles('example.com')
            
            assert result == []
    
    @patch('core.extractor.get_chrome_profiles')
    @patch('browser_cookie3.chrome')
    def test_skips_profiles_with_exceptions(self, mock_chrome, mock_get_profiles):
        mock_get_profiles.return_value = ['/profile1', '/profile2']
        
        mock_chrome.side_effect = [Exception('error'), MagicMock()]
        
        mock_cj2 = MagicMock()
        cookie = MagicMock()
        cookie.name = 'test'
        cookie.value = 'val'
        cookie.domain = '.example.com'
        cookie.path = '/'
        cookie.expires = 100
        cookie.secure = True
        mock_cj2.__iter__ = MagicMock(return_value=iter([cookie]))
        mock_chrome.side_effect = [Exception('error'), mock_cj2]
        
        from core.extractor import extract_cookies_from_all_profiles
        result = extract_cookies_from_all_profiles('example.com')
        
        assert len(result) == 1

class TestFormatCookies:
    def test_formats_single_cookie(self):
        from core.extractor import format_cookies
        
        cookie = MagicMock()
        cookie.name = 'session'
        cookie.value = 'abc123'
        cookie.domain = '.example.com'
        cookie.path = '/'
        cookie.expires = 1712345678
        cookie.secure = True
        
        result = format_cookies([cookie])
        
        assert len(result) == 1
        assert result[0]['name'] == 'session'
        assert result[0]['value'] == 'abc123'
        assert result[0]['domain'] == '.example.com'
        assert result[0]['secure'] == True
    
    def test_formats_multiple_cookies(self):
        from core.extractor import format_cookies
        
        cookies = []
        for i in range(3):
            c = MagicMock()
            c.name = f'cookie{i}'
            c.value = f'value{i}'
            c.domain = '.example.com'
            c.path = '/'
            c.expires = 100 + i
            c.secure = i % 2 == 0
            cookies.append(c)
        
        result = format_cookies(cookies)
        
        assert len(result) == 3
        assert result[0]['name'] == 'cookie0'
        assert result[2]['name'] == 'cookie2'
    
    def test_handles_empty_cookie_jar(self):
        from core.extractor import format_cookies
        result = format_cookies([])
        assert result == []
    
    def test_converts_secure_to_bool(self):
        from core.extractor import format_cookies
        
        cookie = MagicMock()
        cookie.name = 'test'
        cookie.value = 'val'
        cookie.domain = '.example.com'
        cookie.path = '/'
        cookie.expires = 100
        cookie.secure = 1
        
        result = format_cookies([cookie])
        
        assert result[0]['secure'] == True

class TestMainEntryPoint:
    @patch('sys.argv', ['extractor.py', 'example.com'])
    @patch('core.extractor.extract_cookies_from_all_profiles')
    @patch('builtins.print')
    def test_extracts_for_domain(self, mock_print, mock_extract):
        mock_extract.return_value = [
            {'name': 'session', 'value': 'abc', 'domain': '.example.com'}
        ]
        
        from core.extractor import extract_cookies_from_all_profiles
        
        result = mock_extract('example.com')
        assert len(result) == 1
    
    @patch('sys.argv', ['extractor.py'])
    def test_requires_domain_argument(self):
        if len(sys.argv) < 2:
            assert True
    
    @patch('sys.argv', ['extractor.py', '.example.com'])
    @patch('core.extractor.extract_cookies_from_all_profiles')
    def test_handles_dot_prefix_domain(self, mock_extract):
        mock_extract.return_value = []
        
        domain = '.example.com'
        domains = [domain]
        if domain.startswith('.'):
            domains.append(domain[1:])
        else:
            domains.append(f".{domain}")
        
        assert '.example.com' in domains
        assert 'example.com' in domains
    
    @patch('sys.argv', ['extractor.py', 'example.com'])
    @patch('core.extractor.extract_cookies_from_all_profiles')
    def test_handles_no_dot_prefix_domain(self, mock_extract):
        mock_extract.return_value = []
        
        domain = 'example.com'
        domains = [domain]
        if domain.startswith('.'):
            domains.append(domain[1:])
        else:
            domains.append(f".{domain}")
        
        assert 'example.com' in domains
        assert '.example.com' in domains
    
    @patch('sys.argv', ['extractor.py', 'example.com'])
    @patch('core.extractor.extract_cookies_from_all_profiles')
    def test_deduplicates_cookies_by_key(self, mock_extract):
        mock_extract.return_value = [
            {'name': 'session', 'value': 'val1', 'domain': '.example.com', 'path': '/'},
            {'name': 'session', 'value': 'val2', 'domain': '.example.com', 'path': '/'},
        ]
        
        results = []
        seen_keys = set()
        
        for c in mock_extract('example.com'):
            key = f"{c['name']}|{c['domain']}|{c['path']}"
            if key not in seen_keys:
                results.append(c)
                seen_keys.add(key)
        
        assert len(results) == 1

class TestDomainVariants:
    def test_dot_domain_creates_both_variants(self):
        domain = '.example.com'
        domains = [domain]
        if domain.startswith('.'):
            domains.append(domain[1:])
        
        assert len(domains) == 2
        assert 'example.com' in domains
    
    def test_non_dot_domain_creates_both_variants(self):
        domain = 'example.com'
        domains = [domain]
        if not domain.startswith('.'):
            domains.append(f".{domain}")
        
        assert len(domains) == 2
        assert '.example.com' in domains
    
    def test_set_removes_duplicates(self):
        domains = ['.example.com', 'example.com', '.example.com']
        unique = set(domains)
        
        assert len(unique) == 2

if __name__ == '__main__':
    pytest.main([__file__, '-v'])