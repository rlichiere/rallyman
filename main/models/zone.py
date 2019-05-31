# -*- coding: utf-8 -*-
from django.db import models

from ..core import constants


class Zone(models.Model):
    name = models.CharField(help_text='Letter that defines the zone.',
                            max_length=1)
    surface = models.CharField(help_text='Surface of the zone.',
                               max_length=16,
                               choices=constants.ZoneSurfaces.as_choices())
    file = models.CharField(help_text='File of the zone.',
                            max_length=200,
                            null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.name, self.surface)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if hasattr(self, 'id') and self.id is None:
            self.file = '%s_%s.jpg' % (str(self.name).lower(), str(self.surface).lower())

        super(Zone, self).save(force_insert=force_insert, force_update=force_update, using=using,
                               update_fields=update_fields)

