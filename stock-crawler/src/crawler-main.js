import ConfigManager from './config-manager.js';
import LinkManager from './link-manager.js';
import BrowserManager from './browser-manager.js';
import LoginHandler from './login-handler.js';
import LinkFinder from './link-finder.js';
import PageParser from './page-parser.js';
import MarkdownGenerator from './markdown-generator.js';
import Logger from './logger.js';
import StatsTracker from './stats-tracker.js';
import PageStorage from './storage/page-storage.js';
import LLMDataExtractor from './llm-data-extractor.js';
import CrawlJobService from './application/crawl-job-service.js';
import UrlProcessingService from './application/url-processing-service.js';
import MetricsAdapter from './infrastructure/metrics-adapter.js';
import CrawlerBootstrapService from './application/crawler-bootstrap-service.js';
import LoginOrchestrationService from './application/login-orchestration-service.js';

class CrawlerMain {
  constructor() {
    this.config = null;
    this.linkManager = null;
    this.browserManager = null;
    this.loginHandler = null;
    this.linkFinder = null;
    this.pageParser = null;
    this.markdownGenerator = null;
    this.logger = null;
    this.statsTracker = null;
    this.pageStorage = null;
    this.llmDataExtractor = null;
    this.isLoggedIn = false;
    this.crawlJobService = null;
    this.urlProcessingService = null;
    this.metricsAdapter = null;
    this.bootstrapService = new CrawlerBootstrapService();
    this.loginOrchestrationService = null;
  }

  /**
   * Initialize crawler with configuration
   * @param {string} configPath - Path to configuration file
   */
  async initialize(configPath) {
    const initialized = await this.bootstrapService.initialize(configPath);
    Object.assign(this, initialized);

    this.loginOrchestrationService = new LoginOrchestrationService({
      browserManager: this.browserManager,
      loginHandler: this.loginHandler,
      logger: this.logger,
      config: this.config
    });
  }

  /**
   * Start crawling process
   */
  async start() {
    try {
      this.logger.info('Starting crawler...');
      this.statsTracker.start();

      // Launch browser
      await this.browserManager.launch({
        headless: this.config.crawler.headless,
        userDataDir: this.config.crawler.userDataDir // Use Chrome user data directory if provided
      });
      this.logger.info(`Browser launched (headless: ${this.config.crawler.headless})`);

      // Attempt login at the start if required
      if (this.config.login.required) {
        this.logger.info('Login is required, attempting to login at start...');
        const loginSuccess = await this.attemptLogin();
        if (loginSuccess) {
          this.logger.info('Login successful at start');
          this.isLoggedIn = true;
        } else {
          this.logger.warn('Login failed at start, will retry on individual pages if needed');
        }
      }

      const batchSize = this.config.crawler.batchSize || 20;
      const linksToProcess = this.buildLinksToProcess(batchSize);
      
      this.statsTracker.setTotalUrls(this.linkManager.links.length);
      let linksDirty = false;
      
      const totalUnfetched = this.linkManager.getUnfetchedLinks().length + (this.config.seedUrls?.length || 0);
      this.logger.info(`Found ${totalUnfetched} URLs to process (including ${this.config.seedUrls?.length || 0} seed URLs), processing ${linksToProcess.length} URLs in this batch`);

      // Process each URL
      for (let i = 0; i < linksToProcess.length; i++) {
        const link = linksToProcess[i];
        this.logProgress(i + 1, linksToProcess.length);
        
        // Mark as fetching
        this.urlProcessingService.markFetching(link.url);
        linksDirty = true;
        
        const success = await this.processUrl(link.url);
        
        if (success) {
          this.statsTracker.incrementCrawled();
        } else {
          this.statsTracker.incrementFailed();
        }

        // Wait between requests
        if (i < linksToProcess.length - 1) {
          await this.sleep(this.config.crawler.waitBetweenRequests);
        }
      }

      if (linksDirty) {
        this.linkManager.saveLinks(this.linksFile, this.linkManager.links);
      }

      // Close browser
      await this.browserManager.close();
      this.logger.info('Browser closed');

      // Generate and display stats
      this.statsTracker.end();
      const stats = this.generateStats();
      this.displayStats(stats);

      // Show remaining unfetched links
      const remainingUnfetched = this.linkManager.getUnfetchedLinks().length;
      if (remainingUnfetched > 0) {
        this.logger.info(`${remainingUnfetched} unfetched URLs remaining. Run again to continue crawling.`);
      }

      this.logger.info('Crawling completed successfully');
    } catch (error) {
      try {
        this.linkManager?.saveLinks(this.linksFile, this.linkManager.links);
      } catch (saveError) {
        this.logger.error('Failed to persist links after fatal error', saveError);
      }
      this.logger.error('Fatal error during crawling', error);
      throw error;
    }
  }

