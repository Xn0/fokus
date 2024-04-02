from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("", views.TasksView.as_view(), name='tasks'),
    path("rep-tasks", views.RepTasksView.as_view(), name='rep-task'),
    path("<int:pk>", views.TaskView.as_view(), name='task'),
    path("rep-tasks/<int:pk>", views.RepTaskView.as_view(), name='rep-task'),
]