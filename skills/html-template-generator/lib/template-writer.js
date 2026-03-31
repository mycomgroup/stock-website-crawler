import fs from 'fs/promises';
import path from 'path';

/**
 * TemplateWriter - Writes generated XPath rules to JSON template file
 */
export class TemplateWriter {
  /**
   * Write template to JSON file
   * @param {string} outputFile - Output file path
   * @param {Object} data - Template data
   * @param {string} data.templateName - Template name
   * @param {Array<string>} data.samples - Sample URLs
   * @param {Object} data.xpaths - XPath rules
   * @param {Object} data.filters - Filter rules
   * @param {Object} data.metadata - Metadata from structure analysis
   * @returns {Promise<void>}
   */
  async write(outputFile, data) {
    console.log('\nWriting template file...');
    
    // Build complete template object
    const template = this._buildTemplate(data);
    
    // Format as JSON
    const json = JSON.stringify(template, null, 2);
    
    // Ensure output directory exists
    const dir = path.dirname(outputFile);
    await fs.mkdir(dir, { recursive: true });
    
    // Write file
    await fs.writeFile(outputFile, json, 'utf-8');
    
    console.log(`✓ Template saved: ${outputFile}\n`);
  }

  /**
   * Build complete template object
   * @param {Object} data - Input data
   * @returns {Object} Complete template object
   * @private
   */
  _buildTemplate(data) {
    return {
      templateName: data.templateName,
      description: data.description || '',
      version: "1.0.0",
      generatedAt: new Date().toISOString(),
      samples: data.samples || [],
      xpaths: data.xpaths || {},
      filters: data.filters || {},
      metadata: this._buildMetadata(data)
    };
  }

  /**
   * Build metadata section
   * @param {Object} data - Input data
   * @returns {Object} Metadata object
   * @private
   */
  _buildMetadata(data) {
    const metadata = {
      sampleCount: data.metadata?.sampleCount || 0,
      commonElements: {}
    };

    const frequencies = data.metadata?.frequencies || {};

    if (data.xpaths) {
      if (data.xpaths.title) {
        metadata.commonElements.title = frequencies.title || data.metadata?.sampleCount || 0;
      }
      
      if (data.xpaths.sections) {
        metadata.commonElements.sections = frequencies.mainContent || data.metadata?.sampleCount || 0;
        
        const extract = data.xpaths.sections.extract;
        if (extract) {
          if (extract.table) {
            metadata.commonElements.tables = frequencies.tables || 0;
          }
          if (extract.codeExample) {
            metadata.commonElements.codeBlocks = frequencies.codeBlocks || 0;
          }
          if (extract.list) {
            metadata.commonElements.lists = frequencies.lists || 0;
          }
        }
      }
    }

    return metadata;
  }
}
