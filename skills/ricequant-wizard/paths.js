import path from 'node:path';
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
  '..', ', 
  'data', 
  'session.json'
);

export function ensureDir(filePath) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

import fs from 'node:fs';