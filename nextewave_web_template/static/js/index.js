// Call the function addNavbar on load script
addNavbar();

/**
 * addNavbar - this function is called to add the section navbar on the current page
 */
function addNavbar() {
  let navbar = document.querySelector("nav");

  if (navbar.childElementCount == 0) {
    navbar.innerHTML = `
    <div id="navbar"
      class="sticky inset-0 z-30 flex h-max w-full max-w-full justify-center border-b rounded-none bg-white py-1.5 transition-all duration-200 ease-in-out">
      <div class="flex xl:gap-x-4 items-center w-full max-w-[90rem] px-8">
        <a href="./index.html" class="block cursor-pointer py-1.5 antialiased">
          <img id="logo" src="./assets/img/logo.png" alt="logo_nextewave"
            class="transition-all duration-200 ease-in-out h-9 md:h-14 pr-6" />
        </a>

        <ul
          class="ml-auto mr-6 hidden laptop:flex items-center gap-4 xl:gap-6 text-gray-600 text-sm xl:text-base font-dosis font-normal leading-none">
          <li class="block p-1 antialiased hover:font-normal hover:text-blue-green transition ease-in-out duration-200">
            <div class="dropdown">
              <a href="./services.html" onmouseover="dropDisplay('dropdown-service')"
                class="dropdown-button cursor-pointer">
                Services
                <i class="ri-arrow-down-s-fill"></i>
              </a>

              <div id="dropdown-service"
                class="dropdown-content min-w-[20rem] border text-neutral-600 border-neutral-300">
                <a href="./services/sourcing.html">Sourcing</a>
                <hr />
                <a href="./services/pack-&-ship.html">Pack & Ship</a>
                <hr />
                <a href="./campaign.html">Campaign</a>
              </div>
            </div>
          </li>
          <li class="block p-1 antialiased hover:font-normal hover:text-blue-green transition ease-in-out duration-200">
            <a class="flex items-center" href="./sourcing-for-you.html">
              We Sourcing For You
            </a>
          </li>
          <li
            class="block p-1 antialiased hover:font-normal hover:text-blue-green transition-colors ease-in-out duration-200">
            <a class="flex items-center" href="./pack-&-ship-for-you.html"> We Pack & Ship For You </a>
          </li>
          <li class="block p-1 antialiased hover:font-normal hover:text-blue-green transition ease-in-out duration-200">
            <a class="flex items-center" href="./success-stories.html"> Success Stories </a>
          </li>
          <li class="block p-1 antialiased hover:font-normal hover:text-blue-green transition ease-in-out duration-200">
            <a class="flex items-center" href="./about-us.html"> About Us </a>
          </li>
        </ul>

        <div
          class="max-phone:ml-0 max-laptop:ml-auto font-dosis font-normal flex items-center gap-6 sm:gap-10 laptop:gap-6">
          <div class="dropdown xl:pr-3" id="user-log">
            <div onmouseover="dropDisplay('dropdown-user')"
              class="dropdown-button leading-none flex items-center text-neutral-500 cursor-pointer focus:text-blue-green hover:text-blue-green transition ease-in-out duration-200">
              <i class="ri-account-circle-line text-2xl leading-none"></i>
              <i class="ri-arrow-down-s-fill"></i>
            </div>

            <div id="dropdown-user" class="dropdown-content min-w-[10rem] border text-neutral-600 border-neutral-300">
              <a href="#"><i class="ri-user-settings-line pr-2"></i>My Account</a>
              <hr />
              <a href="#"><i class="ri-logout-circle-r-line pr-2"></i>Logout</a>
            </div>
          </div>

          <div onclick="openMenu()"
            class="laptop:hidden leading-none text-3xl text-neutral-500 cursor-pointer focus:text-blue-green hover:text-blue-green transition ease-in-out duration-200">
            <i class="ri-menu-fill"></i>
          </div>

          <a href="./contact-us.html" class="max-sm:hidden">
            <button
              class="truncate rounded-md bg-blue-green py-3 px-2.5 sm:px-4 font-normal leading-none text-white shadow-md transition-all ease-in-out duration-300 hover:scale-105 hover:bg-transparent hover:text-blue-green hover:border hover:border-blue-green lg:inline-block"
              type="button">
              <span>Contact Us</span>
            </button>
          </a>
        </div>
      </div>

    </div>

    <!-- Mobile navigation bar -->
    <div id="mobile-navbar" class="xl:hidden fixed inset-0 top-0 h-full w-full z-50 flex translate-x-full">
      <div
        class="h-full overflow-scroll w-4/5 sm:w-[40rem] relative flex flex-col items-center justify-between gap-14 py-14 pt-20 bg-white/80 backdrop-blur-md">
        <div onclick="closeMenu()"
          class="absolute cursor-pointer top-4 right-4 sm:top-6 leading-none text-2xl sm:text-3xl text-neutral-600 hover:text-neutral-800 transition ease-in-out duration-200">
          <i class="ri-close-fill"></i>
        </div>

        <a href="./index.html" class="order-last block cursor-pointer">
          <img id="logo" src="./assets/img/logo.png" alt="logo_nextewave" class="h-14" />
        </a>

        <ul
          class="flex flex-col w-full px-14 gap-6 font-light font-dosis text-neutral-600 transition duration-200 ease-in-out">
          <li class=" w-full">
            <a href="./services.html"
              class="block w-full border-b border-slate-300 pb-1 focus:text-blue-green hover:text-blue-green">Service
            </a>
            <!-- <i class="ri-arrow-down-s-fill"></i> -->
            <ul class="flex flex-col gap-4 pl-4 pt-3">
              <li class="focus:text-blue-green hover:text-blue-green">
                <i class="ri-arrow-right-line"></i> <a href="./services/sourcing.html">Sourcing</a>
              </li>
              <li class="focus:text-blue-green hover:text-blue-green">
                <i class="ri-arrow-right-line"></i> <a href="./services/pack-&-ship.html">Pack & Ship</a>
              </li>
              <li class="focus:text-blue-green hover:text-blue-green">
                <i class="ri-arrow-right-line"></i> <a href="./campaign.html">Campaign</a>
              </li>
            </ul>
          </li>
          <!-- <li class="hover:text-blue-green focus:text-blue-green">
                  <a href="#">Pricing</a>
                </li> -->
          <li class="block w-full border-b border-slate-300 pb-1 hover:text-blue-green focus:text-blue-green">
            <a href="./sourcing-for-you.html">We Sourcing For You</a>
          </li>
          <li class="block w-full border-b border-slate-300 pb-1 hover:text-blue-green focus:text-blue-green">
            <a href="./pack-&-ship-for-you.html">We Pack & Ship For You</a>
          </li>
          <li class="block w-full border-b border-slate-300 pb-1 hover:text-blue-green focus:text-blue-green">
            <a href="./success-stories.html">Success Stories</a>
          </li>
          <li class="block w-full border-b border-slate-300 pb-1 hover:text-blue-green focus:text-blue-green">
            <a href="./about-us.html">About Us</a>
          </li>
          <li class="block w-full border-b border-slate-300 pb-1 hover:text-blue-green focus:text-blue-green">
            <a href="./contact-us.html">Contact Us</a>
          </li>
        </ul>
      </div>

      <div onclick="closeMenu()" class="order-first h-full w-1/5 sm:w-full bg-black/50"></div>
    </div>  `;
  }
}
// Call the function addFooter on load script
addFooter();

