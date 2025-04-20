document.addEventListener("DOMContentLoaded", function () {
    const milestoneItems = document.querySelectorAll(".milestone-item");

    // Function to restore milestone statuses from localStorage
    function restoreMilestoneStatus() {
        milestoneItems.forEach((item) => {
            const milestoneId = item.dataset.milestoneId; // Using data-milestone-id
            const checkbox = item.querySelector('input[type="checkbox"]');
            const savedStatus = localStorage.getItem(`milestone-${milestoneId}`);
            
            if (savedStatus !== null) {
                checkbox.checked = savedStatus === "true";
                const statusLabel = item.querySelector(`label[for="status-${milestoneId}"]`);
                statusLabel.textContent = checkbox.checked ? "Complete" : "Incomplete";
            }
        });
    }

    // Restore saved statuses when the page loads
    restoreMilestoneStatus();

    milestoneItems.forEach((item) => {
        // Highlight milestone on hover
        item.addEventListener("mouseover", () => {
            item.style.backgroundColor = "#e8e6e1"; // Light greige
        });

        item.addEventListener("mouseout", () => {
            item.style.backgroundColor = "#f5f5f3"; // Default greige
        });

        // Add click animation
        item.addEventListener("click", () => {
            item.style.transform = "scale(0.98)";
            setTimeout(() => {
                item.style.transform = "scale(1)";
            }, 100);
        });
    });

    // Function to toggle completion status
    window.toggleCompletion = function (milestoneId) {
        const checkbox = document.querySelector(`#status-${milestoneId}`);
        const statusLabel = document.querySelector(`label[for="status-${milestoneId}"]`);

        if (!checkbox || !statusLabel) {
            console.error(`Elements not found for milestone ID: ${milestoneId}`);
            return;
        }

        // Fetch the new status directly from the checkbox state
        const newStatus = checkbox.checked;

        // Update UI instantly
        statusLabel.textContent = newStatus ? "Complete" : "Incomplete";

        // Save the new status to localStorage
        localStorage.setItem(`milestone-${milestoneId}`, newStatus);

        // Function to get CSRF token dynamically from cookies
        function getCsrfToken() {
            const cookieValue = document.cookie
                .split("; ")
                .find(row => row.startsWith("csrftoken="));
            return cookieValue ? cookieValue.split("=")[1] : null;
        }

        const csrfToken = getCsrfToken();
        if (!csrfToken) {
            alert("CSRF token not found. Ensure cookies are enabled.");
            return;
        }

        // Send AJAX request to update the completion status on the server
        fetch(`/milestones/${milestoneId}/toggle_completion/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ completed: newStatus }),
        })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    throw new Error(data.error || "Failed to update milestone.");
                }
            })
            .catch(error => {
                console.error("Error updating milestone status:", error);
                alert("Failed to update milestone status.");
                // Revert UI if error occurs
                checkbox.checked = !newStatus;
                statusLabel.textContent = !newStatus ? "Complete" : "Incomplete";
            });
    };
});
