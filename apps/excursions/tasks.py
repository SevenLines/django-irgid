# coding=utf-8
import traceback

from celery.task import task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.utils import translation
from django.template.loader import render_to_string
from django.utils.translation import activate, ugettext_lazy as _

from custom_settings.models import Setting
from excursions.models import ExcursionAppointment


def send_appointment_func(appointment_pk, language):
    with translation.override(language):
        address = filter(
            None,
            Setting.objects.get_value('email_for_appointments').split(',')
        )

        if not address:
            return

        with transaction.atomic():
            appointment = ExcursionAppointment.objects.get(pk=appointment_pk)
            try:
                mail = EmailMultiAlternatives(
                    u"Заявка №{} на сайте irgid.ru".format(appointment.id),
                    u"ФИО: {full_name} | Телефон: {phone} |  email: {email} | {comment}".format(
                        **appointment.__dict__),
                    settings.EMAIL_HOST_USER,
                    address
                )
                mail.attach_alternative(render_to_string("emails/appointment.html", {
                    'appointment': appointment
                }), "text/html")
                mail.send()

                if appointment.email:
                    mail = EmailMultiAlternatives(
                        _(u"Заявка №{} на сайте irgid.ru").format(appointment.id),
                        _(u"ФИО: {full_name} | Телефон: {phone} |  email: {email} | {comment}").format(
                            **appointment.__dict__),
                        settings.EMAIL_HOST_USER,
                        [appointment.email, ]
                    )
                    mail.attach_alternative(render_to_string("emails/appointment_client.html", {
                        'appointment': appointment
                    }), "text/html")
                    mail.send()

            except Exception as e:
                traceback.print_exc()
            else:
                appointment.sended = True
                appointment.save()


@task(ignore_result=True)
def send_appointment(appointment_pk, language="ru"):
    send_appointment_func(appointment_pk, language)