import uuid
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


"""
    Pet model is made up of: name, reference to the owner user, picture of the animal, and slug which is created
    internally when we create an instance of the model
"""


class Pet(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='images', blank=False)
    slug = models.SlugField(unique=True, default='')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Pet, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


"""
    UserProfile model is made up of: user, username, and email
"""


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, unique=True, blank=False, primary_key=True)
    email = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.user.username


"""
    Category model is made up of: name, the date it was created, and slug which is created internally when we create 
    an instance of the model
"""


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, default='')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


"""
    Picture model is made up of: id, number of references to users who liked this picture, creator reference,
    category reference, picture field representing the picture itself, and the date it was created
"""


class Picture(models.Model):
    id = models.AutoField(primary_key=True)
    likes = models.ManyToManyField(User, related_name='picture_like')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='images', blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return str(self.id)


"""
    Comment model is made up of: id, comment body, creator reference, picture reference, and the date it was created
"""


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=300, blank=None)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
