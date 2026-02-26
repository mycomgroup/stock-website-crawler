import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert';
import { XPathGenerator } from '../lib/xpath-generator.js';

describe('XPathGenerator', () => {
  let generator;

  beforeEach(() => {
    generator = new XPathGenerator();
  });

  describe('generate()', () => {
    it('should generate complete XPath rules from structure', () => {
      const structure = {
        mainContent: {
          xpath: "//div[@class='main-content']",
          frequency: 1.0
        },
        headings: {
          h1: {
            xpath: "//h1[@class='page-title']",
            frequency: 1.0,
            samples: ['API Documentation']
          },
          h2: {
            xpath: "//h2[@class='section-title']",
            frequency: 1.0,
            samples: ['Overview', 'Parameters']
          }
        },
        tables: [{
          xpath: "//table[@class='params-table']",
          frequency: 1.0,
          caption: 'Parameters',
          columnCount: 4
        }],
        codeBlocks: [{
          xpath: "//pre/code",
          frequency: 1.0,
          language: 'json'
        }],
        lists: [{
          xpath: "//ul[@class='api-list']",
          frequency: 1.0,
          type: 'ul'
        }],
        metadata: {
          sampleCount: 5,
          analyzedAt: new Date().toISOString()
        }
      };

      const rules = generator.generate(structure);

      assert.ok(rules, 'Should return rules object');
      assert.ok(rules.title, 'Should have title XPath');
      assert.ok(rules.sections, 'Should have sections rules');
      assert.ok(rules.filters, 'Should have filter rules');
    });

    it('should handle structure with missing elements', () => {
      const structure = {
        mainContent: null,
        headings: {},
        tables: [],
        codeBlocks: [],
        lists: [],
        metadata: {
          sampleCount: 5,
          analyzedAt: new Date().toISOString()
        }
      };

      const rules = generator.generate(structure);

      assert.ok(rules, 'Should return rules object');
      assert.strictEqual(rules.title, null, 'Should have null title when no headings');
      assert.ok(rules.filters, 'Should still have filter rules');
    });
  });

  describe('_generateTitleXPath()', () => {
    it('should prioritize h1 with high frequency', () => {
      const headings = {
        h1: {
          xpath: "//h1[@class='page-title']",
          frequency: 1.0
        },
        h2: {
          xpath: "//h2[@class='section-title']",
          frequency: 1.0
        }
      };

      const titleXPath = generator._generateTitleXPath(headings);

      assert.strictEqual(titleXPath, "//h1[@class='page-title']/text()");
    });

    it('should fallback to h2 when h1 frequency is low', () => {
      const headings = {
        h1: {
          xpath: "//h1[@class='page-title']",
          frequency: 0.6
        },
        h2: {
          xpath: "//h2[@class='section-title']",
          frequency: 1.0
        }
      };

      const titleXPath = generator._generateTitleXPath(headings);

      assert.strictEqual(titleXPath, "//h2[@class='section-title']/text()");
    });

    it('should return null when no suitable heading found', () => {
      const headings = {
        h3: {
          xpath: "//h3",
          frequency: 0.5
        }
      };

      const titleXPath = generator._generateTitleXPath(headings);

      assert.strictEqual(titleXPath, null);
    });
  });

  describe('_findContentContainer()', () => {
    it('should use mainContent when frequency is high', () => {
      const structure = {
        mainContent: {
          xpath: "//div[@class='main-content']",
          frequency: 0.9
        }
      };

      const containerXPath = generator._findContentContainer(structure);

      assert.strictEqual(containerXPath, "//div[@class='main-content']");
    });

    it('should use fallback when mainContent frequency is low', () => {
      const structure = {
        mainContent: {
          xpath: "//div[@class='main-content']",
          frequency: 0.5
        }
      };

      const containerXPath = generator._findContentContainer(structure);

      assert.strictEqual(containerXPath, "//main | //article | //div[contains(@class, 'content')]");
    });

    it('should use fallback when mainContent is null', () => {
      const structure = {
        mainContent: null
      };

      const containerXPath = generator._findContentContainer(structure);

      assert.strictEqual(containerXPath, "//main | //article | //div[contains(@class, 'content')]");
    });
  });

  describe('_generateRelativeXPath()', () => {
    it('should convert absolute XPath to relative', () => {
      const headings = {
        h2: {
          xpath: "//h2[@class='section-title']",
          frequency: 1.0
        }
      };

      const relativeXPath = generator._generateRelativeXPath(headings, 'h2');

      assert.strictEqual(relativeXPath, ".//h2[@class='section-title']/text()");
    });

    it('should use generic XPath when frequency is low', () => {
      const headings = {
        h2: {
          xpath: "//h2[@class='section-title']",
          frequency: 0.5
        }
      };

      const relativeXPath = generator._generateRelativeXPath(headings, 'h2');

      assert.strictEqual(relativeXPath, ".//h2/text()");
    });

    it('should use generic XPath when heading not found', () => {
      const headings = {};

      const relativeXPath = generator._generateRelativeXPath(headings, 'h2');

      assert.strictEqual(relativeXPath, ".//h2/text()");
    });
  });

  describe('_generateTableXPath()', () => {
    it('should generate table extraction rules', () => {
      const tables = [{
        xpath: "//table[@class='params-table']",
        frequency: 1.0,
        caption: 'Parameters',
        columnCount: 4
      }];

      const tableXPath = generator._generateTableXPath(tables);

      assert.ok(tableXPath, 'Should return table rules');
      assert.strictEqual(tableXPath.xpath, ".//table[@class='params-table']");
      assert.strictEqual(tableXPath.headers, './/thead/tr/th/text()');
      assert.strictEqual(tableXPath.rows, './/tbody/tr');
      assert.strictEqual(tableXPath.cells, './/td/text()');
    });

    it('should return null when no common table found', () => {
      const tables = [{
        xpath: "//table",
        frequency: 0.5
      }];

      const tableXPath = generator._generateTableXPath(tables);

      assert.strictEqual(tableXPath, null);
    });

    it('should return null when tables array is empty', () => {
      const tables = [];

      const tableXPath = generator._generateTableXPath(tables);

      assert.strictEqual(tableXPath, null);
    });
  });

  describe('_generateCodeXPath()', () => {
    it('should generate code block XPath', () => {
      const codeBlocks = [{
        xpath: "//pre/code",
        frequency: 1.0,
        language: 'json'
      }];

      const codeXPath = generator._generateCodeXPath(codeBlocks);

      assert.strictEqual(codeXPath, ".//pre/code/text()");
    });

    it('should return null when no common code block found', () => {
      const codeBlocks = [{
        xpath: "//code",
        frequency: 0.5
      }];

      const codeXPath = generator._generateCodeXPath(codeBlocks);

      assert.strictEqual(codeXPath, null);
    });

    it('should return null when codeBlocks array is empty', () => {
      const codeBlocks = [];

      const codeXPath = generator._generateCodeXPath(codeBlocks);

      assert.strictEqual(codeXPath, null);
    });
  });

  describe('_generateListXPath()', () => {
    it('should generate list extraction rules', () => {
      const lists = [{
        xpath: "//ul[@class='api-list']",
        frequency: 1.0,
        type: 'ul'
      }];

      const listXPath = generator._generateListXPath(lists);

      assert.ok(listXPath, 'Should return list rules');
      assert.strictEqual(listXPath.xpath, ".//ul[@class='api-list']");
      assert.strictEqual(listXPath.items, './/li/text()');
    });

    it('should return null when no common list found', () => {
      const lists = [{
        xpath: "//ul",
        frequency: 0.5
      }];

      const listXPath = generator._generateListXPath(lists);

      assert.strictEqual(listXPath, null);
    });

    it('should return null when lists array is empty', () => {
      const lists = [];

      const listXPath = generator._generateListXPath(lists);

      assert.strictEqual(listXPath, null);
    });
  });

  describe('_generateFilters()', () => {
    it('should generate filter rules', () => {
      const structure = {
        mainContent: null,
        headings: {},
        tables: [],
        codeBlocks: [],
        lists: []
      };

      const filters = generator._generateFilters(structure);

      assert.ok(filters, 'Should return filters object');
      assert.ok(Array.isArray(filters.removeXPaths), 'Should have removeXPaths array');
      assert.ok(filters.removeXPaths.length > 0, 'Should have filter XPaths');
      assert.strictEqual(filters.cleanText, true, 'Should have cleanText flag');
    });

    it('should include baseline noise element filters', () => {
      const structure = {};
      const filters = generator._generateFilters(structure);

      assert.ok(filters.removeXPaths.includes('//nav'), 'Should filter nav');
      assert.ok(filters.removeXPaths.includes('//header'), 'Should filter header');
      assert.ok(filters.removeXPaths.includes('//footer'), 'Should filter footer');
      assert.ok(filters.removeXPaths.includes('//aside'), 'Should filter aside');
    });

    it('should include ad element filters', () => {
      const structure = {};
      const filters = generator._generateFilters(structure);

      const hasAdFilter = filters.removeXPaths.some(xpath => 
        xpath.includes('ad') || xpath.includes('advertisement') || xpath.includes('banner')
      );
      assert.ok(hasAdFilter, 'Should include ad-related filters');
    });

    it('should include navigation element filters', () => {
      const structure = {};
      const filters = generator._generateFilters(structure);

      const hasNavFilter = filters.removeXPaths.some(xpath => 
        xpath.includes('menu') || xpath.includes('navigation') || xpath.includes('navbar')
      );
      assert.ok(hasNavFilter, 'Should include navigation-related filters');
    });

    it('should include sidebar element filters', () => {
      const structure = {};
      const filters = generator._generateFilters(structure);

      const hasSidebarFilter = filters.removeXPaths.some(xpath => 
        xpath.includes('sidebar') || xpath.includes('widget')
      );
      assert.ok(hasSidebarFilter, 'Should include sidebar-related filters');
    });

    it('should not have duplicate XPath expressions', () => {
      const structure = {};
      const filters = generator._generateFilters(structure);

      const uniqueXPaths = new Set(filters.removeXPaths);
      assert.strictEqual(
        uniqueXPaths.size, 
        filters.removeXPaths.length,
        'Should not have duplicate XPath expressions'
      );
    });

    it('should set cleanText to true', () => {
      const structure = {};
      const filters = generator._generateFilters(structure);

      assert.strictEqual(filters.cleanText, true, 'cleanText should be true');
    });
  });

  describe('_identifyAdElements()', () => {
    it('should generate XPath filters for ad elements', () => {
      const structure = {};
      const adFilters = generator._identifyAdElements(structure);

      assert.ok(Array.isArray(adFilters), 'Should return an array');
      assert.ok(adFilters.length > 0, 'Should have ad filters');
      
      const hasAdFilter = adFilters.some(xpath => xpath.includes('ad'));
      assert.ok(hasAdFilter, 'Should include ad pattern');
    });

    it('should include common ad patterns', () => {
      const structure = {};
      const adFilters = generator._identifyAdElements(structure);

      const patterns = ['ad', 'advertisement', 'banner', 'promo', 'sponsored'];
      patterns.forEach(pattern => {
        const hasPattern = adFilters.some(xpath => xpath.includes(pattern));
        assert.ok(hasPattern, `Should include ${pattern} pattern`);
      });
    });
  });

  describe('_identifyNavigationElements()', () => {
    it('should generate XPath filters for navigation elements', () => {
      const structure = {};
      const navFilters = generator._identifyNavigationElements(structure);

      assert.ok(Array.isArray(navFilters), 'Should return an array');
      assert.ok(navFilters.length > 0, 'Should have navigation filters');
    });

    it('should include common navigation patterns', () => {
      const structure = {};
      const navFilters = generator._identifyNavigationElements(structure);

      const patterns = ['menu', 'navigation', 'navbar', 'breadcrumb'];
      patterns.forEach(pattern => {
        const hasPattern = navFilters.some(xpath => xpath.includes(pattern));
        assert.ok(hasPattern, `Should include ${pattern} pattern`);
      });
    });
  });

  describe('_identifySidebarElements()', () => {
    it('should generate XPath filters for sidebar elements', () => {
      const structure = {};
      const sidebarFilters = generator._identifySidebarElements(structure);

      assert.ok(Array.isArray(sidebarFilters), 'Should return an array');
      assert.ok(sidebarFilters.length > 0, 'Should have sidebar filters');
    });

    it('should include common sidebar patterns', () => {
      const structure = {};
      const sidebarFilters = generator._identifySidebarElements(structure);

      const patterns = ['sidebar', 'widget', 'related'];
      patterns.forEach(pattern => {
        const hasPattern = sidebarFilters.some(xpath => xpath.includes(pattern));
        assert.ok(hasPattern, `Should include ${pattern} pattern`);
      });
    });
  });

  describe('_generateSectionsXPath()', () => {
    it('should generate complete sections rules', () => {
      const structure = {
        mainContent: {
          xpath: "//div[@class='main-content']",
          frequency: 1.0
        },
        headings: {
          h2: {
            xpath: "//h2[@class='section-title']",
            frequency: 1.0
          }
        },
        tables: [{
          xpath: "//table[@class='params-table']",
          frequency: 1.0
        }],
        codeBlocks: [{
          xpath: "//pre/code",
          frequency: 1.0
        }],
        lists: [{
          xpath: "//ul[@class='api-list']",
          frequency: 1.0
        }]
      };

      const sections = generator._generateSectionsXPath(structure);

      assert.ok(sections, 'Should return sections object');
      assert.strictEqual(sections.xpath, "//div[@class='main-content']");
      assert.ok(sections.extract, 'Should have extract rules');
      assert.ok(sections.extract.heading, 'Should have heading XPath');
      assert.ok(sections.extract.description, 'Should have description XPath');
      assert.ok(sections.extract.table, 'Should have table rules');
      assert.ok(sections.extract.codeExample, 'Should have code XPath');
      assert.ok(sections.extract.list, 'Should have list rules');
    });

    it('should handle missing optional elements', () => {
      const structure = {
        mainContent: {
          xpath: "//main",
          frequency: 1.0
        },
        headings: {},
        tables: [],
        codeBlocks: [],
        lists: []
      };

      const sections = generator._generateSectionsXPath(structure);

      assert.ok(sections, 'Should return sections object');
      assert.strictEqual(sections.xpath, "//main");
      assert.strictEqual(sections.extract.table, null, 'Should have null table when not found');
      assert.strictEqual(sections.extract.codeExample, null, 'Should have null code when not found');
      assert.strictEqual(sections.extract.list, null, 'Should have null list when not found');
    });
  });
});
