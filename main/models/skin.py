# -*- coding: utf-8 -*-
from django.db import models


class CarSkin(models.Model):
    label = models.CharField(help_text='Human readable name of the skin. 32 characters max.',
                             max_length=32,
                             unique=True)
    file = models.CharField(help_text='File of the skin. 32 characters max.'
                                      ' The corresponding file must be placed in /static/main/car_skins/ folder.',
                            max_length=32,
                            unique=True)

    def __str__(self):
        return self.label
