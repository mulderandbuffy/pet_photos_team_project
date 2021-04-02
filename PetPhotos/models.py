from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Pet(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='images', blank=True)
    about_pet = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='images', blank=True)

    # last login - add and check after user interface is done------------------------------------------------

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Picture(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='pictures', blank=False)  # upload to the file---------------------------
    creation_date = models.DateTimeField(auto_now_add=True)

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
