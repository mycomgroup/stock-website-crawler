import { JSDOM } from 'jsdom';

/**
 * StructureAnalyzer - Analyzes HTML structure to identify common patterns
 */
export class StructureAnalyzer {
  /**
   * Analyze multiple HTML contents to find common patterns
   * @param {Array<{url: string, html: string, title: string}>} htmlContents - Array of HTML content objects
   * @returns {Promise<Object>} Structure analysis result
   */
  async analyze(htmlContents) {
    if (!htmlContents || htmlContents.length === 0) {
      throw new Error('No HTML content provided for analysis');
    }

    console.log(`\nAnalyzing ${htmlContents.length} HTML samples...`);
    
    // Analyze each sample
    const structures = [];
    for (const content of htmlContents) {
      const structure = await this._analyzeSingle(content.html);
      structures.push(structure);
    }
    
    // Merge structures to find common patterns
    const merged = this._mergeStructures(structures);
    
    console.log('✓ Structure analysis complete\n');
    
    return merged;
  }

  /**
   * Analyze single HTML document
   * @param {string} html - HTML content
   * @returns {Promise<Object>} Single structure analysis
   * @private
   */
  async _analyzeSingle(html) {
    const dom = new JSDOM(html);
    const document = dom.window.document;
    
    return {
      mainContent: this._findMainContent(document),
      headings: this._extractHeadings(document),
      tables: this._extractTables(document),
      codeBlocks: this._extractCodeBlocks(document),
      lists: this._extractLists(document)
    };
  }

  /**
   * Find main content area
   * @param {Document} document - DOM document
   * @returns {Object|null} Main content element info
   * @private
   */
  _findMainContent(document) {
    // Try semantic HTML5 elements first
    const semanticSelectors = [
      'main',
      'article',
      '[role="main"]'
    ];
    
    for (const selector of semanticSelectors) {
      const element = document.querySelector(selector);
      if (element && !this._isNoiseElement(element)) {
        return this._elementToInfo(element);
      }
    }
    
    // Try common class/id patterns
    const commonSelectors = [
      '.data-booth',      // Lixinger SPA content
      '.main-content',
      '.content',
      '#content',
      '.page-content',
      '.article-content',
      '.post-content'
    ];
    
    for (const selector of commonSelectors) {
      const element = document.querySelector(selector);
      if (element && !this._isNoiseElement(element)) {
        return this._elementToInfo(element);
      }
    }
    
    // Fallback: find element with highest content density
    return this._findByContentDensity(document);
  }

  /**
   * Check if element is likely noise (navigation, sidebar, ads)
   * @param {Element} element - DOM element
   * @returns {boolean} True if element is noise
   * @private
   */
  _isNoiseElement(element) {
    const noisePatterns = [
      /nav/i,
      /sidebar/i,
      /aside/i,
      /advertisement/i,
      /\bad\b/i,
      /banner/i,
      /footer/i,
      /header/i,
      /menu/i
    ];
    
    const className = element.className || '';
    const id = element.id || '';
    const combined = `${className} ${id}`;
    
    return noisePatterns.some(pattern => pattern.test(combined));
  }

  /**
   * Find main content by calculating content density
   * @param {Document} document - DOM document
   * @returns {Object|null} Element with highest content density
   * @private
   */
  _findByContentDensity(document) {
    // Get all potential container elements
    const containers = document.querySelectorAll('div, section, article');
    
    let bestCandidate = null;
    let bestScore = 0;
    
    for (const container of containers) {
      // Skip noise elements
      if (this._isNoiseElement(container)) {
        continue;
      }
      
      // Calculate content density score
      const score = this._calculateContentScore(container);
      
      if (score > bestScore) {
        bestScore = score;
        bestCandidate = container;
      }
    }
    
    return bestCandidate ? this._elementToInfo(bestCandidate) : null;
  }

