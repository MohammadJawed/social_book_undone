from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import UploadedFile

from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()	
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email","username","first_name","last_name",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email","username","first_name","last_name",)

class UploadedFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'description', 'file', 'visibility', 'cost', 'year_published']