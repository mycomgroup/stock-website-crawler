import dotenv from 'dotenv';
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { SKILL_ROOT } from './paths.js';

const envPath = resolve(SKILL_ROOT, '.env');
if (existsSync(envPath)) {
  dotenv.config({ path: envPath });
}

export * from './paths.js';
