# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 07:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0012_auto_20170428_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='text_da',
            field=models.CharField(max_length=200, null=True, verbose_name='Choice Text'),
        ),
        migrations.AddField(
            model_name='choice',
            name='text_de',
            field=models.CharField(max_length=200, null=True, verbose_name='Choice Text'),
        ),
        migrations.AddField(
            model_name='choice',
            name='text_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Choice Text'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('open', 'Open: A simple one line input box'), ('open-textfield', 'Textfield: A box for lengthy answers'), ('choice', 'Choice: A list of choices to choose from'), ('range', 'Range: A range of options from which can be chosen'), ('number', 'Number: A number'), ('comment', 'Comment: Not a question, but only a comment displayed to the user')], max_length=50),
        ),
    ]
