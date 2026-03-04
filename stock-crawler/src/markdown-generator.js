import fs from 'fs';
import path from 'path';

/**
 * Markdown Generator - 负责将解析的页面数据转换为Markdown格式
 */
class MarkdownGenerator {
  /**
   * 生成Markdown内容
   * @param {PageData} pageData - 页面数据
   * @returns {string} Markdown文本
   */
  generate(pageData) {
    // 根据页面类型选择生成方法
    if (pageData.type === 'api-doc') {
      return this.generateApiDoc(pageData);
    } else if (pageData.type === 'generic') {
      return this.generateGeneric(pageData);
    } else if (pageData.type === 'core-content') {
      return this.generateCoreContent(pageData);
    } else {
      // 兼容旧格式（没有type字段）
      return this.generateApiDoc(pageData);
    }
  }

  /**
   * 生成API文档Markdown
   * @param {PageData} pageData - API文档页面数据
   * @returns {string} Markdown文本
   */
  generateApiDoc(pageData) {
    const sections = [];

    // 添加标题
    if (pageData.title) {
      sections.push(`# ${pageData.title}\n`);
    }

    // 添加源URL（始终添加，即使其他内容为空）
    if (pageData.url) {
      sections.push('## 源URL\n');
      sections.push(pageData.url);
      sections.push('');
    }

    // 添加简要描述
    if (pageData.briefDesc) {
      sections.push('## 简要描述\n');
      sections.push(pageData.briefDesc);
      sections.push('');
    }

    // 添加请求URL
    if (pageData.requestUrl) {
      sections.push('## 请求URL\n');
      sections.push('```');
      sections.push(pageData.requestUrl);
      sections.push('```');
      sections.push('');
    }

    // 添加请求方式
    if (pageData.requestMethod) {
      sections.push('## 请求方式\n');
      sections.push(pageData.requestMethod);
      sections.push('');
    }

    // 添加参数
    if (pageData.params && pageData.params.length > 0) {
      sections.push('## 参数\n');
      sections.push('| 参数名称 | 必选 | 数据类型 | 说明 |');
      sections.push('| -------- | ---- | -------- | ---- |');
      pageData.params.forEach(p => {
        const desc = this.escapeMarkdown(p.desc);
        sections.push(`| ${p.name} | ${p.required} | ${p.type} | ${desc} |`);
      });
      sections.push('');
    }

    // 添加API试用示例
    if (pageData.apiExamples && pageData.apiExamples.length > 0) {
      sections.push('## API试用示例\n');
      pageData.apiExamples.forEach((example, index) => {
        if (pageData.apiExamples.length > 1) {
          sections.push(`### ${example.name}\n`);
        }
        sections.push('```json');
        // 尝试格式化 JSON
        try {
          const parsed = JSON.parse(example.code);
          sections.push(JSON.stringify(parsed, null, 2));
        } catch {
          sections.push(example.code);
        }
        sections.push('```');
        sections.push('');
      });
    }

    // 添加返回数据说明
    if (pageData.responseData && 
        (pageData.responseData.description || pageData.responseData.table.length > 0)) {
      sections.push('## 返回数据说明\n');
      
      // 添加返回数据表格
      if (pageData.responseData.table && pageData.responseData.table.length > 0) {
        const hasDesc = pageData.responseData.table.some(r => r.desc);
        if (hasDesc) {
          sections.push('| 参数名称 | 数据类型 | 说明 |');
          sections.push('| -------- | -------- | ---- |');
          pageData.responseData.table.forEach(r => {
            const desc = this.escapeMarkdown(r.desc || '');
            sections.push(`| ${r.name} | ${r.type} | ${desc} |`);
          });
        } else {
          sections.push('| 参数名称 | 数据类型 |');
          sections.push('| -------- | -------- |');
          pageData.responseData.table.forEach(r => {
            sections.push(`| ${r.name} | ${r.type} |`);
          });
        }
        sections.push('');
      }
      
      // 添加返回数据描述文本
      if (pageData.responseData.description) {
        if (pageData.responseData.table && pageData.responseData.table.length > 0) {
          sections.push('');
        }
        sections.push(pageData.responseData.description);
        sections.push('');
      }
    }

    return sections.join('\n');
  }


