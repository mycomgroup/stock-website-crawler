import { jest } from '@jest/globals';
import { HTMLFetcher } from '../lib/html-fetcher.js';

describe('HTMLFetcher', () => {
  let fetcher;
  let mockBrowserManager;
  let mockBrowser;
  let mockPage;

  beforeEach(() => {
    // Create mock page
    mockPage = {
      goto: jest.fn().mockResolvedValue(undefined),
      waitForTimeout: jest.fn().mockResolvedValue(undefined),
      content: jest.fn().mockResolvedValue('<html><body>Test</body></html>'),
      title: jest.fn().mockResolvedValue('Test Page'),
      url: jest.fn().mockReturnValue('https://example.com'),
      close: jest.fn().mockResolvedValue(undefined)
    };

    // Create mock browser
    mockBrowser = {
      newPage: jest.fn().mockResolvedValue(mockPage)
    };

    // Create mock browser manager
    mockBrowserManager = {
      getBrowser: jest.fn().mockReturnValue(mockBrowser)
    };

    fetcher = new HTMLFetcher(mockBrowserManager);
  });

  test('should create fetcher with default timeout', () => {
    expect(fetcher.timeout).toBe(30000);
  });

  test('should create fetcher with custom timeout', () => {
    fetcher = new HTMLFetcher(mockBrowserManager, 60000);
    expect(fetcher.timeout).toBe(60000);
  });

  test('should fetch single URL successfully', async () => {
    const result = await fetcher.fetchOne('https://example.com');

    expect(result.url).toBe('https://example.com');
    expect(result.html).toBe('<html><body>Test</body></html>');
    expect(result.title).toBe('Test Page');
    expect(result.timestamp).toBeDefined();
    expect(mockPage.goto).toHaveBeenCalledWith('https://example.com', {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    expect(mockPage.close).toHaveBeenCalled();
  });

  test('should throw error if browser not launched', async () => {
    mockBrowserManager.getBrowser.mockReturnValue(null);

    await expect(
      fetcher.fetchOne('https://example.com')
    ).rejects.toThrow('Browser not launched');
  });

  test('should handle timeout error', async () => {
    const timeoutError = new Error('Timeout');
    timeoutError.name = 'TimeoutError';
    mockPage.goto.mockRejectedValue(timeoutError);

    await expect(
      fetcher.fetchOne('https://example.com')
    ).rejects.toThrow('Timeout loading');
    
    expect(mockPage.close).toHaveBeenCalled();
  });

  test('should handle network error', async () => {
    mockPage.goto.mockRejectedValue(new Error('Network error'));

    await expect(
      fetcher.fetchOne('https://example.com')
    ).rejects.toThrow('Failed to fetch');
    
    expect(mockPage.close).toHaveBeenCalled();
  });

  test('should fetch multiple URLs', async () => {
    const urls = [
      'https://example.com/page1',
      'https://example.com/page2'
    ];

    const results = await fetcher.fetchAll(urls);

    expect(results).toHaveLength(2);
    expect(results[0].url).toBe('https://example.com');
    expect(results[1].url).toBe('https://example.com');
    expect(mockPage.goto).toHaveBeenCalledTimes(2);
  });

  test('should continue fetching after error', async () => {
    const urls = [
      'https://example.com/page1',
      'https://example.com/page2',
      'https://example.com/page3'
    ];

    // Make second URL fail
    mockPage.goto
      .mockResolvedValueOnce(undefined)
      .mockRejectedValueOnce(new Error('Network error'))
      .mockResolvedValueOnce(undefined);

    const results = await fetcher.fetchAll(urls);

    // Should have 2 successful results (1st and 3rd)
    expect(results).toHaveLength(2);
    expect(mockPage.goto).toHaveBeenCalledTimes(3);
  });

  test('should update timeout', () => {
    fetcher.setTimeout(60000);
    expect(fetcher.timeout).toBe(60000);
  });
});
