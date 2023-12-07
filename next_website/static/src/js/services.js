/**
 * Carousel for header home page
 */

// Variable global
let index = 0; // Slide index
let timer, slides, elements, slideWidth, speed;

window.onload = () => {
  const carousel = document.querySelector(".carousel-serv");
  elements = document.querySelector(".slides-serv");

  // Duplicate fisrt element of the carousel and add to the end of slides list
  let firstSlide = elements.firstElementChild.cloneNode(true);
  elements.appendChild(firstSlide);

  slides = Array.from(elements.children);

  // Arrow direction
  let next = document.querySelector(".next-slide-serv");
  let preview = document.querySelector(".prev-slide-serv");

  // Get size on current slide
  slideWidth = carousel.getBoundingClientRect().width;

  // Active function on event click
  next.addEventListener("click", slideNext);
  preview.addEventListener("click", slidePrev);

  speed = carousel.dataset.speed;
  // Auto-play of slide
  timer = setInterval(slideNext, speed);

  // Stop play with mouse moves
  carousel.addEventListener("mouseover", stopTimer);
  carousel.addEventListener("mouseout", startTimer);
};

/**
 * Function for next slide
 */
function slideNext() {
  index++;
  let translateSize = -slideWidth * index;

  elements.style.transition = "1s linear";
  elements.style.transform = `translateX(${translateSize}px)`;

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
 * Function for previous slide
 */
function slidePrev() {
  index--;

  if (index < 0) {
    index = slides.length - 1;
    let translateSize = -slideWidth * index;

    elements.style.transition = "unset";
    elements.style.transform = `translateX(${translateSize}px)`;
    setTimeout(slidePrev, 1);
  } else {
    let translateSize = -slideWidth * index;
    elements.style.transition = "1s linear";
    elements.style.transform = `translateX(${translateSize}px)`;
  }
}

function stopTimer() {
  clearInterval(timer);
}

function startTimer() {
  timer = setInterval(slideNext, speed);
}