  /**
   * 生成核心正文Markdown
   * @param {PageData} pageData - 核心正文页面数据
   * @returns {string} Markdown文本
   */
  generateCoreContent(pageData) {
    const sections = [];

    if (pageData.title) {
      sections.push(`# ${pageData.title}\n`);
    }

    if (pageData.url) {
      sections.push('## 源URL\n');
      sections.push(pageData.url);
      sections.push('');
    }

    if (pageData.mainContent && pageData.mainContent.length > 0) {
      sections.push('## 核心正文\n');
      pageData.mainContent.forEach(item => {
        if (item.type === 'heading') {
          sections.push(`${'#'.repeat(Math.min((item.level || 2) + 1, 6))} ${item.content}\n`);
        } else {
          sections.push(item.content);
          sections.push('');
        }
      });
    } else if (pageData.contentText) {
      sections.push('## 核心正文\n');
      sections.push(pageData.contentText);
      sections.push('');
    }

    return sections.join('\n');
  }

  /**
   * 生成通用页面Markdown
   * @param {PageData} pageData - 通用页面数据
   * @returns {string} Markdown文本
   */
  generateGeneric(pageData) {
    const sections = [];

    // 添加标题
    if (pageData.title) {
      sections.push(`# ${pageData.title}\n`);
    }

    // 添加源URL
    if (pageData.url) {
      sections.push('## 源URL\n');
      sections.push(pageData.url);
      sections.push('');
    }

    // 添加描述
    if (pageData.description) {
      sections.push('## 描述\n');
      sections.push(pageData.description);
      sections.push('');
    }

    // 如果有mainContent（混排内容），优先使用它
    if (pageData.mainContent && pageData.mainContent.length > 0) {
      sections.push('## 内容\n');
      
      pageData.mainContent.forEach(item => {
        switch (item.type) {
          case 'heading':
            sections.push(`${'#'.repeat(item.level + 1)} ${item.content}\n`);
            break;
            
          case 'paragraph':
            sections.push(item.content);
            sections.push('');
            break;
            
          case 'image':
            const imgAlt = item.alt || item.title || '图片';
            const imgSrc = item.localPath || item.src;
            sections.push(`![${imgAlt}](${imgSrc})`);
            if (item.title && item.title !== item.alt) {
              sections.push(`*${item.title}*`);
            }
            sections.push('');
            break;
            
          case 'list':
            item.items.forEach((listItem, i) => {
              if (item.listType === 'ol') {
                sections.push(`${i + 1}. ${listItem}`);
              } else {
                sections.push(`- ${listItem}`);
              }
            });
            sections.push('');
            break;
            
          case 'blockquote':
            sections.push(`> ${item.content}`);
            sections.push('');
            break;
            
          case 'codeblock':
            const lang = item.language || 'text';
            sections.push(`\`\`\`${lang}`);
            sections.push(item.content);
            sections.push('```');
            sections.push('');
            break;
            
          case 'hr':
            sections.push('---');
            sections.push('');
            break;
            
          case 'table':
            if (item.headers && item.headers.length > 0) {
              sections.push('| ' + item.headers.join(' | ') + ' |');
              sections.push('| ' + item.headers.map(() => '---').join(' | ') + ' |');
            }
            if (item.rows && item.rows.length > 0) {
              item.rows.forEach(row => {
                sections.push('| ' + row.join(' | ') + ' |');
              });
            }
            sections.push('');
            break;
        }
      });
      
      // 即使使用了mainContent，也要添加单独提取的图片和图表（如果它们不在mainContent中）
      if (pageData.images && pageData.images.length > 0) {
        sections.push('## 图片\n');
        pageData.images.forEach(img => {
          const alt = img.alt || img.title || '图片';
          const src = img.localPath || img.src;
          sections.push(`![${alt}](${src})`);
          if (img.title && img.title !== img.alt) {
            sections.push(`*${img.title}*`);
          }
          sections.push('');
        });
      }

      // 添加图表（Canvas/SVG截图）
      if (pageData.charts && pageData.charts.length > 0) {
        sections.push('## 图表\n');
        pageData.charts.forEach(chart => {
          const alt = `${chart.type.toUpperCase()}图表 ${chart.index}`;
          sections.push(`![${alt}](${chart.filename})`);
          sections.push(`*尺寸: ${chart.width}x${chart.height}px*`);
          sections.push('');
        });
      }
    } else {
      // 回退到旧的分段方式
      // 添加标题结构
      if (pageData.headings && pageData.headings.length > 0) {
        sections.push('## 页面结构\n');
        pageData.headings.forEach(h => {
          const indent = '  '.repeat(h.level - 1);
          sections.push(`${indent}- ${h.text}`);
        });
        sections.push('');
      }

      // 添加Tab页内容
      if (pageData.tabs && pageData.tabs.length > 0) {
        sections.push('## Tab页内容\n');
        pageData.tabs.forEach(tab => {
          sections.push(`### ${tab.name}\n`);
          sections.push(tab.content);
          sections.push('');
        });
      }

      // 添加段落
      if (pageData.paragraphs && pageData.paragraphs.length > 0) {
        sections.push('## 正文内容\n');
        pageData.paragraphs.forEach(p => {
          if (p.trim()) {
            sections.push(p);
            sections.push('');
          }
        });
      }

      // 添加引用块
      if (pageData.blockquotes && pageData.blockquotes.length > 0) {
        sections.push('## 引用\n');
        pageData.blockquotes.forEach(quote => {
          sections.push(`> ${quote}`);
          sections.push('');
        });
      }

      // 添加定义列表
      if (pageData.definitionLists && pageData.definitionLists.length > 0) {
        sections.push('## 术语定义\n');
        pageData.definitionLists.forEach((dlist, index) => {
          if (pageData.definitionLists.length > 1) {
            sections.push(`### 定义列表 ${index + 1}\n`);
          }
          dlist.forEach(item => {
            sections.push(`**${item.term}**`);
            sections.push(`: ${item.definition}`);
            sections.push('');
          });
        });
      }

      // 添加列表
      if (pageData.lists && pageData.lists.length > 0) {
        sections.push('## 列表\n');
        pageData.lists.forEach((list, index) => {
          if (pageData.lists.length > 1) {
            sections.push(`### 列表 ${index + 1}\n`);
          }
          list.items.forEach((item, i) => {
            if (list.type === 'ol') {
              sections.push(`${i + 1}. ${item}`);
            } else {
              sections.push(`- ${item}`);
            }
          });
          sections.push('');
        });
      }

      // 添加表格
      if (pageData.tables && pageData.tables.length > 0) {
        sections.push('## 表格\n');
        pageData.tables.forEach((table, index) => {
          if (pageData.tables.length > 1) {
            sections.push(`### 表格 ${index + 1}\n`);
          }
          if (table.caption) {
            sections.push(`**${table.caption}**\n`);
          }
          const markdown = this.tableToMarkdown(table);
          if (markdown) {
            sections.push(markdown);
            sections.push('');
          }
        });
      }

      // 添加代码块
      if (pageData.codeBlocks && pageData.codeBlocks.length > 0) {
        sections.push('## 代码示例\n');
        pageData.codeBlocks.forEach((block, index) => {
          if (pageData.codeBlocks.length > 1) {
            sections.push(`### 代码 ${index + 1}\n`);
          }
          sections.push(this.codeBlockToMarkdown(block));
          sections.push('');
        });
      }

      // 添加图片
      if (pageData.images && pageData.images.length > 0) {
        sections.push('## 图片\n');
        pageData.images.forEach(img => {
          const alt = img.alt || img.title || '图片';
          // 使用本地路径（如果有）或原始URL
          const src = img.localPath || img.src;
          sections.push(`![${alt}](${src})`);
          if (img.title && img.title !== img.alt) {
            sections.push(`*${img.title}*`);
          }
          sections.push('');
        });
      }

      // 添加视频
      if (pageData.videos && pageData.videos.length > 0) {
        sections.push('## 视频\n');
        pageData.videos.forEach((video, index) => {
          sections.push(`### 视频 ${index + 1}\n`);
          sections.push(`视频链接: ${video.src}`);
          if (video.poster) {
            sections.push(`![视频封面](${video.poster})`);
          }
          sections.push('');
        });
      }

      // 添加音频
      if (pageData.audios && pageData.audios.length > 0) {
        sections.push('## 音频\n');
        pageData.audios.forEach((audio, index) => {
          sections.push(`### 音频 ${index + 1}\n`);
          sections.push(`音频链接: ${audio.src}`);
          sections.push('');
        });
      }

      // 添加图表（Canvas/SVG截图）
      if (pageData.charts && pageData.charts.length > 0) {
        sections.push('## 图表\n');
        pageData.charts.forEach(chart => {
          const alt = `${chart.type.toUpperCase()}图表 ${chart.index}`;
          sections.push(`![${alt}](${chart.filename})`);
          sections.push(`*尺寸: ${chart.width}x${chart.height}px*`);
          sections.push('');
        });
      }

      // 添加Tab页和下拉框内容
      if (pageData.tabsAndDropdowns && pageData.tabsAndDropdowns.length > 0) {
        pageData.tabsAndDropdowns.forEach(item => {
          if (item.type === 'tab') {
            sections.push(`\n## Tab页: ${item.name}\n`);
            
            if (item.paragraphs && item.paragraphs.length > 0) {
              item.paragraphs.forEach(p => {
                if (p.trim()) {
                  sections.push(p);
                  sections.push('');
                }
              });
            }
            
            if (item.tables && item.tables.length > 0) {
              item.tables.forEach(table => {
                const markdown = this.tableToMarkdown(table);
                if (markdown) {
                  sections.push(markdown);
                  sections.push('');
                }
              });
            }
          } else if (item.type === 'dropdown') {
            sections.push(`\n## 下拉框: ${item.label}\n`);
            
            item.options.forEach(option => {
              sections.push(`### 选项: ${option.text}\n`);
              
              if (option.paragraphs && option.paragraphs.length > 0) {
                option.paragraphs.forEach(p => {
                  if (p.trim()) {
                    sections.push(p);
                    sections.push('');
                  }
                });
              }
              
              if (option.tables && option.tables.length > 0) {
                option.tables.forEach(table => {
                  const markdown = this.tableToMarkdown(table);
                  if (markdown) {
                    sections.push(markdown);
                    sections.push('');
                  }
                });
              }
            });
          }
        });
      }
    }

    return sections.join('\n');
  }

