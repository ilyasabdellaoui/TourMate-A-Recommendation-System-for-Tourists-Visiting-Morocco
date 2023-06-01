const doc = document;
const menuOpen = doc.querySelector(".menu");
const menuClose = doc.querySelector(".close");
const overlay = doc.querySelector(".overlay");

menuOpen.addEventListener("click", () => {
  overlay.classList.add("overlay--active");
});

menuClose.addEventListener("click", () => {
  overlay.classList.remove("overlay--active");
});

// Open google map of hotel in new tab
function openMap(name, address) {
  var mapSearch = name + '+' + address.replaceAll(' ', '+');
  var mapLink = 'https://www.google.com/maps/search/' + mapSearch;
  window.open(mapLink, '_blank');
}