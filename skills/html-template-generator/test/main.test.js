import { TemplateGenerator } from '../main.js';
import { writeFile, mkdir, rm, readFile } from 'fs/promises';
import { join } from 'path';

describe('TemplateGenerator', () => {
  const testDir = join(process.cwd(), 'test', 'fixtures');
  const patternsFile = join(testDir, 'test-patterns.json');
  const outputFile = join(testDir, 'output', 'test-template.json');
  let generator;

  beforeAll(async () => {
    await mkdir(join(testDir, 'output'), { recursive: true });
  });

  afterAll(async () => {
    await rm(testDir, { recursive: true, force: true });
  });

  beforeEach(() => {
    generator = new TemplateGenerator({
      browser: {
        headless: true,
        userDataDir: '../../stock-crawler/chrome_user_data'
      }
    });
  });

  describe('constructor', () => {
    it('should create instance with default config', () => {
      const gen = new TemplateGenerator();
      expect(gen).toBeDefined();
      expect(gen.patternReader).toBeDefined();
      expect(gen.browserManager).toBeDefined();
      expect(gen.htmlFetcher).toBeDefined();
      expect(gen.structureAnalyzer).toBeDefined();
      expect(gen.xpathGenerator).toBeDefined();
      expect(gen.templateWriter).toBeDefined();
    });

    it('should create instance with custom config', () => {
      const config = {
        browser: {
          userDataDir: '/custom/path',
          headless: false
        }
      };
      const gen = new TemplateGenerator(config);
      expect(gen).toBeDefined();
      expect(gen.browserManager.userDataDir).toContain('custom');
    });
  });

  describe('generate - error handling', () => {
    it('should throw error for non-existent patterns file', async () => {
      await expect(
        generator.generate('test-template', 'non-existent.json', outputFile)
      ).rejects.toThrow();
    });

    it('should throw error for non-existent template', async () => {
      const patterns = [
        {
          name: 'other-template',
          description: 'Other template',
          samples: ['https://example.com']
        }
      ];
      await writeFile(patternsFile, JSON.stringify(patterns));

      await expect(
        generator.generate('non-existent-template', patternsFile, outputFile)
      ).rejects.toThrow('Template "non-existent-template" not found');
    });
  });

  describe('_displayAnalysisSummary', () => {
    it('should display complete structure summary', () => {
      const structure = {
        mainContent: { xpath: '//main', frequency: 1.0 },
        headings: { h1: {}, h2: {} },
        tables: [{ xpath: '//table' }],
        codeBlocks: [{ xpath: '//pre/code' }],
        lists: [{ xpath: '//ul' }],
        metadata: { sampleCount: 5 }
      };

      // Should not throw
      expect(() => generator._displayAnalysisSummary(structure)).not.toThrow();
    });

    it('should handle minimal structure', () => {
      const structure = {
        mainContent: null,
        headings: {},
        tables: [],
        codeBlocks: [],
        lists: [],
        metadata: { sampleCount: 1 }
      };

      // Should not throw
      expect(() => generator._displayAnalysisSummary(structure)).not.toThrow();
    });
  });

  describe('_displayXPathSummary', () => {
    it('should display complete XPath summary', () => {
      const xpaths = {
        title: '//h1/text()',
        sections: {
          xpath: '//main',
          extract: {
            heading: './/h2/text()',
            table: { xpath: './/table' },
            codeExample: './/pre/code/text()',
            list: { xpath: './/ul' }
          }
        },
        filters: {
          removeXPaths: ['//nav', '//footer']
        }
      };

      // Should not throw
      expect(() => generator._displayXPathSummary(xpaths)).not.toThrow();
    });

    it('should handle minimal XPath rules', () => {
      const xpaths = {
        title: null,
        sections: null,
        filters: null
      };

      // Should not throw
      expect(() => generator._displayXPathSummary(xpaths)).not.toThrow();
    });

    it('should handle sections without extract', () => {
      const xpaths = {
        title: '//h1/text()',
        sections: {
          xpath: '//main',
          extract: {}
        },
        filters: {
          removeXPaths: []
        }
      };

      // Should not throw
      expect(() => generator._displayXPathSummary(xpaths)).not.toThrow();
    });
  });
});
