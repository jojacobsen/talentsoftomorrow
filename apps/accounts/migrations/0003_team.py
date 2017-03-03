# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 08:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20161230_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('club', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.Club')),
                ('players', models.ManyToManyField(blank=True, to='accounts.Player')),
            ],
        ),
    ]
