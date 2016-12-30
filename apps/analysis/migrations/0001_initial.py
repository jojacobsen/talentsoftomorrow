# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-30 15:02
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django_measurement.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KhamisRoche',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField()),
                ('predicted_height', django_measurement.models.MeasurementField(measurement_class='Distance')),
                ('meta', django.contrib.postgres.fields.jsonb.JSONField(default={})),
            ],
        ),
    ]