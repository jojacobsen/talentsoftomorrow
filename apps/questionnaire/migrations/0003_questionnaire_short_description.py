# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0002_question_sort'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='short_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]