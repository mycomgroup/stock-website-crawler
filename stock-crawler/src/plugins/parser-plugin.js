class ParserPlugin {
  canHandle() {
    throw new Error('ParserPlugin.canHandle must be implemented by subclass');
  }

  async extract() {
    throw new Error('ParserPlugin.extract must be implemented by subclass');
  }

  normalize(result) {
    return result;
  }
}

export default ParserPlugin;
