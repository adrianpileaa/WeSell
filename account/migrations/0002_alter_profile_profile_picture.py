# Generated by Django 3.2.7 on 2021-12-24 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='images/default.png', max_length=255, upload_to='profile_pictures/'),
        ),
    ]
