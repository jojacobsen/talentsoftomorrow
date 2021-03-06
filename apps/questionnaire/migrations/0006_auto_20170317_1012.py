# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0005_auto_20170317_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='input_placeholder',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='required',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('choice-yesno', 'Choice: Yes or No'), ('choice-yesnocomment', 'Choice & Comment: Yes or No with a chance to comment on the answer'), ('open', 'Open: A simple one line input box'), ('open-textfield', 'Textfield: A box for lengthy answers'), ('choice', 'Choice: A list of choices to choose from'), ('choice-freeform', 'Choice & Free Form: A list of choices with a chance to enter something else'), ('choice-multiple', 'Multiple Choice: A list of choices with multiple answers'), ('choice-multiple-freeform', 'Multiple Choice & Free Form: Multiple Answers with multiple user defined answers'), ('range', 'Range: A range of number from which one number can be chosen'), ('number', 'Number: A number'), ('comment', 'Not a question, but only a comment displayed to the user')], max_length=50),
        ),
    ]
