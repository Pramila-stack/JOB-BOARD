from django.contrib import admin

from job.models import Application, Job, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(Application)