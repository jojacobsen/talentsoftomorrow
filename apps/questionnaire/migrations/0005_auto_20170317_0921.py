# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0004_question_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
