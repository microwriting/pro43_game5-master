from django.db import models
# from authapp.models import User
from django.contrib.auth.models import User

from pro43_game5 import settings


class SlotMachine(models.Model):
    slot = models.CharField(max_length=255)
    game_count = models.IntegerField(default=0)
    medal = models.IntegerField(default=0, verbose_name='medal')

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.slot


class History(models.Model):
    # user = models.ForeignKey(User, verbose_name='slot_user', on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    history = models.IntegerField(default=0)
    slot_number = models.ForeignKey(SlotMachine, verbose_name='slot_number', on_delete=models.PROTECT)
    medals = models.PositiveIntegerField(default=0, verbose_name='medals')
    turbo2 = models.PositiveIntegerField(default=0, verbose_name='turbo2')
    deposit = models.BooleanField(default=False, verbose_name="deposit")


class GraphHistory1(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    player_history = models.IntegerField(default=0)
    slot = models.PositiveIntegerField()
    game = models.PositiveIntegerField(default=0)
    medal = models.PositiveIntegerField(default=0)


class GraphHistory2(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    player_history2 = models.PositiveIntegerField(default=0)
    # user = models.ForeignKey(Profile, verbose_name='slot_user', on_delete=models.PROTECT)
    slot = models.PositiveIntegerField()
    game = models.PositiveIntegerField(default=0)
    medal = models.PositiveIntegerField(default=0)
