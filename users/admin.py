from django.contrib import admin

from .models import (Project, Event, Function)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'full_name',
                    'legal_form',
                    'website',
                    'material_url',
                    'avatar_url',
                    'status',
                    'description',
                    'goal',
                    'result',
                    'slug',
                    'organization_id',
                    'user_id')
    search_fields = ('name', 'status')
    empty_value_display = '-пусто-'


class EventAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'avatar_url',
                    'status',
                    'description',
                    'date_start',
                    'date_end',
                    'project_id',
                    'slug',
                    'client_id',
                    'user_id')
    search_fields = ('name', 'status')
    empty_value_display = '-пусто-'


class FunctionAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'description',
                    'task',
                    'condition',
                    'event_id',
                    'client_id',
                    'slug')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Project, ProjectAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Function, FunctionAdmin)