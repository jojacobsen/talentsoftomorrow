# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 10:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_phv_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bioage',
            name='method',
            field=models.CharField(choices=[('pre', 'Height Prediction'), ('phv', 'Peak Height Velocity')], default='pre', max_length=5),
        ),
        migrations.AddField(
            model_name='bioage',
            name='phv',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile.PHV'),
        ),
        migrations.AlterField(
            model_name='bioage',
            name='current_height',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile.Height'),
        ),
        migrations.AlterField(
            model_name='bioage',
            name='predicted_height',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile.PredictedHeight'),
        ),
    ]
