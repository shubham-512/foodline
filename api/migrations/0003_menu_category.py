# Generated by Django 3.2 on 2021-05-01 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_product_order_dish'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
