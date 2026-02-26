/**
 * Test filter generation functionality
 */
import { XPathGenerator } from '../lib/xpath-generator.js';

console.log('Testing Filter Generation\n');
console.log('='.repeat(50));

const generator = new XPathGenerator();

// Test structure
const structure = {
  mainContent: {
    xpath: "//div[@class='main-content']",
    frequency: 1.0
  },
  headings: {
    h1: {
      xpath: "//h1[@class='page-title']",
      frequency: 1.0
    }
  },
  tables: [],
  codeBlocks: [],
  lists: []
};

console.log('\n1. Testing _identifyAdElements()');
const adFilters = generator._identifyAdElements(structure);
console.log(`   Found ${adFilters.length} ad filters:`);
adFilters.slice(0, 5).forEach(xpath => console.log(`   - ${xpath}`));

console.log('\n2. Testing _identifyNavigationElements()');
const navFilters = generator._identifyNavigationElements(structure);
console.log(`   Found ${navFilters.length} navigation filters:`);
navFilters.slice(0, 5).forEach(xpath => console.log(`   - ${xpath}`));

console.log('\n3. Testing _identifySidebarElements()');
const sidebarFilters = generator._identifySidebarElements(structure);
console.log(`   Found ${sidebarFilters.length} sidebar filters:`);
sidebarFilters.slice(0, 5).forEach(xpath => console.log(`   - ${xpath}`));

console.log('\n4. Testing complete _generateFilters()');
const filters = generator._generateFilters(structure);
console.log(`   Total filters: ${filters.removeXPaths.length}`);
console.log(`   Clean text: ${filters.cleanText}`);
console.log('\n   Sample filters:');
filters.removeXPaths.slice(0, 10).forEach(xpath => console.log(`   - ${xpath}`));

console.log('\n5. Testing filter output format');
const rules = generator.generate(structure);
console.log('\n   Generated rules structure:');
console.log(JSON.stringify(rules, null, 2));

console.log('\n' + '='.repeat(50));
console.log('✓ All filter generation tests completed successfully!');
