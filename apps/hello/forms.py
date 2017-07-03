from django.forms import ModelForm
from django.forms import forms
from django.core.validators import validate_email
from django_hello_world.hello.models import Person
from django_hello_world.hello.widgets import DatePickerWidget


class ContactForm(ModelForm):
    class Meta:
        model = Person
        widgets = {
            'birthday': DatePickerWidget(
            params="dateFormat: 'yy-mm-dd', changeYear: true, yearRange: '-50:'",
            attrs={'class': 'datepicker'})
        }

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if len(bio) > 140:
            raise forms.ValidationError("Max length 140 characters!")
        return bio

    def clean_othercontacts(self):
        othercontacts = self.cleaned_data['othercontacts']
        if len(othercontacts) > 140:
            raise forms.ValidationError("Max length 140 characters!")
        return other
