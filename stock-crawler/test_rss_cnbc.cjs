const https = require('https');

https.get('https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664', (res) => {
  let data = '';
  res.on('data', (chunk) => { data += chunk; });
  res.on('end', () => {
    console.log(data.substring(0, 1000));
  });
}).on('error', (e) => {
  console.error(e);
});
