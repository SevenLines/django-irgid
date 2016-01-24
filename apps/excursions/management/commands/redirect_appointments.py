# coding=utf-8
from django.core.management import BaseCommand
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

from custom_settings.models import Setting
from excursions.models import ExcursionAppointment
import logging
import traceback

logger = logging.getLogger('excursions')

class Command(BaseCommand):
    help = 'redirect apointments to specified email'

    def handle(self, *args, **options):
        appointments = ExcursionAppointment.objects.filter(sended=False)

        address = filter(
            None,
            Setting.objects.get_value('email_for_appointments').split(',')
        )

        if not address:
            return

        for appointment in appointments:
            try:
                mail = EmailMultiAlternatives(
                    u"Заявка № {} на сайте irgid.ru".format(appointment.id),
                    u"Телефон: {phone} |  email: {email}\n{comment}".format(**appointment.__dict__),
                    settings.EMAIL_HOST_USER,
                    address
                )
                mail.attach_alternative(render_to_string("emails/appointment.html", {
                    'appointment': appointment
                }), "text/html")
                mail.send()
            except Exception as e:
                logger.error(traceback.format_exc())
            else:
                appointment.sended = True
                appointment.save()
