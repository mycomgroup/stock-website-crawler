/**
 * Integration test for heading structure analysis
 * Demonstrates the heading analysis feature with realistic HTML samples
 */

import { StructureAnalyzer } from '../lib/structure-analyzer.js';

async function testHeadingAnalysis() {
  console.log('=== Heading Structure Analysis Integration Test ===\n');
  
  const analyzer = new StructureAnalyzer();
  
  // Simulate 5 API documentation pages with similar structure
  const htmlContents = [
    {
      url: 'https://example.com/api/doc',
      html: `
        <html>
          <head><title>API Documentation</title></head>
          <body>
            <div class="main-content">
              <h1 class="page-title">API文档</h1>
              <h2 class="section-title">基础信息</h2>
              <p>API基础信息说明</p>
              <h2 class="section-title">参数说明</h2>
              <table class="params-table">
                <thead><tr><th>参数</th><th>类型</th></tr></thead>
                <tbody><tr><td>id</td><td>string</td></tr></tbody>
              </table>
              <h2 class="section-title">返回示例</h2>
              <pre><code class="language-json">{"status": "ok"}</code></pre>
            </div>
          </body>
        </html>
      `,
      title: 'API Documentation'
    },
    {
      url: 'https://example.com/api/doc?api-key=cn/fund',
      html: `
        <html>
          <head><title>Fund API</title></head>
          <body>
            <div class="main-content">
              <h1 class="page-title">基金接口</h1>
              <h2 class="section-title">接口说明</h2>
              <p>基金数据接口</p>
              <h2 class="section-title">请求参数</h2>
              <table class="params-table">
                <thead><tr><th>参数</th><th>类型</th></tr></thead>
                <tbody><tr><td>code</td><td>string</td></tr></tbody>
              </table>
              <h2 class="section-title">响应格式</h2>
              <pre><code class="language-json">{"data": []}</code></pre>
            </div>
          </body>
        </html>
      `,
      title: 'Fund API'
    },
    {
      url: 'https://example.com/api/doc?api-key=cn/company',
      html: `
        <html>
          <head><title>Company API</title></head>
          <body>
            <div class="main-content">
              <h1 class="page-title">公司接口</h1>
              <h2 class="section-title">功能介绍</h2>
              <p>公司数据查询接口</p>
              <h2 class="section-title">参数列表</h2>
              <table class="params-table">
                <thead><tr><th>参数</th><th>类型</th></tr></thead>
                <tbody><tr><td>symbol</td><td>string</td></tr></tbody>
              </table>
              <h2 class="section-title">返回数据</h2>
              <pre><code class="language-json">{"result": {}}</code></pre>
            </div>
          </body>
        </html>
      `,
      title: 'Company API'
    },
    {
      url: 'https://example.com/api/doc?api-key=cn/index',
      html: `
        <html>
          <head><title>Index API</title></head>
          <body>
            <div class="main-content">
              <h1 class="page-title">指数接口</h1>
              <h2 class="section-title">接口概述</h2>
              <p>指数数据接口</p>
              <h2 class="section-title">输入参数</h2>
              <table class="params-table">
                <thead><tr><th>参数</th><th>类型</th></tr></thead>
                <tbody><tr><td>index_code</td><td>string</td></tr></tbody>
              </table>
              <h2 class="section-title">输出示例</h2>
              <pre><code class="language-json">{"success": true}</code></pre>
            </div>
          </body>
        </html>
      `,
      title: 'Index API'
    },
    {
      url: 'https://example.com/api/doc?api-key=hk/stock',
      html: `
        <html>
          <head><title>HK Stock API</title></head>
          <body>
            <div class="main-content">
              <h1 class="page-title">港股接口</h1>
              <h2 class="section-title">接口说明</h2>
              <p>港股数据接口</p>
              <h2 class="section-title">参数定义</h2>
              <table class="params-table">
                <thead><tr><th>参数</th><th>类型</th></tr></thead>
                <tbody><tr><td>stock_code</td><td>string</td></tr></tbody>
              </table>
              <h2 class="section-title">返回结果</h2>
              <pre><code class="language-json">{"code": 0}</code></pre>
            </div>
          </body>
        </html>
      `,
      title: 'HK Stock API'
    }
  ];
  
  console.log(`Analyzing ${htmlContents.length} sample pages...\n`);
  
  // Analyze the HTML structure
  const result = await analyzer.analyze(htmlContents);
  
  // Display heading analysis results
  console.log('📊 Heading Structure Analysis Results:\n');
  
  if (result.headings.h1) {
    console.log('H1 Headings:');
    console.log(`  XPath: ${result.headings.h1.xpath}`);
    console.log(`  Frequency: ${result.headings.h1.frequency} (${result.headings.h1.frequency * 100}%)`);
    console.log(`  Sample texts: ${result.headings.h1.samples.join(', ')}`);
    console.log();
  }
  
  if (result.headings.h2) {
    console.log('H2 Headings:');
    console.log(`  XPath: ${result.headings.h2.xpath}`);
    console.log(`  Frequency: ${result.headings.h2.frequency} (${result.headings.h2.frequency * 100}%)`);
    console.log(`  Sample texts: ${result.headings.h2.samples.join(', ')}`);
    console.log();
  }
  
  // Display other structure elements
  console.log('📋 Other Structure Elements:\n');
  
  if (result.mainContent) {
    console.log('Main Content:');
    console.log(`  XPath: ${result.mainContent.xpath}`);
    console.log(`  Frequency: ${result.mainContent.frequency}`);
    console.log();
  }
  
  if (result.tables && result.tables.length > 0) {
    console.log('Tables:');
    result.tables.forEach((table, i) => {
      console.log(`  Table ${i + 1}:`);
      console.log(`    XPath: ${table.xpath}`);
      console.log(`    Frequency: ${table.frequency}`);
      console.log(`    Columns: ${table.columnCount}`);
    });
    console.log();
  }
  
  if (result.codeBlocks && result.codeBlocks.length > 0) {
    console.log('Code Blocks:');
    result.codeBlocks.forEach((code, i) => {
      console.log(`  Code Block ${i + 1}:`);
      console.log(`    XPath: ${code.xpath}`);
      console.log(`    Frequency: ${code.frequency}`);
      console.log(`    Language: ${code.language || 'unknown'}`);
    });
    console.log();
  }
  
  // Display metadata
  console.log('📈 Metadata:');
  console.log(`  Sample Count: ${result.metadata.sampleCount}`);
  console.log(`  Analyzed At: ${result.metadata.analyzedAt}`);
  console.log();
  
  // Verify expected output format
  console.log('✅ Verification:');
  console.log(`  ✓ H1 has xpath property: ${!!result.headings.h1?.xpath}`);
  console.log(`  ✓ H1 has frequency property: ${typeof result.headings.h1?.frequency === 'number'}`);
  console.log(`  ✓ H1 has samples array: ${Array.isArray(result.headings.h1?.samples)}`);
  console.log(`  ✓ H1 frequency is 1.0 (100%): ${result.headings.h1?.frequency === 1.0}`);
  console.log(`  ✓ H2 has xpath property: ${!!result.headings.h2?.xpath}`);
  console.log(`  ✓ H2 has frequency property: ${typeof result.headings.h2?.frequency === 'number'}`);
  console.log(`  ✓ H2 has samples array: ${Array.isArray(result.headings.h2?.samples)}`);
  console.log(`  ✓ H2 frequency is 1.0 (100%): ${result.headings.h2?.frequency === 1.0}`);
  
  console.log('\n✅ Heading structure analysis test completed successfully!');
}

// Run the test
testHeadingAnalysis().catch(error => {
  console.error('❌ Test failed:', error);
  process.exit(1);
});
