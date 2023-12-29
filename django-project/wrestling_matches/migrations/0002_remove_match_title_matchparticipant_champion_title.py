# Generated by Django 4.2.1 on 2023-12-25 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wrestling_matches', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='title',
        ),
        migrations.AddField(
            model_name='matchparticipant',
            name='champion',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('matches', models.ManyToManyField(related_name='titles', to='wrestling_matches.match')),
            ],
        ),
    ]