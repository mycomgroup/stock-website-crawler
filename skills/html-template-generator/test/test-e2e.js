#!/usr/bin/env node

/**
 * End-to-End Test for HTML Template Generator
 * 
 * This test verifies the complete workflow from reading URL patterns
 * to generating the final template JSON file.
 * 
 * Test Coverage:
 * - Complete workflow (api-doc template)
 * - Output file format validation
 * - XPath expression validation
 * - Metadata validation
 * - Error scenarios
 * 
 * Run with: node test/test-e2e.js
 */

import { TemplateGenerator } from '../main.js';
import { PatternReader } from '../lib/pattern-reader.js';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { JSDOM } from 'jsdom';
import xpath from 'xpath';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Test configuration
const TEST_CONFIG = {
  // Use a test patterns file (we'll create a minimal one)
  patternsFile: path.join(__dirname, 'fixtures', 'test-url-patterns.json'),
  outputFile: path.join(__dirname, 'fixtures', 'output', 'test-e2e-template.json'),
  templateName: 'test-template',
  // Use example.com for reliable testing
  testUrls: [
    'https://example.com',
    'https://example.org'
  ]
};

/**
 * Test utilities
 */
class TestUtils {
  static passed = 0;
  static failed = 0;

  static assert(condition, message) {
    if (condition) {
      console.log(`  ✓ ${message}`);
      this.passed++;
    } else {
      console.error(`  ✗ ${message}`);
      this.failed++;
      throw new Error(`Assertion failed: ${message}`);
    }
  }

  static assertEqual(actual, expected, message) {
    this.assert(actual === expected, `${message} (expected: ${expected}, got: ${actual})`);
  }

  static assertNotNull(value, message) {
    this.assert(value !== null && value !== undefined, `${message} (got: ${value})`);
  }

  static assertGreaterThan(actual, threshold, message) {
    this.assert(actual > threshold, `${message} (expected > ${threshold}, got: ${actual})`);
  }

  static assertArrayLength(array, expectedLength, message) {
    this.assert(
      Array.isArray(array) && array.length === expectedLength,
      `${message} (expected length: ${expectedLength}, got: ${array?.length})`
    );
  }

  static assertHasProperty(obj, property, message) {
    this.assert(
      obj && Object.prototype.hasOwnProperty.call(obj, property),
      `${message} (property: ${property})`
    );
  }

  static printSummary() {
    console.log('\n' + '='.repeat(60));
    console.log('Test Summary');
    console.log('='.repeat(60));
    console.log(`Passed: ${this.passed}`);
    console.log(`Failed: ${this.failed}`);
    console.log(`Total: ${this.passed + this.failed}`);
    console.log('='.repeat(60));
    
    if (this.failed > 0) {
      console.log('\n❌ Some tests failed!');
      process.exit(1);
    } else {
      console.log('\n✅ All tests passed!');
      process.exit(0);
    }
  }
}

/**
 * Setup test fixtures
 */
async function setupFixtures() {
  console.log('Setting up test fixtures...\n');

  // Create fixtures directory
  const fixturesDir = path.join(__dirname, 'fixtures');
  const outputDir = path.join(fixturesDir, 'output');
  
  await fs.mkdir(fixturesDir, { recursive: true });
  await fs.mkdir(outputDir, { recursive: true });

  // Create test url-patterns.json
  const testPatterns = [
    {
      name: TEST_CONFIG.templateName,
      description: 'Test template for E2E testing',
      pathTemplate: '/',
      pattern: '^https://example\\.(com|org)/?$',
      urlCount: 2,
      samples: TEST_CONFIG.testUrls
    }
  ];

  await fs.writeFile(
    TEST_CONFIG.patternsFile,
    JSON.stringify(testPatterns, null, 2),
    'utf-8'
  );

  console.log('✓ Test fixtures created\n');
}

/**
 * Cleanup test fixtures
 */
async function cleanupFixtures() {
  console.log('\nCleaning up test fixtures...');
  
  try {
    const fixturesDir = path.join(__dirname, 'fixtures');
    await fs.rm(fixturesDir, { recursive: true, force: true });
    console.log('✓ Test fixtures cleaned up\n');
  } catch (error) {
    console.warn('Warning: Could not clean up fixtures:', error.message);
  }
}

/**
 * Test 1: Complete Workflow
 */
async function testCompleteWorkflow() {
  console.log('Test 1: Complete Workflow (api-doc template)');
  console.log('-'.repeat(60));

  const generator = new TemplateGenerator({
    browser: {
      headless: true,
      userDataDir: '../../stock-crawler/chrome_user_data'
    }
  });

  try {
    await generator.generate(
      TEST_CONFIG.templateName,
      TEST_CONFIG.patternsFile,
      TEST_CONFIG.outputFile
    );

    TestUtils.assert(true, 'Complete workflow executed without errors');
  } catch (error) {
    console.error('Error during workflow:', error.message);
    throw error;
  }

  console.log('');
}

