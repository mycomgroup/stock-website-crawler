export default {
  testEnvironment: 'node',
  testMatch: ['**/tests/**/*.test.js'],
  collectCoverageFrom: [
    '**/*.js',
    '!**/node_modules/**',
    '!**/tests/**',
    '!**/tmp/**',
    '!**/data/**'
  ],
  coverageDirectory: 'coverage',
  verbose: true,
  transform: {},
  moduleFileExtensions: ['js', 'mjs'],
  testPathIgnorePatterns: ['/node_modules/', '/tmp/'],
  globals: {
    'jest': {
      'isolatedModules': true
    }
  }
};