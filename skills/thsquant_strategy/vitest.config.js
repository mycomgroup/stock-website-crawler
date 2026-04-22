import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['__tests__/**/*.test.js'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: [
        'request/**/*.js',
        'lib/**/*.js',
        'browser/**/*.js',
        '*.js'
      ],
      exclude: [
        '__tests__/**',
        'data/**',
        'examples/**',
        'node_modules/**'
      ]
    },
    testTimeout: 10000,
    hookTimeout: 10000
  }
});