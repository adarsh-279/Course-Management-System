from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('student', 'Student'), ('admin', 'Admin')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']