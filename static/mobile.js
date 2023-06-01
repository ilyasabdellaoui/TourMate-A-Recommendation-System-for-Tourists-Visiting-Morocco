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
// function removeApostrophes(value) {
//   value = value.replace(/['"‘’“”]/g, '');
//   return value.replace(/'/g, '');
// }

function openMap(name, city) {
  var mapSearch = name + '+' + city.replaceAll(' ', '+');
  var mapLink = 'https://www.google.com/maps/search/?api=1&query=' + mapSearch;
  window.open(mapLink, '_blank');
}



// Show Amnities Checkbox
function toggleInput(inputId) {
  var inputField = document.getElementById(inputId);
  var button = inputField.previousElementSibling;
  var label = button.previousElementSibling;

  if (inputField.style.display === "none") {
    inputField.style.display = "inline-block";
    button.textContent = "No";
    if (inputId === "room-types-input") {
      label.textContent = "Room Types preferences: Changed your mind? Click \"NO\".";
    } else if (inputId === "room-features-input") {
      label.textContent = "Room Features preferences: Changed your mind? Click \"NO\".";
    } else if (inputId === "property-amenities-input") {
      label.textContent = "Property Amenities preferences: Changed your mind? Click \"NO\".";
    }
  } else {
    inputField.style.display = "none";
    button.textContent = "Yes";
    if (inputId === "room-types-input") {
      label.textContent = "Do you have specific Room Types preferences? Click \"Yes\" to specify.";
    } else if (inputId === "room-features-input") {
      label.textContent = "Do you have specific Room Features preferences? Click \"Yes\" to specify.";
    } else if (inputId === "property-amenities-input") {
      label.textContent = "Do you have specific Property Amenities preferences? Click \"Yes\" to specify.";
    }
  }
}