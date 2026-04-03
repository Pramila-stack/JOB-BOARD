from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from job.models import Application, Job, Profile



class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title","description","company","location","salary"]

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["cv","cover_letter"]

