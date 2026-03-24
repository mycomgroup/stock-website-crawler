import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

export const SKILL_ROOT = __dirname;
export const BROWSER_ROOT = resolve(SKILL_ROOT, 'browser');
export const REQUEST_ROOT = resolve(SKILL_ROOT, 'request');
export const REPO_ROOT = resolve(SKILL_ROOT, '..', '..');
export const OUTPUT_ROOT = resolve(REPO_ROOT, 'output');
export const LIXINGER_OUTPUT_DIR = resolve(OUTPUT_ROOT, 'playwright', 'lixinger-screener');
export const SESSION_FILE = resolve(SKILL_ROOT, '.session.json');
export const CHROME_USER_DATA_DIR = resolve(REPO_ROOT, 'stock-crawler', 'chrome_user_data');
