# Generated by Django 5.0 on 2024-02-14 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DM_APP', '0002_banner_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner_area',
            name='link',
            field=models.CharField(max_length=200, null=True),
        ),
    ]