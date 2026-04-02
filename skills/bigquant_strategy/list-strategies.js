#!/usr/bin/env node
import './load-env.js';
import { BigQuantClient } from './request/bigquant-client.js';
import { ensureBigQuantSession } from './browser/session-manager.js';

async function listStrategies() {
  console.log('='.repeat(60));
  console.log('BigQuant Strategy List');
  console.log('='.repeat(60));
  
  try {
    const credentials = {
      username: process.env.BIGQUANT_USERNAME,
      password: process.env.BIGQUANT_PASSWORD
    };
    
    const cookies = await ensureBigQuantSession(credentials);
    const client = new BigQuantClient({ cookies });
    
    console.log('\nFetching strategies...\n');
    
    const strategies = await client.listStrategies();
    
    if (strategies.length === 0) {
      console.log('No strategies found.');
      return;
    }
    
    console.log(`Found ${strategies.length} strategies:\n`);
    
    strategies.forEach((s, i) => {
      console.log(`${i + 1}. ID: ${s.id}`);
      console.log(`   Name: ${s.name}`);
      if (s.path) console.log(`   Path: ${s.path}`);
      console.log('');
    });
    
  } catch (e) {
    console.error('Error:', e.message);
  }
}

listStrategies();