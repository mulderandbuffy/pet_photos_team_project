# Generated by Django 3.1.7 on 2021-04-01 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PetPhotos', '0004_auto_20210401_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='login',
        ),
    ]
