import fs from 'node:fs';
import path from 'node:path';
import { JoinQuantStrategyClient } from './joinquant-strategy-client.js';
import { SESSION_FILE } from '../paths.js';
import { captureJoinQuantSession } from '../browser/capture-session.js';

export async function ensureJoinQuantSession(options = {}) {
  const sessionFile = path.resolve(options.sessionFile || SESSION_FILE);
  const strategyId = options.algorithmId;

  if (fs.existsSync(sessionFile) && !options.forceRefresh) {
    try {
      const client = new JoinQuantStrategyClient({ sessionFile });
      // Test session by fetching context if algorithmId is provided, or just assume valid
      if (strategyId) {
        await client.getStrategyContext(strategyId);
      }
      return { sessionFile, refreshed: false };
    } catch (error) {
      console.log('Session invalid, refreshing...', error.message);
    }
  }

  const result = await captureJoinQuantSession({
    url: options.url || 'https://www.joinquant.com/algorithm/index/list',
    headed: options.headed
  });
  
  return { sessionFile, refreshed: true, result };
}
