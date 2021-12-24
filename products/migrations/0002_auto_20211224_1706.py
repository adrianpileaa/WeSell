# Generated by Django 3.2.7 on 2021-12-24 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='picture',
            field=models.ImageField(upload_to='category_images/'),
        ),
        migrations.AlterField(
            model_name='product_image',
            name='image',
            field=models.ImageField(upload_to='product_images/'),
        ),
    ]
