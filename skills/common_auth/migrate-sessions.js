import fs from 'node:fs';
import path from 'node:path';

const SKILLS_ROOT = path.resolve(import.meta.dirname, '../');
const SESSION_HUB = path.join(SKILLS_ROOT, '.sessions');

const MAPPINGS = [
  { 
    src: 'guorn_strategy/data/session.json', 
    dest: 'guorn.json' 
  },
  { 
    src: '10jqka_backtest/data/session.json', 
    dest: '10jqka.json' 
  },
  { 
    src: 'thsquant_strategy/data/session.json', 
    dest: 'thsquant.json' 
  }
];

function migrate() {
  console.log('📦 启动 Session 迁移脚本...');
  
  if (!fs.existsSync(SESSION_HUB)) {
    fs.mkdirSync(SESSION_HUB, { recursive: true });
    console.log(`创建共享目录: ${SESSION_HUB}`);
  }

  for (const item of MAPPINGS) {
    const srcPath = path.join(SKILLS_ROOT, item.src);
    const destPath = path.join(SESSION_HUB, item.dest);
    
    if (fs.existsSync(srcPath)) {
      console.log(`发现旧 Session: ${item.src} -> ${item.dest}`);
      
      // 读取并确保格式统一
      try {
        const raw = JSON.parse(fs.readFileSync(srcPath, 'utf8'));
        // 如果是纯数组格式 (guorn)，包装一层
        const unified = Array.isArray(raw) ? { cookies: raw, timestamp: Date.now() } : raw;
        
        fs.writeFileSync(destPath, JSON.stringify(unified, null, 2));
        console.log(`✅ 成功迁移并格式化: ${item.dest}`);
      } catch (e) {
        console.error(`❌ 迁移 ${item.src} 失败: ${e.message}`);
      }
    } else {
      console.log(`ℹ️ 跳过: 未找到 ${item.src}`);
    }
  }
  
  console.log('\n✨ 迁移完成！');
}

migrate();
