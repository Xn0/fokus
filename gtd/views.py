import datetime
import json
import logging

from django.http import HttpResponse, JsonResponse
from django.http.request import QueryDict
from django.views.generic import ListView, edit, DetailView
from django.shortcuts import render, reverse, get_object_or_404
from django.db import transaction
from django.db.models import F

from .models import *
from .forms import TaskForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def test_view(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class TasksView(ListView):
    model = Task
    context_object_name = "task_list"

    # def get_queryset(self):
    #     return (Task.objects.filter(user=self.request.user)
    #             .exclude(done=True, update_date__lt=datetime.date.today()))

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskView(DetailView):
    model = Task

    def get(self, request, *arg, **kwarg):
        return HttpResponse(f"This is single task number {self.kwargs['pk']}")

    @transaction.atomic
    def patch(self,request, pk, *arg, **kwarg):
        body = QueryDict(request.body)
        query = {}
        try:
            for k, v in body.items():
                match k:
                    case 'done':
                        query['done'] = False if v[0] == 'True' else True
                    case 'text':
                        query['text'] = v[0]
                    case _:
                        pass
        except (IndexError, TypeError) as e:
            logging.warning(f'[Task:PATCH]: {pk=} | {request.body=} | exception: {e}')
            return JsonResponse({'status': 'Fail'}, status=500)

        task = get_object_or_404(Task, pk=pk)
        # update missed tasks
        (Task.objects.filter(done=False, update_date__lte=task.update_date)
         .update(update_date=datetime.datetime.now(), show_count=F("show_count") + 1))
        task.done = True
        task.save()
        return JsonResponse({'status': 'Success'}, status=204)

    # def post(self, request, pk):
    #     print('sfhfsh')
    #     return HttpResponse(f"This is single task number {self.kwargs['pk']}")


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