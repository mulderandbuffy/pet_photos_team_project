from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone
import uuid


class Pet(models.Model):
    id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)  # URLS??
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __init__(self):
        super(Pet, self).__init__()
        self.id = str(uuid.uuid4())

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)
    website = models.URLField(blank=True)  # URLS??
    picture = models.ImageField(upload_to='profile_images', blank=True)
    login = models.DateField(auto_now=True) # login get date

    def __init__(self):
        super(Pet, self).__init__()
        self.id = str(uuid.uuid4())

    def __str__(self):
        return self.user.username


class Category(models.Model):
    id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __init__(self):
        super(Pet, self).__init__()
        self.id = str(uuid.uuid4())

    def __str__(self):
        return self.name


class Picture(models.Model):
    id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)
    rating = models.IntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __init__(self):
        super(Pet, self).__init__()
        self.id = str(uuid.uuid4())

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4, primary_key=True)
    comment = models.CharField(max_length=300)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=timezone.now)

    def __init__(self):
        super(Pet, self).__init__()
        self.id = str(uuid.uuid4())

    def __str__(self):
        return self.name
