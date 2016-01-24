from django import forms
from django.forms import ModelForm
from filer.fields.image import AdminImageFormField
from excursions.models import Excursion, ExcursionAppointment

__author__ = 'm'


class ExcursionForm(forms.Form):
    img_preview = AdminImageFormField(label="img_preview",
                                      queryset=None,
                                      rel=Excursion,
                                      to_field_name="img_preview")


class ExcursionAppointmentForm(ModelForm):
    class Meta:
        model = ExcursionAppointment
        fields = ['email', 'phone', 'comment']
