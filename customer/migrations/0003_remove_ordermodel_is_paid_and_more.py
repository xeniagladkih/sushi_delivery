# Generated by Django 4.2 on 2023-04-08 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_rename_product_ordermodel_menu_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='is_shipped',
        ),
    ]