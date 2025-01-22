from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from app.models import Answer

class LoginForm(forms.Form):
    username = forms.CharField(min_length=2)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        return self.cleaned_data['username'].lower().strip()

class SignupForm(forms.ModelForm):
    username = forms.CharField(min_length=2)
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        data = super().clean()

        if data['password'] != data['password_confirmation']:
            raise ValidationError('Passwords do not match')

        return data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password'])

        user.save()
        return user

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
