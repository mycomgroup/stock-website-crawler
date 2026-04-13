import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const SKILL_ROOT = __dirname;
export const DATA_DIR = path.join(SKILL_ROOT, 'data');
export const OUTPUT_ROOT = path.join(SKILL_ROOT, 'output');
export const SESSION_FILE = '/Users/fengzhi/Downloads/git/testlixingren/skills/.sessions/10jqka.json';

// 确保目录存在
import fs from 'node:fs';
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
if (!fs.existsSync(OUTPUT_ROOT)) fs.mkdirSync(OUTPUT_ROOT, { recursive: true });
