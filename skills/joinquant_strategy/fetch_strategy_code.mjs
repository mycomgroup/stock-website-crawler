import { JoinQuantStrategyClient } from './request/joinquant-strategy-client.js';
import { ensureJoinQuantSession } from './request/ensure-session.js';
import fs from 'fs';

async function main() {
  await ensureJoinQuantSession({ headed: false, headless: true });
  const client = new JoinQuantStrategyClient();
  const html = await client.request('/algorithm/index/edit?algorithmId=f6f29dc22892065a41a058f6360da41d', { method: 'GET' });

  // Extract code from textarea
  const codeMatch = html.match(/<textarea[^>]*>([\s\S]*?)<\/textarea>/);

  if (codeMatch) {
    console.log('=== STRATEGY CODE ===');
    console.log(codeMatch[1]);
  } else {
    fs.writeFileSync('/tmp/jq_strategy_debug.html', html);
    console.log('Code not found in textarea. Saved HTML to /tmp/jq_strategy_debug.html');
    // Look for ace editor content
    const aceMatch = html.match(/ace[^;]*\.setValue\(['"`]([\s\S]*?)['"`]\s*[),]/);
    if (aceMatch) {
      console.log('Found in ace editor');
      console.log(aceMatch[1].slice(0, 1000));
    }
    // Look for any script containing python code
    const pyMatch = html.match(/def\s+initialize[\s\S]{0,5000}/);
    if (pyMatch) {
      console.log('Found python code in page');
      console.log(pyMatch[0].slice(0, 2000));
    }
  }
}

main().catch(e => console.error('Error:', e.message));
