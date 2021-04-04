from django import forms
from PetPhotos.models import Category, Pet, Picture
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
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Pet
        fields = ('name', 'picture')


class PictureForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'), label='Select Category')
    creation_date = timezone.now()

    class Meta:
        model = Picture
        fields = ('category', 'picture')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

