# Generated by Django 3.1.7 on 2021-04-03 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PetPhotos', '0019_remove_pet_about_pet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
