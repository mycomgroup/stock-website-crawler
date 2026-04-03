import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const ROOT_DIR = __dirname;
export const DATA_DIR = path.join(ROOT_DIR, 'data');
export const SHARED_DIR = path.join(ROOT_DIR, 'shared');
export const EXAMPLES_DIR = path.join(ROOT_DIR, 'examples');
export const TEMPLATES_DIR = path.join(ROOT_DIR, 'templates');

export const SESSION_FILE = path.join(DATA_DIR, 'session.json');
export const FACTOR_CATALOG_FILE = path.join(SHARED_DIR, 'factor-catalog.json');

export const RICEQUANT_STRATEGY_SESSION = path.join(
  ROOT_DIR, 
  '..', 
  'ricequant_strategy', 
  'data', 
  'session.json'
);

// 如果跨 skill 的 session 文件不存在，提前给出明确提示
if (!fs.existsSync(RICEQUANT_STRATEGY_SESSION)) {
  const localSession = path.join(DATA_DIR, 'session.json');
  if (!fs.existsSync(localSession)) {
    // 仅在非 --help / --validate / --factors 场景下会真正用到，这里只记录路径供调试
    process.env._RQ_SESSION_MISSING = '1';
  }
}

export function ensureDir(filePath) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}