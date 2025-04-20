function delete_goal(goal_id) {
    console.log('Sending DELETE request for goal ID:', goal_id);

    // Show confirmation alert
    if (!confirm('Are you sure you want to delete this goal? This action cannot be undone.')) {
        return; // Exit the function if the user cancels
    }

    fetch(`/goals/${goal_id}/delete/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.status === 204) {
            console.log('Goal deleted successfully');
            // Remove the goal from the UI
            document.querySelector(`.goal-item[data-goal-id="${goal_id}"]`).remove();
        } else {
            return response.json().then(data => {
                throw new Error(data.error || 'Failed to delete');
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}