export function createMockSession(cookies = []) {
  return {
    cookies: cookies.length > 0 ? cookies : [
      { name: 'sid', value: 'test-sid-value', domain: '.10jqka.com.cn' },
      { name: 'ths_token', value: 'test-token-value', domain: '.10jqka.com.cn' }
    ],
    timestamp: Date.now()
  };
}

export function createMockCookie(name = 'sid', value = 'test-value') {
  return { name, value, domain: '.10jqka.com.cn', path: '/' };
}

export function createMockResponse(data, options = {}) {
  return {
    ok: options.ok ?? true,
    status: options.status ?? 200,
    statusText: options.statusText ?? 'OK',
    headers: new Map(Object.entries(options.headers || {})),
    json: async () => data,
    text: async () => typeof data === 'string' ? data : JSON.stringify(data),
    ...options
  };
}

export function createMockStrategy(overrides = {}) {
  return {
    id: 'test-algo-id-123',
    name: 'Test Strategy',
    backtestCount: 5,
    latestBacktestId: 'backtest-456',
    modified: '2024-01-15T10:30:00Z',
    ...overrides
  };
}

export function createMockTHSQuantClient(methods = {}) {
  return {
    checkLogin: methods.checkLogin || (async () => ({ logged: true, userId: 'user-123', code: 0 })),
    listStrategies: methods.listStrategies || (async () => []),
    getStrategyInfo: methods.getStrategyInfo || (async () => ({})),
    saveStrategy: methods.saveStrategy || (async () => ({ success: true })),
    createStrategy: methods.createStrategy || (async () => ({ success: true, algoId: 'new-id' })),
    deleteStrategy: methods.deleteStrategy || (async () => ({ success: true })),
    runBacktest: methods.runBacktest || (async () => ({ backtestId: 'bt-123', progress: 0 })),
    pollBacktestStatus: methods.pollBacktestStatus || (async () => ({ status: 'SUCCESS', progress: 100 })),
    waitForBacktest: methods.waitForBacktest || (async () => ({ success: true })),
    getBacktestInfo: methods.getBacktestInfo || (async () => ({})),
    getFullReport: methods.getFullReport || (async () => ({})),
    ...methods
  };
}

export const mockFsPromises = {
  readFile: async () => '',
  writeFile: async () => {},
  mkdir: async () => undefined,
  stat: async () => ({ isFile: () => true, isDirectory: () => false }),
  unlink: async () => {},
  readdir: async () => [],
  access: async () => {},
  copyFile: async () => {},
  rename: async () => {}
};

export const mockPlaywright = {
  chromium: {
    launch: async () => ({
      newContext: async () => ({
        newPage: async () => ({
          goto: async () => {},
          waitForSelector: async () => {},
          waitForLoadState: async () => {},
          fill: async () => {},
          click: async () => {},
          type: async () => {},
          press: async () => {},
          waitForTimeout: async () => {},
          waitForURL: async () => {},
          waitForResponse: async () => ({
            json: async () => ({}),
            text: async () => '',
            ok: () => true,
            status: () => 200
          }),
          cookies: async () => [],
          context: () => ({
            cookies: async () => [],
            addCookies: async () => {}
          }),
          close: async () => {},
          screenshot: async () => Buffer.from(''),
          evaluate: async () => null,
          $: async () => null,
          $$: async () => [],
          waitFor: async () => {},
          isVisible: async () => true
        }),
        cookies: async () => [],
        addCookies: async () => {},
        close: async () => {}
      }),
      close: async () => {}
    })
  }
};

export function resetAllMocks() {}