import fs from 'node:fs';
import path from 'node:path';
import '../load-env.js';
import { SESSION_FILE } from '../paths.js';
import { captureJoinQuantSession } from '../browser/capture-joinquant-session.js';
import { JoinQuantClient } from './joinquant-client.js';

function resolveSessionFile(sessionFile) {
  return path.resolve(sessionFile || SESSION_FILE);
}

function shouldRefreshSession(error) {
  const message = String(error?.stack || error?.message || error || '');
  if (!message) return true;
  if (message.includes('404')) return false;
  return /ENOENT|Unexpected token|缺少 `_xsrf` cookie|请求失败 401|请求失败 403|接口未返回 JSON|Failed to fetch|fetch failed|ECONNRESET|socket hang up/i.test(message);
}

export async function ensureJoinQuantSession(options = {}) {
  const sessionFile = resolveSessionFile(options.sessionFile);
  const notebookUrl = options.notebookUrl;

  if (!notebookUrl) {
    throw new Error('ensureJoinQuantSession 缺少 notebookUrl');
  }

  if (fs.existsSync(sessionFile) && !options.forceRefresh) {
    try {
      const client = new JoinQuantClient({
        sessionFile,
        notebookUrl,
        outputRoot: options.outputRoot
      });
      await client.getNotebookMetadata();
      return {
        sessionFile,
        refreshed: false,
        reason: 'existing-session-valid'
      };
    } catch (error) {
      if (!shouldRefreshSession(error)) {
        return {
          sessionFile,
          refreshed: false,
          reason: 'existing-session-valid-but-target-notebook-missing'
        };
      }
    }
  }

  const captureResult = await captureJoinQuantSession({
    notebookUrl,
    headed: options.headed,
    headless: options.headless
  });

  return {
    sessionFile,
    refreshed: true,
    reason: 'captured-new-session',
    captureResult
  };
}
