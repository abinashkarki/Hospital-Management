from management.views import appointment
from django.contrib import admin
from .models import Doctor, History, Info
# Register your models here.
admin.site.register(Info)
admin.site.register(Doctor)
admin.site.register(History)