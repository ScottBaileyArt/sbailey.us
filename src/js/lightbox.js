import PhotoSwipeLightbox from "/js/photoswipe/photoswipe-lightbox.esm.min.js";

// CAPTION_HEIGHT must match the reserved space in the .pswp__custom-caption
// CSS rule (sb.css). EDGE_GAP is the breathing room between the image and
// the screen edge/caption top -- same value on both, so the image sits with
// an equal gap above it and above the caption.
const CAPTION_HEIGHT = 104;
const EDGE_GAP = 16;

// Pinch-zooming the page (trackpad or touchscreen) doesn't change the page's
// layout; the browser just magnifies a smaller window onto it, called the
// "visual viewport". PhotoSwipe sizes itself to the whole un-zoomed page, so
// a lightbox opened while zoomed is partly off screen, with its buttons
// magnified along with everything else. (Chrome on Android does something
// similar even at normal zoom, on any page wider than the screen.) The code
// below fits the lightbox's contents to the visual viewport instead, and
// (with the .pswp--page-zoomed rules in sb.css) draws its controls at normal
// size. On a page that fits the screen, at normal zoom, the visual viewport
// is the window, so none of this changes anything.
//
// What gets fitted is PhotoSwipe's inner wrapper (.pswp__scroll-wrap, which
// holds the image, buttons and caption), not its outer element (.pswp). The
// outer element stays window-sized, with PhotoSwipe's dark background filling
// it, because that is what lets iPhone Safari fill the strips behind its
// status bar and tab bar with the background colour. Tested on-device: if
// that element is sized to the zoomed screen instead, Safari leaves those
// strips showing the page whenever the lightbox is opened while zoomed in.
const vv = window.visualViewport;
const pageZoom = () => (vv ? vv.scale : 1);
const isPageZoomed = () => Math.abs(pageZoom() - 1) > 0.01;

function fitToVisualViewport(pswp) {
  const { element: root, scrollWrap } = pswp;
  if (!root || !scrollWrap || !vv) return;
  root.classList.toggle("pswp--page-zoomed", isPageZoomed());
  root.style.setProperty("--page-zoom", pageZoom());
  scrollWrap.style.left = `${vv.offsetLeft}px`;
  scrollWrap.style.top = `${vv.offsetTop}px`;
  scrollWrap.style.width = `${vv.width}px`;
  scrollWrap.style.height = `${vv.height}px`;
}

const lightbox = new PhotoSwipeLightbox({
  gallery: ".artworkGallery",
  children: "a.artworkLink",
  pswpModule: () => import("/js/photoswipe/photoswipe.esm.min.js"),
  // How dark the background is; PhotoSwipe's default is 0.8. sb.css has a
  // copy of this value (.pswp--opening).
  bgOpacity: 0.9,
  // Called whenever PhotoSwipe (re)measures the screen, which makes it the
  // one place to also reposition the lightbox. Returning nothing (old
  // browsers without visualViewport) means "use PhotoSwipe's own measurement".
  getViewportSizeFn: (options, pswp) => {
    fitToVisualViewport(pswp);
    return vv ? { x: vv.width, y: vv.height } : undefined;
  },
  // Divided by the zoom so the gaps stay the same size on screen.
  paddingFn: () => {
    const zoom = pageZoom();
    return {
      top: EDGE_GAP / zoom,
      bottom: (CAPTION_HEIGHT + EDGE_GAP) / zoom,
      left: EDGE_GAP / zoom,
      right: EDGE_GAP / zoom,
    };
  },
});

// PhotoSwipe turns touch/mouse positions into lightbox positions by
// subtracting where the lightbox sits on the page. It assumes the lightbox
// is at the window's top-left corner, which isn't true when the page is
// zoomed (or scrolled sideways), so point it at the visual viewport instead.
// PhotoSwipe resets this value on open, resize and scroll; re-apply each time.
function syncPointerOffset() {
  if (!vv) return;
  lightbox.pswp.offset.x = vv.pageLeft;
  lightbox.pswp.offset.y = vv.pageTop;
}
lightbox.on("initialLayout", syncPointerOffset);
lightbox.on("updateScrollOffset", syncPointerOffset);

// The open/close animation grows the image out of its thumbnail, measured
// relative to the window; shift that to be relative to the fitted wrapper.
lightbox.addFilter("thumbBounds", (bounds) => {
  if (bounds && vv) {
    bounds.x -= vv.offsetLeft;
    bounds.y -= vv.offsetTop;
  }
  return bounds;
});

// Trackpad pinch inside the lightbox: PhotoSwipe's own handler centres the
// zoom on the pointer's position in the window, which is off by the visual
// viewport's offset when the page is zoomed. Same maths as PhotoSwipe's,
// with the position corrected.
lightbox.on("wheel", (e) => {
  const wheel = e.originalEvent;
  const slide = lightbox.pswp.currSlide;
  if (!isPageZoomed() || !wheel.ctrlKey || !slide?.isZoomable()) return;
  e.preventDefault();
  const step = wheel.deltaMode === 1 ? 0.05 : wheel.deltaMode ? 1 : 0.002;
  slide.zoomTo(slide.currZoomLevel * 2 ** (-wheel.deltaY * step), {
    x: wheel.pageX - vv.pageLeft,
    y: wheel.pageY - vv.pageTop,
  });
});

// If the visual viewport moves or resizes while the lightbox is open, refit.
// Listeners added through pswp.events are removed automatically on close.
lightbox.on("bindEvents", () => {
  if (!vv) return;
  const refit = () => lightbox.pswp.updateSize(true);
  lightbox.pswp.events.add(vv, "resize", refit);
  lightbox.pswp.events.add(vv, "scroll", refit);
});

// iPhone Safari picks the colour for the strips behind its status bar and
// tab bar when the lightbox first appears. PhotoSwipe fades its background
// in from almost clear, so Safari would see no colour and leave the strips
// showing the page (tested on-device). While the opening animation runs, the
// .pswp--opening rule in sb.css holds the background at full darkness
// instead; the image still zooms out of its thumbnail as normal. By the time
// the class comes off, PhotoSwipe's own fade has reached the same value, so
// nothing visibly changes. Closing and drag-to-dismiss fades are untouched.
lightbox.on("firstUpdate", () => {
  lightbox.pswp.element.classList.add("pswp--opening");
});
lightbox.on("openingAnimationEnd", () => {
  lightbox.pswp.element.classList.remove("pswp--opening");
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
    // Inside the wrapper that fitToVisualViewport sizes, with the buttons.
    appendTo: "wrapper",
    onInit: (el) => {
      lightbox.pswp.on("change", () => {
        const link = lightbox.pswp.currSlide?.data?.element;
        el.innerHTML = link ? link.dataset.pswpCaption || "" : "";
      });
    },
  });
});

lightbox.init();
