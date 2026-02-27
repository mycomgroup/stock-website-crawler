import { readFile } from 'fs/promises';
import { JSDOM } from 'jsdom';
import xpath from 'xpath';

/**
 * TemplateRenderer - Renders HTML to Markdown using template XPath rules
 */
export class TemplateRenderer {
  /**
   * Render HTML content to Markdown using template
   * @param {string} html - HTML content to render
   * @param {Object} template - Template object with XPath rules
   * @returns {string} Rendered Markdown content
   */
  render(html, template) {
    const dom = new JSDOM(html);
    const doc = dom.window.document;
    
    let markdown = '';
    
    // Add title
    if (template.metadata?.title) {
      markdown += `# ${template.metadata.title}\n\n`;
    }
    
    // Add metadata section
    markdown += this._renderMetadata(template);
    
    // Extract content using XPath rules
    if (template.xpaths) {
      markdown += this._renderContent(doc, template.xpaths);
    }
    
    return markdown.trim() + '\n';
  }
  
  /**
   * Render metadata section
   * @param {Object} template - Template object
   * @returns {string} Markdown metadata section
   * @private
   */
  _renderMetadata(template) {
    let md = '## 模板信息\n\n';
    md += `- **模板名称**: ${template.templateName}\n`;
    
    // Try to get description from different places
    const description = template.description || 
                       template.metadata?.description || 
                       template.samples?.[0] || 
                       'N/A';
    md += `- **描述**: ${description}\n`;
    md += `- **生成时间**: ${template.generatedAt}\n`;
    md += `- **版本**: ${template.version}\n`;
    md += `- **样本数量**: ${template.metadata?.sampleCount || template.samples?.length || 0}\n`;
    md += '\n---\n\n';
    return md;
  }
  
  /**
   * Render content using XPath rules
   * @param {Document} doc - DOM document
   * @param {Object} xpaths - XPath rules object
   * @returns {string} Rendered content
   * @private
   */
  _renderContent(doc, xpaths) {
    let md = '## 提取内容\n\n';
    
    // Extract title
    if (xpaths.title) {
      const title = this._extractText(doc, xpaths.title);
      if (title) {
        md += `### ${title}\n\n`;
      }
    }
    
    // Extract sections
    if (xpaths.sections) {
      md += this._renderSections(doc, xpaths.sections);
    }
    
    // Extract main content
    if (xpaths.mainContent) {
      md += this._renderMainContent(doc, xpaths.mainContent);
    }
    
    return md;
  }
  
  /**
   * Render sections
   * @param {Document} doc - DOM document
   * @param {Object|string} sectionsRule - Sections XPath rule
   * @returns {string} Rendered sections
   * @private
   */
  _renderSections(doc, sectionsRule) {
    let md = '';
    
    // Handle string XPath (simple case)
    if (typeof sectionsRule === 'string') {
      const sections = this._selectNodes(doc, sectionsRule);
      sections.forEach((section, index) => {
        md += `### Section ${index + 1}\n\n`;
        md += this._nodeToMarkdown(section) + '\n\n';
      });
      return md;
    }
    
    // Handle object with xpath and extract rules
    if (sectionsRule.xpath) {
      const sections = this._selectNodes(doc, sectionsRule.xpath);
      
      sections.forEach((section, index) => {
        // Extract heading
        if (sectionsRule.extract?.heading) {
          const heading = this._extractText(section, sectionsRule.extract.heading);
          if (heading) {
            md += `### ${heading}\n\n`;
          } else {
            md += `### Section ${index + 1}\n\n`;
          }
        }
        
        // Extract table
        if (sectionsRule.extract?.table) {
          md += this._renderTable(section, sectionsRule.extract.table);
        }
        
        // Extract list
        if (sectionsRule.extract?.list) {
          md += this._renderList(section, sectionsRule.extract.list);
        }
        
        // Extract paragraphs
        if (sectionsRule.extract?.paragraphs) {
          const paragraphs = this._selectNodes(section, sectionsRule.extract.paragraphs);
          paragraphs.forEach(p => {
            const text = this._getTextContent(p);
            if (text) {
              md += `${text}\n\n`;
            }
          });
        }
        
        md += '\n';
      });
    }
    
    return md;
  }
  
  /**
   * Render main content
   * @param {Document} doc - DOM document
   * @param {string} contentRule - Main content XPath rule
   * @returns {string} Rendered main content
   * @private
   */
  _renderMainContent(doc, contentRule) {
    const content = this._selectNodes(doc, contentRule);
    if (content.length === 0) return '';
    
    let md = '### 主要内容\n\n';
    content.forEach(node => {
      md += this._nodeToMarkdown(node) + '\n\n';
    });
    
    return md;
  }
  
