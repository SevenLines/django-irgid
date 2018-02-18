from django.core.management import BaseCommand
from django.db import connections, connection
from django.db.models import F

from excursions.models import Excursion, ExcursionCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("""
            UPDATE excursions_excursion
            SET title_ru = title, short_description_ru = short_description, description_ru = description,published_ru = published
            """)

            cursor.execute("""
            UPDATE excursions_excursioncategory
            SET title_ru = title, description_ru = description,visible_ru = visible
            """)

            cursor.execute("""
            UPDATE custom_settings_textsetting
            SET value_ru = value
            """)
