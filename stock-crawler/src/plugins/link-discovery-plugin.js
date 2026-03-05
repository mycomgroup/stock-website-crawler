class LinkDiscoveryPlugin {
  async discover() {
    throw new Error('LinkDiscoveryPlugin.discover must be implemented by subclass');
  }
}

export default LinkDiscoveryPlugin;
