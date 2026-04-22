import path from 'node:path';
import { fileURLToPath } from 'node:url';
import fs from 'node:fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const SKILL_ROOT = __dirname;
export const DATA_DIR = path.join(SKILL_ROOT, 'data');
export const OUTPUT_ROOT = path.join(SKILL_ROOT, 'output');
export const SESSION_FILE = process.env.SESSION_FILE || path.join(SKILL_ROOT, 'data', 'session.json');

export function ensureDirectories() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
  if (!fs.existsSync(OUTPUT_ROOT)) fs.mkdirSync(OUTPUT_ROOT, { recursive: true });
}

ensureDirectories();
