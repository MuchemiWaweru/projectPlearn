document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".add-goal-form");
    const submitButton = form.querySelector("button[type='submit']");

    // Prevent multiple submissions
    form.addEventListener("submit", function (event) {
        submitButton.disabled = true; // Disable the button
        submitButton.textContent = "Adding..."; // Update button text
    });

    // Add focus effect to input fields
    const inputs = form.querySelectorAll("input, textarea, select");
    inputs.forEach((input) => {
        input.addEventListener("focus", () => {
            input.style.borderColor = "#007bff"; // Highlight border on focus
        });
        input.addEventListener("blur", () => {
            input.style.borderColor = "#ddd"; // Reset border on blur
        });
    });
});