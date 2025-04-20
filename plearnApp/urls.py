from django.urls import path
from . import views
from .views import TaskDeleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('addtask/', views.addtask, name='addtask'),
    path('sign_up/', views.sign_up, name= 'sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('task_list/', views.task_list, name='task_list'),
    path('api/tasks/<int:task_id>/delete/', views.TaskDeleteView, name='task-delete'),
    path('addcategory/', views.add_category, name='add_category'),
    path('update_notifications/', views.update_notifications, name='update_notifications'),
    path('goals/', views.goal_list, name='goal_list'),
    path('goals/add/', views.add_goal, name='add_goal'),
    path('goals/<int:goal_id>/', views.goal_detail, name='goal_detail'),
    path('goals/<int:goal_id>/add_milestone/', views.add_milestone, name='add_milestone'),
    path('milestones/<int:milestone_id>/toggle_completion/', views.toggle_completion, name='toggle_completion'),
    path('goals/<int:goal_id>/delete/', views.delete_goal, name='delete_goal'),
    path('tasks/update_completion/<int:task_id>/', views.update_completion, name='update_completion'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='PlearnApp/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='PlearnApp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='PlearnApp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='PlearnApp/password_reset_complete.html'), name='password_reset_complete'),

    ]
