import dotenv from 'dotenv';
import path from 'node:path';
import { SKILL_ROOT } from './paths.js';

dotenv.config({ path: path.join(SKILL_ROOT, '.env') });
