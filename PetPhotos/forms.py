from django import forms
from PetPhotos.models import Category, Pet, Picture, Comment
from django.contrib.auth.models import User
from django.utils import timezone


"""
    CategoryForm form creates a Category model instance, requesting the name of the category
"""


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name. Max 128 characters.", widget=forms.TextInput(attrs={'class': 'form-control', 
                                                    'placeholder': 'Category Name'}))
    creation_date = timezone.now()
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


"""
    PetForm form creates a Pet model instance, requesting the name of the pet and picture
"""


class PetForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the pet name. Max 128 characters.", widget=forms.TextInput(attrs={'class':'form-control', 
                                                        'placeholder': 'Pet Name'}))
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Pet
        fields = ('name', 'picture')
        widgets = {'picture': forms.FileInput(attrs={'class': 'btn btn-outline-secondary'})}


"""
    PictureForm form creates a Picture model instance, requesting the picture and the name of the category it will 
    belong to
"""


class PictureForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('name'), label='Select Category', 
                    widget=forms.Select(attrs={'class': 'form-control', 'placeholder':'Category'}), help_text="Choose a Category")
    creation_date = timezone.now()

    class Meta:
        model = Picture
        fields = ('category', 'picture')
        widgets = {'picture': forms.FileInput(attrs={'class': 'btn btn-outline-secondary'})}


"""
    UserForm form creates a User model instance, requesting the username, email, and password
"""


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}), label='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {'username': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username - 150 characters or fewer. Letters, digits and @/./+/-/_ only', 'aria-describedby':'usernameHelp'}),
                    'email': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Email Address', 'aria-describedby':'usernameHelp'})}
        labels = {'username': '', 'email': ''}
        help_texts = {'username': ''}


"""
    CommentForm form creates a Comment model instance, requesting the body of the comment
"""


class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'size': 80, 'class':'form-control', 'placeholder':'Comment'}),
                              help_text="Max 300 characters.")
    creation_date = timezone.now()

    class Meta:
        model = Comment
        fields = ('comment',)