  /**
   * Calculate content score for an element
   * @param {Element} element - DOM element
   * @returns {number} Content score
   * @private
   */
  _calculateContentScore(element) {
    const textContent = element.textContent || '';
    const innerHTML = element.innerHTML || '';
    
    // Text length
    const textLength = textContent.trim().length;
    
    // HTML length
    const htmlLength = innerHTML.length;
    
    // Avoid division by zero
    if (htmlLength === 0) return 0;
    
    // Content density: ratio of text to HTML
    const density = textLength / htmlLength;
    
    // Count meaningful elements (paragraphs, headings, lists)
    const paragraphs = element.querySelectorAll('p').length;
    const headings = element.querySelectorAll('h1, h2, h3, h4, h5, h6').length;
    const lists = element.querySelectorAll('ul, ol').length;
    const tables = element.querySelectorAll('table').length;
    const codeBlocks = element.querySelectorAll('pre, code').length;
    
    const meaningfulElements = paragraphs + headings + lists + tables + codeBlocks;
    
    // Calculate score: combine density with element count
    // Favor elements with good density and meaningful content
    const score = density * Math.log(textLength + 1) * (1 + meaningfulElements * 0.1);
    
    return score;
  }

  /**
   * Extract headings from document
   * @param {Document} document - DOM document
   * @returns {Object} Headings by level
   * @private
   */
  _extractHeadings(document) {
    const headings = {};
    
    for (let level = 1; level <= 6; level++) {
      const tag = `h${level}`;
      const elements = document.querySelectorAll(tag);
      
      if (elements.length > 0) {
        headings[tag] = Array.from(elements).map(el => ({
          text: el.textContent.trim(),
          class: el.className,
          id: el.id,
          xpath: this._generateXPath(el)
        }));
      }
    }
    
    return headings;
  }

  /**
   * Extract tables from document
   * @param {Document} document - DOM document
   * @returns {Array} Table information
   * @private
   */
  _extractTables(document) {
    const tables = document.querySelectorAll('table');
    
    return Array.from(tables).map(table => {
      const caption = table.querySelector('caption');
      const thead = table.querySelector('thead');
      const tbody = table.querySelector('tbody');
      
      return {
        class: table.className,
        id: table.id,
        caption: caption ? caption.textContent.trim() : null,
        columnCount: thead ? thead.querySelectorAll('th').length : 0,
        rowCount: tbody ? tbody.querySelectorAll('tr').length : 0,
        xpath: this._generateXPath(table)
      };
    });
  }

  /**
   * Extract code blocks from document
   * @param {Document} document - DOM document
   * @returns {Array} Code block information
   * @private
   */
  _extractCodeBlocks(document) {
    // Prioritize pre>code combinations, then standalone pre and code
    const codeBlocks = [];
    const seen = new Set();
    
    // First, get pre>code combinations
    const preCodeBlocks = document.querySelectorAll('pre code');
    for (const code of preCodeBlocks) {
      codeBlocks.push({
        class: code.className,
        language: this._detectLanguage(code),
        xpath: this._generateXPath(code)
      });
      // Mark both the code and its parent pre as seen
      seen.add(code);
      seen.add(code.parentElement);
    }
    
    // Then get standalone pre elements (not already processed)
    const preBlocks = document.querySelectorAll('pre');
    for (const pre of preBlocks) {
      if (!seen.has(pre)) {
        codeBlocks.push({
          class: pre.className,
          language: this._detectLanguage(pre),
          xpath: this._generateXPath(pre)
        });
        seen.add(pre);
      }
    }
    
    // Finally get standalone code elements (not already processed)
    const codeElements = document.querySelectorAll('code');
    for (const code of codeElements) {
      if (!seen.has(code)) {
        codeBlocks.push({
          class: code.className,
          language: this._detectLanguage(code),
          xpath: this._generateXPath(code)
        });
      }
    }
    
    return codeBlocks;
  }

