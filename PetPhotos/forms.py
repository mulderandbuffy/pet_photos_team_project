from django import forms
from django.http import request
from PetPhotos.models import Category, UserProfile, Pet, Picture
from django.contrib.auth.models import User
from django.utils import timezone


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    creation_date = timezone.now()
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class PetForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Pet Name")
    picture = forms.ImageField()
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Pet
        fields = ('name',)


class PictureForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    picture = forms.ImageField()
    creation_date = timezone.now()

    class Meta:
        model = Picture
        fields = ('name',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', )
