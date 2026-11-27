#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

function findLatestPagesDir(rootDir) {
  if (!fs.existsSync(rootDir)) return null;
  const dirs = fs.readdirSync(rootDir)
    .filter(name => name.startsWith('pages-'))
    .map(name => ({ name, fullPath: path.join(rootDir, name), mtime: fs.statSync(path.join(rootDir, name)).mtimeMs }))
    .sort((a, b) => b.mtime - a.mtime);
  return dirs[0]?.fullPath || null;
}

function validateMarkdown(md, file) {
  const issues = [];
  if (!/^#\s+/m.test(md)) issues.push('缺少 H1 标题');
  if (md.length < 300) issues.push(`正文过短(${md.length})，疑似抽取不完整`);
  if (/\n{4,}/.test(md)) issues.push('存在 4 个以上连续空行');

  const tableLines = md.split('\n').filter(line => /^\|.*\|$/.test(line));
  if (tableLines.length > 0) {
    const hasSeparator = tableLines.some(line => /\|\s*---/.test(line));
    if (!hasSeparator) issues.push('检测到表格行但缺少分隔符行');
  }

  return { file, issues };
}

function main() {
  const outputRoot = path.resolve(process.argv[2] || './output/alltick-api-docs');
  const latestDir = findLatestPagesDir(outputRoot);

  if (!latestDir) {
    console.error(`❌ 未找到 pages-* 目录: ${outputRoot}`);
    process.exit(1);
  }

  const mdFiles = fs.readdirSync(latestDir)
    .filter(name => name.endsWith('.md'))
    .map(name => path.join(latestDir, name));

  if (mdFiles.length === 0) {
    console.error(`❌ ${latestDir} 下没有 Markdown 文件`);
    process.exit(1);
  }

  const results = mdFiles.map(file => validateMarkdown(fs.readFileSync(file, 'utf-8'), file));
  const failed = results.filter(r => r.issues.length > 0);

  console.log(`检查目录: ${latestDir}`);
  console.log(`Markdown 文件数: ${mdFiles.length}`);

  if (failed.length > 0) {
    console.error(`\n❌ 发现 ${failed.length} 个文件不满足格式/完整性要求`);
    for (const item of failed) {
      console.error(`- ${path.basename(item.file)}: ${item.issues.join('；')}`);
    }
    process.exit(2);
  }

  console.log('\n✅ Markdown 格式与最小完整性检查通过');
}

main();
