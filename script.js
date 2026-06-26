// ===============================
// Library Management System
// script.js
// ===============================

// Welcome Message
console.log("Library Management System Loaded Successfully!");

// Delete Confirmation
function confirmDelete() {
    return confirm("Are you sure you want to delete this book?");
}

// Greeting Message
window.onload = function () {

    let hour = new Date().getHours();
    let greeting = "";

    if (hour < 12) {
        greeting = "Good Morning";
    } else if (hour < 17) {
        greeting = "Good Afternoon";
    } else {
        greeting = "Good Evening";
    }

    console.log(greeting);

    // Display greeting if an element exists
    let greetingElement = document.getElementById("greeting");

    if (greetingElement) {
        greetingElement.innerHTML = greeting + " 👋";
    }
};