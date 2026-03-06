import CrawlJobService from './application/crawl-job-service.js';
import CrawlerBootstrapService from './application/crawler-bootstrap-service.js';
import LoginOrchestrationService from './application/login-orchestration-service.js';
import PageOutputService from './application/page-output-service.js';

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
    this.pageOutputService = null;
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
    this.pageOutputService = new PageOutputService({
      logger: this.logger,
      markdownGenerator: this.markdownGenerator,
      pageStorage: this.pageStorage,
      pagesDir: this.pagesDir
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
    const startTime = Date.now();

    try {
      this.logger.info(`Processing: ${url}`);

      const page = await this.browserManager.newPage();
      await this.browserManager.goto(page, url, this.config.crawler.timeout);
      this.logger.info(`Loaded: ${url}`);

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

            if (page.url() !== url) {
              await this.browserManager.goto(page, url, this.config.crawler.timeout);
            }
          } else {
            this.logger.warn('Login failed on this page');
          }
        }
      }

      await this.browserManager.waitForLoad(page, this.config.crawler.timeout);
      await this.linkFinder.expandCollapsibles(page);
      await this.discoverAndStoreLinks(page);

      const pageTitle = await page.evaluate(() => {
        return document.title || '';
      });

      const outputContext = this.pageOutputService.createOutputContext(pageTitle, url);
      const onDataChunk = this.pageOutputService.createChunkWriter(outputContext, url);

      const pageData = await this.pageParser.parsePage(page, url, {
        onDataChunk,
        filepath: outputContext.filepath,
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

      if (pageData.type === 'table-only') {
        const savedCsvFiles = await this.pageOutputService.saveTablesAsCsv(pageData, url);
        this.logger.info(`Saved ${savedCsvFiles.length} CSV file(s) for table-only page`);
      } else if (outputContext.isFirstChunk) {
        this.pageOutputService.writeFallbackMarkdown(pageData, url, outputContext);
      }

      if (pageData.llmExtraction && outputContext.filepath) {
        this.pageOutputService.appendLlmSection(outputContext.filepath, pageData.llmExtraction);
      }

      if (pageData.type !== 'table-only' && outputContext.filepath) {
        await this.pageOutputService.persistMarkdown(
          outputContext.filepath,
          url,
          pageData.title || pageTitle,
          outputContext.filename
        );
      }

      this.statsTracker.incrementFilesGenerated();

      const duration = ((Date.now() - startTime) / 1000).toFixed(2);
      if (pageData.type === 'table-only') {
        this.logger.success(`Saved table CSV output (${duration}s)`);
      } else {
        this.logger.success(`Saved: ${outputContext.filename}.md (${duration}s)`);
      }

      await page.close();

      this.urlProcessingService.markFetched(url);
      this.metricsAdapter.increment('crawl_success_total');

      return true;
    } catch (error) {
      const duration = ((Date.now() - startTime) / 1000).toFixed(2);
      this.logError(url, error, duration);

      this.urlProcessingService.handleFailure(url, error);
      this.metricsAdapter.increment('crawl_failed_total');

      return false;
    }
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
