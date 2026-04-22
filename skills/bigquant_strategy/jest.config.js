export default {
  testEnvironment: 'node',
  testMatch: ['**/tests/**/*.test.js'],
  collectCoverageFrom: [
    'request/**/*.js',
    'lib/**/*.js',
    'browser/**/*.js',
    '!**/node_modules/**',
    '!**/tests/**',
    '!**/data/**'
  ],
  coverageDirectory: 'coverage',
  verbose: true,
  transform: {},
  moduleFileExtensions: ['js', 'mjs'],
  testPathIgnorePatterns: ['/node_modules/', '/data/'],
  moduleNameMapper: {
    '^../../common/http-security.js$': '<rootDir>/tests/__mocks__/http-security.js'
  },
  globals: {
    'jest': {
      'isolatedModules': true
    }
  }
};