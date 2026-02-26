import { PatternReader } from './lib/pattern-reader.js';
import { BrowserManager } from './lib/browser-manager.js';
import { HTMLFetcher } from './lib/html-fetcher.js';
import { StructureAnalyzer } from './lib/structure-analyzer.js';
import { XPathGenerator } from './lib/xpath-generator.js';
import { TemplateWriter } from './lib/template-writer.js';

/**
 * TemplateGenerator - Main orchestration class for HTML template generation
 * 
 * Coordinates all modules to generate XPath extraction templates from sample URLs:
 * 1. Read URL patterns from url-patterns.json
 * 2. Launch browser with persistent context
 * 3. Fetch HTML from sample URLs
 * 4. Analyze HTML structure to find common patterns
 * 5. Generate XPath extraction rules
 * 6. Write template to JSON file
 */
export class TemplateGenerator {
  /**
   * @param {Object} config - Configuration options
   * @param {Object} config.browser - Browser configuration
   * @param {string} config.browser.userDataDir - Path to Chrome user data directory
   * @param {boolean} config.browser.headless - Whether to run in headless mode
   * @param {string} config.browser.channel - Browser channel (default: 'chrome')
   * @param {number} config.browser.timeout - Timeout in milliseconds
   */
  constructor(config = {}) {
    this.patternReader = new PatternReader();
    this.browserManager = new BrowserManager(config.browser || {});
    this.htmlFetcher = new HTMLFetcher(this.browserManager);
    this.structureAnalyzer = new StructureAnalyzer();
    this.xpathGenerator = new XPathGenerator();
    this.templateWriter = new TemplateWriter();
  }

  /**
   * Generate template from URL patterns
   * 
   * @param {string} templateName - Name of template to generate (from url-patterns.json)
   * @param {string} patternsFile - Path to url-patterns.json file
   * @param {string} outputFile - Path to output template JSON file
   * @returns {Promise<void>}
   * 
   * @example
   * const generator = new TemplateGenerator();
   * await generator.generate(
   *   'api-doc',
   *   './url-patterns.json',
   *   './output/api-doc.json'
   * );
   */
  async generate(templateName, patternsFile, outputFile) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`HTML Template Generator`);
    console.log(`${'='.repeat(60)}`);
    console.log(`\nTemplate: ${templateName}`);
    console.log(`Input: ${patternsFile}`);
    console.log(`Output: ${outputFile}`);
    console.log(`${'='.repeat(60)}\n`);

    try {
      // Step 1: Read template from url-patterns.json
      console.log('Step 1: Reading URL patterns...');
      const template = await this.patternReader.read(patternsFile, templateName);
      console.log(`✓ Template found: ${template.name}`);
      console.log(`  Description: ${template.description}`);
      console.log(`  Sample URLs: ${template.samples.length}`);

      // Step 2: Launch browser
      console.log('\nStep 2: Launching browser...');
      await this.browserManager.launch();
      console.log('✓ Browser launched successfully');

      // Step 3: Fetch HTML from sample URLs
      console.log('\nStep 3: Fetching sample pages...');
      const htmlContents = await this.htmlFetcher.fetchAll(template.samples);
      
      if (htmlContents.length === 0) {
        throw new Error('Failed to fetch any sample pages');
      }
      
      console.log(`✓ Successfully fetched ${htmlContents.length}/${template.samples.length} pages`);

      // Step 4: Analyze HTML structure
      console.log('\nStep 4: Analyzing HTML structure...');
      const structure = await this.structureAnalyzer.analyze(htmlContents);
      
      // Display analysis summary
      this._displayAnalysisSummary(structure);

      // Step 5: Generate XPath rules
      console.log('\nStep 5: Generating XPath rules...');
      const xpaths = this.xpathGenerator.generate(structure);
      
      // Display XPath summary
      this._displayXPathSummary(xpaths);

      // Step 6: Write template file
      console.log('\nStep 6: Writing template file...');
      await this.templateWriter.write(outputFile, {
        templateName,
        samples: template.samples,
        xpaths,
        filters: xpaths.filters,
        metadata: structure.metadata
      });

      // Success message
      console.log(`${'='.repeat(60)}`);
      console.log('✓ Template generation complete!');
      console.log(`${'='.repeat(60)}\n`);

    } catch (error) {
      console.error('\n✗ Error:', error.message);
      throw error;
    } finally {
      // Always close browser
      await this.browserManager.close();
    }
  }

  /**
   * Display structure analysis summary
   * @param {Object} structure - Structure analysis result
   * @private
   */
  _displayAnalysisSummary(structure) {
    console.log('\nStructure Analysis Summary:');
    console.log(`  Samples analyzed: ${structure.metadata.sampleCount}`);
    
    if (structure.mainContent) {
      console.log(`  Main content: ${structure.mainContent.xpath} (${(structure.mainContent.frequency * 100).toFixed(0)}%)`);
    }
    
    const headingCount = Object.keys(structure.headings).length;
    if (headingCount > 0) {
      console.log(`  Headings: ${headingCount} levels found`);
    }
    
    if (structure.tables.length > 0) {
      console.log(`  Tables: ${structure.tables.length} patterns found`);
    }
    
    if (structure.codeBlocks.length > 0) {
      console.log(`  Code blocks: ${structure.codeBlocks.length} patterns found`);
    }
    
    if (structure.lists.length > 0) {
      console.log(`  Lists: ${structure.lists.length} patterns found`);
    }
  }

  /**
   * Display XPath generation summary
   * @param {Object} xpaths - Generated XPath rules
   * @private
   */
  _displayXPathSummary(xpaths) {
    console.log('\nGenerated XPath Rules:');
    
    if (xpaths.title) {
      console.log(`  Title: ${xpaths.title}`);
    }
    
    if (xpaths.sections) {
      console.log(`  Sections: ${xpaths.sections.xpath}`);
      
      const extract = xpaths.sections.extract;
      if (extract.heading) {
        console.log(`    - Heading: ${extract.heading}`);
      }
      if (extract.table) {
        console.log(`    - Table: ${extract.table.xpath}`);
      }
      if (extract.codeExample) {
        console.log(`    - Code: ${extract.codeExample}`);
      }
      if (extract.list) {
        console.log(`    - List: ${extract.list.xpath}`);
      }
    }
    
    if (xpaths.filters && xpaths.filters.removeXPaths) {
      console.log(`  Filters: ${xpaths.filters.removeXPaths.length} noise removal rules`);
    }
  }
}

export default TemplateGenerator;
