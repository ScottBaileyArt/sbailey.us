import PhotoSwipeLightbox from "/js/photoswipe/photoswipe-lightbox.esm.min.js";

// CAPTION_HEIGHT must match the reserved space in the .pswp__custom-caption
// CSS rule (sb.css). EDGE_GAP is the breathing room between the image and
// the screen edge/caption top -- same value on both, so the image sits with
// an equal gap above it and above the caption.
const CAPTION_HEIGHT = 104;
const EDGE_GAP = 16;

const lightbox = new PhotoSwipeLightbox({
  gallery: ".artworkGallery",
  children: "a.artworkLink",
  pswpModule: () => import("/js/photoswipe/photoswipe.esm.min.js"),
  paddingFn: () => ({
    top: EDGE_GAP,
    bottom: CAPTION_HEIGHT + EDGE_GAP,
    left: EDGE_GAP,
    right: EDGE_GAP,
  }),
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
