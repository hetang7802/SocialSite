# Generated by Django 3.2.5 on 2022-05-20 05:01

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='user'),
        ),
    ]
