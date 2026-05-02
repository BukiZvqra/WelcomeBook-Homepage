require('dotenv').config();

module.exports = function(eleventyConfig) {
  // Get client_id from CLI environment variable
  const clientId = process.env.CLIENT_ID;

  if (!clientId) {
    throw new Error('CLIENT_ID environment variable is required. Run with: CLIENT_ID=yavor npx eleventy');
  }

  // Load client config
  let clientConfig;
  try {
    clientConfig = require(`./clients/${clientId}/website/config.json`);
  } catch (err) {
    throw new Error(`Could not load config for client: ${clientId}. Path: clients/${clientId}/website/config.json`);
  }

  // Determine which template to use
  const template = clientConfig.template || 'multiproperty';

  // Make config available globally in templates
  eleventyConfig.addGlobalData("client", clientConfig);

  // Cloudinary image shortcode (used as {% img "filename.jpg" %})
  eleventyConfig.addShortcode("img", function(filename) {
    const cloudName = process.env.CLOUDINARY_CLOUD_NAME || 'PLACEHOLDER';
    return `https://res.cloudinary.com/${cloudName}/image/upload/f_auto,q_auto/clients/${clientId}/${filename}`;
  });

  // Copy assets folder
  eleventyConfig.addPassthroughCopy({ [`templates/website-${template}/assets`]: "assets" });

  return {
    dir: {
      input: `templates/website-${template}/src`,
      output: `_site/${clientId}`,
      includes: "_includes",
      layouts: "_layouts"
    },
    templateFormats: ["njk", "md", "html"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk"
  };
};
