# -*- coding: utf-8 -*-
from django.contrib import admin

from .core import renderers
from . import models


class CarSkinAdmin(admin.ModelAdmin):
    list_display = ('label', 'image', 'file')

    readonly_fields = ('image', )

    @staticmethod
    def image(instance):
        return renderers.CarSkinRenderer(instance).as_image()


class GameStepAdmin(admin.ModelAdmin):
    list_display = ('rally', 'index', 'player', 'status', 'started_at')
    list_filter = ('rally', 'player', 'status', )

    readonly_fields = ('started_at', )


class RallyAdmin(admin.ModelAdmin):
    list_display = ('label', 'status', 'creator', 'created_at', 'opened_at', 'started_at', 'finished_at',
                    'participants_count', 'stages_count', 'is_persisting')
    list_filter = ('status', 'creator', )
    search_fields = ('label', )

    readonly_fields = ('created_at', 'stages', 'participants', )
    fieldsets = (
        (None, {
            'fields': ('label', 'created_at', 'opened_at', 'started_at', 'finished_at',
                       'status', 'creator', 'is_persisting')
        }),
        ('Stages', {
            'fields': ('stages', 'participants', )
        }),
    )

    @staticmethod
    def participants_count(instance):
        return models.Participation.objects.filter(rally=instance).count()

    @staticmethod
    def stages_count(instance):
        return models.Stage.objects.filter(rally=instance).count()

    @staticmethod
    def stages(instance):
        return renderers.RallyStagesRenderer(instance).as_table()

    @staticmethod
    def participants(instance):
        return renderers.RallyParticipationsRenderer(models.Participation, instance).as_table()


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('rally', 'player', 'turn_position', 'car', )
    list_filter = ('rally', 'player', )
    search_fields = ('rally', 'player', )

    @staticmethod
    def car(instance):
        return renderers.CarSkinRenderer(instance.car_skin).as_image()


class StageAdmin(admin.ModelAdmin):
    list_display = ('rally', 'position_in_roadbook', 'roadbook_as_label', )
    list_filter = ('rally', )
    search_fields = ('rally', )

    readonly_fields = ('stages', )
    fieldsets = (
        (None, {
            'fields': ('rally', 'position_in_roadbook', 'roadbook', 'has_assistance', )
        }),
        ('Roadbook', {
            'fields': ('stages', )
        }),
    )

    @staticmethod
    def stages(instance):
        _roadbook = instance.get_roadbook
        return renderers.RoadbookRenderer(_roadbook).as_list()


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'surface', )
    list_filter = ('name', 'surface', )


admin.site.register(models.CarSkin, CarSkinAdmin)
admin.site.register(models.GameStep, GameStepAdmin)
admin.site.register(models.Rally, RallyAdmin)
admin.site.register(models.Participation, ParticipationAdmin)
admin.site.register(models.Stage, StageAdmin)
admin.site.register(models.Zone, ZoneAdmin)
