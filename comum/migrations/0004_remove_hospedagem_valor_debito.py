# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-23 11:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comum', '0003_auto_20180223_0723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospedagem',
            name='valor_debito',
        ),
    ]