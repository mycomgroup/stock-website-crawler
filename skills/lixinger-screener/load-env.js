import dotenv from 'dotenv';
import { resolve } from 'node:path';
import { SKILL_ROOT } from './paths.js';

dotenv.config({ path: resolve(SKILL_ROOT, '.env') });

export * from './paths.js';
