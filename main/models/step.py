# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from ..core.const.rally import StepStatus
from .rally import Rally


class GameStep(models.Model):
    rally = models.ForeignKey(help_text='Rally to which the step applies',
                              to=Rally)

    index = models.IntegerField(help_text='Index of the step in the rally',
                                default=1)

    player = models.ForeignKey(help_text='Player to whom the step applies',
                               to=User)

    started_at = models.DateTimeField(help_text='Start date of the step',
                                      auto_now_add=True)

    status = models.CharField(help_text='Status of the step',
                              max_length=16,
                              choices=StepStatus.as_choices(),
                              default=StepStatus.get_default())

    def __str__(self):
        return '%s - %s - %s - %s' % (self.rally.id, self.index, self.player.get_full_name(), self.status)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(GameStep, self).save(force_insert, force_update, using, update_fields)

        self.index = GameStep.objects.filter(rally=self.rally).count()
