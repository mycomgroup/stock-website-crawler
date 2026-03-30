#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { SESSION_FILE } from '../paths.js';

export class SessionManager {
  constructor(options = {}) {
    this.sessionFile = path.resolve(options.sessionFile || SESSION_FILE);
    this.maxAge = options.maxAge || 24 * 60 * 60 * 1000; // 24 hours default
  }

  /**
   * Check if session exists
   */
  exists() {
    return fs.existsSync(this.sessionFile);
  }

  /**
   * Load session from file
   */
  load() {
    if (!this.exists()) {
      return null;
    }
    try {
      return JSON.parse(fs.readFileSync(this.sessionFile, 'utf8'));
    } catch (e) {
      return null;
    }
  }

  /**
   * Save session to file
   */
  save(sessionPayload) {
    const dir = path.dirname(this.sessionFile);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(this.sessionFile, JSON.stringify(sessionPayload, null, 2));
  }

  /**
   * Check if session is expired
   */
  isExpired() {
    const session = this.load();
    if (!session || !session.capturedAt) {
      return true;
    }
    const capturedTime = new Date(session.capturedAt).getTime();
    const now = Date.now();
    return (now - capturedTime) > this.maxAge;
  }

  /**
   * Get cookie value by name
   */
  getCookie(name) {
    const session = this.load();
    if (!session || !session.cookies) {
      return null;
    }
    const cookie = session.cookies.find(c => c.name === name);
    return cookie ? cookie.value : null;
  }

  /**
   * Get all cookies as string
   */
  getCookieString() {
    const session = this.load();
    if (!session || !session.cookies) {
      return '';
    }
    return session.cookies.map(c => `${c.name}=${c.value}`).join('; ');
  }

  /**
   * Clear session
   */
  clear() {
    if (fs.existsSync(this.sessionFile)) {
      fs.unlinkSync(this.sessionFile);
    }
  }

  /**
   * Get session age in milliseconds
   */
  getAge() {
    const session = this.load();
    if (!session || !session.capturedAt) {
      return Infinity;
    }
    const capturedTime = new Date(session.capturedAt).getTime();
    return Date.now() - capturedTime;
  }

  /**
   * Check if session is valid (exists and not expired)
   */
  isValid() {
    return this.exists() && !this.isExpired();
  }
}

export default SessionManager;
