from django import forms
from PetPhotos.models import Category, Pet


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the category name.")
    creation_date = forms.DateTimeField(widget=forms.HiddenInput())
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class PetForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
    help_text="Enter your pet's name")
    picture = forms.ImageField(help_text="Upload a photo of your pet")
    slug = forms.CharField(widget=forms.HiddenInput(), required = False)


    class Meta:
        model = Pet
        fields = ('name', 'picture')
