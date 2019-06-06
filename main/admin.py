# -*- coding: utf-8 -*-
from django.contrib import admin

from .core.renderers import CarSkinRenderer, RallyStagesRenderer, RoadbookRenderer
from .models import CarSkin, Rally, Participation, Stage, Zone


class CarSkinAdmin(admin.ModelAdmin):
    list_display = ('label', 'image', 'file')

    readonly_fields = ('image', )

    @staticmethod
    def image(instance):
        return CarSkinRenderer(instance).as_image()


class RallyAdmin(admin.ModelAdmin):
    list_display = ('label', 'status', 'creator', 'created_at', 'opened_at', 'finished_at')
    list_filter = ('status', 'creator', )
    search_fields = ('label', )

    readonly_fields = ('created_at', 'stages', )
    fieldsets = (
        (None, {
            'fields': ('label', 'created_at', 'opened_at', 'started_at', 'finished_at', 'status', 'creator', )
        }),
        ('Stages', {
            'fields': ('stages', )
        }),
    )

    @staticmethod
    def stages(instance):
        return RallyStagesRenderer(instance).as_table()


class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('rally', 'player', 'turn_position', 'car', )
    list_filter = ('rally', 'player', )
    search_fields = ('rally', 'player', )

    @staticmethod
    def car(instance):
        return CarSkinRenderer(instance.car_skin).as_image()


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
        return RoadbookRenderer(_roadbook).as_list()


class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'surface', )
    list_filter = ('name', 'surface', )


admin.site.register(CarSkin, CarSkinAdmin)
admin.site.register(Rally, RallyAdmin)
admin.site.register(Participation, ParticipationAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Zone, ZoneAdmin)
