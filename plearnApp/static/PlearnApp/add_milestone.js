document.addEventListener("DOMContentLoaded", function () {
    // Initialize the calendar widget
    const dueDateField = document.querySelector("#id_due_date");
    dueDateField.addEventListener("focus", function () {
        this.type = "datetime-local"; // Show the calendar widget
    });

    dueDateField.addEventListener("blur", function () {
        this.type = "text"; // Hide the calendar widget when the mouse leaves
    });

    // Handle the status radio button
    const statusRadios = document.querySelectorAll("input[name='status']");
    statusRadios.forEach((radio) => {
        radio.addEventListener("change", function () {
            if (this.checked) {
                alert(`Milestone marked as: ${this.value}`);
            }
        });
    });
});