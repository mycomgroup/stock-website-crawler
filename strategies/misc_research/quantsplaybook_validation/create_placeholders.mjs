import fs from 'node:fs';
import path from 'node:path';
import { RiceQuantClient } from '../../skills/ricequant_strategy/request/ricequant-client.js';

const STRATEGIES_DIR = './strategies';
const MAPPING_FILE = './NEW_STRATEGY_MAPPING.json';

async function main() {
  const client = new RiceQuantClient();
  const loginStatus = await client.checkLogin();
  if (!loginStatus) {
    console.error('Not logged in. Please ensure session.json is valid.');
    process.exit(1);
  }

  // 获取现有的策略列表，避免重复创建
  const existingStrategies = await client.listStrategies();
  const existingNames = new Set(existingStrategies.map(s => s.name));

  const files = fs.readdirSync(STRATEGIES_DIR).filter(f => f.endsWith('.py'));
  const newStrategies = [];

  // 筛选出 26-56 和 notebook 系列
  for (const file of files) {
    const numMatch = file.match(/^(\d+)_/);
    const isNotebook = file.startsWith('notebook_');
    
    let isNew = false;
    if (numMatch) {
      const num = parseInt(numMatch[1], 10);
      if (num >= 26 && num <= 56) isNew = true;
    } else if (isNotebook) {
      isNew = true;
    }

    if (isNew) {
      // 检查标题是否已存在
      const title = file.replace('.py', '').replace(/_/g, ' ');
      if (existingNames.has(title)) {
        console.log(`[Skip] Strategy already exists: ${title}`);
        const s = existingStrategies.find(s => s.name === title);
        newStrategies.push({ file, id: s.id, title });
        continue;
      }

      console.log(`[Create] Creating strategy for: ${file}`);
      try {
        const result = await client.createStrategy(title, '# Placeholder');
        if (result && (result._id || result.id || result.strategy_id)) {
          const id = result._id || result.id || result.strategy_id;
          console.log(`   Success: ${title} -> ID: ${id}`);
          newStrategies.push({ file, id, title });
        } else {
          console.error(`   Failed to create: ${title}`, result);
        }
      } catch (e) {
        console.error(`   Error creating ${title}:`, e.message);
      }
      
      // 稍微 sleep 一下，避免频率限制
      await new Promise(r => setTimeout(r, 1000));
    }
  }

  fs.writeFileSync(MAPPING_FILE, JSON.stringify(newStrategies, null, 2));
  console.log(`\nMapping saved to ${MAPPING_FILE}`);
}

main().catch(console.error);
