from django import forms
from django.contrib.auth.models import User
from .models import Course

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('student', 'Student'), ('admin', 'Admin')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'capacity', 'instructor']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }