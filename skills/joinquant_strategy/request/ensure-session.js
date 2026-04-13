import fs from 'node:fs';
import path from 'node:path';
import { AuthManager } from '../../common_auth/auth-manager.js';
import siteJoinQuant from '../../common_auth/sites/joinquant.js';
import { SESSION_FILE } from '../paths.js';

export async function ensureJoinQuantSession(options = {}) {
  const sessionFile = path.resolve(options.sessionFile || SESSION_FILE);
  const strategyId = options.algorithmId;
  const manager = new AuthManager({
    ...siteJoinQuant,
    sessionPath: sessionFile
  });

  manager.sessionPath = sessionFile;

  if (fs.existsSync(sessionFile) && !options.forceRefresh) {
    try {
      const session = manager.loadSession();
      if (session && session.cookies) {
        const v = manager.normalizeVerify(await siteJoinQuant.verifySession(session.cookies));
        if (v.success) {
          console.log(`✅ Session valid: ${v.user}`);
          return { sessionFile, refreshed: false };
        }
        console.log(`⚠️ Session expired: ${v.message}`);
      }
    } catch (error) {
      console.log('Session check failed, refreshing...', error.message);
    }
  }

  const cookies = await manager.getValidSession({
    forceRefresh: true,
    method: options.method || 'all'
  });

  return { sessionFile, refreshed: true };
}