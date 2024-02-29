# Generated by Django 5.0 on 2024-02-18 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DM_APP', '0006_product_slug_alter_product_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterModelTable(
            name='product',
            table='DM_APP_Product',
        ),
    ]