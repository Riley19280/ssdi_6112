from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class DatasetUploadForm(forms.Form):
    dataset_name = forms.CharField(max_length=32)
    file = forms.FileField()
