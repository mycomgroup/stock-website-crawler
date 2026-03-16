import fc from 'fast-check';
import fs from 'fs';
import path from 'path';
import MarkdownGenerator from '../src/parsers/markdown-generator.js';

describe('MarkdownGenerator', () => {
  let generator;
  const testOutputDir = './test-output';

  beforeEach(() => {
    generator = new MarkdownGenerator();
  });

  afterEach(() => {
    // Clean up test output directory
    if (fs.existsSync(testOutputDir)) {
      fs.rmSync(testOutputDir, { recursive: true, force: true });
    }
  });

  describe('Property 16: Markdown生成格式正确性', () => {
    /**
     * Feature: stock-website-crawler, Property 16: Markdown生成格式正确性
     * **Validates: Requirements 6.1, 6.2, 6.3, 6.6**
     * 
     * For any PageData object, the generated Markdown should contain the title 
     * as a heading, all tables in Markdown table format, all code blocks in 
     * Markdown code block format, and the original URL
     */
    test('generated markdown contains all required elements', () => {
      fc.assert(
        fc.property(
          fc.record({
            url: fc.webUrl(),
            title: fc.string({ minLength: 1, maxLength: 100 }),
            briefDesc: fc.string({ minLength: 0, maxLength: 200 }),
            requestUrl: fc.option(fc.webUrl(), { nil: '' }),
            requestMethod: fc.option(fc.constantFrom('GET', 'POST', 'PUT', 'DELETE'), { nil: '' }),
            params: fc.array(
              fc.record({
                name: fc.string({ minLength: 1 }),
                required: fc.constantFrom('Yes', 'No'),
                type: fc.constantFrom('String', 'Number', 'Boolean', 'Array'),
                desc: fc.string({ minLength: 0, maxLength: 100 })
              }),
              { minLength: 0, maxLength: 3 }
            ),
            apiExamples: fc.array(
              fc.record({
                name: fc.string({ minLength: 1, maxLength: 50 }),
                code: fc.string({ minLength: 1, maxLength: 100 })
              }),
              { minLength: 0, maxLength: 2 }
            ),
            responseData: fc.record({
              description: fc.string({ minLength: 0, maxLength: 200 }),
              table: fc.array(
                fc.record({
                  name: fc.string({ minLength: 1 }),
                  type: fc.string({ minLength: 1 }),
                  desc: fc.string({ minLength: 0, maxLength: 100 })
                }),
                { minLength: 0, maxLength: 3 }
              )
            })
          }),
          (pageData) => {
            const markdown = generator.generate(pageData);

            // Should contain title as heading
            if (pageData.title) {
              expect(markdown).toContain(`# ${pageData.title}`);
            }

            // Should contain source URL
            if (pageData.url) {
              expect(markdown).toContain('## 源URL');
              expect(markdown).toContain(pageData.url);
            }

            // Should contain params table if params exist
            if (pageData.params && pageData.params.length > 0) {
              expect(markdown).toContain('## 参数');
              expect(markdown).toContain('---');
            }

            // Should contain API examples in code blocks
            pageData.apiExamples.forEach(example => {
              expect(markdown).toContain('```');
            });

            // Should contain response data table if exists
            if (pageData.responseData && pageData.responseData.table.length > 0) {
              expect(markdown).toContain('## 返回数据说明');
            }
          }
        ),
        { numRuns: 50 }
      );
    });
  });

  describe('Property 17: Markdown文件生成唯一性', () => {
    /**
     * Feature: stock-website-crawler, Property 17: Markdown文件生成唯一性
     * **Validates: Requirements 6.4**
     * 
     * For any PageData object, generating a Markdown file should create 
     * exactly one file with a unique filename based on the page title
     */
    test('each page generates a unique file', () => {
      fc.assert(
        fc.property(
          fc.array(
            fc.record({
              url: fc.webUrl(),
              title: fc.string({ minLength: 1, maxLength: 50 }),
              briefDesc: fc.string(),
              requestUrl: fc.string(),
              requestMethod: fc.string(),
              params: fc.array(fc.record({ name: fc.string(), required: fc.string(), type: fc.string(), desc: fc.string() })),
              apiExamples: fc.array(fc.record({ name: fc.string(), code: fc.string() })),
              responseData: fc.record({ description: fc.string(), table: fc.array(fc.record({ name: fc.string(), type: fc.string(), desc: fc.string() })) })
            }),
            { minLength: 1, maxLength: 3 }
          ),
          (pageDataArray) => {
            const filenames = new Set();

            pageDataArray.forEach(pageData => {
              const markdown = generator.generate(pageData);
              const filename = generator.safeFilename(pageData.title) + '.md';
              const filepath = generator.saveToFile(markdown, filename, testOutputDir);

              // File should exist
              expect(fs.existsSync(filepath)).toBe(true);

              // Track filenames
              filenames.add(filename);
            });

            // Each unique title should generate a unique filename
            const uniqueTitles = new Set(pageDataArray.map(p => p.title));
            expect(filenames.size).toBe(uniqueTitles.size);
          }
        ),
        { numRuns: 20 }
      );
    });
  });

  describe('Property 18: 文件名安全性', () => {
    /**
     * Feature: stock-website-crawler, Property 18: 文件名安全性
     * **Validates: Requirements 6.5**
     * 
     * For any string containing special characters, the safe filename function 
     * should return a string with all special characters replaced by underscores
     */
    test('special characters are replaced in filenames', () => {
      fc.assert(
        fc.property(
          fc.string({ minLength: 1, maxLength: 100 }),
          (title) => {
            const safeFilename = generator.safeFilename(title);

            // Should not contain filesystem-unsafe characters
            const unsafeChars = /[\/\\?*:|"<>]/;
            expect(safeFilename).not.toMatch(unsafeChars);

            // Should not be empty (unless input was all special chars)
            if (title.replace(/[\/\\?*:|"<>\s]/g, '').length > 0) {
              expect(safeFilename.length).toBeGreaterThan(0);
            }

            // Should not exceed max length
            expect(safeFilename.length).toBeLessThanOrEqual(200);
          }
        ),
        { numRuns: 100 }
      );
    });
  });

  describe('Unit Tests', () => {
    test('should generate markdown with title', () => {
      const pageData = {
        url: 'https://example.com',
        title: 'Test Page',
        briefDesc: 'Test description',
        requestUrl: 'https://api.example.com',
        requestMethod: 'POST',
        params: [],
        apiExamples: [],
        responseData: { description: '', table: [] }
      };

      const markdown = generator.generate(pageData);

      expect(markdown).toContain('# Test Page');
      expect(markdown).toContain('## 简要描述');
      expect(markdown).toContain('Test description');
    });

    test('should convert table to markdown format', () => {
      const table = {
        headers: ['Name', 'Age'],
        rows: [
          ['Alice', '30'],
          ['Bob', '25']
        ]
      };

      const markdown = generator.tableToMarkdown(table);

      expect(markdown).toContain('| Name | Age |');
      expect(markdown).toContain('| --- | --- |');
      expect(markdown).toContain('| Alice | 30 |');
      expect(markdown).toContain('| Bob | 25 |');
    });

    test('should handle empty table', () => {
      const table = {
        headers: [],
        rows: []
      };

      const markdown = generator.tableToMarkdown(table);
      expect(markdown).toBe('');
    });

    test('should escape pipe characters in table cells', () => {
      const table = {
        headers: ['Data'],
        rows: [['Value | with | pipes']]
      };

      const markdown = generator.tableToMarkdown(table);
      expect(markdown).toContain('Value \\| with \\| pipes');
    });

    test('should convert code block to markdown format', () => {
      const codeBlock = {
        language: 'javascript',
        code: 'console.log("Hello");'
      };

      const markdown = generator.codeBlockToMarkdown(codeBlock);

      expect(markdown).toBe('```javascript\nconsole.log("Hello");\n```');
    });

    test('should generate safe filename', () => {
      expect(generator.safeFilename('Test Page')).toBe('Test_Page');
      expect(generator.safeFilename('Test/Page')).toBe('Test_Page');
      expect(generator.safeFilename('Test:Page?')).toBe('Test_Page');
      expect(generator.safeFilename('Test|Page*')).toBe('Test_Page');
      expect(generator.safeFilename('')).toBe('untitled');
      expect(generator.safeFilename(null)).toBe('untitled');
    });


    test('should add H1 title when parser markdown has no heading', () => {
      const markdown = generator.normalizeMarkdownOutput('纯文本内容\n\n第二段', { title: '统一标题测试' });
      expect(markdown.startsWith('# 统一标题测试')).toBe(true);
      expect(markdown).toContain('纯文本内容');
    });

    test('should normalize extra blank lines in generated markdown', () => {
      const markdown = generator.normalizeMarkdownOutput('# 已有标题\n\n\n\n正文', { title: '空行标准化测试' });
      expect(markdown).toContain('# 已有标题');
      expect(markdown).not.toContain('\n\n\n');
    });
    test('should save markdown to file', () => {
      const content = '# Test\n\nContent';
      const filename = 'test.md';

      const filepath = generator.saveToFile(content, filename, testOutputDir);

      expect(fs.existsSync(filepath)).toBe(true);
      const savedContent = fs.readFileSync(filepath, 'utf-8');
      expect(savedContent).toBe(content);
    });

    test('should create output directory if not exists', () => {
      const content = '# Test';
      const filename = 'test.md';
      const newDir = path.join(testOutputDir, 'subdir');

      generator.saveToFile(content, filename, newDir);

      expect(fs.existsSync(newDir)).toBe(true);
    });

    test('should handle newlines in table cells', () => {
      const table = {
        headers: ['Data'],
        rows: [['Line1\nLine2']]
      };

      const markdown = generator.tableToMarkdown(table);
      expect(markdown).toContain('Line1<br>Line2');
    });
  });
});
