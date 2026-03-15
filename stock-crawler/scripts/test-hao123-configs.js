import fs from 'fs';
import path from 'path';
import ConfigManager from '../src/config-manager.js';

const PROJECT_ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const CONFIGURE_DIR = path.join(PROJECT_ROOT, 'configure');

function main() {
  if (!fs.existsSync(CONFIGURE_DIR)) {
    throw new Error('configure 目录不存在，请先运行 crawl-hao123.js');
  }

  const files = fs
    .readdirSync(CONFIGURE_DIR)
    .filter((file) => file.endsWith('.json'))
    .sort();

  if (files.length === 0) {
    throw new Error('configure 目录下没有配置文件，请先运行 crawl-hao123.js');
  }

  const configManager = new ConfigManager();

  for (const file of files) {
    const configPath = path.join(CONFIGURE_DIR, file);
    configManager.loadConfig(configPath);
  }

  console.log(`配置校验通过，共 ${files.length} 个文件`);
}

main();
