import { config } from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load .env file
config({ path: join(__dirname, '.env') });

export const ENV = {
  GOOGLE_EMAIL: process.env.GOOGLE_EMAIL || '',
  CHROME_PROFILE_PATH: process.env.CHROME_PROFILE_PATH || '',
  HEADLESS: process.env.HEADLESS !== 'false',
  DEFAULT_MODEL: process.env.DEFAULT_MODEL || 'gpt-4',
  HTTP_PROXY: process.env.HTTP_PROXY || '',
  HTTPS_PROXY: process.env.HTTPS_PROXY || ''
};

// Set proxy for Node.js fetch
if (ENV.HTTP_PROXY) {
  process.env.HTTP_PROXY = ENV.HTTP_PROXY;
}
if (ENV.HTTPS_PROXY) {
  process.env.HTTPS_PROXY = ENV.HTTPS_PROXY;
}
