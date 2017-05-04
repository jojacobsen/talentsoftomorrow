# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 08:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0010_auto_20170407_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaire',
            name='language',
        ),
        migrations.AddField(
            model_name='question',
            name='footer_da',
            field=models.TextField(blank=True, help_text='Footer rendered below the question interpreted as textile', null=True, verbose_name='Footer'),
        ),
        migrations.AddField(
            model_name='question',
            name='footer_de',
            field=models.TextField(blank=True, help_text='Footer rendered below the question interpreted as textile', null=True, verbose_name='Footer'),
        ),
        migrations.AddField(
            model_name='question',
            name='footer_en',
            field=models.TextField(blank=True, help_text='Footer rendered below the question interpreted as textile', null=True, verbose_name='Footer'),
        ),
        migrations.AddField(
            model_name='question',
            name='input_placeholder_da',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='input_placeholder_de',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='input_placeholder_en',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='text_da',
            field=models.TextField(blank=True, null=True, verbose_name='Text'),
        ),
        migrations.AddField(
            model_name='question',
            name='text_de',
            field=models.TextField(blank=True, null=True, verbose_name='Text'),
        ),
        migrations.AddField(
            model_name='question',
            name='text_en',
            field=models.TextField(blank=True, null=True, verbose_name='Text'),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='name_da',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='name_de',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='name_en',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='short_description_da',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='short_description_de',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='short_description_en',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='heading_da',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='heading_de',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='heading_en',
            field=models.CharField(max_length=64, null=True),
        ),
    ]