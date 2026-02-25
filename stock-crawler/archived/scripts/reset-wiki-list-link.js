import fs from 'fs';

const linksFile = 'output/lixinger-crawler/links.txt';
const lines = fs.readFileSync(linksFile, 'utf-8').split('\n').filter(l => l.trim());

const updated = lines.map(line => {
  if (!line.trim()) return line;
  const link = JSON.parse(line);
  if (link.url === 'https://www.lixinger.com/wiki/list') {
    link.status = 'unfetched';
    link.fetchedAt = null;
    link.retryCount = 0;
    link.error = null;
    console.log('Reset wiki/list page status to unfetched');
  }
  return JSON.stringify(link);
});

fs.writeFileSync(linksFile, updated.join('\n') + '\n', 'utf-8');
console.log('Done!');
