from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from .models import History, Info
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class InfoForm(forms.ModelForm):
    # widget is for drop down menu which is currently done on the template
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    patient_name = forms.CharField(max_length=120)
    # doctor = forms.CharField(max_length=120)
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}))

    class Meta:
        model = Info
        fields = ('date', 'patient_name', 'doctor', 'time',)

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", 'password1', 'password2')

    def save(self, commit = True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ('name', 'img')


    