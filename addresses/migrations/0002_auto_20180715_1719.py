# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-15 11:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='address_line_1',
            field=models.CharField(default='a', max_length=120),
            preserve_default=False,
        ),
    ]