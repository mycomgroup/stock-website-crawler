import fs from 'node:fs';
import path from 'node:path';
import { GuornStrategyClient } from './guorn-strategy-client.js';
import { SESSION_FILE } from '../paths.js';
import { captureGuornSession } from '../browser/capture-session.js';

export async function ensureGuornSession(options = {}) {
  const sessionFile = path.resolve(options.sessionFile || SESSION_FILE);

  if (fs.existsSync(sessionFile) && !options.forceRefresh) {
    try {
      const client = new GuornStrategyClient({ sessionFile });
      // Test session by fetching user profile
      const profile = await client.getUserProfile();
      if (profile.status === 'ok') {
        console.log('Session valid');
        return { sessionFile, refreshed: false };
      }
    } catch (error) {
      console.log('Session invalid, refreshing...', error.message);
    }
  }

  const result = await captureGuornSession({
    headed: options.headed
  });
  
  return { sessionFile, refreshed: true, result };
}