  buildLinksToProcess(batchSize) {
    if (!this.crawlJobService) {
      this.crawlJobService = new CrawlJobService({
        linkManager: this.linkManager,
        config: this.config
      });
    }

    return this.crawlJobService.buildLinksToProcess(batchSize);
  }

  async discoverAndStoreLinks(page) {
    const linkDiscoveryOptions = this.getLinkDiscoveryOptions();
    const newLinks = await this.linkFinder.extractLinks(page, this.config.urlRules, linkDiscoveryOptions);

    if (newLinks.length === 0) {
      return;
    }

    this.logger.info(`Found ${newLinks.length} new links`);
    newLinks.forEach(link => {
      this.linkManager.addLink(link, 'unfetched');
    });
    this.statsTracker.addNewLinks(newLinks.length);
  }

  getLinkDiscoveryOptions() {
    const options = {};
    if (Array.isArray(this.config.linkDiscovery?.prioritizedPatterns)) {
      options.prioritizedPatterns = this.config.linkDiscovery.prioritizedPatterns;
    }
    return options;
  }

  /**
   * Attempt to login at the start of crawling
   * Tries multiple strategies to find and complete login
   * @returns {Promise<boolean>} Success status
   */
  async attemptLogin() {
    return this.loginOrchestrationService.attemptLogin();
  }

