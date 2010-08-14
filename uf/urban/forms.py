from django.forms.models import modelformset_factory
from django import forms
from urban.models import *
from django.forms import ModelForm

IntervalFormSet = modelformset_factory(Interval)



class SignUpForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget= forms.PasswordInput)

class LogInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

class VenueForm(ModelForm):
    class Meta:
        model = Venue