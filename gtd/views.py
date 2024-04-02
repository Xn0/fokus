import datetime

from django.http import HttpResponse
from django.views.generic import ListView, edit, DetailView
from django.shortcuts import render, reverse

from .models import *
from .forms import TaskForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def test_view(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class TasksView(ListView):
    model = Task
    context_object_name = "task_list"

    def get_queryset(self):
        return (Task.objects.filter(user=self.request.user)
                .exclude(done=True, update_date__lt=datetime.date.today()))


class TaskView(DetailView):
    # TODO

    def get(self, request, *arg, **kwarg):
        return HttpResponse(f"This is single task number {self.kwargs['pk']}")

    def put(self, request, *arg, **kwarg):
        return HttpResponse(f"This is single task number {self.kwargs['pk']}")


class RepTasksView(ListView):
    model = RepTask
    context_object_name = "rep_task_list"

    def get_queryset(self):
        return RepTask.objects.filter(user=self.request.user).exclude(status=RepTaskStatus.DELETED)


class RepTaskView(DetailView):
    # TODO

    def get(self, request, *arg, **kwarg):
        return HttpResponse(f"This is rep task number {self.kwargs['pk']}")


class TaskFormView(edit.FormView):
    template_name = ""
    form_class = TaskForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)