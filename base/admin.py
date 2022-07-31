from django.contrib import admin
from base.models import Topic, Blog, Comment

# Register your models here.

admin.site.register(Topic)
admin.site.register(Blog)
admin.site.register(Comment)
