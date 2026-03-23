#!/usr/bin/env node
import { readFileSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const CONFIG_DIR = join(__dirname, '../config/hao123-sites');
const MASTER_CONFIG_PATH = join(CONFIG_DIR, 'master-config.json');

async function runCrawler(configPath) {
  return new Promise((resolve, reject) => {
    console.log(`\n🚀 Starting crawler with config: ${configPath}`);
    
    const crawler = spawn('node', ['src/index.js', configPath], {
      cwd: join(__dirname, '..'),
      stdio: 'inherit'
    });
    
    crawler.on('close', (code) => {
      if (code === 0) {
        console.log(`✅ Crawler completed successfully`);
        resolve();
      } else {
        console.error(`❌ Crawler failed with code ${code}`);
        reject(new Error(`Crawler exited with code ${code}`));
      }
    });
    
    crawler.on('error', (error) => {
      console.error(`❌ Failed to start crawler:`, error);
      reject(error);
    });
  });
}

async function main() {
  console.log('🎯 Testing all hao123 site configurations...\n');
  
  try {
    // Read master config
    const masterConfig = JSON.parse(readFileSync(MASTER_CONFIG_PATH, 'utf-8'));
    console.log(`📋 Found ${masterConfig.totalSites} sites to test\n`);
    
    const results = {
      total: masterConfig.totalSites,
      success: 0,
      failed: 0,
      errors: []
    };
    
    // Test each site
    for (let i = 0; i < masterConfig.sites.length; i++) {
      const site = masterConfig.sites[i];
      const configPath = join(CONFIG_DIR, site.configFile);
      
      console.log(`\n${'='.repeat(60)}`);
      console.log(`[${i + 1}/${masterConfig.totalSites}] Testing: ${site.title}`);
      console.log(`Host: ${site.host}`);
      console.log(`Config: ${site.configFile}`);
      console.log('='.repeat(60));
      
      try {
        await runCrawler(configPath);
        results.success++;
      } catch (error) {
        results.failed++;
        results.errors.push({
          site: site.name,
          host: site.host,
          error: error.message
        });
      }
    }
    
    // Print summary
    console.log(`\n${'='.repeat(60)}`);
    console.log('📊 TEST SUMMARY');
    console.log('='.repeat(60));
    console.log(`Total sites: ${results.total}`);
    console.log(`✅ Successful: ${results.success}`);
    console.log(`❌ Failed: ${results.failed}`);
    
    if (results.errors.length > 0) {
      console.log(`\n❌ Failed sites:`);
      results.errors.forEach((err, idx) => {
        console.log(`  ${idx + 1}. ${err.host}: ${err.error}`);
      });
    }
    
    console.log('='.repeat(60));
    
  } catch (error) {
    console.error('❌ Test suite failed:', error);
    process.exit(1);
  }
}

main().catch(console.error);
