class ExtractionResult {
  constructor({ url, title, type = 'generic', contentBlocks = [], artifacts = {}, quality = {} }) {
    this.meta = {
      url,
      title,
      extractedAt: Date.now(),
      type
    };
    this.contentBlocks = contentBlocks;
    this.artifacts = artifacts;
    this.quality = quality;
  }
}

export default ExtractionResult;
