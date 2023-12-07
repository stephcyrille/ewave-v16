/**
 * Carousel for header home page
 */

let index = 0; // Slide index
let timer, slides, elements, speed;
const carousel = document.querySelector(".carousel");

window.onload = () => {
  let firstSlide;

  if (carousel) {
    // Duplicate fisrt element of the carousel and add to the end of slides list
    elements = document.querySelector(".slides");
    firstSlide = elements.firstElementChild.cloneNode(true);
    elements.appendChild(firstSlide);

    slides = Array.from(elements.children);
    speed = carousel.dataset.speed;

    // Auto-play of slide
    activeDot();
    timer = setInterval(slideNext, speed);
  }
};

/**
 * activeDot - this funtion change the animation of active dot
 */
function activeDot() {
  let dotList = document.querySelectorAll(".slide-dot");

  for (let id = 0; id < dotList.length; id++) {
    if (id == index || id == index % dotList.length) {
      dotList[id].style.background = "#2362AC";
      dotList[id].style.width = "2rem";
    } else {
      dotList[id].style.background = "#a0a0a0";
      dotList[id].style.width = "1rem";
    }
  }
}

/**
 * slideNext - this function run to next slide
 */
function slideNext() {
  index++;
  let slideWidth = carousel.getBoundingClientRect().width;
  let translateSize = -slideWidth * index;

  elements.style.transition = "1s linear";
  elements.style.transform = `translateX(${translateSize}px)`;
  activeDot();

  // Reboot carousel after the end of animation
  setTimeout(() => {
    if (index >= slides.length - 1) {
      index = 0;

      elements.style.transition = "unset";
      elements.style.transform = "translateX(0)";
    }
  }, 1005);
}

/**
 * slidePrev - this function run to previous slide
 */
function slidePrev() {
  index--;
  let translateSize;
  let slideWidth = carousel.getBoundingClientRect().width;

  activeDot();
  if (index < 0) {
    index = slides.length - 1;
    translateSize = -slideWidth * index;

    elements.style.transition = "unset";
    elements.style.transform = `translateX(${translateSize}px)`;

    setTimeout(slidePrev, 1);
  } else {
    translateSize = -slideWidth * index;

    elements.style.transition = "1s linear";
    elements.style.transform = `translateX(${translateSize}px)`;
  }
}

/**
 * stopTimer - this function stop carousel
 */
function stopTimer() {
  clearInterval(timer);
}

/**
 * startTimer - this function restart carousel
 */
function startTimer() {
  timer = setInterval(slideNext, speed);
}

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
  });
}
