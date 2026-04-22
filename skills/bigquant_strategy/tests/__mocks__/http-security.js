export const USER_AGENT = 'test-user-agent';
export const SEC_CH_UA = 'test-sec-ch-ua';

export class SecureHttpClient {
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || '';
    this.maxRequestsPerMinute = options.maxRequestsPerMinute || 10;
    this.sessionValidator = options.sessionValidator;
  }

  async request(url, options = {}) {
    return '{}';
  }
}

export class RateLimiter {
  constructor(maxRequestsPerMinute = 10) {
    this.maxRequestsPerMinute = maxRequestsPerMinute;
  }

  async waitForSlot() {}
}

export default {
  SecureHttpClient,
  RateLimiter,
  USER_AGENT,
  SEC_CH_UA
};