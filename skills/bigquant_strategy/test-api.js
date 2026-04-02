#!/usr/bin/env node
import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function testBigQuantAPI() {
  const client = new BigQuantAPIClient();

  console.log('='.repeat(60));
  console.log('BigQuant API Test');
  console.log('='.repeat(60));

  // Test 1: Get current user
  console.log('\n1. Testing getCurrentUser...');
  try {
    const user = await client.getCurrentUser();
    console.log('Response:', JSON.stringify(user, null, 2).substring(0, 500));
  } catch (e) {
    console.log('Error:', e.message);
  }

  // Test 2: Get default studio
  console.log('\n2. Testing getDefaultStudio...');
  try {
    const studio = await client.getDefaultStudio();
    console.log('Response:', JSON.stringify(studio, null, 2).substring(0, 500));
  } catch (e) {
    console.log('Error:', e.message);
  }

  // Test 3: List tasks
  console.log('\n3. Testing listTasks...');
  try {
    const tasks = await client.listTasks({ size: 5 });
    console.log('Response:', JSON.stringify(tasks, null, 2).substring(0, 1000));
  } catch (e) {
    console.log('Error:', e.message);
  }

  // Test 4: List strategies
  console.log('\n4. Testing listStrategies...');
  try {
    const strategies = await client.listStrategies({ size: 5 });
    console.log('Response:', JSON.stringify(strategies, null, 2).substring(0, 1000));
  } catch (e) {
    console.log('Error:', e.message);
  }

  // Test 5: Get modules
  console.log('\n5. Testing getModules...');
  try {
    const modules = await client.getModules();
    console.log('Response:', JSON.stringify(modules, null, 2).substring(0, 500));
  } catch (e) {
    console.log('Error:', e.message);
  }

  console.log('\n' + '='.repeat(60));
  console.log('Test complete');
  console.log('='.repeat(60));
}

testBigQuantAPI().catch(console.error);