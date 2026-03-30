import './load-env.js';
import { RiceQuantClient } from './request/ricequant-client.js';
import { ensureRiceQuantSession } from './browser/session-manager.js';
import fs from 'node:fs';

async function main() {
  const credentials = {
    username: process.env.RICEQUANT_USERNAME,
    password: process.env.RICEQUANT_PASSWORD
  };
  const cookies = await ensureRiceQuantSession(credentials);
  
  const client = new RiceQuantClient({ cookies });
  const strategies = await client.listStrategies();
  
  console.log('Strategy data structure:');
  console.log(JSON.stringify(strategies[0], null, 2));
  
  fs.writeFileSync('strategies-debug.json', JSON.stringify(strategies, null, 2));
  console.log('\n✓ Saved to strategies-debug.json');
}

main();
