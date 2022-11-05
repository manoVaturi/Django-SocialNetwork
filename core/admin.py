from django.contrib import admin
from .models import Room, Topic, Message

# Register your models here.

admin.site.register([Room, Topic, Message])
