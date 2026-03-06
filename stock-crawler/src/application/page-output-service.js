import fs from 'fs';
import crypto from 'crypto';

class PageOutputService {
  constructor({ logger, markdownGenerator, pageStorage, pagesDir }) {
    this.logger = logger;
    this.markdownGenerator = markdownGenerator;
    this.pageStorage = pageStorage;
    this.pagesDir = pagesDir;
  }

  createOutputContext(pageTitle, url) {
    let filename = this.markdownGenerator.safeFilename(pageTitle || 'untitled', url);
    let filepath = `${this.pagesDir}/${filename}.md`;

    if (fs.existsSync(filepath)) {
      const urlHash = crypto.createHash('md5').update(url).digest('hex').substring(0, 8);
      filename = `${filename}_${urlHash}`;
      filepath = `${this.pagesDir}/${filename}.md`;
    }

    return {
      isFirstChunk: true,
      pageTitle,
      filename,
      filepath
    };
  }

  createChunkWriter(context, url) {
    return async (chunk) => {
      try {
        if (context.isFirstChunk) {
          const header = `# ${context.pageTitle || 'Untitled'}\n\n## 源URL\n\n${url}\n\n`;
          fs.writeFileSync(context.filepath, header, 'utf-8');
          context.isFirstChunk = false;
        }

        const content = this.buildChunkContent(chunk);
        if (!content) {
          return;
        }

        fs.appendFileSync(context.filepath, content, 'utf-8');
      } catch (error) {
        this.logger.error(`Failed to write data chunk: ${error.message}`);
      }
    };
  }

  buildChunkContent(chunk) {
    if (chunk.type === 'table') {
      if (chunk.isFirstPage) {
        let content = `\n## 表格 ${chunk.tableIndex + 1}\n\n`;
        content += this.renderMarkdownTable(chunk.headers, chunk.rows);
        this.logger.debug(`Appended table ${chunk.tableIndex + 1}, page ${chunk.page}`);
        return content;
      }

      if (!chunk.isLastPage && chunk.rows && chunk.rows.length > 0) {
        const rowsContent = chunk.rows.map(row => `| ${row.join(' | ')} |\n`).join('');
        this.logger.debug(`Appended ${chunk.rows.length} rows to table ${chunk.tableIndex + 1}, page ${chunk.page}`);
        return rowsContent;
      }
      return '';
    }

    if (chunk.type === 'table-new') {
      let content = `\n## 表格 ${chunk.tableIndex + 1} (结构变化)\n\n`;
      content += this.renderMarkdownTable(chunk.headers, chunk.rows);
      this.logger.info(`Started new table ${chunk.tableIndex + 1} due to structure change`);
      return content;
    }

    if (chunk.type === 'tab') {
      let content = `\n## Tab页: ${chunk.name}\n\n`;
      content += this.renderRichContent(chunk.data);
      this.logger.debug(`Appended tab content: ${chunk.name}`);
      return content;
    }

    if (chunk.type === 'dropdown-option') {
      let content = `\n## 下拉框: ${chunk.dropdown} - 选项: ${chunk.option}\n\n`;
      content += this.renderRichContent(chunk.data);
      this.logger.debug(`Appended dropdown option: ${chunk.dropdown} - ${chunk.option}`);
      return content;
    }

    if (chunk.type === 'date-filter') {
      let content = `\n## 时间筛选: ${chunk.range}\n\n`;
      content += `时间范围: ${chunk.startDate} 至 ${chunk.endDate}\n\n`;

      if (chunk.tables && chunk.tables.length > 0) {
        chunk.tables.forEach((table, idx) => {
          content += `### 表格 ${idx + 1}\n\n`;
          content += this.renderMarkdownTable(table.headers, table.rows);
          if (table.headers && table.headers.length > 0) {
            content += '\n';
          }
        });
      }

      this.logger.debug(`Appended date filter data: ${chunk.range}`);
      return content;
    }

    return '';
  }

