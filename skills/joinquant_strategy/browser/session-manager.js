import fs from 'node:fs';
import { SESSION_FILE } from '../paths.js';
import { captureJoinQuantSession } from './capture-session.js';

/**
 * Ensures a valid JoinQuant session exists, using cache if available and not expired.
 */
export async function ensureJoinQuantSession(credentials = {}) {
  if (fs.existsSync(SESSION_FILE)) {
    try {
      const session = JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
      // Check if session is older than 12 hours
      const ageHours = (Date.now() - new Date(session.capturedAt).getTime()) / (1000 * 3600);
      
      if (ageHours < 12) {
        console.log('Using cached JoinQuant session.');
        return session.cookies;
      }
      console.log('Cached session expired.');
    } catch (e) {
      console.log('Failed to read cached session.');
    }
  }

  console.log('Capturing new JoinQuant session via browser...');
  const session = await captureJoinQuantSession(credentials);
  return session.cookies;
}
