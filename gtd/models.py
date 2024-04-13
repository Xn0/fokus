import logging

from datetime import datetime, timedelta, date

from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.shortcuts import reverse

__all__ = ['RepTask', 'Task']


class RepTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    last_created_date = models.DateTimeField('last task created', null=True, blank=True)
    running = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    start_date = models.DateTimeField('start date', null=True, blank=True)
    rep_interval = models.IntegerField('repeat every N days', null=True, blank=True)
    rep_n_a_week = models.IntegerField('repeat N times a week', null=True, blank=True)

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

    #  TODO 10 minutes cache
    def check_and_create_task(self) -> None:
        if not self.running:
            return

        # if active task exist or if the last task was done today
        if self.task_set.filter(done=False) or self.task_set.filter(
                done=True,
                update_date__date=datetime.today()
        ):
            return

        # repeats a week case
        if self.rep_n_a_week:
            today = date.today()
            last_monday = today - timedelta(days=today.weekday())
            cnt = self.task_set.filter(update_date__gt=last_monday).count()
            if cnt < self.rep_n_a_week:
                self.task_set.create(text=self.text, user=self.user)

        # repeat by interval case
        elif self.start_date and self.rep_interval:
            now = datetime.now()
            last_task = self.task_set.order_by("-creation_date").first()
            if last_task:
                if now - last_task.creation_date > timedelta(days=self.rep_interval):
                    self.task_set.create(
                        creation_date=last_task.creation_date + timedelta(days=self.rep_interval),
                        text=self.text,
                        user=self.user
                    )
            else:
                self.task_set.create(
                    creation_date=self.start_date,
                    text=self.text,
                    user=self.user
                )
        else:
            logging.warning(f'[RepTask:check_and_create_task]: Error - no rep intervals')


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    show_count = models.IntegerField(default=0)
    done = models.BooleanField('task done', default=False)
    creation_date = models.DateTimeField('creation date', default=datetime.now)
    update_date = models.DateTimeField('updated date', default=datetime.now)
    deleted = models.BooleanField(default=False)
    rep_task = models.ForeignKey(
        RepTask,
        on_delete=models.CASCADE,
        unique_for_date='updated_date',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["done", "update_date"]
        indexes = [
            models.Index(fields=['user', 'done']),
        ]
        index_together = ['user', 'done', 'update_date']

    def __str__(self):
        return f'{self.user.username} | {self.text} | repeatable: {bool(self.rep_task)}'

    def _update_missed_tasks(self) -> None:
        """
        update all tasks that are viewed before current task
        """
        # TODO need to save tasks order somehow
        Task.objects.filter(
            done=False,
            update_date__lte=self.update_date,
            user=self.user,
            deleted=False
        ).update(update_date=datetime.now(), show_count=F("show_count") + 1)

    def update_task(self, update: dict) -> None:
        self._update_missed_tasks()
        for k, v in update.items():
            setattr(self, k, v)
        self.update_date = datetime.now()
        self.save()

    def delete_task(self) -> None:
        self._update_missed_tasks()
        self.deleted = True
        self.save()
