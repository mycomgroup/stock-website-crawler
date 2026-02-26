import { TemplateWriter } from '../lib/template-writer.js';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

describe('TemplateWriter', () => {
  let writer;
  let testOutputDir;

  beforeEach(() => {
    writer = new TemplateWriter();
    testOutputDir = path.join(__dirname, '../output/test');
  });

  afterEach(async () => {
    // Clean up test files
    try {
      await fs.rm(testOutputDir, { recursive: true, force: true });
    } catch (error) {
      // Ignore cleanup errors
    }
  });

  describe('write()', () => {
    test('should write template file with complete structure', async () => {
      const outputFile = path.join(testOutputDir, 'test-template.json');
      const data = {
        templateName: 'test-template',
        samples: [
          'https://example.com/page1',
          'https://example.com/page2'
        ],
        xpaths: {
          title: "//h1[@class='title']/text()",
          sections: {
            xpath: "//div[@class='content']",
            extract: {
              heading: ".//h2/text()",
              description: ".//p/text()",
              table: {
                xpath: ".//table",
                headers: ".//thead/tr/th/text()",
                rows: ".//tbody/tr",
                cells: ".//td/text()"
              },
              codeExample: ".//pre/code/text()",
              list: {
                xpath: ".//ul",
                items: ".//li/text()"
              }
            }
          },
          filters: {
            removeXPaths: ["//nav", "//footer"],
            cleanText: true
          }
        },
        filters: {
          removeXPaths: ["//nav", "//footer"],
          cleanText: true
        },
        metadata: {
          sampleCount: 2,
          analyzedAt: '2024-01-15T10:30:00.000Z'
        }
      };

      await writer.write(outputFile, data);

      // Verify file exists
      const fileExists = await fs.access(outputFile).then(() => true).catch(() => false);
      expect(fileExists).toBe(true);

      // Read and parse file
      const content = await fs.readFile(outputFile, 'utf-8');
      const template = JSON.parse(content);

      // Verify structure
      expect(template.templateName).toBe('test-template');
      expect(template.version).toBe('1.0.0');
      expect(template.generatedAt).toBeDefined();
      expect(template.samples).toHaveLength(2);
      expect(template.xpaths).toBeDefined();
      expect(template.filters).toBeDefined();
      expect(template.metadata).toBeDefined();
    });

    test('should include correct metadata', async () => {
      const outputFile = path.join(testOutputDir, 'metadata-test.json');
      const data = {
        templateName: 'metadata-test',
        samples: ['https://example.com/page1'],
        xpaths: {
          title: "//h1/text()",
          sections: {
            xpath: "//div[@class='content']",
            extract: {
              heading: ".//h2/text()",
              table: {
                xpath: ".//table",
                headers: ".//thead/tr/th/text()"
              },
              codeExample: ".//pre/code/text()"
            }
          }
        },
        filters: {},
        metadata: {
          sampleCount: 5,
          analyzedAt: '2024-01-15T10:30:00.000Z'
        }
      };

      await writer.write(outputFile, data);

      const content = await fs.readFile(outputFile, 'utf-8');
      const template = JSON.parse(content);

      expect(template.metadata.sampleCount).toBe(5);
      expect(template.metadata.commonElements).toBeDefined();
      expect(template.metadata.commonElements.title).toBe(5);
      expect(template.metadata.commonElements.sections).toBe(5);
      expect(template.metadata.commonElements.tables).toBe(5);
      expect(template.metadata.commonElements.codeBlocks).toBe(5);
    });

    test('should create output directory if it does not exist', async () => {
      const deepPath = path.join(testOutputDir, 'deep/nested/path/template.json');
      const data = {
        templateName: 'nested-test',
        samples: [],
        xpaths: {},
        filters: {},
        metadata: { sampleCount: 0 }
      };

      await writer.write(deepPath, data);

      const fileExists = await fs.access(deepPath).then(() => true).catch(() => false);
      expect(fileExists).toBe(true);
    });

    test('should handle minimal data', async () => {
      const outputFile = path.join(testOutputDir, 'minimal-test.json');
      const data = {
        templateName: 'minimal-test'
      };

      await writer.write(outputFile, data);

      const content = await fs.readFile(outputFile, 'utf-8');
      const template = JSON.parse(content);

      expect(template.templateName).toBe('minimal-test');
      expect(template.version).toBe('1.0.0');
      expect(template.samples).toEqual([]);
      expect(template.xpaths).toEqual({});
      expect(template.filters).toEqual({});
      expect(template.metadata.sampleCount).toBe(0);
    });

    test('should format JSON with proper indentation', async () => {
      const outputFile = path.join(testOutputDir, 'format-test.json');
      const data = {
        templateName: 'format-test',
        samples: ['https://example.com'],
        xpaths: { title: "//h1/text()" },
        filters: {},
        metadata: { sampleCount: 1 }
      };

      await writer.write(outputFile, data);

      const content = await fs.readFile(outputFile, 'utf-8');
      
      // Verify JSON is formatted with 2-space indentation
      expect(content).toContain('  "templateName"');
      expect(content).toContain('  "version"');
    });

    test('should include timestamp in generatedAt field', async () => {
      const outputFile = path.join(testOutputDir, 'timestamp-test.json');
      const data = {
        templateName: 'timestamp-test',
        samples: [],
        xpaths: {},
        filters: {},
        metadata: { sampleCount: 0 }
      };

      const beforeTime = new Date().toISOString();
      await writer.write(outputFile, data);
      const afterTime = new Date().toISOString();

      const content = await fs.readFile(outputFile, 'utf-8');
      const template = JSON.parse(content);

      expect(template.generatedAt).toBeDefined();
      expect(template.generatedAt).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/);
      expect(template.generatedAt >= beforeTime).toBe(true);
      expect(template.generatedAt <= afterTime).toBe(true);
    });
  });

  describe('_buildTemplate()', () => {
    test('should build complete template object', () => {
      const data = {
        templateName: 'test',
        samples: ['https://example.com'],
        xpaths: { title: "//h1/text()" },
        filters: { removeXPaths: ["//nav"] },
        metadata: { sampleCount: 1 }
      };

      const template = writer._buildTemplate(data);

      expect(template.templateName).toBe('test');
      expect(template.version).toBe('1.0.0');
      expect(template.generatedAt).toBeDefined();
      expect(template.samples).toEqual(['https://example.com']);
      expect(template.xpaths).toEqual({ title: "//h1/text()" });
      expect(template.filters).toEqual({ removeXPaths: ["//nav"] });
      expect(template.metadata).toBeDefined();
    });
  });

  describe('_buildMetadata()', () => {
    test('should count common elements correctly', () => {
      const data = {
        xpaths: {
          title: "//h1/text()",
          sections: {
            xpath: "//div",
            extract: {
              heading: ".//h2/text()",
              table: { xpath: ".//table" },
              codeExample: ".//pre/code/text()",
              list: { xpath: ".//ul" }
            }
          }
        },
        metadata: { sampleCount: 5 }
      };

      const metadata = writer._buildMetadata(data);

      expect(metadata.sampleCount).toBe(5);
      expect(metadata.commonElements.title).toBe(5);
      expect(metadata.commonElements.sections).toBe(5);
      expect(metadata.commonElements.tables).toBe(5);
      expect(metadata.commonElements.codeBlocks).toBe(5);
      expect(metadata.commonElements.lists).toBe(5);
    });

    test('should handle missing elements', () => {
      const data = {
        xpaths: {
          title: "//h1/text()",
          sections: {
            xpath: "//div",
            extract: {
              heading: ".//h2/text()"
            }
          }
        },
        metadata: { sampleCount: 3 }
      };

      const metadata = writer._buildMetadata(data);

      expect(metadata.sampleCount).toBe(3);
      expect(metadata.commonElements.title).toBe(3);
      expect(metadata.commonElements.sections).toBe(3);
      expect(metadata.commonElements.tables).toBeUndefined();
      expect(metadata.commonElements.codeBlocks).toBeUndefined();
      expect(metadata.commonElements.lists).toBeUndefined();
    });

    test('should handle empty xpaths', () => {
      const data = {
        xpaths: {},
        metadata: { sampleCount: 0 }
      };

      const metadata = writer._buildMetadata(data);

      expect(metadata.sampleCount).toBe(0);
      expect(metadata.commonElements).toEqual({});
    });
  });
});