  /**
   * Process a single URL
   * @param {string} url - URL to process
   * @returns {boolean} Success status
   */
  async processUrl(url) {
    const startTime = Date.now(); // 记录开始时间

    try {
      this.logger.info(`Processing: ${url}`);

      // Create new page
      const page = await this.browserManager.newPage();

      // Navigate to URL
      await this.browserManager.goto(page, url, this.config.crawler.timeout);
      this.logger.info(`Loaded: ${url}`);

      // Handle login if needed
      if (this.config.login.required && !this.isLoggedIn) {
        const needsLogin = await this.loginHandler.needsLogin(page);
        
        if (needsLogin) {
          this.logger.info('Login required on this page, attempting to log in...');
          const loginSuccess = await this.loginHandler.login(page, {
            username: this.config.login.username,
            password: this.config.login.password
          });

          if (loginSuccess) {
            this.logger.info('Login successful');
            this.isLoggedIn = true;
            
            // Navigate to original URL after login
            if (page.url() !== url) {
              await this.browserManager.goto(page, url, this.config.crawler.timeout);
            }
          } else {
            this.logger.warn('Login failed on this page');
          }
        }
      }

      // Wait for page to load
      await this.browserManager.waitForLoad(page, this.config.crawler.timeout);

      // Expand collapsible content
      await this.linkFinder.expandCollapsibles(page);

      await this.discoverAndStoreLinks(page);

      // Parse page content with streaming support
      let filename = null;
      let filepath = null;
      let isFirstChunk = true;
      let pageTitle = null;
      
      // 先提取页面标题以确定文件名
      pageTitle = await page.evaluate(() => {
        return document.title || '';
      });
      
      // 生成文件名和路径
      const fs = await import('fs');
      const crypto = await import('crypto');
      
      filename = this.markdownGenerator.safeFilename(pageTitle || 'untitled', url);
      filepath = `${this.pagesDir}/${filename}.md`;
      
      // 检查文件是否存在，如果存在则添加hash
      if (fs.existsSync(filepath)) {
        const urlHash = crypto.createHash('md5').update(url).digest('hex').substring(0, 8);
        filename = `${filename}_${urlHash}`;
        filepath = `${this.pagesDir}/${filename}.md`;
      }
      
      const onDataChunk = async (chunk) => {
        try {
          const fs = await import('fs');
          
          // 初始化文件（第一次）
          if (isFirstChunk) {
            // 写入文件头
            const header = `# ${pageTitle || 'Untitled'}\n\n## 源URL\n\n${url}\n\n`;
            fs.writeFileSync(filepath, header, 'utf-8');
            isFirstChunk = false;
          }
          
          // 追加数据块
          if (chunk.type === 'table') {
            if (chunk.isFirstPage) {
              // 新表格开始
              let tableContent = `\n## 表格 ${chunk.tableIndex + 1}\n\n`;
              
              // 表头
              if (chunk.headers && chunk.headers.length > 0) {
                tableContent += '| ' + chunk.headers.join(' | ') + ' |\n';
                tableContent += '| ' + chunk.headers.map(() => '---').join(' | ') + ' |\n';
              }
              
              // 数据行
              if (chunk.rows && chunk.rows.length > 0) {
                chunk.rows.forEach(row => {
                  tableContent += '| ' + row.join(' | ') + ' |\n';
                });
              }
              
              fs.appendFileSync(filepath, tableContent, 'utf-8');
              this.logger.debug(`Appended table ${chunk.tableIndex + 1}, page ${chunk.page}`);
            } else if (!chunk.isLastPage && chunk.rows && chunk.rows.length > 0) {
              // 追加数据行
              let rowsContent = '';
              chunk.rows.forEach(row => {
                rowsContent += '| ' + row.join(' | ') + ' |\n';
              });
              fs.appendFileSync(filepath, rowsContent, 'utf-8');
              this.logger.debug(`Appended ${chunk.rows.length} rows to table ${chunk.tableIndex + 1}, page ${chunk.page}`);
            }
          } else if (chunk.type === 'table-new') {
            // 结构变化，新表格
            let tableContent = `\n## 表格 ${chunk.tableIndex + 1} (结构变化)\n\n`;
            
            if (chunk.headers && chunk.headers.length > 0) {
              tableContent += '| ' + chunk.headers.join(' | ') + ' |\n';
              tableContent += '| ' + chunk.headers.map(() => '---').join(' | ') + ' |\n';
            }
            
            if (chunk.rows && chunk.rows.length > 0) {
              chunk.rows.forEach(row => {
                tableContent += '| ' + row.join(' | ') + ' |\n';
              });
            }
            
            fs.appendFileSync(filepath, tableContent, 'utf-8');
            this.logger.info(`Started new table ${chunk.tableIndex + 1} due to structure change`);
          } else if (chunk.type === 'tab') {
            // Tab页内容（只有数据变化时才会收到）
            let tabContent = `\n## Tab页: ${chunk.name}\n\n`;
            
            // 添加段落
            if (chunk.data.paragraphs && chunk.data.paragraphs.length > 0) {
              chunk.data.paragraphs.forEach(p => {
                if (p.trim()) {
                  tabContent += p + '\n\n';
                }
              });
            }
            
            // 添加列表
            if (chunk.data.lists && chunk.data.lists.length > 0) {
              chunk.data.lists.forEach(list => {
                list.items.forEach((item, i) => {
                  if (list.type === 'ol') {
                    tabContent += `${i + 1}. ${item}\n`;
                  } else {
                    tabContent += `- ${item}\n`;
                  }
                });
                tabContent += '\n';
              });
            }
            
            // 添加表格
            if (chunk.data.tables && chunk.data.tables.length > 0) {
              chunk.data.tables.forEach(table => {
                if (table.headers && table.headers.length > 0) {
                  tabContent += '| ' + table.headers.join(' | ') + ' |\n';
                  tabContent += '| ' + table.headers.map(() => '---').join(' | ') + ' |\n';
                  
                  if (table.rows && table.rows.length > 0) {
                    table.rows.forEach(row => {
                      tabContent += '| ' + row.join(' | ') + ' |\n';
                    });
                  }
                  tabContent += '\n';
                }
              });
            }
            
            // 添加代码块
            if (chunk.data.codeBlocks && chunk.data.codeBlocks.length > 0) {
              chunk.data.codeBlocks.forEach(block => {
                tabContent += `\`\`\`${block.language}\n${block.code}\n\`\`\`\n\n`;
              });
            }
            
            fs.appendFileSync(filepath, tabContent, 'utf-8');
            this.logger.debug(`Appended tab content: ${chunk.name}`);
          } else if (chunk.type === 'dropdown-option') {
            // 下拉框选项内容（只有数据变化时才会收到）
            let dropdownContent = `\n## 下拉框: ${chunk.dropdown} - 选项: ${chunk.option}\n\n`;
            
            // 添加段落
            if (chunk.data.paragraphs && chunk.data.paragraphs.length > 0) {
              chunk.data.paragraphs.forEach(p => {
                if (p.trim()) {
                  dropdownContent += p + '\n\n';
                }
              });
            }
            
            // 添加列表
            if (chunk.data.lists && chunk.data.lists.length > 0) {
              chunk.data.lists.forEach(list => {
                list.items.forEach((item, i) => {
                  if (list.type === 'ol') {
                    dropdownContent += `${i + 1}. ${item}\n`;
                  } else {
                    dropdownContent += `- ${item}\n`;
                  }
                });
                dropdownContent += '\n';
              });
            }
            
            // 添加表格
            if (chunk.data.tables && chunk.data.tables.length > 0) {
              chunk.data.tables.forEach(table => {
                if (table.headers && table.headers.length > 0) {
                  dropdownContent += '| ' + table.headers.join(' | ') + ' |\n';
                  dropdownContent += '| ' + table.headers.map(() => '---').join(' | ') + ' |\n';
                  
                  if (table.rows && table.rows.length > 0) {
                    table.rows.forEach(row => {
                      dropdownContent += '| ' + row.join(' | ') + ' |\n';
                    });
                  }
                  dropdownContent += '\n';
                }
              });
            }
            
            // 添加代码块
            if (chunk.data.codeBlocks && chunk.data.codeBlocks.length > 0) {
              chunk.data.codeBlocks.forEach(block => {
                dropdownContent += `\`\`\`${block.language}\n${block.code}\n\`\`\`\n\n`;
              });
            }
            
            fs.appendFileSync(filepath, dropdownContent, 'utf-8');
            this.logger.debug(`Appended dropdown option: ${chunk.dropdown} - ${chunk.option}`);
          } else if (chunk.type === 'date-filter') {
            // 日期筛选内容
            let dateFilterContent = `\n## 时间筛选: ${chunk.range}\n\n`;
            dateFilterContent += `时间范围: ${chunk.startDate} 至 ${chunk.endDate}\n\n`;
            
            // 添加表格数据
            if (chunk.tables && chunk.tables.length > 0) {
              chunk.tables.forEach((table, idx) => {
                dateFilterContent += `### 表格 ${idx + 1}\n\n`;
                
                if (table.headers && table.headers.length > 0) {
                  dateFilterContent += '| ' + table.headers.join(' | ') + ' |\n';
                  dateFilterContent += '| ' + table.headers.map(() => '---').join(' | ') + ' |\n';
                  
                  if (table.rows && table.rows.length > 0) {
                    table.rows.forEach(row => {
                      dateFilterContent += '| ' + row.join(' | ') + ' |\n';
                    });
                  }
                  dateFilterContent += '\n';
                }
              });
            }
            
            fs.appendFileSync(filepath, dateFilterContent, 'utf-8');
            this.logger.debug(`Appended date filter data: ${chunk.range}`);
          }
        } catch (error) {
          this.logger.error(`Failed to write data chunk: ${error.message}`);
        }
      };
      
      const pageData = await this.pageParser.parsePage(page, url, { 
        onDataChunk,
        filepath,
        pagesDir: this.pagesDir,
        parserMode: this.config.parser?.mode
      });
      this.logger.info(`Parsed page: ${pageData.title || 'Untitled'}`);

      if (this.llmDataExtractor?.isEnabled()) {
        const llmExtraction = await this.llmDataExtractor.extract(pageData, { url });
        if (llmExtraction) {
          pageData.llmExtraction = llmExtraction;
          this.logger.info(`LLM数据抽取完成: ${llmExtraction.records.length} 条记录`);
        }
      }

      // 大表格页面：仅保存为CSV
      if (pageData.type === 'table-only') {
        const savedCsvFiles = await this.saveTablesAsCsv(pageData, url);
        this.logger.info(`Saved ${savedCsvFiles.length} CSV file(s) for table-only page`);
      }
      // 如果没有使用流式写入（没有分页数据），使用传统方式
      else if (isFirstChunk) {
        const markdown = this.markdownGenerator.generate(pageData);
        filename = this.markdownGenerator.safeFilename(pageData.title || 'untitled', url);
        
        const fs = await import('fs');
        filepath = `${this.pagesDir}/${filename}.md`;
        if (fs.existsSync(filepath)) {
          const crypto = await import('crypto');
          const urlHash = crypto.createHash('md5').update(url).digest('hex').substring(0, 8);
          filename = `${filename}_${urlHash}`;
          this.logger.info(`File exists, using unique filename: ${filename}.md`);
        }
        
        filepath = this.markdownGenerator.saveToFile(
          markdown,
          filename,
          this.pagesDir
        );
      }


      if (pageData.llmExtraction && filepath) {
        const fs = await import('fs');
        const llmSection = `
## LLM结构化抽取

模型: ${pageData.llmExtraction.model}

\`\`\`json
${JSON.stringify(pageData.llmExtraction, null, 2)}
\`\`\`
`;
        fs.appendFileSync(filepath, llmSection, 'utf-8');
      }

      if (pageData.type !== 'table-only' && filepath) {
        const savedPath = await this.pageStorage.persistMarkdown({
          filepath,
          url,
          title: pageData.title || pageTitle,
          filename
        });

        if (this.pageStorage.isLanceDb()) {
          this.logger.info(`Persisted page content to ${savedPath}`);
        }
      }
      
      this.statsTracker.incrementFilesGenerated();
      
      // 计算处理时间
      const duration = ((Date.now() - startTime) / 1000).toFixed(2);
      if (pageData.type === 'table-only') {
        this.logger.success(`Saved table CSV output (${duration}s)`);
      } else {
        this.logger.success(`Saved: ${filename}.md (${duration}s)`);
      }

      // Close page
      await page.close();

      // Update link status to fetched
      this.urlProcessingService.markFetched(url);
      this.metricsAdapter.increment('crawl_success_total');

      return true;
    } catch (error) {
      // 计算处理时间（即使失败也记录）
      const duration = ((Date.now() - startTime) / 1000).toFixed(2);
      this.logError(url, error, duration);

      this.urlProcessingService.handleFailure(url, error);
      this.metricsAdapter.increment('crawl_failed_total');
      
      return false;
    }
  }

