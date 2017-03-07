# coding=utf-8
import json

from django.urls.base import reverse

from excursions.models import ExcursionCalendar, Excursion
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

    def test_replace_title_in_text_with_links(self):
        title1 = u"1) Самая лучшая экскурсия от 240 руб."
        ex1 = Excursion.objects.create(
            title=title1
        )
        url1 = reverse('excursions:item', args=[ex1.pk, ex1.title])

        title2 = u"Самая (лучшая) экскурсия.? от"
        ex2 = Excursion.objects.create(
            title=title2
        )
        url2 = reverse('excursions:item', args=[ex2.pk, ex2.title])

        comment = u"Проснулся я ночью часа в два {{{title1}}} \n" \
                  u"провелась у меня {{{title2}}}, {{{title2}}}{{{title1}}}".format(title1=title1,
                                                                                    title2=title2)
        expected_comment = u"Проснулся я ночью часа в два <a href=\"{url1}\">{title1}</a> \n" \
                           u"провелась у меня <a href=\"{url2}\">{title2}</a>, " \
                           u"<a href=\"{url2}\">{title2}</a><a href=\"{url1}\">{title1}</a>".format(
            url1=url1, url2=url2, title1=title1, title2=title2)
        result = ExcursionCalendar.replace_with_links(comment)

        self.assertEqual(expected_comment, result)

        ex = ExcursionCalendar.objects.create(
            comment=comment
        )
        self.assertEqual(ex.comment_rendered, ExcursionCalendar.replace_with_links(ex.comment))

