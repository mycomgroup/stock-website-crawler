#!/usr/bin/env node
import './load-env.js';
import { THSQuantClient } from './request/thsquant-client.js';
import { ensureTHSQuantSession } from './browser/session-manager.js';

async function listStrategies() {
  try {
    console.log('Fetching THSQuant strategies...\n');
    
    const credentials = {
      username: process.env.THSQUANT_USERNAME,
      password: process.env.THSQUANT_PASSWORD
    };
    const cookies = await ensureTHSQuantSession(credentials);
    
    const client = new THSQuantClient({ cookies });
    
    // Check login
    const loginStatus = await client.checkLogin();
    if (loginStatus.code === -1) {
      console.error('Error: Not logged in');
      return;
    }
    
    // List strategies
    const strategies = await client.listStrategies();
    
    if (strategies.length === 0) {
      console.log('No strategies found');
      return;
    }
    
    console.log(`Found ${strategies.length} strategies:\n`);
    console.log('ID'.padEnd(20) + 'Name');
    console.log('-'.repeat(40));
    
    strategies.forEach(s => {
      console.log((s.id || 'N/A').padEnd(20) + (s.name || 'Unnamed'));
    });
    
  } catch (e) {
    console.error('Error:', e.message);
  }
}

listStrategies();