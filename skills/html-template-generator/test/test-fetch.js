/**
 * Integration test for page fetching functionality
 * This test requires a running browser and network access
 * Run with: node test/test-fetch.js
 */

import { BrowserManager } from '../lib/browser-manager.js';
import { HTMLFetcher } from '../lib/html-fetcher.js';

async function testFetch() {
  console.log('🧪 Testing Page Fetching Functionality\n');
  
  const browserManager = new BrowserManager({
    headless: true,
    userDataDir: '../../stock-crawler/chrome_user_data'
  });
  
  try {
    // Test 1: Launch browser
    console.log('Test 1: Launching browser...');
    await browserManager.launch();
    console.log('✓ Browser launched successfully\n');
    
    const fetcher = new HTMLFetcher(browserManager);
    
    // Test 2: Fetch single URL
    console.log('Test 2: Fetching single URL...');
    const testUrl = 'https://example.com';
    const result = await fetcher.fetchOne(testUrl);
    
    console.log(`✓ URL: ${result.url}`);
    console.log(`✓ Title: ${result.title}`);
    console.log(`✓ HTML length: ${result.html.length} characters`);
    console.log(`✓ Timestamp: ${result.timestamp}\n`);
    
    // Validate result
    if (!result.html || result.html.length === 0) {
      throw new Error('HTML content is empty');
    }
    if (!result.title) {
      throw new Error('Title is missing');
    }
    
    // Test 3: Fetch multiple URLs
    console.log('Test 3: Fetching multiple URLs...');
    const urls = [
      'https://example.com',
      'https://example.org'
    ];
    
    const results = await fetcher.fetchAll(urls);
    console.log(`✓ Fetched ${results.length} pages successfully\n`);
    
    results.forEach((r, i) => {
      console.log(`  Page ${i + 1}:`);
      console.log(`    URL: ${r.url}`);
      console.log(`    Title: ${r.title}`);
      console.log(`    HTML length: ${r.html.length} characters`);
    });
    
    if (results.length !== urls.length) {
      throw new Error(`Expected ${urls.length} results, got ${results.length}`);
    }
    
    // Test 4: Handle invalid URL (should not crash)
    console.log('\nTest 4: Testing error handling...');
    const invalidResults = await fetcher.fetchAll(['https://invalid-url-that-does-not-exist-12345.com']);
    console.log(`✓ Error handled gracefully (${invalidResults.length} successful fetches)\n`);
    
    // Test 5: Timeout handling
    console.log('Test 5: Testing timeout...');
    fetcher.setTimeout(5000);
    console.log('✓ Timeout set to 5000ms\n');
    
    console.log('✅ All tests passed!');
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    process.exit(1);
  } finally {
    // Cleanup
    console.log('\nClosing browser...');
    await browserManager.close();
    console.log('✓ Browser closed');
  }
}

// Run tests
testFetch().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
