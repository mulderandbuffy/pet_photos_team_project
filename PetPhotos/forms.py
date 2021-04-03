from django import forms
from PetPhotos.models import Category, UserProfile
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the category name.")
    creation_date = forms.DateTimeField(widget=forms.HiddenInput())
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
       model = User
       fields = ('username', 'email', 'password', )
       
class UserProfileForm(forms.ModelForm):
    class Meta:
       model = UserProfile
       fields = ('picture',)
