from django.contrib import admin

from .models import CallSession, KasaDakaUser


# Register your models here.


admin.site.register(CallSession)
admin.site.register(KasaDakaUser)
