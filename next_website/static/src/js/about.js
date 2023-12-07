/**
 * infinite scroll list for the  section campaign
 */
const scrollers = document.querySelectorAll(".scroller");

if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  addAnimation();
}

function addAnimation() {
  scrollers.forEach((scroller) => {
    scroller.setAttribute("data-animated", true);

    const scrollerInner = scroller.querySelector(".scroller-inner");
    const scrollerContent = Array.from(scrollerInner.children);

    scrollerContent.forEach((item) => {
      const duplicateItem = item.cloneNode(true);
      duplicateItem.setAttribute("aria-hidden", true);

      scrollerInner.appendChild(duplicateItem);
    });

    scrollerContent.forEach((item) => {
      const duplicateItem = item.cloneNode(true);
      duplicateItem.setAttribute("aria-hidden", true);

      scrollerInner.appendChild(duplicateItem);
    });
  });
}
