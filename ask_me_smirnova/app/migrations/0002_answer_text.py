# Generated by Django 5.1 on 2025-01-22 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='text',
            field=models.CharField(default=2, max_length=2047),
            preserve_default=False,
        ),
    ]
