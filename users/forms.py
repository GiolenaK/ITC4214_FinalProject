from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from users.models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()


#Model that we want the above form to interact with
    class Meta:
        model = User #when it validates create new user
        fields = ['username', 'email', 'password1', 'password2'] #fields shown on the form


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']