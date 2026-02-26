/**
 * 测试parseURLs()方法
 */

const LinksReader = require('../lib/links-reader');

async function testParseURLs() {
  const reader = new LinksReader();
  let testsPassed = 0;
  let testsFailed = 0;
  
  console.log('=== parseURLs() 方法测试 ===\n');
  
  // 测试1: 解析有效的URL字符串
  console.log('测试1: 解析有效的URL字符串');
  console.log('-------------------');
  try {
    const urlStrings = [
      'https://www.lixinger.com/open/api/doc?api-key=cn/company',
      'https://www.lixinger.com/analytics/company/dashboard',
      'https://example.com:8080/path/to/page?query=value#fragment'
    ];
    
    const urlObjects = reader.parseURLs(urlStrings);
    
    console.log(`✓ 成功解析 ${urlObjects.length} 个URL对象`);
    console.log(`  URL 1:`);
    console.log(`    - href: ${urlObjects[0].href}`);
    console.log(`    - protocol: ${urlObjects[0].protocol}`);
    console.log(`    - hostname: ${urlObjects[0].hostname}`);
    console.log(`    - pathname: ${urlObjects[0].pathname}`);
    console.log(`    - search: ${urlObjects[0].search}`);
    console.log(`  URL 3:`);
    console.log(`    - port: ${urlObjects[2].port}`);
    console.log(`    - hash: ${urlObjects[2].hash}`);
    
    if (urlObjects.length === 3 && 
        urlObjects[0] instanceof URL &&
        urlObjects[0].hostname === 'www.lixinger.com' &&
        urlObjects[0].pathname === '/open/api/doc' &&
        urlObjects[2].port === '8080') {
      testsPassed++;
    } else {
      console.log(`✗ URL对象属性不符合预期`);
      testsFailed++;
    }
  } catch (error) {
    console.log(`✗ 测试失败: ${error.message}`);
    testsFailed++;
  }
  
  // 测试2: 处理无效的URL（不跳过）
  console.log('\n测试2: 处理无效的URL（不跳过）');
  console.log('-------------------');
  try {
    const urlStrings = [
      'https://valid.com/page',
      'not a valid url',
      'https://another-valid.com'
    ];
    
    reader.parseURLs(urlStrings);
    console.log(`✗ 应该抛出错误但没有`);
    testsFailed++;
  } catch (error) {
    if (error.message.includes('Invalid URL at index 1')) {
      console.log(`✓ 正确抛出错误: ${error.message}`);
      testsPassed++;
    } else {
      console.log(`✗ 错误消息不符合预期: ${error.message}`);
      testsFailed++;
    }
  }
  
  // 测试3: 跳过无效的URL
  console.log('\n测试3: 跳过无效的URL');
  console.log('-------------------');
  try {
    const urlStrings = [
      'https://valid1.com/page',
      'not a valid url',
      'https://valid2.com',
      'also invalid',
      'https://valid3.com/path'
    ];
    
    const urlObjects = reader.parseURLs(urlStrings, { skipInvalid: true });
    
    console.log(`✓ 成功解析 ${urlObjects.length} 个有效URL（跳过了无效的）`);
    console.log(`  有效URL:`);
    urlObjects.forEach((url, i) => {
      console.log(`    ${i + 1}. ${url.hostname}`);
    });
    
    if (urlObjects.length === 3 &&
        urlObjects[0].hostname === 'valid1.com' &&
        urlObjects[1].hostname === 'valid2.com' &&
        urlObjects[2].hostname === 'valid3.com') {
      testsPassed++;
    } else {
      console.log(`✗ 解析结果不符合预期`);
      testsFailed++;
    }
  } catch (error) {
    console.log(`✗ 测试失败: ${error.message}`);
    testsFailed++;
  }
  
  // 测试4: 空数组
  console.log('\n测试4: 空数组');
  console.log('-------------------');
  try {
    const urlObjects = reader.parseURLs([]);
    
    console.log(`✓ 空数组返回空结果: ${urlObjects.length} 个URL`);
    
    if (urlObjects.length === 0) {
      testsPassed++;
    } else {
      console.log(`✗ 预期0个URL，实际${urlObjects.length}个`);
      testsFailed++;
    }
  } catch (error) {
    console.log(`✗ 测试失败: ${error.message}`);
    testsFailed++;
  }
  
  // 测试5: 完整工作流（从记录到URL对象）
  console.log('\n测试5: 完整工作流（从记录到URL对象）');
  console.log('-------------------');
  try {
    const records = [
      { url: 'https://www.lixinger.com/open/api/doc?api-key=cn/company', status: 'fetched', error: null },
      { url: 'https://www.lixinger.com/open/api/doc?api-key=hk/index', status: 'fetched', error: null },
      { url: 'https://www.lixinger.com/analytics/company/dashboard', status: 'pending', error: null },
      { url: 'https://www.lixinger.com/open/api/doc?api-key=us/stock', status: 'fetched', error: 'timeout' }
    ];
    
    // 步骤1: 提取URL字符串（只要fetched且无错误的）
    const urlStrings = reader.extractURLs(records, { status: 'fetched', excludeErrors: true });
    console.log(`✓ 步骤1: 提取了 ${urlStrings.length} 个URL字符串`);
    
    // 步骤2: 解析为URL对象
    const urlObjects = reader.parseURLs(urlStrings);
    console.log(`✓ 步骤2: 解析为 ${urlObjects.length} 个URL对象`);
    
    // 验证结果
    console.log(`  URL对象详情:`);
    urlObjects.forEach((url, i) => {
      console.log(`    ${i + 1}. ${url.pathname}${url.search}`);
    });
    
    if (urlObjects.length === 2 &&
        urlObjects[0].searchParams.get('api-key') === 'cn/company' &&
        urlObjects[1].searchParams.get('api-key') === 'hk/index') {
      testsPassed++;
    } else {
      console.log(`✗ 工作流结果不符合预期`);
      testsFailed++;
    }
  } catch (error) {
    console.log(`✗ 测试失败: ${error.message}`);
    testsFailed++;
  }
  
  // 总结
  console.log('\n=== 测试总结 ===');
  console.log(`通过: ${testsPassed}`);
  console.log(`失败: ${testsFailed}`);
  console.log(`总计: ${testsPassed + testsFailed}`);
  
  if (testsFailed === 0) {
    console.log('\n✓ 所有测试通过！');
  } else {
    console.log(`\n✗ ${testsFailed} 个测试失败`);
    process.exit(1);
  }
}

// 运行测试
testParseURLs().catch(error => {
  console.error('测试运行失败:', error);
  process.exit(1);
});
