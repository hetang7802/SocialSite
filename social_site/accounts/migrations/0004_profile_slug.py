# Generated by Django 3.2.5 on 2022-05-20 04:55

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_profile_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='NULL', editable=False, populate_from='user'),
        ),
    ]