  /**
   * Extract lists from document
   * @param {Document} document - DOM document
   * @returns {Array} List information
   * @private
   */
  _extractLists(document) {
    const lists = document.querySelectorAll('ul, ol');
    
    return Array.from(lists).map(list => ({
      type: list.tagName.toLowerCase(),
      class: list.className,
      id: list.id,
      itemCount: list.querySelectorAll('li').length,
      xpath: this._generateXPath(list)
    }));
  }

  /**
   * Escape quotes for XPath string
   * @param {string} str - String to escape
   * @returns {string} Escaped string
   * @private
   */
  _escapeXPathString(str) {
    if (!str) return str;
    if (str.includes("'") && str.includes('"')) {
      return 'concat(' + str.split("'").map(part => `'${part}'`).join(', "\'", ') + ')';
    } else if (str.includes("'")) {
      return `"${str}"`;
    }
    return `'${str}'`;
  }

  /**
   * Generate XPath for element
   * @param {Element} element - DOM element
   * @returns {string} XPath expression
   * @private
   */
  _generateXPath(element) {
    // Prioritize id
    if (element.id) {
      const escapedId = this._escapeXPathString(element.id);
      return `//*[@id=${escapedId}]`;
    }
    
    // Use class - use //* instead of //tagname for JSDOM compatibility
    if (element.className) {
      const classes = element.className.trim().split(/\s+/);
      if (classes.length > 0) {
        const escapedClass = this._escapeXPathString(classes[0]);
        return `//*[contains(@class, ${escapedClass})]`;
      }
    }
    
    // Fallback to tag name with //*
    return `//${element.tagName.toLowerCase()}`;
  }

  /**
   * Detect code language from element
   * @param {Element} element - Code element
   * @returns {string|null} Detected language
   * @private
   */
  _detectLanguage(element) {
    const className = element.className;
    if (!className) return null;
    
    const match = className.match(/language-(\w+)/);
    return match ? match[1] : null;
  }

  /**
   * Convert element to info object
   * @param {Element} element - DOM element
   * @returns {Object} Element information
   * @private
   */
  _elementToInfo(element) {
    return {
      xpath: this._generateXPath(element),
      class: element.className,
      id: element.id
    };
  }

  /**
   * Merge multiple structures to find common patterns
   * @param {Array} structures - Array of structure objects
   * @returns {Object} Merged structure with frequencies
   * @private
   */
  _mergeStructures(structures) {
    const sampleCount = structures.length;
    
    return {
      mainContent: this._findCommonElement(structures.map(s => s.mainContent), sampleCount),
      headings: this._mergeHeadings(structures.map(s => s.headings), sampleCount),
      tables: this._mergeTables(structures.map(s => s.tables), sampleCount),
      codeBlocks: this._mergeCodeBlocks(structures.map(s => s.codeBlocks), sampleCount),
      lists: this._mergeLists(structures.map(s => s.lists), sampleCount),
      metadata: {
        sampleCount,
        analyzedAt: new Date().toISOString()
      }
    };
  }

  /**
   * Find common element across samples
   * @param {Array} elements - Array of element info objects
   * @param {number} sampleCount - Total number of samples
   * @returns {Object|null} Common element with frequency
   * @private
   */
  _findCommonElement(elements, sampleCount) {
    const xpaths = {};
    
    for (const element of elements) {
      if (element && element.xpath) {
        xpaths[element.xpath] = (xpaths[element.xpath] || 0) + 1;
      }
    }
    
    const entries = Object.entries(xpaths);
    if (entries.length === 0) return null;
    
    const [xpath, count] = entries.sort((a, b) => {
      if (b[1] !== a[1]) return b[1] - a[1];
      return a[0].localeCompare(b[0]);
    })[0];
    return {
      xpath,
      frequency: count / sampleCount
    };
  }

