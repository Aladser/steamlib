# Generated by Django 5.1.4 on 2025-01-29 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_game_is_free'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='short_description',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Резюме'),
        ),
    ]
