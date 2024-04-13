from django import forms
from django.forms import widgets

from .models import Task, RepTask


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['text']


class RepTaskForm(forms.ModelForm):
    running = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "id": "running"})
    )

    class Meta:
        model = RepTask
        fields = ['text', 'start_date', 'rep_interval', 'rep_n_a_week', 'running']
        # TODO add validation rep_interval or rep_n_a_week
