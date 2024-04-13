from django.urls import path

from . import views

app_name = "gtd"

urlpatterns = [
    path("", views.TaskListView.as_view(), name='tasks'),
    path("rep-tasks", views.RepTasksView.as_view(), name='rep-tasks'),
    path("new-task", views.NewTaskView.as_view(), name='new-task'),
    path("new-rep-task", views.RepTaskCreateView.as_view(), name='new-rep-task'),
    path("<int:pk>", views.TaskView.as_view(), name='task'),
    path("rep-task/<int:pk>", views.RepTaskEditView.as_view(), name='rep-task'),
]
