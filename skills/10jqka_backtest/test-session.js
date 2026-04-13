import './load-env.js';
import { JqkaBacktestClient } from './request/10jqka-client.js';
import { SESSION_FILE } from './paths.js';
import fs from 'node:fs';

async function testSession() {
  try {
    console.log('🔍 Testing 10jqka Backtest session...\n');
    
    if (!fs.existsSync(SESSION_FILE)) {
      console.error('❌ Error: session.json not found in data directory.');
      console.log('Please run "npm run login" first to capture your session.');
      process.exit(1);
    }
    
    console.log('1. Loading session from file...');
    const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
    console.log(`   Found ${session.cookies?.length || 0} cookies.`);
    console.log(`   Captured at: ${new Date(session.timestamp).toLocaleString()}`);
    
    const client = new JqkaBacktestClient({ cookies: session.cookies });
    
    console.log('\n2. Verifying auth via a dummy backtest request...');
    // We send a minimal query to see if it rejects with 401
    try {
      const result = await client.runBacktest({
        query: "测试",
        startDate: "2024-01-01",
        endDate: "2024-01-02"
      });
      
      if (result.success) {
        console.log('   ✅ Auth verification passed!');
        console.log('   Response hint:', JSON.stringify(result.data).slice(0, 100) + '...');
      } else {
        console.log('   ❌ Auth failed: Received successful HTTP but logic error.');
      }
    } catch (e) {
      if (e.message.includes('noauth') || e.message.includes('401')) {
        console.error('   ❌ Session expired or invalid (401 NoAuth).');
        console.log('   Please re-run manual login.');
      } else {
        // Other errors might be 500 or network issues, still might mean auth is OK but params are bad
        console.warn('   ⚠️ Received an error, but it might not be auth-related:', e.message);
      }
    }
    
    console.log('\n🏁 Test finished.');
    
  } catch (e) {
    console.error('\n❌ Test execution failed:', e.message);
    process.exit(1);
  }
}

testSession();
