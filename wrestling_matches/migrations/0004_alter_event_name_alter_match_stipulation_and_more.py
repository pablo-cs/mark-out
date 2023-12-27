# Generated by Django 4.2.1 on 2023-12-27 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wrestling_matches', '0003_wrestler_img_src'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='match',
            name='stipulation',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='venue',
            name='location',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
