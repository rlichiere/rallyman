# -*- coding: utf-8 -*-
from django.db import models

from ..core.renderers import CarSkinRenderer


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

    @classmethod
    def availableSkins(cls):
        return CarSkin.objects.all()

    @classmethod
    def as_choices(cls, qs_carskins=None):
        _qs = qs_carskins
        if _qs is None:
            _qs = cls.availableSkins()
        return [(_carSkin[0], _carSkin[1]) for _carSkin in _qs.values_list('id', 'label')
                                                              .order_by('label')]

    def render(self, direction=None):
        return CarSkinRenderer(self).as_image(direction)
