# Generated by Django 3.1.7 on 2021-04-02 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PetPhotos', '0014_pet_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='slug',
        ),
    ]
