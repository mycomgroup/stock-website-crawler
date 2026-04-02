#!/usr/bin/env node
import { chromium } from 'playwright';
import '../load-env.js';
import { SESSION_FILE } from '../paths.js';
import fs from 'fs';

console.log('='.repeat(60));
console.log('BigQuant Manual Session Capture');
console.log('='.repeat(60));
console.log('\nThis script will open BigQuant in a browser.');
console.log('Please log in manually, then press Enter in this terminal.');
console.log('The session will be saved automatically.\n');

async function manualCapture() {
  console.log('Launching browser...');
  
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 }
  });
  
  const page = await context.newPage();
  
  try {
    await page.goto('https://bigquant.com', { waitUntil: 'networkidle' });
    
    console.log('\n✓ Browser opened. Please log in manually now.');
    console.log('Waiting for you to complete login...');
    console.log('(After logging in, press Enter in this terminal to continue)\n');
    
    await new Promise(resolve => {
      process.stdin.once('data', () => {
        resolve();
      });
    });
    
    console.log('\nCapturing session...');
    const cookies = await context.cookies();
    
    if (cookies.length === 0) {
      console.log('✗ No cookies found. Please try again.');
      await browser.close();
      return false;
    }
    
    const session = {
      cookies,
      timestamp: Date.now()
    };
    
    const dir = './data';
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    fs.writeFileSync(SESSION_FILE, JSON.stringify(session, null, 2));
    console.log(`✓ Session saved to ${SESSION_FILE}`);
    console.log(`  Cookies: ${cookies.length}`);
    
    console.log('\nVerifying session...');
    const hasSession = cookies.some(c => 
      c.name.toLowerCase().includes('session') ||
      c.name.toLowerCase().includes('token') ||
      c.name.toLowerCase().includes('jwt')
    );
    
    if (hasSession) {
      console.log('✓ Valid session token found');
    } else {
      console.log('⚠ Warning: No clear session token found');
      console.log('  Cookies may still work, try running tests');
    }
    
    await browser.close();
    
    console.log('\n' + '='.repeat(60));
    console.log('✓ Manual capture completed successfully');
    console.log('='.repeat(60));
    console.log('\nNext steps:');
    console.log('  1. Run: npm run test:session');
    console.log('  2. Run: npm run list');
    
    return true;
    
  } catch (error) {
    console.error('\n✗ Error:', error.message);
    await browser.close();
    return false;
  }
}

manualCapture().then(success => {
  process.exit(success ? 0 : 1);
});