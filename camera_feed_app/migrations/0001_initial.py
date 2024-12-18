# Generated by Django 5.1.4 on 2024-12-17 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machines', to='camera_feed_app.cluster')),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ip_address', models.CharField(max_length=15)),
                ('port', models.IntegerField(default=554)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('machine', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='cameras', to='camera_feed_app.machine')),
            ],
        ),
    ]
