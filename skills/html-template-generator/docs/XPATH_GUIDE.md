# XPath Guide for HTML Template Generator

## Table of Contents

1. [Introduction to XPath](#introduction-to-xpath)
2. [XPath Basics](#xpath-basics)
3. [Generated XPath Patterns](#generated-xpath-patterns)
4. [Understanding Template XPath](#understanding-template-xpath)
5. [Customizing XPath Rules](#customizing-xpath-rules)
6. [XPath Best Practices](#xpath-best-practices)
7. [Common XPath Patterns](#common-xpath-patterns)
8. [Troubleshooting XPath](#troubleshooting-xpath)

## Introduction to XPath

XPath (XML Path Language) is a query language for selecting nodes from an XML/HTML document. The HTML Template Generator uses XPath because it's more powerful than CSS selectors for data extraction.

### Why XPath?

**Advantages over CSS Selectors:**
- ✅ Can select based on text content: `//h2[contains(text(), 'Parameters')]`
- ✅ Can navigate up to parent elements: `//table/../div`
- ✅ Supports complex logic: `//div[@class='content' and not(@class='hidden')]`
- ✅ Can select by position: `//table[1]`, `//table[last()]`
- ✅ More expressive for data extraction

**When to Use CSS Selectors:**
- Styling and visual selection
- Simple element selection
- Browser DevTools testing

**When to Use XPath:**
- Data extraction and scraping
- Complex element relationships
- Text-based selection
- Template generation (like this tool)

## XPath Basics

### Syntax Overview

```xpath
// - Select from anywhere in document
/  - Select from root or direct child
.  - Current node
.. - Parent node
@  - Attribute
[] - Predicate (filter)
```

### Simple Examples

```xpath
# Select all h1 elements
//h1

# Select h1 with specific class
//h1[@class='title']

# Select h1 text content
//h1[@class='title']/text()

# Select all paragraphs inside main
//main//p

# Select first table
//table[1]

# Select last table
//table[last()]
```

### Predicates (Filters)

```xpath
# Element with specific attribute
//div[@id='content']

# Element with class containing text
//div[contains(@class, 'article')]

# Element with specific text
//h2[text()='Introduction']

# Element containing text
//h2[contains(text(), 'Intro')]

# Multiple conditions (AND)
//div[@class='content' and @id='main']

# Multiple conditions (OR)
//div[@class='content' or @class='article']

# Negation
//div[not(@class='hidden')]
```

### Axes (Navigation)

```xpath
# Child axis (default)
//div/p

# Descendant axis
//div//p

# Parent axis
//table/..

# Following sibling
//h2/following-sibling::p

# Preceding sibling
//h2/preceding-sibling::h1

# Ancestor
//td/ancestor::table
```

## Generated XPath Patterns

The HTML Template Generator creates XPath expressions following specific patterns. Understanding these patterns helps you customize and debug templates.

### Pattern 1: Attribute-Based Selection

**Generated XPath:**
```xpath
//h1[@class='page-title']
```

**Why this pattern:**
- Most stable selector
- Uses unique class or id
- Avoids position-based selection

**HTML Example:**
```html
<h1 class="page-title">API Documentation</h1>
```

### Pattern 2: Contains for Multiple Classes

**Generated XPath:**
```xpath
//div[contains(@class, 'main-content')]
```

**Why this pattern:**
- Works when element has multiple classes
- More flexible than exact match
- Handles dynamic class names

**HTML Example:**
```html
<div class="main-content container-fluid">...</div>
```

### Pattern 3: Relative Paths

**Generated XPath:**
```xpath
.//h2/text()
```

**Why this pattern:**
- Searches within current context
- Used in nested extraction
- More efficient than absolute paths

**Usage in Template:**
```json
{
  "sections": {
    "xpath": "//section[@class='api-section']",
    "extract": {
      "heading": ".//h2/text()"  // Relative to section
    }
  }
}
```

### Pattern 4: Text Extraction

**Generated XPath:**
```xpath
//h1[@class='title']/text()
```

**Why this pattern:**
- Extracts text content only
- Excludes child element tags
- Returns clean text

**HTML Example:**
```html
<h1 class="title">Hello <span>World</span></h1>
<!-- /text() returns: "Hello " (not "Hello World") -->
<!-- Use string() for all text: string(//h1[@class='title']) -->
```

### Pattern 5: Table Structure

**Generated XPath:**
```json
{
  "xpath": ".//table[@class='params-table']",
  "headers": ".//thead/tr/th/text()",
  "rows": ".//tbody/tr",
  "cells": ".//td/text()"
}
```

**Why this pattern:**
- Captures complete table structure
- Separates headers from data
- Allows row-by-row processing

### Pattern 6: Filter Rules

**Generated XPath:**
```xpath
//nav
//aside
//div[contains(@class, 'ad')]
//div[contains(@class, 'sidebar')]
```

**Why this pattern:**
- Removes navigation elements
- Filters out advertisements
- Cleans up noise content

## Understanding Template XPath

### Template Structure

```json
{
  "xpaths": {
    "title": "//h1[@class='page-title']/text()",
    "sections": {
      "xpath": "//section[@class='api-section']",
      "extract": {
        "heading": ".//h2/text()",
        "description": ".//p[@class='description']/text()",
        "table": {
          "xpath": ".//table[@class='params-table']",
          "headers": ".//thead/tr/th/text()",
          "rows": ".//tbody/tr"
        }
      }
    }
  }
}
```

### Execution Flow

1. **Extract Title** (absolute path):
   ```xpath
   //h1[@class='page-title']/text()
   ```
   Searches entire document for h1 with class 'page-title'

2. **Find Sections** (absolute path):
   ```xpath
   //section[@class='api-section']
   ```
   Finds all section elements with class 'api-section'

3. **For Each Section** (relative paths):
   ```xpath
   .//h2/text()                    # Heading within section
   .//p[@class='description']/text() # Description within section
   .//table[@class='params-table']   # Table within section
   ```

4. **For Each Table** (relative paths):
   ```xpath
   .//thead/tr/th/text()  # Headers within table
   .//tbody/tr            # Rows within table
   ```

### Absolute vs Relative Paths

**Absolute Path (`//`):**
- Searches from document root
- Used for top-level elements
- Example: `//h1[@class='title']`

**Relative Path (`.//`):**
- Searches from current context
- Used for nested elements
- Example: `.//p` (paragraphs within current element)

**When to Use Each:**

```javascript
// Absolute: Top-level title
const title = xpath.select("//h1[@class='title']/text()", doc);

// Relative: Content within sections
const sections = xpath.select("//section", doc);
for (const section of sections) {
  // Relative to section
  const heading = xpath.select(".//h2/text()", section);
  const paragraphs = xpath.select(".//p/text()", section);
}
```

## Customizing XPath Rules

### Common Customizations

#### 1. Make XPath More Specific

**Original:**
```xpath
//table
```

**More Specific:**
```xpath
//table[@class='data-table' and contains(@id, 'results')]
```

#### 2. Make XPath More Flexible

**Original:**
```xpath
//div[@class='main-content']
```

**More Flexible:**
```xpath
//div[contains(@class, 'content')]
```

#### 3. Add Text-Based Selection

**Original:**
```xpath
//h2[@class='section-title']
```

**With Text Filter:**
```xpath
//h2[@class='section-title' and contains(text(), 'Parameters')]
```

#### 4. Select by Position

**Original:**
```xpath
//table
```

**First Table:**
```xpath
//table[1]
```

**Last Table:**
```xpath
//table[last()]
```

**Second to Last:**
```xpath
//table[last()-1]
```

#### 5. Navigate to Parent

**Original:**
```xpath
//td[@class='value']
```

**Get Parent Row:**
```xpath
//td[@class='value']/..
```

**Get Ancestor Table:**
```xpath
//td[@class='value']/ancestor::table
```

#### 6. Get All Text (Including Children)

**Original:**
```xpath
//div[@class='content']/text()
```

**All Text:**
```xpath
string(//div[@class='content'])
```

### Modifying Generated Templates

#### Example: Add Custom Extraction

```json
{
  "xpaths": {
    "title": "//h1[@class='page-title']/text()",
    
    // Add custom field
    "author": "//span[@class='author-name']/text()",
    "publishDate": "//time[@class='publish-date']/@datetime",
    
    "sections": {
      "xpath": "//section[@class='api-section']",
      "extract": {
        "heading": ".//h2/text()",
        
        // Add custom nested field
        "examples": {
          "xpath": ".//div[@class='example']",
          "code": ".//pre/code/text()",
          "language": ".//pre/code/@class"
        }
      }
    }
  }
}
```

#### Example: Refine Table Extraction

```json
{
  "table": {
    "xpath": ".//table[@class='params-table']",
    
    // Original
    "headers": ".//thead/tr/th/text()",
    "rows": ".//tbody/tr",
    
    // Add cell extraction with structure
    "data": {
      "xpath": ".//tbody/tr",
      "cells": {
        "name": ".//td[1]/text()",
        "type": ".//td[2]/text()",
        "required": ".//td[3]/text()",
        "description": ".//td[4]/text()"
      }
    }
  }
}
```

## XPath Best Practices

### 1. Prefer Attributes Over Position

❌ **Bad:**
```xpath
/html/body/div[3]/div[2]/table[1]
```

✅ **Good:**
```xpath
//table[@class='data-table']
```

**Why:** Position-based XPath breaks when page structure changes.

### 2. Use `contains()` for Flexibility

❌ **Bad:**
```xpath
//div[@class='main-content container-fluid responsive']
```

✅ **Good:**
```xpath
//div[contains(@class, 'main-content')]
```

**Why:** Classes may change or have multiple values.

### 3. Avoid Overly Specific Paths

❌ **Bad:**
```xpath
//div[@id='root']/div[@class='app']/main[@class='content']/section[@class='api']/h1
```

✅ **Good:**
```xpath
//section[@class='api']//h1
```

**Why:** Shorter paths are more maintainable and flexible.

### 4. Use Relative Paths in Nested Extraction

❌ **Bad:**
```xpath
// In section context
"heading": "//h2/text()"  // Searches entire document
```

✅ **Good:**
```xpath
// In section context
"heading": ".//h2/text()"  // Searches within section
```

**Why:** Relative paths respect context and are more efficient.

### 5. Handle Missing Elements

```javascript
// Check if element exists before extracting
const titleNodes = xpath.select("//h1[@class='title']/text()", doc);
const title = titleNodes.length > 0 ? titleNodes[0].data : 'No title';
```

### 6. Use Specific Selectors

❌ **Bad:**
```xpath
//div  // Too broad
```

✅ **Good:**
```xpath
//div[@class='article-content']  // Specific
```

**Why:** Specific selectors are faster and more accurate.

### 7. Test XPath in Browser

```javascript
// In Chrome DevTools Console
$x("//h1[@class='title']")  // Returns array of elements
$x("//h1[@class='title']/text()")  // Returns text nodes
```

## Common XPath Patterns

### Pattern: Extract Links

```xpath
# All links
//a/@href

# Links in navigation
//nav//a/@href

# Links with specific text
//a[contains(text(), 'Read more')]/@href

# External links
//a[starts-with(@href, 'http')]/@href
```

### Pattern: Extract Images

```xpath
# All image sources
//img/@src

# Images with alt text
//img[@alt]/@src

# Images in specific container
//div[@class='gallery']//img/@src
```

### Pattern: Extract Lists

```xpath
# All list items
//ul/li/text()

# Ordered list items
//ol/li/text()

# Nested lists
//ul//li/text()

# List items with links
//ul/li/a/text()
```

### Pattern: Extract Tables

```xpath
# Table headers
//table//th/text()

# Table cells
//table//td/text()

# Specific column (2nd column)
//table//tr/td[2]/text()

# Rows with specific content
//table//tr[td[contains(text(), 'Active')]]
```

### Pattern: Extract Metadata

```xpath
# Meta description
//meta[@name='description']/@content

# Meta keywords
//meta[@name='keywords']/@content

# Open Graph title
//meta[@property='og:title']/@content

# Canonical URL
//link[@rel='canonical']/@href
```

### Pattern: Extract Code Blocks

```xpath
# All code blocks
//pre/code/text()

# Code with language class
//pre/code[@class='language-javascript']/text()

# Inline code
//code/text()
```

### Pattern: Extract Dates

```xpath
# Time elements
//time/@datetime

# Date in specific format
//span[@class='date']/text()

# Published date
//meta[@property='article:published_time']/@content
```

## Troubleshooting XPath

### Problem: XPath Returns Empty

**Possible Causes:**
1. Element doesn't exist
2. Wrong attribute name or value
3. Case sensitivity issue
4. Namespace issue (XML)

**Solutions:**
```xpath
# Check if element exists
//h1  # Returns any h1

# Check attribute
//h1[@class]  # Returns h1 with any class

# Case-insensitive search
//h1[contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'title')]
```

### Problem: XPath Returns Too Many Results

**Solution:** Add more specific predicates
```xpath
# Too broad
//div

# More specific
//div[@class='content' and @id='main']

# Even more specific
//div[@class='content' and @id='main']/div[@class='article']
```

### Problem: XPath Breaks After Site Update

**Solution:** Use more flexible selectors
```xpath
# Brittle
//div[@class='main-content-v2-responsive']

# Flexible
//div[contains(@class, 'main-content')]

# Very flexible
//main | //div[@role='main'] | //div[contains(@class, 'content')]
```

### Problem: Can't Select by Text

**Solution:** Use `contains()` or `text()`
```xpath
# Exact match
//h2[text()='Introduction']

# Partial match
//h2[contains(text(), 'Intro')]

# Case-insensitive
//h2[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'intro')]
```

### Problem: Need Parent Element

**Solution:** Use parent axis
```xpath
# Get parent
//td[@class='value']/..

# Get specific ancestor
//td[@class='value']/ancestor::tr

# Get ancestor with condition
//td[@class='value']/ancestor::tr[@class='data-row']
```

## Testing XPath

### In Browser DevTools

```javascript
// Chrome/Firefox Console

// Test XPath
$x("//h1[@class='title']")

// Get text content
$x("//h1[@class='title']/text()")[0].data

// Get attribute
$x("//a[@class='link']/@href")[0].value

// Count results
$x("//table").length
```

### In Node.js

```javascript
import { JSDOM } from 'jsdom';
import xpath from 'xpath';

const html = '<h1 class="title">Hello</h1>';
const dom = new JSDOM(html);
const doc = dom.window.document;

// Test XPath
const result = xpath.select("//h1[@class='title']/text()", doc);
console.log(result[0].data);  // "Hello"
```

### Validation Script

```javascript
// validate-xpath.js
import fs from 'fs/promises';
import { JSDOM } from 'jsdom';
import xpath from 'xpath';

async function validateTemplate(templateFile, sampleHTML) {
  const template = JSON.parse(await fs.readFile(templateFile, 'utf-8'));
  const dom = new JSDOM(sampleHTML);
  const doc = dom.window.document;
  
  // Test title XPath
  const title = xpath.select(template.xpaths.title, doc);
  console.log('Title:', title.length > 0 ? '✓' : '✗');
  
  // Test sections XPath
  const sections = xpath.select(template.xpaths.sections.xpath, doc);
  console.log('Sections:', sections.length > 0 ? '✓' : '✗');
}
```

## Resources

### XPath References

- [MDN XPath Documentation](https://developer.mozilla.org/en-US/docs/Web/XPath)
- [W3C XPath Specification](https://www.w3.org/TR/xpath/)
- [XPath Cheat Sheet](https://devhints.io/xpath)

### Tools

- [XPath Tester](https://www.freeformatter.com/xpath-tester.html)
- Chrome DevTools Console (`$x()` function)
- Firefox Developer Tools

### Libraries

- [xpath (npm)](https://www.npmjs.com/package/xpath) - XPath evaluation
- [jsdom (npm)](https://www.npmjs.com/package/jsdom) - HTML parsing with XPath support
- [playwright (npm)](https://www.npmjs.com/package/playwright) - Browser automation

## Next Steps

- Practice XPath in browser DevTools
- Customize generated templates for your needs
- Test XPath expressions on sample pages
- Read the [Usage Guide](USAGE_GUIDE.md) for more examples
- Check the [FAQ](FAQ.md) for common issues
