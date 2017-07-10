from django.forms import ModelForm
from django.forms import forms
from .models import Person
from .widgets import DatePickerWidget


class ContactForm(ModelForm):
    class Meta:
        model = Person
        widgets = {
            'dob': DatePickerWidget(
                attrs={"yearRange": '-50:'}
            )
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
        return othercontacts
