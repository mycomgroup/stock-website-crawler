import './load-env.js';
import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './browser/session-manager.js';
import minimist from 'minimist';

async function main() {
  const args = minimist(process.argv.slice(2));
  const backtestId = args.id || args.backtestId;
  const algorithmId = args.algo || args.algorithmId;

  if (!backtestId) {
    console.error('Usage: node fetch-report.js --id <backtestId> [--algo <algorithmId>]');
    process.exit(1);
  }

  try {
    console.log('Verifying JoinQuant session...');
    const credentials = {
      username: process.env.JOINQUANT_USERNAME,
      password: process.env.JOINQUANT_PASSWORD
    };
    const cookies = await ensureJoinQuantSession(credentials);

    const client = new JoinQuantStrategyClient({ cookies });
    
    // We need algorithmId to get the CSRF token from the edit page
    // If not provided, we might fail if the API requires a fresh token
    let context = {};
    if (algorithmId) {
       console.log(`Fetching context for algorithm ${algorithmId}...`);
       context = await client.getStrategyContext(algorithmId);
    } else {
       console.log('Warning: No algorithmId provided. Using empty context (might fail if token is needed).');
    }

    console.log(`Fetching full report for backtest ${backtestId}...`);
    const fullReport = await client.getFullReport(backtestId, context);
    
    const resultPath = client.writeArtifact(`backtest-full-${backtestId}`, fullReport);
    console.log(`Report successfully saved to: ${resultPath}`);
    
    console.log('\nSummary:');
    console.log(JSON.stringify(fullReport.summary, null, 2));

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
