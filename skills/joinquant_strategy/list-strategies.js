import './load-env.js';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './browser/session-manager.js';

async function main() {
  try {
    console.log('Verifying JoinQuant session...');
    const credentials = {
      username: process.env.JOINQUANT_USERNAME,
      password: process.env.JOINQUANT_PASSWORD
    };
    const cookies = await ensureJoinQuantSession(credentials);

    const client = new JoinQuantStrategyClient({ cookies });
    
    console.log('Fetching strategies...');
    const strategies = await client.listStrategies();
    
    if (strategies.length === 0) {
      console.log('No strategies found.');
      return;
    }

    console.log('\nAvailable Strategies:');
    console.log('------------------------------------------------------------');
    console.log(`${'ID'.padEnd(35)} | ${'Name'}`);
    console.log('------------------------------------------------------------');
    strategies.forEach(s => {
      console.log(`${s.id.padEnd(35)} | ${s.name}`);
    });
    console.log('------------------------------------------------------------');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
