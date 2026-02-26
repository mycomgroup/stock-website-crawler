/**
 * TemplateContentAnalyzer - 模板内容分析器
 * 
 * 职责：分析markdown页面内容，识别模板内容和独特数据
 */

const fs = require('fs').promises;
const path = require('path');

class TemplateContentAnalyzer {
  constructor() {
    this.blockTypes = {
      HEADING: 'heading',
      PARAGRAPH: 'paragraph',
      TABLE: 'table',
      CODE: 'code',
      LIST: 'list'
    };
    
    // 缓存：文本标准化结果
    this.normalizeCache = new Map();
    // 缓存：内容块提取结果
    this.blockCache = new Map();
  }
  
  /**
   * 清除缓存
   */
  clearCache() {
    this.normalizeCache.clear();
    this.blockCache.clear();
  }

  /**
   * 批量加载markdown页面
   * @param {Array<string>} filePaths - markdown文件路径数组
   * @param {Object} options - 选项
   * @param {number} options.batchSize - 批次大小，默认100
   * @returns {AsyncGenerator<Array<Object>>} 异步生成器，每次yield一批页面数据
   */
  async *loadMarkdownPages(filePaths, options = {}) {
    const batchSize = options.batchSize || 100;
    
    for (let i = 0; i < filePaths.length; i += batchSize) {
      const batch = filePaths.slice(i, i + batchSize);
      const pages = [];
      
      for (const filePath of batch) {
        try {
          const content = await fs.readFile(filePath, 'utf-8');
          pages.push({
            filePath,
            fileName: path.basename(filePath),
            content,
            size: content.length
          });
        } catch (error) {
          console.warn(`Failed to read file ${filePath}:`, error.message);
          // 继续处理其他文件
        }
      }
      
      yield pages;
    }
  }

  /**
   * 匹配URL和markdown文件
   * @param {Object} urlPattern - URL模式对象
   * @param {string} pagesDir - pages目录路径
   * @returns {Promise<Array<string>>} 匹配的文件路径数组
   */
  async matchPagesToURLs(urlPattern, pagesDir) {
    try {
      // 读取pages目录下的所有.md文件
      const allFiles = await this._getAllMarkdownFiles(pagesDir);
      
      // 根据URL模式匹配文件
      const matchedFiles = [];
      const pattern = new RegExp(urlPattern.pattern);
      
      for (const file of allFiles) {
        // 从文件名或内容中提取URL信息进行匹配
        // 简化版本：基于文件名匹配
        const fileName = path.basename(file, '.md');
        
        // 检查文件名是否包含模式的关键部分
        if (this._fileMatchesPattern(fileName, urlPattern)) {
          matchedFiles.push(file);
        }
      }
      
      return matchedFiles;
    } catch (error) {
      console.error(`Failed to match pages to URLs:`, error.message);
      return [];
    }
  }

  /**
   * 递归获取目录下所有markdown文件
   * @private
   */
  async _getAllMarkdownFiles(dir) {
    const files = [];
    
    try {
      const entries = await fs.readdir(dir, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        
        if (entry.isDirectory()) {
          // 递归读取子目录
          const subFiles = await this._getAllMarkdownFiles(fullPath);
          files.push(...subFiles);
        } else if (entry.isFile() && entry.name.endsWith('.md')) {
          files.push(fullPath);
        }
      }
    } catch (error) {
      console.warn(`Failed to read directory ${dir}:`, error.message);
    }
    
    return files;
  }

  /**
   * 检查文件名是否匹配URL模式
   * @private
   */
  _fileMatchesPattern(fileName, urlPattern) {
    // 提取pathTemplate的关键部分
    const templateParts = urlPattern.pathTemplate
      .split('/')
      .filter(part => part && !part.startsWith('{'));
    
    // 如果没有关键部分，使用name
    if (templateParts.length === 0 && urlPattern.name) {
      templateParts.push(urlPattern.name);
    }
    
    // 检查文件名是否包含所有关键部分
    const normalizedFileName = fileName.toLowerCase().replace(/[_\-\s]/g, '');
    
    return templateParts.some(part => {
      const normalizedPart = part.toLowerCase().replace(/[_\-\s]/g, '');
      return normalizedFileName.includes(normalizedPart);
    });
  }

  /**
   * 提取内容块（带缓存）
   * @param {string} markdownContent - Markdown内容
   * @returns {Array<Object>} 内容块数组
   */
  extractContentBlocks(markdownContent) {
    // 生成缓存键（使用内容的哈希或前100字符）
    const cacheKey = markdownContent.substring(0, 100);
    
    // 检查缓存
    if (this.blockCache.has(cacheKey)) {
      const cached = this.blockCache.get(cacheKey);
      // 验证完整内容是否匹配
      if (cached.fullContent === markdownContent) {
        return cached.blocks;
      }
    }
    
    // 提取内容块
    const blocks = this._extractContentBlocksImpl(markdownContent);
    
    // 存入缓存（限制缓存大小）
    if (this.blockCache.size > 1000) {
      // 清除最旧的缓存项
      const firstKey = this.blockCache.keys().next().value;
      this.blockCache.delete(firstKey);
    }
    
    this.blockCache.set(cacheKey, {
      fullContent: markdownContent,
      blocks
    });
    
    return blocks;
  }
  
