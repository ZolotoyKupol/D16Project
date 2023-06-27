from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Person, Ad, Response, NewsletterSubscriber


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Person
        fields = ('username', 'email', 'password1', 'password2')


class ConfirmationForm(forms.Form):
    code = forms.CharField(label='Confirmation Code', max_length=6)


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'text', 'category']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']


class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']