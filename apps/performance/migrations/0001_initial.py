# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-12-30 15:02
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benchmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('benchmark', models.DecimalField(decimal_places=3, max_digits=6)),
                ('benchmark_bio', models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bio_age', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile.BioAge')),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('slug_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=2000)),
                ('precision', models.IntegerField(default=2, help_text='How many decimals should be shown in Webapp?')),
                ('upper_limit', models.DecimalField(decimal_places=10, help_text='Highest possible value.', max_digits=16)),
                ('lower_limit', models.DecimalField(decimal_places=10, help_text='Lowest possible value.', max_digits=16)),
                ('statistic_array', django.contrib.postgres.fields.jsonb.JSONField(default=[[], [], []], help_text='Use the following format (age, average, SD) with all the same length: [[9,10,11],[3,3.5,4],[2,2,2]].', validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(3)])),
                ('smaller_is_better', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=10, max_digits=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField()),
                ('description', models.CharField(blank=True, max_length=2000)),
                ('measurement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.Measurement')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(max_length=50)),
                ('system', models.CharField(choices=[('SI', 'Metric'), ('Imp', 'Imperial'), ('-', 'None')], max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='measurement',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.Unit'),
        ),
        migrations.AddField(
            model_name='benchmark',
            name='performance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='performance.Performance'),
        ),
    ]
