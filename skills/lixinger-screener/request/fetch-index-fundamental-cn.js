// 指数基本面筛选器（A股）
// https://www.lixinger.com/analytics/screener/index-fundamental/cn
import { runScreener } from './screener-runner.js';

runScreener({
  defaultUrl: 'https://www.lixinger.com/analytics/screener/index-fundamental/cn',
  screenerKey: 'index-cn',
  profilePath: 'request/profiles/index-fundamental-cn.profile.json',
  helpName: 'fetch-index-fundamental-cn.js'
}).catch(err => {
  console.error(err.stack || err.message);
  process.exit(1);
});
