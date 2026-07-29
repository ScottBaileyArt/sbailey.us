module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy("src/images");
  eleventyConfig.addPassthroughCopy("src/css");

  // Oldest first, for listing pages.
  eleventyConfig.addCollection("orderedCollections", (api) =>
    api.getFilteredByTag("collections").sort((a, b) => a.data.number - b.data.number)
  );

  // The timeline nav runs newest-to-oldest, left to right.
  eleventyConfig.addCollection("timelineCollections", (api) =>
    api.getFilteredByTag("collections").sort((a, b) => b.data.number - a.data.number)
  );

  // Only 8 of the 17 collections have a long exhibition statement.
  eleventyConfig.addCollection("statements", (api) =>
    api.getFilteredByTag("collections").filter((item) => item.data.exhibition_statement)
  );

  return {
    dir: {
      input: "src",
      includes: "_includes",
      output: "_site",
    },
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
  };
};
