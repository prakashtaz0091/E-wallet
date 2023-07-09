from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class UserRegistrationForm(UserCreationForm):
    # Customize additional fields if needed
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    # Specify the form layout using crispy-forms Layout
    helper = FormHelper()
    helper.layout = Layout(
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2',
        Submit('submit', 'Register')
    )
