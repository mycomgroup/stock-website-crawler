#!/usr/bin/env node
import { main } from './rotation_longterm/run.js';

main().catch(error => {
  console.error('主程序错误:', error.stack || error.message);
  process.exit(1);
});
