import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const session = JSON.parse(fs.readFileSync(path.join(__dirname, 'data/session.json'), 'utf8'));
const cookieHeader = session.cookies.map(c => `${c.name}=${c.value}`).join('; ');

const headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'X-Requested-With': 'XMLHttpRequest',
  'Cookie': cookieHeader,
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
  'Referer': 'https://quant.10jqka.com.cn/view/study-index.html',
  'Origin': 'https://quant.10jqka.com.cn'
};

const post = async (url, body) => {
  const r = await fetch(url, { method: 'POST', headers, body });
  const t = await r.text();
  try { const m = t.match(/\((.+)\)/s); return JSON.parse(m ? m[1] : t); } catch(e) { return { raw: t.slice(0, 200) }; }
};

const BASE = 'https://quant.10jqka.com.cn';
const algoId = '67c935e607887b957629ad72';

// 验证 session
const info = await post(`${BASE}/platform/algorithms/queryinfo/`, `algoId=${algoId}&isajax=1`);
console.log('策略:', info?.result?.algo_name, '| errorcode:', info?.errorcode);
if (info?.errorcode !== 0) { console.log('Session 无效'); process.exit(1); }

// 先 update 策略代码（可能是必要前置步骤）
const code = info.result.algo_code;
const algoName = info.result.algo_name;
const updateR = await post(`${BASE}/platform/algorithms/update/`,
  `algo_id=${algoId}&algo_name=${encodeURIComponent(algoName)}&code=${encodeURIComponent(code)}&isajax=1`
);
console.log('update:', updateR?.errorcode, updateR?.errormsg || '');

// 测试 run 参数
const runTests = [
  // 基础格式
  [`section`, `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`],
  [`section+stock_market`, `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&stock_market=STOCK&isajax=1`],
  [`section+capital=1000000`, `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=1000000&frequency=DAILY&benchmark=000300.SH&isajax=1`],
  [`section+freq=1d`, `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=1d&benchmark=000300.SH&isajax=1`],
  [`section+freq=day`, `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=day&benchmark=000300.SH&isajax=1`],
  [`section+no-benchmark`, `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&isajax=1`],
  [`section+jsonp`, `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&datatype=jsonp&isajax=1`],
  // 不同日期格式
  [`section-short`, `algo_id=${algoId}&section=2024-01-01--2024-06-30&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`],
  // 带 code
  [`with-code`, `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&code=${encodeURIComponent(code.slice(0, 50))}&isajax=1`],
  // 带 user_id
  [`with-user_id`, `algo_id=${algoId}&user_id=772028948&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`],
  // 不同 Referer
];

console.log('\n=== 测试 backtest/run ===');
for (const [name, body] of runTests) {
  const r = await post(`${BASE}/platform/backtest/run/`, body);
  const status = r?.errorcode === 0 ? '✓ 成功' : `✗ ${r?.errorcode} ${r?.errormsg || r?.raw || ''}`;
  console.log(`${name}: ${status}`);
  if (r?.errorcode === 0) {
    console.log('  result:', JSON.stringify(r.result).slice(0, 150));
    break;
  }
}

// 也测试带不同 Referer 的请求
console.log('\n=== 测试不同 Referer ===');
const referers = [
  'https://quant.10jqka.com.cn/view/study-index.html',
  'https://quant.10jqka.com.cn/view/study-index.html#/strategy/list',
  'https://quant.10jqka.com.cn/platform/study/html/editor.html',
];

for (const referer of referers) {
  const h = { ...headers, Referer: referer };
  const r = await fetch(`${BASE}/platform/backtest/run/`, {
    method: 'POST', headers: h,
    body: `algo_id=${algoId}&section=2024-01-01--2024-12-31&capital_base=100000&frequency=DAILY&benchmark=000300.SH&isajax=1`
  });
  const t = await r.text();
  let data;
  try { const m = t.match(/\((.+)\)/s); data = JSON.parse(m ? m[1] : t); } catch(e) { data = { raw: t.slice(0, 100) }; }
  console.log(`Referer=${referer.split('/').pop()}: ${data?.errorcode} ${data?.errormsg || ''}`);
}
