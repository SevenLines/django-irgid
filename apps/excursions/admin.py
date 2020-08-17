from django.contrib import admin

from excursions.models import ExcursionAppointment


@admin.register(ExcursionAppointment)
class ExcursionAppointmentAdmin(admin.ModelAdmin):
    ordering = ['-create_date']
    list_display = ('create_date', 'full_name', 'phone', 'email', 'comment')