/**
 * addFooter - this function is called to add the section footer on the current page
 */
function addFooter() {
  let footer = document.querySelector("footer");

  // If the page is located in a sub-directory (sub-service), do not add a footer, as the links will be erroneous.
  if (footer.childElementCount == 0) {
    footer.innerHTML = `
  <div class="w-full max-w-[90rem] p-8 pb-3 text-neutral-600 font-open-sans text-sm">
      <!-- Link for contact us -->
      <div class="flex flex-wrap justify-between gap-10">
        <div>
          <p
            class="font-dosis text-lg font-medium text-neutral-700 leading-none pb-2 ">
            NexteWave Sarl
          </p>
          <hr class="border-b-2 w-[3rem] mb-3  border-b-blue-green" />
          <div class="flex flex-col gap-2">
            <h3 class="">
              <i class="fa-solid fa-house pr-2"></i>Nouvelle route cité CICAM
            </h3>
            <h3 class="pl-5">P.B: Douala Cameroun</h3>
          </div>
        </div>

        <div>
          <p
            class="font-dosis text-lg font-medium text-neutral-700 leading-none pb-2">
            Call us
          </p>
          <hr class="border-b-2 w-[3rem] mb-3  border-b-blue-green" />
          <div class="flex flex-col gap-2">
            <a href="tel:+1650-555-0111" target="_blank"
              class="hover:text-blue-green transition ease-in-out duration-200"><i class="ri-phone-fill pr-2"></i>+1
              (650) 555-0111</a>
            <a href="https://wa.me/+1650-555-0111" target="_blank"
              class="hover:text-blue-green transition ease-in-out duration-200"><i class="ri-whatsapp-fill pr-2"></i>+1
              (650) 555-0111</a>
          </div>
        </div>

        <div>
          <p
            class="font-dosis text-lg font-medium text-neutral-700 leading-none pb-2">
            Write us
          </p>
          <hr class="border-b-2 w-[3rem] mb-3  border-b-blue-green" />
          <a href="mailto:hello@mycompany.com" target="_blank"
            class="hover:text-blue-green transition ease-in-out duration-200"><i class="fa-solid fa-envelope pr-2"></i>
            hello@mycompany.com</a>
        </div>

        <div>
          <p
            class="font-dosis text-lg font-medium text-neutral-700 leading-none pb-2 ">
            Follow us
          </p>
          <hr class="border-b-2 w-[3rem] mb-3  border-b-blue-green" />
          <div class="flex items-center leading-none gap-3 text-2xl">
            <a href="https://facebook.com" target="_blank" class="hover:text-blue-green transition"><i
                class="ri-facebook-box-fill"></i></a>
            <a href="https://linkedin.com" target="_blank" class="hover:text-blue-green transition"><i
                class="ri-linkedin-box-fill"></i></a>
            <a href="https://twitter.com" target="_blank" class="hover:text-blue-green transition"><i
                class="ri-twitter-x-fill"></i></a>
          </div>
        </div>
      </div>

      <hr class="my-6 border-slate-300" />

      <!-- Link into the website -->
      <div class="flex flex-row flex-wrap items-center justify-center gap-y-6 gap-x-12 text-center md:justify-between">
        <img src="./assets/img/logo.png" alt="logo-ct" class="h-12" />
        <ul class="flex flex-wrap items-center gap-y-2 gap-x-8">
          <li>
            <a href="./index.html"
              class="block font-open-sans text-sm font-normal leading-relaxed text-blue-gray-900 antialiased transition-colors hover:hover:text-blue-green focus:hover:text-blue-green">
              Home
            </a>
          </li>
          <li>
            <a href="./services.html"
              class="block font-open-sans text-sm font-normal leading-relaxed text-blue-gray-900 antialiased transition-colors hover:hover:text-blue-green focus:hover:text-blue-green">
              Services
            </a>
          </li>
          <li>
            <a href="./about-us.html"
              class="block font-open-sans text-sm font-normal leading-relaxed text-blue-gray-900 antialiased transition-colors hover:hover:text-blue-green focus:hover:text-blue-green">
              About Us
            </a>
          </li>
          <li>
            <a href="#"
              class="block font-open-sans text-sm font-normal leading-relaxed text-blue-gray-900 antialiased transition-colors hover:hover:text-blue-green focus:hover:text-blue-green">
              Terms of Services
            </a>
          </li>
          <li>
            <a href="#"
              class="block font-open-sans text-sm font-normal leading-relaxed text-blue-gray-900 antialiased transition-colors hover:hover:text-blue-green focus:hover:text-blue-green">
              Privacy Policy
            </a>
          </li>
        </ul>
      </div>
    </div>

    <!-- Copyrigth -->
    <div class="w-full bg-neutral-800 text-white py-2 mt-4">
      <p class="block text-center font-open-sans text-base font-normal leading-relaxed text-blue-gray-900 antialiased">
        Copyright 2023 NexteWave ©
      </p>
    </div>`;
  }
}

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
