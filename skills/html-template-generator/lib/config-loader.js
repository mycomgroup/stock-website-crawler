/**
 * Configuration Loader
 * 
 * Loads and merges configuration from multiple sources:
 * 1. Default config (config/default.json)
 * 2. Custom config file (--config parameter)
 * 3. Command-line arguments
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export class ConfigLoader {
  constructor() {
    this.defaultConfigPath = path.join(__dirname, '../config/default.json');
  }

  /**
   * Load configuration with priority:
   * CLI args > custom config > default config
   */
  async load(customConfigPath = null, cliArgs = {}) {
    // Load default config
    const defaultConfig = await this._loadJsonFile(this.defaultConfigPath);
    
    // Load custom config if provided
    let customConfig = {};
    if (customConfigPath) {
      customConfig = await this._loadJsonFile(customConfigPath);
    }
    
    // Merge configs: default < custom < CLI
    const merged = this._deepMerge(defaultConfig, customConfig);
    const final = this._applyCLIArgs(merged, cliArgs);
    
    return final;
  }

  /**
   * Load JSON file
   */
  async _loadJsonFile(filePath) {
    try {
      const content = await fs.readFile(filePath, 'utf-8');
      return JSON.parse(content);
    } catch (error) {
      if (error.code === 'ENOENT') {
        throw new Error(`Config file not found: ${filePath}`);
      }
      throw new Error(`Failed to parse config file ${filePath}: ${error.message}`);
    }
  }

  /**
   * Deep merge two objects
   */
  _deepMerge(target, source) {
    const result = { ...target };
    
    for (const key in source) {
      if (source[key] instanceof Object && !Array.isArray(source[key])) {
        result[key] = this._deepMerge(result[key] || {}, source[key]);
      } else {
        result[key] = source[key];
      }
    }
    
    return result;
  }

  /**
   * Apply CLI arguments to config
   */
  _applyCLIArgs(config, cliArgs) {
    const result = { ...config };
    
    // Browser settings
    if (cliArgs.headless !== undefined) {
      result.browser.headless = cliArgs.headless;
    }
    if (cliArgs.timeout !== undefined) {
      result.browser.timeout = cliArgs.timeout;
    }
    if (cliArgs.userDataDir !== undefined) {
      result.browser.userDataDir = cliArgs.userDataDir;
    }
    
    // Fetching settings
    if (cliArgs.maxSamples !== undefined) {
      result.fetching.maxSamples = cliArgs.maxSamples;
    }
    if (cliArgs.minSamples !== undefined) {
      result.fetching.minSamples = cliArgs.minSamples;
    }
    if (cliArgs.waitTime !== undefined) {
      result.fetching.waitTime = cliArgs.waitTime;
    }
    if (cliArgs.waitForSelector !== undefined) {
      result.fetching.waitForSelector = cliArgs.waitForSelector;
    }
    
    // Analysis settings
    if (cliArgs.frequencyThreshold !== undefined) {
      result.analysis.frequencyThreshold = cliArgs.frequencyThreshold;
    }
    if (cliArgs.detectPageType !== undefined) {
      result.analysis.detectPageType = cliArgs.detectPageType;
    }
    
    // Pattern filtering
    if (cliArgs.includePatterns !== undefined) {
      result.patterns.include = this._parsePatternList(cliArgs.includePatterns);
    }
    if (cliArgs.excludePatterns !== undefined) {
      result.patterns.exclude = this._parsePatternList(cliArgs.excludePatterns);
    }
    if (cliArgs.priorityPatterns !== undefined) {
      result.patterns.priority = this._parsePatternList(cliArgs.priorityPatterns);
    }
    
    // Output settings
    if (cliArgs.generatePreview !== undefined) {
      result.output.generatePreview = cliArgs.generatePreview;
    }
    
    return result;
  }

  /**
   * Parse comma-separated pattern list
   */
  _parsePatternList(str) {
    if (Array.isArray(str)) return str;
    return str.split(',').map(s => s.trim()).filter(s => s);
  }

  /**
   * List available config files
   */
  async listConfigs() {
    const configDir = path.join(__dirname, '../config');
    const files = await fs.readdir(configDir);
    const configs = [];
    
    for (const file of files) {
      if (file.endsWith('.json')) {
        const filePath = path.join(configDir, file);
        try {
          const content = await this._loadJsonFile(filePath);
          configs.push({
            name: file,
            path: filePath,
            description: content.description || 'No description'
          });
        } catch (error) {
          // Skip invalid files
        }
      }
    }
    
    return configs;
  }

  /**
   * Validate configuration
   */
  validate(config) {
    const errors = [];
    
    // Required sections
    if (!config.browser) errors.push('Missing browser configuration');
    if (!config.fetching) errors.push('Missing fetching configuration');
    if (!config.analysis) errors.push('Missing analysis configuration');
    
    // Value ranges
    if (config.analysis.frequencyThreshold < 0 || config.analysis.frequencyThreshold > 1) {
      errors.push('frequencyThreshold must be between 0 and 1');
    }
    if (config.fetching.maxSamples < 1) {
      errors.push('maxSamples must be at least 1');
    }
    if (config.fetching.minSamples > config.fetching.maxSamples) {
      errors.push('minSamples cannot be greater than maxSamples');
    }
    
    if (errors.length > 0) {
      throw new Error('Configuration validation failed:\n' + errors.join('\n'));
    }
    
    return true;
  }
}
