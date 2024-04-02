from django import forms

from .models import Task, RepTask


class TaskForm(forms.Form):

    class Meta:
        model = Task
        fields = ['text']


class RepTaskForm(forms.Form):

    class Meta:
        model = Task
        fields = ['text', 'start_date', 'rep_interval', 'rep_n_a_week']
