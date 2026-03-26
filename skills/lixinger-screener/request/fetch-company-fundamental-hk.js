// 公司基本面筛选器（港股）
// https://www.lixinger.com/analytics/screener/company-fundamental/hk
import { runScreener } from './screener-runner.js';

runScreener({
  defaultUrl: 'https://www.lixinger.com/analytics/screener/company-fundamental/hk',
  screenerKey: 'company-hk',
  profilePath: 'request/profiles/company-fundamental-hk.profile.json',
  helpName: 'fetch-company-fundamental-hk.js'
}).catch(err => {
  console.error(err.stack || err.message);
  process.exit(1);
});
