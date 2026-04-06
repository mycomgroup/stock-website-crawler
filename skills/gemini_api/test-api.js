#!/usr/bin/env node

import { readFileSync } from 'fs';
import { PATHS } from './paths.js';

// Load session
const sessionData = JSON.parse(readFileSync(PATHS.sessionFile, 'utf-8'));

console.log('Session cookies:');
sessionData.cookies.forEach(cookie => {
  console.log(`  ${cookie.name}: ${cookie.value.substring(0, 50)}...`);
});

// Build cookie string
const cookieString = sessionData.cookies
  .map(c => `${c.name}=${c.value}`)
  .join('; ');

console.log('\n测试 API 调用...\n');

// Test API call
const payload = {
  action: 'next',
  messages: [
    {
      id: crypto.randomUUID(),
      author: { role: 'user' },
      content: {
        content_type: 'text',
        parts: ['你好，请用一句话介绍你自己']
      }
    }
  ],
  model: 'gpt-4o',
  parent_message_id: crypto.randomUUID()
};

try {
  const response = await fetch('https://chatgpt.com/backend-api/conversation', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Cookie': cookieString,
      'User-Agent': sessionData.userAgent,
      'Accept': 'text/event-stream',
      'Origin': 'https://chatgpt.com',
      'Referer': 'https://chatgpt.com/'
    },
    body: JSON.stringify(payload)
  });

  console.log('Status:', response.status, response.statusText);
  console.log('Headers:', Object.fromEntries(response.headers.entries()));
  
  if (!response.ok) {
    const text = await response.text();
    console.log('\nResponse body:', text);
  } else {
    const text = await response.text();
    console.log('\nResponse (first 500 chars):', text.substring(0, 500));
  }

} catch (error) {
  console.error('Error:', error);
}
