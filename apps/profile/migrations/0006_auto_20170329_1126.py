# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 11:26
from __future__ import unicode_literals

from django.db import migrations, models
import profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0005_bodyfat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodyfat',
            name='body_fat',
            field=models.DecimalField(decimal_places=1, max_digits=4, validators=[profile.models.valid_pct]),
        ),
    ]
