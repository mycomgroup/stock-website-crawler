#!/usr/bin/env node
import './load-env.js';
import { RiceQuantClient } from './request/ricequant-client.js';
import { ensureRiceQuantSession } from './browser/session-manager.js';

async function main() {
  try {
    console.log('Verifying RiceQuant session...');
    const credentials = {
      username: process.env.RICEQUANT_USERNAME,
      password: process.env.RICEQUANT_PASSWORD
    };
    const cookies = await ensureRiceQuantSession(credentials);
    console.log(`Session verified (${cookies.length} cookies)`);

    const client = new RiceQuantClient({ cookies });
    
    console.log('Fetching strategies...');
    const strategies = await client.listStrategies();
    
    if (strategies.length === 0) {
      console.log('No strategies found.');
      return;
    }

    console.log('\nAvailable Strategies:');
    console.log('------------------------------------------------------------');
    console.log(`${'ID'.padEnd(12)} | ${'Name'}`);
    console.log('------------------------------------------------------------');
    strategies.forEach(s => {
      const id = s.id || 'N/A';
      const name = s.name || 'Unnamed';
      console.log(`${id.toString().padEnd(12)} | ${name}`);
    });
    console.log('------------------------------------------------------------');
    console.log(`Total: ${strategies.length} strategies`);

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
