from django.contrib import admin
from .models import Participant, Winner


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'get_user_email', 'status', 'registered_at', 'verified_at')
    list_filter = ('status', 'registered_at', 'verified_at')
    search_fields = ('user__email', 'user__full_name', 'user__phone')
    ordering = ('-registered_at',)
    readonly_fields = ('id', 'registered_at', 'verified_at', 'updated_at')

    fieldsets = (
        ('Usuario', {'fields': ('user',)}),
        ('Estado', {'fields': ('status',)}),
        ('Fechas', {'fields': ('registered_at', 'verified_at', 'updated_at')}),
        ('ID', {'fields': ('id',)}),
    )

    def get_user_name(self, obj):
        return obj.user.full_name

    get_user_name.short_description = 'Nombre'
    get_user_name.admin_order_field = 'user__full_name'

    def get_user_email(self, obj):
        return obj.user.email

    get_user_email.short_description = 'Email'
    get_user_email.admin_order_field = 'user__email'


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ('get_winner_name', 'get_winner_email', 'draw_date', 'is_notified', 'drawn_by')
    list_filter = ('is_notified', 'draw_date')
    search_fields = ('participant__user__email', 'participant__user__full_name')
    ordering = ('-draw_date',)
    readonly_fields = ('id', 'draw_date', 'notified_at', 'created_at', 'updated_at')

    fieldsets = (
        ('Ganador', {'fields': ('participant',)}),
        ('Sorteo', {'fields': ('draw_date', 'drawn_by')}),
        ('Notificación', {'fields': ('is_notified', 'notified_at')}),
        ('Notas', {'fields': ('notes',)}),
        ('Metadata', {'fields': ('id', 'created_at', 'updated_at')}),
    )

    def get_winner_name(self, obj):
        return obj.participant.user.full_name

    get_winner_name.short_description = 'Ganador'
    get_winner_name.admin_order_field = 'participant__user__full_name'

    def get_winner_email(self, obj):
        return obj.participant.user.email

    get_winner_email.short_description = 'Email'
    get_winner_email.admin_order_field = 'participant__user__email'