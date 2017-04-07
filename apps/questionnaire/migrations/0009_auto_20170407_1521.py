# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-07 15:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0008_auto_20170331_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('open', 'Open: A simple one line input box'), ('open-textfield', 'Textfield: A box for lengthy answers'), ('range', 'Range: A range of options from which can be chosen'), ('number', 'Number: A number'), ('comment', 'Comment: Not a question, but only a comment displayed to the user')], max_length=50),
        ),
        migrations.AlterField(
            model_name='submission',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
