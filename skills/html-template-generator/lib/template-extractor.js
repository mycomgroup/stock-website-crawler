import { JSDOM } from 'jsdom';

/**
 * TemplateExtractor - Extracts structured data from HTML based on generated template
 *
 * Designed for production usage:
 * 1) stable machine-readable output
 * 2) confidence scoring for human-in-loop review
 * 3) optional manual selector overrides
 */
export class TemplateExtractor {
  constructor(options = {}) {
    this.minTextLength = options.minTextLength || 10;
  }

  extract(html, template, context = {}) {
    const dom = new JSDOM(html);
    const doc = dom.window.document;

    const overrides = template.manualOverrides || {};
    const xpaths = {
      ...template.xpaths,
      ...overrides
    };

    const title = this._extractFirstText(doc, overrides.title || xpaths.title);
    const sections = this._extractSections(doc, xpaths.sections);
    const paragraphs = this._extractParagraphs(doc, xpaths.mainContent || xpaths.sections?.xpath);
    const tables = this._extractTables(doc, xpaths.sections?.extract?.table);
    const lists = this._extractLists(doc, xpaths.sections?.extract?.list);
    const codeExamples = this._extractTexts(doc, xpaths.sections?.extract?.codeExample);

    const confidence = this._calculateConfidence({ title, sections, paragraphs, tables, lists, codeExamples });

    return {
      url: context.url || null,
      extractedAt: new Date().toISOString(),
      templateName: template.templateName,
      title,
      sections,
      paragraphs,
      tables,
      lists,
      codeExamples,
      stats: {
        sectionCount: sections.length,
        paragraphCount: paragraphs.length,
        tableCount: tables.length,
        listCount: lists.length,
        codeCount: codeExamples.length
      },
      confidence,
      needsHumanReview: confidence.score < 0.7 || confidence.missingCritical.length > 0
    };
  }

  _extractSections(doc, sectionsRule) {
    if (!sectionsRule?.xpath) return [];
    const sections = this._selectNodes(doc, sectionsRule.xpath);

    return sections.map((section, index) => {
      const heading = this._extractFirstText(section, sectionsRule.extract?.heading) || `Section ${index + 1}`;
      const description = this._extractTexts(section, sectionsRule.extract?.description).join('\n').trim();
      return {
        heading,
        description
      };
    }).filter(item => item.heading || item.description);
  }

  _extractParagraphs(doc, containerXPath) {
    if (!containerXPath) return [];
    const containers = this._selectNodes(doc, containerXPath);
    const paragraphs = [];

    for (const container of containers) {
      const nodes = this._selectNodes(container, './/p');
      for (const p of nodes) {
        const text = this._getText(p);
        if (text.length >= this.minTextLength) {
          paragraphs.push(text);
        }
      }
    }

    return Array.from(new Set(paragraphs));
  }

  _extractTables(doc, tableRule) {
    if (!tableRule) return [];
    const tableXPath = typeof tableRule === 'string' ? tableRule : tableRule.xpath;
    const tables = this._selectNodes(doc, tableXPath);

    return tables.map((table) => {
      const headerXPath = (typeof tableRule === 'object' && tableRule.headers) ? tableRule.headers : './/thead/tr/th | .//tr[1]/th';
      const rowXPath = (typeof tableRule === 'object' && tableRule.rows) ? tableRule.rows : './/tbody/tr | .//tr[position()>1]';

      const headers = this._selectNodes(table, headerXPath).map(node => this._getText(node)).filter(Boolean);
      const rows = this._selectNodes(table, rowXPath).map(row => {
        const cells = this._selectNodes(row, './/td | .//th').map(cell => this._getText(cell));
        return cells.filter(Boolean);
      }).filter(cells => cells.length > 0);

      return { headers, rows };
    }).filter(table => table.headers.length > 0 || table.rows.length > 0);
  }

  _extractLists(doc, listRule) {
    if (!listRule) return [];

    const listXPath = typeof listRule === 'string' ? listRule : listRule.xpath;
    const itemXPath = typeof listRule === 'object' && listRule.items ? listRule.items : './/li/text()';
    const lists = this._selectNodes(doc, listXPath);

    return lists.map(list => {
      const items = this._selectNodes(list, itemXPath)
        .map(node => this._getText(node))
        .filter(Boolean);
      return items;
    }).filter(items => items.length > 0);
  }

  _extractTexts(context, xpathExpr) {
    if (!xpathExpr) return [];
    return this._selectNodes(context, xpathExpr)
      .map(node => this._getText(node))
      .filter(Boolean);
  }

  _extractFirstText(context, xpathExpr) {
    const values = this._extractTexts(context, xpathExpr);
    return values[0] || '';
  }

  _calculateConfidence(payload) {
    const missingCritical = [];
    if (!payload.title) missingCritical.push('title');
    if (payload.sections.length === 0) missingCritical.push('sections');

    let score = 1;
    if (!payload.title) score -= 0.35;
    if (payload.sections.length === 0) score -= 0.35;
    if (payload.paragraphs.length === 0) score -= 0.15;
    if (payload.tables.length === 0 && payload.lists.length === 0) score -= 0.15;

    return {
      score: Math.max(0, Number(score.toFixed(2))),
      missingCritical
    };
  }

  _selectNodes(context, xpathExpr) {
    if (!xpathExpr) return [];
    try {
      const doc = context.nodeType === 9 ? context : context.ownerDocument;
      const XPathResult = doc.defaultView?.XPathResult;
      if (!XPathResult) {
        return this._selectNodesFallback(context, xpathExpr);
      }
      const result = doc.evaluate(
        xpathExpr,
        context,
        null,
        XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
        null
      );
      const nodes = [];
      for (let i = 0; i < result.snapshotLength; i++) {
        nodes.push(result.snapshotItem(i));
      }
      return nodes;
    } catch {
      return [];
    }
  }

  _selectNodesFallback(context, xpathExpr) {
    try {
      const doc = context.nodeType === 9 ? context : context.ownerDocument;
      const result = doc.evaluate(
        xpathExpr,
        context,
        null,
        7,
        null
      );
      const nodes = [];
      for (let i = 0; i < result.snapshotLength; i++) {
        nodes.push(result.snapshotItem(i));
      }
      return nodes;
    } catch {
      return [];
    }
  }

  _getText(node) {
    if (typeof node === 'string') {
      return node.replace(/\s+/g, ' ').trim();
    }
    return (node?.textContent || node?.toString?.() || '').replace(/\s+/g, ' ').trim();
  }
}

export default TemplateExtractor;
