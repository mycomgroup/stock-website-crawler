/**
 * 理杏仁开放平台 API 测试脚本
 * Token 从环境变量 LIXINGER_TOKEN 或命令行第一个参数读取，不要写死在代码里。
 *
 * 使用方式：
 *   LIXINGER_TOKEN=你的token node test-api.js
 *   或
 *   node test-api.js 你的token
 */

const https = require('https');
const zlib = require('zlib');

const token = process.env.LIXINGER_TOKEN || process.argv[2];
if (!token) {
  console.error('请设置 LIXINGER_TOKEN 或传入 token：node test-api.js <token>');
  process.exit(1);
}

function post(host, path, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = https.request(
      {
        host,
        path,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept-Encoding': 'gzip',
          'Content-Length': Buffer.byteLength(data),
        },
      },
      (res) => {
        const chunks = [];
        res.on('data', (chunk) => chunks.push(chunk));
        res.on('end', () => {
          let buf = Buffer.concat(chunks);
          const enc = (res.headers['content-encoding'] || '').toLowerCase();
          if (enc.includes('gzip')) {
            buf = zlib.gunzipSync(buf);
          } else if (enc.includes('deflate')) {
            buf = zlib.inflateSync(buf);
          }
          const raw = buf.toString('utf8');
          try {
            resolve(JSON.parse(raw));
          } catch {
            resolve({ _raw: raw });
          }
        });
      }
    );
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function main() {
  console.log('使用 Token:', token.slice(0, 8) + '...');
  console.log('');

  // 1. 股票信息 API
  console.log('--- 1. 股票信息 API (cn/company) ---');
  try {
    const r1 = await post('open.lixinger.com', '/api/cn/company', {
      token,
      stockCodes: ['300750', '600519'],
      pageIndex: 0,
    });
    if (r1.data) {
      console.log('成功，返回条数:', r1.data.length);
      if (r1.data[0]) console.log('首条示例:', JSON.stringify(r1.data[0], null, 2).slice(0, 500) + '...');
    } else {
      console.log('响应:', JSON.stringify(r1, null, 2));
    }
  } catch (e) {
    console.error('请求失败', e.message);
  }
  console.log('');

  // 2. 基本面数据 API（PE、PB 等）
  console.log('--- 2. 基本面数据 API (cn/company/fundamental/non_financial) ---');
  try {
    const r2 = await post('open.lixinger.com', '/api/cn/company/fundamental/non_financial', {
      token,
      stockCodes: ['300750'],
      date: '2025-02-20',
      metricsList: ['pe_ttm', 'pb', 'mc', 'dyr'],
    });
    if (r2.data) {
      console.log('成功，返回条数:', r2.data.length);
      if (r2.data[0]) console.log('首条示例:', JSON.stringify(r2.data[0], null, 2));
    } else {
      console.log('响应:', JSON.stringify(r2, null, 2));
    }
  } catch (e) {
    console.error('请求失败', e.message);
  }
}

main();
