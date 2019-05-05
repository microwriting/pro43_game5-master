from django.contrib import admin
from .models import SlotMachine,History


class MyModelAdmin(admin.ModelAdmin):
    fields = ('slot', 'game_count', 'medal')
    readonly_fields = ('game_count',)

admin.site.register(SlotMachine, MyModelAdmin)

