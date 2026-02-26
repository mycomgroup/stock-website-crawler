# HTML Template Generator - Implementation Tasks

## Phase 1: Infrastructure Setup

- [x] 1.1 Create project structure
- [x] 1.2 Configure package.json and dependencies
- [x] 1.3 Implement pattern-reader.js
- [x] 1.4 Implement browser-manager.js
- [x] 1.5 Implement html-fetcher.js
- [x] 1.6 Test page fetching functionality

## Phase 2: Structure Analysis

- [x] 2.1 Implement structure-analyzer.js base framework
- [x] 2.2 Implement heading structure analysis
- [x] 2.3 Implement table structure analysis
- [x] 2.4 Implement code block and list analysis
- [x] 2.5 Implement main content area identification

## Phase 3: Rule Generation

- [x] 3.1 Implement xpath-generator.js base framework
- [x] 3.2 Implement XPath expression generation
- [x] 3.3 Implement filter rule generation
- [x] 3.4 Implement template-writer.js

## Phase 4: Integration and Testing

- [x] 4.1 Implement main.js core logic
- [x] 4.2 Implement run-skill.js CLI entry point
- [x] 4.3 End-to-end testing
- [x] 4.4 Write documentation

---

## Task Details

### 1.1 Create project structure

**Priority**: High | **Estimated Time**: 30 minutes

Create complete project directory structure and base files.

**Acceptance Criteria**:
- Create `skills/html-template-generator/` directory
- Create `lib/` subdirectory
- Create `test/` subdirectory
- Create `docs/` subdirectory
- Create `output/` subdirectory
- Create `package.json` file
- Create `README.md` file
- Create `SKILL.md` file
- Create `.gitignore` file

**Dependencies**: None

---

### 1.2 Configure package.json and dependencies

**Priority**: High | **Estimated Time**: 30 minutes

Configure project dependencies and scripts.

**Acceptance Criteria**:
- Add Playwright dependency (`playwright`)
- Add jsdom dependency (`jsdom`)
- Add xpath dependency (`xpath`)
- Configure ES modules (`"type": "module"`)
- Add run scripts
- Add test scripts
- Run `npm install` successfully

**Dependencies**: 1.1

---

### 1.3 Implement pattern-reader.js

**Priority**: High | **Estimated Time**: 1 hour

Implement module to read url-patterns.json.

**Acceptance Criteria**:
- Create `lib/pattern-reader.js`
- Implement `PatternReader` class
- Implement `read(patternsFile, templateName)` method
- Return template object (name, description, samples)
- Handle file not found errors
- Handle template not found errors
- Add unit tests

**Interface Design**:
```javascript
class PatternReader {
  async read(patternsFile, templateName) {
    // Returns: { name, description, samples }
  }
}
```

**Dependencies**: 1.2

---

### 1.4 Implement browser-manager.js

**Priority**: High | **Estimated Time**: 1.5 hours

Implement Playwright browser management module.

**Acceptance Criteria**:
- Create `lib/browser-manager.js`
- Implement `BrowserManager` class
- Implement `launch()` method (using launchPersistentContext)
- Implement `close()` method
- Configure userDataDir to `../../stock-crawler/chrome_user_data`
- Configure headless mode
- Configure channel as 'chrome'
- Add error handling
- Add unit tests

**Interface Design**:
```javascript
class BrowserManager {
  constructor(config) {
    this.userDataDir = config.userDataDir;
    this.headless = config.headless;
  }
  
  async launch() {
    // Returns browser context
  }
  
  async close() {
    // Close browser
  }
}
```

**Dependencies**: 1.2

---

### 1.5 Implement html-fetcher.js

**Priority**: High | **Estimated Time**: 1.5 hours

Implement module to fetch page HTML.

**Acceptance Criteria**:
- Create `lib/html-fetcher.js`
- Implement `HTMLFetcher` class
- Implement `fetchAll(urls)` method
- Implement `fetchOne(url)` method
- Wait for page load completion (networkidle)
- Extract HTML content
- Extract page title
- Add timeout handling
- Add error handling
- Add unit tests

**Interface Design**:
```javascript
class HTMLFetcher {
  constructor(browserManager) {
    this.browserManager = browserManager;
  }
  
  async fetchAll(urls) {
    // Returns: [{ url, html, title }]
  }
  
  async fetchOne(url) {
    // Returns: { url, html, title }
  }
}
```

