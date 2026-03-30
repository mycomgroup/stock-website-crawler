import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export const OUTPUT_ROOT = join(__dirname, 'data');
export const SESSION_FILE = join(OUTPUT_ROOT, 'session.json');
export const CONTRACT_FILE = join(OUTPUT_ROOT, 'notebook-contract.json');
export const RAW_CAPTURE_FILE = join(OUTPUT_ROOT, 'raw-capture.json');
