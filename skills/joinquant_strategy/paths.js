import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

export const SKILL_ROOT = __dirname;
export const BROWSER_ROOT = resolve(SKILL_ROOT, 'browser');
export const REQUEST_ROOT = resolve(SKILL_ROOT, 'request');
export const DATA_ROOT = resolve(SKILL_ROOT, 'data');
export const REPO_ROOT = resolve(SKILL_ROOT, '..', '..');
export const OUTPUT_ROOT = resolve(REPO_ROOT, 'output');

export const SESSION_FILE = resolve(DATA_ROOT, 'session.json');
export const DEFAULT_STRATEGY_URL = 'https://www.joinquant.com/algorithm/index/list';
