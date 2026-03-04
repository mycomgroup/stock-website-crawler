/**
 * Link Finder测试
 * 包含Property-Based Tests和Unit Tests
 */

import fc from 'fast-check';
import { chromium } from 'playwright';
import LinkFinder from '../src/link-finder.js';

describe('Link Finder', () => {
  let browser;
  let page;
  let linkFinder;
  
  beforeAll(async () => {
    browser = await chromium.launch();
  });
  
  afterAll(async () => {
    await browser.close();
  });
  
  beforeEach(async () => {
    page = await browser.newPage();
    linkFinder = new LinkFinder();
  });
  
  afterEach(async () => {
    await page.close();
  });
  
  // ========== Property-Based Tests ==========
  
  describe('Property 11: 链接提取完整性', () => {
    /**
     * **Validates: Requirements 4.1**
     * 
     * Property: For any HTML page and URL rules, all extracted links
     * should be valid absolute URLs that match the URL rules
     */
    test('extracted links are valid absolute URLs matching rules', async () => {
      await fc.assert(
        fc.asyncProperty(
          // 生成链接数组
          fc.array(
            fc.record({
              href: fc.webUrl(),
              text: fc.string({ minLength: 1, maxLength: 20 })
            }),
            { minLength: 0, maxLength: 10 }
          ),
          // 生成URL规则
          fc.record({
            include: fc.array(fc.string(), { minLength: 0, maxLength: 3 }),
            exclude: fc.array(fc.string(), { minLength: 0, maxLength: 3 })
          }),
          async (links, urlRules) => {
            // 生成HTML页面
            const html = `
              <!DOCTYPE html>
              <html>
                <head><title>Test Page</title></head>
                <body>
                  ${links.map(link => `<a href="${link.href}">${link.text}</a>`).join('\n')}
                </body>
              </html>
            `;
            
            // 加载HTML
            await page.setContent(html);
            
            // 提取链接
            const extractedLinks = await linkFinder.extractLinks(page, urlRules);
            
            // 验证所有提取的链接都是绝对URL
            for (const link of extractedLinks) {
              expect(
                link.startsWith('http://') || link.startsWith('https://')
              ).toBe(true);
            }
            
            // 验证所有提取的链接都符合规则
            for (const link of extractedLinks) {
              // 如果有include规则，必须至少匹配一个
              if (urlRules.include.length > 0) {
                const matchesInclude = urlRules.include.some(pattern => {
                  try {
                    return new RegExp(pattern).test(link);
                  } catch {
                    return false;
                  }
                });
                expect(matchesInclude).toBe(true);
              }
              
              // 不能匹配任何exclude规则
              for (const pattern of urlRules.exclude) {
                try {
                  const regex = new RegExp(pattern);
                  expect(regex.test(link)).toBe(false);
                } catch {
                  // 无效的正则表达式，跳过
                }
              }
            }
            
            return true;
          }
        ),
        { numRuns: 100 }
      );
    });
    
    test('extracted links are derived from page links', async () => {
      await fc.assert(
        fc.asyncProperty(
          fc.array(fc.webUrl(), { minLength: 0, maxLength: 10 }),
          fc.record({
            include: fc.array(fc.string(), { minLength: 0, maxLength: 3 }),
            exclude: fc.array(fc.string(), { minLength: 0, maxLength: 3 })
          }),
          async (urls, urlRules) => {
            // 生成HTML页面
            const html = `
              <!DOCTYPE html>
              <html>
                <head><title>Test Page</title></head>
                <body>
                  ${urls.map(url => `<a href="${url}">Link</a>`).join('\n')}
                </body>
              </html>
            `;
            
            await page.setContent(html);
            
            const extractedLinks = await linkFinder.extractLinks(page, urlRules);
            
            // 提取的链接数量不应超过页面中的链接数量
            expect(extractedLinks.length).toBeLessThanOrEqual(urls.length);
            
            // 所有提取的链接都应该是有效的绝对URL
            for (const link of extractedLinks) {
              expect(
                link.startsWith('http://') || link.startsWith('https://')
              ).toBe(true);
            }
            
            return true;
          }
        ),
        { numRuns: 100 }
      );
    });
  });
  
  // ========== Unit Tests ==========
  
  describe('extractLinks', () => {
    test('returns empty array for empty page', async () => {
      const html = `
        <!DOCTYPE html>
        <html>
          <head><title>Empty Page</title></head>
          <body></body>
        </html>
      `;
      
      await page.setContent(html);
      const links = await linkFinder.extractLinks(page, {});
      
      expect(links).toEqual([]);
    });
    
    test('returns empty array for page with no links', async () => {
      const html = `
        <!DOCTYPE html>
        <html>
          <head><title>No Links</title></head>
          <body>
            <p>This page has no links</p>
            <div>Just some text</div>
          </body>
        </html>
      `;
      
      await page.setContent(html);
      const links = await linkFinder.extractLinks(page, {});
      
      expect(links).toEqual([]);
    });
    
    test('extracts absolute URLs', async () => {
      const html = `
        <!DOCTYPE html>
        <html>
          <head><title>Test Page</title></head>
          <body>
            <a href="https://example.com/page1">Link 1</a>
            <a href="https://example.com/page2">Link 2</a>
          </body>
        </html>
      `;
      
      await page.setContent(html);
      const links = await linkFinder.extractLinks(page, {});
      
      expect(links).toHaveLength(2);
      expect(links).toContain('https://example.com/page1');
      expect(links).toContain('https://example.com/page2');
    });
    
    test('converts relative URLs to absolute', async () => {
      const html = `
        <!DOCTYPE html>
        <html>
          <head>
            <base href="https://example.com/path/page.html">
            <title>Test Page</title>
          </head>
          <body>
            <a href="./other.html">Relative Link</a>
            <a href="/absolute/path.html">Absolute Path</a>
          </body>
        </html>
      `;
      
      await page.setContent(html, { url: 'https://example.com/path/page.html' });
      const links = await linkFinder.extractLinks(page, {});
      
      expect(links.length).toBeGreaterThan(0);
      // 所有链接都应该是绝对URL
      for (const link of links) {
        expect(
          link.startsWith('http://') || link.startsWith('https://')
        ).toBe(true);
      }
    });
    
    test('filters links by include pattern', async () => {
      const html = `
        <!DOCTYPE html>
        <html>
          <head><title>Test Page</title></head>
          <body>
            <a href="https://example.com/api/v1">API Link</a>
            <a href="https://example.com/page">Page Link</a>
            <a href="https://example.com/api/v2">API Link 2</a>
          </body>
        </html>
      `;
      
      await page.setContent(html);
      const links = await linkFinder.extractLinks(page, {
        include: ['.*api.*']
      });
      
      expect(links).toHaveLength(2);
      expect(links).toContain('https://example.com/api/v1');
      expect(links).toContain('https://example.com/api/v2');
    });
    
    test('filters links by exclude pattern', async () => {
      const html = `
        <!DOCTYPE html>
        <html>
          <head><title>Test Page</title></head>
          <body>
            <a href="https://example.com/login">Login</a>
            <a href="https://example.com/page1">Page 1</a>
            <a href="https://example.com/page2">Page 2</a>
          </body>
        </html>
      `;
      
      await page.setContent(html);
      const links = await linkFinder.extractLinks(page, {
        exclude: ['.*login.*']
      });
      
      expect(links).toHaveLength(2);
      expect(links).not.toContain('https://example.com/login');
    });
    

    test('supports prioritized patterns for API docs', async () => {
      const html = `
        <!DOCTYPE html>
        <html>
          <head><title>Priority Link Test</title></head>
          <body>
            <a href="https://example.com/open/api/doc?api-key=stock/list">API Doc</a>
            <a href="https://example.com/open/api/doc?api-key=undefined">Invalid API Doc</a>
            <a href="https://example.com/page">Normal Page</a>
          </body>
        </html>
      `;

      await page.setContent(html);
      const links = await linkFinder.extractLinks(
        page,
        { include: ['.*example\.com.*'] },
        {
          prioritizedPatterns: [
            {
              selector: 'a[href*="api-key="]',
              requiredQueryParams: ['api-key'],
              pathIncludes: ['/open/api/doc']
            }
          ]
        }
      );

      expect(links).toEqual(['https://example.com/open/api/doc?api-key=stock/list']);
    });

    test('falls back to generic links when no prioritized match', async () => {
      const html = `
        <!DOCTYPE html>
        <html>
          <head><title>Fallback Link Test</title></head>
          <body>
            <a href="https://example.com/page1">Page 1</a>
            <a href="https://example.com/page2">Page 2</a>
          </body>
        </html>
      `;

      await page.setContent(html);
      const links = await linkFinder.extractLinks(
        page,
        { include: ['.*example\.com.*'] },
        {
          prioritizedPatterns: [
            {
              selector: 'a[href*="api-key="]',
              requiredQueryParams: ['api-key'],
              pathIncludes: ['/open/api/doc']
            }
          ]
        }
      );

      expect(links).toHaveLength(2);
      expect(links).toContain('https://example.com/page1');
      expect(links).toContain('https://example.com/page2');
    });
    test('removes duplicate links', async () => {
      const html = `
        <!DOCTYPE html>
        <html>
          <head><title>Test Page</title></head>
          <body>
            <a href="https://example.com/page">Link 1</a>
            <a href="https://example.com/page">Link 2</a>
            <a href="https://example.com/page">Link 3</a>
          </body>
        </html>
      `;
      
      await page.setContent(html);
      const links = await linkFinder.extractLinks(page, {});
      
      expect(links).toHaveLength(1);
      expect(links).toContain('https://example.com/page');
    });
  });
  
  describe('expandCollapsibles', () => {
    test('expands details elements', async () => {
      const html = `
        <!DOCTYPE html>
        <html>
          <head><title>Test Page</title></head>
          <body>
            <details>
              <summary>Click to expand</summary>
              <p>Hidden content</p>
            </details>
          </body>
        </html>
      `;
      
      await page.setContent(html);
      await linkFinder.expandCollapsibles(page);
      
      const isOpen = await page.evaluate(() => {
        const details = document.querySelector('details');
        return details.open;
      });
      
      expect(isOpen).toBe(true);
    });
    
    test('handles pages without collapsibles', async () => {
      const html = `
        <!DOCTYPE html>
        <html>
          <head><title>Test Page</title></head>
          <body>
            <p>No collapsible content</p>
          </body>
        </html>
      `;
      
      await page.setContent(html);
      
      // Should not throw error
      await expect(linkFinder.expandCollapsibles(page)).resolves.not.toThrow();
    });
  });
});
