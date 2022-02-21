from django.contrib import admin

from .models import ChatGroupUser, ChatGroups, Messages, emotions
# Register your models here.
admin.site.register((ChatGroupUser, ChatGroups, Messages, emotions))