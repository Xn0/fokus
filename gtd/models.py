from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

__all__ = ['RepTask', 'Task', 'RepTaskStatus']

RepTaskStatus = models.TextChoices("RepTaskStatus", "RUNNING STOPPED DELETED")


class RepTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    last_created_date = models.DateTimeField('last task created', null=True, blank=True)
    status = models.CharField(max_length=10, choices=RepTaskStatus, default=RepTaskStatus.STOPPED)
    start_date = models.DateTimeField('start date', null=True, blank=True)
    rep_interval = models.IntegerField('repeat every N days', null=True, blank=True)
    rep_n_a_week = models.IntegerField('repeat every N times a week', null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(rep_n_a_week__lte=7), name="rep_n_a_week_lte_7"),
        ]

    def __str__(self):
        return f'{self.user.username} | {self.text}'

    def get_absolute_url(self):
        return reverse('gtd:rep-task', kwargs={'pk': self.pk})


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    show_count = models.IntegerField(default=0)
    done = models.BooleanField('task done', default=False)
    update_date = models.DateTimeField('updated date', default=datetime.now)
    rep_task = models.ForeignKey(
        RepTask,
        on_delete=models.CASCADE,
        unique_for_date='updated_date',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["update_date"]
        indexes = [
            models.Index(fields=['user', 'done']),
        ]
        index_together = ['user', 'done', 'update_date']

    def __str__(self):
        return f'{self.user.username} | {self.text} | repeatable: {bool(self.rep_task)}'