**Dependencies**: 1.4

---

### 1.6 Test page fetching functionality

**Priority**: High | **Estimated Time**: 1 hour

End-to-end test of page fetching functionality.

**Acceptance Criteria**:
- Create test script `test/test-fetch.js`
- Test fetching single URL
- Test fetching multiple URLs
- Verify HTML content is not empty
- Verify title is correctly extracted
- Test error handling (invalid URL)
- Test timeout handling
- All tests pass

**Dependencies**: 1.5

---

### 2.1 Implement structure-analyzer.js base framework

**Priority**: High | **Estimated Time**: 2 hours

Implement base framework for HTML structure analysis.

**Acceptance Criteria**:
- Create `lib/structure-analyzer.js`
- Implement `StructureAnalyzer` class
- Implement `analyze(htmlContents)` method
- Use jsdom to parse HTML
- Implement basic element extraction framework
- Add unit tests

**Interface Design**:
```javascript
class StructureAnalyzer {
  async analyze(htmlContents) {
    // Returns: { mainContent, headings, tables, codeBlocks, lists, metadata }
  }
}
```

**Dependencies**: 1.6

---

### 2.2 Implement heading structure analysis

**Priority**: High | **Estimated Time**: 1.5 hours

Analyze heading structure (h1-h6) in pages.

**Acceptance Criteria**:
- Extract all heading elements (h1-h6)
- Record heading class and id attributes
- Record heading text content
- Calculate heading frequency across samples
- Identify common heading patterns
- Add unit tests

**Output Format**:
```javascript
{
  h1: { 
    xpath: "//h1[@class='page-title']", 
    frequency: 5/5,
    samples: ["API文档", "基金接口"]
  }
}
```

**Dependencies**: 2.1

---

### 2.3 Implement table structure analysis

**Priority**: High | **Estimated Time**: 2 hours

Analyze table structure in pages.

**Acceptance Criteria**:
- Extract all table elements
- Record table class and id attributes
- Extract table caption
- Extract table header (thead)
- Calculate column count
- Calculate table frequency across samples
- Identify common table patterns
- Add unit tests

**Output Format**:
```javascript
{
  xpath: "//table[@class='params-table']",
  frequency: 5/5,
  caption: "参数说明",
  columnCount: 4
}
```

**Dependencies**: 2.1

---

### 2.4 Implement code block and list analysis

**Priority**: Medium | **Estimated Time**: 1.5 hours

Analyze code blocks and lists in pages.

**Acceptance Criteria**:
- Extract code blocks (pre/code)
- Identify code language
- Extract ordered lists (ol)
- Extract unordered lists (ul)
- Calculate frequency
- Identify common patterns
- Add unit tests

**Dependencies**: 2.1

---

### 2.5 Implement main content area identification

**Priority**: Medium | **Estimated Time**: 1 hour

Identify main content area of pages.

**Acceptance Criteria**:
- Identify main, article, .content containers
- Filter navigation, sidebar, ads
- Calculate content density
- Select most likely main content area
- Add unit tests

**Dependencies**: 2.1

---

### 3.1 Implement xpath-generator.js base framework

**Priority**: High | **Estimated Time**: 1.5 hours

Implement base framework for XPath generation.

**Acceptance Criteria**:
- Create `lib/xpath-generator.js`
- Implement `XPathGenerator` class
- Implement `generate(structure)` method
- Implement basic XPath generation logic
- Add unit tests

**Interface Design**:
```javascript
class XPathGenerator {
  generate(structure) {
    // Returns: { title, sections, filters }
  }
}
```

**Dependencies**: 2.5

---

### 3.2 Implement XPath expression generation

**Priority**: High | **Estimated Time**: 2 hours

Generate XPath expressions for various elements.

