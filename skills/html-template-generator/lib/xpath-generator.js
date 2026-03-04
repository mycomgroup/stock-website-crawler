/**
 * XPathGenerator - Generates XPath extraction rules from structure analysis
 */
export class XPathGenerator {
  constructor(options = {}) {
    this.frequencyThreshold = options.frequencyThreshold || 0.8;
  }

  /**
   * Generate XPath rules from structure analysis
   * @param {Object} structure - Structure analysis result from StructureAnalyzer
   * @returns {Object} XPath rules for content extraction
   */
  generate(structure) {
    console.log('\nGenerating XPath rules...');
    
    const rules = {
      title: this._generateTitleXPath(structure.headings),
      sections: this._generateSectionsXPath(structure),
      filters: this._generateFilters(structure)
    };
    
    console.log('✓ XPath rules generated\n');
    
    return rules;
  }

  /**
   * Generate title XPath
   * @param {Object} headings - Headings from structure analysis
   * @returns {string|null} XPath expression for title
   * @private
   */
  _generateTitleXPath(headings) {
    // Prioritize h1 with high frequency
    if (headings.h1 && headings.h1.frequency >= this.frequencyThreshold) {
      return `${headings.h1.xpath}/text()`;
    }
    
    // Fallback to h2
    if (headings.h2 && headings.h2.frequency >= this.frequencyThreshold) {
      return `${headings.h2.xpath}/text()`;
    }
    
    return null;
  }

  /**
   * Generate sections XPath
   * @param {Object} structure - Complete structure analysis
   * @returns {Object|null} Sections extraction rules
   * @private
   */
  _generateSectionsXPath(structure) {
    // Find content container
    const containerXPath = this._findContentContainer(structure);
    
    if (!containerXPath) {
      return null;
    }
    
    return {
      xpath: containerXPath,
      extract: {
        heading: this._generateRelativeXPath(structure.headings, 'h2'),
        description: './/p/text()',
        table: this._generateTableXPath(structure.tables),
        codeExample: this._generateCodeXPath(structure.codeBlocks),
        list: this._generateListXPath(structure.lists)
      }
    };
  }

  /**
   * Find content container XPath
   * @param {Object} structure - Structure analysis
   * @returns {string|null} Container XPath
   * @private
   */
  _findContentContainer(structure) {
    if (structure.mainContent && structure.mainContent.frequency >= this.frequencyThreshold) {
      return structure.mainContent.xpath;
    }
    
    // Fallback to common container patterns
    return "//main | //article | //div[contains(@class, 'content')]";
  }

  /**
   * Generate relative XPath for heading
   * @param {Object} headings - Headings structure
   * @param {string} tag - Heading tag (h1, h2, etc.)
   * @returns {string} Relative XPath
   * @private
   */
  _generateRelativeXPath(headings, tag) {
    if (headings[tag] && headings[tag].frequency >= this.frequencyThreshold) {
      const xpath = headings[tag].xpath;
      // Convert to relative path
      return xpath.replace(/^\/\//, './/') + '/text()';
    }
    
    return `.//${tag}/text()`;
  }

  /**
   * Generate table XPath
   * @param {Array} tables - Tables from structure analysis
   * @returns {Object|null} Table extraction rules
   * @private
   */
  _generateTableXPath(tables) {
    // Find most common table
    const commonTable = tables.find(t => t.frequency >= this.frequencyThreshold);
    
    if (!commonTable) {
      return null;
    }
    
    return {
      xpath: commonTable.xpath.replace(/^\/\//, './/'),
      headers: './/thead/tr/th/text()',
      rows: './/tbody/tr',
      cells: './/td/text()'
    };
  }

  /**
   * Generate code block XPath
   * @param {Array} codeBlocks - Code blocks from structure analysis
   * @returns {string|null} Code block XPath
   * @private
   */
  _generateCodeXPath(codeBlocks) {
    const commonCode = codeBlocks.find(c => c.frequency >= this.frequencyThreshold);
    
    if (!commonCode) {
      return null;
    }
    
    return commonCode.xpath.replace(/^\/\//, './/') + '/text()';
  }

  /**
   * Generate list XPath
   * @param {Array} lists - Lists from structure analysis
   * @returns {Object|null} List extraction rules
   * @private
   */
  _generateListXPath(lists) {
    const commonList = lists.find(l => l.frequency >= this.frequencyThreshold);
    
    if (!commonList) {
      return null;
    }
    
    return {
      xpath: commonList.xpath.replace(/^\/\//, './/'),
      items: './/li/text()'
    };
  }

  /**
   * Generate filter rules to remove noise elements
   * @param {Object} structure - Structure analysis
   * @returns {Object} Filter rules
   * @private
   */
  _generateFilters(structure) {
    const removeXPaths = new Set();
    
    // Add baseline filters for common noise elements
    const baselineFilters = [
      "//nav",
      "//header",
      "//footer",
      "//aside"
    ];
    baselineFilters.forEach(xpath => removeXPaths.add(xpath));
    
    // Identify ad elements
    const adFilters = this._identifyAdElements(structure);
    adFilters.forEach(xpath => removeXPaths.add(xpath));
    
    // Identify navigation elements
    const navFilters = this._identifyNavigationElements(structure);
    navFilters.forEach(xpath => removeXPaths.add(xpath));
    
    // Identify sidebar elements
    const sidebarFilters = this._identifySidebarElements(structure);
    sidebarFilters.forEach(xpath => removeXPaths.add(xpath));
    
    return {
      removeXPaths: Array.from(removeXPaths),
      cleanText: true
    };
  }

  /**
   * Identify ad elements from structure
   * @param {Object} structure - Structure analysis
   * @returns {Array<string>} XPath expressions for ad elements
   * @private
   */
  _identifyAdElements(structure) {
    const adXPaths = [];
    
    // Common ad-related class patterns
    const adPatterns = [
      'ad',
      'advertisement',
      'banner',
      'promo',
      'sponsored'
    ];
    
    // Generate XPath filters for ad patterns
    adPatterns.forEach(pattern => {
      adXPaths.push(`//div[contains(@class, '${pattern}')]`);
      adXPaths.push(`//section[contains(@class, '${pattern}')]`);
    });
    
    return adXPaths;
  }

  /**
   * Identify navigation elements from structure
   * @param {Object} structure - Structure analysis
   * @returns {Array<string>} XPath expressions for navigation elements
   * @private
   */
  _identifyNavigationElements(structure) {
    const navXPaths = [];
    
    // Common navigation class patterns
    const navPatterns = [
      'menu',
      'navigation',
      'navbar',
      'nav-bar',
      'breadcrumb'
    ];
    
    // Generate XPath filters for navigation patterns
    navPatterns.forEach(pattern => {
      navXPaths.push(`//div[contains(@class, '${pattern}')]`);
      navXPaths.push(`//ul[contains(@class, '${pattern}')]`);
    });
    
    return navXPaths;
  }

  /**
   * Identify sidebar elements from structure
   * @param {Object} structure - Structure analysis
   * @returns {Array<string>} XPath expressions for sidebar elements
   * @private
   */
  _identifySidebarElements(structure) {
    const sidebarXPaths = [];
    
    // Common sidebar class patterns
    const sidebarPatterns = [
      'sidebar',
      'side-bar',
      'widget',
      'related'
    ];
    
    // Generate XPath filters for sidebar patterns
    sidebarPatterns.forEach(pattern => {
      sidebarXPaths.push(`//div[contains(@class, '${pattern}')]`);
      sidebarXPaths.push(`//aside[contains(@class, '${pattern}')]`);
    });
    
    return sidebarXPaths;
  }
}
