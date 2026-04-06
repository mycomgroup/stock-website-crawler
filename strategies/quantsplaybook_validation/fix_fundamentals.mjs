#!/usr/bin/env node
/**
 * 批量修复所有策略文件中的 get_fundamentals 用法错误：
 * 1. stockcode.in_(x) -> order_book_id.in_(x)
 * 2. query() 中补充 fundamentals.eod_derivative_indicator.order_book_id
 * 3. df.index.tolist() -> 先 set_index('order_book_id') 再取 index
 * 4. df.columns 去前缀
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STRATEGIES_DIR = path.join(__dirname, 'strategies');

const files = fs.readdirSync(STRATEGIES_DIR).filter(f => f.endsWith('.py'));

let fixedCount = 0;

for (const filename of files) {
  const filepath = path.join(STRATEGIES_DIR, filename);
  let code = fs.readFileSync(filepath, 'utf8');
  const original = code;

  // 1. stockcode.in_ -> order_book_id.in_
  code = code.replace(
    /fundamentals\.eod_derivative_indicator\.stockcode\.in_\(/g,
    'fundamentals.eod_derivative_indicator.order_book_id.in_('
  );

  // 2. 如果用了 order_book_id.in_ 但 query() 里没有 select order_book_id，补上
  //    找 query( 块，检查是否已有 order_book_id
  if (code.includes('order_book_id.in_(') && !code.includes('eod_derivative_indicator.order_book_id,')) {
    // 在 query( 的第一个字段前插入 order_book_id
    code = code.replace(
      /(q\s*=\s*query\(\s*\n\s*)(fundamentals\.)/,
      '$1fundamentals.eod_derivative_indicator.order_book_id,\n            $2'
    );
  }

  // 3. 修复 df.index.tolist() 用法：
  //    在 get_fundamentals 之后，如果没有 set_index，加上列名处理和 set_index
  //    匹配模式：get_fundamentals(...) 后紧跟 if df is None... 然后 df.index.tolist()
  //    替换为正确的 columns + set_index 模式
  if (code.includes('order_book_id.in_(') || code.includes('eod_derivative_indicator.order_book_id,')) {
    // 只处理有 order_book_id 查询但没有 set_index 的文件
    if (!code.includes('set_index(') && code.includes('df.index.tolist()')) {
      // 在 "if df is None" 检查之后、"df.index.tolist()" 之前插入处理逻辑
      code = code.replace(
        /(if df is None or len\(df\) == 0:\s*\n\s*return\s*\n)/,
        '$1        df.columns = [c.split(\'.\')[-1] for c in df.columns]\n        df = df.set_index(\'order_book_id\')\n'
      );
      code = code.replace(
        /(if df is None:\s*\n\s*return\s*\n)/,
        '$1        df.columns = [c.split(\'.\')[-1] for c in df.columns]\n        df = df.set_index(\'order_book_id\')\n'
      );
    }
  }

  if (code !== original) {
    fs.writeFileSync(filepath, code);
    fixedCount++;
    console.log(`✓ 修复: ${filename}`);
  }
}

console.log(`\n完成！共修复 ${fixedCount} 个文件`);
