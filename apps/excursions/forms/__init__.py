from django import forms
from filer.fields.image import AdminImageFormField
from excursions.models import Excursion

__author__ = 'm'


class ExcursionForm(forms.Form):
    img_preview = AdminImageFormField(label="img_preview",
                                      queryset=None,
                                      rel=Excursion,
                                      to_field_name="img_preview")