  /**
   * Merge headings across samples
   * @param {Array} headingsList - Array of headings objects
   * @param {number} sampleCount - Total number of samples
   * @returns {Object} Merged headings with frequencies
   * @private
   */
  _mergeHeadings(headingsList, sampleCount) {
    const merged = {};
    
    for (let level = 1; level <= 6; level++) {
      const tag = `h${level}`;
      const xpaths = {};
      
      // Collect xpath occurrences and sample texts
      for (const headings of headingsList) {
        if (headings[tag]) {
          for (const heading of headings[tag]) {
            const xpath = heading.xpath;
            if (!xpaths[xpath]) {
              xpaths[xpath] = {
                count: 0,
                samples: []
              };
            }
            xpaths[xpath].count++;
            // Collect sample text (limit to first few samples to avoid duplication)
            if (xpaths[xpath].samples.length < 3 && heading.text) {
              xpaths[xpath].samples.push(heading.text);
            }
          }
        }
      }
      
      const entries = Object.entries(xpaths);
      if (entries.length > 0) {
        const [xpath, data] = entries.sort((a, b) => b[1].count - a[1].count)[0];
        merged[tag] = {
          xpath,
          frequency: data.count / sampleCount,
          samples: data.samples
        };
      }
    }
    
    return merged;
  }

  /**
   * Merge tables across samples
   * @param {Array} tablesList - Array of tables arrays
   * @param {number} sampleCount - Total number of samples
   * @returns {Array} Merged tables with frequencies
   * @private
   */
  _mergeTables(tablesList, sampleCount) {
    const xpaths = {};
    
    for (const tables of tablesList) {
      for (const table of tables) {
        const xpath = table.xpath;
        if (!xpaths[xpath]) {
          xpaths[xpath] = {
            count: 0,
            caption: table.caption,
            columnCount: table.columnCount
          };
        }
        xpaths[xpath].count++;
      }
    }
    
    return Object.entries(xpaths)
      .map(([xpath, data]) => ({
        xpath,
        frequency: data.count / sampleCount,
        caption: data.caption,
        columnCount: data.columnCount
      }))
      .sort((a, b) => b.frequency - a.frequency);
  }

  /**
   * Merge code blocks across samples
   * @param {Array} codeBlocksList - Array of code blocks arrays
   * @param {number} sampleCount - Total number of samples
   * @returns {Array} Merged code blocks with frequencies
   * @private
   */
  _mergeCodeBlocks(codeBlocksList, sampleCount) {
    const xpaths = {};
    
    for (const codeBlocks of codeBlocksList) {
      for (const code of codeBlocks) {
        const xpath = code.xpath;
        if (!xpaths[xpath]) {
          xpaths[xpath] = {
            count: 0,
            languages: []
          };
        }
        xpaths[xpath].count++;
        // Collect languages to find the most common one
        if (code.language && !xpaths[xpath].languages.includes(code.language)) {
          xpaths[xpath].languages.push(code.language);
        }
      }
    }
    
    return Object.entries(xpaths)
      .map(([xpath, data]) => ({
        xpath,
        frequency: data.count / sampleCount,
        // Use the first language if available, or null
        language: data.languages.length > 0 ? data.languages[0] : null
      }))
      .sort((a, b) => b.frequency - a.frequency);
  }

  /**
   * Merge lists across samples
   * @param {Array} listsList - Array of lists arrays
   * @param {number} sampleCount - Total number of samples
   * @returns {Array} Merged lists with frequencies
   * @private
   */
  _mergeLists(listsList, sampleCount) {
    const xpaths = {};
    
    for (const lists of listsList) {
      for (const list of lists) {
        const xpath = list.xpath;
        if (!xpaths[xpath]) {
          xpaths[xpath] = {
            count: 0,
            type: list.type
          };
        }
        xpaths[xpath].count++;
      }
    }
    
    return Object.entries(xpaths)
      .map(([xpath, data]) => ({
        xpath,
        frequency: data.count / sampleCount,
        type: data.type
      }))
      .sort((a, b) => b.frequency - a.frequency);
  }
}
