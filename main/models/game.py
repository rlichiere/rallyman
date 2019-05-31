# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from ..core.constants import GameStatus


class Game(models.Model):
    label = models.CharField(help_text='Human readable name of the game. 200 characters max.',
                             max_length=200)
    created_at = models.DateTimeField(help_text='Creation date of the game.',
                                      auto_now_add=True)
    opened_at = models.DateTimeField(help_text='Opening date of the game.',
                                     auto_created=True)
    started_at = models.DateTimeField(help_text='Start date of the game.',
                                      null=True,
                                      blank=True)
    finished_at = models.DateTimeField(help_text='Finish date of the game.',
                                       null=True,
                                       blank=True)
    status = models.CharField(help_text='Status of the game.',
                              max_length=16,
                              choices=GameStatus.as_choices(),
                              default=GameStatus.get_default())
    creator = models.ForeignKey(help_text='Creator of the game.',
                                to=User)

    def __str__(self):
        return self.label
