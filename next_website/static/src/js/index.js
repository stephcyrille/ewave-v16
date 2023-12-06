
// Windows scroll viewer
window.onscroll = function () {
  scrollFunction();
};

/**
 * scrollFunction - the function that is called to manage the size
 * of the navbar during scrolling.
 */
function scrollFunction() {
  let navbar = document.getElementById("navbar");
  let logo = document.getElementById("logo");
  let width = navbar.offsetWidth;

  if (document.body.scrollTop > 80 || document.documentElement.scrollTop > 80) {
    navbar.style.position = "fixed";
    navbar.classList.add("shadow-md");
    if (width >= 1024) {
      logo.style.height = "44px";
    } else if (width >= 768) {
      logo.style.height = "40px";
    } else {
      logo.style.height = "36px";
    }
  } else {
    navbar.style.position = "sticky";
    navbar.classList.remove("shadow-md");
    if (width >= 1024) {
      logo.style.height = "54px";
    } else if (width >= 768) {
      logo.style.height = "48px";
    } else {
      logo.style.height = "40px";
    }
  }
}

/**
 * dropDisplay - the function that is called when the user clicks
 * on the profile button
 */
function dropDisplay(value) {
  let content = document.getElementById(value);
  content.classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onmouseover = function (event) {
  let dropdowns = document.getElementsByClassName("dropdown-button");
  let navbar = document.getElementById("navbar");
  let i;

  for (i = 0; i < dropdowns.length; i++) {
    if (!navbar.contains(event.target)) {
      let dropdowns = document.getElementsByClassName("dropdown-content");
      let openDropdown = dropdowns[i];
      if (openDropdown.classList.contains("show")) {
        openDropdown.classList.remove("show");
      }
    }
  }
};

/**
 * closeMenu: the function that is called when the user clicks
 * on the close menu button
 */
function closeMenu() {
  const navbar = document.querySelector("#mobile-navbar");
  let navbarWidth = navbar.getBoundingClientRect().width;

  navbar.style.transition = "500ms linear";
  navbar.style.transform = `translateX(${navbarWidth}px)`;
}

/**
 * openMenu: the function that is called when the user clicks
 * on the menu button
 */
function openMenu() {
  const navbar = document.querySelector("#mobile-navbar");

  navbar.style.transition = "500ms linear";
  navbar.style.transform = `translateX(0)`;
}
