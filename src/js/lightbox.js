import PhotoSwipeLightbox from "/js/photoswipe/photoswipe-lightbox.esm.min.js";

const lightbox = new PhotoSwipeLightbox({
  gallery: ".artworkGallery",
  children: "a.artworkLink",
  pswpModule: () => import("/js/photoswipe/photoswipe.esm.min.js"),
});

// Caption reads data-pswp-caption off the clicked <a> -- see PhotoSwipe's
// own "Adding caption" docs for this pattern. No separate plugin needed.
lightbox.on("uiRegister", () => {
  lightbox.pswp.ui.registerElement({
    name: "caption",
    order: 9,
    isButton: false,
    appendTo: "root",
    onInit: (el) => {
      lightbox.pswp.on("change", () => {
        const link = lightbox.pswp.currSlide?.data?.element;
        el.innerHTML = link ? link.dataset.pswpCaption || "" : "";
      });
    },
  });
});

lightbox.init();