  /**
   * 将表格转换为Markdown表格
   * @param {Table} table - 表格数据
   * @returns {string} Markdown表格
   */
  tableToMarkdown(table) {
    if (!table.headers || table.headers.length === 0) {
      // 如果没有表头，只输出数据行
      if (!table.rows || table.rows.length === 0) {
        return '';
      }
      return table.rows.map(row => 
        '| ' + row.map(cell => this.escapeMarkdown(cell)).join(' | ') + ' |'
      ).join('\n');
    }

    const lines = [];

    // 表头行
    const headerRow = '| ' + table.headers.map(h => this.escapeMarkdown(h)).join(' | ') + ' |';
    lines.push(headerRow);

    // 分隔行
    const separator = '| ' + table.headers.map(() => '---').join(' | ') + ' |';
    lines.push(separator);

    // 数据行
    if (table.rows && table.rows.length > 0) {
      table.rows.forEach(row => {
        const cells = row.map(cell => this.escapeMarkdown(cell));
        // 确保行的列数与表头一致
        while (cells.length < table.headers.length) {
          cells.push('');
        }
        const dataRow = '| ' + cells.slice(0, table.headers.length).join(' | ') + ' |';
        lines.push(dataRow);
      });
    }

    return lines.join('\n');
  }

  /**
   * 将代码块转换为Markdown代码块
   * @param {CodeBlock} codeBlock - 代码块数据
   * @returns {string} Markdown代码块
   */
  codeBlockToMarkdown(codeBlock) {
    const language = codeBlock.language || 'text';
    return `\`\`\`${language}\n${codeBlock.code}\n\`\`\``;
  }

