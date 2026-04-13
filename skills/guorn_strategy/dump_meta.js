import fs from 'node:fs';
import path from 'node:path';
import { GuornStrategyClient } from './request/guorn-strategy-client.js';
import { ensureGuornSession } from './request/ensure-session.js';

async function dumpMeta() {
  await ensureGuornSession();
  const client = new GuornStrategyClient();
  console.log('Fetching stock meta...');
  const meta = await client.getStockMeta('stock');
  
  const outFile = 'guorn_meta_full.json';
  fs.writeFileSync(outFile, JSON.stringify(meta, null, 2));
  console.log(`Saved full meta to ${outFile}`);
  
  // Extract summary
  const summary = {
    indicatorCount: 0,
    categories: []
  };
  
  if (meta.data?.measures) {
    summary.indicatorCount = meta.data.measures.length;
    // ... basic summary
  }
}

dumpMeta().catch(console.error);
