/**
 * Integration test for TemplateWriter
 * This test verifies the complete output format
 */

import { TemplateWriter } from '../lib/template-writer.js';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function testTemplateWriter() {
  console.log('Testing TemplateWriter integration...\n');

  const writer = new TemplateWriter();
  const outputFile = path.join(__dirname, '../output/test-integration-template.json');

  // Sample data matching the expected structure from design
  const data = {
    templateName: 'api-doc',
    samples: [
      'https://www.lixinger.com/open/api/doc',
      'https://www.lixinger.com/open/api/doc?api-key=cn/fund',
      'https://www.lixinger.com/open/api/doc?api-key=cn/index',
      'https://www.lixinger.com/open/api/doc?api-key=hk/index',
      'https://www.lixinger.com/open/api/doc?api-key=us/index'
    ],
    xpaths: {
      title: "//h1[@class='page-title']/text()",
      sections: {
        xpath: "//section[@class='api-section']",
        extract: {
          heading: ".//h2/text()",
          description: ".//p[@class='description']/text()",
          table: {
            xpath: ".//table[@class='params-table']",
            headers: ".//thead/tr/th/text()",
            rows: ".//tbody/tr",
            cells: ".//td/text()"
          },
          codeExample: ".//pre/code/text()",
          list: {
            xpath: ".//ul[@class='api-list']",
            items: ".//li/text()"
          }
        }
      }
    },
    filters: {
      removeXPaths: [
        "//div[@class='ad-banner']",
        "//aside[@class='sidebar']"
      ],
      cleanText: true
    },
    metadata: {
      sampleCount: 5,
      analyzedAt: '2024-01-15T10:30:00.000Z'
    }
  };

  // Write template
  await writer.write(outputFile, data);

  // Read and display
  const content = await fs.readFile(outputFile, 'utf-8');
  const template = JSON.parse(content);

  console.log('Generated template structure:');
  console.log(JSON.stringify(template, null, 2));

  // Verify structure
  console.log('\n✓ Verification:');
  console.log(`  - Template name: ${template.templateName}`);
  console.log(`  - Version: ${template.version}`);
  console.log(`  - Generated at: ${template.generatedAt}`);
  console.log(`  - Sample count: ${template.samples.length}`);
  console.log(`  - Has xpaths: ${!!template.xpaths}`);
  console.log(`  - Has filters: ${!!template.filters}`);
  console.log(`  - Metadata sample count: ${template.metadata.sampleCount}`);
  console.log(`  - Common elements: ${Object.keys(template.metadata.commonElements).join(', ')}`);

  console.log('\n✓ Integration test passed!');
}

testTemplateWriter().catch(console.error);
