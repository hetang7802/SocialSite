from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile


class UserCreateForm(UserCreationForm):

    email = forms.EmailField()

    class Meta():
        fields = ['username','password1','password2','email']
        model = get_user_model()

        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)

            self.fields['username'].label = "Display Name"
            self.fields['email'].label = "Email Adress"

class ProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ['image','bio']