/**
 * Test 2: Output File Format Validation
 */
async function testOutputFileFormat() {
  console.log('Test 2: Output File Format Validation');
  console.log('-'.repeat(60));

  // Read the generated file
  const content = await fs.readFile(TEST_CONFIG.outputFile, 'utf-8');
  const template = JSON.parse(content);

  // Validate top-level structure
  TestUtils.assertHasProperty(template, 'templateName', 'Has templateName property');
  TestUtils.assertHasProperty(template, 'version', 'Has version property');
  TestUtils.assertHasProperty(template, 'generatedAt', 'Has generatedAt property');
  TestUtils.assertHasProperty(template, 'samples', 'Has samples property');
  TestUtils.assertHasProperty(template, 'xpaths', 'Has xpaths property');
  TestUtils.assertHasProperty(template, 'filters', 'Has filters property');
  TestUtils.assertHasProperty(template, 'metadata', 'Has metadata property');

  // Validate values
  TestUtils.assertEqual(template.templateName, TEST_CONFIG.templateName, 'Template name matches');
  TestUtils.assertEqual(template.version, '1.0.0', 'Version is 1.0.0');
  TestUtils.assert(Array.isArray(template.samples), 'Samples is an array');
  TestUtils.assertGreaterThan(template.samples.length, 0, 'Has sample URLs');

  // Validate timestamp format
  const timestamp = new Date(template.generatedAt);
  TestUtils.assert(!isNaN(timestamp.getTime()), 'generatedAt is valid ISO timestamp');

  // Validate xpaths structure
  TestUtils.assertNotNull(template.xpaths, 'XPaths object exists');
  
  // Validate filters structure
  TestUtils.assertNotNull(template.filters, 'Filters object exists');
  TestUtils.assertHasProperty(template.filters, 'removeXPaths', 'Filters has removeXPaths');
  TestUtils.assert(Array.isArray(template.filters.removeXPaths), 'removeXPaths is an array');

  // Validate metadata
  TestUtils.assertHasProperty(template.metadata, 'sampleCount', 'Metadata has sampleCount');
  TestUtils.assertGreaterThan(template.metadata.sampleCount, 0, 'Sample count is positive');

  console.log('');
}

/**
 * Test 3: XPath Expression Validation
 */
async function testXPathValidation() {
  console.log('Test 3: XPath Expression Validation');
  console.log('-'.repeat(60));

  // Read the generated file
  const content = await fs.readFile(TEST_CONFIG.outputFile, 'utf-8');
  const template = JSON.parse(content);

  // Create a test HTML document
  const testHtml = `
    <!DOCTYPE html>
    <html>
      <head><title>Test Page</title></head>
      <body>
        <h1 class="page-title">Test Title</h1>
        <main>
          <section class="content">
            <h2>Section 1</h2>
            <p>Description text</p>
            <table>
              <thead><tr><th>Header</th></tr></thead>
              <tbody><tr><td>Data</td></tr></tbody>
            </table>
            <pre><code>console.log('test');</code></pre>
            <ul><li>Item 1</li></ul>
          </section>
        </main>
        <nav>Navigation</nav>
        <footer>Footer</footer>
      </body>
    </html>
  `;

  const dom = new JSDOM(testHtml);
  const document = dom.window.document;

  // Test XPath expressions are valid (don't throw errors)
  const xpaths = template.xpaths;

  // Test title XPath if present
  if (xpaths.title) {
    try {
      const select = xpath.useNamespaces({});
      const result = select(xpaths.title, document);
      TestUtils.assert(true, `Title XPath is valid: ${xpaths.title}`);
    } catch (error) {
      TestUtils.assert(false, `Title XPath is invalid: ${xpaths.title} - ${error.message}`);
    }
  }

  // Test sections XPath if present
  if (xpaths.sections && xpaths.sections.xpath) {
    try {
      const select = xpath.useNamespaces({});
      const result = select(xpaths.sections.xpath, document);
      TestUtils.assert(true, `Sections XPath is valid: ${xpaths.sections.xpath}`);
    } catch (error) {
      TestUtils.assert(false, `Sections XPath is invalid: ${xpaths.sections.xpath} - ${error.message}`);
    }
  }

  // Test filter XPaths
  if (template.filters && template.filters.removeXPaths) {
    for (const filterXPath of template.filters.removeXPaths) {
      try {
        const select = xpath.useNamespaces({});
        const result = select(filterXPath, document);
        TestUtils.assert(true, `Filter XPath is valid: ${filterXPath}`);
      } catch (error) {
        TestUtils.assert(false, `Filter XPath is invalid: ${filterXPath} - ${error.message}`);
      }
    }
  }

  console.log('');
}

