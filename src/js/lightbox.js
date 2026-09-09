import PhotoSwipeLightbox from "/js/photoswipe/photoswipe-lightbox.esm.min.js";

// CAPTION_HEIGHT must match the reserved space in the .pswp__custom-caption
// CSS rule (sb.css) -- the padding below tells PhotoSwipe to keep images out
// of that strip so the caption never overlaps the image itself.
const CAPTION_HEIGHT = 70;

const lightbox = new PhotoSwipeLightbox({
  gallery: ".artworkGallery",
  children: "a.artworkLink",
  pswpModule: () => import("/js/photoswipe/photoswipe.esm.min.js"),
  paddingFn: () => ({ top: 16, bottom: CAPTION_HEIGHT, left: 16, right: 16 }),
});

// Caption reads data-pswp-caption off the clicked <a> -- see PhotoSwipe's
// own "Adding caption" docs for this pattern. No separate plugin needed.
// pointer-events is set in CSS so the caption bar can never intercept a
// click meant for the image underneath it.
lightbox.on("uiRegister", () => {
  lightbox.pswp.ui.registerElement({
    name: "caption",
    className: "pswp__custom-caption",
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