  renderRichContent(data = {}) {
    let content = '';

    if (data.paragraphs && data.paragraphs.length > 0) {
      data.paragraphs.forEach(p => {
        if (p.trim()) {
          content += `${p}\n\n`;
        }
      });
    }

    if (data.lists && data.lists.length > 0) {
      data.lists.forEach(list => {
        list.items.forEach((item, i) => {
          if (list.type === 'ol') {
            content += `${i + 1}. ${item}\n`;
          } else {
            content += `- ${item}\n`;
          }
        });
        content += '\n';
      });
    }

    if (data.tables && data.tables.length > 0) {
      data.tables.forEach(table => {
        if (table.headers && table.headers.length > 0) {
          content += this.renderMarkdownTable(table.headers, table.rows);
          content += '\n';
        }
      });
    }

    if (data.codeBlocks && data.codeBlocks.length > 0) {
      data.codeBlocks.forEach(block => {
        content += `\`\`\`${block.language}\n${block.code}\n\`\`\`\n\n`;
      });
    }

    return content;
  }

  renderMarkdownTable(headers, rows) {
    let content = '';

    if (headers && headers.length > 0) {
      content += `| ${headers.join(' | ')} |\n`;
      content += `| ${headers.map(() => '---').join(' | ')} |\n`;
    }

    if (rows && rows.length > 0) {
      rows.forEach(row => {
        content += `| ${row.join(' | ')} |\n`;
      });
    }

    return content;
  }

  async saveTablesAsCsv(pageData, url) {
    let baseName = this.markdownGenerator.safeFilename(pageData.title || 'table', url);
    const urlHash = crypto.createHash('md5').update(url).digest('hex').substring(0, 8);
    baseName = `${baseName}_${urlHash}`;

    const savedFiles = [];
    for (let i = 0; i < pageData.tables.length; i++) {
      const table = pageData.tables[i];
      const fileName = pageData.tables.length > 1 ? `${baseName}_table_${i + 1}.csv` : `${baseName}.csv`;
      const filePath = `${this.pagesDir}/${fileName}`;

      const lines = [];
      if (table.headers && table.headers.length > 0) {
        lines.push(table.headers.map(h => this.escapeCsvField(h)).join(','));
      }
      if (table.rows && table.rows.length > 0) {
        table.rows.forEach(row => {
          lines.push(row.map(cell => this.escapeCsvField(cell)).join(','));
        });
      }

      fs.writeFileSync(filePath, lines.join('\n'), 'utf-8');
      savedFiles.push(fileName);
      this.logger.success(`Saved: ${fileName}`);
    }

    return savedFiles;
  }

  escapeCsvField(value) {
    const stringValue = value == null ? '' : String(value);
    const escaped = stringValue.replace(/"/g, '""');
    if (/[",\n]/.test(escaped)) {
      return `"${escaped}"`;
    }
    return escaped;
  }

  writeFallbackMarkdown(pageData, url, context) {
    const markdown = this.markdownGenerator.generate(pageData);
    context.filename = this.markdownGenerator.safeFilename(pageData.title || 'untitled', url);

    let fallbackPath = `${this.pagesDir}/${context.filename}.md`;
    if (fs.existsSync(fallbackPath)) {
      const urlHash = crypto.createHash('md5').update(url).digest('hex').substring(0, 8);
      context.filename = `${context.filename}_${urlHash}`;
      this.logger.info(`File exists, using unique filename: ${context.filename}.md`);
    }

    context.filepath = this.markdownGenerator.saveToFile(markdown, context.filename, this.pagesDir);
  }

  appendLlmSection(filepath, llmExtraction) {
    const llmSection = `
## LLM结构化抽取

模型: ${llmExtraction.model}

\`\`\`json
${JSON.stringify(llmExtraction, null, 2)}
\`\`\`
`;
    fs.appendFileSync(filepath, llmSection, 'utf-8');
  }

  async persistMarkdown(filepath, url, title, filename) {
    const savedPath = await this.pageStorage.persistMarkdown({
      filepath,
      url,
      title,
      filename
    });

    if (this.pageStorage.isLanceDb()) {
      this.logger.info(`Persisted page content to ${savedPath}`);
    }
  }
}

export default PageOutputService;
