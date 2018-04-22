# coding=utf-8
from django.core import mail
from django.utils.translation import activate

from tests import BaseTestCase


class TestOrder(BaseTestCase):
    def test_set_order_default(self):
        r = self.api("appointment_create", {
            "email": "mmailm@mail.ru",
            "phone": "12345",
            "comment": "comment",
            "full_name": "full_name",
        }, post=True, ajax=True)
        self.assertEqual(2, len(mail.outbox))

        mail_item = mail.outbox[1]
        self.assertIn(u"ФИО", mail_item.body)
        self.assertIn(u"Телефон", mail_item.body)
        self.assertIn(u"email", mail_item.body)
        self.assertIn(u"comment", mail_item.body)

    def test_set_order_en(self):
        activate("en")
        r = self.api("appointment_create", {
            "email": "mmailm@mail.ru",
            "phone": "12345",
            "comment": "comment",
            "full_name": "full_name",
        }, post=True, ajax=True)
        self.assertEqual(2, len(mail.outbox))
        mail_item = mail.outbox[1]
        self.assertIn("Name", mail_item.body)
        self.assertIn("Phone", mail_item.body)
        self.assertIn("email", mail_item.body)
        self.assertIn("comment", mail_item.body)

