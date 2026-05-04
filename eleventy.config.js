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

  // Cloudinary image shortcode (used as {% img "filename.jpg" %} or {% img "filename.jpg", "hero" %})
  // Variants: "hero" = w_1600 retina fill | "thumb" = w_600 square fill | "full" = w_2000 lightbox
  eleventyConfig.addShortcode("img", function(filename, variant) {
    const cloudName = process.env.CLOUDINARY_CLOUD_NAME || 'PLACEHOLDER';
    const transforms = {
      hero:  'w_1600,c_fill,f_auto,q_auto:good',
      thumb: 'w_600,h_600,c_fill,f_auto,q_auto:eco',
      full:  'w_2000,c_limit,f_auto,q_auto:good'
    };
    const t = transforms[variant] || 'f_auto,q_auto';
    return `https://res.cloudinary.com/${cloudName}/image/upload/${t}/clients/${clientId}/${filename}`;
  });

  // Cloudinary shortcode for assets at account root (no clients/clientId prefix)
  eleventyConfig.addShortcode("imgabs", function(filename, variant) {
    const cloudName = process.env.CLOUDINARY_CLOUD_NAME || 'PLACEHOLDER';
    const transforms = {
      hero:  'w_1600,c_fill,f_auto,q_auto:good',
      thumb: 'w_600,h_600,c_fill,f_auto,q_auto:eco',
      full:  'w_2000,c_limit,f_auto,q_auto:good'
    };
    const t = transforms[variant] || 'f_auto,q_auto';
    return `https://res.cloudinary.com/${cloudName}/image/upload/${t}/${filename}`;
  });

  // Filter properties by complex id — replaces broken selectattr("equalto") in Eleventy Nunjucks
  eleventyConfig.addFilter("filterByComplex", (properties, complexId) => {
    if (!Array.isArray(properties)) return [];
    return properties.filter(p => p.complex === complexId);
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
