import fs from 'fs';
import { isValidUrl } from './url-utils.js';

/**
 * Link Manager - 负责管理URL列表的读取、写入、去重和状态跟踪
 */
class LinkManager {
  constructor() {
    this.links = [];
  }

  /**
   * 从文件加载链接列表
   * @param {string} filePath - links.txt路径
   * @returns {Link[]} 链接对象数组
   */
  loadLinks(filePath) {
    // 如果文件不存在，返回空数组
    if (!fs.existsSync(filePath)) {
      this.links = [];
      return this.links;
    }

    try {
      const fileContent = fs.readFileSync(filePath, 'utf-8');
      const lines = fileContent.split('\n').filter(line => line.trim() !== '');
      
      this.links = lines.map(line => {
        try {
          // 尝试解析JSON格式的链接对象
          return JSON.parse(line);
        } catch (e) {
          // 如果不是JSON，则作为简单URL处理
          return {
            url: line.trim(),
            status: 'unfetched',
            addedAt: Date.now(),
            fetchedAt: null,
            retryCount: 0,
            error: null
          };
        }
      });

      return this.links;
    } catch (error) {
      throw new Error(`读取链接文件失败: ${error.message}`);
    }
  }

  /**
   * 保存链接列表到文件
   * @param {string} filePath - links.txt路径
   * @param {Link[]} links - 链接对象数组
   */
  saveLinks(filePath, links) {
    try {
      // 将每个链接对象转换为JSON字符串，每行一个
      const content = links.map(link => JSON.stringify(link)).join('\n');
      fs.writeFileSync(filePath, content, 'utf-8');
    } catch (error) {
      throw new Error(`保存链接文件失败: ${error.message}`);
    }
  }

  /**
   * 添加新链接
   * @param {string} url - URL字符串
   * @param {string} status - 状态：unfetched/fetching/fetched/failed
   */
  addLink(url, status = 'unfetched') {
    // 验证URL的有效性
    if (!isValidUrl(url)) {
      console.warn(`Skipped invalid URL when adding: ${url}`);
      return;
    }
    
    // 去掉URL中的锚点（#后面的部分）
    const urlWithoutAnchor = url.split('#')[0];
    
    // 检查链接是否已存在
    const existingLink = this.links.find(link => link.url === urlWithoutAnchor);
    if (existingLink) {
      return; // 已存在，不添加
    }

    const newLink = {
      url: urlWithoutAnchor,
      status,
      addedAt: Date.now(),
      fetchedAt: null,
      retryCount: 0,
      error: null
    };

    this.links.push(newLink);
  }

  /**
   * 更新链接状态
   * @param {string} url - URL字符串
   * @param {string} status - 新状态
   * @param {string} error - 错误信息（可选）
   */
  updateLinkStatus(url, status, error = null) {
    // 去掉URL中的锚点（#后面的部分）
    const urlWithoutAnchor = url.split('#')[0];
    
    const link = this.links.find(l => l.url === urlWithoutAnchor);
    if (link) {
      link.status = status;
      if (status === 'fetched') {
        link.fetchedAt = Date.now();
      }
      if (error) {
        link.error = error;
      }
    }
  }

  /**
   * 获取待爬取的链接
   * @returns {Link[]} 状态为unfetched的链接
   */
  getUnfetchedLinks() {
    return this.links.filter(link => link.status === 'unfetched');
  }

  /**
   * 增加重试次数
   * @param {string} url - URL字符串
   * @returns {number} 当前重试次数
   */
  incrementRetryCount(url) {
    const urlWithoutAnchor = url.split('#')[0];
    const link = this.links.find(l => l.url === urlWithoutAnchor);
    if (link) {
      link.retryCount++;
      return link.retryCount;
    }
    return 0;
  }

  /**
   * 去重和排序
   */
  deduplicateAndSort() {
    // 使用Map去重，保留第一次出现的链接
    const uniqueLinksMap = new Map();
    for (const link of this.links) {
      if (!uniqueLinksMap.has(link.url)) {
        uniqueLinksMap.set(link.url, link);
      }
    }

    // 转换回数组并按URL排序
    this.links = Array.from(uniqueLinksMap.values()).sort((a, b) => {
      return a.url.localeCompare(b.url);
    });
  }
}

export default LinkManager;