**Acceptance Criteria**:
- Generate XPath for headings
- Generate XPath for tables
- Generate XPath for code blocks
- Generate XPath for lists
- Prioritize class and id attributes
- Use contains() for multiple classes
- Generate relative paths (.//）
- Add unit tests

**XPath Examples**:
```javascript
"//h1[@class='page-title']/text()"
"//table[contains(@class, 'params-table')]"
".//pre/code/text()"
```

**Dependencies**: 3.1

---

### 3.3 Implement filter rule generation

**Priority**: Medium | **Estimated Time**: 1 hour

Generate filter rules to remove noise elements.

**Acceptance Criteria**:
- Identify ad elements
- Identify navigation elements
- Identify sidebar elements
- Generate removeXPaths list
- Add cleanText option
- Add unit tests

**Output Format**:
```javascript
{
  removeXPaths: [
    "//div[@class='ad-banner']",
    "//aside[@class='sidebar']"
  ],
  cleanText: true
}
```

**Dependencies**: 3.1

---

### 3.4 Implement template-writer.js

**Priority**: High | **Estimated Time**: 1 hour

Implement template file output module.

**Acceptance Criteria**:
- Create `lib/template-writer.js`
- Implement `TemplateWriter` class
- Implement `write(outputFile, data)` method
- Generate complete JSON format
- Add metadata (sampleCount, commonElements)
- Add timestamp
- Format JSON output
- Add unit tests

**Output Format**:
```javascript
{
  templateName: "api-doc",
  version: "1.0.0",
  generatedAt: "2024-01-15T10:30:00Z",
  samples: [...],
  xpaths: {...},
  filters: {...},
  metadata: {...}
}
```

**Dependencies**: 3.3

---

### 4.1 Implement main.js core logic

**Priority**: High | **Estimated Time**: 1.5 hours

Implement main process control logic.

**Acceptance Criteria**:
- Create `main.js`
- Implement `TemplateGenerator` class
- Implement `generate(templateName, patternsFile, outputFile)` method
- Integrate all modules
- Add progress output
- Add error handling
- Add unit tests

**Dependencies**: 3.4

---

### 4.2 Implement run-skill.js CLI entry point

**Priority**: High | **Estimated Time**: 1 hour

Implement command-line interface.

**Acceptance Criteria**:
- Create `run-skill.js`
- Parse command-line arguments
- Support `--input` parameter
- Support `--output` parameter
- Display help information
- Display progress information
- Handle errors with friendly messages
- Add usage examples

**Usage Example**:
```bash
node run-skill.js api-doc \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output ./output/api-doc.json
```

**Dependencies**: 4.1

---

### 4.3 End-to-end testing

**Priority**: High | **Estimated Time**: 2 hours

Complete end-to-end testing.

**Acceptance Criteria**:
- Create test script `test/test-e2e.js`
- Test complete workflow (api-doc template)
- Verify output file format is correct
- Verify XPath expressions are valid
- Verify metadata is correct
- Test error scenarios
- All tests pass

**Dependencies**: 4.2

---

### 4.4 Write documentation

**Priority**: Medium | **Estimated Time**: 2 hours

Write complete usage documentation.

**Acceptance Criteria**:
- Update `README.md` (features, installation, usage)
- Create `docs/USAGE_GUIDE.md` (detailed usage guide)
- Create `docs/XPATH_GUIDE.md` (XPath rules explanation)
- Update `SKILL.md` (skill metadata)
- Add usage examples
- Add FAQ

**Dependencies**: 4.3

---

## Summary

- **Total Tasks**: 18
- **Phase 1**: 6 tasks (Infrastructure)
- **Phase 2**: 5 tasks (Structure Analysis)
- **Phase 3**: 4 tasks (Rule Generation)
- **Phase 4**: 3 tasks (Integration and Testing)

## Milestones

1. **M1: Infrastructure Complete** - Tasks 1.1-1.6 complete
   - Can fetch page HTML
   
2. **M2: Structure Analysis Complete** - Tasks 2.1-2.5 complete
   - Can analyze HTML structure
   
3. **M3: Rule Generation Complete** - Tasks 3.1-3.4 complete
   - Can generate XPath rules
   
4. **M4: Project Complete** - Tasks 4.1-4.4 complete
   - Can run complete workflow and generate templates

## Notes

1. **Test-Driven**: Each module should have unit tests
2. **Error Handling**: All async operations need error handling
3. **Code Quality**: Keep code clean and readable
4. **Documentation Sync**: Keep code and documentation in sync
5. **Independence**: Ensure no dependency on stock-crawler code
