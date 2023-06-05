// modal -------------------------

const isOpenClass = "modal-is-open";
const openingClass = "modal-is-opening";
const closingClass = "modal-is-closing";
const animationDuration = 400; // ms
var visibleModal = null;

function toggleModal(event) {
    event.preventDefault();
    const modal = document.getElementById(event.currentTarget.getAttribute("data-target"))

    if (modal != "undenfined" && modal != null && isModalOpen(modal)) {
        closeModal(modal);
    } else {
        openModal(modal);
    }
}

function isModalOpen(modal) {
    return modal.hasAttribute("open") && modal.getAttribute("open") != "false" ? true : false;
}

function openModal(modal) {
    if (isScrollbarVisible()) {
        document.documentElement.style.setProperty("--scrollbar-width", `${getScrollbarWidth()}px`);
    }
    document.documentElement.classList.add(isOpenClass, openingClass);
    setTimeout(() => {
        visibleModal = modal;
        document.documentElement.classList.remove(openingClass);
    }, animationDuration);
    modal.setAttribute("open", true);
}

function closeModal(modal) {
    visibleModal = null;
    document.documentElement.classList.add(closingClass);
    setTimeout(() => {
        document.documentElement.classList.remove(closingClass, isOpenClass);
        document.documentElement.style.removeProperty("--scrollbar-width");
        modal.removeAttribute("open");
    }, animationDuration);
}

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && visibleModal != null) {
      closeModal(visibleModal);
    }
  });

function getScrollbarWidth() {
    // Creating invisible container
  const outer = document.createElement("div");
  outer.style.visibility = "hidden";
  outer.style.overflow = "scroll"; // forcing scrollbar to appear
  outer.style.msOverflowStyle = "scrollbar"; // needed for WinJS apps
  document.body.appendChild(outer);

  // Creating inner element and placing it in the container
  const inner = document.createElement("div");
  outer.appendChild(inner);

  // Calculating difference between container's full width and the child width
  const scrollbarWidth = outer.offsetWidth - inner.offsetWidth;

  // Removing temporary elements from the DOM
  outer.parentNode.removeChild(outer);

  return scrollbarWidth;
}

function isScrollbarVisible() {
    return document.body.scrollHeight > screen.height;
}

// -----------------------

// Sidenav ---------------

var isSidenavOpen = false;

function hideSidenav() {
    $(".shadower").css("display", "none");
    $(".sidenav").css("display", "none");
    document.documentElement.style.removeProperty("--scrollbar-width", `${getScrollbarWidth()}px`);
    isSidenavOpen = false;
}

function showSidenav() {
    $(".shadower").css("display", "block");
    $(".sidenav").css("display", "block");
    document.documentElement.style.setProperty("--scrollbar-width", `${getScrollbarWidth()}px`);
    isSidenavOpen = true;
}

$(".shadower").on("click", function(event) {
    event.preventDefault();
    hideSidenav();
});

$(".shadower").on("scroll", function(event) {
    event.preventDefault();
});

$("#sidenav-btn").on("click", function() {
    if (!isSidenavOpen) {
        showSidenav();
    } else {
        hideSidenav();
    }
});

// -------------