# Generated by Django 5.0 on 2024-02-24 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DM_APP', '0010_product_packing_cost_product_tax'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('discount', models.IntegerField()),
            ],
        ),
    ]