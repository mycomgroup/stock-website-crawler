import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export const PATHS = {
  root: __dirname,
  data: join(__dirname, 'data'),
  browser: join(__dirname, 'browser'),
  request: join(__dirname, 'request'),
  examples: join(__dirname, 'examples'),
  
  // Data files
  sessionFile: '/Users/fengzhi/Downloads/git/testlixingren/skills/.sessions/chatgpt.json',
  conversationsFile: join(__dirname, 'data', 'conversations.json'),
  
  // Browser data
  userDataDir: join(__dirname, 'data', 'browser-profile')
};
