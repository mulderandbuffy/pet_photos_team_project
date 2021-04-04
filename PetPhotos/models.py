import uuid
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify



class Pet(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='images', blank=True)
    slug = models.SlugField(unique=True, default='')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Pet, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, unique=True, blank=False, primary_key=True)
    email = models.CharField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.user.username


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


class Picture(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField(default=0)  # get rid of this + update population script ------------------------
    likes = models.ManyToManyField(User, related_name='picture_like')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='images', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=300, blank=None)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
