# Generated by Django 4.1.2 on 2022-10-19 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('save_image', '0003_remove_generatedimage_image_generatedimage_img_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatedimage',
            name='image',
            field=models.ImageField(default=None, upload_to='img/'),
        ),
    ]