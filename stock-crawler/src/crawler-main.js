import ConfigManager from './config-manager.js';
import LinkManager from './link-manager.js';
import LinkFinder from './link-finder.js';
import PageParser from './page-parser.js';
import MarkdownGenerator from './parsers/markdown-generator.js';
import Logger from './logger.js';
import StatsTracker from './stats-tracker.js';
import PageStorage from './storage/page-storage.js';
import LLMDataExtractor from './parsers/llm-data-extractor.js';
import CrawlJobService from './application/crawl-job-service.js';
import UrlProcessingService from './application/url-processing-service.js';
import MetricsAdapter from './infrastructure/metrics-adapter.js';
import BrowserCrawlProcessor from './application/browser-crawl-processor.js';

class CrawlerMain {
  constructor() {
    this.config = null;
    this.linkManager = null;
    this.linkFinder = null;
    this.pageParser = null;
    this.markdownGenerator = null;
    this.logger = null;
    this.statsTracker = null;
    this.pageStorage = null;
    this.llmDataExtractor = null;
    this.crawlJobService = null;
    this.urlProcessingService = null;
    this.metricsAdapter = null;
    this.browserCrawlProcessor = null;
  }

  /**
   * Initialize crawler with configuration
   * @param {string} configPath - Path to configuration file
   */
  async initialize(configPath) {
    // Load configuration first
    const configManager = new ConfigManager();
    this.config = configManager.loadConfig(configPath);
    
    // Setup project directory structure
    // output/project-name/
    this.projectDir = `${this.config.output.directory}/${this.config.name}`;
    this.logsDir = `${this.projectDir}/logs`;
    this.linksFile = `${this.projectDir}/links.txt`;
    
    // Create directories if they don't exist
    const fs = await import('fs');
    if (!fs.existsSync(this.projectDir)) {
      fs.mkdirSync(this.projectDir, { recursive: true });
    }
    if (!fs.existsSync(this.logsDir)) {
      fs.mkdirSync(this.logsDir, { recursive: true });
    }
    
    // Initialize logger with project-specific log directory
    this.logger = new Logger(this.logsDir, this.config.crawler.logLevel || 'INFO');
    this.statsTracker = new StatsTracker();
    
    // Create pages directory with timestamp suffix matching log file
    const timestamp = this.logger.getTimestamp();
    this.pagesDir = `${this.projectDir}/pages-${timestamp}`;
    if (!fs.existsSync(this.pagesDir)) {
      fs.mkdirSync(this.pagesDir, { recursive: true });
    }
    
    this.logger.info(`Loaded configuration: ${this.config.name}`);

    // Initialize link manager
    this.linkManager = new LinkManager();
    this.linkManager.loadLinks(this.linksFile);
    this.logger.info(`Loaded ${this.linkManager.links.length} links from ${this.linksFile}`);
    
    // If no links loaded, initialize with seed URLs
    if (this.linkManager.links.length === 0 && this.config.seedUrls && this.config.seedUrls.length > 0) {
      this.logger.info(`Initializing with ${this.config.seedUrls.length} seed URLs`);
      this.config.seedUrls.forEach(url => {
        // Seed URLs must be marked as unfetched so they can enter normal processing flow
        this.linkManager.addLink(url, 'unfetched');
      });
      this.linkManager.saveLinks(this.linksFile, this.linkManager.links);
    }

    // Initialize other modules
    this.linkFinder = new LinkFinder();
    this.pageParser = new PageParser();
    this.markdownGenerator = new MarkdownGenerator();
    this.pageStorage = new PageStorage(this.config, this.logger);
    await this.pageStorage.initialize(this.projectDir);
    this.llmDataExtractor = new LLMDataExtractor(this.config.llmExtraction || {}, this.logger);
    this.crawlJobService = new CrawlJobService({
      linkManager: this.linkManager,
      config: this.config
    });
    this.urlProcessingService = new UrlProcessingService(
      this.linkManager,
      this.logger,
      this.config.crawler.maxRetries || 3
    );
    this.metricsAdapter = new MetricsAdapter(this.logger);
    this.browserCrawlProcessor = new BrowserCrawlProcessor({
      config: this.config,
      logger: this.logger,
      linkFinder: this.linkFinder,
      pageParser: this.pageParser,
      markdownGenerator: this.markdownGenerator,
      pagesDir: this.pagesDir,
      statsTracker: this.statsTracker,
      pageStorage: this.pageStorage,
      llmDataExtractor: this.llmDataExtractor,
      urlProcessingService: this.urlProcessingService,
      metricsAdapter: this.metricsAdapter,
      discoverAndStoreLinks: (page) => this.discoverAndStoreLinks(page),
      saveTablesAsCsv: (pageData, url) => this.saveTablesAsCsv(pageData, url),
      logError: (url, error, duration) => this.logError(url, error, duration)
    });

    this.logger.info(`Project directory: ${this.projectDir}`);
    this.logger.info(`Pages directory: ${this.pagesDir}`);
    this.logger.info(`Logs directory: ${this.logsDir}`);
    this.logger.info('Crawler initialized successfully');
  }

  /**
   * Start crawling process
   */
  async start() {
    try {
      this.logger.info('Starting crawler...');
      this.statsTracker.start();

      // Launch browser
      await this.browserCrawlProcessor.launch();
      this.logger.info(`Browser launched (headless: ${this.config.crawler.headless})`);

      // Attempt login at the start if required
      if (this.config.login.required) {
        this.logger.info('Login is required, attempting to login at start...');
        const loginSuccess = await this.browserCrawlProcessor.attemptInitialLogin();
        if (loginSuccess) {
          this.logger.info('Login successful at start');
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
        
        const success = await this.browserCrawlProcessor.processUrl(link.url);
        
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
      await this.browserCrawlProcessor.close();
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
