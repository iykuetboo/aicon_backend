# Generated by Django 4.1.2 on 2022-10-20 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservation_id', models.CharField(max_length=128, primary_key=True, serialize=False, unique=True)),
                ('prompt', models.TextField(blank=True, default='')),
                ('state', models.IntegerField(choices=[(0, 'inprocessing'), (1, 'completed'), (-1, 'desabled')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('input_tags', models.ManyToManyField(to='aiconapi.tag')),
            ],
        ),
        migrations.CreateModel(
            name='GeneratedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_id', models.IntegerField(default=None)),
                ('img_idx', models.IntegerField(default=None)),
                ('image', models.ImageField(upload_to='img/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ganarated_image', to='aiconapi.reservation')),
            ],
        ),
    ]
