from django.core.management.base import BaseCommand

from excursions.models import ExcursionCalendar


class Command(BaseCommand):
    def handle(self, *args, **options):
        for calendar in ExcursionCalendar.objects.all():
            calendar.save()