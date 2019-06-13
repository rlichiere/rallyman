# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from ..core.const.lobby.rallies import RallyStatus


class Rally(models.Model):
    label = models.CharField(help_text='Human readable name of the rally. 200 characters max.',
                             max_length=200)
    created_at = models.DateTimeField(help_text='Creation date of the rally.',
                                      auto_now_add=True)
    opened_at = models.DateTimeField(help_text='Opening date of the rally.',
                                     auto_created=True)
    started_at = models.DateTimeField(help_text='Start date of the rally.',
                                      null=True,
                                      blank=True)
    finished_at = models.DateTimeField(help_text='Finish date of the rally.',
                                       null=True,
                                       blank=True)
    status = models.CharField(help_text='Status of the rally.',
                              max_length=16,
                              choices=RallyStatus.as_choices(),
                              default=RallyStatus.get_default())
    creator = models.ForeignKey(help_text='Creator of the rally.',
                                to=User)

    is_persisting = models.BooleanField(help_text='A persisting rally reopens automatically when finished.'
                                                  'This option can only be enabled by an administrator',
                                        default=False)

    class Meta:
        verbose_name_plural = "rallies"

    def __str__(self):
        return self.label
