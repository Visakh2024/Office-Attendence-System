from django import forms
from .models import Attendance
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _("Your username or password is incorrect."),
        'inactive': _("This account is inactive."),
    }

class CheckInForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['check_in_photo']

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['check_out_photo']
