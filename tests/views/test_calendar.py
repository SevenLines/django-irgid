import json

from excursions.models import ExcursionCalendar
from tests import BaseTestCase


class ExcursionCalendarTestCase(BaseTestCase):
    def test_calendar_item_create(self):
        with self.login():
            r2 = self.api("calendar_update", {
                'items': json.dumps([
                    {
                        'year': 2017,
                        'month': 1,
                        'day': 1,
                        'description': "1",
                    },
                    {
                        'year': 2017,
                        'month': 1,
                        'day': 2,
                        'description': "2",
                    },
                    {
                        'year': 2017,
                        'month': 2,
                        'day': 1,
                        'description': "3",
                    },
                    {
                        'year': 2018,
                        'month': 2,
                        'day': 1,
                        'description': "4",
                    },
                ])
            }, ajax=True, post=True)

            self.assertEqual(4, ExcursionCalendar.objects.count())

        r = self.api("calendar", {
            'year': 2017,
            'month': 1,
        })

        self.api("calendar", {
            'year': 2017,
            'month': 2,
        })

        self.api("calendar", {
            'year': 2018,
            'month': 1,
        })