  escapeCsvField(value) {
    const stringValue = value == null ? '' : String(value);
    const escaped = stringValue.replace(/"/g, '""');
    if (/[",\n]/.test(escaped)) {
      return `"${escaped}"`;
    }
    return escaped;
  }

  async saveTablesAsCsv(pageData, url) {
    const fs = await import('fs');
    const crypto = await import('crypto');

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


  /**
   * Log progress
   * @param {number} current - Current progress
   * @param {number} total - Total count
   */
  logProgress(current, total) {
    const percentage = ((current / total) * 100).toFixed(1);
    this.logger.info(`Progress: ${current}/${total} (${percentage}%)`);
  }

  /**
   * Log error
   * @param {string} url - URL that caused error
   * @param {Error} error - Error object
   * @param {string} duration - Processing duration in seconds
   */
  logError(url, error, duration = null) {
    const durationStr = duration ? ` (${duration}s)` : '';
    this.logger.error(`Error processing ${url}${durationStr}`, error);
  }

  /**
   * Generate statistics
   * @returns {Object} Statistics object
   */
  generateStats() {
    return this.statsTracker.getStats();
  }

  /**
   * Display statistics
   * @param {Object} stats - Statistics object
   */
  displayStats(stats) {
    this.logger.info('=== Crawling Statistics ===');
    this.logger.info(`Total URLs: ${stats.totalUrls}`);
    this.logger.info(`Crawled: ${stats.crawledUrls}`);
    this.logger.info(`Failed: ${stats.failedUrls}`);
    this.logger.info(`New Links Found: ${stats.newLinksFound}`);
    this.logger.info(`Files Generated: ${stats.filesGenerated}`);
    this.logger.info(`Duration: ${stats.duration}s`);

    const metrics = this.metricsAdapter.snapshot();
    if (Object.keys(metrics).length > 0) {
      this.logger.info(`Metrics: ${JSON.stringify(metrics)}`);
    }
  }

  /**
   * Sleep utility
   * @param {number} ms - Milliseconds to sleep
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

export default CrawlerMain;
