// 基金基本面筛选器（A股）
// https://www.lixinger.com/analytics/screener/fund-fundamental/cn
import { runScreener } from './screener-runner.js';

runScreener({
  defaultUrl: 'https://www.lixinger.com/analytics/screener/fund-fundamental/cn',
  screenerKey: 'fund-cn',
  profilePath: 'request/profiles/fund-fundamental-cn.profile.json',
  helpName: 'fetch-fund-fundamental-cn.js'
}).catch(err => {
  console.error(err.stack || err.message);
  process.exit(1);
});
