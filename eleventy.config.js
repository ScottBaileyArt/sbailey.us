const path = require("path");
// @11ty/eleventy-img's classic callable API is the default export
// (named "queueImage" internally); the "Image" named export is a
// lower-level class, not directly callable.
const Image = require("@11ty/eleventy-img").default;
const { generateHTML } = require("@11ty/eleventy-img");

module.exports = function (eleventyConfig) {
  // Only the site-chrome images and collection-index icon crops are ever
  // linked directly (as /images/...). Everything else under src/images/ --
  // the full-resolution artwork source files -- is read straight off disk
  // by the image pipeline shortcodes below and only ever shipped as their
  // resized /img/... output, so it's deliberately not copied wholesale
  // here; that would roughly 6x the deployed site for files nothing links to.
  eleventyConfig.addPassthroughCopy("src/images/common");
  eleventyConfig.addPassthroughCopy("src/images/collections");
  eleventyConfig.addPassthroughCopy({
    "src/images/c17/c17 03Ws Accretion 5 Detail 2 icon.jpg":
      "images/c17/c17 03Ws Accretion 5 Detail 2 icon.jpg",
  });
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/js");

  eleventyConfig.addPassthroughCopy({
    "node_modules/photoswipe/dist/photoswipe.esm.min.js": "js/photoswipe/photoswipe.esm.min.js",
    "node_modules/photoswipe/dist/photoswipe-lightbox.esm.min.js":
      "js/photoswipe/photoswipe-lightbox.esm.min.js",
    "node_modules/photoswipe/dist/photoswipe.css": "css/photoswipe.css",
  });

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

  // Artwork thumbnails: responsive <picture>, WebP + JPEG fallback. Shown
  // 300px wide on wider screens and the full content width on phones (see
  // .artworkThumb in sb.css, which `sizes` must match: phones are under
  // 760px, with a 20px inset each side). Widths cover both at 1x-3x pixel
  // density; eleventy-img skips any that would upscale past the source. src
  // is a repo-relative path like "images/c17/foo.jpg". Deliberately resizes
  // down from the full-size `image` field rather than the pre-made
  // `thumbnail` file -- those are often already tiny (~216px), too small to
  // produce a sharp thumbnail from.
  eleventyConfig.addAsyncShortcode("thumbnailImage", async (src, alt) => {
    const metadata = await Image(path.join("src", src), {
      widths: [300, 600, 800, 1050],
      formats: ["webp", "jpeg"],
      outputDir: "_site/img/",
      urlPath: "/img/",
    });
    return generateHTML(metadata, {
      alt,
      sizes: "(max-width: 759px) calc(100vw - 40px), 300px",
      loading: "lazy",
      decoding: "async",
      class: "artworkThumb",
    });
  });

  // Homepage featured artwork, with its caption as the content between the
  // opening and closing tags:
  //   {% featuredArtwork "images/c17/foo.jpg", "Title", "/accretions/" %}
  //     ...caption...
  //   {% endfeaturedArtwork %}
  // Shown as wide as the window allows, but never taller than fits on screen
  // (.homeFeature in sb.css). That needs the image's proportions, which is
  // why the shortcode writes them out (--feature-ratio) rather than the page
  // hardcoding them, so changing the image needs nothing else changed.
  // `sizes` is the full window width, which is never smaller than the image
  // is shown. Not lazy-loaded -- it's the only image on the page and above
  // the fold.
  eleventyConfig.addPairedAsyncShortcode("featuredArtwork", async (caption, src, alt, href) => {
    const metadata = await Image(path.join("src", src), {
      widths: [800, 1200, 1800, 2400],
      formats: ["webp", "jpeg"],
      outputDir: "_site/img/",
      urlPath: "/img/",
    });
    const { width, height } = metadata.jpeg[metadata.jpeg.length - 1];
    const picture = generateHTML(metadata, {
      alt,
      sizes: "100vw",
      decoding: "async",
      class: "heroImage",
    });
    return `<figure class="homeFeature" style="--feature-ratio: ${(width / height).toFixed(4)}">`
      + `<a href="${href}">${picture}</a>`
      + `<figcaption class="homeCaption">${caption}</figcaption>`
      + `</figure>`;
  });

  // Lightbox full-size image: real responsive loading, not one fixed size
  // for every visitor. Several widths are generated (eleventy-img silently
  // skips any that would upscale past the source), and data-pswp-srcset --
  // read natively by PhotoSwipe -- lets it pick a size appropriate to the
  // viewer's actual screen and zoom level, same principle as the thumbnail
  // srcset. href/width/height (used for the no-JS fallback and PhotoSwipe's
  // zoom ceiling) come from the largest generated size. Dimensions are the
  // real generated output, not stored metadata, since they must exactly
  // match what's served. (Returning an object here for use via {% set %}
  // does not work with Eleventy's async shortcodes; this direct-output
  // form does.)
  eleventyConfig.addAsyncShortcode("lightboxImageAttrs", async (src) => {
    const metadata = await Image(path.join("src", src), {
      widths: [800, 1600, 2400],
      formats: ["jpeg"],
      outputDir: "_site/img/",
      urlPath: "/img/",
    });
    const sizes = metadata.jpeg;
    const largest = sizes[sizes.length - 1];
    const srcset = sizes.map((s) => `${s.url} ${s.width}w`).join(", ");
    return `href="${largest.url}" data-pswp-width="${largest.width}" `
      + `data-pswp-height="${largest.height}" data-pswp-srcset="${srcset}"`;
  });

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
