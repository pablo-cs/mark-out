# Generated by Django 4.2.1 on 2023-12-21 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wrestling_matches', '0002_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagteam',
            name='wrestlers',
            field=models.ManyToManyField(related_name='tag_teams', to='wrestling_matches.wrestler'),
        ),
    ]
