/**
 * URL Pattern Analyzer - 单元测试
 */

const URLPatternAnalyzer = require('../lib/url-clusterer');

describe('URLPatternAnalyzer', () => {
  let analyzer;
  
  beforeEach(() => {
    analyzer = new URLPatternAnalyzer();
  });
  
  describe('extractFeatures()', () => {
    test('should extract URL features correctly from string URL', () => {
      const url = 'https://www.lixinger.com/open/api/doc?api-key=cn/company';
      const features = analyzer.extractFeatures(url);
      
      expect(features.protocol).toBe('https');
      expect(features.host).toBe('www.lixinger.com');
      expect(features.pathSegments).toEqual(['open', 'api', 'doc']);
      expect(features.queryParams).toEqual(['api-key']);
      expect(features.pathDepth).toBe(3);
    });
    
    test('should extract URL features correctly from URL object', () => {
      const url = new URL('https://www.lixinger.com/open/api/doc?api-key=cn/company');
      const features = analyzer.extractFeatures(url);
      
      expect(features.protocol).toBe('https');
      expect(features.host).toBe('www.lixinger.com');
      expect(features.pathSegments).toEqual(['open', 'api', 'doc']);
      expect(features.queryParams).toEqual(['api-key']);
      expect(features.pathDepth).toBe(3);
    });
    
    test('should handle URL without query parameters', () => {
      const url = 'https://www.lixinger.com/analytics/company/dashboard';
      const features = analyzer.extractFeatures(url);
      
      expect(features.queryParams).toEqual([]);
      expect(features.pathSegments).toEqual(['analytics', 'company', 'dashboard']);
    });
    
    test('should handle URL with multiple query parameters', () => {
      const url = 'https://www.lixinger.com/analytics/index/dashboard?type=cn&date=2024';
      const features = analyzer.extractFeatures(url);
      
      expect(features.queryParams).toContain('type');
      expect(features.queryParams).toContain('date');
      expect(features.queryParams.length).toBe(2);
    });
    
    test('should handle root path correctly', () => {
      const url = 'https://www.lixinger.com/';
      const features = analyzer.extractFeatures(url);
      
      expect(features.pathSegments).toEqual([]);
      expect(features.pathDepth).toBe(0);
    });
    
    test('should filter out empty path segments', () => {
      const url = 'https://www.lixinger.com/open/api/doc/';
      const features = analyzer.extractFeatures(url);
      
      expect(features.pathSegments).toEqual(['open', 'api', 'doc']);
      expect(features.pathDepth).toBe(3);
    });
  });
  
  describe('calculateSimilarity()', () => {
    test('should return high score for URLs with same path and query params', () => {
      const url1 = 'https://www.lixinger.com/open/api/doc?api-key=cn/company';
      const url2 = 'https://www.lixinger.com/open/api/doc?api-key=hk/index';
      const similarity = analyzer.calculateSimilarity(url1, url2);
      
      // 路径深度相同 +20, 3个路径段匹配 +30, 1个查询参数匹配 +5 = 55
      expect(similarity).toBe(55);
    });
    
    test('should return 0 for URLs with different protocols', () => {
      const url1 = 'https://www.lixinger.com/open/api/doc';
      const url2 = 'http://www.lixinger.com/open/api/doc';
      const similarity = analyzer.calculateSimilarity(url1, url2);
      
      expect(similarity).toBe(0);
    });
    
    test('should return 0 for URLs with different hosts', () => {
      const url1 = 'https://www.lixinger.com/open/api/doc';
      const url2 = 'https://api.lixinger.com/open/api/doc';
      const similarity = analyzer.calculateSimilarity(url1, url2);
      
      expect(similarity).toBe(0);
    });
    
    test('should calculate partial match for different paths', () => {
      const url1 = 'https://www.lixinger.com/analytics/company/dashboard';
      const url2 = 'https://www.lixinger.com/analytics/index/dashboard';
      const similarity = analyzer.calculateSimilarity(url1, url2);
      
      // 路径深度相同 +20, 第1段匹配 +10, 第3段匹配 +10 = 40
      expect(similarity).toBe(40);
    });
    
    test('should handle URLs with different path depths', () => {
      const url1 = 'https://www.lixinger.com/open/api/doc';
      const url2 = 'https://www.lixinger.com/open/api';
      const similarity = analyzer.calculateSimilarity(url1, url2);
      
      // 路径深度不同 +0, 前2段匹配 +20 = 20
      expect(similarity).toBe(20);
    });
    
    test('should add score for matching query parameters', () => {
      const url1 = 'https://www.lixinger.com/analytics/dashboard?type=cn&date=2024';
      const url2 = 'https://www.lixinger.com/analytics/dashboard?type=hk&date=2025';
      const similarity = analyzer.calculateSimilarity(url1, url2);
      
      // 路径深度相同 +20, 2段路径匹配 +20, 2个查询参数匹配 +10 = 50
      expect(similarity).toBe(50);
    });
  });
  
  describe('clusterURLs()', () => {
    test('should return empty array for empty input', () => {
      const result = analyzer.clusterURLs([]);
      expect(result).toEqual([]);
    });
    
    test('should return single cluster for single URL', () => {
      const urls = ['https://www.lixinger.com/open/api/doc?api-key=cn/company'];
      const result = analyzer.clusterURLs(urls);
      
      expect(result.length).toBe(1);
      expect(result[0]).toEqual(urls);
    });
    
    test('should cluster similar URLs together', () => {
      const urls = [
        'https://www.lixinger.com/open/api/doc?api-key=cn/company',
        'https://www.lixinger.com/open/api/doc?api-key=hk/index',
        'https://www.lixinger.com/open/api/doc?api-key=us/stock',
        'https://www.lixinger.com/analytics/company/dashboard',
        'https://www.lixinger.com/analytics/index/dashboard'
      ];
      const result = analyzer.clusterURLs(urls);
      
      // 应该有2个簇：api-doc (3个URL) 和 dashboard (2个URL)
      expect(result.length).toBe(2);
      
      // 第一个簇应该是最大的（api-doc，3个URL）
      expect(result[0].length).toBe(3);
      expect(result[0]).toContain('https://www.lixinger.com/open/api/doc?api-key=cn/company');
      expect(result[0]).toContain('https://www.lixinger.com/open/api/doc?api-key=hk/index');
      expect(result[0]).toContain('https://www.lixinger.com/open/api/doc?api-key=us/stock');
      
      // 第二个簇（dashboard，2个URL）
      expect(result[1].length).toBe(2);
      expect(result[1]).toContain('https://www.lixinger.com/analytics/company/dashboard');
      expect(result[1]).toContain('https://www.lixinger.com/analytics/index/dashboard');
    });
    
    test('should not cluster URLs with different paths', () => {
      const urls = [
        'https://www.lixinger.com/open/api/doc',
        'https://www.lixinger.com/analytics/dashboard',
        'https://www.lixinger.com/user/profile'
      ];
      const result = analyzer.clusterURLs(urls);
      
      // 这些URL路径完全不同，应该各自成簇
      expect(result.length).toBe(3);
      result.forEach(cluster => {
        expect(cluster.length).toBe(1);
      });
    });
    
    test('should cluster URLs with same path structure but different segments', () => {
      const urls = [
        'https://www.lixinger.com/analytics/company/dashboard',
        'https://www.lixinger.com/analytics/index/dashboard',
        'https://www.lixinger.com/analytics/stock/dashboard',
        'https://www.lixinger.com/analytics/fund/dashboard'
      ];
      const result = analyzer.clusterURLs(urls);
      
      // 这些URL有相同的路径结构（/analytics/*/dashboard），应该聚在一起
      expect(result.length).toBe(1);
      expect(result[0].length).toBe(4);
    });
    
    test('should handle URLs with different hosts separately', () => {
      const urls = [
        'https://www.lixinger.com/open/api/doc',
        'https://api.lixinger.com/open/api/doc',
        'https://www.lixinger.com/open/api/doc?key=value'
      ];
      const result = analyzer.clusterURLs(urls);
      
      // 不同主机的URL不应该聚在一起
      expect(result.length).toBe(2);
      
      // 相同主机的应该聚在一起
      const samehostCluster = result.find(cluster => cluster.length === 2);
      expect(samehostCluster).toBeDefined();
      expect(samehostCluster).toContain('https://www.lixinger.com/open/api/doc');
      expect(samehostCluster).toContain('https://www.lixinger.com/open/api/doc?key=value');
    });
    
    test('should sort clusters by size in descending order', () => {
      const urls = [
        'https://www.lixinger.com/a',
        'https://www.lixinger.com/b/c',
        'https://www.lixinger.com/b/d',
        'https://www.lixinger.com/b/e',
        'https://www.lixinger.com/x/y/z',
        'https://www.lixinger.com/x/y/w'
      ];
      const result = analyzer.clusterURLs(urls);
      
      // 验证簇按大小降序排列
      for (let i = 0; i < result.length - 1; i++) {
        expect(result[i].length).toBeGreaterThanOrEqual(result[i + 1].length);
      }
    });
  });
  
  describe('generatePattern()', () => {
    test('should throw error for empty URL group', () => {
      expect(() => analyzer.generatePattern([])).toThrow('URL group cannot be empty');
    });
    
    test('should generate pattern for single URL', () => {
      const urls = ['https://www.lixinger.com/open/api/doc?api-key=cn/company'];
      const result = analyzer.generatePattern(urls);
      
      expect(result.pattern).toBe('https://www\\.lixinger\\.com/open/api/doc\\?api-key=cn/company');
      expect(result.pathTemplate).toBe('/open/api/doc');
      expect(result.queryParams).toEqual(['api-key']);
    });
    
    test('should generate pattern for URLs with same path and different query values', () => {
      const urls = [
        'https://www.lixinger.com/open/api/doc?api-key=cn/company',
        'https://www.lixinger.com/open/api/doc?api-key=hk/index',
        'https://www.lixinger.com/open/api/doc?api-key=us/stock'
      ];
      const result = analyzer.generatePattern(urls);
      
      // 路径固定，查询参数键相同但值不同
      expect(result.pattern).toContain('/open/api/doc');
      expect(result.pattern).toContain('api-key=');
      expect(result.pathTemplate).toBe('/open/api/doc');
      expect(result.queryParams).toEqual(['api-key']);
    });
    
    test('should generate pattern with variable path segments', () => {
      const urls = [
        'https://www.lixinger.com/analytics/company/dashboard',
        'https://www.lixinger.com/analytics/index/dashboard',
        'https://www.lixinger.com/analytics/stock/dashboard'
      ];
      const result = analyzer.generatePattern(urls);
      
      // 第一段和第三段固定，第二段变化
      expect(result.pattern).toContain('/analytics/');
      expect(result.pattern).toContain('/dashboard');
      expect(result.pattern).toMatch(/\(\[\^\/\]\+\)/); // 包含捕获组
      expect(result.pathTemplate).toBe('/analytics/{param1}/dashboard');
      expect(result.queryParams).toEqual([]);
    });
    
    test('should generate pattern for URLs without query parameters', () => {
      const urls = [
        'https://www.lixinger.com/analytics/company/dashboard',
        'https://www.lixinger.com/analytics/index/dashboard'
      ];
      const result = analyzer.generatePattern(urls);
      
      expect(result.pattern).not.toContain('?');
      expect(result.queryParams).toEqual([]);
    });
    
    test('should generate pattern for URLs with multiple query parameters', () => {
      const urls = [
        'https://www.lixinger.com/analytics/dashboard?type=cn&date=2024',
        'https://www.lixinger.com/analytics/dashboard?type=hk&date=2025'
      ];
      const result = analyzer.generatePattern(urls);
      
      expect(result.pattern).toContain('type=');
      expect(result.pattern).toContain('date=');
      expect(result.queryParams).toContain('type');
      expect(result.queryParams).toContain('date');
      expect(result.queryParams.length).toBe(2);
    });
    
    test('should throw error for URLs with different protocols', () => {
      const urls = [
        'https://www.lixinger.com/open/api/doc',
        'http://www.lixinger.com/open/api/doc'
      ];
      
      expect(() => analyzer.generatePattern(urls)).toThrow('same protocol and host');
    });
    
    test('should throw error for URLs with different hosts', () => {
      const urls = [
        'https://www.lixinger.com/open/api/doc',
        'https://api.lixinger.com/open/api/doc'
      ];
      
      expect(() => analyzer.generatePattern(urls)).toThrow('same protocol and host');
    });
    
    test('should handle URLs with different path lengths', () => {
      const urls = [
        'https://www.lixinger.com/open/api',
        'https://www.lixinger.com/open/api/doc'
      ];
      const result = analyzer.generatePattern(urls);
      
      // 路径长度不同，使用宽松匹配
      expect(result.pattern).toContain('/.*');
    });
    
    test('should handle URLs with different query parameters', () => {
      const urls = [
        'https://www.lixinger.com/analytics/dashboard?type=cn',
        'https://www.lixinger.com/analytics/dashboard?date=2024'
      ];
      const result = analyzer.generatePattern(urls);
      
      // 查询参数不同，使用宽松匹配
      expect(result.pattern).toMatch(/\(\\\?\.\*\)\?/);
      expect(result.queryParams).toContain('type');
      expect(result.queryParams).toContain('date');
    });
    
    test('should escape special regex characters in URLs', () => {
      const urls = ['https://www.lixinger.com/api/v1.0/doc'];
      const result = analyzer.generatePattern(urls);
      
      // 点号应该被转义
      expect(result.pattern).toContain('\\.');
    });
    
    test('should generate correct path template with multiple variable segments', () => {
      const urls = [
        'https://www.lixinger.com/analytics/company/cn/dashboard',
        'https://www.lixinger.com/analytics/index/hk/dashboard',
        'https://www.lixinger.com/analytics/stock/us/dashboard'
      ];
      const result = analyzer.generatePattern(urls);
      
      // 第一段和最后一段固定，中间两段变化
      expect(result.pathTemplate).toBe('/analytics/{param1}/{param2}/dashboard');
    });
    
    test('should handle root path correctly', () => {
      const urls = [
        'https://www.lixinger.com/',
        'https://www.lixinger.com/'
      ];
      const result = analyzer.generatePattern(urls);
      
      expect(result.pathTemplate).toBe('/');
      expect(result.queryParams).toEqual([]);
    });
    
    test('should generate pattern for complex real-world URLs', () => {
      const urls = [
        'https://www.lixinger.com/open/api/doc?api-key=cn/company/fundamental',
        'https://www.lixinger.com/open/api/doc?api-key=hk/index/valuation',
        'https://www.lixinger.com/open/api/doc?api-key=us/stock/financial'
      ];
      const result = analyzer.generatePattern(urls);
      
      expect(result.pattern).toContain('https://www\\.lixinger\\.com');
      expect(result.pattern).toContain('/open/api/doc');
      expect(result.pattern).toContain('api-key=');
      expect(result.pathTemplate).toBe('/open/api/doc');
      expect(result.queryParams).toEqual(['api-key']);
    });
  });
});
