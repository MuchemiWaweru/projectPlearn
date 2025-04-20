from django import template

register = template.Library()


@register.filter
def priority_color(priority):
    if priority == 'High':
        return '#ff4d4d'  # Red
    elif priority == 'Medium':
        return '#ffa500'  # Orange
    elif priority == 'Low':
        return '#4caf50'  # Green
    return '#d3d3d3'  # Default gray