from django import forms
from PetPhotos.models import Category, Pet, Picture, Comment
from django.contrib.auth.models import User
from django.utils import timezone


"""
    CategoryForm form creates a Category model instance, requesting the name of the category
"""


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    creation_date = timezone.now()
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


"""
    PetForm form creates a Pet model instance, requesting the name of the pet and picture
"""


class PetForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Pet Name")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Pet
        fields = ('name', 'picture')


"""
    PictureForm form creates a Picture model instance, requesting the picture and the name of the category it will 
    belong to
"""


class PictureForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'), label='Select Category')
    creation_date = timezone.now()

    class Meta:
        model = Picture
        fields = ('category', 'picture')


"""
    UserForm form creates a User model instance, requesting the username, email, and password
"""


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


"""
    CommentForm form creates a Comment model instance, requesting the body of the comment
"""


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.TextInput(attrs={'size': 80}))
    creation_date = timezone.now()

    class Meta:
        model = Comment
        fields = ('comment',)