  /**
   * Render table
   * @param {Node} context - Context node
   * @param {Object|string} tableRule - Table XPath rule
   * @returns {string} Rendered table
   * @private
   */
  _renderTable(context, tableRule) {
    let md = '';
    
    const tableXPath = typeof tableRule === 'string' ? tableRule : tableRule.xpath;
    const tables = this._selectNodes(context, tableXPath);
    
    tables.forEach(table => {
      // Extract headers
      let headers = [];
      if (tableRule.headers) {
        headers = this._selectNodes(table, tableRule.headers).map(h => 
          this._getTextContent(h).trim()
        );
      } else {
        // Fallback: find headers automatically
        const headerCells = this._selectNodes(table, './/thead//th | .//tr[1]//th');
        headers = headerCells.map(h => this._getTextContent(h).trim());
      }
      
      // Extract rows
      const rowsXPath = tableRule.rows || './/tbody//tr | .//tr[position()>1]';
      const rows = this._selectNodes(table, rowsXPath);
      
      if (headers.length > 0) {
        // Render table header
        md += '| ' + headers.join(' | ') + ' |\n';
        md += '| ' + headers.map(() => '---').join(' | ') + ' |\n';
        
        // Render table rows
        rows.forEach(row => {
          const cells = this._selectNodes(row, './/td | .//th');
          const cellTexts = cells.map(cell => this._getTextContent(cell).trim());
          md += '| ' + cellTexts.join(' | ') + ' |\n';
        });
        
        md += '\n';
      }
    });
    
    return md;
  }
  
  /**
   * Render list
   * @param {Node} context - Context node
   * @param {string} listRule - List XPath rule
   * @returns {string} Rendered list
   * @private
   */
  _renderList(context, listRule) {
    let md = '';
    
    const lists = this._selectNodes(context, listRule);
    lists.forEach(list => {
      const items = this._selectNodes(list, './/li');
      items.forEach(item => {
        const text = this._getTextContent(item).trim();
        if (text) {
          md += `- ${text}\n`;
        }
      });
      md += '\n';
    });
    
    return md;
  }
  
  /**
   * Convert DOM node to Markdown
   * @param {Node} node - DOM node
   * @returns {string} Markdown text
   * @private
   */
  _nodeToMarkdown(node) {
    const tagName = node.tagName?.toLowerCase();
    
    switch (tagName) {
      case 'h1':
        return `# ${this._getTextContent(node)}`;
      case 'h2':
        return `## ${this._getTextContent(node)}`;
      case 'h3':
        return `### ${this._getTextContent(node)}`;
      case 'h4':
        return `#### ${this._getTextContent(node)}`;
      case 'p':
        return this._getTextContent(node);
      case 'ul':
      case 'ol':
        return this._renderList(node.parentNode, `./*[local-name()='${tagName}']`);
      case 'table':
        return this._renderTable(node.parentNode, `./*[local-name()='table']`);
      default:
        return this._getTextContent(node);
    }
  }
  
  /**
   * Extract text using XPath
   * @param {Node} context - Context node
   * @param {string} xpathExpr - XPath expression
   * @returns {string} Extracted text
   * @private
   */
  _extractText(context, xpathExpr) {
    try {
      const result = xpath.select(xpathExpr, context);
      if (Array.isArray(result) && result.length > 0) {
        return result[0].textContent?.trim() || result[0].toString().trim();
      }
      return '';
    } catch (error) {
      console.warn(`XPath error: ${error.message}`);
      return '';
    }
  }
  
  /**
   * Select nodes using XPath
   * @param {Node} context - Context node
   * @param {string} xpathExpr - XPath expression
   * @returns {Array} Selected nodes
   * @private
   */
  _selectNodes(context, xpathExpr) {
    try {
      const result = xpath.select(xpathExpr, context);
      return Array.isArray(result) ? result : [];
    } catch (error) {
      console.warn(`XPath error: ${error.message}`);
      return [];
    }
  }
  
  /**
   * Get text content from node
   * @param {Node} node - DOM node
   * @returns {string} Text content
   * @private
   */
  _getTextContent(node) {
    return node.textContent?.trim() || '';
  }
  
  /**
   * Load template from file
   * @param {string} templatePath - Path to template JSON file
   * @returns {Promise<Object>} Template object
   */
  async loadTemplate(templatePath) {
    const content = await readFile(templatePath, 'utf-8');
    return JSON.parse(content);
  }
}
