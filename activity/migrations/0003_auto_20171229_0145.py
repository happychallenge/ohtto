# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-29 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20171225_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('PL', 'Liked'), ('PC', 'Commented'), ('PC', 'Bucket'), ('TM', 'Theme'), ('IV', 'Invited')], max_length=2),
        ),
    ]