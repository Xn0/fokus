from django.contrib import admin
from .models import Task, RepTask


admin.site.register([Task, RepTask])