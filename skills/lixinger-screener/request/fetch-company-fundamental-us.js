// 公司基本面筛选器（美股）
// https://www.lixinger.com/analytics/screener/company-fundamental/us
import { runScreener } from './screener-runner.js';

runScreener({
  defaultUrl: 'https://www.lixinger.com/analytics/screener/company-fundamental/us',
  screenerKey: 'company-us',
  profilePath: 'request/profiles/company-fundamental-us.profile.json',
  helpName: 'fetch-company-fundamental-us.js'
}).catch(err => {
  console.error(err.stack || err.message);
  process.exit(1);
});
