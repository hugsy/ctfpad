# Generated by Django 3.1.3 on 2021-01-13 20:21

import ctfpad.helpers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctfpad', '0003_auto_20210113_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctf',
            name='note_id',
            field=models.CharField(blank=True, default=ctfpad.helpers.create_new_note, max_length=38),
        ),
    ]