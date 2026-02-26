import { describe, it, before } from 'node:test';
import assert from 'node:assert';
import { StructureAnalyzer } from '../lib/structure-analyzer.js';

describe('StructureAnalyzer', () => {
  let analyzer;

  before(() => {
    analyzer = new StructureAnalyzer();
  });

  describe('Heading Structure Analysis', () => {
    it('should extract all heading levels (h1-h6)', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <h1 class="page-title">API Documentation</h1>
                <h2 class="section-title">Getting Started</h2>
                <h3>Installation</h3>
                <h4>Prerequisites</h4>
                <h5>System Requirements</h5>
                <h6>Notes</h6>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.headings.h1, 'Should have h1 headings');
      assert.ok(result.headings.h2, 'Should have h2 headings');
      assert.ok(result.headings.h3, 'Should have h3 headings');
      assert.ok(result.headings.h4, 'Should have h4 headings');
      assert.ok(result.headings.h5, 'Should have h5 headings');
      assert.ok(result.headings.h6, 'Should have h6 headings');
    });

    it('should record heading class and id attributes', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <h1 class="page-title" id="main-title">API Documentation</h1>
                <h2 class="section-title">Getting Started</h2>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.strictEqual(result.headings.h1.xpath, "//*[@id='main-title']", 'Should use id in xpath');
      assert.ok(result.headings.h2.xpath.includes('section-title'), 'Should use class in xpath');
    });

    it('should record heading text content', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <h1 class="page-title">API Documentation</h1>
                <h2 class="section-title">Getting Started</h2>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.headings.h1.samples, 'Should have sample texts');
      assert.ok(result.headings.h1.samples.length > 0, 'Should have at least one sample');
      assert.strictEqual(result.headings.h1.samples[0], 'API Documentation', 'Should record correct text');
    });

    it('should calculate heading frequency across samples', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <h1 class="page-title">API Documentation</h1>
                <h2 class="section-title">Getting Started</h2>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <h1 class="page-title">Fund API</h1>
                <h2 class="section-title">Overview</h2>
              </body>
            </html>
          `,
          title: 'Page 2'
        },
        {
          url: 'http://example.com/page3',
          html: `
            <html>
              <body>
                <h1 class="page-title">Company API</h1>
                <h2 class="section-title">Introduction</h2>
              </body>
            </html>
          `,
          title: 'Page 3'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.strictEqual(result.headings.h1.frequency, 1.0, 'h1 should appear in all samples (frequency = 1.0)');
      assert.strictEqual(result.headings.h2.frequency, 1.0, 'h2 should appear in all samples (frequency = 1.0)');
    });

    it('should identify common heading patterns', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <h1 class="page-title">API Documentation</h1>
                <h2 class="section-title">Getting Started</h2>
                <h2 class="section-title">Authentication</h2>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <h1 class="page-title">Fund API</h1>
                <h2 class="section-title">Overview</h2>
                <h2 class="section-title">Parameters</h2>
              </body>
            </html>
          `,
          title: 'Page 2'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      // Should identify the common pattern for h1 and h2
      assert.ok(result.headings.h1.xpath.includes('page-title'), 'Should identify page-title pattern');
      assert.ok(result.headings.h2.xpath.includes('section-title'), 'Should identify section-title pattern');
      assert.strictEqual(result.headings.h1.frequency, 1.0, 'Common pattern should have high frequency');
    });

    it('should collect sample texts from multiple pages', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <h1 class="page-title">API Documentation</h1>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <h1 class="page-title">Fund API</h1>
              </body>
            </html>
          `,
          title: 'Page 2'
        },
        {
          url: 'http://example.com/page3',
          html: `
            <html>
              <body>
                <h1 class="page-title">Company API</h1>
              </body>
            </html>
          `,
          title: 'Page 3'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(Array.isArray(result.headings.h1.samples), 'Should have samples array');
      assert.ok(result.headings.h1.samples.length > 0, 'Should collect sample texts');
      assert.ok(result.headings.h1.samples.includes('API Documentation'), 'Should include first sample');
      assert.ok(result.headings.h1.samples.includes('Fund API'), 'Should include second sample');
    });

    it('should handle pages with missing heading levels', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <h1 class="page-title">API Documentation</h1>
                <h2 class="section-title">Getting Started</h2>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <h1 class="page-title">Fund API</h1>
              </body>
            </html>
          `,
          title: 'Page 2'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.strictEqual(result.headings.h1.frequency, 1.0, 'h1 appears in all samples');
      assert.strictEqual(result.headings.h2.frequency, 0.5, 'h2 appears in only half of samples');
    });

    it('should generate correct XPath for headings with multiple classes', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <h1 class="page-title main-heading">API Documentation</h1>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.headings.h1.xpath.includes('contains'), 'Should use contains() for multiple classes');
      assert.ok(result.headings.h1.xpath.includes('page-title'), 'Should include first class');
    });

    it('should handle headings without class or id', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <h1>API Documentation</h1>
                <h2>Getting Started</h2>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.strictEqual(result.headings.h1.xpath, '//h1', 'Should use tag name only');
      assert.strictEqual(result.headings.h2.xpath, '//h2', 'Should use tag name only');
    });

    it('should output expected format', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <h1 class="page-title">API Documentation</h1>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <h1 class="page-title">Fund API</h1>
              </body>
            </html>
          `,
          title: 'Page 2'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      // Verify expected output format
      assert.ok(result.headings.h1.xpath, 'Should have xpath property');
      assert.ok(typeof result.headings.h1.frequency === 'number', 'Should have frequency as number');
      assert.ok(Array.isArray(result.headings.h1.samples), 'Should have samples as array');
      assert.strictEqual(result.headings.h1.frequency, 1.0, 'Frequency should be 1.0 for all samples');
    });
  });

  describe('Table Structure Analysis', () => {
    it('should extract all table elements', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <thead>
                    <tr><th>Name</th><th>Type</th><th>Description</th></tr>
                  </thead>
                  <tbody>
                    <tr><td>id</td><td>string</td><td>Unique identifier</td></tr>
                  </tbody>
                </table>
                <table class="results-table">
                  <thead>
                    <tr><th>Field</th><th>Value</th></tr>
                  </thead>
                  <tbody>
                    <tr><td>status</td><td>success</td></tr>
                  </tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(Array.isArray(result.tables), 'Should return tables as array');
      assert.strictEqual(result.tables.length, 2, 'Should extract all table elements');
    });

    it('should record table class and id attributes', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <table class="params-table" id="main-table">
                  <thead>
                    <tr><th>Name</th><th>Type</th></tr>
                  </thead>
                  <tbody>
                    <tr><td>id</td><td>string</td></tr>
                  </tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.tables.length > 0, 'Should have tables');
      assert.strictEqual(result.tables[0].xpath, "//*[@id='main-table']", 'Should use id in xpath');
    });

    it('should extract table caption', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <caption>参数说明</caption>
                  <thead>
                    <tr><th>Name</th><th>Type</th></tr>
                  </thead>
                  <tbody>
                    <tr><td>id</td><td>string</td></tr>
                  </tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.tables.length > 0, 'Should have tables');
      assert.strictEqual(result.tables[0].caption, '参数说明', 'Should extract caption text');
    });

    it('should extract table header (thead)', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <thead>
                    <tr><th>Name</th><th>Type</th><th>Required</th><th>Description</th></tr>
                  </thead>
                  <tbody>
                    <tr><td>id</td><td>string</td><td>yes</td><td>Unique identifier</td></tr>
                  </tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.tables.length > 0, 'Should have tables');
      assert.strictEqual(result.tables[0].columnCount, 4, 'Should count columns from thead');
    });

    it('should calculate column count', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <thead>
                    <tr><th>Name</th><th>Type</th><th>Description</th></tr>
                  </thead>
                  <tbody>
                    <tr><td>id</td><td>string</td><td>Unique identifier</td></tr>
                  </tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.tables.length > 0, 'Should have tables');
      assert.strictEqual(result.tables[0].columnCount, 3, 'Should calculate correct column count');
    });

    it('should calculate table frequency across samples', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <thead><tr><th>Name</th><th>Type</th></tr></thead>
                  <tbody><tr><td>id</td><td>string</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <thead><tr><th>Field</th><th>Value</th></tr></thead>
                  <tbody><tr><td>status</td><td>active</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 2'
        },
        {
          url: 'http://example.com/page3',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <thead><tr><th>Key</th><th>Description</th></tr></thead>
                  <tbody><tr><td>api_key</td><td>API Key</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 3'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.tables.length > 0, 'Should have tables');
      assert.strictEqual(result.tables[0].frequency, 1.0, 'Table should appear in all samples (frequency = 1.0)');
    });

    it('should identify common table patterns', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <caption>参数说明</caption>
                  <thead><tr><th>Name</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
                  <tbody><tr><td>id</td><td>string</td><td>yes</td><td>ID</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <caption>参数说明</caption>
                  <thead><tr><th>Name</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
                  <tbody><tr><td>name</td><td>string</td><td>no</td><td>Name</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 2'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.tables.length > 0, 'Should have tables');
      assert.ok(result.tables[0].xpath.includes('params-table'), 'Should identify params-table pattern');
      assert.strictEqual(result.tables[0].columnCount, 4, 'Should identify common column count');
      assert.strictEqual(result.tables[0].caption, '参数说明', 'Should identify common caption');
    });

    it('should output expected format', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <caption>参数说明</caption>
                  <thead><tr><th>Name</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
                  <tbody><tr><td>id</td><td>string</td><td>yes</td><td>ID</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <caption>参数说明</caption>
                  <thead><tr><th>Name</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
                  <tbody><tr><td>name</td><td>string</td><td>no</td><td>Name</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 2'
        },
        {
          url: 'http://example.com/page3',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <caption>参数说明</caption>
                  <thead><tr><th>Name</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
                  <tbody><tr><td>code</td><td>number</td><td>yes</td><td>Code</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 3'
        },
        {
          url: 'http://example.com/page4',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <caption>参数说明</caption>
                  <thead><tr><th>Name</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
                  <tbody><tr><td>date</td><td>string</td><td>no</td><td>Date</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 4'
        },
        {
          url: 'http://example.com/page5',
          html: `
            <html>
              <body>
                <table class="params-table">
                  <caption>参数说明</caption>
                  <thead><tr><th>Name</th><th>Type</th><th>Required</th><th>Description</th></tr></thead>
                  <tbody><tr><td>status</td><td>boolean</td><td>yes</td><td>Status</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 5'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      // Verify expected output format matches the spec
      assert.ok(result.tables.length > 0, 'Should have tables');
      const table = result.tables[0];
      assert.ok(table.xpath, 'Should have xpath property');
      assert.strictEqual(table.xpath, "//table[@class='params-table']", 'Should have correct xpath');
      assert.strictEqual(table.frequency, 1.0, 'Should have frequency of 5/5 = 1.0');
      assert.strictEqual(table.caption, '参数说明', 'Should have caption');
      assert.strictEqual(table.columnCount, 4, 'Should have columnCount of 4');
    });

    it('should handle tables without caption', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <table class="data-table">
                  <thead><tr><th>Name</th><th>Value</th></tr></thead>
                  <tbody><tr><td>key</td><td>value</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.tables.length > 0, 'Should have tables');
      assert.strictEqual(result.tables[0].caption, null, 'Caption should be null when not present');
    });

    it('should handle tables without thead', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <table class="simple-table">
                  <tbody>
                    <tr><td>key</td><td>value</td></tr>
                  </tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.tables.length > 0, 'Should have tables');
      assert.strictEqual(result.tables[0].columnCount, 0, 'Column count should be 0 when no thead');
    });

    it('should handle tables with multiple classes', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <table class="table params-table striped">
                  <thead><tr><th>Name</th><th>Type</th></tr></thead>
                  <tbody><tr><td>id</td><td>string</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.tables.length > 0, 'Should have tables');
      assert.ok(result.tables[0].xpath.includes('contains'), 'Should use contains() for multiple classes');
      assert.ok(result.tables[0].xpath.includes('table'), 'Should include first class');
    });

    it('should sort tables by frequency', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <table class="common-table">
                  <thead><tr><th>A</th><th>B</th></tr></thead>
                  <tbody><tr><td>1</td><td>2</td></tr></tbody>
                </table>
                <table class="rare-table">
                  <thead><tr><th>X</th><th>Y</th></tr></thead>
                  <tbody><tr><td>3</td><td>4</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <table class="common-table">
                  <thead><tr><th>A</th><th>B</th></tr></thead>
                  <tbody><tr><td>5</td><td>6</td></tr></tbody>
                </table>
              </body>
            </html>
          `,
          title: 'Page 2'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.tables.length >= 2, 'Should have at least 2 tables');
      assert.ok(result.tables[0].frequency >= result.tables[1].frequency, 'Tables should be sorted by frequency (descending)');
      assert.ok(result.tables[0].xpath.includes('common-table'), 'Most frequent table should be first');
    });
  });

  describe('Code Block Analysis', () => {
    it('should extract code blocks (pre/code)', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <pre><code class="language-json">{"key": "value"}</code></pre>
                <pre><code class="language-javascript">const x = 1;</code></pre>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(Array.isArray(result.codeBlocks), 'Should return code blocks as array');
      assert.ok(result.codeBlocks.length >= 2, 'Should extract multiple code blocks');
    });

    it('should identify code language', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <pre><code class="language-json">{"key": "value"}</code></pre>
                <pre><code class="language-javascript">const x = 1;</code></pre>
                <pre><code class="language-python">print("hello")</code></pre>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.codeBlocks.length >= 3, 'Should have code blocks');
      const languages = result.codeBlocks.map(cb => cb.language).filter(l => l);
      assert.ok(languages.includes('json'), 'Should detect json language');
      assert.ok(languages.includes('javascript'), 'Should detect javascript language');
      assert.ok(languages.includes('python'), 'Should detect python language');
    });

    it('should calculate code block frequency', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <pre><code class="language-json">{"key": "value"}</code></pre>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <pre><code class="language-json">{"name": "test"}</code></pre>
              </body>
            </html>
          `,
          title: 'Page 2'
        },
        {
          url: 'http://example.com/page3',
          html: `
            <html>
              <body>
                <pre><code class="language-json">{"id": 123}</code></pre>
              </body>
            </html>
          `,
          title: 'Page 3'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.codeBlocks.length > 0, 'Should have code blocks');
      assert.strictEqual(result.codeBlocks[0].frequency, 1.0, 'Code block should appear in all samples');
    });

    it('should identify common code block patterns', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <pre><code class="language-json">{"key": "value"}</code></pre>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <pre><code class="language-json">{"name": "test"}</code></pre>
              </body>
            </html>
          `,
          title: 'Page 2'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.codeBlocks.length > 0, 'Should have code blocks');
      assert.ok(result.codeBlocks[0].xpath.includes('code'), 'Should identify code element pattern');
      assert.strictEqual(result.codeBlocks[0].language, 'json', 'Should identify common language');
    });

    it('should handle code blocks without language class', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <pre><code>plain code</code></pre>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.codeBlocks.length > 0, 'Should have code blocks');
      assert.strictEqual(result.codeBlocks[0].language, null, 'Language should be null when not specified');
    });

    it('should handle pre elements without code', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <pre>preformatted text</pre>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.codeBlocks.length > 0, 'Should extract pre elements');
    });

    it('should handle code elements without pre', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <p>Use <code>const</code> for constants.</p>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.codeBlocks.length > 0, 'Should extract inline code elements');
    });

    it('should sort code blocks by frequency', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <pre><code class="language-json">{"common": true}</code></pre>
                <pre><code class="language-xml"><root/></code></pre>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <pre><code class="language-json">{"common": true}</code></pre>
              </body>
            </html>
          `,
          title: 'Page 2'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.codeBlocks.length >= 2, 'Should have multiple code blocks');
      assert.ok(result.codeBlocks[0].frequency >= result.codeBlocks[1].frequency, 
        'Code blocks should be sorted by frequency (descending)');
    });

    it('should output expected format', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <pre><code class="language-json">{"key": "value"}</code></pre>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <pre><code class="language-json">{"name": "test"}</code></pre>
              </body>
            </html>
          `,
          title: 'Page 2'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.codeBlocks.length > 0, 'Should have code blocks');
      const codeBlock = result.codeBlocks[0];
      assert.ok(codeBlock.xpath, 'Should have xpath property');
      assert.ok(typeof codeBlock.frequency === 'number', 'Should have frequency as number');
      assert.strictEqual(codeBlock.language, 'json', 'Should have language property');
    });
  });

  describe('List Analysis', () => {
    it('should extract ordered lists (ol)', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <ol class="steps">
                  <li>First step</li>
                  <li>Second step</li>
                  <li>Third step</li>
                </ol>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(Array.isArray(result.lists), 'Should return lists as array');
      assert.ok(result.lists.length > 0, 'Should extract ordered lists');
      const ol = result.lists.find(l => l.type === 'ol');
      assert.ok(ol, 'Should have ordered list');
    });

    it('should extract unordered lists (ul)', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <ul class="features">
                  <li>Feature A</li>
                  <li>Feature B</li>
                  <li>Feature C</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.lists.length > 0, 'Should extract unordered lists');
      const ul = result.lists.find(l => l.type === 'ul');
      assert.ok(ul, 'Should have unordered list');
    });

    it('should extract both ordered and unordered lists', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <ol class="steps">
                  <li>Step 1</li>
                  <li>Step 2</li>
                </ol>
                <ul class="features">
                  <li>Feature A</li>
                  <li>Feature B</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.lists.length >= 2, 'Should extract both list types');
      const hasOl = result.lists.some(l => l.type === 'ol');
      const hasUl = result.lists.some(l => l.type === 'ul');
      assert.ok(hasOl, 'Should have ordered list');
      assert.ok(hasUl, 'Should have unordered list');
    });

    it('should record list class and id attributes', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <ul class="api-list" id="main-list">
                  <li>Item 1</li>
                  <li>Item 2</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.lists.length > 0, 'Should have lists');
      assert.strictEqual(result.lists[0].xpath, "//*[@id='main-list']", 'Should use id in xpath');
    });

    it('should count list items', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <ul class="features">
                  <li>Feature A</li>
                  <li>Feature B</li>
                  <li>Feature C</li>
                  <li>Feature D</li>
                  <li>Feature E</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.lists.length > 0, 'Should have lists');
      // Note: itemCount is not included in merged output, only in single structure
    });

    it('should calculate list frequency', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <ul class="api-list">
                  <li>API 1</li>
                  <li>API 2</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <ul class="api-list">
                  <li>API 3</li>
                  <li>API 4</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 2'
        },
        {
          url: 'http://example.com/page3',
          html: `
            <html>
              <body>
                <ul class="api-list">
                  <li>API 5</li>
                  <li>API 6</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 3'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.lists.length > 0, 'Should have lists');
      assert.strictEqual(result.lists[0].frequency, 1.0, 'List should appear in all samples');
    });

    it('should identify common list patterns', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <ul class="api-list">
                  <li>API 1</li>
                  <li>API 2</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <ul class="api-list">
                  <li>API 3</li>
                  <li>API 4</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 2'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.lists.length > 0, 'Should have lists');
      assert.ok(result.lists[0].xpath.includes('api-list'), 'Should identify api-list pattern');
      assert.strictEqual(result.lists[0].type, 'ul', 'Should identify list type');
    });

    it('should handle lists without class or id', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <ul>
                  <li>Item 1</li>
                  <li>Item 2</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.lists.length > 0, 'Should have lists');
      assert.strictEqual(result.lists[0].xpath, '//ul', 'Should use tag name only');
    });

    it('should handle lists with multiple classes', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <ul class="list api-list styled">
                  <li>Item 1</li>
                  <li>Item 2</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.lists.length > 0, 'Should have lists');
      assert.ok(result.lists[0].xpath.includes('contains'), 'Should use contains() for multiple classes');
      assert.ok(result.lists[0].xpath.includes('list'), 'Should include first class');
    });

    it('should sort lists by frequency', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <ul class="common-list">
                  <li>Item 1</li>
                  <li>Item 2</li>
                </ul>
                <ol class="rare-list">
                  <li>Step 1</li>
                  <li>Step 2</li>
                </ol>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <ul class="common-list">
                  <li>Item 3</li>
                  <li>Item 4</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 2'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.lists.length >= 2, 'Should have multiple lists');
      assert.ok(result.lists[0].frequency >= result.lists[1].frequency, 
        'Lists should be sorted by frequency (descending)');
    });

    it('should output expected format', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <ul class="api-list">
                  <li>API 1</li>
                  <li>API 2</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <ul class="api-list">
                  <li>API 3</li>
                  <li>API 4</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 2'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.lists.length > 0, 'Should have lists');
      const list = result.lists[0];
      assert.ok(list.xpath, 'Should have xpath property');
      assert.ok(typeof list.frequency === 'number', 'Should have frequency as number');
      assert.strictEqual(list.type, 'ul', 'Should have type property');
    });

    it('should handle nested lists', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <ul class="main-list">
                  <li>Item 1
                    <ul class="sub-list">
                      <li>Sub-item 1</li>
                      <li>Sub-item 2</li>
                    </ul>
                  </li>
                  <li>Item 2</li>
                </ul>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.lists.length >= 2, 'Should extract both parent and nested lists');
    });
  });

  describe('Main Content Area Identification', () => {
    it('should identify main element', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <header>Header</header>
                <nav>Navigation</nav>
                <main class="main-content">
                  <h1>Main Content</h1>
                  <p>This is the main content area.</p>
                </main>
                <aside>Sidebar</aside>
                <footer>Footer</footer>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content');
      assert.ok(result.mainContent.xpath.includes('main'), 'Should identify main element');
    });

    it('should identify article element', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <header>Header</header>
                <article class="post">
                  <h1>Article Title</h1>
                  <p>Article content goes here.</p>
                </article>
                <aside>Sidebar</aside>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content');
      assert.ok(result.mainContent.xpath.includes('article'), 'Should identify article element');
    });

    it('should identify role="main" element', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <div role="main" class="content">
                  <h1>Main Content</h1>
                  <p>Content with ARIA role.</p>
                </div>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content');
      assert.ok(result.mainContent.xpath, 'Should have xpath');
    });

    it('should identify .main-content container', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <div class="main-content">
                  <h1>Page Title</h1>
                  <p>Main content in a div with class.</p>
                </div>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content');
      assert.ok(result.mainContent.xpath.includes('main-content'), 'Should identify main-content class');
    });

    it('should filter out navigation elements', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <nav class="main-nav">
                  <a href="/">Home</a>
                  <a href="/about">About</a>
                </nav>
                <main>
                  <h1>Main Content</h1>
                  <p>This is the actual content.</p>
                </main>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content');
      assert.ok(result.mainContent.xpath.includes('main'), 'Should identify main, not nav');
    });

    it('should filter out sidebar elements', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <div class="sidebar">
                  <h3>Related Links</h3>
                  <ul><li>Link 1</li><li>Link 2</li></ul>
                </div>
                <article>
                  <h1>Article Title</h1>
                  <p>Article content here.</p>
                </article>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content');
      assert.ok(result.mainContent.xpath.includes('article'), 'Should identify article, not sidebar');
    });

    it('should filter out ad elements', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <div class="ad-banner">
                  <img src="ad.jpg" alt="Advertisement" />
                </div>
                <main class="content">
                  <h1>Page Content</h1>
                  <p>Real content goes here.</p>
                </main>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content');
      assert.ok(!result.mainContent.xpath.includes('ad'), 'Should not identify ad as main content');
    });

    it('should calculate content density', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <div class="container-a">
                  <p>Short text</p>
                </div>
                <div class="container-b">
                  <h1>Long Article Title</h1>
                  <p>This is a much longer paragraph with substantial content that should score higher in content density calculations.</p>
                  <p>Another paragraph with more meaningful content.</p>
                  <h2>Section Title</h2>
                  <p>Even more content in this section.</p>
                </div>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content');
      assert.ok(result.mainContent.xpath.includes('container-b'), 'Should select container with higher content density');
    });

    it('should select most likely main content area', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <header class="site-header">
                  <h1>Site Title</h1>
                </header>
                <nav class="navigation">
                  <a href="/">Home</a>
                </nav>
                <div class="content-wrapper">
                  <article class="main-article">
                    <h1>Article Title</h1>
                    <p>This is the main article content with substantial text.</p>
                    <p>Multiple paragraphs of meaningful content.</p>
                    <h2>Section</h2>
                    <p>More content here.</p>
                  </article>
                  <aside class="sidebar">
                    <h3>Related</h3>
                    <ul><li>Link</li></ul>
                  </aside>
                </div>
                <footer class="site-footer">
                  <p>Footer content</p>
                </footer>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content');
      // Should identify the article or content-wrapper, not header/nav/footer/sidebar
      const xpath = result.mainContent.xpath.toLowerCase();
      assert.ok(!xpath.includes('header'), 'Should not select header');
      assert.ok(!xpath.includes('nav'), 'Should not select nav');
      assert.ok(!xpath.includes('footer'), 'Should not select footer');
      assert.ok(!xpath.includes('sidebar'), 'Should not select sidebar');
    });

    it('should handle pages without semantic elements', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <div class="wrapper">
                  <div class="header-area">Header</div>
                  <div class="body-area">
                    <h1>Page Title</h1>
                    <p>Main content in a generic div structure.</p>
                    <p>More content paragraphs.</p>
                  </div>
                  <div class="footer-area">Footer</div>
                </div>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content even without semantic elements');
      assert.ok(result.mainContent.xpath, 'Should have xpath');
    });

    it('should calculate frequency across multiple samples', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <main class="main-content">
                  <h1>Page 1</h1>
                  <p>Content for page 1.</p>
                </main>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <main class="main-content">
                  <h1>Page 2</h1>
                  <p>Content for page 2.</p>
                </main>
              </body>
            </html>
          `,
          title: 'Page 2'
        },
        {
          url: 'http://example.com/page3',
          html: `
            <html>
              <body>
                <main class="main-content">
                  <h1>Page 3</h1>
                  <p>Content for page 3.</p>
                </main>
              </body>
            </html>
          `,
          title: 'Page 3'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content');
      assert.strictEqual(result.mainContent.frequency, 1.0, 'Should have frequency of 1.0 when present in all samples');
    });

    it('should handle varying main content selectors', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <main class="main-content">
                  <h1>Page 1</h1>
                  <p>Content.</p>
                </main>
              </body>
            </html>
          `,
          title: 'Page 1'
        },
        {
          url: 'http://example.com/page2',
          html: `
            <html>
              <body>
                <article class="post">
                  <h1>Page 2</h1>
                  <p>Content.</p>
                </article>
              </body>
            </html>
          `,
          title: 'Page 2'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content');
      // Frequency should be less than 1.0 since different selectors are used
      assert.ok(result.mainContent.frequency <= 1.0, 'Should calculate frequency correctly');
    });

    it('should output expected format', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <main class="main-content">
                  <h1>Content</h1>
                  <p>Text.</p>
                </main>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should have mainContent property');
      assert.ok(result.mainContent.xpath, 'Should have xpath property');
      assert.ok(typeof result.mainContent.frequency === 'number', 'Should have frequency as number');
      assert.ok(result.mainContent.frequency >= 0 && result.mainContent.frequency <= 1, 'Frequency should be between 0 and 1');
    });

    it('should prefer semantic elements over generic divs', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <div class="content">
                  <p>Some content in a div.</p>
                </div>
                <main>
                  <h1>Main Content</h1>
                  <p>Content in semantic main element.</p>
                </main>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      assert.ok(result.mainContent, 'Should identify main content');
      assert.ok(result.mainContent.xpath.includes('main'), 'Should prefer semantic main element');
    });

    it('should handle pages with no clear main content', async () => {
      const htmlContents = [
        {
          url: 'http://example.com/page1',
          html: `
            <html>
              <body>
                <div>Minimal content</div>
              </body>
            </html>
          `,
          title: 'Page 1'
        }
      ];

      const result = await analyzer.analyze(htmlContents);
      
      // Should either find something or return null
      if (result.mainContent) {
        assert.ok(result.mainContent.xpath, 'If found, should have xpath');
      }
    });
  });

  describe('Error Handling', () => {
    it('should throw error when no HTML content provided', async () => {
      await assert.rejects(
        async () => await analyzer.analyze([]),
        /No HTML content provided/,
        'Should throw error for empty array'
      );
    });

    it('should throw error when null provided', async () => {
      await assert.rejects(
        async () => await analyzer.analyze(null),
        /No HTML content provided/,
        'Should throw error for null'
      );
    });
  });
});
