# Generated by Django 4.1.2 on 2022-10-20 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aiconapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatedimage',
            name='request_id',
            field=models.CharField(default=None, max_length=128),
        ),
    ]
