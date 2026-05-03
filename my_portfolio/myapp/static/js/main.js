document.addEventListener("DOMContentLoaded", () => {
    console.log("JS Loaded");

    const form = document.querySelector("#contact-form");

    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault();
            alert("Form working");
        });
    }
});