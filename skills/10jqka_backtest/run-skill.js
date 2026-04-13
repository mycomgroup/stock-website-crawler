import fs from 'node:fs';
import path from 'node:path';
import { StrategyRunner } from './request/strategy-runner.js';
import { loadSession, isSessionValid } from './browser/session-manager.js';
import { login } from './browser/automated-login.js';
import './load-env.js';

async function main() {
  const args = process.argv.slice(2);
  let configFile = args[0];

  if (!configFile) {
    configFile = 'examples/formula_strategy.json';
    console.error(`Usage: node run-skill.js <config.json>`);
    console.error(`Example: node run-skill.js examples/formula_strategy.json`);
    process.exit(1);
  }

  const cwd = process.cwd();
  const resolvedPath = path.resolve(cwd, configFile);

  if (!fs.existsSync(resolvedPath)) {
    console.error(`File not found: ${resolvedPath}`);
    process.exit(1);
  }

  const config = JSON.parse(fs.readFileSync(resolvedPath, 'utf8'));

  const runner = new StrategyRunner({ verbose: true });

  try {
    const result = await runner.run(config);
    
    console.log('\n' + JSON.stringify(result, null, 2));
    
    if (result.status === 'ok') {
      process.exit(0);
    } else {
      process.exit(1);
    }
    
  } catch (err) {
    const isAuthError = err.message.includes('未授权') || err.message.includes('noauth') || err.message.includes('401');
    
    if (isAuthError) {
      try {
        await login();
        const retryResult = await runner.run(config);
        console.log('\n' + JSON.stringify(retryResult, null, 2));
        process.exit(retryResult.status === 'ok' ? 0 : 1);
      } catch (retryErr) {
        console.error(JSON.stringify({
          status: 'error',
          error: 'auth_failed',
          message: retryErr.message
        }));
        process.exit(1);
      }
    } else {
      console.error(JSON.stringify({
        status: 'error',
        error: 'execution_failed',
        message: err.message
      }));
      process.exit(1);
    }
  }
}

main();