  /**
   * 转义Markdown特殊字符
   * @param {string} text - 原始文本
   * @returns {string} 转义后的文本
   */
  escapeMarkdown(text) {
    if (typeof text !== 'string') {
      return String(text);
    }
    // 转义表格中的管道符和换行符
    return text
      .replace(/\|/g, '\\|')
      .replace(/\n/g, '<br>');
  }

  /**
   * 清理标题（移除特殊字符和冗余信息）
   * @param {string} title - 原始标题
   * @returns {string} 清理后的标题
   */
  cleanTitle(title) {
    if (!title || typeof title !== 'string') {
      return '';
    }

    return title
      .replace(/\|/g, '_')              // 管道符转下划线
      .replace(/\s+/g, '_')             // 空格转下划线
      .replace(/_-_[^_]+$/i, '')        // 移除常见网站名后缀
      .replace(/[\/\\?*:|"<>]/g, '_')   // 替换文件系统不允许的字符
      .replace(/_{2,}/g, '_')           // 合并多个下划线
      .replace(/^_|_$/g, '');           // 移除首尾下划线
  }

  /**
   * 从URL中提取关键部分
   * @param {string} url - URL字符串
   * @returns {string[]} 关键部分数组
   */
  extractKeyParts(url) {
    const parts = [];
    
    try {
      const urlObj = new URL(url);
      const pathname = urlObj.pathname;
      const searchParams = urlObj.searchParams;
      
      // 1. 提取市场代码 (cn/hk/us/a/b/h)
      const marketCodes = ['cn', 'hk', 'us', 'a', 'b', 'h'];
      marketCodes.forEach(code => {
        const pattern = new RegExp(`\\/${code}\\/|\\/${code}$|=${code}(?:&|$)|\\/${code}\\/`);
        if (pattern.test(pathname) || pattern.test(searchParams.toString())) {
          if (!parts.includes(code)) {
            parts.push(code);
          }
        }
      });
      
      // 2. 提取数据类型/周期
      const dataTypes = {
        'weekly': 'weekly',
        'monthly': 'monthly',
        'quarterly': 'quarterly',
        'annually': 'annually',
        'daily': 'daily',
        'custom': 'custom',
        'realtime': 'realtime'
      };
      
      Object.entries(dataTypes).forEach(([key, value]) => {
        if (pathname.includes(key) || searchParams.toString().includes(key)) {
          if (!parts.includes(value)) {
            parts.push(value);
          }
        }
      });
      
      // 3. 提取 API Key 的关键部分
      const apiKey = searchParams.get('api-key');
      if (apiKey && apiKey !== 'undefined') {
        // 取最后两段作为关键部分
        const apiParts = apiKey.split('/').filter(p => p && p !== 'undefined');
        
        // 如果第一段是市场代码，单独提取
        if (apiParts.length > 0 && marketCodes.includes(apiParts[0])) {
          if (!parts.includes(apiParts[0])) {
            parts.push(apiParts[0]);
          }
        }
        
        // 提取最后两段（排除市场代码）
        const nonMarketParts = apiParts.filter(p => !marketCodes.includes(p));
        if (nonMarketParts.length > 0) {
          const keyParts = nonMarketParts.slice(-2).join('_');
          if (keyParts && !parts.includes(keyParts)) {
            parts.push(keyParts);
          }
        }
      }
      
      // 4. 提取查询参数中的关键字
      const importantParams = [
        'chart-granularity',
        'date-range',
        'period',
        'type',
        'category',
        'granularity'
      ];
      
      importantParams.forEach(param => {
        const value = searchParams.get(param);
        if (value && value !== 'undefined') {
          // 简化参数值（只取前10个字符，移除特殊字符）
          const shortValue = value.substring(0, 10).replace(/[^a-zA-Z0-9]/g, '');
          if (shortValue && !parts.includes(shortValue)) {
            parts.push(shortValue);
          }
        }
      });
      
      // 5. 提取路径中的关键段
      const pathSegments = pathname.split('/').filter(s => s);
      const keywordSegments = [
        'index', 'constituents', 'fundamental', 'financial',
        'non-financial', 'industry', 'company', 'macro',
        'analytics', 'chart-maker', 'shareholders', 'treasury',
        'money-supply', 'cpi', 'ppi', 'gdp', 'bs', 'pl', 'cf'
      ];
      
      pathSegments.forEach(segment => {
        if (keywordSegments.includes(segment) && !parts.includes(segment)) {
          parts.push(segment);
        }
      });
      
    } catch (error) {
      // URL解析失败，返回空数组
    }
    
    return parts;
  }

  /**
   * 生成安全的文件名
   * @param {string} title - 原始标题
   * @param {string} url - 页面URL（可选，用于生成更好的文件名）
   * @returns {string} 安全的文件名
   */
  safeFilename(title, url = null) {
    if (!title || typeof title !== 'string') {
      return 'untitled';
    }

    // 1. 清理标题
    let cleanedTitle = this.cleanTitle(title);
    
    // 2. 如果提供了URL，提取关键部分
    let urlParts = [];
    if (url) {
      urlParts = this.extractKeyParts(url);
    }
    
    // 3. 组合文件名
    let filename = cleanedTitle;
    
    if (urlParts.length > 0) {
      // 限制URL部分最多3个关键字
      const limitedParts = urlParts.slice(0, 3);
      filename += '_' + limitedParts.join('_');
    }
    
    // 4. 限制总长度
    if (filename.length > 60) {
      // 优先保留标题，截断URL部分
      const titlePart = cleanedTitle.substring(0, 40);
      const urlPart = urlParts.slice(0, 2).join('_').substring(0, 18);
      filename = titlePart + (urlPart ? '_' + urlPart : '');
    }
    
    // 5. 最终清理
    filename = filename
      .replace(/_{2,}/g, '_')
      .replace(/^_|_$/g, '');
    
    // 6. 如果文件名为空，使用默认值
    if (!filename) {
      filename = 'untitled';
    }
    
    // 7. 限制最终长度（保险起见）
    if (filename.length > 200) {
      filename = filename.substring(0, 200);
    }

    return filename;
  }

  /**
   * 保存Markdown文件
   * @param {string} content - Markdown内容
   * @param {string} filename - 文件名（不含扩展名）
   * @param {string} outputDir - 输出目录
   * @returns {string} 保存的文件路径
   */
  saveToFile(content, filename, outputDir) {
    try {
      // 确保输出目录存在
      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
      }

      // 确保文件名有.md扩展名
      const filenameWithExt = filename.endsWith('.md') ? filename : `${filename}.md`;

      // 生成完整路径
      const filepath = path.join(outputDir, filenameWithExt);

      // 写入文件
      fs.writeFileSync(filepath, content, 'utf-8');

      return filepath;
    } catch (error) {
      throw new Error(`Failed to save file: ${error.message}`);
    }
  }
}

export default MarkdownGenerator;
