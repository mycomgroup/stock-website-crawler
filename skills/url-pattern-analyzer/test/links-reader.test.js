/**
 * Links Reader - 单元测试 (Jest格式)
 */

const LinksReader = require('../lib/links-reader');
const fs = require('fs').promises;
const path = require('path');
const os = require('os');

describe('LinksReader', () => {
  let reader;
  let tempDir;
  
  beforeEach(() => {
    reader = new LinksReader();
  });
  
  afterEach(async () => {
    // 清理临时文件
    if (tempDir) {
      try {
        await fs.rm(tempDir, { recursive: true, force: true });
      } catch (error) {
        // 忽略清理错误
      }
      tempDir = null;
    }
  });
  
  // 辅助函数：创建临时测试文件
  async function createTestFile(filename, content) {
    tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'links-reader-test-'));
    const filePath = path.join(tempDir, filename);
    await fs.writeFile(filePath, content, 'utf-8');
    return filePath;
  }
  
  describe('readLinksFile()', () => {
    test('should read valid links file correctly', async () => {
      const validContent = `{"url":"https://example.com/page1","status":"fetched","addedAt":1234567890,"retryCount":0,"error":null}
{"url":"https://example.com/page2","status":"fetched","addedAt":1234567891,"retryCount":0,"error":null}
{"url":"https://example.com/page3","status":"pending","addedAt":1234567892,"retryCount":1,"error":"timeout"}`;
      
      const filePath = await createTestFile('links.txt', validContent);
      const records = await reader.readLinksFile(filePath);
      
      expect(records).toHaveLength(3);
      expect(records[0].url).toBe('https://example.com/page1');
      expect(records[0].status).toBe('fetched');
      expect(records[1].url).toBe('https://example.com/page2');
      expect(records[2].url).toBe('https://example.com/page3');
      expect(records[2].status).toBe('pending');
    });
    
    test('should handle files with invalid JSON lines gracefully', async () => {
      const invalidContent = `{"url":"https://example.com/page1","status":"fetched"}
invalid json line
{"url":"https://example.com/page2","status":"fetched"}
{"incomplete json
{"url":"https://example.com/page3","status":"fetched"}`;
      
      const filePath = await createTestFile('links-invalid.txt', invalidContent);
      const records = await reader.readLinksFile(filePath);
      
      // 应该跳过无效行，只返回有效记录
      expect(records).toHaveLength(3);
      expect(records[0].url).toBe('https://example.com/page1');
      expect(records[1].url).toBe('https://example.com/page2');
      expect(records[2].url).toBe('https://example.com/page3');
    });
    
    test('should handle empty file', async () => {
      const filePath = await createTestFile('empty.txt', '');
      const records = await reader.readLinksFile(filePath);
      
      expect(records).toEqual([]);
    });
    
    test('should handle file with only blank lines', async () => {
      const filePath = await createTestFile('blank-lines.txt', '\n\n\n');
      const records = await reader.readLinksFile(filePath);
      
      expect(records).toEqual([]);
    });
    
    test('should throw error for non-existent file', async () => {
      await expect(reader.readLinksFile('/nonexistent/path/links.txt'))
        .rejects.toThrow('not found');
    });
    
    test('should handle file with mixed valid and empty lines', async () => {
      const content = `{"url":"https://example.com/page1","status":"fetched"}

{"url":"https://example.com/page2","status":"fetched"}

`;
      
      const filePath = await createTestFile('mixed.txt', content);
      const records = await reader.readLinksFile(filePath);
      
      expect(records).toHaveLength(2);
    });
  });
  
  describe('extractURLs()', () => {
    test('should extract all URLs without filters', () => {
      const records = [
        { url: 'https://example.com/page1', status: 'fetched', error: null },
        { url: 'https://example.com/page2', status: 'pending', error: null },
        { url: 'https://example.com/page3', status: 'fetched', error: 'timeout' },
        { url: 'https://example.com/page4', status: 'fetched', error: null }
      ];
      
      const urls = reader.extractURLs(records);
      
      expect(urls).toHaveLength(4);
      expect(urls).toContain('https://example.com/page1');
      expect(urls).toContain('https://example.com/page2');
      expect(urls).toContain('https://example.com/page3');
      expect(urls).toContain('https://example.com/page4');
    });
    
    test('should filter URLs by status', () => {
      const records = [
        { url: 'https://example.com/page1', status: 'fetched', error: null },
        { url: 'https://example.com/page2', status: 'pending', error: null },
        { url: 'https://example.com/page3', status: 'fetched', error: null },
        { url: 'https://example.com/page4', status: 'error', error: 'failed' }
      ];
      
      const fetchedUrls = reader.extractURLs(records, { status: 'fetched' });
      
      expect(fetchedUrls).toHaveLength(2);
      expect(fetchedUrls).toContain('https://example.com/page1');
      expect(fetchedUrls).toContain('https://example.com/page3');
    });
    
    test('should exclude URLs with errors', () => {
      const records = [
        { url: 'https://example.com/page1', status: 'fetched', error: null },
        { url: 'https://example.com/page2', status: 'pending', error: null },
        { url: 'https://example.com/page3', status: 'fetched', error: 'timeout' },
        { url: 'https://example.com/page4', status: 'fetched', error: null }
      ];
      
      const noErrorUrls = reader.extractURLs(records, { excludeErrors: true });
      
      expect(noErrorUrls).toHaveLength(3);
      expect(noErrorUrls).not.toContain('https://example.com/page3');
    });
    
    test('should apply multiple filters', () => {
      const records = [
        { url: 'https://example.com/page1', status: 'fetched', error: null },
        { url: 'https://example.com/page2', status: 'pending', error: null },
        { url: 'https://example.com/page3', status: 'fetched', error: 'timeout' },
        { url: 'https://example.com/page4', status: 'fetched', error: null }
      ];
      
      const filteredUrls = reader.extractURLs(records, { 
        status: 'fetched', 
        excludeErrors: true 
      });
      
      expect(filteredUrls).toHaveLength(2);
      expect(filteredUrls).toContain('https://example.com/page1');
      expect(filteredUrls).toContain('https://example.com/page4');
    });
    
    test('should filter out records without url field', () => {
      const records = [
        { url: 'https://example.com/page1', status: 'fetched', error: null },
        { status: 'fetched', error: null }, // 缺少url字段
        { url: 'https://example.com/page2', status: 'fetched', error: null }
      ];
      
      const urls = reader.extractURLs(records);
      
      expect(urls).toHaveLength(2);
      expect(urls).toContain('https://example.com/page1');
      expect(urls).toContain('https://example.com/page2');
    });
    
    test('should return empty array for empty records', () => {
      const urls = reader.extractURLs([]);
      expect(urls).toEqual([]);
    });
  });
  
  describe('parseURLs()', () => {
    test('should parse valid URL strings', () => {
      const urlStrings = [
        'https://example.com/page1',
        'https://example.com/page2?key=value',
        'https://example.com/page3#section'
      ];
      
      const urlObjects = reader.parseURLs(urlStrings);
      
      expect(urlObjects).toHaveLength(3);
      expect(urlObjects[0]).toBeInstanceOf(URL);
      expect(urlObjects[0].href).toBe('https://example.com/page1');
      expect(urlObjects[1].searchParams.get('key')).toBe('value');
    });
    
    test('should throw error for invalid URL by default', () => {
      const urlStrings = [
        'https://example.com/page1',
        'not-a-valid-url',
        'https://example.com/page2'
      ];
      
      expect(() => reader.parseURLs(urlStrings)).toThrow('Invalid URL');
    });
    
    test('should skip invalid URLs when skipInvalid is true', () => {
      const urlStrings = [
        'https://example.com/page1',
        'not-a-valid-url',
        'https://example.com/page2',
        'also-invalid',
        'https://example.com/page3'
      ];
      
      const urlObjects = reader.parseURLs(urlStrings, { skipInvalid: true });
      
      expect(urlObjects).toHaveLength(3);
      expect(urlObjects[0].href).toBe('https://example.com/page1');
      expect(urlObjects[1].href).toBe('https://example.com/page2');
      expect(urlObjects[2].href).toBe('https://example.com/page3');
    });
    
    test('should handle empty array', () => {
      const urlObjects = reader.parseURLs([]);
      expect(urlObjects).toEqual([]);
    });
    
    test('should parse URLs with various protocols', () => {
      const urlStrings = [
        'https://example.com/page',
        'http://example.com/page',
        'ftp://example.com/file'
      ];
      
      const urlObjects = reader.parseURLs(urlStrings);
      
      expect(urlObjects).toHaveLength(3);
      expect(urlObjects[0].protocol).toBe('https:');
      expect(urlObjects[1].protocol).toBe('http:');
      expect(urlObjects[2].protocol).toBe('ftp:');
    });
  });
  
  describe('getStatistics()', () => {
    test('should calculate correct statistics', () => {
      const records = [
        { url: 'https://example.com/page1', status: 'fetched', error: null },
        { url: 'https://example.com/page2', status: 'fetched', error: null },
        { url: 'https://example.com/page3', status: 'pending', error: null },
        { url: 'https://example.com/page4', status: 'fetched', error: 'timeout' },
        { status: 'fetched', error: null } // 缺少url字段
      ];
      
      const stats = reader.getStatistics(records);
      
      expect(stats.total).toBe(5);
      expect(stats.byStatus.fetched).toBe(4);
      expect(stats.byStatus.pending).toBe(1);
      expect(stats.withErrors).toBe(1);
      expect(stats.withoutUrl).toBe(1);
    });
    
    test('should handle empty records', () => {
      const stats = reader.getStatistics([]);
      
      expect(stats.total).toBe(0);
      expect(stats.byStatus).toEqual({});
      expect(stats.withErrors).toBe(0);
      expect(stats.withoutUrl).toBe(0);
    });
    
    test('should count multiple status types', () => {
      const records = [
        { url: 'https://example.com/page1', status: 'fetched', error: null },
        { url: 'https://example.com/page2', status: 'pending', error: null },
        { url: 'https://example.com/page3', status: 'error', error: 'failed' },
        { url: 'https://example.com/page4', status: 'fetched', error: null },
        { url: 'https://example.com/page5', status: 'skipped', error: null }
      ];
      
      const stats = reader.getStatistics(records);
      
      expect(stats.byStatus.fetched).toBe(2);
      expect(stats.byStatus.pending).toBe(1);
      expect(stats.byStatus.error).toBe(1);
      expect(stats.byStatus.skipped).toBe(1);
    });
    
    test('should handle records without status field', () => {
      const records = [
        { url: 'https://example.com/page1', error: null },
        { url: 'https://example.com/page2', status: 'fetched', error: null }
      ];
      
      const stats = reader.getStatistics(records);
      
      expect(stats.total).toBe(2);
      expect(stats.byStatus.fetched).toBe(1);
    });
  });
});
