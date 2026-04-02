#!/usr/bin/env node
/**
 * Check BigQuant resources
 */

import './load-env.js';
import { BigQuantAPIClient } from './request/bigquant-api-client.js';

async function checkResources() {
  const client = new BigQuantAPIClient();

  // Get resource specs
  console.log('=== Resource Specs ===');
  try {
    const specs = await client.request('GET', '/aiflow/v1/resourcespecs');
    console.log(JSON.stringify(specs, null, 2));
  } catch (e) {
    console.log('Error:', e.message);
  }

  // Get user resource specs
  console.log('\n=== User Resource Specs ===');
  try {
    const userSpecs = await client.request('GET', '/aistudio/v1/userresourcespecs');
    console.log(JSON.stringify(userSpecs, null, 2));
  } catch (e) {
    console.log('Error:', e.message);
  }

  // Get current taskrun details
  console.log('\n=== Current Taskrun ===');
  try {
    const taskruns = await client.request('GET', '/aiflow/v1/taskruns?task_id=877c594e-a905-4d0b-8025-e1f4c1a0a9bd');
    console.log(JSON.stringify(taskruns, null, 2));
  } catch (e) {
    console.log('Error:', e.message);
  }
}

checkResources().catch(console.error);