  /**
   * 提取内容块的实际实现
   * @private
   * @param {string} markdownContent - Markdown内容
   * @returns {Array<Object>} 内容块数组
   */
  _extractContentBlocksImpl(markdownContent) {
    const blocks = [];
    const lines = markdownContent.split('\n');
    let i = 0;

    while (i < lines.length) {
      const line = lines[i];

      // 跳过空行
      if (line.trim() === '') {
        i++;
        continue;
      }

      // 标题 (## xxx)
      if (line.match(/^#{1,6}\s+/)) {
        blocks.push({
          type: this.blockTypes.HEADING,
          content: line.trim(),
          lineNumber: i + 1
        });
        i++;
        continue;
      }

      // 表格 (| xxx |)
      if (line.trim().startsWith('|')) {
        const tableBlock = this._extractTable(lines, i);
        if (tableBlock) {
          blocks.push(tableBlock);
          i = tableBlock.endLine;
          continue;
        }
      }

      // 代码块 (```xxx```)
      if (line.trim().startsWith('```')) {
        const codeBlock = this._extractCodeBlock(lines, i);
        if (codeBlock) {
          blocks.push(codeBlock);
          i = codeBlock.endLine;
          continue;
        }
      }

      // 列表 (- xxx 或 1. xxx)
      if (line.match(/^(\s*[-*+]\s+|\s*\d+\.\s+)/)) {
        const listBlock = this._extractList(lines, i);
        if (listBlock) {
          blocks.push(listBlock);
          i = listBlock.endLine;
          continue;
        }
      }

      // 段落（连续的文本行）
      const paragraphBlock = this._extractParagraph(lines, i);
      if (paragraphBlock) {
        blocks.push(paragraphBlock);
        i = paragraphBlock.endLine;
        continue;
      }

      i++;
    }

    return blocks;
  }

  /**
   * 提取表格
   * @private
   */
  _extractTable(lines, startIndex) {
    const tableLines = [];
    let i = startIndex;

    while (i < lines.length && lines[i].trim().startsWith('|')) {
      tableLines.push(lines[i].trim());
      i++;
    }

    if (tableLines.length === 0) {
      return null;
    }

    return {
      type: this.blockTypes.TABLE,
      content: tableLines.join('\n'),
      lineNumber: startIndex + 1,
      endLine: i,
      rows: tableLines.length
    };
  }

  /**
   * 提取代码块
   * @private
   */
  _extractCodeBlock(lines, startIndex) {
    const codeLines = [lines[startIndex]];
    let i = startIndex + 1;

    // 查找结束的```
    while (i < lines.length) {
      codeLines.push(lines[i]);
      if (lines[i].trim().startsWith('```')) {
        i++;
        break;
      }
      i++;
    }

    return {
      type: this.blockTypes.CODE,
      content: codeLines.join('\n'),
      lineNumber: startIndex + 1,
      endLine: i,
      language: lines[startIndex].trim().substring(3).trim()
    };
  }

  /**
   * 提取列表
   * @private
   */
  _extractList(lines, startIndex) {
    const listLines = [];
    let i = startIndex;
    const firstIndent = lines[i].match(/^\s*/)[0].length;

    while (i < lines.length) {
      const line = lines[i];
      const currentIndent = line.match(/^\s*/)[0].length;

      // 列表项或缩进的内容
      if (line.match(/^(\s*[-*+]\s+|\s*\d+\.\s+)/) || 
          (currentIndent > firstIndent && line.trim() !== '')) {
        listLines.push(line);
        i++;
      } else if (line.trim() === '') {
        // 空行，检查下一行是否还是列表
        if (i + 1 < lines.length && 
            lines[i + 1].match(/^(\s*[-*+]\s+|\s*\d+\.\s+)/)) {
          listLines.push(line);
          i++;
        } else {
          break;
        }
      } else {
        break;
      }
    }

    return {
      type: this.blockTypes.LIST,
      content: listLines.join('\n'),
      lineNumber: startIndex + 1,
      endLine: i,
      items: listLines.filter(l => l.match(/^(\s*[-*+]\s+|\s*\d+\.\s+)/)).length
    };
  }

  /**
   * 提取段落
   * @private
   */
  _extractParagraph(lines, startIndex) {
    const paragraphLines = [];
    let i = startIndex;

    while (i < lines.length) {
      const line = lines[i];

      // 遇到空行、标题、表格、代码块、列表则停止
      if (line.trim() === '' ||
          line.match(/^#{1,6}\s+/) ||
          line.trim().startsWith('|') ||
          line.trim().startsWith('```') ||
          line.match(/^(\s*[-*+]\s+|\s*\d+\.\s+)/)) {
        break;
      }

      paragraphLines.push(line);
      i++;
    }

    if (paragraphLines.length === 0) {
      return null;
    }

    return {
      type: this.blockTypes.PARAGRAPH,
      content: paragraphLines.join('\n'),
      lineNumber: startIndex + 1,
      endLine: i
    };
  }

  /**
   * 文本标准化（用于比较，带缓存）
   * @param {string} text - 原始文本
   * @returns {string} 标准化后的文本
   */
  normalizeText(text) {
    // 检查缓存
    if (this.normalizeCache.has(text)) {
      return this.normalizeCache.get(text);
    }
    
    // 标准化文本
    const normalized = text
      .toLowerCase()
      .replace(/\s+/g, ' ')
      .replace(/[^\w\s\u4e00-\u9fa5]/g, '') // 保留中文字符
      .trim();
    
    // 存入缓存（限制缓存大小）
    if (this.normalizeCache.size > 5000) {
      // 清除最旧的缓存项
      const firstKey = this.normalizeCache.keys().next().value;
      this.normalizeCache.delete(firstKey);
    }
    
    this.normalizeCache.set(text, normalized);
    
    return normalized;
  }

  /**
   * 计算内容频率（优化：并行处理）
   * @param {Array<string>} pages - 页面内容数组
   * @param {Object} options - 选项
   * @param {number} options.parallel - 并行度，默认4
   * @returns {Map} 内容块频率映射
   */
  calculateFrequency(pages, options = {}) {
    const parallel = options.parallel || 4;
    const blockFrequency = new Map();

    // 如果页面数量较少，直接处理
    if (pages.length <= parallel) {
      return this._calculateFrequencySerial(pages);
    }

    // 将页面分成多个批次并行处理
    const batchSize = Math.ceil(pages.length / parallel);
    const batches = [];
    
    for (let i = 0; i < pages.length; i += batchSize) {
      batches.push(pages.slice(i, i + batchSize));
    }

    // 并行处理每个批次
    const batchResults = batches.map(batch => this._calculateFrequencySerial(batch));

    // 合并结果
    for (const batchFreq of batchResults) {
      batchFreq.forEach((data, key) => {
        if (blockFrequency.has(key)) {
          const existing = blockFrequency.get(key);
          existing.count += data.count;
          existing.pages.push(...data.pages);
        } else {
          blockFrequency.set(key, data);
        }
      });
    }

    return blockFrequency;
  }

  /**
   * 串行计算内容频率
   * @private
   * @param {Array<string>} pages - 页面内容数组
   * @returns {Map} 内容块频率映射
   */
  _calculateFrequencySerial(pages) {
    const blockFrequency = new Map();

    pages.forEach((page, pageIndex) => {
      const blocks = this.extractContentBlocks(page);
      const seenInThisPage = new Set(); // 避免同一页面重复计数

      blocks.forEach(block => {
        const normalized = this.normalizeText(block.content);
        const key = `${block.type}:${normalized}`;

        // 只在每个页面中计数一次
        if (!seenInThisPage.has(key)) {
          const current = blockFrequency.get(key) || {
            type: block.type,
            content: block.content,
            normalizedContent: normalized,
            count: 0,
            pages: []
          };

          current.count++;
          current.pages.push(pageIndex);
          blockFrequency.set(key, current);
          seenInThisPage.add(key);
        }
      });
    });

    return blockFrequency;
  }

  /**
   * 分类内容
   * @param {Map} frequency - 频率映射
   * @param {number} totalPages - 总页面数
   * @param {Object} thresholds - 阈值配置
   * @returns {Object} 分类结果
   */
  classifyContent(frequency, totalPages, thresholds = { template: 0.8, unique: 0.2 }) {
    const result = {
      template: [],  // 高频 >80%
      unique: [],    // 低频 <20%
      mixed: []      // 中频 20-80%
    };

    frequency.forEach((data, key) => {
      const ratio = data.count / totalPages;
      const item = {
        type: data.type,
        content: data.content,
        normalizedContent: data.normalizedContent,
        count: data.count,
        ratio: ratio,
        pages: data.pages
      };

      if (ratio > thresholds.template) {
        result.template.push(item);
      } else if (ratio < thresholds.unique) {
        result.unique.push(item);
      } else {
        result.mixed.push(item);
      }
    });

    // 按频率降序排序
    result.template.sort((a, b) => b.ratio - a.ratio);
    result.unique.sort((a, b) => a.ratio - b.ratio);
    result.mixed.sort((a, b) => b.ratio - a.ratio);

    return result;
  }

  /**
   * 识别表格结构（优化：并行处理）
   * @param {Array<string>} pages - 页面内容数组
   * @param {Object} options - 选项
   * @param {number} options.parallel - 并行度，默认4
   * @returns {Array<Object>} 表格结构数组
   */
  identifyTableStructures(pages, options = {}) {
    const parallel = options.parallel || 4;
    const tableStructures = new Map();

    // 如果页面数量较少，直接处理
    if (pages.length <= parallel) {
      return this._identifyTableStructuresSerial(pages);
    }

    // 将页面分成多个批次并行处理
    const batchSize = Math.ceil(pages.length / parallel);
    const batches = [];
    
    for (let i = 0; i < pages.length; i += batchSize) {
      batches.push({
        pages: pages.slice(i, i + batchSize),
        offset: i
      });
    }

    // 并行处理每个批次
    const batchResults = batches.map(batch => 
      this._identifyTableStructuresBatch(batch.pages, batch.offset)
    );

    // 合并结果
    for (const batchTables of batchResults) {
      batchTables.forEach((tableData, key) => {
        if (tableStructures.has(key)) {
          const existing = tableStructures.get(key);
          existing.occurrences += tableData.occurrences;
          existing.pages.push(...tableData.pages);
        } else {
          tableStructures.set(key, tableData);
        }
      });
    }

    // 转换为数组并按出现次数排序
    return Array.from(tableStructures.values())
      .sort((a, b) => b.occurrences - a.occurrences);
  }

  /**
   * 串行识别表格结构
   * @private
   * @param {Array<string>} pages - 页面内容数组
   * @returns {Array<Object>} 表格结构数组
   */
  _identifyTableStructuresSerial(pages) {
    const tableStructures = new Map();

    pages.forEach((page, pageIndex) => {
      const blocks = this.extractContentBlocks(page);
      
      blocks.forEach(block => {
        if (block.type === this.blockTypes.TABLE) {
          const structure = this._analyzeTableStructure(block.content);
          if (structure) {
            const key = this._getTableStructureKey(structure);
            
            if (!tableStructures.has(key)) {
              tableStructures.set(key, {
                columns: structure.columns,
                columnCount: structure.columnCount,
                rowCount: structure.rowCount,
                hasHeader: structure.hasHeader,
                occurrences: 0,
                pages: []
              });
            }
            
            const tableData = tableStructures.get(key);
            tableData.occurrences++;
            tableData.pages.push(pageIndex);
          }
        }
      });
    });

    // 转换为数组并按出现次数排序
    return Array.from(tableStructures.values())
      .sort((a, b) => b.occurrences - a.occurrences);
  }

  /**
   * 批次识别表格结构
   * @private
   * @param {Array<string>} pages - 页面内容数组
   * @param {number} offset - 页面索引偏移量
   * @returns {Map} 表格结构映射
   */
  _identifyTableStructuresBatch(pages, offset) {
    const tableStructures = new Map();

    pages.forEach((page, batchIndex) => {
      const pageIndex = offset + batchIndex;
      const blocks = this.extractContentBlocks(page);
      
      blocks.forEach(block => {
        if (block.type === this.blockTypes.TABLE) {
          const structure = this._analyzeTableStructure(block.content);
          if (structure) {
            const key = this._getTableStructureKey(structure);
            
            if (!tableStructures.has(key)) {
              tableStructures.set(key, {
                columns: structure.columns,
                columnCount: structure.columnCount,
                rowCount: structure.rowCount,
                hasHeader: structure.hasHeader,
                occurrences: 0,
                pages: []
              });
            }
            
            const tableData = tableStructures.get(key);
            tableData.occurrences++;
            tableData.pages.push(pageIndex);
          }
        }
      });
    });

    return tableStructures;
  }

  /**
   * 分析表格结构
   * @private
   */
  _analyzeTableStructure(tableContent) {
    const lines = tableContent.split('\n').filter(line => line.trim());
    
    if (lines.length < 2) {
      return null;
    }

    // 解析表头
    const headerLine = lines[0];
    const columns = headerLine
      .split('|')
      .map(col => col.trim())
      .filter(col => col !== '');

    // 检查是否有分隔行
    const hasHeader = lines.length > 1 && lines[1].includes('---');
    
    // 计算行数（排除表头和分隔行）
    const rowCount = hasHeader ? lines.length - 2 : lines.length - 1;

    return {
      columns,
      columnCount: columns.length,
      rowCount,
      hasHeader
    };
  }

  /**
   * 生成表格结构的唯一键
   * @private
   */
  _getTableStructureKey(structure) {
    // 使用列名和列数作为键
    const normalizedColumns = structure.columns
      .map(col => this.normalizeText(col))
      .join('|');
    return `${structure.columnCount}:${normalizedColumns}`;
  }

  /**
   * 识别代码块（优化：并行处理）
   * @param {Array<string>} pages - 页面内容数组
   * @param {Object} options - 选项
   * @param {number} options.parallel - 并行度，默认4
   * @returns {Array<Object>} 代码块结构数组
   */
  identifyCodeBlocks(pages, options = {}) {
    const parallel = options.parallel || 4;
    const codeBlockStructures = new Map();

    // 如果页面数量较少，直接处理
    if (pages.length <= parallel) {
      return this._identifyCodeBlocksSerial(pages);
    }

    // 将页面分成多个批次并行处理
    const batchSize = Math.ceil(pages.length / parallel);
    const batches = [];
    
    for (let i = 0; i < pages.length; i += batchSize) {
      batches.push({
        pages: pages.slice(i, i + batchSize),
        offset: i
      });
    }

    // 并行处理每个批次
    const batchResults = batches.map(batch => 
      this._identifyCodeBlocksBatch(batch.pages, batch.offset)
    );

    // 合并结果
    for (const batchCodes of batchResults) {
      batchCodes.forEach((codeData, key) => {
        if (codeBlockStructures.has(key)) {
          const existing = codeBlockStructures.get(key);
          existing.occurrences += codeData.occurrences;
          existing.pages.push(...codeData.pages);
          existing.totalLength += codeData.totalLength;
          existing.avgLength = Math.round(existing.totalLength / existing.occurrences);
        } else {
          codeBlockStructures.set(key, codeData);
        }
      });
    }

    // 转换为数组并按出现次数排序
    return Array.from(codeBlockStructures.values())
      .sort((a, b) => b.occurrences - a.occurrences);
  }

  /**
   * 串行识别代码块
   * @private
   * @param {Array<string>} pages - 页面内容数组
   * @returns {Array<Object>} 代码块结构数组
   */
  _identifyCodeBlocksSerial(pages) {
    const codeBlockStructures = new Map();

    pages.forEach((page, pageIndex) => {
      const blocks = this.extractContentBlocks(page);
      
      blocks.forEach(block => {
        if (block.type === this.blockTypes.CODE) {
          const structure = this._analyzeCodeBlockStructure(block);
          const key = structure.language || 'unknown';
          
          if (!codeBlockStructures.has(key)) {
            codeBlockStructures.set(key, {
              language: structure.language,
              occurrences: 0,
              pages: [],
              avgLength: 0,
              totalLength: 0
            });
          }
          
          const codeData = codeBlockStructures.get(key);
          codeData.occurrences++;
          codeData.pages.push(pageIndex);
          codeData.totalLength += structure.length;
          codeData.avgLength = Math.round(codeData.totalLength / codeData.occurrences);
        }
      });
    });

    // 转换为数组并按出现次数排序
    return Array.from(codeBlockStructures.values())
      .sort((a, b) => b.occurrences - a.occurrences);
  }

  /**
   * 批次识别代码块
   * @private
   * @param {Array<string>} pages - 页面内容数组
   * @param {number} offset - 页面索引偏移量
   * @returns {Map} 代码块结构映射
   */
  _identifyCodeBlocksBatch(pages, offset) {
    const codeBlockStructures = new Map();

    pages.forEach((page, batchIndex) => {
      const pageIndex = offset + batchIndex;
      const blocks = this.extractContentBlocks(page);
      
      blocks.forEach(block => {
        if (block.type === this.blockTypes.CODE) {
          const structure = this._analyzeCodeBlockStructure(block);
          const key = structure.language || 'unknown';
          
          if (!codeBlockStructures.has(key)) {
            codeBlockStructures.set(key, {
              language: structure.language,
              occurrences: 0,
              pages: [],
              avgLength: 0,
              totalLength: 0
            });
          }
          
          const codeData = codeBlockStructures.get(key);
          codeData.occurrences++;
          codeData.pages.push(pageIndex);
          codeData.totalLength += structure.length;
          codeData.avgLength = Math.round(codeData.totalLength / codeData.occurrences);
        }
      });
    });

    return codeBlockStructures;
  }

  /**
   * 分析代码块结构
   * @private
   */
  _analyzeCodeBlockStructure(block) {
    const lines = block.content.split('\n');
    
    // 提取语言标识（第一行的```后面的内容）
    let language = block.language || '';
    
    // 如果没有语言标识，尝试从内容推断
    if (!language && lines.length > 1) {
      const content = lines.slice(1, -1).join('\n');
      language = this._inferLanguage(content);
    }

    // 计算代码长度（排除```行）
    const codeLines = lines.slice(1, -1);
    const length = codeLines.join('\n').length;

    return {
      language: language || 'unknown',
      length,
      lineCount: codeLines.length
    };
  }

  /**
   * 推断代码语言
   * @private
   */
  _inferLanguage(content) {
    // 简单的语言推断规则
    if (content.includes('function') || content.includes('const') || content.includes('let')) {
      return 'javascript';
    }
    if (content.includes('def ') || content.includes('import ')) {
      return 'python';
    }
    if (content.includes('{') && content.includes('}') && content.includes('"')) {
      return 'json';
    }
    if (content.includes('curl') || content.includes('http://') || content.includes('https://')) {
      return 'bash';
    }
    return 'unknown';
  }

  /**
   * 识别列表（优化：并行处理）
   * @param {Array<string>} pages - 页面内容数组
   * @param {Object} options - 选项
   * @param {number} options.parallel - 并行度，默认4
   * @returns {Array<Object>} 列表结构数组
   */
  identifyLists(pages, options = {}) {
    const parallel = options.parallel || 4;
    const listStructures = new Map();

    // 如果页面数量较少，直接处理
    if (pages.length <= parallel) {
      return this._identifyListsSerial(pages);
    }

    // 将页面分成多个批次并行处理
    const batchSize = Math.ceil(pages.length / parallel);
    const batches = [];
    
    for (let i = 0; i < pages.length; i += batchSize) {
      batches.push({
        pages: pages.slice(i, i + batchSize),
        offset: i
      });
    }

    // 并行处理每个批次
    const batchResults = batches.map(batch => 
      this._identifyListsBatch(batch.pages, batch.offset)
    );

    // 合并结果
    for (const batchLists of batchResults) {
      batchLists.forEach((listData, key) => {
        if (listStructures.has(key)) {
          const existing = listStructures.get(key);
          existing.occurrences += listData.occurrences;
          existing.pages.push(...listData.pages);
        } else {
          listStructures.set(key, listData);
        }
      });
    }

    // 转换为数组并按出现次数排序
    return Array.from(listStructures.values())
      .sort((a, b) => b.occurrences - a.occurrences);
  }

  /**
   * 串行识别列表
   * @private
   * @param {Array<string>} pages - 页面内容数组
   * @returns {Array<Object>} 列表结构数组
   */
  _identifyListsSerial(pages) {
    const listStructures = new Map();

    pages.forEach((page, pageIndex) => {
      const blocks = this.extractContentBlocks(page);
      
      blocks.forEach(block => {
        if (block.type === this.blockTypes.LIST) {
          const structure = this._analyzeListStructure(block);
          const key = `${structure.listType}:${structure.itemCount}`;
          
          if (!listStructures.has(key)) {
            listStructures.set(key, {
              listType: structure.listType,
              itemCount: structure.itemCount,
              hasNesting: structure.hasNesting,
              occurrences: 0,
              pages: []
            });
          }
          
          const listData = listStructures.get(key);
          listData.occurrences++;
          listData.pages.push(pageIndex);
        }
      });
    });

    // 转换为数组并按出现次数排序
    return Array.from(listStructures.values())
      .sort((a, b) => b.occurrences - a.occurrences);
  }

  /**
   * 批次识别列表
   * @private
   * @param {Array<string>} pages - 页面内容数组
   * @param {number} offset - 页面索引偏移量
   * @returns {Map} 列表结构映射
   */
  _identifyListsBatch(pages, offset) {
    const listStructures = new Map();

    pages.forEach((page, batchIndex) => {
      const pageIndex = offset + batchIndex;
      const blocks = this.extractContentBlocks(page);
      
      blocks.forEach(block => {
        if (block.type === this.blockTypes.LIST) {
          const structure = this._analyzeListStructure(block);
          const key = `${structure.listType}:${structure.itemCount}`;
          
          if (!listStructures.has(key)) {
            listStructures.set(key, {
              listType: structure.listType,
              itemCount: structure.itemCount,
              hasNesting: structure.hasNesting,
              occurrences: 0,
              pages: []
            });
          }
          
          const listData = listStructures.get(key);
          listData.occurrences++;
          listData.pages.push(pageIndex);
        }
      });
    });

    return listStructures;
  }

  /**
   * 分析列表结构
   * @private
   */
  _analyzeListStructure(block) {
    const lines = block.content.split('\n').filter(line => line.trim());
    
    // 判断列表类型
    const firstLine = lines[0];
    const isOrdered = /^\s*\d+\.\s+/.test(firstLine);
    const listType = isOrdered ? 'ordered' : 'unordered';
    
    // 计算项目数量
    const itemCount = block.items || lines.filter(line => 
      /^(\s*[-*+]\s+|\s*\d+\.\s+)/.test(line)
    ).length;
    
    // 检查是否有嵌套
    const indents = lines
      .filter(line => /^(\s*[-*+]\s+|\s*\d+\.\s+)/.test(line))
      .map(line => line.match(/^\s*/)[0].length);
    const hasNesting = new Set(indents).size > 1;

    return {
      listType,
      itemCount,
      hasNesting
    };
  }

  /**
   * 识别噪音模式
   * @param {Array<Object>} templateContent - 高频模板内容数组
   * @param {Object} options - 选项
   * @returns {Array<Object>} 噪音模式数组
   */
  identifyNoisePatterns(templateContent, options = {}) {
    const minRatio = options.minRatio || 0.9; // 默认90%以上才认为是噪音
    const maxPatternLength = options.maxPatternLength || 100; // 模式最大长度
    
    const noisePatterns = [];

    templateContent.forEach(item => {
      // 只处理高频内容（>90%）
      if (item.ratio < minRatio) {
        return;
      }

      // 生成匹配模式
      let pattern = item.normalizedContent || this.normalizeText(item.content);
      
      // 截断过长的模式
      if (pattern.length > maxPatternLength) {
        pattern = pattern.substring(0, maxPatternLength);
      }

      // 转义正则表达式特殊字符
      pattern = this._escapeRegex(pattern);

      noisePatterns.push({
        type: item.type,
        pattern,
        originalContent: item.content.substring(0, 100), // 保留原始内容的前100字符
        ratio: item.ratio,
        count: item.count,
        reason: `Template noise (${(item.ratio * 100).toFixed(0)}% frequency)`
      });
    });

    return noisePatterns;
  }

  /**
   * 识别数据模式
   * @param {Array<Object>} uniqueContent - 低频独特内容数组
   * @param {Object} dataStructures - 数据结构信息
   * @param {Object} options - 选项
   * @returns {Array<Object>} 数据模式数组
   */
  identifyDataPatterns(uniqueContent, dataStructures, options = {}) {
    const maxRatio = options.maxRatio || 0.2; // 默认20%以下才认为是独特数据
    
    const dataPatterns = [];

    // 1. 从独特内容中识别数据模式
    uniqueContent.forEach(item => {
      // 只处理低频内容（<20%）
      if (item.ratio > maxRatio) {
        return;
      }

      dataPatterns.push({
        type: item.type,
        contentType: this._inferContentType(item.content, item.type),
        ratio: item.ratio,
        count: item.count,
        sample: item.content.substring(0, 100), // 保留样例的前100字符
        reason: `Unique data (${(item.ratio * 100).toFixed(0)}% frequency)`
      });
    });

    // 2. 从数据结构中识别模式
    if (dataStructures.tables && dataStructures.tables.length > 0) {
      dataStructures.tables.forEach(table => {
        dataPatterns.push({
          type: 'table',
          contentType: 'structured_data',
          columns: table.columns,
          columnCount: table.columnCount,
          occurrences: table.occurrences,
          reason: 'Structured table data'
        });
      });
    }

    if (dataStructures.codeBlocks && dataStructures.codeBlocks.length > 0) {
      dataStructures.codeBlocks.forEach(code => {
        dataPatterns.push({
          type: 'code',
          contentType: 'code_snippet',
          language: code.language,
          occurrences: code.occurrences,
          avgLength: code.avgLength,
          reason: 'Code snippet or API example'
        });
      });
    }

    if (dataStructures.lists && dataStructures.lists.length > 0) {
      dataStructures.lists.forEach(list => {
        dataPatterns.push({
          type: 'list',
          contentType: 'list_data',
          listType: list.listType,
          itemCount: list.itemCount,
          occurrences: list.occurrences,
          reason: 'List data'
        });
      });
    }

    return dataPatterns;
  }

  /**
   * 生成清洗规则
   * @param {Object} classified - 分类后的内容
   * @param {Object} dataStructures - 数据结构信息
   * @param {Object} options - 选项
   * @returns {Object} 清洗规则
   */
  generateCleaningRules(classified, dataStructures, options = {}) {
    // 1. 识别噪音模式
    const noisePatterns = this.identifyNoisePatterns(classified.template, options);

    // 2. 识别数据模式
    const dataPatterns = this.identifyDataPatterns(classified.unique, dataStructures, options);

    // 3. 生成移除规则（基于噪音模式）
    const removePatterns = noisePatterns.map(noise => ({
      type: 'remove',
      target: noise.type,
      pattern: noise.pattern,
      reason: noise.reason,
      frequency: noise.ratio
    }));

    // 4. 生成保留规则（基于数据模式）
    const keepPatterns = dataPatterns
      .filter(data => data.contentType && data.contentType !== 'unknown')
      .map(data => ({
        type: 'keep',
        target: data.type,
        contentType: data.contentType,
        reason: data.reason,
        frequency: data.ratio
      }));

    // 5. 生成移除元素规则（基于高频标题和导航）
    const removeElements = [];
    classified.template.forEach(item => {
      if (item.type === 'heading' && item.ratio > 0.95) {
        // 高频标题通常是导航或模板标题
        const headingText = item.content.replace(/^#+\s*/, '').trim();
        if (headingText.length > 0 && headingText.length < 50) {
          removeElements.push({
            type: 'heading',
            text: headingText,
            reason: `Template heading (${(item.ratio * 100).toFixed(0)}% frequency)`
          });
        }
      }
    });

    return {
      removePatterns,
      keepPatterns,
      removeElements,
      summary: {
        totalNoisePatterns: noisePatterns.length,
        totalDataPatterns: dataPatterns.length,
        totalRemoveRules: removePatterns.length,
        totalKeepRules: keepPatterns.length,
        totalRemoveElements: removeElements.length
      }
    };
  }

  /**
   * 转义正则表达式特殊字符
   * @private
   */
  _escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  /**
   * 推断内容类型
   * @private
   */
  _inferContentType(content, blockType) {
    const normalized = content.toLowerCase();

    // 根据内容特征推断类型
    if (blockType === 'table') {
      return 'structured_data';
    }

    if (blockType === 'code') {
      if (normalized.includes('http://') || normalized.includes('https://')) {
        return 'api_endpoint';
      }
      if (normalized.includes('{') && normalized.includes('}')) {
        return 'json_data';
      }
      return 'code_snippet';
    }

    if (blockType === 'heading') {
      return 'section_title';
    }

    if (blockType === 'paragraph') {
      // 检查是否包含特定关键词
      if (normalized.includes('参数') || normalized.includes('parameter')) {
        return 'parameter_description';
      }
      if (normalized.includes('返回') || normalized.includes('response')) {
        return 'response_description';
      }
      if (normalized.includes('示例') || normalized.includes('example')) {
        return 'example_description';
      }
      return 'text_content';
    }

    if (blockType === 'list') {
      return 'list_data';
    }

    return 'unknown';
  }

  /**
   * 分析模板（完整流程，优化：支持并行处理）
   * @param {Array<string>} pages - 页面内容数组
   * @param {Object} options - 选项
   * @param {Object} options.thresholds - 阈值配置
   * @param {number} options.parallel - 并行度，默认4
   * @returns {Object} 分析结果
   */
  analyzeTemplate(pages, options = {}) {
    const thresholds = options.thresholds || { template: 0.8, unique: 0.2 };
    const parallel = options.parallel || 4;

    // 1. 计算频率（并行）
    const frequency = this.calculateFrequency(pages, { parallel });

    // 2. 分类内容
    const classified = this.classifyContent(frequency, pages.length, thresholds);

    // 3. 识别数据结构（并行）
    const dataStructures = {
      tables: this.identifyTableStructures(pages, { parallel }),
      codeBlocks: this.identifyCodeBlocks(pages, { parallel }),
      lists: this.identifyLists(pages, { parallel })
    };

    // 4. 生成清洗规则
    const cleaningRules = this.generateCleaningRules(classified, dataStructures, options);

    // 5. 生成统计信息
    const stats = {
      totalPages: pages.length,
      totalBlocks: frequency.size,
      templateBlocks: classified.template.length,
      uniqueBlocks: classified.unique.length,
      mixedBlocks: classified.mixed.length,
      tableStructures: dataStructures.tables.length,
      codeBlockTypes: dataStructures.codeBlocks.length,
      listTypes: dataStructures.lists.length
    };

    return {
      stats,
      classified,
      dataStructures,
      cleaningRules,
      frequency
    };
  }

  /**
   * 生成JSON格式的分析报告
   * @param {Object} analysisResult - 分析结果（来自analyzeTemplate）
   * @param {Object} urlPattern - URL模式信息
   * @param {Object} options - 选项
   * @returns {Object} JSON格式的报告
   */
  generateAnalysisJSON(analysisResult, urlPattern, options = {}) {
    const { stats, classified, dataStructures, cleaningRules } = analysisResult;
    
    return {
      templateName: urlPattern.name || 'unknown',
      urlPattern: {
        name: urlPattern.name,
        pathTemplate: urlPattern.pathTemplate,
        pattern: urlPattern.pattern,
        queryParams: urlPattern.queryParams || [],
        urlCount: urlPattern.urlCount || 0
      },
      metadata: {
        generatedAt: new Date().toISOString(),
        pageCount: stats.totalPages,
        version: '1.0.0',
        thresholds: options.thresholds || { template: 0.8, unique: 0.2 }
      },
      statistics: {
        totalPages: stats.totalPages,
        totalBlocks: stats.totalBlocks,
        templateBlocks: stats.templateBlocks,
        uniqueBlocks: stats.uniqueBlocks,
        mixedBlocks: stats.mixedBlocks,
        tableStructures: stats.tableStructures,
        codeBlockTypes: stats.codeBlockTypes,
        listTypes: stats.listTypes
      },
      contentClassification: {
        template: classified.template.map(item => ({
          type: item.type,
          content: item.content.substring(0, 200),
          ratio: item.ratio,
          count: item.count,
          pageCount: item.pages.length
        })),
        unique: classified.unique.map(item => ({
          type: item.type,
          content: item.content.substring(0, 200),
          ratio: item.ratio,
          count: item.count,
          pageCount: item.pages.length
        })),
        mixed: classified.mixed.map(item => ({
          type: item.type,
          content: item.content.substring(0, 200),
          ratio: item.ratio,
          count: item.count,
          pageCount: item.pages.length
        }))
      },
      dataStructures: {
        tables: dataStructures.tables.map(table => ({
          columns: table.columns,
          columnCount: table.columnCount,
          occurrences: table.occurrences,
          pageCount: table.pages.length
        })),
        codeBlocks: dataStructures.codeBlocks.map(code => ({
          language: code.language,
          occurrences: code.occurrences,
          avgLength: code.avgLength,
          pageCount: code.pages.length
        })),
        lists: dataStructures.lists.map(list => ({
          listType: list.listType,
          itemCount: list.itemCount,
          hasNesting: list.hasNesting,
          occurrences: list.occurrences,
          pageCount: list.pages.length
        }))
      },
      cleaningRules: {
        removePatterns: cleaningRules.removePatterns,
        keepPatterns: cleaningRules.keepPatterns,
        removeElements: cleaningRules.removeElements,
        summary: cleaningRules.summary
      }
    };
  }

  /**
   * 生成Markdown格式的分析报告
   * @param {Object} analysisResult - 分析结果（来自analyzeTemplate）
   * @param {Object} urlPattern - URL模式信息
   * @param {Object} options - 选项
   * @returns {string} Markdown格式的报告
   */
  generateAnalysisMarkdown(analysisResult, urlPattern, options = {}) {
    const { stats, classified, dataStructures, cleaningRules } = analysisResult;
    const lines = [];

    // 标题和基本信息
    lines.push(`# 模板分析报告: ${urlPattern.name || 'unknown'}`);
    lines.push('');
    lines.push(`**生成时间**: ${new Date().toISOString()}`);
    lines.push(`**分析页面数**: ${stats.totalPages}`);
    lines.push(`**URL模式**: \`${urlPattern.pathTemplate}\``);
    lines.push('');

    // 统计概览
    lines.push('## 统计概览');
    lines.push('');
    lines.push('| 指标 | 数量 |');
    lines.push('|------|------|');
    lines.push(`| 总内容块数 | ${stats.totalBlocks} |`);
    lines.push(`| 模板内容块 (>80%) | ${stats.templateBlocks} |`);
    lines.push(`| 独特内容块 (<20%) | ${stats.uniqueBlocks} |`);
    lines.push(`| 混合内容块 (20-80%) | ${stats.mixedBlocks} |`);
    lines.push(`| 表格结构类型 | ${stats.tableStructures} |`);
    lines.push(`| 代码块类型 | ${stats.codeBlockTypes} |`);
    lines.push(`| 列表类型 | ${stats.listTypes} |`);
    lines.push('');

    // 模板内容（噪音）
    lines.push('## 模板内容（噪音）');
    lines.push('');
    lines.push('高频出现的内容，通常是页面模板的一部分，应该被过滤：');
    lines.push('');
    
    if (classified.template.length > 0) {
      const topTemplate = classified.template.slice(0, 10);
      topTemplate.forEach((item, index) => {
        lines.push(`### ${index + 1}. ${item.type} (${(item.ratio * 100).toFixed(1)}%)`);
        lines.push('');
        lines.push('```');
        lines.push(item.content.substring(0, 200));
        if (item.content.length > 200) {
          lines.push('...');
        }
        lines.push('```');
        lines.push('');
      });
    } else {
      lines.push('*未发现高频模板内容*');
      lines.push('');
    }

    // 独特内容（数据）
    lines.push('## 独特内容（数据）');
    lines.push('');
    lines.push('低频出现的内容，通常是页面的独特数据，应该被保留：');
    lines.push('');
    
    if (classified.unique.length > 0) {
      const topUnique = classified.unique.slice(0, 10);
      topUnique.forEach((item, index) => {
        lines.push(`### ${index + 1}. ${item.type} (${(item.ratio * 100).toFixed(1)}%)`);
        lines.push('');
        lines.push('```');
        lines.push(item.content.substring(0, 200));
        if (item.content.length > 200) {
          lines.push('...');
        }
        lines.push('```');
        lines.push('');
      });
    } else {
      lines.push('*未发现低频独特内容*');
      lines.push('');
    }

    // 数据结构
    lines.push('## 数据结构');
    lines.push('');

    // 表格结构
    if (dataStructures.tables.length > 0) {
      lines.push('### 表格结构');
      lines.push('');
      dataStructures.tables.forEach((table, index) => {
        lines.push(`**表格 ${index + 1}** (出现 ${table.occurrences} 次):`);
        lines.push('');
        lines.push(`- 列数: ${table.columnCount}`);
        lines.push(`- 列名: ${table.columns.join(', ')}`);
        lines.push('');
      });
    }

    // 代码块
    if (dataStructures.codeBlocks.length > 0) {
      lines.push('### 代码块');
      lines.push('');
      dataStructures.codeBlocks.forEach((code, index) => {
        lines.push(`**代码块 ${index + 1}** (出现 ${code.occurrences} 次):`);
        lines.push('');
        lines.push(`- 语言: ${code.language}`);
        lines.push(`- 平均长度: ${code.avgLength} 字符`);
        lines.push('');
      });
    }

    // 列表
    if (dataStructures.lists.length > 0) {
      lines.push('### 列表');
      lines.push('');
      dataStructures.lists.forEach((list, index) => {
        lines.push(`**列表 ${index + 1}** (出现 ${list.occurrences} 次):`);
        lines.push('');
        lines.push(`- 类型: ${list.listType}`);
        lines.push(`- 项目数: ${list.itemCount}`);
        lines.push(`- 嵌套: ${list.hasNesting ? '是' : '否'}`);
        lines.push('');
      });
    }

    // 清洗规则
    lines.push('## 清洗规则');
    lines.push('');
    lines.push(`- 移除规则: ${cleaningRules.removePatterns.length}`);
    lines.push(`- 保留规则: ${cleaningRules.keepPatterns.length}`);
    lines.push(`- 移除元素: ${cleaningRules.removeElements.length}`);
    lines.push('');

    // 建议
    lines.push('## 建议');
    lines.push('');
    lines.push('1. 使用移除规则过滤高频模板内容');
    lines.push('2. 保留低频独特内容作为有价值数据');
    lines.push('3. 对中频内容进行人工审查');
    lines.push('4. 根据数据结构配置专用提取器');
    lines.push('');

    return lines.join('\n');
  }

  /**
   * 生成清洗前后对比示例
   * @param {Array<string>} pages - 页面内容数组
   * @param {Object} cleaningRules - 清洗规则
   * @param {Object} options - 选项
   * @returns {Array<Object>} 对比示例数组
   */
  generateCleaningExamples(pages, cleaningRules, options = {}) {
    const maxExamples = options.maxExamples || 3;
    const examples = [];

    // 选择几个页面作为示例
    const samplePages = pages.slice(0, Math.min(maxExamples, pages.length));

    samplePages.forEach((page, index) => {
      // 原始内容
      const original = page;

      // 应用清洗规则
      let cleaned = page;

      // 1. 应用移除规则
      cleaningRules.removePatterns.forEach(rule => {
        try {
          const regex = new RegExp(rule.pattern, 'gi');
          cleaned = cleaned.replace(regex, '');
        } catch (error) {
          // 忽略无效的正则表达式
        }
      });

      // 2. 移除高频元素
      cleaningRules.removeElements.forEach(element => {
        if (element.type === 'heading') {
          // 移除特定标题
          const headingRegex = new RegExp(`^#+\\s*${this._escapeRegex(element.text)}\\s*$`, 'gim');
          cleaned = cleaned.replace(headingRegex, '');
        }
      });

      // 3. 清理多余空行
      cleaned = cleaned.replace(/\n{3,}/g, '\n\n');
      cleaned = cleaned.trim();

      // 计算清洗效果
      const originalLength = original.length;
      const cleanedLength = cleaned.length;
      const reduction = ((originalLength - cleanedLength) / originalLength * 100).toFixed(1);

      examples.push({
        index: index + 1,
        original: {
          content: original.substring(0, 500),
          length: originalLength,
          preview: original.substring(0, 200) + (original.length > 200 ? '...' : '')
        },
        cleaned: {
          content: cleaned.substring(0, 500),
          length: cleanedLength,
          preview: cleaned.substring(0, 200) + (cleaned.length > 200 ? '...' : '')
        },
        stats: {
          originalLength,
          cleanedLength,
          reduction: `${reduction}%`,
          removedLength: originalLength - cleanedLength
        }
      });
    });

    return examples;
  }
}

module.exports = TemplateContentAnalyzer;
