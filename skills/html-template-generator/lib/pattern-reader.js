import { readFile } from 'fs/promises';
import { resolve } from 'path';

/**
 * PatternReader - Reads and parses url-patterns.json files
 */
export class PatternReader {
  /**
   * Read url-patterns.json and extract specified template
   * @param {string} patternsFile - Path to url-patterns.json
   * @param {string} templateName - Name of template to extract
   * @returns {Promise<Object>} Template object with name, description, samples
   */
  async read(patternsFile, templateName) {
    try {
      // Read and parse JSON file
      const absolutePath = resolve(patternsFile);
      const content = await readFile(absolutePath, 'utf-8');
      const patterns = JSON.parse(content);

      // Find template by name
      const template = patterns.find(p => p.name === templateName);
      
      if (!template) {
        throw new Error(`Template "${templateName}" not found in ${patternsFile}`);
      }

      // Validate template structure
      this._validateTemplate(template);

      return {
        name: template.name,
        description: template.description,
        samples: template.samples,
        pathTemplate: template.pathTemplate,
        pattern: template.pattern,
        urlCount: template.urlCount
      };
    } catch (error) {
      if (error.code === 'ENOENT') {
        throw new Error(`File not found: ${patternsFile}`);
      }
      if (error instanceof SyntaxError) {
        throw new Error(`Invalid JSON in ${patternsFile}: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * Validate template data completeness
   * @param {Object} template - Template object to validate
   * @throws {Error} If template data is incomplete
   * @private
   */
  _validateTemplate(template) {
    const required = ['name', 'description', 'samples'];
    const missing = required.filter(field => !template[field]);
    
    if (missing.length > 0) {
      throw new Error(`Template missing required fields: ${missing.join(', ')}`);
    }

    if (!Array.isArray(template.samples) || template.samples.length === 0) {
      throw new Error('Template must have at least one sample URL');
    }
  }
}
