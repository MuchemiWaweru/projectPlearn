document.addEventListener('DOMContentLoaded', function () {
    const token = document.getElementById('csrf-token').value;
    const taskList = document.getElementById('task-list');
    if (!taskList) {
        console.error('The task-list element is not found in the DOM.');
        return;
    }

    // Expand/Collapse task container on click
    document.querySelectorAll('.task-container').forEach(container => {
        container.addEventListener('click', function (e) {
            if (e.target.closest('.btn-edit') || e.target.closest('.delete-btn')) {
                return; // Don't toggle on Edit/Delete
            }

            const expandedView = this.querySelector('.task-expanded');
            if (!expandedView) {
                console.error('No expanded view found.');
                return;
            }

            const isHidden = expandedView.style.display === 'none' || expandedView.style.display === '';
            expandedView.style.display = isHidden ? 'block' : 'none';
        });
    });

    // Toggle dropdown visibility
    document.querySelectorAll('.completion-circle').forEach(circle => {
        circle.addEventListener('click', function () {
            const dropdown = circle.closest('.completion-wrapper').querySelector('.completion-dropdown');
            if (dropdown) {
                dropdown.style.display = (dropdown.style.display === 'none' || dropdown.style.display === '') ? 'block' : 'none';
            } else {
                console.error('Dropdown element not found for the clicked circle.');
            }
        });
    });

    // Task completion update
    document.querySelectorAll('.completion-option').forEach(option => {
        option.addEventListener('click', function () {
            const value = this.dataset.value;
            const wrapper = this.closest('.task-container');
            const taskId = wrapper.dataset.taskId;
            const circle = wrapper.querySelector('.completion-circle');

            fetch(`/tasks/update_completion/${taskId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': token,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ completion: value })
            })
            .then(response => response.json())
            .then(data => {
                circle.textContent = data.completion;
                wrapper.querySelector('.completion-dropdown').style.display = 'none';
            })
            .catch(error => console.error("Error:", error));
        });
    });

    // Handle delete button click with confirmation
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-btn')) {
            const task_id = e.target.dataset.taskId;
            if (task_id) {
                if (confirm('Are you sure you want to delete this task? This action cannot be undone.')) {
                    fetch(`/api/tasks/${task_id}/delete/`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    })
                    .then(response => {
                        if (response.ok) {
                            document.querySelector(`.task-container[data-task-id="${task_id}"]`).remove();
                        } else {
                            console.error('Delete failed:', response.status);
                        }
                    })
                    .catch(error => console.error('Error:', error));
                }
            } else {
                console.error('Task ID is missing or undefined');
            }
        }
    });

    
        
});