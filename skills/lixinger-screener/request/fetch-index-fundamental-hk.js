// 指数基本面筛选器（港股）
// https://www.lixinger.com/analytics/screener/index-fundamental/hk
import { runScreener } from './screener-runner.js';

runScreener({
  defaultUrl: 'https://www.lixinger.com/analytics/screener/index-fundamental/hk',
  screenerKey: 'index-hk',
  profilePath: 'request/profiles/index-fundamental-hk.profile.json',
  helpName: 'fetch-index-fundamental-hk.js'
}).catch(err => {
  console.error(err.stack || err.message);
  process.exit(1);
});
