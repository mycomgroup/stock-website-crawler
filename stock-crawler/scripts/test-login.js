#!/usr/bin/env node

/**
 * Test Login Functionality
 * 
 * This script tests the login functionality without running the full crawler.
 * Useful for debugging login issues.
 */

import CrawlerMain from '../src/crawler-main.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function testLogin() {
  try {
    // Get config file path from command line
    const configPath = process.argv[2];
    
    if (!configPath) {
      console.error('Usage: node scripts/test-login.js <config-file>');
      console.error('Example: node scripts/test-login.js config/lixinger.json');
      process.exit(1);
    }

    const resolvedConfigPath = path.isAbsolute(configPath) 
      ? configPath 
      : path.resolve(process.cwd(), configPath);

    console.log('Testing Login Functionality');
    console.log('===========================\n');
    console.log(`Configuration: ${resolvedConfigPath}\n`);

    // Initialize crawler
    const crawler = new CrawlerMain();
    await crawler.initialize(resolvedConfigPath);

    // Check if login is required
    if (!crawler.config.login.required) {
      console.log('Login is not required in this configuration.');
      process.exit(0);
    }

    console.log('Login is required, attempting to login...\n');

    // Launch browser
    await crawler.browserManager.launch({
      headless: crawler.config.crawler.headless
    });
    console.log(`Browser launched (headless: ${crawler.config.crawler.headless})\n`);

    // Attempt login
    const loginSuccess = await crawler.attemptLogin();

    if (loginSuccess) {
      console.log('\n✓ Login test PASSED');
      console.log('Login was successful!');
      
      // Verify by visiting a protected page
      console.log('\nVerifying login by visiting a protected page...');
      const page = await crawler.browserManager.newPage();
      const testUrl = crawler.config.seedUrls[0];
      await crawler.browserManager.goto(page, testUrl, crawler.config.crawler.timeout);
      await crawler.browserManager.waitForLoad(page, crawler.config.crawler.timeout);
      
      const needsLogin = await crawler.loginHandler.needsLogin(page);
      if (needsLogin) {
        console.log('✗ Verification FAILED: Still showing login page');
      } else {
        console.log('✓ Verification PASSED: Successfully accessed protected page');
      }
      
      await page.close();
    } else {
      console.log('\n✗ Login test FAILED');
      console.log('Login was not successful. Check the logs above for details.');
    }

    // Close browser
    await crawler.browserManager.close();
    console.log('\nBrowser closed');

    process.exit(loginSuccess ? 0 : 1);
  } catch (error) {
    console.error('\nError:', error.message);
    if (process.env.DEBUG) {
      console.error(error.stack);
    }
    process.exit(1);
  }
}

testLogin();
