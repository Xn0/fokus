import datetime
import json
import logging

from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseRedirect,
    HttpResponseNotAllowed
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http.request import QueryDict
from django.views.generic import ListView, edit, DetailView
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.db import transaction
from django.db.models import F

from .models import *
from .forms import TaskForm, RepTaskForm


@method_decorator(login_required, name='dispatch')
class TaskListView(ListView):
    model = Task
    context_object_name = "task_list"

    def get_queryset(self):
        return (Task.objects.filter(user=self.request.user, deleted=False)
                .exclude(done=True, update_date__lt=datetime.date.today()))

    def get(self, *args, **kwargs):
        rep_tasks = RepTask.objects.filter(user=self.request.user)
        for r in rep_tasks:
            r.check_and_create_task()

        return super().get(*args, **kwargs)

    def patch(self, *arg, **kwarg):
        return self.get(*arg, **kwarg)

    def delete(self, *arg, **kwarg):
        return self.get(*arg, **kwarg)


@method_decorator(login_required, name='dispatch')
class TaskView(DetailView):
    model = Task

    def get(self, request, *arg, **kwarg):
        """
        Return form for editing task text
        TODO make sepatare edit view
        """
        if not request.headers.get('HX-Request'):
            # if not from HTMX
            return HttpResponseNotAllowed(permitted_methods=[])

        task = get_object_or_404(self.model, pk=kwarg.get('pk'))
        return render(request, 'gtd/forms/task_edit_snippet.html', {'task': task})

    @transaction.atomic
    def patch(self, request, pk, *arg, **kwarg):
        body = QueryDict(request.body)
        query = {}
        try:
            for k, v in body.items():
                match k:
                    case 'done':
                        query['done'] = True if v == 'True' else False
                    case 'text':
                        query['text'] = v
                        query['show_count'] = 0
                    case _:
                        pass
        except Exception as e:
            logging.warning(f'[Task:PATCH]: {pk=} | {request.body=} | exception: {e}')
            return JsonResponse({'status': 'Fail'}, status=500)

        task = get_object_or_404(self.model, pk=pk, user=request.user, deleted=False)
        task.update_task(query)
        return redirect(reverse('gtd:tasks'))

    def delete(self, request, pk):
        task = get_object_or_404(self.model, pk=pk, user=request.user, deleted=False)
        task.delete_task()
        return HttpResponseRedirect(reverse('gtd:tasks'))


@method_decorator(login_required, name='dispatch')
class NewTaskView(edit.CreateView):
    template_name = 'gtd/forms/task_create_snippet.html'
    form_class = TaskForm
    http_method_names = ['get', 'post']

    def get_success_url(self):
        return reverse('gtd:tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class RepTasksView(ListView):
    model = RepTask
    context_object_name = "rep_task_list"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).exclude(deleted=True)


@method_decorator(login_required, name='dispatch')
class RepTaskCreateView(edit.CreateView):
    form_class = RepTaskForm
    template_name = 'gtd/forms/rep_task_form.html'

    def get_success_url(self):
        return reverse('gtd:rep-tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class RepTaskEditView(edit.UpdateView):
    model = RepTask
    form_class = RepTaskForm
    context_object_name = 'task'
    template_name = 'gtd/forms/rep_task_form.html'

    def get_success_url(self):
        return reverse('gtd:rep-tasks')

    def form_valid(self, form):
        return super().form_valid(form)
