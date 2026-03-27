import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

export const SKILL_ROOT = __dirname;
export const BROWSER_ROOT = resolve(SKILL_ROOT, 'browser');
export const REQUEST_ROOT = resolve(SKILL_ROOT, 'request');
export const DATA_ROOT = resolve(SKILL_ROOT, 'data');
export const EXAMPLES_ROOT = resolve(SKILL_ROOT, 'examples');
export const REPO_ROOT = resolve(SKILL_ROOT, '..', '..');
export const OUTPUT_ROOT = resolve(REPO_ROOT, 'output');

export const SESSION_FILE = resolve(DATA_ROOT, 'session.json');
export const CONTRACT_FILE = resolve(DATA_ROOT, 'api-contract.json');
export const RAW_CAPTURE_FILE = resolve(DATA_ROOT, 'network-capture.json');
export const DEFAULT_NOTEBOOK_URL = 'https://www.joinquant.com/research?target=research&url=/user/21333940833/notebooks/test.ipynb';
export const DEFAULT_NOTEBOOK_PATH = '/user/21333940833/notebooks/test.ipynb';