/**
 * Test 4: Metadata Validation
 */
async function testMetadataValidation() {
  console.log('Test 4: Metadata Validation');
  console.log('-'.repeat(60));

  // Read the generated file
  const content = await fs.readFile(TEST_CONFIG.outputFile, 'utf-8');
  const template = JSON.parse(content);

  const metadata = template.metadata;

  // Validate metadata structure
  TestUtils.assertNotNull(metadata, 'Metadata exists');
  TestUtils.assertHasProperty(metadata, 'sampleCount', 'Metadata has sampleCount');

  // Validate sample count matches samples array
  TestUtils.assertEqual(
    metadata.sampleCount,
    template.samples.length,
    'Metadata sampleCount matches samples array length'
  );

  // Validate sample count is reasonable
  TestUtils.assertGreaterThan(metadata.sampleCount, 0, 'Sample count is positive');

  console.log('');
}

/**
 * Test 5: Error Scenarios
 */
async function testErrorScenarios() {
  console.log('Test 5: Error Scenarios');
  console.log('-'.repeat(60));

  const generator = new TemplateGenerator({
    browser: {
      headless: true,
      userDataDir: '../../stock-crawler/chrome_user_data'
    }
  });

  // Test 5.1: Non-existent patterns file
  console.log('  Test 5.1: Non-existent patterns file');
  try {
    await generator.generate(
      'test-template',
      'non-existent-file.json',
      TEST_CONFIG.outputFile
    );
    TestUtils.assert(false, 'Should throw error for non-existent file');
  } catch (error) {
    TestUtils.assert(
      error.message.includes('ENOENT') || error.message.includes('not found'),
      'Throws error for non-existent file'
    );
  }

  // Test 5.2: Non-existent template name
  console.log('  Test 5.2: Non-existent template name');
  try {
    await generator.generate(
      'non-existent-template',
      TEST_CONFIG.patternsFile,
      TEST_CONFIG.outputFile
    );
    TestUtils.assert(false, 'Should throw error for non-existent template');
  } catch (error) {
    TestUtils.assert(
      error.message.includes('not found') || error.message.includes('Template'),
      'Throws error for non-existent template'
    );
  }

  // Test 5.3: Invalid patterns file format
  console.log('  Test 5.3: Invalid patterns file format');
  const invalidPatternsFile = path.join(__dirname, 'fixtures', 'invalid-patterns.json');
  await fs.writeFile(invalidPatternsFile, 'invalid json content', 'utf-8');
  
  try {
    await generator.generate(
      'test-template',
      invalidPatternsFile,
      TEST_CONFIG.outputFile
    );
    TestUtils.assert(false, 'Should throw error for invalid JSON');
  } catch (error) {
    TestUtils.assert(
      error.message.includes('JSON') || error.message.includes('parse'),
      'Throws error for invalid JSON format'
    );
  }

  console.log('');
}

/**
 * Test 6: Pattern Reader Integration
 */
async function testPatternReaderIntegration() {
  console.log('Test 6: Pattern Reader Integration');
  console.log('-'.repeat(60));

  const reader = new PatternReader();

  // Test reading the test patterns file
  const template = await reader.read(TEST_CONFIG.patternsFile, TEST_CONFIG.templateName);

  TestUtils.assertNotNull(template, 'Template was read successfully');
  TestUtils.assertEqual(template.name, TEST_CONFIG.templateName, 'Template name matches');
  TestUtils.assertNotNull(template.description, 'Template has description');
  TestUtils.assert(Array.isArray(template.samples), 'Template has samples array');
  TestUtils.assertGreaterThan(template.samples.length, 0, 'Template has sample URLs');

  console.log('');
}

/**
 * Main test runner
 */
async function runTests() {
  console.log('\n' + '='.repeat(60));
  console.log('HTML Template Generator - End-to-End Tests');
  console.log('='.repeat(60) + '\n');

  try {
    // Setup
    await setupFixtures();

    // Run tests
    await testCompleteWorkflow();
    await testOutputFileFormat();
    await testXPathValidation();
    await testMetadataValidation();
    await testErrorScenarios();
    await testPatternReaderIntegration();

    // Print summary
    TestUtils.printSummary();

  } catch (error) {
    console.error('\n❌ Test execution failed:', error.message);
    console.error(error.stack);
    process.exit(1);
  } finally {
    // Cleanup
    await cleanupFixtures();
  }
}

// Run tests
runTests().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
